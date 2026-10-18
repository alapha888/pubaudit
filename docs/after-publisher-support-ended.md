# Found .pub files after Publisher support ended? Read this before you delete anything

Microsoft removed Publisher from Microsoft 365 on October 1, 2026, and support for the perpetual version ended October 13, 2026. If you are reading this after those dates, you are in the most common situation of all: the application is gone, and the files are still there — a folder of newsletters, certificates, flyers, or directories from a school, church, club, or small office.

The good news: the files are not lost, and you do not need Publisher to rescue them. The trap is different, and it is quieter.

## The one rule

**Do not delete any original .pub file until its replacement PDF has been verified — not just produced.**

Converters can report success and produce no file at all. They can also produce a PDF whose text did not survive. Both failures look fine in a file listing. Deleting the originals on the strength of a converter's exit code is the one step in this process that cannot be undone.

## A safe order of operations

1. **Inventory first.** Count the .pub files and note where they live (which folders, whose archive, roughly how old). Work on a copy of the folder if the originals are the only copies.
2. **Convert a whole folder at once, locally.** Single-file web converters mean uploading rosters and directories to a third party, one file at a time. A local batch run keeps the files on your own machine.
3. **Classify every file, not just the successes.** A useful report sorts each file into one of three buckets:
   - `OK` — PDF produced, has pages and extractable text.
   - `REVIEW` — PDF produced, but little or no extractable text. Open it and check it visually before deleting the .pub.
   - `FAILED` — no usable PDF: silent failure, corrupted file, or a file that was never really a Publisher file.
4. **Work the REVIEW pile by eye.** Conversion quality is the underlying converter's quality; complex multi-column layouts and very old files can convert imperfectly. REVIEW exists precisely so those files get human eyes instead of a silent pass.
5. **Only then delete** — and only the originals whose PDFs are `OK` or have passed your visual check.

Short on time? The [30-minute rescue checklist](https://gist.github.com/alapha888/5057703ca29367493f688330a7154940) walks the same steps in checklist form.

## Doing it with PubAudit

PubAudit is a free, open-source command-line tool (MIT, Python standard library only) that converts a folder of .pub files locally via LibreOffice and writes a report classifying every file as above:

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/
```

Requirements: Python 3, LibreOffice (`soffice`), and `pdfinfo` + `pdftotext` from poppler-utils.

Repo: https://github.com/alapha888/pubaudit

In a verified test run over seven files (five real Publisher flyers, one plain-text file renamed to `.pub`, one truncated real file), the five real files came back `OK`; both bad files came back `FAILED` — including the truncated one, where the converter had exited with code 0 and produced no PDF at all.

## Not comfortable with a command line?

A Windows desktop edition (pick a folder, get the report, no command line) is in development, indicatively $29 one-time. It is not on sale yet. The free command-line tool above is complete and usable today; the Windows edition exists for the person who inherits one of these archives and has never opened a terminal.

## Limits, stated plainly

- PubAudit verifies that a PDF exists, has pages, and carries text. It cannot prove the layout *looks* right; `REVIEW` files need human eyes.
- Nothing here recovers a file that is already corrupted beyond what the converter can read — those land in `FAILED`, which at least tells you exactly which ones they are while other copies may still exist elsewhere.
