# Prompts

Three personas read the same athlete log and each write one section of the Staff Report: **coach** (technical), **psychologist** (mental), **tactics** (strategy). `_shared_rules.md` is prepended to all three.

## The design decision this rests on

The point of the system is not the personas. It is that an LLM reads **across** sessions where a person reads within one. You notice how today went; the model notices that your serve has been stuck the same way for three weeks and that the stuckness is trust, not mechanics. Everything else serves that.

That decision has a cost, and the cost is the price of admission: the entry format has to be rigid and the same every time, or cross-session comparison breaks. A looser, friendlier capture format would be easier to write and useless to read across. The rigidity is the feature.

## Why three, not five

An earlier version had five roles (added physio and nutritionist). They were cut. Nutrition and recovery data in a personal log is too thin to earn a standing voice, and a persona that usually has nothing to say teaches the model that filling space is expected. Three roles that reliably have signal beats five where two pad. Cutting a role you designed is the same judgment as adding one; both are editorial.

## Boundaries (what these are not)

- Not a medical or mental-health tool. The psychologist names trainable patterns, never diagnoses; if a log needs a clinician, the answer is "see a professional," said once.
- Not exhaustive. Each persona reports the two or three patterns that matter this block, not everything it noticed.
- Not a coach replacement. Coach's Notes is written to hand to a real coach, who has context the log does not.

## How it runs

`synthesis/run.py` prepends `_shared_rules.md` to each persona, feeds the block's entries, and concatenates the three sections into one Staff Report. The evals in `../evals/` check that each persona stays in lane, refuses to invent findings, and reads across rather than within.

## Porting to another domain

Swap the three personas; keep the rules file. Writing: line editor, structural critic, target reader. A codebase: reviewer, architect, the engineer who inherits it. The cross-session rule and the boundaries do not change.
