# Submission Form: Task 3, Forward Deployed Engineer Case Study (Client A, Ceramic Tiles)

**Case study:** case-study.md
**One-page client note:** note-to-procurement.md

---

### 1. In two sentences: what is the client's real problem, and how is it different from what they asked for?

They asked for a vision system that compares the master and production tile. The real problem is a control problem: they can already measure the shade gap with a spectrophotometer, but nobody can turn that gap into "change brown by X%", so QC guesses by eye and loops for 6-7 hours per round. The need is a recommended edit to the print file at batch change, approved by QC, not an always-on camera on the line.

### 2. Who are the people in this deal, and what does each need to hear from you?

- **Special Projects Lead** (champion): wants proof it works. Hear: a demo on your own tiles in week 4; the 5-minute number is the decision step, because the kiln is in the loop.
- **Head of IT & OT Procurement** (gatekeeper): wants low vendor risk. Hear: software only, existing instruments, nothing connected to the line, data can stay on-site, fixed price with milestone payments, no hardware resale.
- **Plant QC & design team** (real users, not on the call): fear being replaced or blamed. Hear: the tool suggests, you approve; it removes the 6-variant guessing, not your judgement. Get them on the next call.
- **Plant / production head:** wants fewer m² in the wrong shade and no downtime. Hear: zero new downtime; savings measured against a baseline.
- **Printer OEM / ink supplier:** may control file access and may already sell closed-loop tools. Engage early.
- **Finance sponsor** (unknown): wants payback in money. Hear: the arithmetic and a thin first-year downside.

### 3. The five questions you would ask on the next call, ranked. For each: why it matters and what you assumed while you wait.

1. **If you print and fire the same file repeatedly, how much does the shade move (within a shift, across days, ink lots, kiln lanes)?** Why: if process noise exceeds the tolerance, editing the file cannot converge, which is the kill-risk. *Assumed:* same-file σ ΔE00 ≤ 0.4, slow drift; I test it in week 2 and stop if it is > 0.5.
2. **What exactly is the input we change (file format, channels, RIP/ICC, per-channel curves) and can software write it?** Why: it defines the output and what can be automated. *Assumed:* 6 editable ink channels in an image file, QC loads files manually; I output a ready file plus a % table.
3. **What counts as "matching" (ΔE formula, tolerance, gloss tolerance, who decides)?** Why: success and stop criteria cannot exist without it. *Assumed:* ΔE00 mean ≤ 1.0, max ≤ 1.5 over 6-8 points; gloss reported only.
4. **What history exists (old Photoshop edits with before/after files and readings) and how many re-runs per line per month?** Why: decides pre-training vs prospective collection, and the size of the value. *Assumed:* patchy history, about 30 corrections per month per plant; I rely on a calibration chart and their sample tiles.
5. **Which spectrophotometer, geometry and aperture, and how are matching regions found on a patterned tile?** Why: all input depends on repeatable readings of the same regions. *Assumed:* d/8, about 8 mm aperture, 6-8 fixed points per SKU placed with an acrylic mask, repeatability ≤ 0.15 ΔE00.

### 4. Which options did you consider, and why did you pick the one you did? What did you rule out, and why?

Considered: (A) SOP and tolerance only; (B) printer OEM closed-loop tools; (C) measurement plus correction advisor with human sign-off; (D) inline vision or hyperspectral cameras; (E) end-to-end deep learning; (F) root-cause engine.
**Picked C:** it targets the actual pain (batch change), uses instruments they already own, needs little data because it predicts the *change* from a small edit anchored to a measured tile, is explainable to QC, and proves value in 16 weeks with no capex.
**Ruled out:** D (the problem is at changeover, camera colour is not colorimetric, needs capex and OT integration); E (not enough paired data, unexplainable, unsafe when wrong); F (client agrees it is hard; I only log context for later). A stays as part of the pilot, and B is checked first and bought if it exists.

### 5. How will the client know the pilot worked? Metric, baseline, threshold, how many runs, who measures, and what would make you stop.

- **Primary metric:** hours from first failed sample to an approved file. **Baseline:** assumed about 16 h (2.5 rounds × 6.5 h), measured on the last ≥ 20 events plus 5 live events in weeks 0-2. **Threshold:** median ≤ 3 h.
- **Co-primary:** first-confirmation pass rate ≥ 75% (≥ 9 of 12 events). With 12 events, a true 50% process passes by luck 7% of the time and a true 80% process passes 79% of the time.
- **Guardrail:** final tile ΔE00 mean ≤ 1.0 and max ≤ 1.5, and no visual fail by the QC lead.
- **Runs:** at least 12 live events on one line, plus 8-10 shadow events and 4 or more concurrent manual controls where possible.
- **Who measures:** the plant's QC, with their own spectrophotometer, after a gauge repeatability check. Not us.
- **Stop if:** same-file repeatability σ ΔE00 > 0.5 (the file is not the lever); instrument repeatability is over a third of the tolerance; the offline backtest RMS error is > 0.7 ΔE00 or it does not beat a naive rule; fewer than 7 of the first 10 live first-confirmation tiles pass; or any batch is released out of tolerance because of an advisor error.

### 6. What does this cost the client, and what does it cost us to deliver? Show the arithmetic and name the pricing structure. What value does the client get, in their money?

