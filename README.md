# PubAudit

Batch-convert Microsoft Publisher (`.pub`) files to PDF — and **verify every single output**.

Microsoft removed Publisher from Microsoft 365 on **October 1, 2026**, and support for the perpetual version ended **October 13, 2026**. Free single-file converters exist (LibreOffice, FreeConvert, Zamzar), and they are fine for a handful of files. They do not answer the question that matters when you have a folder — or twenty years — of files:

**Which of my files actually converted, and which ones silently didn't?**

Converters can report success and produce no file at all. They can also produce a PDF whose text did not survive. PubAudit converts a whole folder locally and writes a report that classifies every file:

| Status | Meaning |
|---|---|
| `OK` | PDF produced, has pages and extractable text |
| `REVIEW` | PDF produced, but little/no extractable text — check it visually before deleting the `.pub` |
| `FAILED` | No usable PDF (silent failure, corrupted file, or not a real Publisher file) |

Everything runs on your own machine. Your files are never uploaded anywhere — relevant if the archive belongs to a school, church, club, or small office.

Working through an archive now that support has ended? Start with the [30-minute rescue checklist](https://gist.github.com/alapha888/5057703ca29367493f688330a7154940) — inventory, convert, and verify, step by step.

Found the files after support already ended? Start with [Found .pub files after Publisher support ended?](docs/after-publisher-support-ended.md) — why verification comes before deleting anything, and a safe order of operations.

Already ran it? [Reading a PubAudit report](docs/reading-the-report.md) explains how each status is decided (including the 20-character text floor and the two different REVIEW cases), what to do with each pile, and what the report does not prove.

Report looks wrong, or the archive is large? [Troubleshooting and large archives](docs/troubleshooting-and-large-archives.md) covers the patterns that point at the environment instead of your files (missing converter, missing `pdfinfo`, one file timing out), why re-running after a fix is safe, and how to stage a big archive starting with a pilot subfolder.

Setting up for the first time? [Installing PubAudit](docs/install-and-preflight.md) covers how to install Python, LibreOffice, and poppler on Ubuntu, Debian, Fedora, and macOS, why a missing `soffice` stops the run loudly while missing poppler degrades the report silently, and a four-command preflight plus a one-file smoke test to run before the whole archive.

Working a large archive in a spreadsheet? [Working with the CSV report](docs/working-with-the-csv-report.md) documents all seven CSV columns (including the two the HTML report does not show), why blank `pages`/`text_chars` means "not measured" rather than zero, and how to filter the REVIEW and FAILED piles into a work list.

Left with a pile of REVIEW files? [Clearing the REVIEW pile](docs/clearing-the-review-pile.md) is the visual check itself — what to look at on each PDF, in what order, why it is a completeness check rather than a comparison against the original, and what each outcome (cleared / failed / unsure) allows you to do with the original `.pub`.

Left with a pile of FAILED files? [Working through the FAILED pile](docs/working-through-the-failed-pile.md) is the reading check — the two FAILED note shapes in the report, why one of them will never be fixed by re-running and the other sometimes will, what the converter's own words in the note tell you, and why FAILED is the strongest reason in the report to keep the original `.pub`.

Want to see a report before you have one of your own? [A worked example: four files, one run, end to end](docs/worked-example-four-files.md) walks a real four-file run whose verdicts were pinned in advance — two image-heavy flyers landing in `REVIEW`, and both `FAILED` shapes (a renamed text file, and a truncated file the converter exited 0 on while producing no PDF) — with the actual report rows in view.

Looking for a specific guide? The [guide index](docs/guide-index.md) maps every guide in this repository — setup, reading the report, working the REVIEW and FAILED piles, and troubleshooting — to the job it is for, with a suggested order for a full archive.

## Requirements

- Python 3 (standard library only)
- LibreOffice (`soffice`) — provides the `.pub` reader (libmspub)
- `pdfinfo` + `pdftotext` (poppler-utils) — used to verify outputs

## Usage

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/
```

The scan is recursive and preserves the folder structure in the output.

## Verified behaviour (2026-10-10 test run)

Seven test files (five real Publisher flyers, one plain-text file renamed to `.pub`, one truncated real file):

- 5 real files → `OK`, each verified with page count and extracted text
- Renamed text file → `FAILED` (missing OLE2 header; without this check, LibreOffice "converts" it as a text document and the audit would lie to you)
- Truncated file → `FAILED` — LibreOffice exited with code 0 and produced **no PDF**; PubAudit catches this because it checks the output exists, not the exit code

## Limits, stated plainly

- Conversion quality is LibreOffice/libmspub quality. Complex multi-column layouts and very old (Publisher 98-era) tables are known to convert imperfectly — that is exactly why `REVIEW` exists.
- PubAudit verifies that a PDF exists, has pages, and carries text. It cannot prove the layout *looks* right; `REVIEW` files need human eyes.
- This is a command-line tool for people comfortable running one command.

## Windows edition (on sale)

A Windows desktop version for non-technical users (select a folder, get the report, no command line) is on sale for **$29 one-time**: https://alapha888.gumroad.com/l/lvodxo — its conversion engine passed end-to-end verification on real Windows CI on **2026-10-16**: real LibreOffice, real `.pub` samples, and the Windows engine and this CLI agreed on every file's verdict. The installer is unsigned in v1 (SmartScreen warns on first run); its SHA-256 is published on the product page. What is still unverified: the GUI window itself has not yet run interactively, so visual rendering remains untested.

## More from the same author

- Full index of free tools, paid tiers, and waitlists: https://gist.github.com/alapha888/fe51434e80dbc0ef5610aeab38b025f4

## License

MIT
