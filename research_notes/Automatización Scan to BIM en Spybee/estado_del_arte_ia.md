# State of the art (academic + open source) for automated point cloud → BIM/IFC (as of Nov 2026)

> Research context: notes for designing an in-house Scan-to-BIM pipeline (point cloud → semantic segmentation → instance/element extraction → parametric fitting → IFC/Revit). Date of research: 2026-11-02.
> **Method caveat:** in this session the hosts arxiv.org, huggingface.co, ncbi.nlm.nih.gov, copernicus.org (ISPRS), ec-3.org, dfki.de and alphaxiv.org could not be fetched (network allowlist). Primary pages were read directly only from github.com (READMEs, LICENSE files, GitHub repo metadata via `gh search repos`). Numbers from arXiv/journal papers come from search-engine snippets of those primary pages; they are flagged "(via search snippet)" and should be checked against the PDFs before being quoted in a client-facing document.

---

## 1. Preprocessing: registration, denoising, downsampling, storey splitting, Manhattan alignment; tooling

### Takeaway
Preprocessing is a solved engineering problem with mature permissively-licensed libraries (Open3D, PCL, PDAL; CloudCompare is GPL desktop tooling). The non-trivial parts for Scan-to-BIM are (a) gravity/Manhattan alignment, because several key learned models (SpatialLM, RoomFormer-style density-map methods) *require* axis-aligned, z-up input, and (b) storey splitting, which open pipelines like Cloud2BIM do with point-density histograms along z.

