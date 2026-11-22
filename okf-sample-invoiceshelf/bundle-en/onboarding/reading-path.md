---
type: Onboarding Guide
title: 5-day reading path for a new QA
description: Reading order for the bundle with a daily exercise so a new member learns the invoice, payment and tax domain and how to write TCs.
tags: [onboarding, reading-path]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

> A proposed path; the durations are estimates. The mentor should adjust it to reality before marking it reviewed.

# Day 1: Vocabulary and the big picture

1. [Invoice](/domain/glossary/invoice.md), [Credit note](/domain/glossary/credit-note.md), [Payment allocation](/domain/glossary/payment-allocation.md), [Minor units](/domain/glossary/minor-units.md).
2. [Invoice to cash](/domain/workflows/invoice-to-cash.md).

**Exercise**: redraw the flow and fill in `status`/`paid_status` at each step yourself, without looking at the document.

# Day 2: Status and balance

1. [State model](/domain/business-rules/invoice-state-model.md).
2. [Balance recalculation](/domain/business-rules/balance-recalculation.md).

**Exercise**: given an invoice with total 300, a payment of 100 already allocated and a credit of 50, compute `due_amount` and `paid_status`. Answer: `due_amount = 300 - 100 - 50 = 150`, `paid_status = PARTIALLY_PAID` (because there is an allocation), `status` goes back to the previous state. Then try the variant with no payment, only a credit of 50, and explain why `paid_status` is `UNPAID`.

# Day 3: Allocation and credit notes

1. [Allocation rules](/domain/business-rules/payment-allocation-rules.md).
2. [Credit note rules](/domain/business-rules/credit-note-rules.md).

**Exercise**: pick any 3 error codes from the table and write TCs using the [API template](/testing/tc-templates/api.md).

# Day 4: Tax

1. [Tax calculation](/domain/business-rules/tax-calculation.md), [tax types](/domain/business-rules/tax-type-rules.md).
2. [TC design for money and rounding](/testing/test-design/money-and-rounding.md).

**Exercise**: compute 3 examples from the table by hand, then create 2 more examples with compound tax and tax-included.

# Day 5: Writing TCs to standard, and lateral testing

1. [Step conventions](/testing/step-conventions.md), [good vs bad TC](/testing/good-vs-bad-tc.md).
2. [Regression map](/regression-map/) and the [bug lesson](/bugs/tax-per-line-second-render-inflated.md).

**Exercise**: suppose the "allocation rules" gain a new condition. Use the regression map to list the areas to retest and write the 5 highest-priority TCs.
