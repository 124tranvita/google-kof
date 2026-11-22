---
type: Glossary Term
title: Minor units and base_ columns
description: Every stored amount is an integer in minor units (cents); each money column has a base_ counterpart converted to the company currency.
tags: [glossary, money, rounding]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice model
  - id: changelog
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/CHANGELOG.md
    title: CHANGELOG
---

# Definition

* Amounts are **integers** in minor units. For example `1000` means 10.00 if the currency has two decimal places.[^invoice-model]
* Each money column has a `base_` counterpart (for example `base_total`, `base_due_amount`) equal to the amount times the document's exchange rate, so the company can report in its base currency without converting again.
* Only two values are real numbers: the discount percentage (`discount`) and the exchange rate (`exchange_rate`).
* Amounts converted to the base currency are **rounded to whole cents before being stored**, everywhere they are written (documents, line items, taxes, copies, recurring invoices, payments, balances). The exchange rate keeps its decimals.[^changelog]

# Consequences for QA

* When writing TCs, always write both the displayed value and the stored value (for example "10.00 (1000)").
* Foreign-currency TCs with a fractional exchange rate are needed. See [TC design for money and rounding](/testing/test-design/money-and-rounding.md).

[^invoice-model]: Invoice model (docblock)
[^changelog]: CHANGELOG, the PostgreSQL fix for fractional exchange rates (#798, #862, #864)
