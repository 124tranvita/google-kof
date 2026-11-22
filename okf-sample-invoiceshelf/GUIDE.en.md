# Sample OKF bundle: InvoiceShelf (Invoices – Payments – Taxes)

[Tiếng Việt](HUONG-DAN.md) · English

This directory is an example showing how to build a knowledge base in **Open Knowledge Format v0.2** for QA work. It is **not** your project's knowledge. The original bundle (`bundle/`) is in Vietnamese; `bundle-en/` is its English translation.

```
okf-sample-invoiceshelf/
├── HUONG-DAN.md            # Vietnamese guide (outside the bundle)
├── GUIDE.en.md             # this file (outside the bundle)
├── tools/check_bundle.py   # bundle checker based on the spec
├── bundle-en/              # English translation of the bundle (same structure)
└── bundle/                 # ← the original Knowledge Bundle (35 concepts, Vietnamese)
    ├── index.md            # root index, declares okf_version: "0.2"
    ├── log.md              # change log
    ├── domain/             # glossary, business-rules, workflows
    ├── features/           # one "hub" file per feature
    ├── data/               # DB tables
    ├── api/                # endpoints, payloads, error codes
    ├── testing/            # TC templates, step conventions, TC design, good vs bad examples
    ├── regression-map/     # "if X changes, retest Y"
    ├── bugs/               # lessons from real bugs
    └── onboarding/         # 5-day reading path
```

**Suggested reading order:** `bundle-en/index.md` → `domain/business-rules/balance-recalculation.md` → `testing/good-vs-bad-tc.md` → `regression-map/payment-allocation-change.md`.

## 1. Why InvoiceShelf

Open source (Laravel + Vue), with a domain close to your project: invoices, taxes, payments, credit notes, tax reports. It has automated tests, so findings can be cross-checked. Version used: **3.0.0-alpha.15, commit `c8d10f7`, branch `3.x`**. It is an alpha, so some behaviour may have changed since.

I covered only **one slice** (Invoices – Payment allocation – Credit notes – Taxes), enough to show the whole method.

## 2. The process followed (you can repeat it on your project)

1. **Read the original OKF spec** (`SPEC.md` v0.2 on GitHub) to learn which fields are required and which optional.
2. **Survey the code by slice**: models, business services, request validation, routes, migrations, tests.
3. **Extract what QA needs**: formulas, validity conditions, **error codes**, boundary values, DB constraints, quirks.
4. **Write each as one concept**, point `sources` at the code files, use footnotes to attribute each important claim.
5. **Connect with links**: feature ↔ rule ↔ data ↔ API ↔ tests ↔ regression map.
6. **Check**: run the checker for conformance/links/footnotes, and validate YAML syntax with a separate tool.

On a real project, steps 2 and 3 are done with AI reading source, DB and specs, then **reviewed by a BA/QA lead**.

## 3. Mapping to your project (voucher registration, tax settlement)

| In the sample | In your project |
|---|---|
| `domain/glossary/` (invoice, credit note) | Terms for vouchers, settlement, tax period, registration status (JP–VN–EN) |
| `business-rules/tax-calculation.md` (formula + 7 numeric examples) | Tax calculation, rounding, voucher registration conditions, with numeric examples taken from the spec |
| `business-rules/payment-allocation-rules.md` (error-code table) | A table of valid conditions ↔ error codes/messages for each input screen |
| `data/*.md` | Main DB tables, column meanings, keys, constraints |
| `testing/tc-templates/` + `step-conventions.md` | Turn your existing TCs into templates: pick the 5–10 **best** TCs as the standard |
| `testing/good-vs-bad-tc.md` | Take one confusing AI-written TC and your corrected version |
| `regression-map/` | "If feature A changes, retest B, C", from code dependencies and bug history |
| `bugs/` | Bugs seen: root cause, affected area, the TC that caught it |
| `onboarding/` | Reading path for newcomers |

The **most valuable** parts for you are `business-rules` (tax logic), `testing/` (fixing hard-to-read TCs) and `regression-map/` (fixing the difficulty of testing laterally).

## 4. OKF v0.2 features demonstrated

