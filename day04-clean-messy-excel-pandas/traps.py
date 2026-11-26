"""The three beginner traps, measured on the same file (run: python traps.py)."""
import os, pandas as pd, warnings
warnings.filterwarnings("ignore")
H = os.path.dirname(os.path.abspath(__file__))
raw = pd.read_excel(os.path.join(H, "input", "Kaveri_Orders_Oct2026.xlsx"), dtype=object)
print("raw dtype of order_date:", raw.order_date.dtype)
naive = pd.to_datetime(raw.order_date.astype(str), errors="coerce")
print(f"trap 1, one-line pd.to_datetime: {naive.isna().sum()} dates became NaT (unreadable)")
oct_ = naive.dropna(); print(f"         of the {len(oct_):,} it did read, {int((oct_.dt.month != 10).sum())} landed outside October (day and month swapped)")
print(f"trap 2, plain drop_duplicates(): removes {len(raw) - len(raw.drop_duplicates())} rows, misses the copies with different case and spaces")
print(f"trap 3, plain dropna(): keeps {len(raw.dropna()):,} of {len(raw):,} rows, because 'landline' is almost always empty")
