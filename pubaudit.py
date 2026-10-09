#!/usr/bin/env python3
"""PubAudit — batch-convert Microsoft Publisher (.pub) files to PDF and
verify every single output.

Why this exists: Microsoft removed Publisher from Microsoft 365 on
2026-10-01 (perpetual support ends 2026-10-13). Single-file online
converters are free and plentiful, but nobody tells you which files in a
folder of hundreds actually converted — converters can report success and
produce no file, or produce a PDF with no usable text. PubAudit converts
a whole folder locally (via LibreOffice/libmspub, no uploads) and writes
a report classifying every file as OK / REVIEW / FAILED.

Stdlib only. Requires: soffice (LibreOffice), pdfinfo + pdftotext
(poppler-utils) for verification.
"""
import argparse
import csv
import html
import os
import shutil
import subprocess
import sys
import tempfile

TEXT_OK_THRESHOLD = 20  # chars of extractable text for a clean OK


OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")


def is_real_pub(path):
    """Real .pub files are OLE2 compound documents. Without this check,
    LibreOffice happily 'converts' a renamed text file as a text document
    and the audit would report a false OK (found in v0.1 testing)."""
    try:
        with open(path, "rb") as f:
            return f.read(8) == OLE_MAGIC
    except OSError:
        return False


def find_pubs(root):
    pubs = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if name.lower().endswith(".pub"):
                pubs.append(os.path.join(dirpath, name))
    return sorted(pubs)


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def pdf_pages(pdf_path):
    try:
        out = run(["pdfinfo", pdf_path], timeout=30)
        for line in out.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":", 1)[1].strip())
    except Exception:
        pass
    return None


def pdf_text_chars(pdf_path):
    try:
        out = run(["pdftotext", pdf_path, "-"], timeout=60)
        return len(out.stdout.strip())
    except Exception:
        return None


def convert_one(pub_path, out_dir, profile_dir):
    """Convert one .pub to PDF. Returns (pdf_path_or_None, soffice_output)."""
    before = set(os.listdir(out_dir)) if os.path.isdir(out_dir) else set()
    cmd = [
        "soffice", "--headless", "--norestore",
        f"-env:UserInstallation=file://{profile_dir}",
        "--convert-to", "pdf", "--outdir", out_dir, pub_path,
    ]
    try:
        proc = run(cmd, timeout=300)
        output = (proc.stdout or "") + (proc.stderr or "")
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT after 300s"
    expected = os.path.join(
        out_dir, os.path.splitext(os.path.basename(pub_path))[0] + ".pdf")
    if os.path.isfile(expected) and os.path.getsize(expected) > 0:
        return expected, output.strip()
    # Fallback: any new PDF in out_dir counts (name normalisation edge cases)
    after = set(os.listdir(out_dir)) if os.path.isdir(out_dir) else set()
    new_pdfs = [f for f in (after - before) if f.lower().endswith(".pdf")]
    if new_pdfs:
        p = os.path.join(out_dir, new_pdfs[0])
        if os.path.getsize(p) > 0:
            return p, output.strip()
    return None, f"rc={rc} no PDF produced. {output.strip()}"


