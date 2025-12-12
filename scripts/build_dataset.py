
import os, json, csv

LEXICON_DIR = "lexicon"
OUTPUT_DIR = "corpus/cleaned"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def collect_sentences():
    out_path = os.path.join(OUTPUT_DIR, "rki_eng_sentences.tsv")
    with open(out_path, "w", encoding="utf-8", newline='') as out:
        writer = csv.writer(out, delimiter='\t')
        for root,_,files in os.walk(LEXICON_DIR):
            for fn in files:
                if fn.endswith(".json") and fn != "index.json":
                    p = os.path.join(root, fn)
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for ex in data.get("examples",[]):
                            eng = ex.get("translation",{}).get("english","")
                            writer.writerow([ex.get("sentence",""), eng])
    print("Wrote", out_path)

if __name__ == '__main__':
    collect_sentences()
