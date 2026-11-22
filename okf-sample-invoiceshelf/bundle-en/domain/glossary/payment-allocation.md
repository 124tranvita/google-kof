---
type: Glossary Term
title: Payment allocation
description: A portion of a payment assigned to a specific invoice; the unassigned remainder is unapplied customer credit.
tags: [glossary, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Application/PaymentAllocationService.php
    title: PaymentAllocationService
---

# Definition

A payment (`Payment`) can be **split across several invoices**. Each split is a record in [customer_payment_allocations](/data/customer-payment-allocations.md), with `amount` and `base_amount`.

* **Unapplied customer credit**: the part of a payment that has not been allocated. An empty allocation list is still valid and represents exactly this case.[^alloc-svc]
* Each (payment, invoice) pair has only **one** allocation row (unique).
* The money allocated to an invoice is an input of [balance recalculation](../business-rules/balance-recalculation.md).

Validity rules: see [payment allocation rules](../business-rules/payment-allocation-rules.md).

[^alloc-svc]: PaymentAllocationService::replace docblock
