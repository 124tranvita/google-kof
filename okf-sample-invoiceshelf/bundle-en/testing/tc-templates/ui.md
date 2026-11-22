---
type: Test Template
title: UI TC template
description: "Structure of a UI TC: screen, actions, messages, display state; screen/button names are filled in by the project."
tags: [testing, template, ui]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

> This sample bundle was generated from backend source code, so it has **no real screen names or button labels**. In a real project, fill in the items marked `[...]` from the UI spec or screenshots.

# Structure

```markdown
## <ID> - <Action + condition → displayed result>

| Item | Content |
|---|---|
| Type / Priority | ... |
| Screen | [Screen name per the spec] |
| Related rule | <concept link> |
| Browser / device | ... |

**Precondition**: <account, role, data>
**Steps**
1. Open the screen [screen name].
2. Enter [field name] = <concrete value>.
3. Press the button [button label].
**Expected result**
- Message: "<verbatim message>" (shown at [location]).
- Field/label: <name> shows <concrete value, money/date format>.
- Button/field state: <enabled/disabled/read-only>.
**Check afterwards**: reopen the screen, the data is still correct.
```

# UI-specific things to check

* **Display format** of money and dates according to the company settings (for example the stored value `1000` is displayed as `10.00`). See [minor units](/domain/glossary/minor-units.md).
* **Buttons locked by status**: the invoice edit function depends on the [edit lock](/domain/business-rules/invoice-edit-lock.md).
* **Error messages**: the backend returns an **error code** (for example `payment_allocation_exceeds_invoice_balance`); the wording the user sees is decided by translation. UI TCs should record the verbatim text for each language to be tested.
* The **customer portal** has its own screens for invoices, estimates and payment history, and needs separate permission TCs.
