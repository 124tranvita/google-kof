---
type: Business Rule
title: Credit note rules
description: Conditions for full/partial credit notes, error codes, and the amount-calculation principle that keeps the sum of all credits equal to the original invoice.
tags: [credit-note, rounding, validation, error-codes]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
  - id: credit-calc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Support/CreditNoteAmounts.php
    title: CreditNoteAmounts
---

# Creating a credit note

Input: the list of lines to credit `[{id, quantity}]` and `reason` (optional, at most 1000 characters). **An empty list means credit the entire remaining quantity.**

| Violated condition | Error code |
|---|---|
| No quantity left to credit, or `total - collected - credited <= 0` | `invoice_already_fully_credited` |
| Credit quantity is greater than the invoiced quantity of the line | `credit_quantity_exceeds_remaining` |
| No line increased compared with the previous credit | `credit_note_must_credit_something` |
| `already credited + this time > total - collected` | `credit_amount_exceeds_invoice_balance` |

Everything runs in a transaction and **locks the original invoice row** before checking, because two concurrent credits could both pass the check and then exceed the invoice.[^credit-svc] After creation, the original invoice gets a [balance recalculation](balance-recalculation.md).

# Amount calculation principle ("telescoping")

The credit for the current call = `cumulative(after) - cumulative(before)`, always computed from the **stored figures of the original invoice**, not from earlier credit notes. This way crediting 3 units as 1+1+1 gives exactly the same cents as crediting 3 at once, and a fully credited invoice sums to exactly 0.[^credit-calc]

* Quantities are handled in **hundredths** (2.50 is 250), with no floating-point comparison.
* Rounding is half away from zero, the same rule as [total calculation](tax-calculation.md).
* **Fixed** tax lines are also split proportionally (not computed in full at the first credit).
* **Percentage** tax lines are split by the **stored** `taxes.amount`, not recomputed as `percent × base`.
* `base_*` columns are split by the original invoice's stored `base_*`, not multiplied by the exchange rate again.

# Consequences

* An invoice that already has a credit note **can no longer be edited**. See [edit lock](invoice-edit-lock.md).
* A credit note **does not accept payments**. See [allocation rules](payment-allocation-rules.md).
* Deleting the original invoice must delete its credit notes too. See the [state model](invoice-state-model.md).
* A credit note inherits the currency, tax mode and discount mode of the original invoice.

See the [regression map for credit note changes](/regression-map/credit-note-change.md).

[^credit-svc]: CreditNoteService::create and ::guard
[^credit-calc]: CreditNoteAmounts (class-level docblock)
