# Scan-to-BIM: economics, workflow time breakdown, quality standards and business models (as of Nov 2026)

> Method note for the report writer: research ran through web search (extended mode) on 2026-11-02. Direct page fetches were **blocked by the session's network allow-list** (concrete-bureau.com, arrival3d.com, lidarmag.com all failed DNS), so every figure below comes from search-engine extracts of the cited pages, not full-page reads. Almost all pricing/time data is **vendor-published marketing content** (self-reported, not audited). Market-size figures come from paid-report publishers' summaries. Unit conversion used throughout: 1 m² = 10.764 sq ft, so **$/sq ft × 10.76 = $/m²**; 50,000 sq ft ≈ 4,645 m²; 10,000 sq ft ≈ 929 m².

## 1. Time breakdown of a manual Scan-to-BIM project (field, registration, cleaning, modeling by discipline, QA/QC, revisions)

### Takeaway
Modeling is by far the dominant cost and time sink: field capture of a ~4,600 m² building takes ~1–3 crew-days and registration ~2–5 days, while manual Revit modeling takes 4–16 weeks; the only measured multi-project dataset found (Concrete Bureau, 35 projects) puts a >15,000 m² building at LOD 400 (Arch+Struct+MEP) at 2,300–5,350 modeler-hours, with LOD 300–350 ≈ 1.35× and LOD 400 ≈ 3.0× the LOD 200 effort. A documented European case logged 8 nights scanning, 8 days registering and 300 days modeling (~95% of labor-days in modeling).

