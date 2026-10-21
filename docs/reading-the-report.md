# Reading a PubAudit report: what OK, REVIEW, and FAILED actually mean

A PubAudit run leaves two files in the output folder: `pubaudit-report.csv` and `pubaudit-report.html`. They hold the same rows. The HTML version opens in any browser and starts with the counts; the CSV version opens in a spreadsheet, where you can sort and filter by status. This page explains how each status is decided, what to do with each pile, and what the report does not prove.

## The columns

| Column | What it is |
|---|---|
| `file` | The `.pub` file, as a path relative to the folder you scanned. The scan is recursive, so subfolders appear here. |
| `size_bytes` | Size of the original `.pub` file. |
| `status` | `OK`, `REVIEW`, or `FAILED` — see below. |
| `pages` | Page count of the produced PDF, read with `pdfinfo`. Blank when no PDF was produced or the count could not be read. |
| `text_chars` | Number of characters of extractable text in the PDF, read with `pdftotext`. Blank on the same conditions as `pages`. |
| `pdf` | Where the produced PDF landed inside the output folder, which mirrors your original folder structure. Blank when there is no PDF. |
| `note` | A plain-language reason for the status, including the converter's own message (truncated) when conversion produced nothing. |

## OK — verified, within stated limits

A file is `OK` only when all three checks pass:

- a PDF file exists in the output folder and is larger than zero bytes;
- it has at least 1 page;
- it carries at least 20 characters of extractable text.

The 20-character line is a floor, not a quality grade: it separates "the text survived" from "the PDF is essentially pictures or empty." An `OK` row means the conversion produced a real, readable document. It does not prove the layout looks right — no automated check in PubAudit compares appearance. If the archive matters, spot-check a sample of `OK` files visually before you retire the originals.

One detail that protects this status: before converting, PubAudit deletes any stale PDF with the same name left in the output folder by an earlier run. An old success can never pose as this run's success.

## REVIEW — a PDF exists; a person needs to look

`REVIEW` means a PDF was produced but verification could not fully clear it. There are two distinct cases, and the `note` column tells you which one you have:

- **Little or no extractable text.** The PDF has pages, but fewer than 20 characters of text could be extracted. That is normal for an image-heavy flyer whose words are part of a picture — and it is also what a conversion that lost its text looks like. Only opening the PDF distinguishes the two.
- **Page count could not be verified.** A PDF exists, but its page count could not be read, so it cannot be promoted to `OK` on an incomplete check.

Work the `REVIEW` pile by eye: open each PDF, compare it with what the document should be, and only then decide about the original `.pub`. Until a `REVIEW` row has passed that visual check, keep the original.

## FAILED — no usable PDF

`FAILED` means there is nothing safe to keep from this file in this run. The `note` column distinguishes the causes:

- **Not a real Publisher file.** Real `.pub` files are OLE2 compound documents and start with a specific 8-byte header. A file without it — for example a text file renamed to `.pub`, or a corrupted download — is failed before conversion is even attempted. Without this check, the converter would happily "convert" a renamed text file as a text document and the row would read as a false success.
- **No PDF produced.** The converter ran (it may even have exited with code 0) and no PDF appeared, or the one that appeared was empty. This silent-failure case is the main reason PubAudit checks that the output exists instead of trusting the exit code. A truncated or unreadable `.pub` typically lands here.
- **Converter timeout or launch failure.** A single file gets up to 300 seconds; a file that exceeds that, or a converter that could not start at all, is recorded rather than hanging the whole batch.

A `FAILED` row is not proof the document is gone forever. It is a precise list of what to hunt for elsewhere: another copy, an email attachment, a backup. Keep the original `.pub` for every `FAILED` row — a future converter version may read what this one could not.

## A workable order for a large report

1. Read the counts line first (`N .pub file(s): X OK, Y to review, Z failed`). That is the size of the remaining work.
2. Filter the CSV to `FAILED` and read the notes. Note which files need another source copy.
3. Filter to `REVIEW` and open each PDF. This is the only pile that strictly needs your eyes.
4. Spot-check a sample of `OK` PDFs, then retire originals only for rows that are `OK` or visually cleared — the HTML report states the same rule at the top: keep the original `.pub` files until every `REVIEW` and `FAILED` row has been dealt with.

## What the report does not prove

- It does not prove layout fidelity. Verification covers existence, pages, and extractable text — not fonts, columns, or image placement.
- It does not recover corrupted files. It identifies them exactly, which is the step that has to come before recovery.
- A re-run is safe: the output folder is excluded from its own scan, and stale PDFs are removed before conversion, so counts from a second run describe the second run.

## Doing it with PubAudit

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/
```

PubAudit is free and open source (MIT, Python standard library only). It converts locally via LibreOffice and verifies with `pdfinfo` / `pdftotext` from poppler-utils; your files are never uploaded. Repo: https://github.com/alapha888/pubaudit

New to the situation? [Found .pub files after Publisher support ended?](after-publisher-support-ended.md) gives the safe order of operations before you run anything, and the [30-minute rescue checklist](https://gist.github.com/alapha888/5057703ca29367493f688330a7154940) walks the whole rescue in checklist form.

A Windows desktop edition (pick a folder, get the report, no command line) is on sale for $29 one-time: https://alapha888.gumroad.com/l/lvodxo — the free command-line tool is complete and usable today.