def audit_file(pub_path, root, out_root, profile_dir):
    rel = os.path.relpath(pub_path, root)
    out_dir = os.path.join(out_root, os.path.dirname(rel))
    os.makedirs(out_dir, exist_ok=True)
    row = {
        "file": rel,
        "size_bytes": os.path.getsize(pub_path),
        "status": "",
        "pages": "",
        "text_chars": "",
        "pdf": "",
        "note": "",
    }
    if not is_real_pub(pub_path):
        row["status"] = "FAILED"
        row["note"] = ("Not a real Publisher file (missing OLE2 header) — "
                       "it may be corrupted or simply renamed from another format.")
        return row
    pdf_path, note = convert_one(pub_path, out_dir, profile_dir)
    if pdf_path is None:
        # The core case this tool exists for: conversion claimed to run
        # (or failed quietly) and there is nothing usable to show for it.
        row["status"] = "FAILED"
        row["note"] = ("No PDF produced (silent failure or unreadable file). "
                       f"Converter said: {note[:200]}")
        return row
    row["pdf"] = os.path.relpath(pdf_path, out_root)
    pages = pdf_pages(pdf_path)
    chars = pdf_text_chars(pdf_path)
    row["pages"] = pages if pages is not None else ""
    row["text_chars"] = chars if chars is not None else ""
    if pages is not None and pages >= 1 and chars is not None and chars >= TEXT_OK_THRESHOLD:
        row["status"] = "OK"
        row["note"] = "Converted; PDF has pages and extractable text."
    elif pages is not None and pages >= 1:
        row["status"] = "REVIEW"
        row["note"] = ("PDF produced but little/no extractable text "
                       "(image-heavy layout, or text lost in conversion). "
                       "Open the PDF and check it visually before deleting the .pub.")
    else:
        row["status"] = "REVIEW"
        row["note"] = "PDF produced but page count could not be verified."
    return row


def write_reports(rows, out_root):
    csv_path = os.path.join(out_root, "pubaudit-report.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "size_bytes", "status",
                                          "pages", "text_chars", "pdf", "note"])
        w.writeheader()
        w.writerows(rows)
    counts = {s: sum(1 for r in rows if r["status"] == s)
              for s in ("OK", "REVIEW", "FAILED")}
    trs = "\n".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            html.escape(str(r["file"])), r["status"], r["pages"],
            r["text_chars"], html.escape(str(r["note"])))
        for r in rows)
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>PubAudit report</title>
<style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:2em auto;padding:0 1em}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:6px 8px;text-align:left;font-size:14px}}</style>
</head><body>
<h1>PubAudit report</h1>
<p>{len(rows)} .pub file(s): {counts['OK']} OK, {counts['REVIEW']} to review, {counts['FAILED']} failed.</p>
<p>Keep the original .pub files until every REVIEW and FAILED row has been dealt with.</p>
<table><tr><th>File</th><th>Status</th><th>Pages</th><th>Text chars</th><th>Note</th></tr>
{trs}
</table></body></html>
"""
    html_path = os.path.join(out_root, "pubaudit-report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return csv_path, html_path, counts


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Batch-convert .pub files to PDF and verify every output.")
    ap.add_argument("folder", help="Folder to scan recursively for .pub files")
    ap.add_argument("--out", default=None,
                    help="Output folder (default: <folder>/pubaudit-output)")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.folder)
    if not os.path.isdir(root):
        print(f"error: {root} is not a folder", file=sys.stderr)
        return 2
    if shutil.which("soffice") is None:
        print("error: LibreOffice (soffice) not found on PATH. "
              "Install LibreOffice first — it provides the .pub reader.",
              file=sys.stderr)
        return 2
    out_root = os.path.abspath(args.out) if args.out else os.path.join(root, "pubaudit-output")
    os.makedirs(out_root, exist_ok=True)
    pubs = find_pubs(root)
    # Do not re-audit our own output tree if it lives inside the scan root
    pubs = [p for p in pubs if not os.path.abspath(p).startswith(out_root)]
    if not pubs:
        print("No .pub files found.")
        return 0
    print(f"Found {len(pubs)} .pub file(s). Converting and verifying...")
    rows = []
    with tempfile.TemporaryDirectory(prefix="pubaudit-profile-") as profile_dir:
        for i, pub in enumerate(pubs, 1):
            row = audit_file(pub, root, out_root, profile_dir)
            rows.append(row)
            print(f"[{i}/{len(pubs)}] {row['status']}: {row['file']}")
    csv_path, html_path, counts = write_reports(rows, out_root)
    print(f"\nDone: {counts['OK']} OK, {counts['REVIEW']} REVIEW, {counts['FAILED']} FAILED")
    print(f"Reports: {csv_path} / {html_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
