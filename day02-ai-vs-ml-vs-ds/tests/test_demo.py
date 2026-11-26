"""Sanity tests: the data is reproducible and the three steps give the numbers the video quotes."""
import subprocess, sys, os, hashlib, re
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PY = sys.executable
run = lambda f: subprocess.run([PY, os.path.join(H, f)], capture_output=True, text=True, check=True).stdout
def test_data_is_reproducible():
    a = hashlib.sha1(open(os.path.join(H, "data", "orders_aug_oct.csv"), "rb").read()).hexdigest(); run("make_data.py")
    assert a == hashlib.sha1(open(os.path.join(H, "data", "orders_aug_oct.csv"), "rb").read()).hexdigest()
def test_answer_key_not_in_public_data():
    assert "is_abuse" not in open(os.path.join(H, "data", "orders_aug_oct.csv")).readline()
def test_data_science_finds_both_causes():
    o = run("01_data_science.py"); assert "Kochi" in o and "6 addresses" in o
def test_model_beats_nothing():
    o = run("02_machine_learning.py"); r = int(re.search(r"recall (\d+)%", o).group(1)); assert r >= 80
def test_ml_bot_holds_fewer_genuine_than_rule_bot():
    o = open(os.path.join(H, "outputs", "03_ai_system.txt")).read(); g = [int(x) for x in re.findall(r"genuine customers held (\d+)", o)]
    assert g[1] <= g[0]
