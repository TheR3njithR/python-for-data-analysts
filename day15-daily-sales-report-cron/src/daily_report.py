"""Daily sales report: yesterday's sales by store vs the same day last week, emailed as a CSV.
Synthetic data. SMTP host comes from the environment (default: a local test inbox, no password)."""
import argparse, os, smtplib, sys
from datetime import date, timedelta
from email.message import EmailMessage
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent.parent          # absolute paths: cron starts in $HOME
def build(day):
    df = pd.read_csv(HERE / "data/sales.csv", parse_dates=["date"])
    by = lambda d: df[df.date == pd.Timestamp(d)].groupby("store").amount.sum()
    t = pd.DataFrame({"today": by(day), "last_week": by(day - timedelta(days=7))})
    if t.today.isna().all(): sys.exit(f"no sales found for {day}: nothing sent")
    t["change_pct"] = ((t.today / t.last_week - 1) * 100).round(1)
    return t.sort_values("today", ascending=False)
def send(t, day):
    out = HERE / f"reports/sales_{day}.csv"; t.to_csv(out)
    msg = EmailMessage(); msg["Subject"] = f"Kaveri Mart daily sales {day}"
    msg["From"] = "reports@kaveri-mart.example"; msg["To"] = "manager@kaveri-mart.example"
    msg.set_content(f"Total {t.today.sum():,.0f} rupees across {len(t)} stores.\n\n{t.to_string()}")
    msg.add_attachment(out.read_bytes(), maintype="text", subtype="csv", filename=out.name)
    host, port = os.environ.get("SMTP_HOST", "localhost"), int(os.environ.get("SMTP_PORT", "8025"))
    with smtplib.SMTP(host, port) as s: s.send_message(msg)
    return out
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--date", type=date.fromisoformat,
                                                    default=date.today() - timedelta(days=1))
    day = ap.parse_args().date; t = build(day)
    print(t.to_string()); print(f"total {t.today.sum():,.0f} rupees; sent {send(t, day).name}")
