# Clearing the REVIEW pile: the visual check, file by file

A PubAudit report sorts every file into `OK`, `REVIEW`, or `FAILED`. Only one of those piles needs your eyes: `REVIEW`. An `OK` file passed every automated check, and a `FAILED` file produced nothing to look at. A `REVIEW` file produced a real PDF — the converter worked — but the automated checks could not clear it, for one of the two reasons the `note` column names:

- **Little or no extractable text** (fewer than 20 characters). Either the document's words are part of a picture, which is normal for image-heavy flyers, or the conversion lost the text. The PDF looks completely different in those two cases, and only a person opening it can tell which one happened.
- **Page count could not be verified.** A PDF exists, but its page count could not be read, so it cannot be promoted to `OK` on an incomplete check.

This page is the check itself: what to look at, in what order, and what each outcome allows you to do with the original `.pub`.

## One honest constraint before you start

Most people clearing a REVIEW pile no longer have a working copy of Publisher — that is usually why they ran PubAudit at all. So this is not a side-by-side comparison against the original rendering. It is a completeness check on the PDF's own terms: does this document read as whole and usable, or is something visibly missing? When you cannot tell, the answer is to keep the original, not to guess.

## Set up the work list

1. Open `pubaudit-report.csv` in a spreadsheet and filter `status` to `REVIEW`, or open the HTML report and work from its REVIEW rows.
2. Keep a simple list of your own next to it — a text file or a spreadsheet column — with three possible marks per file: **cleared**, **failed**, **unsure**. The report itself is not edited; your list is the record of the visual pass.
3. Open each PDF from the `pdf` column's path inside the output folder (the output mirrors your original folder structure).

## What to check on each PDF, in order

1. **It opens and has pages.** A file that will not open, or opens to nothing, is not cleared — mark it failed. If the report's `pages` column has a number, the PDF should show that many pages.
2. **No blank or half-empty pages.** Flip through every page. A page that should carry content but is blank or stops mid-layout is the most common sign of a conversion that lost material.
3. **The text reads.** Read the headline and the first lines of body text on the first page, and spot-read one later page. You are looking for readable, complete sentences — not garbled characters, not empty boxes where text blocks should be, not text cut off at a page edge.
4. **Pictures and tables are present, not placeholders.** Images should show as images, not empty frames. A table should have its rows and its words, not just its grid lines.
5. **The document ends like a document.** The last page should end the way this kind of document ends — a closing line, contact details, a final row — not stop abruptly mid-sentence or mid-table.
6. **For the low-text case specifically:** if the words are visibly there *as part of a picture* and you can read them in the image, that is the benign case the 20-character floor cannot distinguish from lost text. Cleared means *you read the words in the PDF*, not that the PDF contains extractable text — it does not, and that is fine for reading and printing, though not for search or copy-paste.

## The three outcomes

- **Cleared.** The PDF is whole and readable on the checks above. Mark it cleared. Its original `.pub` can be retired on the same terms as an `OK` file's.
- **Failed.** Something is visibly missing, garbled, or truncated. Mark it failed and treat the file like a `FAILED` row: keep the original `.pub`, and look for another source copy (a backup, an email attachment, a printed copy to re-scan) or a future converter version.
- **Unsure.** You cannot tell whether something is missing — for example a document you do not recognise, in a folder you inherited. Keep the original `.pub`. Unsure is a valid end state, not a problem to force: storage is cheap, and an unrecoverable original is not.

## Finishing the pile

- Retire originals only for `OK` rows and REVIEW rows you marked cleared. Keep the original of every `FAILED` row and every REVIEW row not marked cleared — this is the same rule stated at the top of the HTML report.
- Keep your cleared/failed/unsure list with the report and the PDFs. Months later, that list is the only record of which PDFs passed a human check and which are still provisional.
- A sample spot-check of `OK` PDFs is still worthwhile before retiring their originals; the full reasoning is in [Reading a PubAudit report](reading-the-report.md). `OK` means existence, pages, and extractable text were verified — not that the layout was compared.

## Doing it with PubAudit

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/
```

PubAudit is free and open source (MIT, Python standard library only). It converts locally via LibreOffice and verifies with `pdfinfo` / `pdftotext` from poppler-utils; your files are never uploaded. Repo: https://github.com/alapha888/pubaudit

Working from the report for the first time? [Reading a PubAudit report](reading-the-report.md) explains how each status is decided, and [Working with the CSV report](working-with-the-csv-report.md) covers filtering a large report into this work list.

A Windows desktop edition (pick a folder, get the report, no command line) is on sale for $29 one-time: https://alapha888.gumroad.com/l/lvodxo — the free command-line tool is complete and usable today.