| Feature | Where |
|---|---|
| `type` (required), `title`, `description`, `tags` | every concept |
| `resource` (ties a concept to a concrete asset) | `data/*.md` |
| `sources` + footnotes attributing each claim | `domain/business-rules/credit-note-rules.md` |
| `generated` (who/what produced the content) | every concept, `claude-code/claude-sonnet-5-5` |
| `verified` | **Deliberately absent**: nobody has reviewed yet, so the bundle is at the "unverified" tier |
| `status: draft` | every concept; change to `stable` after review |
| `stale_after` | concepts derived from code: expire after 3 months, forcing a re-review |
| `index.md` in each directory (no frontmatter) | every directory |
| `okf_version` in the root `index.md` | `bundle/index.md` |
| `log.md` | `bundle/log.md` |
| Absolute links `/path/file.md` | throughout |
| Custom extension key | `code_ref` (the code version that was read) |

**Not used:** `Attested Computation` (a concept carrying the canonical formula plus a check that confirms the AI ran the formula correctly). Very suitable later for enforcing "tax must be computed with the prescribed formula", but it needs an executor and attester, so it is left for a later phase.

## 5. Using it with an AI

Put the bundle (or the relevant files) into context, then ask, for example:

* **Write TCs**: *"Based on `domain/business-rules/payment-allocation-rules.md`, `testing/step-conventions.md` and `testing/tc-templates/api.md`, write API TCs for every row of the error-code table. Use only the error codes and formulas in the documents."*
* **Lateral testing**: *"I am about to change `PaymentAllocationService`. Based on `regression-map/payment-allocation-change.md`, list the 10 highest-priority regression TCs."*
* **Onboarding**: *"Explain to a newcomer why an invoice that is only partially credited still has `paid_status = UNPAID`, citing the source files."*

## 6. Limits (stated plainly)

* Every concept is an **AI-generated draft from source code, reviewed by no one**. Do not use it as a testing standard before review.
* **The app was never run.** Behaviour is inferred from reading code and tests; anything marked "needs confirmation" has not been verified in practice.
* The **regression map** is based on reading code (call sites, listeners, scopes), not a full dependency analysis. Some rows are marked "not surveyed".
* **No UI**: the UI TC template leaves screen and button names blank.
* The `testing/` part is a **starting proposal** written by AI; the team must agree on it.
* The OKF spec is new (v0.2) and may change.

## 7. Notable findings from the survey (to show the value of writing things down)

These are points a hastily written TC usually misses. All need confirmation in a real run:

1. An invoice that is only **partially credited** (nothing collected) has `paid_status = UNPAID` even though the balance dropped; only an allocation moves it to `PARTIALLY_PAID`.
2. `POST /invoices/{id}/status` with `SENT` sets `status = SENT` unconditionally, which seems to downgrade a `VIEWED` invoice to `SENT`.
3. `retrospective_edits`: the two modes `disable_on_invoice_sent` and `disable_on_invoice_partial_paid` seem to behave identically.
4. `InvoicesController` has no `destroy`, yet the route `DELETE /invoices/{invoice}` is registered.
5. Editing a tax type with `PATCH` while keeping the same name is reported as a duplicate; `PUT` is not.
6. The create-invoice payload requires `total/sub_total/tax` but the server recomputes them; per-line tax amounts sent by the client are still used.

## 8. Checking the bundle

```bash
python3 -I tools/check_bundle.py bundle-en   # or: bundle
```

Checks: every concept has `type`, `index.md` outside the root has no frontmatter, footnotes are defined and match `sources[].id`, internal links are not broken. Install `pyyaml` so the script parses YAML fully. Last run: 35 concepts, 0 errors, and also 0 syntax errors with `js-yaml`. A lesson learned: a `description` containing `: ` must be quoted, otherwise the YAML is invalid.

**List of concepts to re-review:**

```bash
python3 -I tools/check_bundle.py --review-list bundle
```

Prints concepts that (1) have no `verified`, (2) have a commit newer than the last `verified`, (3) are past `stale_after`. Report only, always exits 0. It compares by **date**, not time, because the commit recording a confirmation always lands after `verified.at`. It must run inside a git repo to read commit dates.

## 9. Corrections relative to the earlier file

I wrote `OKF-cho-du-an-QA.md` before reading the original spec. After reading it I updated: the current version is **v0.2** (not v0.1), `timestamp` is replaced by `generated.at`, the source list is `sources` (not `source`), links should be absolute `/path.md`, and `index.md` / `log.md` are reserved names.
