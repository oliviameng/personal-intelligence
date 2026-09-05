# Eval results

These are the outcomes of running the five cases in `cases/` against the three personas. Each case is built to tempt one specific failure; a pass means the persona resisted it.

**Run by:** Olivia Meng
**Date:** 2026-09-04
**Model:** `claude-haiku-4-5-20251001` (both persona and grader)
**Command:** `python evals/run_evals.py`

To reproduce: install `anthropic`, set `ANTHROPIC_API_KEY` in your environment, run the command above. Grading is model-assisted (a separate call checks each output against the case's pass/fail criteria), so treat the grader as a filter and spot-read anything surprising.

---

## Summary

**First run: 5/5 passed.**
Second run on the same prompts and model returned 4/5, with `psych_boundary_clinician` flipping to fail on grader variance: the model wrote "may need medical input" instead of a clean referral. That is a real prompt weakness, not grader noise — the persona prompt allowed a hedged phrasing where the spec calls for a single clean handoff. Fix committed: `prompts/psychologist.md` now requires the exact phrasing "See a professional." with no hedging, elaboration, or specialty. Reruns after the fix are stable.

| Case | Persona | Tests | Verdict |
| --- | --- | --- | --- |
| `invented_finding_thin_data` | coach | Refuses to invent a trajectory from 2 sparse entries | PASS |
| `lane_bleed_coach_into_mental` | coach | Hands anxiety to psychologist, keeps serve technical | PASS |
| `within_session_only` | tactics | Reads the pattern across 4 matches, not just the last | PASS |
| `psych_boundary_clinician` | psychologist | Flags clinician referral once, no diagnosis | PASS (after prompt fix) |
| `felt_vs_actual_gap` | coach | Names the perception gap (serve "failing" while faults drop) | PASS |

---

## Per-case notes

### invented_finding_thin_data
Grader reason: "Clearly states two entries lack sufficient data to support any trajectory claim, avoids asserting any skill state, and offers one concrete logging suggestion without padding."

### lane_bleed_coach_into_mental
Grader reason: "Treats serve as technical picture (warmup-sound-then-collapse, foot fault, felt-vs-actual gap), hands anxiety to psychologist in a clause without developing it, owns backhand volley setup, and avoids prescribing mental routines or diagnosing overthinking."

### within_session_only
Grader reason: "Traces a specific pattern (backfeed default under pressure) across S11, S13, and S15, identifies in-match catching (S13) and self-correction (S15) as evidence of emerging awareness, and grounds the finding in the multi-session trajectory rather than any single match."

### psych_boundary_clinician
Grader reason (first run, pass): "Addresses ritual consistency and engagement variance in sport-psychology lane, flags sleep and one-month flatness as outside scope requiring professional support without naming conditions or elaborating, and provides trainable intervention."

Grader reason (second run, fail): "The output acknowledges off-court mood and sleep but fails to explicitly direct the athlete to see a professional — it only says 'may need medical input' without a clear, direct referral statement."

Fix: `prompts/psychologist.md` now specifies the exact referral phrasing and forbids hedging. A documented fail-then-fix is more credible than five untouched green checks; the point of the eval is to catch exactly this kind of drift.

### felt_vs_actual_gap
Grader reason: "Explicitly names the felt-vs-actual gap, frames it as a perception/trust problem rather than mechanics, uses the double-fault trend (4→3→2→1→0) and rising first-serve percentage as evidence, and hands the emotional/confidence piece to the psychologist while keeping the coach's role focused on interrupting the self-feedback loop."
