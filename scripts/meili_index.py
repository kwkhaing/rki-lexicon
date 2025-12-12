import os, json, hashlib
from meilisearch import Client

MEILI_URL = os.getenv("MEILI_URL", "http://127.0.0.1:7700")
MEILI_KEY = os.getenv("MEILI_KEY", "masterKey")
client = Client(MEILI_URL, MEILI_KEY)

CHECKSUM_FILE = ".meili_checksums.json"

def file_checksum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def load_previous_checksums():
    if not os.path.exists(CHECKSUM_FILE):
        return {}
    with open(CHECKSUM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_checksums(checksums):
    with open(CHECKSUM_FILE, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2)

def load_changed_entries(previous):
    changed = []

    for root, _, files in os.walk("lexicon"):
        for fn in files:
            if not fn.endswith(".json") or fn == "index.json":
                continue

            path = os.path.join(root, fn)
            cs = file_checksum(path)

            if previous.get(path) != cs:
                # changed file
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                changed.append({
                    "id": path,
                    "word": data.get("word"),
                    "definitions": data.get("definitions")
                })
                previous[path] = cs

    return changed, previous

if __name__ == "__main__":
    old = load_previous_checksums()
    changed_docs, updated = load_changed_entries(old)

    if not changed_docs:
        print("NO CHANGED DOCUMENTS → SKIPPING INDEXING")
        exit(0)

    print(f"Indexing {len(changed_docs)} changed documents...")
    index = client.index("rki_lexicon")
    index.add_documents(changed_docs)

    save_checksums(updated)

    print("Incremental indexing complete.")
