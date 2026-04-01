import json
import ollama
from ingestion import chunk



def embed_chunkz(): 
    chunkz = chunk()
    # embed 
    embedded_chunks = []
    for chnk in chunkz:
        response = ollama.embed(
            model='nomic-embed-text',
            input= chnk["text"]
        )

        embedded_chunks.append({
            "embedding": response["embeddings"][0],
            "source": chnk["source"],
            "page": chnk["page"],
            "text": chnk["text"]
        })
    return embedded_chunks

embedded = embed_chunkz()
with open("data/processed/embedded_chunks.json", "w") as f:
    json.dump(embedded, f)
