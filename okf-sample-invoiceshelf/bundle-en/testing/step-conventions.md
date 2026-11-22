---
type: Test Convention
title: Step and TC writing conventions
description: "Mandatory rules when writing TCs (human or AI): naming, numbering, concrete data, expected results, traceability."
tags: [testing, convention, step]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

> This is a **starting proposal** written by AI. The team must agree on it and adjust it before treating it as a standard. Once agreed, the authorized person records `verified: { by: human:<id>, at: ... }` in the frontmatter.

# General rules (the AI must follow them when generating TCs)

1. **One TC checks one thing.** Title pattern: `<Action> + <condition> → <result>`. Example: "Reject allocation when the amount exceeds the invoice balance".
2. **ID pattern** `<MODULE>-<FEATURE>-<3-digit number>`, for example `INV-ALLOC-003`.
3. **Each step is one action** by one actor. Start with a verb: "Call", "Press", "Enter", "Select". Do not merge several actions into one step.
4. **Concrete data, not generic descriptions.** Write "Amount: 1.01 (101)" instead of "enter a large amount". Money is always written with **both the displayed and the stored value** (see [minor units](/domain/glossary/minor-units.md)).
5. **Expected results must be verifiable**: field values, error codes, statuses, DB records. The phrases "works correctly" and "displays normally" are forbidden.
6. **For negative TCs, state clearly which state does NOT change.** For example "No allocation record is created; `due_amount` stays 100".
7. **Preconditions describe the data state** (customer, currency, invoice status, balance), not just "logged in".
8. **Traceability**: each TC has a "Related rule" line pointing to a concept in the bundle (for example [allocation rules](/domain/business-rules/payment-allocation-rules.md)).
9. **Business terms** follow the glossary exactly; do not invent new names.
10. **Data after the test**: state how to clean up or use independent data so the TC can be rerun.

# Final checklist (the AI reviews itself before submitting)

* [ ] Does every expected result have a concrete figure or error code?
* [ ] Is there a negative TC for each error-code row in the related rule?
* [ ] Are there boundary TCs (0, 1, the value just below/above the threshold)?
* [ ] Is there a TC checking that the state is unchanged when rejected?
* [ ] Are the TCs independent, with no dependency on run order?

See [good vs bad TC](good-vs-bad-tc.md) for how to apply this.
