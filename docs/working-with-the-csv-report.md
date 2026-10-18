# Working with the PubAudit CSV report

Every run writes two reports into the output folder: `pubaudit-report.html` and `pubaudit-report.csv`. They carry the same rows, but they are built for different jobs. The HTML file is for reading top to bottom in a browser. The CSV file is for sorting, filtering, and splitting a large archive into piles you can work through — that is what this page covers.

For what OK / REVIEW / FAILED mean and how each status is decided, see [Reading a PubAudit report](reading-the-report.md). This page is only about using the CSV once you have it.

## The seven columns

| Column | What it holds |
| --- | --- |
| `file` | The `.pub` file's path, relative to the folder you scanned. Subfolders are preserved, so `newsletters/2023/spring.pub` stays recognisable. |
| `size_bytes` | The original `.pub` file's size in bytes. |
| `status` | `OK`, `REVIEW`, or `FAILED`. |
| `pages` | Page count of the produced PDF. Blank when the page count could not be verified (see below). |
| `text_chars` | Number of extractable text characters in the PDF. Blank when the text could not be measured (see below). |
| `pdf` | The produced PDF's path, relative to the output folder. Blank on `FAILED` rows — no PDF exists. |
| `note` | A plain-language reason for the row's status, written by the audit itself. |

The HTML report shows only five of these (File, Status, Pages, Text chars, Note). `size_bytes` and the `pdf` path exist only in the CSV — one more reason to keep the CSV, not just the HTML.

## Blank does not mean zero

`pages` and `text_chars` are left blank when the measurement tools were unavailable, not when the answer was zero. A row with blank `pages` and a note saying the page count could not be verified is a different situation from a row with `pages` filled in and `text_chars` under the 20-character floor — the first means "not measured", the second means "measured, and the text is not there". Filtering on blanks in a spreadsheet is how you separate the two REVIEW cases without opening every PDF.

## Four things to do with the CSV

Open it in Excel, LibreOffice Calc, or Google Sheets, turn on filters, and:

1. **Filter `status` = REVIEW, then split by the note.** Rows whose note says "little/no extractable text" need your eyes on the PDF. Rows whose note says the page count could not be verified usually point at a missing measurement tool instead — see [Troubleshooting](troubleshooting-and-large-archives.md) before re-checking files by hand.
2. **Filter `status` = FAILED and read the `note` column as a work list.** Notes starting "Not a real Publisher file (missing OLE2 header)" mark corrupted or renamed files, where re-running will not help. Notes starting "No PDF produced" quote the converter's own message in the note (truncated at 200 characters) as your starting point. Filter on the opening words, not the full sentence — the notes continue past the part quoted here.
3. **Sort by `size_bytes`, largest first.** On a big inherited archive this finds the handful of very large originals — often the image-heavy files most likely to land in REVIEW — so you can check those first instead of working alphabetically.
4. **Keep the CSV next to the output folder as the run's record.** It is the only artefact that ties each original (column `file`) to its PDF (column `pdf`) and its verdict in one place. If you re-run into the same output folder, the reports are rewritten — save a copy of the CSV first if you want to compare runs.

## Limits, stated plainly

- The CSV records what the audit measured: PDF existence, page count, extractable text. It does not record whether a layout *looks* right — no column can tell you that; REVIEW rows still need a visual check before you delete an original.
- Paths are relative, not absolute. If you move the CSV away from the reports and PDFs it describes, resolve `file` against the scanned folder and `pdf` against the output folder yourself.
- The file is written as UTF-8. If a spreadsheet shows mangled characters in non-English file names, import it explicitly as UTF-8 rather than double-clicking it open.
