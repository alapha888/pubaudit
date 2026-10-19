# PubAudit guide index: every guide, by the job you are doing

PubAudit's guides grew one at a time — a page per stage of rescuing an archive of Microsoft Publisher (`.pub`) files after Publisher support ended. This page is the map: which guide to read for which job, in which order, and what each one does not cover. Everything linked here is in this repository.

## Start here

- **You found `.pub` files and have not run anything yet.** Start with [Found .pub files after Publisher support ended?](after-publisher-support-ended.md) — why verification comes before deleting anything, and a safe order of operations. Its one rule governs everything below: do not delete any original `.pub` file until its replacement PDF has been verified, not just produced.
- **You are setting up for the first time.** Go to [Installing PubAudit](install-and-preflight.md) before your first real run.
- **You already have a report.** Go to [Reading a PubAudit report](reading-the-report.md) first, then to the pile you are working: REVIEW, FAILED, or the CSV work list.

## Before the first run

- [Installing PubAudit](install-and-preflight.md) — how to install Python, LibreOffice, and poppler on Ubuntu, Debian, Fedora, and macOS; why a missing `soffice` stops the run loudly (exit 2, no report) while missing poppler degrades the report silently (files that should read `OK` land in `REVIEW`); and a four-command preflight plus a one-file smoke test to run before the whole archive.

## Reading the result

- [Reading a PubAudit report](reading-the-report.md) — how each status (`OK`, `REVIEW`, `FAILED`) is decided, including the 20-character text floor and the two different REVIEW cases; what to do with each pile; and what the report does not prove.
- [Working with the CSV report](working-with-the-csv-report.md) — all seven CSV columns, including the two the HTML report does not show; why a blank `pages` or `text_chars` means "not measured" rather than zero; and how to filter the REVIEW and FAILED piles into a work list in a spreadsheet.

## Working the piles

- [Clearing the REVIEW pile](clearing-the-review-pile.md) — the visual check itself: what to look at on each PDF, in what order, and what each outcome (cleared / failed / unsure) allows you to do with the original `.pub`. It is a completeness check on the PDF's own terms, not a comparison against the original — most people clearing this pile no longer have a working copy of Publisher.
- [Working through the FAILED pile](working-through-the-failed-pile.md) — the reading check: the two FAILED note shapes in the report, why one of them (missing OLE2 header) will never be fixed by re-running and the other sometimes will, what the converter's own words in the note tell you, and why FAILED is the strongest reason in the report to keep the original `.pub`.

## When something looks wrong, or the archive is large

- [Troubleshooting and large archives](troubleshooting-and-large-archives.md) — read the pattern, not the rows: the repeated-note patterns that point at the environment instead of your files (missing converter, missing `pdfinfo`, one file timing out), why re-running after a fix is safe, and how to stage a big archive starting with a pilot subfolder.

## A suggested order for a full archive

1. Read [after Publisher support ended](after-publisher-support-ended.md) and keep its one rule in view.
2. Install and preflight with [Installing PubAudit](install-and-preflight.md); run the one-file smoke test.
3. Run PubAudit on a pilot subfolder first if the archive is large (see [Troubleshooting and large archives](troubleshooting-and-large-archives.md)).
4. Read the report with [Reading a PubAudit report](reading-the-report.md); split the piles with [Working with the CSV report](working-with-the-csv-report.md).
5. Clear REVIEW visually, work FAILED by reading its notes, and only retire an original `.pub` once its PDF has been verified.

## What this index does not do

An index is not a verdict on your files. Each guide states its own limits — PubAudit converts and verifies PDFs, it does not prove a conversion preserved everything that mattered in the original layout — and the keep-original rule in the first guide applies until you have verified a replacement yourself. If a guide and your report disagree, the report from the version you ran is the one to trust, and the mismatch is worth reporting.
