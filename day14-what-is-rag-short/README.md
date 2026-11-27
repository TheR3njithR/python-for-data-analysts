# Day 14 — What Is RAG? Explained in 30 Seconds with One Diagram #Shorts

Companion files for **What Is RAG? Explained in 30 Seconds with One Diagram #Shorts** on **TheDataScientist | Renjith R** (ML Explained with Real Business Problems, Daily Growth Day 14). The scheduled YouTube URL will be added here after upload.

`rag.py` is a fully offline demo of retrieval-augmented generation on six made-up help notes for Kaveri Mart, a made-up shop. It retrieves the top two notes, builds the prompt a model would see, and stops there. There is no model, no API key and no network. Three tests in `tests/test_rag.py` check that the phone-return question finds the phones note, that the prompt quotes that note word for word, and that the script still runs when the network is blocked.

For "How many days to return a phone?", retrieval ranks `returns-phones.txt` (7 days) above `returns-general.txt` (30 days).

All notes are synthetic. Kaveri Mart is made up. No real company, customer or credential.

| File | What it does |
|---|---|
| `rag.py` | Offline retrieve-and-augment demo (`--diagram`, or pass a question) |
| `notes/` | Six short help notes used in the video |
| `tests/test_rag.py` | 3 pytest checks, including a no-network test |
| `run_all.sh` | Prints the diagram, runs the phone question and the tests |

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pytest
./run_all.sh                                           # or: PY=python3 ./run_all.sh
# or one command at a time:
# python rag.py --diagram
# python rag.py "How many days to return a phone?"
# python -m pytest -q tests
```

Origin of the RAG idea: Lewis et al. 2020, https://arxiv.org/abs/2005.11401
