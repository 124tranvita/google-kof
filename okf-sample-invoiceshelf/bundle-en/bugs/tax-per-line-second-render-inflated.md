---
type: Bug Lesson
title: Rendering an invoice several times inflates per-line tax
description: "A real bug fixed in InvoiceShelf 3.0 alpha 13: the second render of the same document with per-line tax printed an inflated tax amount."
tags: [bug, tax, pdf, side-effect]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
sources:
  - id: changelog
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/CHANGELOG.md
    title: CHANGELOG (alpha 13 release, issue #934)
---

# Description

According to the CHANGELOG: rendering an invoice or estimate with **per-line tax** used to change the very tax lines it was reading, so the **second** render of the same document (for example sending mail after downloading) printed an **inflated** tax amount. Fixed in #934.[^changelog]

> The detailed cause was not verified here (the diff was not read). What follows is the lesson drawn from the CHANGELOG description.

# Lessons for QA

* **Reading must not change data.** Every "view only" operation (render PDF, preview, download, send mail, open a public link, customer portal) needs a repeated-run TC.
* The bug appears only on the **second run**, so a TC that runs once will miss it.

# TCs to have (sample)

1. Create an invoice with `tax_per_item = YES`, one percentage tax per line. Record the total tax T.
2. Download the PDF the first time, then a second time, then send a preview mail. Expected: the printed tax is the same and equals T all three times.
3. Reopen the invoice on the admin screen and through the customer portal: the tax is still T; the `taxes` records in the DB are unchanged.

# Affected area

[When tax calculation changes](/regression-map/tax-change.md), row #5.

[^changelog]: CHANGELOG, bug-fix section of the alpha 13 release (#934)
