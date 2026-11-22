# Exploring OKF (Open Knowledge Format) as a knowledge base for a QA project

[🇻🇳 Tiếng Việt](README.md) · 🇬🇧 English

This repo collects notes and a sample bundle for applying **Open Knowledge Format v0.2** (Google Cloud) to a SaaS project about voucher (denpyo) registration and tax settlement.

## Contents

```
.
├── README.md / README.en.md       # this file (Vietnamese / English)
└── okf-sample-invoiceshelf/       # sample bundle built from the open-source InvoiceShelf project
    ├── HUONG-DAN.md               # guide: how to read the bundle, mapping to a real project, limits (Vietnamese)
    ├── GUIDE.en.md                # English version of HUONG-DAN.md
    ├── tools/check_bundle.py      # checks conformance, links, footnotes
    ├── bundle/                    # the Knowledge Bundle (35 concepts, Vietnamese, the original)
    └── bundle-en/                 # English translation of the bundle (same structure)
```

## Suggested reading order

1. `okf-sample-invoiceshelf/GUIDE.en.md`: how the sample bundle was made and how to map it to your own project.
2. `okf-sample-invoiceshelf/bundle-en/index.md`, then `domain/business-rules/balance-recalculation.md`, `testing/good-vs-bad-tc.md`, `regression-map/payment-allocation-change.md`.

## OKF in brief

- It is a **format**, not a tool: a directory of Markdown files with YAML frontmatter. The only required field is `type`.
- v0.2 adds provenance and trust fields: `sources`, `generated`, `verified`, `status`, `stale_after`.
- `index.md` and `log.md` are reserved names. Links should be absolute `/path/file.md` (from the bundle root).
- OKF does **not** define search or serving. An agent can read the directory directly, or you can build RAG/MCP on top.
- Whatever the AI reads costs tokens. Use `index.md` so the AI reads layer by layer instead of loading the whole bundle.

## Several modules in one business flow

The spec defines no links between bundles. For three consecutive modules (registration → approval → tax settlement), use **one bundle with one subdirectory per module**:

```
denpyo-knowledge/
├── index.md
├── shared/            # glossary, data, workflows/denpyo-end-to-end.md
├── registration/
├── approval/
├── tax-settlement/
├── testing/
└── regression-map/
```

For the AI to trace the whole flow, write down: an end-to-end flow concept, handoff tables between modules, bidirectional links with context, and a shared glossary/data. A missing link breaks the chain, so the bundle needs a maintenance process.

## Checking the sample bundle

```bash
cd okf-sample-invoiceshelf
python3 -I tools/check_bundle.py bundle      # Vietnamese
python3 -I tools/check_bundle.py bundle-en   # English
```

Last run: 35 concepts each, 0 errors. Install `pyyaml` for full YAML parsing.

## Notes

- English is available for the README, the guide (`GUIDE.en.md`) and the bundle (`bundle-en/`). **The original is `bundle/` (Vietnamese)**; when content changes, edit the original first, then update `bundle-en/`. There is no tool that keeps the two in sync.
- The sample bundle is an **AI-generated draft from source code, reviewed by no one** (`status: draft`, no `verified`), and the app was never run. It is **not** your project's knowledge.
- Do not put customer source code, DB or specs into external AI tools without checking company policy. Do not put real data into a bundle.

## Next steps

- Scaffold a bundle for the real project (denpyo): you need the denpyo statuses across the three modules, 1–2 key handoff conditions, one confusing AI-written test case and one good one.
- If you lack that information, leave `<...>` placeholders and fill them in later.
