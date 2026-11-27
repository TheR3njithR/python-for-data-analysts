import importlib.util, os, sys
from datetime import datetime
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE); sys.argv = ["token_check.py", "2026-12-08 22:00"]
spec = importlib.util.spec_from_file_location("token_check", os.path.join(HERE, "token_check.py")); tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)


def test_evening_login_expires_next_morning():
    assert tc.expiry(datetime(2026, 12, 8, 21, 40)) == datetime(2026, 12, 9, 6, 0)


def test_early_login_expires_same_morning():
    assert tc.expiry(datetime(2026, 12, 9, 5, 30)) == datetime(2026, 12, 9, 6, 0)


def test_login_at_six_lasts_until_next_six():
    assert tc.expiry(datetime(2026, 12, 9, 6, 0)) == datetime(2026, 12, 10, 6, 0)
