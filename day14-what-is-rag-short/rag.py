"""RAG in one file, fully offline: retrieve notes, augment the prompt.
Kaveri Mart is made up. No model, no API key, no network."""
import math, re, sys, textwrap
from pathlib import Path
STOP = set("a an the to of in is are can i do how many what for my with if from".split())
def words(t):
    return [re.sub(r"(ed|s)$", "", w) for w in re.findall(r"[a-z]+", t.lower())
            if w not in STOP]
def load(folder="notes"):
    return {p.name: p.read_text().strip() for p in sorted(Path(folder).glob("*.txt"))}
def retrieve(question, notes, k=2):
    docs = {n: words(t) for n, t in notes.items()}
    idf = {w: math.log(len(docs) / sum(w in d for d in docs.values()))
           for d in docs.values() for w in d}
    q = set(words(question))
    score = {n: sum(idf[w] for w in set(d) & q) / math.sqrt(len(d))
             for n, d in docs.items()}
    return sorted(score.items(), key=lambda x: -x[1])[:k], len(docs)
def augment(question, notes, top):
    ctx = "\n".join(textwrap.fill(f"[{n}] {notes[n]}", 38) for n, _ in top)
    return f"Answer only from these notes.\n{ctx}\nQuestion: {question}"
DIAGRAM = """question
   |
[1 RETRIEVE] search your notes
   |          -> top 2 notes
[2 AUGMENT]  notes + question
   |          -> one prompt
[3 GENERATE] a model answers
              from the prompt"""
if __name__ == "__main__":
    if sys.argv[1] == "--diagram":
        sys.exit(print(DIAGRAM))
    q, notes = sys.argv[1], load()
    top, n = retrieve(q, notes)
    print(f"1 RETRIEVE: {n} notes scored, top 2:")
    for name, s in top:
        print(f"  {s:.2f}  {name}")
    print("2 AUGMENT: the prompt\n" + augment(q, notes, top))
    print("3 GENERATE: a model answers from it\n  (none here: offline demo)")
