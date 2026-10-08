# Shade Correction at Batch Change: Case Study for Client A (Ceramic Tiles)

*Forward Deployed Engineer: Harsh Upadhyay. Status: proposal draft after the first discovery call. Confidential. Nothing here has been proposed to the client yet.*

## 0. The short version

The client does not have a vision problem. They have a **control problem**. They can already *measure* the shade gap (their spectrophotometer gives ΔL, Δa, Δb against the master tile). What nobody can do is turn that gap into "brown +3.1%, yellow −0.8%". So QC guesses in Photoshop, prints 6-7 variants, fires them, measures, and repeats. Each round takes 6-7 hours, and the line keeps running meanwhile.

I recommend a **Shade Correction Advisor**, used in the QC lab at batch change. QC measures the master and the first production tile. The tool returns the per-colour edit to the print file, with a predicted result. A QC engineer approves it, and one confirmation tile is printed, fired and measured. No new line hardware, no cameras, no root-cause engine. The decision step takes about 5 minutes. The target is one round (about 2 hours to an approved file) instead of several 6-7 hour rounds. Proposed: a 16-week fixed-fee pilot on one line at the India plant, USD 85,000, with 40% payable only if agreed thresholds are met.

---

## 1. Problem understanding

### 1.1 What they asked for vs what they need

| They said | What is actually needed | Why it differs |
|---|---|---|
| "Video / vision analytics, compare master and production tile" | A **recommendation**: how much to change each ink channel in the print file | The comparison is mostly solved (spectro → ΔL/a/b). The missing piece is the *inverse*: gap → edit. |
| "Takes minutes, not hours" | Minutes for the **decision**; one kiln pass for the **proof** | Firing is physically in the loop. Compute can be 5 min; "5-6 min end to end" is not achievable. I will say so on the next call. Honest target: about 2 h to an approved file. |
| Sounds like an always-on line system | A check **at batch change only** | They told us: once the first sample of a batch is right, the batch runs fine. The pain is at changeover. |
| "Delta gloss too" | Gloss is **reported and flagged**, not corrected | Gloss is driven mostly by glaze and kiln, not by the colour print file. Unless there is a digital glaze or effect channel, we cannot fix it via the file. |
| "Ideally find the root cause" (they then say it is not realistic) | **Not now.** Log context so it becomes possible later | Raw material and 30 s of kiln time can shift shade. Agreed with the client's own view. |
| "Compare with the reference image" | The **physical master tile (as measured values)** is the truth. The old print file is not | A 2021 reference file edited many times has drifted. We need a stable target and version control. |

### 1.2 Stakeholders

| Who | What they want | What I need to tell them |
|---|---|---|
| **Special Projects Lead** (champion, did the talking) | A proof that it can be done, case studies, extra value. Wants the lab loop gone. | "You will see it work on your own sample tiles in week 4. The 5-minute number is the decision step, not the kiln." |
| **Head of IT & OT Procurement** (asked about OEMs and hardware deployments) | Low vendor and security risk, no surprise hardware, clear price | Software on instruments you already own. No line connection in the pilot. Data can stay in the plant. Fixed price, milestone payments. We do not resell hardware. |
| **Plant QC & design team** (the real users, not on the call) | Less rework, no blame, keep their judgement | The tool suggests, you approve. It learns from your edits. It removes the 6-variant guessing, not your role. I want them on the next call. |
| **Plant / production head** | Fewer m² in the wrong shade, no line downtime | Zero new downtime. Savings measured in m² and hours against a baseline we capture first. |
| **Printer OEM / ink supplier** (not in the deal yet) | Not being blamed, protecting their software | May control file access and RIP settings. Could block or enable us. Ask early whether they already sell closed-loop colour tools. |
| **Finance / business sponsor** (unknown) | Payback in their money | Value arithmetic in §7, using their numbers once measured. |

### 1.3 As-is process (as I understand it)

