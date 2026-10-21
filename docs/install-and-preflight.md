# Installing PubAudit: get the three dependencies working before your first run

PubAudit itself is one Python file with no packages to install. What takes a few minutes is the three external tools it relies on — and they do not fail in the same way, which is why a two-minute preflight is worth doing before you point the tool at a real archive.

## Why preflight matters: the three tools fail differently

| Tool | What PubAudit uses it for | What happens if it is missing |
|---|---|---|
| Python 3 | Runs `pubaudit.py`. Standard library only; there is nothing to `pip install`. | The tool does not start at all. |
| LibreOffice (`soffice`) | Converts each `.pub` file to PDF, using its Publisher reader. | Hard stop. PubAudit checks for `soffice` before scanning and exits 2 with `LibreOffice (soffice) not found on PATH`, without converting or judging any file. No report is produced — and nothing about your files has been decided. |
| `pdfinfo` and `pdftotext` (poppler-utils) | Verify each produced PDF: page count and extractable text. | No error, and this is the quiet one. Conversion still runs, but verification cannot complete, so files that should read `OK` land in `REVIEW` instead. A first run where nearly everything says `REVIEW` with blank page counts is usually this, not bad files — see [Troubleshooting and large archives](troubleshooting-and-large-archives.md). |

So: `soffice` missing stops you loudly; poppler missing degrades the report silently. The preflight below catches both before they cost you a run.

## Install

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 libreoffice poppler-utils
```

### Fedora

```bash
sudo dnf install python3 libreoffice poppler-utils
```

### macOS

With [Homebrew](https://brew.sh):

```bash
brew install --cask libreoffice
brew install poppler
```

Python 3 is available as `python3` on current macOS versions; if it is not, `brew install python` provides it.

One macOS note: if you installed LibreOffice by downloading the `.dmg` instead of using Homebrew, the program is present but `soffice` is usually not on your `PATH` — PubAudit will report it as not found even though LibreOffice opens fine. Either install via Homebrew, or add the bundled binary to your `PATH` for the session:

```bash
export PATH="/Applications/LibreOffice.app/Contents/MacOS:$PATH"
```

### Windows

Use the Windows desktop edition (on sale — see below), or run this command-line tool inside WSL (Windows Subsystem for Linux) and follow the Ubuntu steps above inside the WSL shell. Running the script natively in a Windows terminal is not the tested path.

## Preflight: four commands, thirty seconds

Run each of these and confirm you get a version back instead of “command not found”:

```bash
python3 --version
soffice --version
pdfinfo -v
pdftotext -v
```

`pdfinfo -v` and `pdftotext -v` print their version to standard error on some builds — the version line appearing at all is the pass signal. If any one of the four is missing, install that piece and check again before the first real run.

## Smoke test: one file before the whole archive

Do not make the full archive your first run. Copy a single `.pub` file — ideally one you can open and recognise — into a new, empty folder and run:

```bash
python3 pubaudit.py /path/to/smoke-test-folder
```

A healthy setup produces a `pubaudit-output` folder containing the PDF plus `pubaudit-report.csv` and `pubaudit-report.html`, and that one file reads `OK` (or `REVIEW` with a note you understand, for example an image-heavy flyer with little extractable text — see [Reading a PubAudit report](reading-the-report.md)). If the smoke test stops on `LibreOffice (soffice) not found on PATH` (exit 2), or the single known-good file comes back `REVIEW` with a blank page count, fix the environment first; do not scale up to the archive on a broken setup.

## Doing it with PubAudit

```bash
python3 pubaudit.py /path/to/folder
# PDFs + pubaudit-report.csv / pubaudit-report.html land in
# /path/to/folder/pubaudit-output/ (or in the folder given with --out)
```

PubAudit is free and open source (MIT, Python standard library only). It converts locally via LibreOffice and verifies with `pdfinfo` / `pdftotext` from poppler-utils; your files are never uploaded. Repo: https://github.com/alapha888/pubaudit

Just found the files? [Found .pub files after Publisher support ended?](after-publisher-support-ended.md) gives the safe order of operations before you run anything. Already ran it and the pattern looks wrong? [Troubleshooting and large archives](troubleshooting-and-large-archives.md) covers the environment patterns and how to stage a big archive.

A Windows desktop edition (pick a folder, get the report, no command line) is on sale for $29 one-time: https://alapha888.gumroad.com/l/lvodxo — the free command-line tool is complete and usable today.
