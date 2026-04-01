from dotenv import load_dotenv
from retrieval import retrieve
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are a compliance document assistant.

Answer the user's question using only the provided context.
If the answer is not clearly supported by the context or the context is empty, say:
"I don't know based on the provided documents."

Be concise.
Include citations in this format:
(Source: document name, Page: page number)
"""

user_question = input("Input your question: ")
retrieved = retrieve(user_question)
print(retrieved)
print("###########################")

if not retrieved:
    print("I don't know based on the provided documents.")
else:
    retrieved_context = "\n\n".join(
        [
            f"Source: {chunk['source']} | Page: {chunk['page']}\nText: {chunk['text']}"
            for chunk in retrieved
        ]
    )

    user_prompt = f"""Question:
{user_question}

Context:
{retrieved_context}
"""

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": [
                    {"type": "input_text", "text": SYSTEM_PROMPT}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt}
                ],
            },
        ],
    )

    print(response.output_text)