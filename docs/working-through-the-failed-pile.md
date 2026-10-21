# Working through the FAILED pile: read the note first, then decide

A PubAudit report sorts every file into `OK`, `REVIEW`, or `FAILED`. The REVIEW pile needs your eyes (there is a separate guide for that check). The FAILED pile needs something different: reading, not looking. A FAILED file produced no usable PDF at all, so there is nothing to inspect visually — but the `note` column tells you which of the only two failure shapes you are dealing with, and the two shapes have almost opposite answers to the obvious question: *will re-running help?*

## The two FAILED notes, exactly as the report writes them

**1. "Not a real Publisher file (missing OLE2 header) — it may be corrupted or simply renamed from another format."**

PubAudit checks the file's first eight bytes before the converter ever sees it. Real Publisher files are OLE2 compound documents and start with a specific magic number; a file without it never reaches LibreOffice at all. That check exists because without it, LibreOffice will happily "convert" a plain text file that someone renamed to `.pub` — as a text document — and the audit would report a false OK.

For this shape, re-running PubAudit will not help: the same bytes will fail the same check every time. What can still be true, and worth a few minutes:

- **It is a different file wearing a `.pub` name.** A document that was renamed, exported wrongly, or saved by another program into the wrong extension. If you can identify what it actually is — an old Word document, a text file, an image — open it as that, and it was never a Publisher file to rescue in the first place.
- **It is a damaged copy of a real file.** Truncation in a copy, a bad download, a failing disk. The `size_bytes` column in the CSV report is a clue, not a proof: a file far smaller than its neighbours from the same era is worth suspecting. The fix is not a different converter — it is a better copy: the original machine, a backup, an email attachment, a duplicate in another folder.

**2. "No PDF produced (silent failure or unreadable file). Converter said: …"**

This file passed the OLE2 check — it looks like a real Publisher file — the converter ran, and no PDF came out. The note appends what the converter reported, cut off at 200 characters, and that tail is the part to read:

- **`TIMEOUT after 300s`** — the converter was still working when PubAudit's five-minute per-file limit stopped it. Very large or complex files can land here. Re-running that one file on its own, in its own folder, is the fair test; [Troubleshooting and large archives](troubleshooting-and-large-archives.md) covers the isolation method. A file that times out alone, repeatedly, belongs with the unrecoverable-for-now group below.
- **`could not launch converter: …`** — the failure is in the environment, not the file. Expect neighbours in the same run to show it too. Fix the setup first ([Installing PubAudit](install-and-preflight.md) has the checks), then re-run — re-running is safe, and the paragraph below explains why.
- **`rc=… no PDF produced.` followed by converter output** — the converter ran to completion and produced nothing. The return code can even be 0: in PubAudit's own verification run, a truncated real file made LibreOffice exit with code 0 and no PDF at all. That is why the report trusts the output file's existence, not the exit code. Re-running the same converter version on the same file will almost always repeat this; a different or future version of LibreOffice/libmspub is a legitimate later retry, not a same-day one.

## Why re-running after a fix is safe

PubAudit deletes the expected PDF from the output folder before each conversion, so a stale PDF from an earlier run can never pose as this run's success. The output folder is also excluded from its own scan. If you fixed the environment, found a better copy of a file, or upgraded the converter, re-running the same folder gives you a fresh verdict on every file — the new report replaces the old one, so keep the old report if the comparison matters to you.

## The honest end states

- **Recovered.** A better copy, a fixed environment, or an isolated re-run turns the row OK or REVIEW on the next report. The new report is the record.
- **Not a Publisher file.** The OLE2 shape, resolved: the file is something else, to be kept or converted as what it actually is.
- **Unrecoverable for now.** Keep the original `.pub`. This is a valid end state, not a forced one: the HTML report's own header says to keep the originals until every REVIEW and FAILED row has been dealt with, and a file nobody can convert today may still be readable by a future converter version. Storage is cheap; an original deleted on the strength of a FAILED row is gone.

Do not delete a `.pub` because its row says FAILED. FAILED is the report saying *no verified copy exists* — it is the strongest reason in the whole report to keep the original.

## Doing it with PubAudit

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/
```

PubAudit is free and open source (MIT, Python standard library only). It converts locally via LibreOffice and verifies with `pdfinfo` / `pdftotext` from poppler-utils; your files are never uploaded. Repo: https://github.com/alapha888/pubaudit

Reading the report for the first time? [Reading a PubAudit report](reading-the-report.md) explains how each status is decided. Working a large FAILED pile out of the CSV? [Working with the CSV report](working-with-the-csv-report.md) covers filtering by the note's opening words.

A Windows desktop edition (pick a folder, get the report, no command line) is on sale for $29 one-time: https://alapha888.gumroad.com/l/lvodxo — the free command-line tool is complete and usable today.
