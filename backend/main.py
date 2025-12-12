
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os, json, uuid

LEXICON_DIR = "lexicon"
PENDING_DIR = "corpus/community_submissions/pending"
AUDIO_RAW = "audio/raw"

app = FastAPI(title="rki-lexicon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_entry(word):
    # naive loader: search files for matching 'word' field
    for root,_,files in os.walk(LEXICON_DIR):
        for fn in files:
            if fn.endswith(".json") and fn != "index.json":
                path = os.path.join(root, fn)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("word") == word or data.get("word").lower() == word.lower():
                        return data
    return None

@app.get("/api/word/{word}")
def get_word(word: str):
    entry = load_entry(word)
    if not entry:
        raise HTTPException(status_code=404, detail="Word not found")
    return entry

@app.get("/api/search")
def search(q: str):
    results=[]
    ql = q.lower()
    for root,_,files in os.walk(LEXICON_DIR):
        for fn in files:
            if fn.endswith(".json") and fn != "index.json":
                path = os.path.join(root, fn)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if ql in data.get("word","").lower() or any(ql in (d.get("gloss","").lower()) for d in data.get("definitions",[])):
                        results.append({"word":data.get("word"), "definitions": data.get("definitions")})
    return {"count": len(results), "results": results}

@app.post("/api/submit")
async def submit_word(entry: str = Form(...)):
    # save raw submission
    uid = str(uuid.uuid4())[:8]
    os.makedirs(PENDING_DIR, exist_ok=True)
    path = os.path.join(PENDING_DIR, f"submission_{uid}.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)
    return {"status":"saved","path":path}

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...), speaker: str = Form("anonymous")):
    os.makedirs(AUDIO_RAW, exist_ok=True)
    filename = f"{speaker}_{str(uuid.uuid4())[:8]}_{file.filename}"
    path = os.path.join(AUDIO_RAW, filename)
    with open(path, "wb") as out:
        content = await file.read()
        out.write(content)
    # minimal metadata append
    meta_path = os.path.join("audio","metadata.csv")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "a", encoding="utf-8") as m:
        m.write(f"{filename},{speaker}\n")
    return {"status":"ok","filename":filename}
