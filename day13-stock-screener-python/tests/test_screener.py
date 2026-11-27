import sys; sys.path.insert(0, "src")
from load_bhav import load
from screener import screen
raw, clean = load(); last = screen(clean)
def test_only_eq_rows(): assert set(clean.SERIES) == {"EQ"}
def test_repeated_file_dropped(): assert not clean.duplicated(["SYMBOL", "DATE1"]).any()
def test_dash_is_missing_not_text():
    assert clean.DELIV_PER.dtype == float and clean.DELIV_PER.isna().any()
def test_missing_delivery_never_passes():
    assert not last[last.deliv20.isna()].passes.any()
def test_every_pass_meets_all_four_rules():
    p = last[last.passes]
    assert (p.CLOSE_PRICE > p.sma50).all() and (p.ret20 > 5).all()
    assert (p.turn20 >= 2500).all() and (p.deliv20 >= 40).all()