### Cited Findings
**Hours benchmarks (best available, vendor-self-reported)**
- Concrete Bureau (EU scan-to-BIM firm) publishes medians of *actual* modeler hours across 35 completed projects, grouped by floor-area band; scanning and registration are **excluded** from the hours; price = hours × rate — [Concrete Bureau, "How Much Does Scan to BIM Cost? Data From 35 Projects"](https://concrete-bureau.com/blog/how-much-does-scan-to-bim-cost)
- Detail multipliers on the base (LOD 200) hours: **LOD 300–350 ≈ ×1.35; LOD 400 ≈ ×3.0** — [Concrete Bureau](https://concrete-bureau.com/blog/how-much-does-scan-to-bim-cost)
- Example bands: building **<2,500 m² at LOD 200, full discipline set: 75–180 h**; building **>15,000 m² at LOD 400 with Arch+Struct+MEP: 2,300–5,350 h** — [Concrete Bureau](https://concrete-bureau.com/blog/how-much-does-scan-to-bim-cost)
- Firm background: Scan-to-BIM since 2021, 180–200 delivered projects, 620,000–700,000 m² of existing buildings modelled (implies avg ≈ 3,100–3,900 m²/project) — [Concrete Bureau](https://concrete-bureau.com/blog/how-much-does-scan-to-bim-cost)
- Full per-band median table could not be retrieved (page fetch blocked) — see Gaps.

**Phase durations (typical commercial building, vendor guides)**
- Scanning: **1–3 days with a two-person crew for a 50,000 sq ft (~4,645 m²) building**; registration/processing **2–5 days**; modeling **4–16 weeks depending on LOD**; QA ~3–5 days — surfaced in search across vendor workflow guides, e.g. [The Future 3D, Scan-to-BIM workflow](https://www.thefuture3d.com/blog/scan-to-bim-workflow/) and [iscano Scan-to-BIM services guide](https://iscano.com/real-world-applications-laser-scanning-lidar/scan-to-bim-services-complete-guide/) (exact page attribution of each number not verifiable because pages could not be opened)
- Alternative timeline: **3–7 business days** of cloud processing + QA, then **2–6 weeks** of BIM modeling at LOD 200–300 for a mid-sized commercial project — [vendor guides surfaced in same search; e.g. Zealot Recap point-cloud QA guide](https://zealotrecap.com/blog/point-cloud-qa-scan-to-bim/)
- The Future 3D: field scanning of 50,000 sq ft ≈ **2–3 days**; modeling **LOD 200: 1–3 weeks** (its pages disagree: 1–2 vs 2–3), **LOD 300: 3–5 weeks**, **LOD 350+: 4–8 weeks**; overall **6–12 weeks from scanning to final BIM** — [The Future 3D cost guide](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/); [The Future 3D LOD explainer](https://www.thefuture3d.com/blog/lod-levels-scan-to-bim-explained/)
- Real project log (Geo Week News case study): budget **€60,000**; **8 nights scanning (126 scan positions), 8 days registering, 300 days modeling** — [Geo Week News, "Scan to BIM: A case study"](https://www.geoweeknews.com/articles/scan-to-bim-a-case-study/) (older article; date not confirmed — likely pre-2020)
- Anecdotal (Matterport-published): a contractor needed **4–5 hours to measure one boiler room plus 4–5 days for an engineer to model it in Revit**; client Bergman reported **40% faster Revit modeling** using point clouds — [Matterport blog, Point Cloud to BIM](https://matterport.com/blog/point-cloud-to-BIM)
- Vendor estimate: manual tracing **8–40 hours per floor** — [The Scan to BIM, Point Cloud to Revit](https://www.thescantobim.com/blog/point-cloud-to-revit)

**Drivers of effort**
- MEP density is the main multiplier: LOD 300 costs **1.5–2× LOD 200 for architectural elements and 2–3× for MEP**; each added discipline raises cost **30–60%**; MEP add-on **+50–100%** for complex LOD 400 work — [The Future 3D, BIM cost per sq ft](https://www.thefuture3d.com/learn/bim-cost-per-square-foot/); [The Future 3D cost guide](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/)
- Claim that tightening LOA20→LOA30 "roughly doubles modeling time per element" and that a stricter accuracy band raises field capture time ~40% and registration ~60% appeared in a search summary of vendor guides, but a follow-up search **could not find any source that substantiates it** — treat as unverified (see Gaps) — [follow-up search found only qualitative support, e.g. Rocha & Mateus survey listing LOD, LOA, tolerance as speed factors](https://doi.org/10.3390/ijgi10080564)
- Academic survey (208 professionals, 78 countries): most scan-to-BIM modeling is done **manually, consuming excessive time**; LOD, LOA, BIM standards and precision/tolerance are listed as factors affecting modeling speed — [Rocha & Mateus 2021, ISPRS IJGI 10(8):564](https://doi.org/10.3390/ijgi10080564) (2021 data)

**Cost split field vs. modeling**
- The Future 3D example budgets: **10,000 sq ft (929 m²) architectural renovation — scanning $3,000–6,000, modeling $15,000–35,000**; **50,000 sq ft (4,645 m²) Arch+MEP — scanning $8,000–20,000, modeling $125,000–250,000** — [The Future 3D cost guide](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/)
- Another vendor: scanning is typically **5–15% of the total project budget** — [surfaced in search of 2026 vendor cost guides, e.g. iscano cost guide](https://iscano.com/real-world-applications-laser-scanning-lidar/scan-to-bim-cost-guide/); a "30% field / 70% modeling" 2026 ratio was also quoted in a search summary but a targeted search **found no page stating it** — [targeted search result set incl. The Future 3D](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/)

### Inferences
- **Labor share:** In the Geo Week case, modeling = 300/(8+8+300) ≈ **95% of labor-days**; in The Future 3D examples, scanning is ≈ **15–17%** of the (scan+model) cost for a small arch-only job and ≈ **6–7%** for an Arch+MEP 4,645 m² job. Modeling is therefore the step that must be compressed to go "months → hours"; field capture is already ~1 day per ~1,500–4,600 m² per crew.
- **Field productivity:** 4,645 m² in 1–3 crew-days ⇒ roughly **1,500–4,600 m²/crew-day** with static TLS (mobile SLAM is faster but no sourced figure was found).
- **Derived hours per 1,000 m² (from Concrete Bureau multipliers; my arithmetic, not their published table):** at the >15,000 m² band, LOD 400 full-disciplines = 2,300–5,350 h ⇒ ≤ **153–357 h per 1,000 m²** (at exactly 15,000 m²). Dividing by 3.0 gives LOD 200 ≈ 767–1,783 h (≈ **51–119 h/1,000 m²**) and multiplying by 1.35 gives LOD 300–350 ≈ 1,035–2,408 h (≈ **69–161 h/1,000 m²**). Small buildings (<2,500 m², LOD 200) run ≥ 30–72 h/1,000 m² (higher per m² for smaller floor areas).
- **Calendar estimate for 5,000–20,000 m² (manual):** LOD 300 full disciplines at ~15,000 m² ≈ 1,000–2,400 h ⇒ with 4 modelers × ~35 productive h/week ≈ **7–17 weeks modeling**, plus ~1–2 weeks field+registration and 1–3 weeks QA/revisions ⇒ **~10–22 weeks end-to-end**; a 5,000 m² LOD 300 job ≈ 350–800 h ⇒ ~3–8 weeks modeling with 2–3 modelers, ~6–12 weeks total — consistent with vendor-stated 6–12 weeks for ~4,645 m². LOD 400 roughly doubles–triples these.
- Revisions are rarely broken out by vendors; QA is typically quoted at ~3–7 days, i.e. ~5–10% of calendar time.

### Gaps
- Full Concrete Bureau hours table per area band × discipline × LOD (page fetch blocked; only two corner examples retrieved).
- No peer-reviewed controlled study of manual Scan-to-BIM hours per m² was found; academic sources are qualitative (survey) or single-case.
- No sourced split of modeling hours *by discipline* (Arch vs Struct vs MEP) beyond cost multipliers.
- No sourced data on time spent specifically on point-cloud cleaning/segmentation or on client revision rounds.
- The "LOA20→LOA30 doubles time" and "30/70 field/modeling" claims are unverified.

## 2. Market pricing (per m² / sq ft; US/Europe vs offshore India/LatAm; by LOD and discipline) and market size

### Takeaway
Published 2026 prices span more than an order of magnitude (≈ $1–$50+/m²) because quotes differ on whether scanning and MEP are included; a reasonable planning band is **~$2–5/m² for LOD 300 Arch+Struct modeling only**, **~$2–8/m² for scanning**, and **~$25–55/m² for full Arch+Struct+MEP LOD 300 all-in at US onshore rates**. Offshore (India, E. Europe, LatAm) labor is ~1/3 of onshore ($18–45/h vs ~$50–150/h). The only segment-specific market estimate (low-credibility publisher) puts Scan-to-BIM services at **USD 1.48 B (2024) → 4.29 B (2033), 13.7% CAGR**.

### Cited Findings
**All-in / modeling price ranges (US-centric vendor guides, 2026)**
- All-in scan-to-BIM (scan + registration + Revit): **$0.10–0.80/sq ft (~$1.1–8.6/m²)**; another guide gives $0.10–8.00+/sq ft depending on MEP density + LOD — [Arrival 3D cost guide 2026](https://arrival3d.com/scan-to-bim-cost-guide/); [iscano cost guide 2026](https://iscano.com/real-world-applications-laser-scanning-lidar/scan-to-bim-cost-guide/)
- LOD 300 quotes found: "Revit BIM, LOD 300: **$0.18–0.50/sq ft all-in** (~$1.9–5.4/m²)"; "Commercial office, Arch+Structural framing, LOD 300: **$0.40–1.20** (~$4.3–12.9/m²)"; "Standard office/retail LOD 300: **$1.80–3.50** (~$19–38/m²)"; "LOD 300–350 with full MEP and structure: **$0.60–1.20** (~$6.5–12.9/m²)" — [search summary of: Arrival 3D](https://arrival3d.com/scan-to-bim-cost-guide/), [iscano](https://iscano.com/real-world-applications-laser-scanning-lidar/scan-to-bim-services-complete-guide/), [The Future 3D](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/), [Eminent BIM](https://www.eminentbim.com/blog/how-much-do-bim-services-cost) (per-quote attribution not verifiable)
- Modeling only (third-party market-rate estimate, not own quote): **LOD 200 $0.15–0.25/sq ft (~$1.6–2.7/m²); LOD 300 $0.25–0.45 (~$2.7–4.8/m²); LOD 400 $0.45–0.75 (~$4.8–8.1/m²)** — [The Future 3D, BIM cost per square foot](https://www.thefuture3d.com/learn/bim-cost-per-square-foot/)
- Conflicting set from the same publisher: **LOD 200 $0.50–1.50; LOD 300 $1.50–3.50; LOD 300+MEP $2.50–5.00/sq ft (~$27–54/m²)** — [The Future 3D cost guide 2026](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/)
- Arch+Struct modeling **$0.30–1.40/sq ft (~$3.2–15/m²)**; MEP **$0.60–2.50/sq ft (~$6.5–27/m²)** — [ViBIM, Scan to BIM cost 2026](https://vibimglobal.com/blog/scan-to-bim-cost/)
- Specialized range **$0.50–10.00/sq ft**, detailed MEP **$3.00–8.00/sq ft (~$32–86/m²)** — [search summary; candidates Designheed / civilmat](https://www.designheed.com/blog/how-much-do-building-information-modelling-services-cost-in-2026/)
- Zealot Recap (US commercial): capture + registration **$0.05–0.20/sq ft (~$0.5–2.2/m²)**; modeling **$0.10–1.75/sq ft**; full scan-to-BIM **$0.35–2.00/sq ft (~$3.8–21.5/m²)** — [Zealot Recap, Costos de Scan-to-BIM (ES)](https://zealotrecap.com/es/blog/costos-scan-to-bim-modelo-revit/)
- Scanning alone: commercial laser scanning **$0.20–0.70/sq ft (~$2.2–7.5/m²)**; The Future 3D scan-to-BIM page lists **$0.15–0.35/sq ft (~$1.6–3.8/m²)** — [The Future 3D](https://www.thefuture3d.com/learn/bim-cost-per-square-foot/)
- Project examples for 50,000 sq ft (4,645 m²): **$125,000–250,000** for LOD 300 Arch+Struct+MEP (~$27–54/m²) vs **$12,000–35,000** modeling-only LOD 300 (~$2.6–7.5/m²) vs **$15,000–50,000+** complete scan+BIM (~$3.2–10.8/m²) — publishers contradict each other — [The Future 3D](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/); [Arrival 3D](https://arrival3d.com/scan-to-bim-cost-guide/)
- Generic outsourced LOD 300 benchmark: **$0.15 / $0.30 / $0.45 per sq ft (low/typical/high) ≈ $1.6 / $3.2 / $4.8 per m²** — [Tesla Outsourcing Services, rates by discipline](https://www.teslaoutsourcingservices.com/blog/how-much-does-outsourcing-bim-modeling-cost-rates-by-discipline/)

**Hourly rates & offshore**
- 2026 modeling rates typically **$50–150/hour** (onshore context) — [search summary of 2026 vendor guides (Concrete Bureau / civilmat result set)](https://civilmat.com/bim-services-cost-per-project/)
- Offshore (India, SE Asia, E. Europe, Latin America): **$18–45/hour**; offshore teams charge **~one-third** of comparable US/UK onshore rates — [Tesla Outsourcing Services](https://www.teslaoutsourcingservices.com/blog/how-much-does-outsourcing-bim-modeling-cost-rates-by-discipline/)
- India list prices: Designheed **₹150–400/sq ft ("$0.50–2.00/sq ft") for scan-to-BIM**; MEP BIM **₹50–180/sq ft ("$0.60–1.50")**; IndiaMART seller asks ₹200/sq ft (Ahmedabad) and ₹70/sq ft MEP — [Designheed](https://www.designheed.com/blog/how-much-do-building-information-modelling-services-cost-in-2026/); [IndiaMART listing](https://www.indiamart.com/proddetail/scan-to-bim-services-22108697612.html). **Note: the INR and USD figures are internally inconsistent** (₹150 ≈ $1.7 at ~88 INR/USD), so these numbers are unreliable.
- Mexico: industrial 3D laser scanning with colorized cloud + 360° panoramas **MXN 40–100/m²** (field only, excl. mobilization); an as-built 3D model costs **2–4× the scan** — [Juárez Thompson (MX)](https://www.juarezthompson.mx/post/cuanto-cuesta-escaneo-laser-3d-mexico); another MX firm quotes "from $10/m² built" (currency unstated) — [Digitarq](https://digitarq.mx/escaner-lidar-en-mexico-precision-y-nubes-de-puntos/)
- Colombia: provider found (Arplan) but **no published rates** — [Arplan](https://arplan.com.co/escaner-laser-3d/)

**Market size**
- Scan-to-BIM services: **USD 1.48 B in 2024, CAGR 13.7% (2025–2033) → ~USD 4.29 B in 2033; APAC fastest at 16.2%** — [Growth Market Reports](https://growthmarketreports.com/report/scan-to-bim-service-market) (low-transparency publisher; use cautiously)
- Overall BIM market (context): **USD 9.03 B (2025) → 15.42 B (2030), CAGR 11.3%** — [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/building-information-modeling-market-95037387.html); other publishers 12.9%–13.2% CAGR to 2034 — [IMARC](https://www.imarcgroup.com/building-information-modeling-market); [Fortune Business Insights](https://www.fortunebusinessinsights.com/building-information-modelling-software-market-102986)
- 3D scanning market >$16 B by 2030, CAGR >4.5% (2024–2030), attributed to IndustryARC via secondary sources, not verified — [TitansBIM trends 2025](https://titansbim.com/scan-to-bim-trends-2025/)

### Inferences
- Normalized planning bands (my synthesis): scanning **$1.5–7.5/m²**; LOD 200 Arch modeling **$1.5–3/m²** (offshore-like) to **$5–16/m²** (onshore); LOD 300 Arch+Struct **$2.5–5/m²** (offshore) to **$15–38/m²** (onshore); adding MEP multiplies modeling 1.5–3×. The spread mostly reflects offshore vs onshore labor and whether MEP is in scope.
- Since modeling is ~85–95% of the job value, a pipeline that removes most modeling hours can undercut offshore pricing while keeping gross margin, or match current prices with much higher margin.
- In LatAm (Mexico data) scanning at ~MXN 40–100/m² ≈ USD 2–5.5/m² (assuming ~18–20 MXN/USD — exchange rate not sourced) is comparable to US scanning prices; the model is 2–4× more, i.e. ~USD 4–22/m².

### Gaps
- No Europe-specific (€/m²) published price lists were retrieved beyond Concrete Bureau's hours-based method; no UK £/m² data found.
- No verified Colombia pricing.
- No credible, methodology-transparent market sizing for reality capture services specifically; all market numbers come from paid-report summaries.
- Gross margins of scan-to-BIM service firms: no source found.

## 3. Quality standards (USIBD LOA, BIMForum LOD, GSA, UK/ISO 19650, tolerances) and deviation-analysis QA / acceptance

### Takeaway
Quality is specified on two independent axes: **geometric accuracy** (USIBD LOA bands at 2σ/95% confidence, separating *measured* accuracy of the cloud from *represented* accuracy of the model; GSA Levels 1–4 ±51/±13/(±6)/±3 mm; RICS bands) and **information/detail content** (BIMForum LOD 100–500 incl. LOD 350; ISO 7817-1 Level of Information Need under ISO 19650 EIRs). Verification is done by independent check measurements (USIBD validation level C, GSA discrete comparisons, NIST acceptance sampling) and by model-vs-cloud deviation analysis (heat maps, per-element pass/fail at a stated tolerance, e.g. ±15 mm in Verity).

### Cited Findings
**USIBD Level of Accuracy (LOA) Specification**
- Current version is **v3.x (v3.1)**; USIBD announced v3.1 with a new website and education center; v3.1 adds a dedicated section on **specifying tolerances using standard deviation** — [Geo Week News, USIBD LOA v3.1 release](https://www.geoweeknews.com/articles/usibd-announces-the-release-of-loa-specification-version-3-1-and-launches-new-website-with-education-center/); [USIBD LOA page](https://usibd.org/level-of-accuracy/)
- LOA bands (from a secondary Italian blog; verify against USIBD): **LOA10: 5–15 cm (disputed/possibly corrected for a unit error); LOA20: 15 mm–5 cm; LOA30: 5–15 mm; LOA40: 1–5 mm; LOA50: 0–1 mm**; tolerances hold at **95%**, deviations measured ±; three validation levels: **A (no check), B (comparison of two datasets captured at different times), C (independent measurement system)** — [Shelidon, BIMpill livello di accuratezza](https://www.shelidon.it/bimpill-livello-di-accuratezza-di-un-rilievo/)
- LOA "always uses the **2-sigma range (95% confidence)**"; **represented accuracy** (model/drawing) is independent of the sensor and **can only be equal to or worse than measured accuracy** — [USIBD LOA Guide Document C120 (v2, older)](https://cdn.ymaws.com/www.nysapls.org/resource/resmgr/2019_conference/handouts/hale-g_bim_loa_guide_c120_v2.pdf)
- 2026 commentary stresses that accuracy is a property of the method/validation, not a scanner setting; a result may be close to truth yet fail a required LOA if the method is not reliable — [LIDAR Magazine, "Accuracy Isn't a Setting" (Jun 2026)](https://lidarmag.com/2026/06/09/accuracy-isnt-a-setting/)
- Structural-engineering use of updated LOA spec — [STRUCTURE magazine](https://www.structuremag.org/article/leveraging-the-usibds-updated-loa-specification-to-enhance-structural-engineering-projects/)

**BIMForum LOD Specification**
- Latest is **LOD Spec 2025** (Part I PDF hosted under a Dec-2024 upload path; a search summary stated publication on 31 Dec 2025 — date conflict); updated annually; **Spanish edition Feb 2026** — [BIMForum LOD page](https://bimforum.org/LOD/); [LOD Spec 2025 Part I](https://bimforum.org/wp-content/uploads/2024/12/LOD-Spec-2025-Part-I-Official.pdf)
- LOD 350 (earlier wording): element represented as a specific system/object/assembly in quantity, size, shape, orientation **and interfaces with other building systems**; added between 300 and 400 as a trade-coordination level — [BD+C Network](https://www.bdcnetwork.com/building-team/architects/article/55144799/level-of-development-will-a-new-standard-bring-clarity-to-bim-model-detail)

**GSA BIM Guide Series 03 – 3D Imaging (US federal; 2009-era, older)**
- Data tolerance by level: **Level 1 ±51 mm; Level 2 ±13 mm; Level 4 ±3 mm** (most detailed) — [NIST, Evaluation of an Acceptance Sampling Method for 2D/3D Building Plans](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=907878); [Sensors 2019 MMS paper citing Level 1/2](https://www.mdpi.com/1424-8220/19/18/3952)
- The spec cannot theoretically quantify per-point uncertainty, so it relies on **discrete comparisons between the point cloud and physical measurements**; GSA also has a 3D Laser Scanning Quality Management Program guide — [GSA BIM Technical Standards: 3D Imaging](https://www.gsa.gov/real-estate/design-construction/3d4d-building-information-modeling/guidelines-for-bim-software/guidelines/technical-standards/bim-technical-standards-3d-imaging)
- NIST evaluated tolerance/sample-size acceptance limits for 2D plans derived from 3D imaging using **285 measurements** from a GSA project — [NIST IR 7638](https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7638.pdf)

**UK / ISO**
- RICS *Measured surveys of land, buildings and utilities* grades surveys by positional accuracy **Band A–J**; e.g. **Band D ±10 mm plan / ±25 mm height (1:50 building surveys); Band E ±25 mm / ±50 mm (1:100)** (RICS-derived table, verify against official); 3rd edition introduced **BIM as an output linked to EIR**, and utilities link to **PAS 128** — [Angell Surveys, RICS specifications](https://angellsurveys.com/insights/specifications-for-land-buildings-and-utilities/); [FIG 2016 presentation](https://www.fig.net/resources/proceedings/fig_proceedings/fig2016/ppt/ts03d/TS03D_kavanagh_8064_ppt.pdf); [isurv RICS downloads](https://www.isurv.com/downloads/176/rics_standards) (edition dating unclear: a listing shows a 3rd-edition professional standard dated Apr 2024 with the 2014 note archived)
- **ISO 7817-1:2024** – concepts/principles for specifying **Level of Information Need** (geometry: detail, dimensionality, location, appearance, parametric behaviour); **ISO/DTS 7817-2** (draft) relates LOIN to **EIR and BEP per ISO 19650** and to **verification/validation of deliverables** against requirements — [ISO 89075 (ISO/DTS 7817-2)](https://www.iso.org/standard/89075.html); [AS ISO 7817.1:2024](https://store.standards.org.au/product/as-iso-7817-1-2024)

**Deviation analysis & QA practice**
- **ClearEdge3D (Topcon) Verity**: compares as-built point clouds to design/fabrication models in **Navisworks/Revit**, flags elements outside specified tolerance, produces deviation reports and heat maps (vs design or vs cloud); it **fits design geometry to the cloud** (EdgeWise-like algorithms) rather than raw point-to-surface distances to avoid false passes; paid Navisworks add-on — [Topcon Verity](https://www.topconpositioning.com/us/en/solutions/technology/infrastructure-software-and-services/clearedge3d-verity); [AEC Magazine](https://aecmag.com/technology/laser-scanning-for-verification/) (≈5 years old); [Geo Week News](https://www.geoweeknews.com/articles/verity-automatic-point-cloud-analysis-construction-qc/)
- Example per-element tolerance **±15 mm** used for scan-to-BIM QA ("analyzes every modeled element… heatmaps and variance reports"); a case showed missing elements in the reference model cause misclassification — [ViBIM best scan-to-BIM software](https://vibimglobal.com/blog/best-scan-to-bim-software/); [AEC Magazine](https://aecmag.com/technology/laser-scanning-for-verification/)
- Point-cloud QA framed as a measurable acceptance test against a stated tolerance at **four gates: field, registration, deliverable, model**; registration treated as a gate before modeling — [Zealot Recap, Point Cloud QA for Scan to BIM 2026](https://zealotrecap.com/blog/point-cloud-qa-scan-to-bim/)
- Other QA/QC technique overviews — [HitechDigital QC & validation](https://www.hitechdigital.com/blog/3d-scan-to-bim-conversion-qc-validation-techniques); [ViBIM QC guide](https://vibimglobal.com/blog/scan-to-bim-quality-control/)

### Inferences
- A machine-checkable acceptance spec for an automated pipeline can combine: (a) LOA band per element category for **represented** accuracy (e.g. LOA20 for walls/slabs ≈ 15–50 mm, LOA30 for structure ≈ 5–15 mm), verified at 2σ by automated model-vs-cloud deviation on 100% of elements; (b) **measured** accuracy of the registered cloud validated against independent control (USIBD level C / total station checkpoints); (c) LOD/LOIN checklist per element type (geometry + required parameters). This turns QA from visual review into a computed report — key for "hours" delivery.
- Deviation analysis cannot detect *omitted* elements or wrong typing by itself (Verity case), so completeness/classification QA still needs a separate check (rules or human).
- Older US federal guidance (GSA 2009, NIST) is still the most explicit about statistical acceptance sampling; newer documents (USIBD v3.1, ISO 7817) are the current references to cite in contracts.

### Gaps
- Official USIBD v3.1 LOA table and publication date not retrieved (commonly cited official LOA10 upper bound "user-defined, lower 50 mm" could not be confirmed from sources).
- GSA Level 3 (±6 mm) and artifact sizes not confirmed.
- No retrieval on **Leica Cyclone 3DR** inspection workflow specifics or default acceptance thresholds.
- BIMForum LOD 2025 text on existing-conditions elements not retrieved.
- No source on typical contractual pass rates (e.g. "≥95% of elements within tolerance").

## 4. What is automatable today vs. what still needs humans; hybrid "AI + human-in-the-loop" evidence and throughput

### Takeaway
Registration, classification/segmentation, and extraction of regular geometry (walls, slabs, planes, pipe runs) are partially automated in commercial tools (EdgeWise, Aurivus, Pointfuse, BricsCAD), and several services now advertise 48-hour or "hours" delivery; but no independent, end-to-end throughput study including human QA was found. Vendors claim 30–70% modeling-time reduction; literature (2021 survey; 2026 Springer chapter; 2026 bridge HITL paper) consistently concludes a hybrid workflow beats full automation, with humans needed for interpretation, typing/families, occluded/hidden elements and system logic.

### Cited Findings
- Survey of **208 professionals in 78 countries**: most scan-to-BIM modeling still manual and excessively time-consuming — [Rocha & Mateus 2021, ISPRS IJGI](https://doi.org/10.3390/ijgi10080564) (2021)
- A vendor cites an international survey where **80.1%** considered manual geometry modeling from point clouds time-consuming (the figure could not be located in the Rocha & Mateus abstract; unverified) — [Timspark, Scan-to-BIM automation with ML (Jul 2026)](https://timspark.com/blog/scan-to-bim-automation-machine-learning/)
- Timspark "from five days of modeling to five minutes" — but by its own caveat the 5 minutes covers **only GPU inference/conversion**, not a complete approved BIM deliverable — [Timspark](https://timspark.com/blog/scan-to-bim-automation-machine-learning/)
- 2026 Springer chapter (literature review + factory-facade case): AI accelerates segmentation/classification; recommends **hybrid human-in-the-loop** with AI as assistant for repetitive tasks and humans for interpretation and domain expertise — [Springer 2026, "Advancing Scan-to-BIM with AI: Emphasizing the Role of a Hybrid Approach"](https://link.springer.com/chapter/10.1007/978-3-032-19495-4_12)
- 2026 bridge study (Sakr & Sadhu, J. Infrastructure Intelligence and Resilience): **strategically placed human intervention with a repeatable protocol optimizes accuracy and time better than fully automated semantic pipelines or deterministic parametric modeling alone** (exact time figures not retrieved) — [ScienceDirect S2772991526000149](https://www.sciencedirect.com/science/article/pii/S2772991526000149)
- Vendor claims of speedups: automated extraction tools reduce modeling time **50–70%** (manual refinement still required); a provider claims its automation cuts modeling cost **30%** — [search summary of 2026 vendor guides, e.g. nCircle Tech](https://ncircletech.com/EN/blogs/unleashing-speed-in-scan-to-bim-how-ai-ml-are-transforming-point-cloud-to-bim-workflows-in-2026); Points2BIM claims a 4–5 day process reduced to **3 hours** — [Points2BIM](https://www.points2bim.de/en/blog/scan-to-bim-neu-gedacht-punktwolken-in-rekordzeit-in-verl%C3%A4ssliche-bim-modelle-verwandelt)
- **Moving Atoms** advertises upload-a-point-cloud → separated, editable **Revit + IFC in 48 hours**, LOD 200–500, contrasting with manual tracing "quoted in weeks, priced per sq ft" — [Moving Atoms Scan to BIM](https://movingatoms.ai/scan-to-bim/)
- Tool coverage: **EdgeWise** automates wall and pipe-run extraction (Lite $1,995/yr; full edition quote-based); **Aurivus** AI object detection in point clouds, aimed at pipes inside Revit; **Pointfuse** detects walls, ceilings, pipes, conduit; **BricsCAD BIM** semi-automatic — [ClearEdge3D EdgeWise](https://www.clearedge3d.com/products/edgewise/); [Aurivus](https://aurivus.com/scan-to-bim-time-saver-ai/); [Matterport, best scan-to-BIM software 2026](https://matterport.com/blog/best-scan-to-bim-software)
- AI-assisted tools detect planes and basic geometry, but converting a cloud into a fully "intelligent" BIM model still **requires skilled human modeling** — [The Future 3D workflow guide](https://www.thefuture3d.com/blog/scan-to-bim-workflow/); see also [Informed Infrastructure, "Scan to BIM Still Requires Expert Modelers"](https://informedinfrastructure.com/post/scan-to-bim-still-requires-expert-modelers)
- Academic assistive modeling direction: A-Scan2BIM (BMVC 2023) predicts next modeling operations to assist modelers — [A-Scan2BIM](https://bmvc2022.mpi-inf.mpg.de/BMVC2023/14)
- Heritage (H-BIM) classification with AI for semi-automatic reconstruction — [Heritage AI classification (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10007271/); a semi-automatic heritage workflow "reduced modelling time significantly" (no figures) — [ISPRS Archives 2023](https://isprs-archives.copernicus.org/articles/XLVIII-M-2-2023/1345/2023/)

### Inferences
- **Most automatable now:** registration (already semi-automatic in field/office software), segmentation/classification of the cloud, extraction of planar elements (walls, floors, ceilings, slabs), straight pipe/duct runs, columns/beams of standard section; automated deviation QA (Verity-style) and report generation.
- **Still human (or HITL-review):** element typing and family/type selection (wall assemblies, door/window types), inference of hidden/occluded elements (inside walls, above ceilings), MEP system logic (connectivity, flow direction, system assignment), interpretation of ambiguous geometry, LOD 350+/400 detailing, and client-specific standards. These map to the "interpretive reasoning" the 2026 literature reserves for humans.
- **Realistic automated target (inference):** if 50–70% of modeling hours are removed (vendor claims) the Concrete Bureau LOD 300 ~15,000 m² job (~1,000–2,400 h) drops to ~300–1,200 h — still weeks, not hours. Getting to "hours" requires (i) near-full automation of Arch+Struct at LOD 200–300 with automated deviation QA, (ii) human review measured in minutes per room rather than hours per element, and (iii) leaving MEP LOD 350+ as a slower tier. Moving Atoms' 48-h promise is the best public proxy for what is commercially claimed today.

### Gaps
- No independent, peer-reviewed measurement of **end-to-end** throughput (m²/hour or hours per 1,000 m²) for an AI+HITL pipeline on buildings, including human QA and revisions.
- No public accuracy statistics (per-class precision/recall, % elements within LOA) for commercial automatic tools at building scale.
- Sakr & Sadhu time figures not retrieved.

## 5. Business models (pay-per-m², subscription platforms, scanning-as-a-service, equipment rental vs buy, robot-as-a-service) and unit economics

### Takeaway
Service firms predominantly price per sq ft/m² (or hours × rate); software vendors use annual seats (EdgeWise Lite $1,995/yr) or pay-per-m² credits (Aurivus ~€0.25/m² starter pack); hardware is bought (~$85–90k for an RTC360, €30–100k for mobile SLAM) or rented (~$750–1,900/day, ~$3.3–4k/week, ~$9–12k/month for an RTC360); robotics (Spot) costs $75k base to $150–375k configured; progress-monitoring SaaS is quote-based at reportedly ~$5–20k/month/site. No reliable margin data was found.

### Cited Findings
**Per-area / hourly service pricing** — see Section 2 (per sq ft dominant; Concrete Bureau = hours × rate) — [Concrete Bureau](https://concrete-bureau.com/blog/how-much-does-scan-to-bim-cost); [Arrival 3D](https://arrival3d.com/scan-to-bim-cost-guide/)

**Software / platform models**
- **Aurivus**: pay-per-use, no subscription; starter pack **100 m² for €25** (≈ €0.25/m², promotional) — [aec+tech Aurivus listing](https://www.aecplustech.com/tools/aurivus)
- **EdgeWise Lite $1,995/year**; full edition quote-based — [ClearEdge3D EdgeWise](https://www.clearedge3d.com/products/edgewise/)
- **Matterport BIM File**: quoted per order after login (scope "up to 50,000+ sq ft / 4,645 m²"); final price may differ; unenclosed areas charged extra; LOD 200 RVT/DWG via resellers; E57 point cloud ~$250/property within ~48 h (reseller) — [Matterport price list](https://support.matterport.com/s/article/Matterport-Price-List-Add-Ons-and-Services?language=en_US); [Matterport BIM file](https://support.matterport.com/s/article/Scan-to-BIM?language=en_US); [Southeast 3D Tours](https://southeast3dtours.com/blog/matterport-point-cloud-e57-as-built-exports.html); [iTourVista](https://itourvista3d.com/3d-virtual-tours-matterport-prices/)
- Progress monitoring SaaS (Buildots, Doxel, OpenSpace): quote-based; enterprise contracts sized by project scale, scan frequency and duration; hardware extra; Doxel FAQ says it generally **charges by the square foot**; third-party estimates **Buildots $5–15k/month/site; Doxel $8–20k/month/site** (unverified) — [Doxel review (bestcre)](https://bestcre.com/doxel-review-cre-ai/); [Construction AI Tools – Buildots](https://constructionaitools.com/tools/buildots/); [Capterra Doxel](https://www.capterra.com/p/227688/Doxel/)

**Equipment purchase vs rental (2025–2026 listings)**
- Purchase: **Leica RTC360 ≈ $85,000** (GPRS via Framesixty), reseller from **$87,290**; **BLK360 ≈ $18,000–26,500** (from $19,077 at Datum); **FARO Focus kits $58,314–84,429** — [Framesixty](https://framesixty.com/how-much-does-3d-scanning-cost/); [Datum Tech Solutions](https://datumtechsolutions.com/collections/laser-scanners); [3D Mag 2026 price roundup](https://www.3dmag.com/3d-scanners/3d-laser-scanner-for-buildings-price-2026/)
- European reseller ranges (ex-VAT): **pro TLS (FARO Focus Premium, RTC360, Trimble X12) €40,000–130,000; mobile SLAM (NavVis VLX, FARO Orbis, Viametris) €30,000–100,000**; mobile SLAM rental **€800–2,500/week** — [ATIS.cloud scanner buyer's guide 2026](https://www.atis.cloud/articles/best-3d-scanners-for-point-clouds)
- NavVis VLX: **no reliable official public price**; quote-driven — [3D Mag 2026](https://www.3dmag.com/3d-scanners/3d-laser-scanner-for-buildings-price-2026/); VLX rental via HTS (daily/weekly/monthly tiers) **requires a trained HTS operator** unless you own a VLX — [HTS NavVis VLX rental](https://hts-3d.com/navvis-vlx-rental/); 2021 forum: NavVis itself did not rent VLX (dated) — [Laser Scanning Forum](https://www.laserscanningforum.com/forum/viewtopic.php?p=107177)
- Rental: **RTC360 $975/day, $3,900/week, $11,700/month (replacement value $88,000)**; another listing $3,265/wk, $9,320/mo — [KWIPPED RTC360](https://www.kwipped.com/rentals/product/leica-geosystems-rtc360-laser-scanner/28323); RTC360 LT **$1,910/day, $4,040/week, $8,485/month** — [CNT Automation](https://cntautomation.com/products/leica-rtc360-lt-3d-laser-scanner-for-rent); RTC360 kit from **$2,500** (2-day minimum), BLK360 G2/G1 from $850/$700 — [Datum rentals](https://datumtechsolutions.com/collections/rentals); average daily scanner rental **$743** (GPRS) — [Framesixty](https://framesixty.com/how-much-does-3d-scanning-cost/)

**Robot-as-a-service / robotics**
- Boston Dynamics Spot: **$74,500 base at 2020 launch**; no current public list price; configured units **~$150,000–375,000** per public procurement records; **Spot Arm ≈ +$65,000**; jobsite capture configuration **>$100,000 all-in + software subscriptions**; one guide reports ~**20 h/week** of manual capture saved on a large project — [IEEE Spectrum (2020)](https://spectrum.ieee.org/boston-dynamics-spot-robot-dog-now-available); [RobotSourced 2026](https://robotsourced.com/guides/boston-dynamics-spot-price/); [BuilderMuse 2026](https://buildermuse.com/commercial/construction-robots-that-actually-earn-their-keep/)
- No published robot-as-a-service price for Spot-based reality capture found — [RobotSourced](https://robotsourced.com/guides/boston-dynamics-spot-price/)

### Inferences
- **Rent vs buy (RTC360):** at $975/day, purchase (~$87k) breaks even after ~90 rental days; at ~$11,700/month, after ~7.5 months of continuous rental — buying makes sense only above ~4–6 scan days/month sustained (excl. maintenance, calibration, insurance, software). For a startup pipeline, renting or partnering with local scanning providers keeps capex off the books.
- **Unit economics sketch (inference):** if a provider charges ~$3–5/m² for LOD 300 Arch+Struct (offshore-competitive) and an automated pipeline needs, say, 10–20 h of human review per 15,000 m² at $25–50/h, labor cost falls to ~$0.02–0.07/m² vs ~$2.5–5/m² in the manual offshore model — leaving room for compute and GPU costs. Validation of the review-hours assumption is required.
- Pay-per-m² credit models (Aurivus €0.25/m²) and subscription per site (progress monitoring, $5–20k/month) are the two SaaS archetypes; scan-to-BIM as a high-frequency service fits the latter better (recurring captures per active project).

### Gaps
- No reported gross/net margins for scan-to-BIM service firms or platforms.
- No NavVis VLX official price or day rate; no NavVis IVION subscription pricing retrieved.
- No robot-as-a-service pricing.
- No Doxel/Buildots price confirmation from the vendors.

## 6. Recurring / high-frequency use cases that benefit from fast turnaround

### Takeaway
The use cases where hours-level turnaround creates value are recurring: progress monitoring (scan vs BIM, weekly/bi-weekly), QA/QC of installed work against tolerance (Verity-style), slab flatness/levelness (ASTM E1155 F-numbers from scans in minutes vs days), quantity/payment verification, and as-builts for renovation/FM. Evidence of value is mostly vendor-claimed (e.g., Doxel: 11% faster delivery, 16% lower monthly cost, 95% less time tracking progress).

### Cited Findings
- **Progress monitoring (scan vs BIM):** Doxel compares 3D site scans with BIM to surface schedule variances; vendor-claimed **11% faster delivery, 16% reduction in monthly costs, 95% less time tracking progress** (unverified) — [bestcre Doxel review](https://bestcre.com/doxel-review-cre-ai/); [Means & Methods Lab – Doxel](https://meansandmethodslab.com/tools/doxel); reality-capture progress reporting time reportedly down **70–90%** (drone monitoring broadly) — [AI in construction 2026 (Ricci blog)](https://www.tommasomariaricci.com/blog/ai-for-construction-guide-2026)
- **Robotic recurring capture:** robot walks a pre-programmed route on schedule capturing 360° imagery at hundreds of waypoints (HoloBuilder/OpenSpace) — [BuilderMuse 2026](https://buildermuse.com/commercial/construction-robots-that-actually-earn-their-keep/)
- **QA/QC of installed work:** Verity provides a complete record of work installed with deviations from specified tolerances, automated from Navisworks — [Topcon Verity](https://www.topconpositioning.com/us/en/solutions/technology/infrastructure-software-and-services/clearedge3d-verity); [AEC Magazine](https://aecmag.com/technology/laser-scanning-for-verification/)
- **Slab flatness/levelness:** scanning software produces **ASTM E1155 FF/FL** reports; ClearEdge3D Rithm claims E1155 numbers in **<15 minutes vs the multiple-day** conventional process (2019 article, older) — [Concrete Products 2019](https://concreteproducts.com/index.php/2019/01/28/laser-scan-data-crunching-speeds-slab-flatness-levelness-measurements/); commercial TLS accuracy ≈ **±3 mm within 20 m** — [Remote Sensing 13(4):714](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-13-00714/article_deploy/remotesensing-13-00714.pdf); ASCC study: E1155 permits laser imaging devices but its precision/bias statement is limited for scanning; consultant critique that heat maps alone are qualitative and that taking minimum F-numbers from a single line violates E1155 — [ASCC 3-D Laser Scanning Study Part 2 (2020)](https://www.ascconline.org/Portals/ASCC/ASCC-3-D-Laser-Scanning-Study-Part2-02-2020.pdf); [ASCC Laser Scan Results (Sept 2022)](https://ascconline.org/Portals/ASCC/Laser_Scan_Results_Sept22.pdf)
- **Quantity take-off in maintenance projects:** scan-to-BIM used for QTO in building maintenance; initial cost high due to equipment, software and skilled operators — [Emerald IJBPA (2022–23)](https://emerald.com/insight/content/doi/10.1108/IJBPA-06-2022-0097/full/html)
- **As-built for renovation:** example 10,000 sq ft renovation — scanning $3–6k, modeling $15–35k — [The Future 3D](https://www.thefuture3d.com/blog/scan-to-bim-cost-guide/)

### Inferences
- For a construction-platform company, the highest-frequency, lowest-LOD needs (progress %, installed vs designed, slab FF/FL, quantities for payment certificates) require mostly **scan-vs-model comparison and simple element extraction**, which are the most automatable steps — a natural first market for an "hours" pipeline, before full LOD 300+ as-built authoring.
- Weekly progress capture on an active site multiplies volume: a single 15,000 m² project scanned bi-weekly over 12 months = ~26 captures ≈ 390,000 m² processed/year — economics only work with near-zero marginal human time per capture.
- Flatness/tolerance reporting must output standard metrics (ASTM E1155 F-numbers using all measurement lines; ACI 117 tolerance classes) rather than only heat maps to be contractually usable.

### Gaps
- ACI 117 tolerance table and FF/FL specified values not retrieved.
- No independent ROI study for progress monitoring (Buildots/Doxel/OpenSpace) in 2025–2026.
- No data on frequency/volume of as-built requests from facility managers or on payment-verification use in LatAm.
