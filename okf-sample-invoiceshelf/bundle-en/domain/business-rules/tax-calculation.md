---
type: Business Rule
title: Tax and invoice total calculation
description: The server recomputes sub_total, tax and total from line items; per-item, discount, compound and tax-inclusive rules, with numeric examples.
tags: [tax, total, rounding, compound-tax]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: totals
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Support/DocumentTotals.php
    title: DocumentTotals
  - id: totals-test
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/tests/Unit/DocumentTotalsTest.php
    title: DocumentTotalsTest
---

# Principle

The server **does not trust** the `total`, `sub_total`, `tax`, `due_amount` sent by the client (advisory GHSA-8c69). It trusts only price, quantity, discount and the **amount of each tax line**. Totals are recomputed by `DocumentTotals::compute`.[^totals]

> Note for QA: the create-invoice payload still **requires** the fields `total`, `sub_total`, `tax`. The submitted values are ignored and recomputed, but the `amount` of each tax line sent by the client is still used. This is a point that needs security/tamper TCs.

# Formula

```
item_total   = round(price × quantity) - item_discount        # item_discount applies only when discount_per_item = YES
sub_total    = Σ item_total
after_disc   = sub_total - round(discount_val)                # document-level discount
taxes        = if tax_per_item = YES: taxes on each line (lines without tax_type_id are skipped)
               otherwise: document-level taxes
               split into a simple group and a compound group
tax          = simple + compound
total        = tax_included ? after_disc + compound : after_disc + tax
```

* `round` is half away from zero.
* With `tax_included = true`, simple tax is already inside the price so it is **not added**, but **compound tax is still added**.
* Negative quantities are supported.

# Numeric examples (from the unit test, minor units)

| # | Input | Result |
|---|---|---|
| 1 | 1 line, price 10000 × 10, no tax | `sub_total` 100000, `tax` 0, `total` 100000 |
| 2 | 1 line 1000 × 2; document tax 150; document discount 500 | `sub_total` 2000, `tax` 150, `total` 1650 |
| 3 | `tax_per_item = YES`; line taxes 100 and 200; document tax 9999 | `sub_total` 3000, `tax` 300, `total` 3300 (document tax ignored) |
| 4 | Tax-included; price 1000; tax 100 | `total` 1000, `tax` 100 |
| 5 | Line 1000 × 2, `discount_val` 300; `discount_per_item` = YES / NO | `sub_total` 1700 / 2000 |
| 6 | Quantities -2 × 100, 1 × 50, 0 × 75 | `sub_total` -150 |
| 7 | 10000; tax 1900 and compound tax 119 | `tax` 2019, `total` 12019 |

The examples above are taken verbatim from the unit test.[^totals-test]

# Related

* [Tax type rules](tax-type-rules.md)
* [Credit notes split tax proportionally](credit-note-rules.md)
* [TC design for money and rounding](/testing/test-design/money-and-rounding.md)
* [Regression map for tax changes](/regression-map/tax-change.md)

[^totals]: DocumentTotals (class-level docblock)
[^totals-test]: DocumentTotalsTest
