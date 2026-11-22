# Glossary

* [Invoice](glossary/invoice.md) - one table, two document types, two status axes
* [Credit note](glossary/credit-note.md) - reverses an invoice, negative amounts
* [Payment allocation](glossary/payment-allocation.md) - splitting one payment across several invoices
* [Minor units](glossary/minor-units.md) - money stored as integers, `base_` columns

# Business rules

* [Invoice state model](business-rules/invoice-state-model.md) - status, paid_status, overdue, deletion
* [Balance recalculation](business-rules/balance-recalculation.md) - the due_amount formula
* [Payment allocation rules](business-rules/payment-allocation-rules.md) - validity conditions and error codes
* [Credit note rules](business-rules/credit-note-rules.md) - conditions, partial amounts
* [Tax and total calculation](business-rules/tax-calculation.md) - exclusive/inclusive, compound, per-item
* [Tax type rules](business-rules/tax-type-rules.md) - snapshot, deletion, EN 16931 codes
* [Invoice edit lock](business-rules/invoice-edit-lock.md) - the retrospective_edits setting

# Workflows

* [Invoice to cash](workflows/invoice-to-cash.md) - end-to-end flow
