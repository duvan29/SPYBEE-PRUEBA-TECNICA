# Reality-Capture Hardware for Scan-to-BIM and Automation of Capture (state as of Nov 2026)

> Research method note: every external page fetch (navvis.com, mdpi.com, isprs-archives.copernicus.org, knowledge.navvis.com, 3dsurvey.si, lidarasbuiltdrawings.com) was blocked by the session's network allow-list. All findings below therefore come from web-search result extracts of the cited pages, not full-text reads. Numbers that are vendor claims are labeled as such. Prices come mostly from resellers and are indicative only. Several "discount" web stores (e.g. globalcapitalpower.com, line-surveying.com, stratosprecision.com, some eBay/Alibaba listings) show implausible prices, such as a FARO Orbis "on sale" at $10,300 or a BLK ARC at $15,870. They look unreliable and are excluded from the price figures.
>
> Units: 1 m² = 10.764 sq ft. 5,000 m² ≈ 53,800 sq ft. 10,000 m² ≈ 107,600 sq ft.

## 1. Terrestrial laser scanners (TLS): accuracy, time per setup, in-field registration, price

### Takeaway
TLS is still the accuracy reference for BIM-grade clouds. In 2026, flagship units reach 1.5–2.3 mm 3D point accuracy at 10 m and take about 1.5–2.5 min per full-dome scan with HDR imagery. VIS-type tracking (Leica) or Flash/automatic workflows (FARO, Trimble) do most of the registration in the field. 2026 brought a generational refresh: the Leica RTC300/500/700 replace the RTC360 and P-series, and FARO launched the Focus i.1. Hardware costs about $25k (BLK360 G2) to $80–95k (RTC700/RTC360-class).

