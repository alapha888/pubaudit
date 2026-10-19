# A worked example: four files, one run, end to end

The other guides in this repository are procedural — how to install, how to read a report, how to work each pile. This page is the opposite: one real run, on a small set of files whose expected verdicts were written down before the run, with the actual report left in view. It is the run to read if you want to see what `REVIEW` and `FAILED` look like when they are the *correct* answers, not errors.

The run took place on October 19, 2026, with this repository's `pubaudit.py` and LibreOffice 24.2.7.2, on copies of the files in a scratch folder. The originals were not modified — PubAudit never writes to its inputs — and nothing in this example deletes anything.

## The four files

These are the smoke-test fixtures of the Windows edition of PubAudit, kept in that project's test corpus with their provenance and expected verdicts pinned in advance:

| File | Size (bytes) | What it actually is |
|---|---:|---|
| `MSPublisher2013-Sample.pub` | 98,304 | A real Publisher 2013 file (from the PRONOM research corpus). Image-heavy. |
| `fdo59355-1.pub` | 10,752 | A real Publisher file from LibreOffice's own libmspub test corpus. |
| `corrupt-ole.pub` | 2,048 | Derived locally: the first 2,048 bytes of `fdo59355-1.pub` — a valid OLE2 header with a truncated body. |
| `fake-renamed.pub` | 48 | One line of plain text saved with a `.pub` name. No OLE2 header. |

The verdicts pinned for this set before any run are: `REVIEW`, `REVIEW`, `FAILED`, `FAILED`. The set is deliberately built to contain no easy `OK` — its job is to exercise the two piles people find confusing.

## The run and the report it wrote

```bash
python3 pubaudit.py /path/to/folder
# Done: 0 OK, 2 REVIEW, 2 FAILED
```

The CSV report, row for row:

| File | Status | Pages | Text chars | Note (shortened) |
|---|---|---:|---:|---|
| `MSPublisher2013-Sample.pub` | `REVIEW` | 1 | 7 | PDF produced but little/no extractable text — check it visually before deleting the `.pub`. |
| `fdo59355-1.pub` | `REVIEW` | 2 | 16 | PDF produced but little/no extractable text — check it visually before deleting the `.pub`. |
| `corrupt-ole.pub` | `FAILED` | — | — | No PDF produced. Converter said: rc=0, no PDF produced; "source file could not be loaded". |
| `fake-renamed.pub` | `FAILED` | — | — | Not a real Publisher file (missing OLE2 header). |

All four verdicts match the pinned expectations. The page counts also match what the fixture documentation says these files convert to (one page and two pages respectively) — a small cross-check that the PDFs are the right documents, not just *some* output.

## Reading the four rows

**The two `REVIEW` rows are successes with homework attached.** Both real files converted: a PDF exists for each, with the expected page count. They land in `REVIEW` rather than `OK` for one stated reason — the extractable text (7 and 16 characters) is under PubAudit's 20-character floor for a clean `OK`. That is what image-heavy flyers look like to a text check: the content is in the pictures, not in a text layer. `REVIEW` here is not a suspicion that conversion failed; it is the report declining to verify what it cannot read. The next step is the visual check in [Clearing the REVIEW pile](clearing-the-review-pile.md), and both originals stay exactly where they are until someone has done it.

**`fake-renamed.pub` is the first `FAILED` shape.** At 48 bytes of plain text, it fails the eight-byte OLE2 header check before the converter ever sees it — the note says so in those words. Re-running will never change this row. The file is not a damaged Publisher file; it is a text file wearing the wrong name, to be kept or discarded as what it actually is.

**`corrupt-ole.pub` is the second `FAILED` shape, and the instructive one.** It passes the header check (its first 2,048 bytes are a genuine Publisher file's), the converter runs — and exits with code 0 while producing no PDF at all. A tool that trusted the exit code would report this file as converted. The row is `FAILED` because PubAudit checks that the output file exists, not what the converter claimed. The note also carries the converter's own tail, cut at 200 characters: alongside the load error there is an unrelated Java warning from LibreOffice's startup. That noise is normal in these tails; the words that matter are "source file could not be loaded". [Working through the FAILED pile](working-through-the-failed-pile.md) covers what each tail means and when a re-run is a fair test.

## Where the run ends

- Nothing was deleted, and nothing in this report licenses a deletion yet. The two `REVIEW` originals wait for eyes; the two `FAILED` originals are kept — for the renamed text file because it was never a Publisher file, for the truncated file because a better copy or a future converter is its only remaining route, and "unrecoverable for now" is a legitimate end state.
- The same four verdicts are what the Windows edition's engine is pinned to produce on this set. Two independent implementations agreeing on the awkward files — not just the easy ones — is the consistency this fixture set exists to check.

## What this example does not show

No `OK` row (the fixture set excludes one on purpose; the repository README records a separate seven-file verification run in which five real flyers all came out `OK`). No timeout, no missing-converter environment failure, and no large archive — [Troubleshooting and large archives](troubleshooting-and-large-archives.md) covers those patterns. And a four-file run proves nothing about your archive: it shows what the two non-`OK` verdicts look like when each is earned, so the first real report you read has a reference point.

## Doing it with PubAudit

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/
```

Start with [Installing PubAudit](install-and-preflight.md) if this is your first run, and keep the one rule from [Found .pub files after Publisher support ended?](after-publisher-support-ended.md) in view throughout: do not delete any original `.pub` until its replacement PDF has been verified, not just produced.
