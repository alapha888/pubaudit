# When the report looks wrong: troubleshooting a PubAudit run, and handling a large archive

Most PubAudit runs need no troubleshooting: you run it, you get a report, and [Reading a PubAudit report](reading-the-report.md) explains the three statuses. This page is for the two situations that page does not cover — a report whose pattern looks wrong (nearly everything failed, or nearly everything needs review), and an archive large enough that "just run it on the folder" needs a plan.

## First: read the pattern, not the rows

A single odd row is a file problem. The *same* note repeated across many rows is usually an environment problem — something about the machine or the setup, not about your documents. Check for these patterns before you conclude anything about the files:

| Pattern in the report | What it most likely means | What to do |
|---|---|---|
| No report at all; the run stops with `LibreOffice (soffice) not found on PATH` | LibreOffice is not installed, or not on the PATH. PubAudit checks this before scanning and exits, so no files were converted or judged. | Install LibreOffice, confirm `soffice` runs, and run again. Nothing about your files has been decided yet. |
| Many `FAILED` rows whose note says `could not launch converter` | The converter was found but could not be started for those files — a local setup problem, not evidence that the files are corrupt. | Check that LibreOffice starts normally on that machine (disk space, a working user profile, no other `soffice` process locking things up), fix the cause, and re-run. Re-running is safe — see below. |
| Many `REVIEW` rows with blank `pages` and the note `page count could not be verified` | A PDF was produced, but the page-count check could not be read. The usual cause is `pdfinfo` (from poppler-utils) missing or failing — the PDFs themselves may be fine. | Install poppler-utils, confirm `pdfinfo` works on one of the produced PDFs, and re-run so the report reflects a complete check. Do not work through a large REVIEW pile by eye until this pattern is ruled out. |
| Many `REVIEW` rows with the note `little/no extractable text` | Either the documents really are image-heavy (scanned flyers, words baked into pictures), or text did not survive conversion. The report cannot distinguish these — only opening a PDF can. | Open two or three of the PDFs. If they look right, the rest of the pile is probably the same kind of document; if the text is visibly missing or garbled, keep every original and treat the pile as unverified. |
| One `FAILED` row whose note says `TIMEOUT after 300s` | That one file took longer than the per-file limit of 300 seconds. Very large or complex files can do this without being corrupt. | Copy that single file into a folder of its own and run PubAudit on just that folder, when the machine is otherwise idle. Whatever the outcome, keep the original. |
| A `FAILED` row with `missing OLE2 header` | That file is not a real Publisher file — it is corrupted, truncated, or was renamed from another format. Re-running will not change this row. | Hunt for another copy (email attachment, backup, another machine). Keep the file itself; a future tool may read what this one could not. |

The general rule: **a pattern is fixed in the environment and then re-run; a single row is investigated as a file.** Judging a whole archive corrupt because of a pattern is the expensive mistake — and so is deleting originals on the strength of a report produced while the environment was broken.

## Handling a large archive

PubAudit scans the folder you give it recursively and converts files one at a time, printing progress as `[i/N]` as it goes. That makes a large archive manageable if you stage it:

1. **Pilot one subfolder first.** Point PubAudit at a single subfolder — a year, a department, one person's folder — before the whole archive. The pilot tells you the real conversion speed on your machine, the OK / REVIEW / FAILED mix to expect, and whether any pattern from the table above is present, while the cost of a wrong setup is still small.
2. **Work on a copy when the originals are the only copy.** The scan does not modify your `.pub` files, but a pilot phase is exactly when you are still changing settings and re-running. A copy makes every early mistake reversible.
3. **Put the output somewhere deliberate.** By default, PDFs and reports land in a `pubaudit-output` folder inside the folder you scanned. With `--out` you can send them elsewhere instead — for example when the archive sits on a nearly full disk or on read-only media:

   ```bash
   python3 pubaudit.py /path/to/archive --out /path/to/output
   ```

4. **Budget time from the pilot, not from a guess.** Files convert sequentially, and a single difficult file can take up to the 300-second limit. Multiply your pilot's average per-file time by the full count for a realistic estimate, and let a large run proceed undisturbed rather than starting it when the machine is needed for something else.
5. **Work the result from the CSV.** Sort or filter by `status` to build your work piles, and by `size_bytes` to spot the very large files most likely to need individual attention. [Reading a PubAudit report](reading-the-report.md) gives the workable order for the piles themselves.

## Why re-running is safe

Fixing the environment and running again does not corrupt the results:

- Before converting each file, PubAudit deletes any stale PDF of the same name left in the output folder by an earlier run, so an old success can never pose as this run's success.
- The output folder is excluded from its own scan, so a second run does not re-audit its own PDFs.
- Each run writes a fresh report describing that run only.

So when a pattern points at the environment, the correct sequence is: fix the cause, re-run the same folder, and judge the files only from the new report.

## Doing it with PubAudit

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/ (or in the folder given with --out)
```

PubAudit is free and open source (MIT, Python standard library only). It converts locally via LibreOffice and verifies with `pdfinfo` / `pdftotext` from poppler-utils; your files are never uploaded. Repo: https://github.com/alapha888/pubaudit

Just found the files? [Found .pub files after Publisher support ended?](after-publisher-support-ended.md) gives the safe order of operations before you run anything.

A Windows desktop edition (pick a folder, get the report, no command line) is on sale for $29 one-time: https://alapha888.gumroad.com/l/lvodxo — the free command-line tool is complete and usable today.
