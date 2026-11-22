---
type: Test Example
title: Good vs bad TC examples
description: Compares a vague TC (the kind AI often produces without knowledge) with a version that uses the bundle's knowledge, explaining each point.
tags: [testing, example, quality]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# Bad TC

> **TC-045: Check the payment allocation feature**
> 1. Go to the payment screen.
> 2. Enter the allocation information.
> 3. Save.
>
> Expected result: The system works correctly.

## Why it is bad

| Problem | Consequence |
|---|---|
| Generic title, no condition stated | No way to know which branch of the [rules](/domain/business-rules/payment-allocation-rules.md) is being tested |
| "Enter information" has no data | A newcomer cannot reproduce it |
| No precondition | No idea what invoice status or balance is needed |
| "Works correctly" cannot be verified | Pass or fail depends on feeling |
| Says nothing about the state after the action | Misses half-written data bugs |

# Good TC (using the bundle's knowledge)

The full version is in the [functional TC template](tc-templates/functional.md) (ID INV-ALLOC-003). Summary:

> **INV-ALLOC-003: Reject allocation when the amount exceeds the invoice balance**
> Precondition: invoice `SENT`, `due_amount = 100` (1.00); payment of the same customer and currency, `amount = 101` (1.01).
> Steps: allocate 101 to the invoice → Save.
> Result: error `payment_allocation_exceeds_invoice_balance`; no allocation row is created; `due_amount` stays 100, `paid_status = UNPAID`.

## Why it is good

* Tied to **exactly one** row of the rule table, so it is easy to trace when the rule changes.
* Has concrete figures in both display and stored form.
* The result is an **error code and DB state** that can be verified.
* Also checks "no side effects", the most common kind of error in money logic.

# Using it with AI

When asking AI to generate TCs, put into context: the [step conventions](step-conventions.md), the [TC template](tc-templates/functional.md), the relevant business rules, and this good/bad pair. Require the AI to quote **error codes and formulas from the rules**, not infer them.
