
# Simple Meilisearch indexing script (requires 'meilisearch' python package)
import os, json
from meilisearch import Client

MEILI_URL = os.getenv('MEILI_URL', 'http://127.0.0.1:7700')
MEILI_KEY = os.getenv('MEILI_KEY', 'masterKey')
client = Client(MEILI_URL, MEILI_KEY)

def load_entries():
    docs=[]
    for root,_,files in os.walk('lexicon'):
        for fn in files:
            if fn.endswith('.json') and fn != 'index.json':
                p=os.path.join(root,fn)
                with open(p,'r',encoding='utf-8') as f:
                    data=json.load(f)
                    docs.append({'id': p, 'word': data.get('word'), 'definitions': data.get('definitions')})
    return docs

if __name__ == '__main__':
    idx = client.index('rki_lexicon')
    docs = load_entries()
    if docs:
        idx.add_documents(docs)
    print('Indexed', len(docs))
