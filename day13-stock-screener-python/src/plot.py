"""Chart one shortlisted symbol: close vs its 50-day average (synthetic data)."""
import sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from load_bhav import load
sym = sys.argv[1] if len(sys.argv) > 1 else "DEMOAGRI17"
d = load()[1].query("SYMBOL == @sym").set_index("DATE1")
ax = d.CLOSE_PRICE.plot(figsize=(9, 4.2), label="close")
d.CLOSE_PRICE.rolling(50).mean().plot(ax=ax, label="50-day average", linestyle="--")
ax.set_title(f"{sym}: close vs 50-day average, Jul-Sep 2026 (synthetic data)")
ax.set_ylabel("Price (rupees)"); ax.set_xlabel(""); ax.grid(alpha=0.3); ax.legend()
plt.tight_layout(); plt.savefig(f"output/{sym}.png", dpi=110); print(f"saved output/{sym}.png")