1. SKU is scheduled. The digital printer loads a reference image (previous run's file). A master tile exists for the version.
2. One sample is printed and fired in the kiln (assumed about 1 h).
3. Lab measures it with a spectrophotometer (small area, point reading) against the master → ΔL, Δa, Δb. If "OK", run the batch.
4. If not, QC edits the file **by eye** in Photoshop across 6 primary colours ("brown +5%") and makes 6-7 variants.
5. Variants are printed, fired, sampled and compared. **One round = 6-7 h.** Repeat until matched.
6. The line keeps producing. 5,000-10,000 m² (recording unclear) end up in the wrong shade before the corrected file arrives.
7. The winning file becomes the new reference. Over years the reference drifts, and sometimes "99% matching" is let go.

**Pain:** no mapping from colour gap to edit; the choice of edit is subjective; there is no explicit tolerance; reference files rot; production is lost while waiting.

---

## 2. What we don't know yet

Ranked by *how badly the answer could kill or reshape the plan*, not by curiosity.

| # | Question | Why it matters | Assumption until answered |
|---|---|---|---|
| 1 | If you print and fire the **same file** repeatedly in one shift, how much does the shade move? Does it also move between days, ink lots, kiln lanes? | If process noise is larger than our tolerance, editing the file cannot converge. This is the kill-risk. | Same-file repeatability σ ΔE00 ≤ 0.4. Drift is slow (days). Tested in week 2. |
| 2 | What exactly is the "input" we change? File format, channels, RIP/ICC, per-channel curves or pixel edits, can software write it? Which printer and ink set? | Decides what the output of the tool looks like and whether anything can be automated. | Multi-channel image files with 6 editable ink channels. QC loads files by hand. We output a ready-to-load file plus a table of % changes. |
| 3 | What is "matching"? ΔE formula, tolerance per customer or market, gloss tolerance, who decides? | We cannot define success or stop criteria without it. | ΔE00 mean ≤ 1.0 and max ≤ 1.5 over 6-8 points. Gloss reported only. Confirmed with QC lead in week 1. |
| 4 | What history exists? Old Photoshop edits with before/after files, readings, how many SKU re-runs per line per month? | Decides whether we can pre-train from history or must collect prospectively. | History is patchy. About 30 corrections per month per plant. We rely on the calibration chart plus their sample tiles. |
| 5 | Which spectrophotometer, geometry, aperture, how many points per tile? Is the tile patterned, and how are comparable regions found on master vs production? | The whole input depends on repeatable point readings of *matching* regions. | Benchtop or handheld d/8, about 8 mm aperture. 6-8 fixed points per SKU, located with a simple acrylic mask. Instrument repeatability ≤ 0.15 ΔE00. |
| 6 | What happens on the line during the 6-7 h? Does it stop, or print on with the old file? What is the output per hour? | Waste per event drives the value case. The 5-10k m² figure is unclear. | Line keeps running. Waste 5,000 m² per event (low end). Implied rate about 800-1,500 m²/h. |
| 7 | Is there a glaze or effect channel that can change gloss? | Decides if gloss is fixable at all. | No. Gloss is flagged only. |
| 8 | Can data leave the plant? On-prem vs cloud, network rules (UAE, India, Bangladesh), IT/OT segregation? | Decides hosting and who sees data. | On-prem web app on plant LAN. Remote support by VPN only. |
| 9 | Does the printer OEM already sell closed-loop colour correction? | If yes, buy it, don't build it. | Not for this printer. Asked early, answer changes the plan. |
| 10 | Who funds this, how is it approved, what is the PO cycle? | Timeline risk before we start. | Procurement signs a PO before week 0. |

---

## 3. Solution

### 3.1 Options considered

| Option | What it is | Verdict |
|---|---|---|
| A. Tighten the SOP only | Write a ΔE tolerance, version-control files, log edits | **Do it anyway** (it is part of the pilot), but it does not remove the loop. |
| B. OEM or RIP vendor closed-loop colour tools | Printer maker's own colour management | **Check first** (Q9). If it exists and works, recommend buying it. |
| C. **Measurement + correction advisor, human approves** | Use existing spectro readings and a calibrated printer-kiln model to compute the edit | **Recommended.** |
| D. Inline vision or hyperspectral cameras on the line | Continuous shade monitoring | **Rejected for now.** The problem is at changeover, not along the line. Camera colour is not colorimetric without heavy calibration. Needs capex, lighting control, and OT integration. |
| E. End-to-end deep learning (image → corrected file) | Black box trained on history | **Rejected for now.** Needs thousands of paired examples, is unexplainable to QC, and is unsafe when it is wrong. Revisit after a year of logged events. |
| F. Root-cause engine (kiln SPC, raw material) | Find why shade drifts | **Not now.** Client agrees it is hard. We log context so it can be built later. |

### 3.2 Why C fits this client

- It sits **where the pain is** (batch change in the lab) and uses **instruments they already own**.
- It needs little data. We never predict absolute colour. We predict the *change* caused by a small edit, anchored to a tile we just measured. A local sensitivity model plus one confirmation tile closes the rest.
- It is explainable. QC sees "brown +3.1% lowers ΔE00 at points 2, 5, 6" and keeps the final say.
- It proves value in 16 weeks without any hardware purchase, and it extends to inline sensing or root cause later because every event is logged.

### 3.3 What I would deliberately not build

Inline cameras or any line integration; auto-pushing files to the printer without sign-off; a root-cause engine; a deep model; gloss correction; a multi-plant rollout before one plant works; dashboards beyond one page; replacing Photoshop for design work; any hardware purchase by the client in the pilot.

---

## 4. Solution engineering

### 4.1 End to end, in the lab at batch change

1. QC picks the SKU. The tool shows the measurement map (6-8 points) and the master target values.
2. QC prints one sample with the current file, fires it, and measures the 6-8 points. CSV export (spectral if available, otherwise Lab) goes to the tool. About 5 min.
3. The tool reads the print file, finds the ink amounts at each measured point, and computes ΔE00 and ΔL/Δa/Δb per point.
4. The solver proposes per-channel changes plus a corrected file, a predicted ΔE00 per point with uncertainty, and flags (low confidence, out of range, gloss out of spec).
5. **QC engineer reviews, accepts or edits the proposal.** The approved file is loaded to the printer.
6. One confirmation tile is printed, fired and measured. If it passes the agreed tolerance, the batch is released. If not, the new reading feeds a second iteration.
7. Every event is logged: files, readings, edits, outcome, and context (ink lot, kiln speed and temperature, body lot, line, operator).

Time after: print 5 min + fire about 60 min + cool and measure about 15 min + advisor 5 min + QC review 10 min ≈ 1.6 h, versus 6-7 h *per round* today.

### 4.2 Inputs and how data is collected

- **Master target:** the master tile measured once at 6-8 fixed points per SKU, stored as spectral or Lab values. A simple acrylic mask with holes, made per SKU, makes the points repeatable.
- **Production reading:** the same points on the fired sample.
- **Print file:** read by the tool to get ink amounts at each point.
- **Calibration chart (once per printer, kiln and ink set; refreshed monthly or at ink-lot change):** about 250 patches covering single-ink ramps, 2-3 ink mixes and colours near the client's SKUs, printed on 2 tiles, fired, and measured (about 1 h of lab time).
- **Client sample set** (offered on the call): master tile, variation tiles, their files, and readings. These are natural experiments for validation.
- **History** if it exists (old edits with before/after readings).

### 4.3 Logic

For measurement regions *r* (6-8): `m_r` is the master Lab, `p_r` the measured production Lab, and `e_r` the 6-vector of ink amounts at that region. A device model gives the local sensitivity `J(e_r)` = ∂Lab/∂ink (3×6). We choose per-channel relative changes `δ` (bounded to ±15%) to minimise

`Σ_r w_r · ΔE00( p_r + J(e_r)·(e_r ⊙ δ), m_r )²  +  λ‖δ‖²`

- **Start with a local linear model** built on per-channel tone curves and a Yule-Nielsen / Neugebauer baseline. Add a Gaussian-process residual only if the offline backtest says linear is not enough. The GP gives uncertainty.
- The solver is a 6-variable bounded least-squares problem, so it runs in under a second.
- Because the tool is anchored to a measured tile, a small bias in the model is corrected by the confirmation tile, not carried forward.
- **Gloss:** Δgloss is displayed and flagged against tolerance, not optimised.
- **Metamerism guard:** if spectral data is available, we also check spectral difference so a "match" under one light is not a mismatch in another. Final visual check in a standard light booth stays with QC.

### 4.4 Where a person signs off

- QC engineer approves each correction, and may override any channel value (overrides are logged and learned from).
- QC lead approves any change to a master target or tolerance.
- Release of a batch is by lab measurement (ΔE00 tolerance) plus visual check. The tool never releases a batch and never writes to the printer in the pilot.

### 4.5 Fit with existing tools, people, routine

- **Tools:** the spectrophotometer stays. Photoshop stays as fallback. The tool outputs a file in the same format and folder QC uses today. It is a web app on the plant LAN. No connection to the line or PLCs, so no OT risk.
- **People:** one half-day training and a one-page SOP. A named QC owner per shift. QC engineers are involved from week 1 so they shape the screens.
- **Routine:** it replaces steps 4-5 of the as-is process. Everything before and after is unchanged.

---

## 5. Evaluation

### 5.1 Baseline (weeks 0-2, before we change anything)

Capture the last ≥ 20 shade corrections from records plus 5 live events: rounds to approval, hours from the first failed sample to an approved file, first-sample ΔE00, m² produced out of tolerance, and QC hours. Assumed until measured: **2.5 rounds × 6.5 h ≈ 16 h** to an approved file.

### 5.2 Metrics and thresholds

| Metric | Baseline (assumed) | Pass threshold |
|---|---|---|
| **Primary: time to approved file** (first failed sample → file released) | about 16 h | **median ≤ 3 h** |
| **Co-primary: first-confirmation pass rate** (the corrected file's first tile is within tolerance) | unknown, measured in week 2 | **≥ 75% (≥ 9 of 12 events)** |
| Quality guardrail: final tile vs master | n/a | ΔE00 mean ≤ 1.0, max ≤ 1.5 (to confirm), and no visual fail by QC lead |
| Secondary: m² out of tolerance per event | 5,000 m² (assumed) | ≥ 50% lower |
| Secondary: QC hours per correction | about 4 h × 2.5 | ≥ 50% lower |

### 5.3 Test protocol

1. **Instrument check first:** gauge repeatability of the spectro (same tile, 10 readings, 2 operators). The tolerance must be at least 3× the measurement σ, or the metric is meaningless.
2. **Offline backtest (week 4):** on the client's sample tiles and any history, compare the predicted shade change from known edits to the measured change. Compare against a naive baseline (a fixed "% per ΔL" rule of thumb). We must beat the naive rule. (A synthetic prototype in `prototype/` shows the mechanism and the repeatability stop line on an assumed device. It is a plausibility check, not evidence about real tiles.)
3. **Shadow mode (weeks 6-10):** QC works as usual, the tool recommends silently, and we compare its advice to what QC finally chose and what worked. About 8-10 events.
4. **Live pilot (weeks 10-16):** on one line, tool-assisted corrections, **at least 12 events** (about 10 per month per line, so 6 weeks gives about 15). Where possible, 4 or more concurrent manual-control events. The plant's QC measures everything with the same instrument, and the QC lead's visual check is recorded for each. We do not measure our own results.
5. **Read-out:** we show raw tables to the client, not only summaries.

A note on statistics: with 12 events and a 9/12 bar, a process that truly passes only 50% of the time would pass by luck 7% of the time. A process that truly passes 80% of the time would reach the bar 79% of the time. That is good enough for a go/no-go on a pilot, not a precise rate.

### 5.4 What makes us stop

- **Same-file repeatability σ ΔE00 > 0.5** in week 2. The file is not the main lever, so we pivot to the process root cause, not the advisor.
- **Instrument repeatability** is more than one-third of the tolerance and cannot be fixed with a better protocol or instrument.
- **Offline backtest:** predicted-vs-measured shade change RMS > 0.7 ΔE00 on held-out edits, or it does not beat the naive rule.
- **Live pilot:** fewer than 7 of the first 10 first-confirmation tiles pass, or any batch is released out of tolerance because of an advisor error.

---

## 6. Build plan and timeline (16 weeks from signed PO)

| Phase | Weeks | What happens | Milestone / gate | Depends on the client |
|---|---|---|---|---|
| 0. Learn and de-risk | 0-2 | Site visit, meet QC, baseline capture, instrument check, same-file repeatability test, decide tolerance | **G0:** repeatability and instrument OK | Signed PO and NDA; site access; QC time; sample master and variation tiles with files and readings shipped by end of week 1 |
| 1. Prove on their tiles | 2-6 | Offline model and backtest on their samples | **M1 (wk 4): first result**, an offline demo on the client's own tiles. **G1** | Calibration chart print and fire slot; readings in agreed format |
| 2. Build and shadow | 6-10 | Tool v1 (capture, solver, review screen, logging), on-prem install, shadow on live events | **G2:** advice matches or beats QC's final choice | IT approval for a plant-LAN server; printer file format and access; QC owner per shift |
| 3. Live pilot | 10-16 | Tool-assisted corrections on one line, with controls where possible | **M3 (wk 16): acceptance** against §5 thresholds | QC engineers using the tool; ≥ 12 eligible events; QC measurements |

**First result the client sees:** week 4 (offline, on their tiles). **First live result:** about week 10-11.

Client time needed: QC engineer about 4 h/week, project owner about 2 h/week, IT 1-2 days, one kiln slot for the calibration chart.

---

## 7. Cost

### 7.1 Effort and team (to us)

| Phase | FDE | ML / colour science | Full-stack | Person-weeks |
|---|---|---|---|---|
| 0 | 2 | 1 | 0 | 3 |
| 1 | 3 | 4 | 1 | 8 |
| 2 | 3 | 3 | 4 | 10 |
| 3 | 5 | 2 | 2 | 9 |
| **Total** | **13** | **10** | **7** | **30** |

### 7.2 Delivery cost

- Labour: 30 pw × USD 1,800 blended loaded rate = **54,000**
- Contingency 15% of labour = **8,100**
- Travel (two site trips) = **4,500**; courier, hosting, misc = **1,500**
- **Total = 68,100**

### 7.3 Running cost (per plant per year, after the pilot)

- Hosting: 300 × 12 = 3,600
- Support and model upkeep: 0.3 FTE × 52 wk × 1,800 = 28,080
- **To us ≈ 31,700.** To the client: an existing plant VM (or about 1,500 one-off mini-server) and about 15 min of QC time per event (≈ 90 h/yr at 360 events).

### 7.4 Price and payment structure

- **Pilot: fixed fee USD 85,000.** 30% (25,500) on signature, 30% (25,500) when the week-4 offline demo is accepted, **40% (34,000) only on meeting the §5 thresholds at week 16.** Our margin on the pilot is 85,000 − 68,100 = 16,900 (about 20%). It is deliberately thin because it is a wedge.
- **Production licence (optional, after the pilot): USD 120,000 per plant per year,** covering all digital lines, support, and retraining. Our margin is about 88,300 (74%).

### 7.5 Value to the client (assumptions are mine, to be replaced by the baseline)

| Input | Value | Source |
|---|---|---|
| Corrections per month per plant | 30 (3 lines × 10) | Assumption |
| Wrong-shade output per event | 5,000 m² | Low end of the client's 5-10k, which was unclear |
| Loss per m² | USD 1.00 | Assume USD 4 ex-factory, sold as downgraded at 25% discount |
| Waste avoided by the tool | 60% | Time to an approved file falls about 16 h → about 2 h, so 60% is conservative |
| QC labour | 1.3 fewer rounds × 4 h × USD 10/h | 2.5 rounds → 1.2 |

- Waste avoided = 30 × 12 × 5,000 × 0.6 × 1.00 = **USD 1,080,000 per year**
- QC labour = 360 × 1.3 × 4 × 10 = **USD 18,720 per year**
- **Total ≈ USD 1.1M per plant per year**, against pilot 85k + first-year licence 120k = 205k. About 5× in year 1.
- **Low case** (15 events/month, 40% reduction, USD 0.50/m²): 180 × 5,000 × 0.4 × 0.5 = **USD 180,000/yr**, which still covers the licence. Year 1 including the pilot fee would not pay back.
- The pilot line alone (10 events/month) is worth about USD 366k/yr, so the pilot fee is repaid in about 3 months of live value once rolled out.

---

## 8. Risks

| Risk | Likelihood / impact | Early signal | Mitigation |
|---|---|---|---|
| Process noise (kiln, ink lot) swamps the edit lever | Medium / **High** | Same-file repeatability test in week 2 | Gate G0; log context; pivot to root-cause work if it fails |
| Patterned tile: measured regions don't line up between master and production | Medium / High | Large point-to-point scatter | Acrylic mask; averaging windows; fewer, larger flat regions |
| Instrument not repeatable enough | Low-Med / High | Gauge study | Better protocol or a mid-grade instrument (client purchase, specified by us) |
| Model doesn't transfer across lines or plants | Medium / Med | Residual grows after moving lines | Per-line calibration chart (1 h); one plant first |
| QC distrust or low adoption | Medium / High | Overrides above 50% | Involve QC from week 1; show per-point reasoning; log and learn overrides |
| Printer file access is closed or awkward | Medium / Med | Q2 answer | Output file plus % table for manual loading; involve the OEM early |
| Too few events in 6 weeks to evaluate | Medium / Med | Event count at week 12 | Extend the pilot (price fixed), add a second line |
| Value figures are overstated | Medium / Med | Baseline vs §7.5 | Re-run the arithmetic on measured numbers before the licence discussion |
| Scope creep (inline vision, root cause, gloss) | High / Med | Requests in meetings | §3.3 in the contract; separate change orders |
| Single-FDE bus factor, procurement delay | Low-Med / Med | PO not signed by week 0 | Second engineer shadows; clock starts at the PO |

---

## Appendix A. Decisions I made where the notes were unclear

| Unclear point | What I decided and why |
|---|---|
| "5,000-10,000 m² [unclear]" | Used 5,000 (low end). The implied line rate of about 1,000 m²/h × one 6.5 h round ≈ 6,500 m², so the figure is plausible for one round. It is inconsistent with several rounds, so I left room. |
| "6-7 h per round" | Treated as elapsed time per round, including waiting. Process time may be lower. Baseline capture will separate waiting from working. |
| "6 primary colours" | Assumed they are 6 independent ink channels. Not verified. |
| "99% matching" | Treated as undefined. We define ΔE00 thresholds explicitly. |
| Which plant | India, to start. Nearest, easiest to visit. UAE plant later. |
| Kiln time | Assumed about 60 min per pass. Check on site. |
| Who measures | The plant's QC, with the plant's own spectrophotometer. |
| Gloss | Report only, because the print file is not a gloss lever. |

## Appendix B. What I did not trust in the notes

The 5-10k m² figure (flagged unclear by the transcript itself); "6 to 7 hours" (a team mapping, not a measurement); "5 to 6 minutes" (a hope, and impossible end to end with a kiln in the loop); "99% matching" (no stated metric); "if the first sample is right the whole batch is fine" (the single claim the batch-start design rests on, so I want within-batch drift data to confirm it); "this is simple" (it rarely is); "video analytics" (may be a word echoed from our own pitch, which was removed from the notes); and everything second-hand, since the people who actually do the work were not on the call.

## Appendix C. Event log (one row per correction)

`event_id, plant, line, sku, master_version, operator, timestamp, ink_lot[6], kiln_speed, kiln_temp, body_lot, file_in, file_out, readings_before[points × Lab/spectral], δ_proposed[6], δ_approved[6], predicted_ΔE00[points], readings_after[points], ΔE00_after, gloss_before/after, rounds, minutes_to_approved, visual_check, notes`
