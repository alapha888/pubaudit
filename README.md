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

## Windows edition (engine verified, coming soon)

A Windows desktop version for non-technical users (pick a folder, get the report, no command line), indicatively **$29 one-time**, is not on sale yet. Its conversion engine passed end-to-end verification on real Windows CI on **2026-10-16**: real LibreOffice, real `.pub` samples, and the Windows engine and this CLI agreed on every file's verdict. The installer is built (its SHA-256 will be published with the listing at launch). What is still unverified: the GUI window itself has not yet run interactively, so drag-and-drop and visual rendering remain untested. [Register interest by email](mailto:alapha888@gmail.com?subject=%5BPubAudit%20Waitlist%5D&body=I%20am%20interested%20in%20a%20Windows%20version%20of%20PubAudit.%0AHow%20many%20.pub%20files%20I%20need%20to%20convert%20(roughly)%3A%0AWhere%20the%20files%20live%20(school%20%2F%20church%20%2F%20office%20%2F%20personal)%3A%0AWhat%20I%20have%20tried%20so%20far%3A) to be notified when it ships, and say roughly how many `.pub` files you need to rescue.

## More from the same author

- Full index of free tools, paid tiers, and waitlists: https://gist.github.com/alapha888/fe51434e80dbc0ef5610aeab38b025f4

## License

MIT
