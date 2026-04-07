import json
import ollama
from numpy import dot
from numpy.linalg import norm 

def cosine_similarity(qst, chunk):
        return dot(qst, chunk)/(norm(qst)*norm(chunk))

with open("data/processed/embedded_chunks.json", "r") as f:
    chunkz = json.load(f)

def retrieve(user_question): 

    embedded_user_question = ollama.embed(
            model='nomic-embed-text',
            input= user_question
        )["embeddings"][0]
    # compare question embedding against chunk embeddings using cosine sim
    comps = []
    for chunk in chunkz:
        cs = cosine_similarity(embedded_user_question, chunk["embedding"])
        if cs > 0.6:
            comps.append((cs, chunk))

    if len(comps) < 1:
        # print("Nothing useful.")
        return []
    
    # print top 3 chunks with source and page
    sorted_similars = sorted(comps, key=lambda x: x[0], reverse=True)
    top_chunks = []
    for score, chunk in sorted_similars[:5]:
        # formatted = f"""Source: {chunk['source']} | "Page:"{chunk["page"]} Text: {chunk["text"]}"""
        # print(formatted)
        res = {
            "score": score,
            "source": chunk['source'],
            "page": chunk["page"],
            "text": chunk["text"]
        }
        top_chunks.append(res)
    return top_chunks


# test
# question = input("Input your question: ")
# print(retrieve())