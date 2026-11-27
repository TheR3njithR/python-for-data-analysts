import socket, sys
sys.path.insert(0, "."); import rag
Q = "How many days to return a phone?"
def test_phone_question_finds_phone_note():
    top, n = rag.retrieve(Q, rag.load())
    assert n == 6 and top[0][0] == "returns-phones.txt"
def test_prompt_quotes_the_note_word_for_word():
    notes = rag.load(); top, _ = rag.retrieve(Q, notes)
    flat = " ".join(rag.augment(Q, notes, top).split())
    assert notes["returns-phones.txt"] in flat
def test_runs_with_no_network(monkeypatch):
    def no_net(*a, **k): raise OSError("network blocked")
    monkeypatch.setattr(socket, "socket", no_net)
    top, _ = rag.retrieve("When do stores open?", rag.load())
    assert top[0][0] == "store-hours.txt"
