---
type: Glossary Term
title: Credit note
description: A document that reverses an invoice in whole or in part, carrying negative amounts.
tags: [glossary, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
---

# Definition

A row in `invoices` with `type = CREDIT_NOTE`, pointing back to the original invoice through `related_invoice_id`. Each credit note line has `source_invoice_item_id` pointing to the original line it reverses.[^credit-svc] The code comments call it *Stornorechnung*.

Main differences from a regular invoice:

* Amounts are **negative**.
* It does not accept payments. See [allocation rules](../business-rules/payment-allocation-rules.md).
* It is numbered separately using the `credit_note_number_format` setting.
* It can credit **partially**, by quantity per line. See [credit note rules](../business-rules/credit-note-rules.md).

[^credit-svc]: CreditNoteService (class-level docblock)