- **Our cost:** 30 person-weeks (13 FDE + 10 ML + 7 full-stack) × USD 1,800 = 54,000; + 15% contingency 8,100; + travel 4,500; + misc 1,500 = **USD 68,100**.
- **Price:** fixed-fee pilot **USD 85,000** (30% on signature, 30% on week-4 demo acceptance, 40% only on meeting the thresholds), a margin of 16,900 (about 20%). Optional licence **USD 120,000 per plant per year** against about 31,700 running cost to us.
- **Value (my assumptions, to be replaced by the baseline):** 30 corrections/month × 12 × 5,000 m² × 60% avoided × USD 1.00/m² = USD 1,080,000, plus QC labour 360 × 1.3 rounds × 4 h × USD 10 = USD 18,720, so about **USD 1.1M per plant per year**. Low case (15 events/month, 40% avoided, USD 0.50/m²) = USD 180,000, which still covers the licence.

### 7. Timeline. What is the first result the client sees, and when? Which steps depend on the client rather than on us?

- **First result: week 4**, an offline demo on the client's own sample tiles (what the difference is between master and test tile, and how much to change the file). Baseline at week 2. First live use at about weeks 10-11. Acceptance at week 16.
- **Client dependencies:** signed PO and NDA before week 0; sample tiles, files and readings by end of week 1; QC time (about 4 h/week) and site access; the tolerance decision; a kiln slot for the calibration chart; IT approval for a plant-LAN server; printer file format and access; at least 12 eligible events in the live window.

### 8. Where did you push back on the client, narrow their ask, or tell them not to do something?

- Told them "5-6 minutes" is only achievable for the decision, not end to end, because the kiln is in the loop. The honest target is about 2 hours to an approved file.
- Narrowed from a line-wide vision system to a batch-change check, based on their own statement that a correct first sample means the batch is fine.
- Told them gloss will be reported and flagged, not corrected, since the print file does not control it.
- Told them not to pursue root cause now, and not to rely on old reference files. The physical master, measured, is the target.
- Told them "99% matching" must become a stated ΔE00 tolerance.
- No auto-push to the printer without QC sign-off, no hardware purchase during the pilot, and one plant and one line before any rollout.

### 9. What is most likely to go wrong with your plan, and what in these notes did you not trust?

**Most likely to go wrong:** process noise (kiln, ink lots) is larger than the tolerance, so the file edit cannot be the lever. I test this in week 2 before spending most of the budget. Next most likely: patterned tiles whose measured regions do not line up, QC not adopting the tool, and too few live events in 6 weeks.
**Did not trust:** the 5-10k m² figure (the transcript itself marks it unclear); "6-7 hours" (a team mapping, possibly including waiting time); "5-6 minutes" (a hope); "99% matching" (no metric); "if the first sample is right the whole batch is fine" (the one claim the design rests on, so I want within-batch drift data); "video analytics" (possibly echoed from our removed pitch); and everything second-hand, since QC were not on the call.

### 10. What did you use AI for? Which tools, where they helped, where they misled you, and what you threw away.

I used Claude (claude.ai) as the main drafting and stress-testing tool. It produced the first full draft of the case study, the procurement note and this form from the discovery notes and the brief. It also checked the arithmetic: cost totals, the 9/12 binomial figures and the value model.

**Where it helped:** turning the messy notes into a ranked list of unknowns, each with a stated assumption. It also helped set measurable thresholds and stop criteria, and spot that the "5-6 minutes" target can't hold end to end because the kiln is in the loop.

**Where it misled or was weak:**
- It filled gaps with plausible numbers that the notes do not support: about 60 min kiln time, USD 1.00 loss per m², USD 1,800 per person-week, 30 corrections per month, and the ΔE00 tolerance. I treat all of these as labelled assumptions to be replaced by the baseline in weeks 0-2, not as facts.
- The transcript says the 5,000-10,000 m² figure is unclear, and an early reading of it did not fit several rounds of 6-7 hours. I used the low end (5,000 m²) and flagged the inconsistency in Appendix B rather than trusting it.
- Some wording was more confident than the evidence allows, for example the "about 5× in year 1" value claim. The low case in the case study shows year 1 would not pay back.

**What was thrown away:**
- An always-on vision system, whether cameras or hyperspectral imaging, on the line. The problem occurs at batch change, and camera colour is not colorimetric without heavy calibration.
- An end-to-end deep learning model that maps an image to a corrected print file. There is no paired data for it, and QC could not inspect why it suggested a change.
- A root-cause engine for kiln and raw-material drift. The client says it isn't realistic, so we log context for later instead.
- Gloss correction through the print file, because the print file isn't a gloss lever. Gloss is reported only.
- The "5-6 minutes end to end" promise, replaced with "5 minutes for the decision, about 2 hours to an approved file".

Claude also wrote the synthetic prototype (`prototype/`). Its first version misled me: it reported about 3.4 rounds to converge because the simulated drift included an offset that no ink change could correct, so even a perfect oracle passed only half the time. I added an oracle solvability check to the notebook and fixed the drift model. The results are from a simulated device, so they show the mechanism works under my assumptions, not that it works on real tiles.


### Github Repo URL

https://github.com/harshupadhyay14/Task-3---Forward-Deployed-Engineer-Case-Study.git

Prototype (synthetic data only): `tile_shade_advisor_prototype.ipynb` plus `sim.py`. It tests one claim from section 4.3 and 5 of the case study: a calibration chart, a local sensitivity solve and one confirmation tile converge to tolerance in about one round, and convergence breaks down when same-file print repeatability is poor (the week-2 stop line). It is a simulation of an assumed device, not evidence about real tiles.
