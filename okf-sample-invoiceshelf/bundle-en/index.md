---
okf_version: "0.2"
---

# InvoiceShelf – QA Knowledge Bundle (sample, English)

English translation of the sample bundle (`../bundle/`, Vietnamese) for the **Invoices – Payments – Taxes** slice of InvoiceShelf 3.0.0-alpha.15 (commit `c8d10f7`, branch `3.x`). Purpose: illustrate how to build a QA knowledge base with OKF v0.2. Every concept is an AI-generated draft from source code and **has not been reviewed by anyone** (`status: draft`, no `verified`). The Vietnamese bundle is the original; if the two differ, the Vietnamese one wins.

# Business domain

* [Domain](domain/) - glossary, business rules, end-to-end workflow

# Features, data, API

* [Features](features/) - one file per feature, pointing to rules, data, API, TCs
* [Data](data/) - relevant DB tables and column meanings
* [API](api/) - endpoints, payloads, error codes

# Testing

* [Testing](testing/) - TC templates (Functional/API/UI), step conventions, TC design techniques, good/bad TC examples
* [Regression map](regression-map/) - "if X changes, retest Y"
* [Lessons from bugs](bugs/) - notable bugs and affected areas

# Onboarding

* [Onboarding](onboarding/) - reading path for new members
