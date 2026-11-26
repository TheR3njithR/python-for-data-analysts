"""SHA-256 of every cell value in the input exports (ignores save timestamps). Same output on every run = reproducible data."""
import glob, hashlib, openpyxl
for f in sorted(glob.glob("input/*.xlsx")):
    h = hashlib.sha256()
    for ws in openpyxl.load_workbook(f).worksheets:
        for r in ws.iter_rows(values_only=True): h.update(repr(r).encode())
    print(h.hexdigest(), f)
