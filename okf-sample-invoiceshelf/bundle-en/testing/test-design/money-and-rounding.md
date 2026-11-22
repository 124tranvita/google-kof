---
type: Test Design Guide
title: TC design for money, tax and rounding
description: "TC design techniques for money logic: boundaries, rounding, invariants to check after every operation, flag matrix, foreign currency, concurrency."
tags: [testing, test-design, money, rounding, tax]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# 1. Invariants: check after EVERY operation involving money

Best written as a shared "Check invariants" step (it can be a SQL query or a read API call).

| # | Invariant | Source |
|---|---|---|
| B1 | `due_amount = max(0, total - Σ allocation - Σ credit)` | [Balance recalculation](/domain/business-rules/balance-recalculation.md) |
| B2 | Σ allocation of one payment ≤ `payment.amount` | [Allocation rules](/domain/business-rules/payment-allocation-rules.md) |
| B3 | A fully allocated payment: Σ `base_amount` of its rows = `payment.base_amount` | same source |
| B4 | `due_amount = 0` ⇒ `status = COMPLETED` and `paid_status = PAID` | [Balance recalculation](/domain/business-rules/balance-recalculation.md) |
| B5 | A credit note has a negative total; Σ credit per line ≤ the original line quantity | [Credit note rules](/domain/business-rules/credit-note-rules.md) |
| B6 | Fully crediting in pieces (1+1+1) gives exactly the same fields as crediting once | same source |

# 2. Boundary values

* **Allocation**: amount = 0 (rejected), 1, balance − 1, **balance**, balance + 1.
* **Overdue**: `due_date` = yesterday, **today** (not yet overdue), tomorrow. See [overdue](/domain/business-rules/invoice-state-model.md).
* **Credit**: quantity = remaining quantity, remaining + 0.01, and a chain of several credits until exhausted.
* **Total**: near the maximum `total` of 999999999999 and beyond it.

# 3. Rounding

* Rule: round **half away from zero** (0.5 → 1, -0.5 → -1). See [total calculation](/domain/business-rules/tax-calculation.md).
* Suggested data: price × a decimal quantity giving a .5 part (for example quantity 2.50), percentage tax producing fractions, negative quantities.
* For partial credits, pick a line with quantity 3 and a line total **not divisible by 3** to expose cent drift. Expected: the sum of three credits equals exactly one credit of everything (B6).

# 4. Matrix of money flags

The flags that affect the formula: `tax_per_item` (YES/NO), `discount_per_item` (YES/NO), `tax_included` (true/false), and whether a compound tax exists. The full set is 16 combinations; use **pairwise** to reduce it, but always keep these combinations:

* all off (baseline);
* `tax_included = true` + compound (compound is still added);
* `tax_per_item = YES` + a document-level tax with a value (the document-level tax is ignored);
* `discount_per_item = YES` + a document-level discount at the same time.

# 5. Foreign currency

* An exchange rate with decimals (for example 1.234567). Check that every `base_*` column is an integer and consistent.
* A foreign-currency payment allocated to several invoices: check B3 (the last row takes the remainder).
* Change the company currency and then update the exchange rate of old documents: each amount must be converted from its own value. The CHANGELOG records an old bug here (discount taken from the subtotal and tax converted twice, #862), so this is an easy area to regress.

# 6. Concurrency

Two requests allocating or crediting the same invoice at the same time. Expected: the system locks the row, only one request succeeds if the total exceeds the balance, and there is never a negative `due_amount` or a total above the invoice.

# 7. Multi-company and permissions

Every endpoint needs the `company` header. Test across companies: call with company B's `company` but company A's invoice id. Test roles (`owner`, the Manager preset, Read only) for every write operation.