### Cited Findings
- Open-source libraries and GitHub-reported licence metadata (Nov 2026): Open3D (isl-org/Open3D, ~14.2k stars, licence field "Other"), PCL (PointCloudLibrary/pcl, ~11.2k stars, "Other"), PDAL ("GDAL for point cloud data", ~1.4k stars, "Other"), CloudCompare (~4.8k stars, "Other"), pyRANSAC-3D (Apache-2.0; "fitting 3D primitive shapes to point clouds with RANSAC. Detect planes, spheres, cylinders…") — [GitHub repo metadata via gh search](https://github.com/isl-org/Open3D); [PDAL](https://github.com/PDAL/PDAL); [CloudCompare](https://github.com/CloudCompare/CloudCompare); [pyRANSAC-3D](https://github.com/leomariga/pyRANSAC-3D)
- SpatialLM requires input point clouds to be axis-aligned with the z-axis pointing up — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- RoomFormer's input is "a top-down-view density map of the input point cloud" (points projected along the vertical axis into density images) — i.e., requires gravity alignment and per-storey slicing — [RoomFormer README](https://github.com/ywyue/RoomFormer)
- Cloud2BIM: slabs/storeys found by "density-based height segmentation, morphological operations, and contour detection"; the segmentation algorithm "utilizes point cloud density analysis" augmented by image and morphological operations; only point XYZ is used (no colour/intensity); handles non-orthogonal walls — [Cloud2BIM README](https://github.com/VaclavNezerka/Cloud2BIM); [Cloud2BIM arXiv 2503.11498 (via search snippet)](https://arxiv.org/html/2503.11498v2)
- BIMStruct3D (EC3 2026) wall reconstruction is "based on axis-aligned point grouping. DBSCAN clustering is applied per axis" — implies a Manhattan-alignment pre-step — [BIMStruct3D, arXiv 2604.24311 (via search snippet)](https://www.alphaxiv.org/abs/2604.24311)
- A 2025 review (Yang et al., J. CAD & Computer Graphics) on large-scale Scan2BIM covers registration/alignment, segmentation and automated BIM modelling and sorts registration methods into optimization-based and deep-learning-based — [JCAD review](https://www.jcad.cn/article/doi/10.3724/SP.J.1089.2024-00265)
- Pointcept-based models need GPU sparse ops / FlashAttention; Pointcept supports CUDA ≥11.3 or ROCm ≥7.0; PTv3 without FlashAttention requires `enable_flash=False` and smaller patch sizes at some accuracy cost — [Pointcept README](https://github.com/Pointcept/Pointcept)

### Inferences
- Recommended preprocessing chain (engineering judgement, standard practice; not benchmarked here): (1) import E57/LAS/LAZ with PDAL; (2) registration is usually already done by the scanner vendor software (Leica/FARO/NavVis) — keep ICP/FPFH-RANSAC (Open3D) only for multi-session merges; (3) statistical/radius outlier removal + voxel downsampling (1–2 cm for element extraction, 2–5 cm for DL inference) in Open3D; (4) gravity alignment via largest horizontal planes (floor/ceiling RANSAC) and Manhattan yaw alignment via histogram of wall-normal azimuths; (5) storey split via z-histogram peaks of horizontal-normal points (as Cloud2BIM does); (6) keep a reversible transform so outputs return to the project/survey coordinate system (IfcMapConversion).
- Prefer Open3D/PDAL/PCL (permissive, per typical BSD/MIT terms — verify "Other" licence field) for anything shipped in a product; CloudCompare (GPL family) is fine as an internal QA/desktop tool or via its CLI as a separate process, but avoid linking it into proprietary code.

### Gaps
- Exact licence texts of Open3D, PCL, PDAL and CloudCompare were not opened (GitHub metadata says "Other"); verify before productization.
- No quantitative benchmark found comparing Manhattan-alignment or storey-splitting methods; no source quantified the impact of downsampling resolution on wall-position error.
- Learned registration (e.g., GeoTransformer-class methods) not researched due to scope/tool budget.

---

## 2. Semantic & instance segmentation (backbones, open-vocabulary, benchmarks, building datasets)

### Takeaway
The Pointcept family (PTv3 → Sonata → Concerto → Utonia, plus the lighter LitePT) defines the 2024–2026 SOTA for indoor semantic segmentation (~77–81% mIoU ScanNet, ~74–78% S3DIS Area 5). OneFormer3D is the strongest open unified semantic+instance model (S3DIS mAP50 72.7). **But most SOTA pretrained weights are CC-BY-NC 4.0 (non-commercial)** and the standard training datasets (ScanNet, Structured3D) carry non-commercial terms; a commercial startup should train its own weights with MIT-licensed code (Pointcept codebase, LitePT, Mask3D, KPConv) on owned/licensed data.

### Cited Findings
**Backbones / self-supervised encoders**
- Pointcept codebase (MIT) supports PTv3, PTv2, PTv1, OA-CNNs, LitePT, SparseUNet, OctFormer, Swin3D, and pretraining methods Utonia (ICML 2026), Concerto (NeurIPS 2025), Sonata (CVPR 2025 Highlight), PPT, MSC; datasets ScanNet, ScanNet200, ScanNet++, S3DIS, ARKitScenes, HM3D, Matterport3D, Structured3D. Utonia code released with Pointcept v1.7.0 in Mar 2026 — [Pointcept README](https://github.com/Pointcept/Pointcept)
- PTv3 reported mIoU in Pointcept: ScanNet val 77.6 (PTv3), 78.5 (PTv3+PPT); ScanNet200 val 35.3; S3DIS Area 5 73.6 (PTv3), 75.4 (PTv3+PPT); typical training on 4–8 GPUs (3090/A100 class) — [Pointcept README](https://github.com/Pointcept/Pointcept)
- **Licence conflict:** the standalone PTv3 repo (Pointcept/PointTransformerV3) LICENSE is CC BY-NC 4.0 ("for NonCommercial purposes only") — [PTv3 LICENSE](https://github.com/Pointcept/PointTransformerV3/blob/main/LICENSE); whereas the Pointcept codebase (which also implements PTv3) states MIT — [Pointcept README](https://github.com/Pointcept/Pointcept)
- Sonata (CVPR 2025): code Apache 2.0; **weights CC-BY-NC 4.0**, further restricted by NC terms of pretraining datasets such as HM3D and ARKitScenes — [Sonata README](https://github.com/facebookresearch/sonata). Linear-probing ScanNet mIoU raised from 21.8% to 72.5% (vs 63.1% for lifted DINOv2 features) — [Sonata CVPR 2025 paper (via search snippet)](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Sonata_Self-Supervised_Learning_of_Reliable_Point_Representations_CVPR_2025_paper.pdf). Third-party listing: Sonata+PTv3 fine-tune 79.4 ScanNet, 76.0 S3DIS Area 5, 82.3 S3DIS 6-fold (unverified) — [same search](https://alphaxiv.org/abs/2503.16429)
- Concerto (NeurIPS 2025, joint 2D–3D SSL): 80.7% ScanNet, 39.2% ScanNet200, 50.7% ScanNet++ mIoU; linear probing beats supervised PTv3 on ScanNet200 and S3DIS — [Concerto arXiv 2510.23607 (via search snippet)](https://arxiv.org/pdf/2510.23607). Repo licence field Apache-2.0 (code) — [GitHub metadata](https://github.com/Pointcept/Concerto)
- Utonia ("one encoder for all point clouds", ICML 2026): full fine-tune 81.1% ScanNet, 78.1% S3DIS — [Utonia arXiv 2603.03283 (via search snippet)](https://arxiv.org/pdf/2603.03283). Code Apache-2.0, **weights CC-BY-NC 4.0** (restricted by HM3D/ARKitScenes terms); encoders utonia / utonia_small / utonia_tiny; inference demo Feb 2026 — [Utonia README](https://github.com/Pointcept/Utonia). Utonia notes Sonata results it cites used extra PPT supervision/data and are not directly comparable — [via search snippet](https://arxiv.org/pdf/2603.03283)
- LitePT (CVPR 2026 Highlight, ETH/Oxford/UZH; released 2025-12-16): code MIT. ScanNet efficiency: PTv3 46.1M params, 51 ms inference, 4.1 GB inference memory vs LitePT-S 12.7M params, 21 ms, 2.0 GB; mIoU ScanNet 76.5 (S), Structured3D 83.6/85.1/85.4 (S/B/L); instance seg ScanNet mAP50 64.9 — [LitePT README](https://github.com/prs-eth/LitePT)
- KPConv-PyTorch: MIT — [GitHub metadata](https://github.com/HuguesTHOMAS/KPConv-PyTorch)

**Instance / panoptic segmentation**
- OneFormer3D (CVPR 2024, mmdetection3d v1.1.0): ScanNet mAP25/50/mAP 86.7/78.8/59.3, mIoU 76.4, PQ 70.7; ScanNet200 mAP 30.2, mIoU 29.4; **S3DIS Area 5 mAP25 80.6, mAP50 72.7, mAP 58.0, mIoU 71.9, PQ 64.6**; trains on a single 32 GB GPU (24 GB for ScanNet); S3DIS model initialised from a checkpoint pretrained on ScanNet+Structured3D — [OneFormer3D README](https://github.com/filaPro/oneformer3d). **LICENSE: CC BY-NC 4.0, commercial use not allowed** — [OneFormer3D LICENSE](https://github.com/filaPro/oneformer3d/blob/main/LICENSE)
- Mask3D: MIT, ~750 stars, "state-of-the-art on ScanNet, ScanNet200, S3DIS" (2023-era) — [GitHub metadata](https://github.com/JonasSchult/Mask3D)

**Open-vocabulary / SAM-based 2D→3D lifting**
- OpenMask3D (NeurIPS 2023, MIT): class-agnostic 3D masks + multi-view CLIP feature fusion; third-party listing 15.4 mAP ScanNet200 (unverified) — [NeurIPS abstract](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d77b5482e38339a8068791d939126be2-Abstract.html); [GitHub](https://github.com/OpenMask3D/openmask3d)
- Open3DIS (CVPR 2024, VinAI, BSD-3-Clause): open-vocab instance segmentation with 2D mask guidance, reproducibility code for ScanNet200, Replica, S3DIS, ScanNet++ — [GitHub](https://github.com/VinAIResearch/Open3DIS)
- SAI3D (CVPR 2024, no licence declared on GitHub); EmbodiedSAM/ESAM (ICLR 2025 Oral, MIT, "online segment any 3D thing in real time"); SAMPart3D (Pointcept, MIT) — [GitHub metadata](https://github.com/yd-yin/SAI3D); [ESAM](https://github.com/xuxw98/ESAM); [SAMPart3D](https://github.com/Pointcept/SAMPart3D)
- SAM 2 is Apache-2.0 — [GitHub](https://github.com/facebookresearch/sam2). SAM 3 (Nov 2025) is under a custom "SAM License" (2025-11-19): royalty-free, commercial use allowed, with use restrictions (military/ITAR/sanctions, no reverse engineering, termination if suing Meta for IP) — [Roboflow licence summary](https://roboflow.com/model-licenses/segment-anything-3); [ScanCode licence DB](https://scancode-licensedb.aboutcode.org/sam-2025-11-19.html)
- A 2025 ISPRS Archives paper uses a segment-anything model for scan-to-BIM and reports centimetre-level accuracy on two case studies with ~9 s runtime per case — [ISPRS Archives XLVIII-4/W15-2025 (via search snippet)](https://isprs-archives.copernicus.org/articles/XLVIII-4-W15-2025/1/2025/)

**Building-specific datasets**
- BIMNet (Tsinghua, 2025): "IFC-based large-scale point cloud to BIM dataset" with real point clouds + manually modelled BIM, and geometric + topological evaluation metrics; student research award at buildingSMART International Summit 2025 — [Tsinghua news](https://www.tsinghua.edu.cn/en/info/1245/14523.htm); [Smart City Gnosys](https://smartcity.efri.uniri.hr/article.php?id=17515)
- HePIC / BIM-Net (Univ. Padua, ICIP 2023): heritage point clouds of two large buildings labelled from existing BIM; BIM-Net 40.6 mIoU on HePIC, 18.4 on Arch2S; BIM-Net++ 43.7 (secondary leaderboard figures) — [ICIP 2023](https://rc.signalprocessingsociety.org/conferences/icip-2023/spsicip23vid0377); [HyperAI listing](https://vercel.hyper.ai/en/papers/fully-automated-scan-to-bim-via-point-cloud)
- DeKH (German hospital) dataset with high-res point clouds, GT BIMs and semantic labels released with BIMStruct3D (EC3 2026); evaluated also on CV4AEC data — [BIMStruct3D (via search snippet)](https://www.alphaxiv.org/abs/2604.24311)
- CV4AEC Scan-to-BIM challenge (CVPR 2021/2022): floorplan and 3D building reconstruction tracks; 3D track training data = 11 floors from 7 buildings, aligned LAZ point clouds — [TUM CMS news](https://cee.ed.tum.de/cms/news/article/cms-team-wins-3rd-prize-in-cv4aec-competition); [FloorPP-Net](https://arxiv.org/pdf/2106.10635)
- Cloud2BIM released the full Kladno railway-station point cloud on Zenodo — [Cloud2BIM README](https://github.com/VaclavNezerka/Cloud2BIM); [Zenodo 14221915](https://zenodo.org/records/14221915)
- One conference paper notes relatively few building-focused DL studies and datasets, so models are often trained on general-purpose S3DIS — [search summary; attribution to this conference paper uncertain](https://journals.hs-offenburg.de/index.php/urai/article/download/143/149/457)

**Dataset licences**
- Structured3D: gated agreement limits use to non-commercial research/education, no redistribution; for-profit employers bound by same terms — [HF Pointcept/structured3d-compressed agreement (via search snippet)](https://www.huggingface.co/datasets/Pointcept/structured3d-compressed/tree/main)
- ScanNet listed as "Non-Commercial" (secondary table); ScanNet++ has its own Terms of Use — [SpatialBench arXiv 2605.27367 (via search snippet)](https://arxiv.org/pdf/2605.27367); [ScanNet++ ToU](https://scannetpp.mlsg.cit.tum.de/scannetpp/static/scannetpp-terms-of-use.pdf)

### Inferences
- S3DIS-style classes (ceiling, floor, wall, beam, column, window, door, clutter…) map almost 1:1 to BIM element classes, so a PTv3/LitePT semantic model + a geometric instancing step is the pragmatic core. Expect ~70–78% mIoU on S3DIS-like data, but per-class IoU for doors/windows/beams is materially lower than for walls/floors (consistent with the ISPRS 2026 openings study in §3).
- Commercial-safe recipe: Pointcept (MIT) or LitePT (MIT) code + **own pretraining/fine-tuning on owned scans** (and synthetic scans from owned BIM, §6). Using Sonata/Utonia/Concerto/OneFormer3D/PTv3-repo weights in a paid product is blocked by CC-BY-NC; they remain useful for internal R&D baselines only (legal review required).
- Open-vocab/SAM lifting is valuable for long-tail objects (fixtures, equipment) and for auto-labelling to bootstrap training data, but not for metric-accurate walls/slabs.
- LitePT-S (2 GB inference memory, ~21 ms per ScanNet scene) suggests building-scale inference is tractable on a single 24 GB GPU if the cloud is tiled per storey/room.

### Gaps
- Per-class IoU for walls/doors/windows/columns from PTv3/Utonia on S3DIS not retrieved (arXiv/HF blocked).
- Concerto weight licence not confirmed (code is Apache-2.0); Utonia "October 2026" weight update date looked inconsistent on its README.
- S3DIS licence text not found; ArCH heritage dataset and industrial MEP datasets not located beyond the RBLSIA/MEP synthetic work (§6).
- Size/class list of BIMNet (Tsinghua) not confirmed; no access to full text.
- No public building-scale (multi-storey, >100M points) segmentation benchmark with runtime numbers was found.

---

## 3. Structured reconstruction: walls/slabs/openings, floorplans, SpatialLM, Cloud2BIM, MEP, structure

### Takeaway
Two families coexist: (a) **geometric/rule-based IFC pipelines** (Cloud2BIM, MIT — slabs, walls, rectangular openings, spaces; ~60 s per building) and hybrid DL+geometry (BIMStruct3D, 2026), and (b) **learned structured-output models** (RoomFormer/PolyRoom/FRI-Net/CAGE for 2D floorplans, room F1 ~95–99 on Structured3D; SpatialLM for walls/doors/windows/boxes as text, wall F1 ~94 on Structured3D fine-tuned but only ~68–69 zero-shot on real reconstructed scans). None outputs Revit-native parametric families out of the box; MEP remains largely segmentation + RANSAC cylinder fitting.

### Cited Findings
**Cloud2BIM (open-source → IFC)**
- Python, MIT licence; targets slabs, walls, windows and doors; entry `cloud2entities.py` with YAML config; modules `generate_ifc.py`, `space_generator.py`, a `DL_module`; input folders for E57 and XYZ; outputs IFC and XYZ — [Cloud2BIM README](https://github.com/VaclavNezerka/Cloud2BIM)
- Published: Zbirovský & Nežerka (2025), *Automation in Construction* 177, 106303, doi:10.1016/j.autcon.2025.106303 — [Cloud2BIM README](https://github.com/VaclavNezerka/Cloud2BIM); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0926580525003437)
- Features: wall & slab segmentation, opening detection, room zoning, non-orthogonal walls; IFC usable in Revit, Archicad, FreeCAD, Blender+Bonsai — [arXiv 2503.11498 (via search snippet)](https://arxiv.org/html/2503.11498v2)
- Benchmark building processed in 60 s total including IFC generation; claimed up to 7× faster than fastest competing solutions; openings limited to rectangular (no arched/circular/irregular); 24/25 (96%) correct in one wall-snapping case; authors say direct comparisons are impossible due to lack of a uniform benchmark — [arXiv 2503.11498 (via search snippet)](https://arxiv.org/pdf/2503.11498)
- A commercial successor "Cloud2BIM-AI" is offered by Constriq (CTU spin-off), claiming broader AI recognition, no manual parameter tuning, GUI (vendor claims) — [Cloud2BIM README](https://github.com/VaclavNezerka/Cloud2BIM)
- 150 stars, actively updated (Oct 2026) — [GitHub metadata](https://github.com/VaclavNezerka/Cloud2BIM)

**BIMStruct3D (EC3 2026, DFKI)**
- Hybrid learning segmentation + topology-aware geometric reconstruction for walls, doors, columns; IFC via IfcOpenShell with project–site–building–storey hierarchy; walls by axis-aligned DBSCAN; proposes vIoU metric robust to fragmented walls; "significant improvements over a RANSAC-based baseline" on DeKH and CV4AEC — [arXiv 2604.24311 (via search snippet)](https://www.alphaxiv.org/abs/2604.24311); [EC3 publication page](https://ec-3.org/publication/ec32026_197/)
- Claims there are "no open-source implementations of complete scan-to-BIM pipelines or benchmark datasets" — [via search snippet](https://www.alphaxiv.org/abs/2604.24311); this is contradicted by Cloud2BIM's MIT release — [Cloud2BIM](https://github.com/VaclavNezerka/Cloud2BIM)

**SpatialLM (Manycore + HKUST, NeurIPS 2025)**
- Encoder–MLP–LLM; outputs walls, doors, windows and oriented 3D boxes (59 categories, user-selectable) as structured text; v1.1 (Jun 2025) uses Sonata encoder, doubles point resolution; models SpatialLM1.1-Llama-1B and -Qwen-0.5B — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- Layout F1 on Structured3D @0.25 IoU: RoomFormer 83.4, SceneScript (ft) 90.4, SpatialLM1.1-Qwen-0.5B (ft) 94.3 (@0.5: 81.4 / 89.2 / 93.5); ScanNet 3D detection F1@0.25: V-DETR 65.1, SpatialLM 65.6 — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- Zero-shot on SpatialLM-Testset (107 point clouds reconstructed from RGB video with MASt3R-SLAM): wall F1 68.9 (Llama-1B) / 68.2 (Qwen-0.5B); bed 96.8; refrigerator 0.0/16.7 — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- SpatialLM-Dataset: 12,328 indoor scenes, 54,778 rooms (released Sep 2025); no IFC/CAD export (only Rerun visualisation); environment Python 3.11, PyTorch 2.4.1, CUDA 12.4 — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- ~5.1k GitHub stars — [GitHub metadata](https://github.com/manycore-research/SpatialLM)
- SceneScript (Meta; SpatialLM 1.0's encoder) code is CC BY-NC 4.0 — [SceneScript LICENSE](https://github.com/facebookresearch/scenescript/blob/main/LICENSE)

**Floorplan reconstruction (2D vectorised rooms)**
- RoomFormer (CVPR 2023, MIT, weights available): density-map input, Structured3D and SceneCAD — [RoomFormer README](https://github.com/ywyue/RoomFormer)
- SceneCAD F1 (room / corner / angle): HEAT 79.1 / 82.5 / 70.4; RoomFormer 85.3 / 88.8 / 75.8; FRI-Net 85.9 / 89.2 / 75.9 — [FRI-Net arXiv 2407.10687 (via search snippet)](https://arxiv.org/pdf/2407.10687)
- Structured3D-B (Raster2Seq, arXiv 2602.09016) F1: HEAT 94.7/84.5/79.6; RoomFormer 95.1/91.7/83.2; FRI-Net 96.5/85.4/83.3; PolyRoom 98.9/96.0/91.9 (different split than original papers) — [Raster2Seq (via search snippet)](https://arxiv.org/pdf/2602.09016)
- CAGE (arXiv 2509.15459): Structured3D 99.1 room F1, 91.7 corner F1, 89.3 angle F1 without post-processing — [CAGE (via search snippet)](https://arxiv.org/pdf/2509.15459)
- Corner-based methods (HEAT) degrade significantly in cross-dataset (Structured3D→SceneCAD) — [same search, FRI-Net/RoomFormer](https://arxiv.org/pdf/2211.15658)
- PolyRoom (ECCV 2024): checkpoints on Google Drive, **no licence file** on GitHub; FRI-Net: no licence declared; HEAT: licence "Other" — [PolyRoom](https://github.com/3dv-casia/PolyRoom); [GitHub metadata](https://github.com/Daisy-1227/FRI-Net); [HEAT](https://github.com/woodfrog/heat)

**Openings, structure, MEP**
- ISPRS 2026 study comparing five DL models for doors/windows: small size, placement variability and occlusion make openings hard; concludes geometric reconstruction algorithms deserve more emphasis than segmentation scores alone — [ISPRS Annals XI-1-2026 (via search snippet)](https://isprs-annals.copernicus.org/articles/XI-1-2026/437/2026/isprs-annals-XI-1-2026-437-2026.pdf)
- MEP pipes: ISARC 2023 framework = DL semantic segmentation then Efficient RANSAC to fit cylinders — [ISARC 2023](https://www.iaarc.org/publications/fulltext/056_ISARC%202023_Paper_139.pdf); DLR preprint (Alex & Stoppe, arXiv 2506.22118) CNN segments pipe/flange/elbow/tee/cross, predicts radius among 23 discrete values plus orientation — [arXiv 2506.22118 (via search snippet)](https://arxiv.org/pdf/2506.22118v1); CityU: DL point-cloud completion of occluded MEP trained on parametric BIM + occlusion simulation — [CityU](https://scholars.cityu.edu.hk/en/publications/deep-learning-based-point-cloud-completion-for-mep-components/)
- Commercial: ClearEdge3D EdgeWise 5.0 automates gridded steel/concrete structure extraction and pipes with Revit integration — [AEC Magazine](https://aecmag.com/news/news-clearedge3d-announces-edgewise-5-0/)

### Inferences
- For a startup MVP, the most defensible architecture is **hybrid**: DL semantic labels (wall/floor/ceiling/column/beam/door/window/pipe/duct) → per-class geometric fitting (planes for walls/slabs with thickness from paired opposite faces; rectangles for openings on wall planes; cylinders for columns/pipes; extruded profiles for beams) → topology repair (wall joins, snapping to grid/orthogonality) → IFC. This is the pattern of BIMStruct3D, Cloud2BIM and the ISARC MEP work.
- Cloud2BIM (MIT) is a legitimate base to fork for slabs/walls/openings/IfcSpace; floorplan transformers (RoomFormer, MIT) can provide room polygons → IfcSpace and wall centrelines; SpatialLM is attractive but its weights are NC and its zero-shot wall F1 (~68) on real scans is insufficient for LOD 300 without fine-tuning on own data (code is usable to retrain).
- PolyRoom/FRI-Net without a licence are "all rights reserved" by default — avoid in product code.
- MEP at LOD 300 (fittings, connectivity, system classification) remains the least automated part; scope an MVP to architecture + structure + straight pipe/duct runs.

### Gaps
- No wall position/thickness error (cm) for Cloud2BIM, BIMStruct3D or SpatialLM was retrievable (full texts blocked); the AI-summary claims of 97.6% wall / 96.2% column detection for Cloud2BIM are unverified and were not found in the primary text — [aimodels.fyi](https://www.aimodels.fyi/papers/arxiv/cloud2bim-open-source-automatic-pipeline-efficient-conversion).
- Cloud2BIM hardware for the 60 s runtime and point count not confirmed.
- No open repo found that extracts beams/columns/MEP straight to IFC with published accuracy; duct (rectangular) extraction not covered.
- No source on curved walls specifically.

---

## 4. Generating BIM: IfcOpenShell/Bonsai, Revit API, Dynamo, APS Design Automation; family mapping; LOD

### Takeaway
IFC can be generated fully open-source with IfcOpenShell (LGPL-3.0), which is what Cloud2BIM and BIMStruct3D use; Revit-native output can be produced headlessly with Autodesk APS Design Automation (billed in Flex tokens, ~2 tokens per processing hour for DA generally) running a custom Revit add-in that instantiates system families (walls/floors) and loadable families (doors/windows) from fitted parameters. LOD 200 (correct geometry + types) is realistic automatically for architecture/structure; LOD 300 requires type matching to a family library and human QA.

### Cited Findings
- IfcOpenShell: "Open source IFC library and geometry engine", LGPL-3.0, ~2.9k stars, active (Nov 2026) — [GitHub metadata](https://github.com/IfcOpenShell/IfcOpenShell)
- BIMStruct3D exports via IfcOpenShell creating project–site–building–storey hierarchy — [via search snippet](https://www.alphaxiv.org/abs/2604.24311); Cloud2BIM IFC is consumable in Revit, Archicad, FreeCAD and Blender+Bonsai — [via search snippet](https://arxiv.org/html/2503.11498v2)
- AECgeeks/ifc-pipeline (MIT): processing queue + front-end for IFC with IfcOpenShell, Docker Compose, Flask — [GitHub metadata](https://github.com/AECgeeks/ifc-pipeline)
- APS Design Automation API: 2.0 Flex tokens per processing hour (DA for Fusion: 3.0); fractional usage accrues; tokens expire 12 months after purchase; enterprise volume discounts from 5,000+ tokens; DA runs headless desktop products (Revit/AutoCAD…) with your add-ins for batch work — [APS pricing](https://aps.autodesk.com/pricing); [Autodesk Flex rate sheet](https://www.autodesk.com/flexratesheet); [APS blog 2020](https://aps.autodesk.com/node/1615)
- Autodesk released an official Revit Public MCP Server (blog June 17, 2026), technical preview with Revit 2027 (April 2026), stdio transport — [Autodesk blog](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/)

### Inferences
- Two output tracks: (1) **IFC-first** (IfcOpenShell, no licence cost, runs on Linux GPU workers next to the ML) — deliver IFC4 with IfcWall(StandardCase)/IfcSlab/IfcOpeningElement+IfcDoor/IfcWindow/IfcColumn/IfcBeam/IfcSpace/IfcPipeSegment; (2) **RVT-on-demand** via APS Design Automation (Revit engine in Autodesk cloud) or a Windows Revit worker, reading a JSON of fitted primitives and creating Revit walls (Wall.Create with WallType chosen by nearest thickness), floors from boundary loops, and family instances for openings (closest family type by width/height). The RVT route avoids IFC-import quality issues (IFC import into Revit yields less editable "IFC objects").
- Note LGPL-3.0: dynamic linking/usage as a Python package in a SaaS backend is generally compatible with proprietary code; modifications to IfcOpenShell itself must be shared if distributed (legal check).
- LOD 200/300 feasibility (judgement): walls/slabs/openings/columns at LOD 200 automatable with current tech; LOD 300 needs (a) a typed family catalogue per client, (b) thickness/material inference (scans can't see inside walls), (c) human-in-the-loop QA.

### Gaps
- Bonsai (BlenderBIM) licence not confirmed in this session (lives in the IfcOpenShell repo; often reported as GPL — verify).
- Revit-specific DA rate not explicitly stated in results (only general 2.0 tokens/hour); no cost per building found.
- No published benchmark found of IFC→Revit import fidelity for scan-derived models.

---

## 5. VLMs / LLM agents in the loop; QA via model-vs-cloud deviation

### Takeaway
As of 2026, LLM agents operate BIM authoring tools through MCP (official Autodesk Revit MCP server, community Revit MCP servers, MCP4IFC/Bonsai-MCP/ifcMCP for IFC), but **no published work was found that closes the loop point cloud → detected primitives → LLM agent → Revit/IFC** with accuracy figures. The deterministic part (deviation heatmaps cloud-vs-model) is well established and is the right QA gate.

### Cited Findings
- MCP4IFC (arXiv 2511.05533): LLMs read, create and edit IFC via MCP, using in-context learning; example builds a small house from natural language — [arXiv 2511.05533 (via search snippet)](https://arxiv.org/pdf/2511.05533v1); [Emergent Mind](https://www.emergentmind.com/topics/mcp4ifc)
- arXiv 2601.00809 (Jan 2026) describes MCP as a JSON-RPC standard for LLM agents and compares tools including Bonsai-MCP and ifcMCP — [arXiv 2601.00809 (via search snippet)](https://arxiv.org/html/2601.00809v1)
- ICCCBE 2026: Revit via MCP with RAG + ReAct multi-agent reasoning + multi-LLM support translating natural language into BIM modelling operations — [EasyChair slides (via search snippet)](https://easychair.org/smart-slide/slide/kz9T)
- Autodesk official Revit MCP server (Revit 2027 preview; auto-configures with Claude Desktop/Cursor); community MCP servers (EraCore Revit MCP, MIT; projects supporting Revit 2022–2026 with wall/room/floorplan creation tools; one with 166 tools) — [Autodesk blog](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/); [Glama EraCore](https://glama.ai/mcp/servers/crt7iv833h); [Glama RevitMCP](https://glama.ai/mcp/servers/AchyErrorJ/RevitMCP)
- LLM agent (ReAct) for reading IFC and computing floor areas — [EasyChair Zhu & Ma](https://wvvw.easychair.org/publications/paper/qnrt/open)
- SpatialLM itself is an LLM that emits structured layout text from point clouds (encoder → LLM) — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- Deviation analysis = computation, visualisation, analysis of element-to-cloud deviations; research Revit plug-in automates it for walls — [ISPRS Archives XLII-2-W9 2019](https://isprs-archives.copernicus.org/articles/XLII-2-W9/455/2019/); point-to-point scan-vs-BIM (sample BIM mesh faces, downsample scan to match, colour by deviation) — [ICCCBE 2018](https://programme.exordo.com/icccbe2018/delegates/presentation/303/); CMU (Anil et al.) deviation analysis as QA of as-is BIM — [CMU RI](https://ri.cmu.edu/publications/assessment-of-quality-of-as-is-building-information-models-generated-from-point-clouds-using-deviation-analysis); commercial deviation analysis (Cupix) — [Cupix support](https://support.cupix.works/hc/en-us/articles/34897571808411-Deviation-Analysis)

### Inferences
- Best use of LLMs/VLMs in a 2026 pipeline (judgement): (1) **orchestration and exception handling** — agent receives a JSON of primitives + per-element confidence + deviation stats and calls deterministic tools (IfcOpenShell API / Revit MCP) to create, type-map and fix elements; (2) **type/family matching** (map fitted wall 0.15 m + finish to client's WallType catalogue); (3) **VLM review** of rendered orthophotos/sections overlaid with the model to flag missed doors/windows; (4) report generation. Geometry should never be "invented" by the LLM — numbers come from fitting.
- QA gate: compute cloud-to-model distances per element (IfcOpenShell geometry → mesh → sample → Open3D KD-tree distances), produce heatmaps and per-element pass/fail (e.g., LOD-dependent tolerance), and route failures to human review; this also yields training signal for active learning.

### Gaps
- No peer-reviewed accuracy for any LLM-agent Scan-to-BIM loop; no benchmark of VLM-based opening detection on orthophotos.
- No source on automated push of deviation heatmaps back into Revit (beyond research wall plug-in).

---

## 6. Synthetic data from BIM and fine-tuning on proprietary data

### Takeaway
Generating labelled synthetic scans by virtually scanning existing BIM models is an active and validated strategy (2020–2026); synthetic-only training suffers a domain gap, but **hybrid synthetic + real consistently beats real-only**, and ray-cast (scanner-simulating) generation beats uniform surface sampling. A company owning many BIM+scan pairs has a direct moat: scans can be auto-labelled by aligning them to the BIM.

### Cited Findings
- BIM-guided virtual-to-real framework (2026): component-level segmentation trained only on BIM-generated supervision; synthetic dataset of 132 scans ≈ 8.75×10⁹ points with component labels; argues public datasets like BIM-Net are too small — [PMC12788284 (via search snippet)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12788284/)
- Ma et al. 2020 (UT Austin): synthetic point clouds from as-built BIM tested against real scans; synthetic+real improves segmentation, synthetic-only has a domain gap — [WSC 2021 paper (attribution via search summary)](https://www.informs-sim.org/wsc21papers/218.pdf); [ISPRS 2026 (via search snippet)](https://isprs-archives.copernicus.org/articles/XLIX-B2-2026/117/2026/isprs-archives-XLIX-B2-2026-117-2026.pdf)
- Ma, Martens, Blankenbach: virtual laser scanning for infrastructure; hybrid datasets markedly outperform real-only — [search summary; link attribution uncertain (via search snippet)](https://pureportal.strath.ac.uk/en/publications/generation-and-evaluation-of-synthetic-point-cloud-data-for-train/)
- RBLSIA (Yue & Wang, EC3 2025): ray-based synthetic MEP point clouds from BIM; mIoU on average +3.32% vs uniform sampling — [EC3 2025](https://ec-3.org/?p=9774)
- Campagnolo et al. (ICIP 2023): BIM-annotated dataset + pretraining + class re-weighting to reduce labelling — [ICIP 2023](https://rc.signalprocessingsociety.org/conferences/icip-2023/spsicip23vid0377)
- CityU: MEP completion trained on parametric BIM + occlusion simulation — [CityU](https://scholars.cityu.edu.hk/en/publications/deep-learning-based-point-cloud-completion-for-mep-components/)
- SpatialLM provides a fine-tuning guide and trained on a 12,328-scene synthetic-layout dataset; fine-tuning lifted Structured3D layout F1 to 94.3 — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- Sonata/Concerto/Utonia show large gains from self-supervised pretraining (e.g., Sonata linear probe 72.5% ScanNet) — [Sonata CVPR 2025 (via search snippet)](https://openaccess.thecvf.com/content/CVPR2025/papers/Wu_Sonata_Self-Supervised_Learning_of_Reliable_Point_Representations_CVPR_2025_paper.pdf)

### Inferences
- Data engine for a startup: (1) IFC/RVT → IfcOpenShell geometry → per-element meshes with IFC class/type labels; (2) virtual TLS/MLS/SLAM scanning (ray casting from plausible stations, range noise, incidence-angle dropout, glass transparency, clutter insertion) → labelled clouds; (3) for real projects with both scan and as-built BIM, register and transfer labels by nearest-element distance (with threshold) → real labelled data at near-zero labelling cost; (4) self-supervised pretraining (Sonata/Utonia recipe in MIT/Apache code) on all unlabelled company scans; (5) supervised fine-tuning on mixed synthetic+real; (6) active learning from QA failures.
- This route also solves the licensing problem: weights trained from scratch on owned data are commercially usable.

### Gaps
- Exact mIoU gaps (synthetic-only vs hybrid vs real) for building elements not retrieved (full texts blocked).
- No open-source virtual-scanner tool for BIM was verified in this session (e.g., Helios++ not researched).

---

## 7. Reported accuracy, runtime/compute, failure modes

### Takeaway
Segmentation accuracy is high on benchmarks (~76–81% mIoU ScanNet; ~72–78% S3DIS), floorplan room-level F1 is ~95–99% on synthetic Structured3D but ~85% on real SceneCAD, and real-scan zero-shot structured outputs (SpatialLM walls F1 ~68) drop substantially. Centimetre-level geometric accuracy is reported only in isolated case studies. Runtime is not the bottleneck (seconds to minutes per building on one GPU/CPU); data domain gap, occlusion, glass, clutter, openings and fragmented walls are.

### Cited Findings
- Semantic seg: PTv3 77.6 ScanNet / 73.6 S3DIS A5 — [Pointcept](https://github.com/Pointcept/Pointcept); Concerto 80.7 ScanNet — [via search snippet](https://arxiv.org/pdf/2510.23607); Utonia 81.1 ScanNet / 78.1 S3DIS — [via search snippet](https://arxiv.org/pdf/2603.03283)
- Instance seg: OneFormer3D S3DIS A5 mAP50 72.7, mAP 58.0 — [OneFormer3D](https://github.com/filaPro/oneformer3d)
- Floorplans: room F1 99.1 (CAGE, Structured3D) vs ~85–86 on real SceneCAD (RoomFormer/FRI-Net) — [CAGE (via search snippet)](https://arxiv.org/pdf/2509.15459); [FRI-Net (via search snippet)](https://arxiv.org/pdf/2407.10687)
- SpatialLM: Structured3D fine-tuned wall F1@0.25 94.3 vs zero-shot real-video scans wall F1 68.2–68.9 — [SpatialLM README](https://github.com/manycore-research/SpatialLM)
- Heritage domain is much harder: BIM-Net ~40.6 mIoU HePIC, 18.4 Arch2S — [HyperAI listing (secondary)](https://vercel.hyper.ai/en/papers/fully-automated-scan-to-bim-via-point-cloud)
- Geometric accuracy: SAM-based scan-to-BIM reports cm-level accuracy, ~9 s per case — [ISPRS 2025 (via search snippet)](https://isprs-archives.copernicus.org/articles/XLVIII-4-W15-2025/1/2025/); Cloud2BIM 60 s per benchmark building incl. IFC — [via search snippet](https://arxiv.org/pdf/2503.11498)
- Compute: PTv3 inference 51 ms / 4.1 GB; LitePT-S 21 ms / 2.0 GB (ScanNet scenes) — [LitePT](https://github.com/prs-eth/LitePT); OneFormer3D trains on 1×32 GB GPU — [OneFormer3D](https://github.com/filaPro/oneformer3d); Pointcept training typically 4–8 GPUs — [Pointcept](https://github.com/Pointcept/Pointcept)
- Failure modes: incomplete clouds from scanner limits, occlusion and reflective glass; fragmented/variably segmented walls — [BIMStruct3D (via search snippet)](https://www.alphaxiv.org/abs/2604.24311); room-based methods struggle with non-room structures and clutter — [search summary; exact source among results uncertain, likely ISPRS Annals 2026](https://isprs-annals.copernicus.org/articles/XI-1-2026/437/2026/isprs-annals-XI-1-2026-437-2026.pdf); occlusion is a core limitation of Scan-to-BIM/Scan-vs-BIM — [MDPI IJGI 12(7):260](https://www.mdpi.com/2220-9964/12/7/260); furniture/fixture clutter for wall modelling — [CMU](https://www.ri.cmu.edu/project/automated-reverse-engineering-of-buildings); openings small/variable/occluded — [ISPRS Annals 2026](https://isprs-annals.copernicus.org/articles/XI-1-2026/437/2026/isprs-annals-XI-1-2026-437-2026.pdf); Cloud2BIM rectangular-openings-only — [via search snippet](https://arxiv.org/pdf/2503.11498); SpatialLM category variance (refrigerator F1 0–16.7) — [SpatialLM](https://github.com/manycore-research/SpatialLM)
- Reviews: Montás-Laracuente et al. 2025 systematic review (J. Building Engineering, CC BY-NC) on AI for Scan-to-BIM — [UFV repository](https://ddfv.ufv.es/entities/publication/c85cdf18-77d1-4212-a780-00bd77ed66e5); Yang et al. 2025 large-scale Scan2BIM review — [JCAD](https://www.jcad.cn/article/doi/10.3724/SP.J.1089.2024-00265)

### Inferences
- Plan for an end-to-end runtime of minutes per storey on a single 24–48 GB GPU + CPU fitting; labelling/QA human time will dominate cost.
- Realistic product target (judgement): automated LOD 200 draft for walls/slabs/columns/doors/windows/spaces with per-element confidence, then human QA; claim cm-level accuracy only where validated against own ground truth (BIM-vs-scan pairs).

### Gaps
- No standardized building-scale benchmark reporting wall centreline/thickness error in cm across methods (Cloud2BIM authors and BIMStruct3D both note the lack of uniform benchmarks).
- No GPU runtime per full multi-storey building for PTv3/SpatialLM found.
- No quantified failure rates for curved walls, glass curtain walls or dense MEP.

---

## 8. Licences (commercial use)

### Takeaway
Code is mostly permissive; **pretrained weights and benchmark datasets are mostly non-commercial**. Commercially safe building blocks: Pointcept codebase (MIT), LitePT (MIT), KPConv (MIT), Mask3D (MIT), OpenMask3D (MIT), Open3DIS (BSD-3), RoomFormer (MIT), Cloud2BIM (MIT), pyRANSAC-3D (Apache-2.0), SAM 2 (Apache-2.0), SAM 3 (custom, commercial OK with restrictions), IfcOpenShell (LGPL-3.0). Non-commercial: PTv3 standalone repo, OneFormer3D, SceneScript (CC BY-NC 4.0 code), Sonata/Utonia/SpatialLM 1.x weights (CC BY-NC 4.0), Structured3D/ScanNet data.

### Cited Findings
| Component | Code licence | Weights / data licence | Source |
|---|---|---|---|
| Pointcept codebase | MIT | n/a | [Pointcept](https://github.com/Pointcept/Pointcept) |
| PTv3 standalone repo | CC BY-NC 4.0 | — | [LICENSE](https://github.com/Pointcept/PointTransformerV3/blob/main/LICENSE) |
| Sonata | Apache 2.0 | CC BY-NC 4.0 (+HM3D/ARKitScenes NC) | [Sonata](https://github.com/facebookresearch/sonata) |
| Utonia | Apache 2.0 | CC BY-NC 4.0 | [Utonia](https://github.com/Pointcept/Utonia) |
| Concerto | Apache-2.0 (GitHub field) | not confirmed | [GitHub](https://github.com/Pointcept/Concerto) |
| LitePT | MIT | not stated | [LitePT](https://github.com/prs-eth/LitePT) |
| OneFormer3D | CC BY-NC 4.0 | (same repo) | [LICENSE](https://github.com/filaPro/oneformer3d/blob/main/LICENSE) |
| Mask3D / KPConv-PyTorch / OpenMask3D | MIT | — | [Mask3D](https://github.com/JonasSchult/Mask3D); [KPConv](https://github.com/HuguesTHOMAS/KPConv-PyTorch); [OpenMask3D](https://github.com/OpenMask3D/openmask3d) |
| Open3DIS | BSD-3-Clause | — | [GitHub](https://github.com/VinAIResearch/Open3DIS) |
| SpatialLM | Pointcept-derived code Apache 2.0 | 1.0 & 1.1 weights CC BY-NC 4.0; Llama variant also under Llama 3.2 licence | [SpatialLM](https://github.com/manycore-research/SpatialLM) |
| SceneScript | CC BY-NC 4.0 | — | [LICENSE](https://github.com/facebookresearch/scenescript/blob/main/LICENSE) |
| RoomFormer | MIT | weights via polybox (no separate licence) | [RoomFormer](https://github.com/ywyue/RoomFormer) |
| PolyRoom / FRI-Net / SAI3D | none declared | — | [PolyRoom](https://github.com/3dv-casia/PolyRoom); [FRI-Net](https://github.com/Daisy-1227/FRI-Net); [SAI3D](https://github.com/yd-yin/SAI3D) |
| HEAT | "Other" | — | [HEAT](https://github.com/woodfrog/heat) |
| Cloud2BIM | MIT | Kladno cloud on Zenodo | [Cloud2BIM](https://github.com/VaclavNezerka/Cloud2BIM) |
| IfcOpenShell | LGPL-3.0 | — | [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) |
| SAM 2 / SAM 3 | Apache-2.0 / SAM License (commercial OK, restrictions) | — | [SAM 2](https://github.com/facebookresearch/sam2); [SAM 3 summary](https://roboflow.com/model-licenses/segment-anything-3) |
| pyRANSAC-3D | Apache-2.0 | — | [GitHub](https://github.com/leomariga/pyRANSAC-3D) |
| Structured3D data | MIT code; data non-commercial research only | — | [HF agreement (via snippet)](https://www.huggingface.co/datasets/Pointcept/structured3d-compressed/tree/main) |
| ScanNet data | Non-commercial (secondary) | — | [SpatialBench (via snippet)](https://arxiv.org/pdf/2605.27367) |

### Inferences
- Even MIT-licensed models whose released checkpoints were trained on ScanNet/Structured3D/S3DIS may inherit dataset restrictions on the *weights*; safest path is retraining on owned/licensed data and keeping a provenance register (code licence, weight licence, training-data licence) per model.
- Avoid repos with no licence (default: all rights reserved) in product code.

### Gaps
- Open3D, PCL, PDAL, CloudCompare, HEAT licence texts not opened (GitHub field "Other").
- S3DIS licence unknown; ScanNet ToU text not opened directly.
- Bonsai licence and Revit API/APS terms for SaaS resale not reviewed.
- Overall note: arXiv, Hugging Face, ISPRS/Copernicus, EC3, DFKI, NCBI and alphaXiv were unreachable from this session; allowing them would enable verification of the "(via search snippet)" figures.