### Cited Findings
**USIBD LOA reference (the yardstick for "BIM-grade")**
- USIBD LOA bands as reported by a secondary source: LOA10 ≈ 5–15 cm (the LOA10 unit was corrected after a reader comment, so verify it), LOA20 15 mm–5 cm, LOA30 5–15 mm, LOA40 1–5 mm, LOA50 0–1 mm. Tolerances are meant to hold 95% of the time. Validation levels: A (no check), B (overlay of two datasets), C (check with independent measurement systems) — [shelidon.it BIMpill](https://www.shelidon.it/bimpill-livello-di-accuratezza-di-un-rilievo/)
- LOA Specification v3.1 was released in January 2025 and is still the referenced version in 2026 — [LIDAR Magazine, USIBD v3.1](https://lidarmag.com/?p=15520); [LIDAR Magazine, "Accuracy Isn't a Setting" (Jun 2026)](https://lidarmag.com/2026/06/09/accuracy-isnt-a-setting/)
- Scanner datasheets usually state accuracy at 68% confidence (1σ), while LOA refers to 95%, so datasheet numbers are not directly comparable to LOA tolerances — [geobimindo, SLAM vs TLS for Scan to BIM](https://geobimindo.com/article/how-to-choose-between-slam-or-tls-for-scan-to-bim)
- One industry guide maps SLAM and drone surveys to LOA20 (15 mm–5 cm) and terrestrial scanners to LOA30–40 — [geobimindo](https://geobimindo.com/article/how-to-choose-between-slam-or-tls-for-scan-to-bim)

**Leica (2026 RTC series, replacing RTC360 and P-series)**
- June 2026: Leica launched the RTC300, RTC500 and RTC700. The series "replaces the existing Leica RTC360/LT and Leica ScanStation P30/P40/P50 product lines." A new Livelink feature in Cyclone FIELD 360 streams scan data to Hexagon GeoCloud during capture — [Leica Geosystems news, Jun 2026](https://leica-geosystems.com/about-us/news-room/news-overview/2026/06/new-leica-rtc-laser-scanner-series)
- RTC series specs: range about 85 m (RTC300), 130 m (RTC500), 270 m (RTC700). Speed up to 1M pts/s (RTC300) and 2M pts/s (RTC500/700). Angular accuracy 10″, range accuracy 1.2 mm + 10 ppm, 3D point accuracy 1.5 mm at 10 m. A reseller lists 1.9 mm at 10 m for the RTC500/700 and 3 mm at 10 m for the RTC300, which is a discrepancy — [ATG USA spec page](https://atgusa.com/product_specs/leica-rtc-series-product-specifications/); [GoGeomatics](https://gogeomatics.ca/leica-rtc-series-scanners/)
- RTC500/700: full-dome scan with HDR image in about 1 min 40 s at 6 mm @ 10 m. RTC300: about 2 min 30 s. RTC700 adds a 0.8 mm "Area Scan" mode and a full-dome resolution of 1.6 mm @ 10 m — [Global Geosystems](https://global-geosystems.com/en/leica-rtc-series-the-new-generation-of-3d-laser-scanners-rtc300-rtc500-y-rtc700/); [Leica shop comparison blog](https://shop.leica-geosystems.com/reality-capture/rtc/blog/leica-rtc-series-comparison)
- Indicative 2026 USD prices (reseller, not MSRP): RTC300 from $42,431, RTC500 from $58,431, RTC700 from $80,992 — [r-e-a-l.it](https://www.r-e-a-l.it/capture/equipment/terrestrial/rtc-series); [rtc700.com](https://www.rtc700.com/)
- RTC360 (legacy, now replaced): 1.9 mm @ 10 m and 2.9 mm @ 20 m, up to 2M pts/s, 0.5–130 m range, VIS (Visual Inertial System) registration — [thefuture3d RTC360 vs FARO Premium](https://www.thefuture3d.com/equipment/compare/leica-rtc360-vs-faro-focus-premium/); [Surveyingpedia 2026 guide](https://surveyingpedia.com/guides/handheld-slam-laser-scanner)
- RTC360 list price about $93,266 (secondary guide). A 2020 comparison gave 48,442 in an unspecified currency, which is outdated — [Alibaba Leica guide](https://electronics.alibaba.com/buyingguides/leica-3d-scanner-guide-which-model-fits-your-workflow); [hagaeus.se 2020 PDF](https://hagaeus.se/wp-content/uploads/2020/05/A-comparison-of-scans-v1.2.pdf)
- RTC360 + VIS + Cyclone REGISTER 360 PLUS "will automatically place project data on real-world coordinates and complete a registration with little to no manual assistance" — [Leica Cyclone REGISTER 360 PLUS](https://leica-geosystems.com/products/laser-scanners/software/leica-cyclone/leica-cyclone-register-360)
- BLK360 G2: full-dome scan plus spherical images in about 20 s. Four settings of 7, 13, 30 or 75 s, at 680,000 pts/s. VIS built in — [Leica BLK360 product page](https://leica-geosystems.com/products/laser-scanners/scanners/leica-blk360); [thefuture3d BLK360 G2 vs RTC360](https://www.thefuture3d.com/equipment/compare/leica-blk360-g2-vs-rtc360/)
- BLK360 G2 price: typical new about $27,300, or about $27–38k (secondary sources, which conflict) — [echosurveying BLK360 review 2025](https://echosurveying.com/blog/leica-blk360-review-2025-complete-comparison-of-all-versions-features-and-workflow-integration); [Kuker-Ranken](https://kukerranken.com/product/leica-blk360-g2-3d-imaging-laser-scanner-951110/)

**FARO**
- Focus 2024 generation (Core / Premium / Premium Max): the same published 3D accuracy of 2 mm @ 10 m and 3.5 mm @ 25 m, ±1 mm ranging error, 19″ angular accuracy. Range 100 m (Core), 200 m (Premium), 400 m (Premium Max). Up to 2M pts/s. "Flash" registration workflow — [thefuture3d Core vs Premium vs Premium Max](https://www.thefuture3d.com/equipment/compare/faro-focus-core-vs-premium-vs-premium-max/); [thefuture3d RTC360 vs Premium](https://www.thefuture3d.com/equipment/compare/leica-rtc360-vs-faro-focus-premium/)
- Focus prices are poorly sourced. Premium Max $62,000–73,000, or $69,990 base. Core figures range from $5,999 (implausible) to about $28,000 — [Alibaba FARO guide](https://electronics.alibaba.com/buyingguides/faro-focus-scanner-guide-core-vs-premium-vs-max) (low reliability)
- 15 Sep 2026 (INTERGEO): FARO (announcing as "FARO INSIGHT") launched the Focus i.1 and i.1 X terrestrial scanners. Vendor "object accuracy up to 0.9 mm", which is an object-scanning figure, not a project tolerance. The i.1 X adds a mountable GNSS/RTK receiver and 400 m range. Launched alongside SCENE 2027, which a trade outlet headline says "cleans the cloud" — [GIM International](https://www.gim-international.com/news/faro-insight-puts-workflow-first-with-new-focus-and-rovi-releases); [Geoinformatics](https://www.geoinformatics.com/faro-insight-unveils-focus-i-1-scanners-and-rovi-i-1/); [BIM Digest](https://www.bimdigest.com/blog/spotlight-faro-focus-i1/)

**Trimble / Z+F**
- Trimble X9: 2.3 mm @ 10 m and 3.0 mm @ 20 m 3D accuracy. Up to 1M pts/s. Automatic self-levelling, which the RTC360 lacks — [thefuture3d X9 vs RTC360](https://www.thefuture3d.com/equipment/compare/trimble-x9-vs-leica-rtc360/)
- Trimble X12 (built with Z+F): 2.2 mm @ 20 m 3D point accuracy, 250 m range — [thefuture3d X12 vs RTC360 vs Premium](https://www.thefuture3d.com/equipment/compare/trimble-x12-vs-leica-rtc360-vs-faro-premium/)
- Used prices only (about 2024 listing): Trimble X7 with T10x tablet $28,495; X9 scanner-only $23,100 — [allterracentral](https://allterracentral.com/collections/3d-laser-scanners)

**Independent accuracy (static vs SLAM, same building)**
- Applied Sciences 2025 (DOI 10.3390/app15148053), indoor commercial building with long corridors and recesses. Overall RMSE: Leica RTC360 1.2 mm, Trimble X7 5.4 mm, Emesent Hovermap ST-X 7.3 mm, FARO Orbis 8.8 mm. GeoSLAM ZEB Horizon RT performed worst (noise > 9 mm). Point clouds are public on Zenodo — [MDPI Applied Sciences](https://www.mdpi.com/2076-3417/15/14/8053); [Zenodo 19127646](https://zenodo.org/records/19127646)
- "All three [RTC360, Focus Premium, X9] deliver accuracy that exceeds the requirements of virtually all commercial AEC projects." Real project accuracy depends more on registration, control, environment and overlap than on single-point specs — [thefuture3d 2026 comparison](https://www.thefuture3d.com/blog/3d-scanner-comparison-2026/)

### Inferences
- With setup and move time added to about 1.7–2.5 min of scanning, a 2026 high-end TLS should average about 3–5 min per station. That is roughly 12–20 setups per hour, or 100–150 per 8-hour day in open interiors. This is my estimate, not a vendor figure.
- At 1.5–2.3 mm (1σ) single-point accuracy, ×2 for 95% gives about 3–5 mm. TLS plus a sound registration and control network comfortably meets LOA30 (5–15 mm) and can reach LOA40 (1–5 mm) at short range with good control.
- VIS (Leica), Flash/auto-registration (FARO) and Livelink cloud streaming (Leica 2026) mean registration now largely happens during capture. The remaining office step is QA and constraint checks, not manual target picking.

### Gaps
- No official 2026 MSRP for the RTC series, FARO Focus i.1 or Trimble X9/X12. Leica, FARO and Trimble do not publish US list prices, and reseller figures conflict.
- Z+F IMAGER 5016A specs and price were not retrieved.
- The Trimble "ST30" (Sep 2026) appeared only in a mixed search snippet and is unverified.
- I found no independent 2026 test of the RTC series or Focus i.1.

## 2. Mobile SLAM (handheld, backpack, trolley): accuracy, coverage speed, colorization, price, LOD 300 suitability

### Takeaway
2025–2026 SLAM devices reach about 4–10 mm local (1σ) accuracy in favorable indoor conditions, and independent indoor RMSE runs about 6–9 mm for the best units. Absolute accuracy across a whole building depends on loop closures and control points. Devices range from about $13k (XGRIDS K1) to about $100k (NavVis VLX 3). They capture roughly 10× faster than TLS, and their clouds are generally adequate for LOD 300 architecture and most MEP routing (LOA20 to low-LOA30). Tight-tolerance elements still need TLS or control.

### Cited Findings
**NavVis**
- VLX 3: 5 mm point cloud accuracy (1σ local) measured in a dedicated 500 m² test environment. Absolute building-wide accuracy depends on environment size and survey control points. Two 32-layer LiDARs (300 m raw range), four 20 MP cameras, 1.5 h on a hot-swappable battery pair, about 8.5 kg, IP42. VLX 2 was rated at 6 mm — [Geo Week News](https://www.geoweeknews.com/articles/navvis-vlx-3-mobile-mapping-slam-lidar-surveying/); [NavVis VLX 3 datasheet PDF](https://dmg-manual-live.s3.ap-south-1.amazonaws.com/Production/exb_doc/646/123469/Datasheet_-_NavVis_VLX_3.pdf); [thefuture3d VLX 3 guide](https://www.thefuture3d.com/blog/navvis-vlx3-review-specifications-guide/)
- VLX 3 price: no official list price. One unverified third-party listing shows about $100,500–101,500 — [Accio](https://www.accio.com/plp/navvis-vlx-3)
- VLX 4 (announced 14 Sep 2026, Munich): triple-LiDAR architecture, "first wearable reality capture device to achieve a native point cloud resolution of 3 mm." A NavVis comparison table lists 4 mm accuracy (1σ), which is provisional — [NavVis blog, VLX 4](https://www.navvis.com/blog/introducing-navvis-vlx-4-a-breakthrough-in-dynamic-reality-capture-delivering-exceptional-detail-at-speed); [NavVis VLX 4 page](https://www.navvis.com/vlx-4)
- Original VLX: manufacturer-stated absolute accuracy of 6 mm at 68% and 15 mm at 95% confidence in controlled environments. An independent Remote Sensing 2024 study (Gharineiat et al.) tested the VLX and BLK2GO against a total station baseline, with indoor results more accurate (about 5 mm) than outdoor — [MDPI Remote Sensing 16(17):3256](https://www.mdpi.com/2072-4292/16/17/3256)
- A 2025 ISPRS paper specifically evaluates VLX 2 and VLX 3 geometric accuracy for indoor use. Numbers were not retrievable — [ISPRS Archives XLVIII-1-W6-2025-107](https://isprs-archives.copernicus.org/articles/XLVIII-1-W6-2025/107/2025/isprs-archives-XLVIII-1-W6-2025-107-2025.pdf)
- NavVis MLX is a handheld with the same ecosystem — [Geo Week News, MLX launch](https://www.geoweeknews.com/articles/navvis-handheld-laser-scanner-mlx-mobile-mapping-slam-lidar/) (specs and price not retrieved)

**Leica**
- BLK2GO: current Leica sheet gives 6–15 mm relative and ±20 mm absolute indoor (controlled). An older 2021 sheet said ±10 mm indoor. $37,500 on the Leica shop — [Leica shop BLK2GO](https://shop.leica-geosystems.com/leica-blk/blk2go/buy); [thefuture3d BLK2GO vs PULSE](https://www.thefuture3d.com/equipment/compare/leica-blk2go-vs-blk2go-pulse/)
- BLK2GO PULSE: ±2 cm indoor accuracy, range noise ±15 mm real-time and ±5 mm post-processed. 0.5–10 m range, indoor-only, live colorized first-person capture. $42,800 on the Leica shop (a reseller lists $35,500) — [Leica shop BLK2GO PULSE](https://shop.leica-geosystems.com/reality-capture/blk2go-pulse/buy); [thefuture3d BLK2GO PULSE](https://www.thefuture3d.com/equipment/leica-blk2go-pulse/)

**FARO**
- FARO Orbis: up to 5 mm in mobile SLAM mode and up to 2 mm in stationary "Flash" mode (about 15 s static scans). 120 m range in SLAM, 80 m in Flash. 3.6 kg with datalogger. Price about €46,000–50,000 (European reviews) — [laserscanner.info Orbis vs BLK2GO vs VLX](https://www.laserscanner.info/en/faroorbis-vs-leicablk2govsnavvisvlx); [3dsurvey.si, 7 SLAM scanners tested](https://3dsurvey.si/7-slam-scanners-put-to-the-test/); [survey-tech.co.uk](https://survey-tech.co.uk/products/faro-orbis-mobile-laser-scanner)
- FARO Rovi i.1 (Sep 2026): handheld hybrid visual + LiDAR SLAM developed with Manifold Tech, sold bundled with Sphere XG and SCENE. 200,000 pts/s, ≤1 cm accuracy with the optional GNSS accessory, 1.24 kg. One page cites a tech-sheet figure of 8 mm against 26 reference points over 250 m² (unconfirmed by FARO). Also captures Gaussian splats — [FARO Rovi page](https://www.faro.com/en/Products/Hardware/Rovi); [point3D, Sep 16 2026](https://www.point3d.com/2026/09/16/faro-rovi-i-1/); [radiancefields.com FARO](https://radiancefields.com/platforms/faro)
- GeoSLAM / FARO ZEB Horizon RT: vendor "relative accuracy up to 6 mm" (GeoSLAM Connect v2+). It performed worst indoors in the 2025 independent test (noise > 9 mm), so it is an older generation — [MDPI Applied Sciences 2025](https://www.mdpi.com/2076-3417/15/14/8053)

**Emesent**
- Hovermap ST-X: vendor ±15 mm general and ±10 mm indoor/underground. Independent indoor RMSE 7.3 mm, the best SLAM unit in the 2025 test. Price about CAD 68,600 — [MDPI Applied Sciences 2025](https://www.mdpi.com/2076-3417/15/14/8053); [Candrone](https://candrone.com/products/emesent-hovermap-st-x)
- Emesent GX1: 5–10 mm global accuracy with SLAM, 15 mm with RTK/PPK. Emesent data now flows natively into Trimble Connect and Trimble Business Center (announced INTERGEO, Sep 2026) — [Geo Week News](https://www.geoweeknews.com/articles/emesents-mobile-slam-scanners-integrated-into-trimble-connect-and-trimble-business-center/); [DroneDJ, 16 Sep 2026](https://dronedj.com/2026/09/16/emesent-trimble-lidar-drone-data/)

**XGRIDS**
- Lixel L2 Pro: processed accuracy 1 cm relative and 3 cm absolute (RMSE), 0.5 cm cloud thickness, up to 300 m range depending on configuration, 320,000–640,000 pts/s. Lixel K1: ±1.2 cm relative, ≤3 cm absolute, about 0.1–40 m range, about 200,000 pts/s — [radiancefields L2 Pro](https://radiancefields.com/xgrids/lixel-l2-pro); [heliguy K1 vs L2 Pro](https://www.heliguy.com/blogs/posts/xgrids-k1-vs-l2-pro/); [rapidscan3d](https://www.rapidscan3d.com/blogs/news/xgridslixelk1vsl2procomparison)
- Indicative prices: L2 Pro $25,000–51,000 and K1 $12,000–14,000, with no fixed public price — [alpinerealitycapture](https://www.alpinerealitycapture.com/blog/xgrids-l2-pro-k1-and-portalcam-comparison); [heliguy](https://www.heliguy.com/blogs/posts/which-xgrids-scanner-is-best-for-me-l2-pro-vs-k1-vs-portalcam/)
- Independent component-based Scan-to-BIM comparison (Sevenich, Kemand, Malkwitz, ISPRS 2025). Average deviations: XGRIDS L2 Pro 6.43 mm (best), NavVis VLX2 in between, XGRIDS K1 9.86 mm (worst), all < 1 cm. VLX2 is a "mature device with consistent quality". L2 Pro is "technically and economically promising" (RTK, local processing, higher density). K1 suits smaller scenarios, with limited range and homogeneity — [ISPRS Archives XLVIII-1-W6-2025-213](https://isprs-archives.copernicus.org/articles/XLVIII-1-W6-2025/213/2025/); [ResearchGate](https://www.researchgate.net/publication/399273031_Comparison_of_mobile_laser_scanning_systems_for_component-based_scan-to-BIM_evaluation_NavVis_VLX2_XGRIDS_L2_Pro_and_XGRIDS_K1)

**LOD 300 / BIM suitability**
- "Mobile and SLAM scanners trade point density for speed, so they typically cap around LOD 300. High-LOD work needs a registered terrestrial scan" — [ViBIM Global, 10 scanners for BIM](https://vibimglobal.com/blog/3d-laser-scanners/)
- With appropriate post-processing (ICP alignment and smoothing), new-generation SLAM devices deliver accuracy "sufficient for most common surveying applications". Static units remain the better choice where accuracy matters most — [MDPI Applied Sciences 2025](https://www.mdpi.com/2076-3417/15/14/8053)
- Handheld SLAM accuracy typically 1–5 cm, or 10–30 mm, depending on source — [Surveyingpedia 2026](https://surveyingpedia.com/guides/handheld-slam-laser-scanner); [icelabz](https://icelabz.co.uk/surveys/measured-building-survey/pillars-2-laser-vs-total-station-vs-handheld/)
- Leica Pegasus TRK is a vehicle-mounted mobile mapping system. No building-interior specs or price were retrieved.

### Inferences
- Converting 1σ to 95% (×2): VLX 3 at 5 mm gives about 10 mm locally, which sits inside LOA30 (5–15 mm). VLX 4 at 4 mm gives about 8 mm. Orbis or Hovermap at 7–9 mm independent RMSE gives about 15–18 mm, at the LOA20/LOA30 boundary. XGRIDS at 3 cm absolute and the BLK2GO PULSE at 2 cm give LOA20. So for LOD 300 architecture (walls, slabs, openings) and MEP routing, top-tier SLAM with control points is usually enough. Clash-critical MEP retrofit, structural steel connections and prefabrication tolerances need TLS (LOA30–40).
- The market split by 2026: premium wearables at $90–100k+ (NavVis), mid-tier SLAM with static-scan modes at $40–70k (Orbis, BLK2GO/PULSE, Hovermap), and low-cost Chinese SLAM at $12–50k (XGRIDS) that independent tests rank surprisingly close to NavVis.
- Hybrid "SLAM + static stop-and-go" modes (Orbis Flash, RTK on the L2 Pro and GX1, GNSS on Rovi) are blurring the TLS/SLAM boundary.

### Gaps
- No official NavVis VLX 3, VLX 4 or MLX prices. No full numbers from the ISPRS 2025 VLX 2 vs VLX 3 paper (fetch blocked).
- Leica Pegasus TRK is a vehicle system with little relevance to building interiors. No spec found.
- "Trimble X7 + Trimble SLAM": I found no Trimble-branded handheld SLAM scanner as of Nov 2026. Trimble's SLAM strategy appears to be partner integrations (Emesent into Trimble Connect and TBC, Sep 2026).
- No independent 2026 tests of the VLX 4 or Rovi i.1.

## 3. Robotic and autonomous capture (Spot + BLK ARC / X7 / RTC360, drones, ground robots): throughput and real deployments

### Takeaway
Autonomous capture is commercially mature but niche. Spot carrying a Leica BLK ARC (SLAM) or a Trimble X7 or RTC360 (stop-and-go TLS) can repeat pre-defined missions without an operator, scheduled at night, with self-charging docks. Documented throughput is modest: about 100 TLS scans in 10 hours (Mace / X7 trial). The value is repeatability and labor savings for progress monitoring, for example 20 hours per week saved at Pomerleau (photos), rather than raw speed versus a walking operator. Indoor drones (Elios 3, BLK2FLY) cover inaccessible spaces at cm-level accuracy.

### Cited Findings
- Leica BLK ARC: the first officially certified reality capture payload for Boston Dynamics Spot. Missions run via Autowalk without a person present. Routes can be drawn on a drawing or BIM model and Spot avoids obstacles. 690 g, powered by Spot — [GIM International](https://www.gim-international.com/content/news/leica-and-boston-dynamics-unveil-certified-reality-capture-for-spot); [AEC Magazine](https://aecmag.com/technology/leica-delivers-autonomous-scanning-with-robots-and-drones-leica-blk2fly/); [Boston Dynamics webinar](https://bostondynamics.com/webinars/autonomous-reality-capture-for-industrial-facilities/)
- BLK ARC specs and price: 420,000 pts/s LiDAR plus 12 MP camera. Internal memory holds 24 h of scanning compressed or 6 h uncompressed. $55,425 on the Leica shop (2021 launch price was about $46,000). Spot itself is extra; no standalone Spot price was found — [Leica shop BLK ARC](https://shop.leica-geosystems.com/leica-blk/blk-arc/buy); [aniwaa](https://www.aniwaa.com/product/3d-scanners/leica-geosystems-blk-arc/)
- BLK ARC + Spot academic test for heritage surveying is a preliminary study, not a production deployment — [ResearchGate (Robotics for Heritage Surveying)](https://www.researchgate.net/publication/381198307_Robotics_for_Heritage_Surveying_preliminary_test_on_Leica_BLK_ARC_SpotR_toward_autonomous_3D_mapping)
- Trimble turnkey autonomous robotic scanning (Oct 2021): Trimble X7, FieldLink, a rugged tablet, Spot Enterprise and a self-charging dock for both Spot and the X7. Waypoint missions "can be scheduled to run on a regular and consistent basis." A composite point cloud is built in real time on the tablet before leaving the site. Hensel Phelps testimonial (vendor-sourced) — [Trimble news, 19 Oct 2021](https://news.trimble.com/2021-10-19-Trimble-Releases-Turnkey-Autonomous-Robotic-Scanning-Solution); [Lidar News](https://lidarnews.com/autonomous-robotic-3d-laser-scanning-system/)
- Mace trial with the Trimble X7 on Spot ("Setanta"): 100 scans in a 10-hour period — [Construction Management (UK)](https://constructionmanagement.co.uk/trimble-goes-laser-scanning-with-bostons-robot-dog/)
- Leica RTC360 on Spot (Feb 2021): Spot "does the walking and stationing of individual scans" — [Leica news, Feb 2021](https://leica-geosystems.com/en-us/about-us/news-room/news-overview/2021/02/2021_02_22_boston_dynamics)
- Pomerleau (Boston Dynamics case study, about 2024): Spot plus HoloBuilder on a 500,000 sq ft project saves about 20 h/week of staff photo capture, with autonomous runs from repeatable locations outside work hours. This is 360° photo documentation, not laser scanning — [Boston Dynamics, Pomerleau](https://bostondynamics.com/case-studies/pomerleau/)
- Turner Construction uses DroneDeploy's robotics solution for daily autonomous capture and 360° walkthroughs, with "inspection time cut by over 95%" (vendor-reported) — [Boston Dynamics, Turner](https://bostondynamics.com/case-studies/turner-construction-uses-ground-robots-to-cut-inspection-time-by-over-95-percent/)
- Suffolk Construction: qualitative claims of more consistent walkthroughs and documentation — [Florida Weekly](https://www.floridaweekly.com/articles/fort-myers-arts-and-entertainment-news/fort-myers/bonita-springs/meet-spot-suffolk-constructions-robot-dog-2/)
- Leica BLK2FLY (autonomous flying scanner): <20 mm relative and 40 mm absolute without GNSS (1σ). Indoor mode reduces the minimum obstacle-avoidance distance to 1.3 m. Radar can miss thin, glossy, transparent or dark objects — [Leica shop BLK2FLY](https://shop.leica-geosystems.com/reality-capture/blk2fly/buy)
- Flyability Elios 3 Surveying Payload (indoor caged drone): vendor about ±6 mm (1σ) precision for the Rev 7 payload, and global drift about 0.16% after FARO Connect processing. The product page lists ±1.8 cm (1x) and ±1.2 cm (1.5x) — [Flyability accuracy report PDF](https://www.flyability.com/hubfs/Knowledge%20Base%20Files/Documents/Surveying%20Payload/Surveying%20Payload%20Accuracy%20Report.pdf); [Flyability Surveying Payload](https://www.flyability.com/elios-3-surveying-payload)

### Inferences
- 100 TLS scans in 10 h (about 10 per hour) is slower than a skilled human with a 2026 TLS (about 12–20 per hour, my estimate). Robots win on unattended night or weekend operation, exact repeatability of stations for 4D comparison, and labor cost, not on per-hour speed.
- Spot + BLK ARC (SLAM, 420k pts/s) suits recurring progress capture at LOA20-type accuracy. Spot + X7/RTC (TLS) suits recurring as-built at LOA30. Neither replaces a first full-building survey with control.
- For a Spybee-type platform, automation potential lies in scheduled robot missions feeding cloud registration and comparison against the BIM model. All parts exist commercially: Autowalk/FieldLink missions, Livelink/GeoCloud streaming, and cloud processing in IVION or Cintoo.

### Gaps
- No independent, quantified construction case study of Spot + BLK ARC (m²/h, accuracy on site). Boston Dynamics and Leica material is promotional.
- No current Spot list price; it is commonly cited at about $75k base but I found no source in this session.
- Skydio indoor/outdoor 3D Scan: no accuracy or construction data found.
- Hilti construction robots (Jaibot is a drilling robot, not capture) and other autonomous ground robots (Doxel, Scaled Robotics, Civ Robotics): not researched due to tool budget.

## 4. Consumer and prosumer capture (iPhone/iPad LiDAR apps, Dot3D, Matterport Pro3): accuracy limits and acceptable uses

### Takeaway
Phone and tablet LiDAR gives cm-level accuracy at room scale (about 1–3 cm static) but drifts to decimetres over whole floors (±10–30 cm). That makes it acceptable only for LOA10–20 tasks: space planning, small renovations, quick documentation and verifying small areas. Matterport Pro3 (±20 mm @ 10 m) sits at LOA20 and is used for LOD 200–300 architectural as-builts. It is not suitable for MEP coordination or structural tolerances.

### Cited Findings
- iPad Pro 2021 vs Trimble TX8 in a university hall: static acquisition reached 2.84 cm RMS (about ±1–2 cm). Moving acquisition degraded to about ±30 cm on features longer than 4 m. The sensor costs about 2.5% of a TLS — [Taylor & Francis 2024 (Indoor mapping accuracy, Apple LiDAR vs TLS)](https://www.tandfonline.com/doi/full/10.1080/16874048.2024.2408839)
- iPhone 13 Pro, four apps (3D Scanner App, PolyCam, SiteScape, Scaniverse) in about 200 m² indoors against a Z+F IMAGER 5016 reference: PolyCam and SiteScape produced less noisy clouds than 3D Scanner App and Scaniverse — [MDPI Digital 3(4):30, 2023](https://www.mdpi.com/2673-7418/3/4/30)
- iPhone 12 Pro + PolyCam vs FARO Focus: only about 62% of points within 1 inch of the reference (2021 thesis, older hardware) — [Gillihan, UC Denver 2021](https://artsandmedia.ucdenver.edu/docs/librariesprovider27/ncmf-docs/theses/gillihan_thesis_fall2021.pdf?sfvrsn=8f32a1ba_2)
- iPad Pro static scanning: deviations under 1 mm from best-fit planes (local noise only). Recommends a 1–1.5 m scanning distance and avoiding large posture changes for Scan-to-BIM — [Teo & Yang 2023, Developments in the Built Environment](https://doaj.org/article/9cbab8e9cd04423aae61f174ca458b1e)
- iPad Pro over a large space reached about ±10 cm absolute and fell short of USIBD-style requirements (TUHH report, not peer-reviewed) — [TUHH](https://tore.tuhh.de/bitstreams/d888f6e1-7923-4027-bd2f-518d76b24b2e/download)
- iPhone LiDAR vs TLS for BIM elements: about 27% of measurements (windows, doors, columns, walls) were mm-level and about 73% cm-level — [UTHM IJIE](https://publisher.uthm.edu.my/ojs/index.php/ijie/article/download/15990/6847/88369)
- Dot3D (DotProduct): requires a LiDAR iPad Pro or iPhone Pro. Claims "verifiable accuracy" with a targeting workflow using known reference measurements. Exports E57, LAS and PTS. These are vendor claims only — [App listing](https://apps.appfollow.io/ios/dot3d-precision-lidar-scanner/1641016966?country=il)
- Matterport Pro3: ±20 mm @ 10 m, 100 m max range. Processed models use 20 m depth per scan, while E57/BIM deliverables carry the 100 m data. Revit plugin and as-built BIM/CAD conversion. Camera-only kit AUD 11,825–12,650, plus a mandatory subscription for processing — [Matterport store, Pro3 As-Built bundle](https://matterport.com/en-gb/store/product/cam-mc3004-x); [CR Kennedy](https://survey.crkennedy.com.au/products/mc300pk/matterport-pro-3-3d-lidar-camera-performance-kit)
- A consultancy rates Pro3 accuracy as suitable for LOD 200 BIM and LOD 300 architectural elements (walls, doors, windows, slabs), but not tighter tolerances — [realitycaptureexperts, Matterport accuracy](https://realitycaptureexperts.com/matterport-accuracy/)
- iPhone 12 Pro LiDAR about ±6–8 cm vs FARO/Leica ±2–3 mm (review) — [3D Mag](https://www.3dmag.com/3d-scanners/handheld-lidar-3d-scanner-what-its-good-at/)

### Inferences
- Phone LiDAR is acceptable for single rooms, quick field verification, punch lists and LOA10–20 space planning. It is unacceptable as the primary source for a multi-floor LOD 300 model, because drift grows with path length.
- A practical niche for a Spybee-like app: crowd-sourced phone scans by site staff for progress or room-level checks, registered to a TLS/SLAM master cloud.

### Gaps
- No independent accuracy data for Dot3D or Intel RealSense rigs. RealSense hardware availability has been uncertain since Intel's 2021 exit announcement (not verified this session).
- No 2025–2026 study on the latest iPhone/iPad Pro LiDAR generations.

## 5. Automated registration and processing pipelines (Cyclone REGISTER 360 PLUS, FARO SCENE / Sphere XG, NavVis IVION, Trimble RealWorks / FieldLink, Cintoo)

### Takeaway
Registration is now largely automatic: VIS or Flash plus auto-alignment for TLS, and SLAM with loop closure and automatic control-point detection for mobile. In 2026 vendors are pushing streaming during capture (Leica Livelink to Hexagon GeoCloud) and cloud processing (NavVis IVION, Cintoo, FARO Sphere XG). However, I found no published, independent benchmark of processing time per scan or per 1,000 m².

### Cited Findings
- Cyclone REGISTER 360 PLUS uses RTC360 VIS data to auto-place and register scans "with little to no manual assistance". It is "optimized for projects up to 500 scans" — [Leica REGISTER 360 PLUS](https://leica-geosystems.com/products/laser-scanners/software/leica-cyclone/leica-cyclone-register-360)
- Leica claims "up to 20× speed improvement" in processing and import of scan and image data in REGISTER 360 PLUS (relative claim, no throughput figure) — [thefuture3d Leica Cyclone review 2026](https://www.thefuture3d.com/software/leica-cyclone/)
- REGISTER 360 2022.1 release notes: the optional re-observation algorithm for BLK2GO / BLK ARC scans increases processing time by up to 20–25% — [Leica release notes 2022.1.0](https://rcdocs.leica-geosystems.com/docs/cyclone-register-360-2022-1-0-cyclone-register-360-release-notes)
- Leica Livelink (2026) streams scan data from Cyclone FIELD 360 to Hexagon GeoCloud during capture — [Leica news, Jun 2026](https://leica-geosystems.com/about-us/news-room/news-overview/2026/06/new-leica-rtc-laser-scanner-series)
- Trimble X7 + FieldLink (also on Spot): the composite registered cloud is created in real time on the tablet before leaving the site — [Trimble news 2021](https://news.trimble.com/2021-10-19-Trimble-Releases-Turnkey-Autonomous-Robotic-Scanning-Solution)
- NavVis IVION processing: a live progress bar with an estimated time remaining, parallel processing of several datasets, and early control-point verification. No published benchmark — [NavVis IVION data processing](https://www.navvis.com/ivion/data-processing)
- Cintoo: direct import of NavVis VLX/MLX data from IVION. Needs at least 400 MB RAM per 10 million pixels to process. Parallel scan processing depends on cores and RAM — [Cintoo help](https://help.cintoo.com/en/support/solutions/articles/101000461502-upload-navvis-vlx-or-mlx-from-ivion)
- FARO Rovi i.1 ships bundled with Sphere XG (cloud) and SCENE. SCENE 2027 is marketed as cleaning the cloud automatically — [GIM International](https://www.gim-international.com/news/faro-insight-puts-workflow-first-with-new-focus-and-rovi-releases); [BIM Digest](https://www.bimdigest.com/blog/spotlight-faro-focus-i1/)
- Emesent Automated Ground Control: machine learning detects reflective targets, which serve as constraints to remove drift and slips. A non-rigid transformation georeferences the cloud — [Emesent GCP](https://www.emesent.com/gcp/)
- Emesent Hovermap and GX1 data now flows natively into Trimble Connect and Trimble Business Center (Sep 2026) — [Geo Week News](https://www.geoweeknews.com/articles/emesents-mobile-slam-scanners-integrated-into-trimble-connect-and-trimble-business-center/)

### Inferences
- The field-to-cloud gap is shrinking from days (2015-era target-based TLS) to hours or the same day. TLS is pre-registered in the field (VIS/FieldLink) or streamed (Livelink). SLAM is processed in the cloud (IVION) or locally (XGRIDS LixelStudio), then pushed to collaboration platforms (Cintoo, GeoCloud, Trimble Connect).
- The remaining manual bottlenecks are QA of registration constraints, control-point verification and cleaning of moving objects. These are the steps a platform could automate further.

### Gaps
- No vendor-neutral processing-time numbers (hours per 1,000 m², or minutes per scan) for REGISTER 360, SCENE/Sphere XG, IVION, RealWorks or Cintoo. These would need timed internal tests.
- Trimble RealWorks / Perspective auto-registration details were not retrieved.

## 6. Hybrid strategies (TLS control + SLAM, GCPs, RTK-GNSS) and recommendations by building type

### Takeaway
Best practice in 2026 is a control-anchored hybrid. Establish a total-station or TLS control framework first, sized to the building. Capture the bulk with SLAM, using loop closures and surveyed control points. Spot-scan critical zones with TLS (plant rooms, structural connections, façades of heritage buildings). Merge everything in one registration environment. RTK-GNSS options (FARO Focus i.1 X, Rovi GNSS, XGRIDS L2 Pro, Emesent GX1) help on exteriors but not indoors.

### Cited Findings
- NavVis: surveyed control points used in post-processing generally fix a drifting dataset, but "control points cannot always save twisted or tilted scans". Loop closures remain the most effective way to minimise drift. Distribute control points across the area and survey them with a total station — [NavVis KB, SLAM drift](https://knowledge.navvis.com/docs/how-do-we-know-if-slam-is-drifting-or-broken-1); [NavVis KB, control points](https://knowledge.navvis.com/docs/an-introduction-to-control-points)
- Using a TLS cloud as a reference to remove SLAM drift gave about ±10 cm agreement on a levee (outdoor, linear site). This is a lower bound on what is achievable — [Penn State, TLS + SLAM for levee monitoring](https://pure.psu.edu/en/publications/combination-of-tls-and-slam-lidar-for-levee-monitoring/)
- SLAM2REF: aligning SLAM to a TLS reference map reduces error after ICP. TLS alignment agrees much better than alignment to a BIM model — [arXiv 2408.15948](https://arxiv.org/pdf/2408.15948)
- Combined SLAM + TLS for indoor mapping has been studied before (older study) — [ResearchGate, Combined use of SLAM and TLS for 3D indoor mapping](https://www.researchgate.net/publication/354211578_The_Combined_Use_of_SLAM_Laser_Scanning_and_TLS_for_the_3D_Indoor_Mapping)
- An XGRIDS partner test ran SLAM without control points against an RTC360 reference to isolate SLAM quality. Point counts: L2 Pro 185M, K1 138M, VLX 2 163M (commercial source) — [3ds-scan.de, L2 Pro vs VLX2](https://www.3ds-scan.de/en/xgrids-l2-pro-vs-navvis-vlx2/)
- GNSS/RTK options: FARO Focus i.1 X (mountable GNSS/RTK), Rovi i.1 (≤1 cm with GNSS), Emesent GX1 (15 mm with RTK/PPK) — [GIM International](https://www.gim-international.com/news/faro-insight-puts-workflow-first-with-new-focus-and-rovi-releases); [FARO Rovi](https://www.faro.com/en/Products/Hardware/Rovi); [Geo Week News](https://www.geoweeknews.com/articles/emesents-mobile-slam-scanners-integrated-into-trimble-connect-and-trimble-business-center/)
- "Mobile/SLAM … typically cap around LOD 300; high-LOD work needs a registered terrestrial scan" — [ViBIM Global](https://vibimglobal.com/blog/3d-laser-scanners/)
- "Match accuracy to the deliverable" (Matterport for LOD 200–300 architecture only) — [realitycaptureexperts](https://realitycaptureexperts.com/matterport-accuracy/)

### Inferences (recommendations by building type; synthesis, not sourced verbatim)
- **Residential high-rise (repetitive floors, many small rooms):** wearable or handheld SLAM (VLX 3/4, Orbis, L2 Pro) floor by floor. Survey control in stair cores and survey-grade benchmarks per floor, tied vertically through the core with a total station. Add a TLS ring on façades and roof. Phone LiDAR is acceptable for unit-level fit-out checks.
- **Commercial / office (open plates, ceilings):** SLAM for the bulk (LOD 300 architecture). Use TLS (RTC500/Focus i.1) above ceilings and in risers where MEP coordination needs LOA30. Robots (Spot + BLK ARC) for recurring progress capture during construction.
- **Industrial / MEP-heavy (plant rooms, pipe racks, plants):** TLS-dominant (LOA30–40), because dense occlusion and small-diameter pipes punish SLAM noise (7–9 mm RMSE, cm-level thickness). Use SLAM only for connecting corridors or context. Spot + X7/RTC for repeated capture in hazardous areas. Elios 3 for confined spaces, tanks and ducts.
- **Heritage:** TLS (high resolution, for example the RTC700 0.8 mm area scan) with a total-station control network for ornament and deformation analysis. SLAM for rapid documentation of attics and secondary spaces. Drones (BLK2FLY or photogrammetry) for roofs. The BLK ARC + Spot heritage test exists but is preliminary.
- **Rule of thumb:** treat datasheet 1σ figures as half of the 95% LOA tolerance. Specify LOA per element class in the scope (for example LOA30 structure and MEP mains, LOA20 finishes) and validate with independent control (USIBD validation level C).

### Gaps
- No peer-reviewed building-interior study quantifying exactly how much control points improve SLAM absolute accuracy (for example, X mm with vs without control on a 10,000 m² building).
- No AEC-firm case study found that documents a full hybrid TLS + SLAM workflow with timings.

## 7. Total field-time benchmarks (5,000 m² and 10,000 m² buildings)

### Takeaway
On published rates, wearable SLAM captures about 1,000–1,200 m² per hour (or about 18,600–27,900 m² per day according to one contractor). TLS manages about 250 m² per hour, or about 1,900–3,700 m² per day. A 5,000 m² building is therefore about half a day with SLAM versus about 1.5–3 days with TLS. A 10,000 m² building is about one day versus about 3–6 days, before control surveys and office processing. Treat all rates as vendor or contractor figures. Partitioned interiors are slower.

### Cited Findings
- NavVis side-by-side test: about 500 m² captured in 25 min with the VLX, versus 2 h with one TLS and about 5.5 h with another TLS workflow including a total station. NavVis claims the VLX is "on average 10 times faster" while meeting standard accuracy criteria (vendor test) — [NavVis blog](https://www.navvis.com/blog/testing-navvis-vlx-side-by-side-with-a-terrestrial-laser-scanner); [NavVis VLX 2 vs TLS video](https://www.navvis.com/resources/videos/navvis-vlx-2-vs-tls)
- A contractor's 2026 cost guide: tripod TLS (Trimble X12/X9) 20,000–40,000 sq ft per day at ±2–4 mm. Mobile SLAM (VLX 3) 200,000–300,000 sq ft per day at 5 mm local accuracy — [thefuture3d 3D scanning cost guide 2026](https://www.thefuture3d.com/learn/3d-scanning-cost-guide/)
- The same provider notes that NavVis publishes no ft²/day or area-per-hour figure. Throughput depends on layout, obstructions, loop closures needed and the accuracy required — [thefuture3d VLX 3 page](https://www.thefuture3d.com/equipment/navvis-vlx-3/)
- NavVis cites a customer capturing about 1–1.5 million sq ft per week with VLX units (fleet figure, vendor-reported) — [NavVis products page](https://www.navvis.com/products)
- Robot TLS throughput: 100 scans in 10 h (Mace, Spot + Trimble X7) — [Construction Management](https://constructionmanagement.co.uk/trimble-goes-laser-scanning-with-bostons-robot-dog/)
- TLS station times (2026): RTC500/700 about 1 min 40 s per full dome with HDR; RTC300 about 2 min 30 s; BLK360 G2 about 20 s (7–75 s); FARO Orbis Flash about 15 s — [Global Geosystems](https://global-geosystems.com/en/leica-rtc-series-the-new-generation-of-3d-laser-scanners-rtc300-rtc500-y-rtc700/); [Leica BLK360](https://leica-geosystems.com/products/laser-scanners/scanners/leica-blk360); [survey-tech.co.uk Orbis](https://survey-tech.co.uk/products/faro-orbis-mobile-laser-scanner)
- Service-market pricing for VLX-type scanning: about $0.20–0.70 per sq ft for commercial projects, with minimums of $3,000 (commercial) and $10,000 (industrial) — [thefuture3d VLX 3 guide](https://www.thefuture3d.com/blog/navvis-vlx3-review-specifications-guide/)

### Inferences (my arithmetic from the cited rates; capture time only, excluding control survey, travel and processing)
| Approach | Rate used | 5,000 m² (≈53,800 sq ft) | 10,000 m² (≈107,600 sq ft) |
|---|---|---|---|
| Wearable SLAM (NavVis test rate, 500 m²/25 min ≈ 1,200 m²/h) | vendor test | ≈ 4.2 h | ≈ 8.3 h (≈ 1 day) |
| Wearable SLAM (contractor 200–300k sq ft/day ≈ 18,600–27,900 m²/day) | contractor | ≈ 0.2–0.3 day | ≈ 0.4–0.6 day |
| TLS, one operator (NavVis test, 500 m²/2 h ≈ 250 m²/h) | vendor test | ≈ 20 h (≈ 2.5 days) | ≈ 40 h (≈ 5 days) |
| TLS, one operator (contractor 20–40k sq ft/day ≈ 1,860–3,720 m²/day) | contractor | ≈ 1.3–2.7 days | ≈ 2.7–5.4 days |
| TLS + total station control (NavVis test, 500 m²/5.5 h ≈ 90 m²/h) | vendor test | ≈ 55 h (≈ 7 days) | ≈ 110 h (≈ 14 days) |
| Spot + TLS robot (≈10 scans/h; assumes ≈25–50 m² per station indoors, my assumption) | trial | ≈ 10–20 h of robot time | ≈ 20–40 h of robot time (unattended, can run nights) |
| Hybrid (SLAM bulk + TLS in about 15–20% critical areas + control) | combined | ≈ 1–1.5 days | ≈ 2–2.5 days |
- Vendor-sourced SLAM rates likely assume open, well-looped spaces. Expect lower throughput in partitioned residential or MEP-dense plant rooms, where real-world SLAM may drop toward 400–600 m²/h (my estimate, unsourced).
- Office processing roughly adds same-day to 1–2 days for SLAM (cloud processing) and 0.5–2 days for TLS registration and QA. No benchmark was found to firm this up (see Section 5 gaps).

### Gaps
- No independent, peer-reviewed field-time study for a full 5,000–10,000 m² building comparing TLS, SLAM and robots.
- The 3dsurvey.si "7 SLAM scanners put to the test" article likely has capture times but could not be fetched (domain blocked).
- Station-spacing assumptions for indoor TLS (m² per setup) are not sourced.
