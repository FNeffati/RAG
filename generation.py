from dotenv import load_dotenv
from retrieval import retrieve
from openai import OpenAI

load_dotenv()
client = OpenAI()


def generate(qst=None):
    SYSTEM_PROMPT = """
    You are a compliance document assistant.

    Your job is to answer questions using ONLY the provided context.
    Return your response as a JSON object with the following fields:

    - "retrieved": boolean  
    True if context was provided (non-empty), false otherwise.

    - "answered": boolean  
    True if the question can be answered using the context, false if not.

    - "answer": string  
    A concise answer based ONLY on the context.  
    If the question cannot be answered, set this to:
    "I don't know based on the provided documents."

    - "citations": list of objects  
    Each citation must include:
        - "source": document name
        - "page": page number

    Rules:
    - Do NOT use any knowledge outside the provided context.
    - If the context is empty or insufficient, set "answered" to false.
    - Do NOT hallucinate.
    - Keep answers concise.

    Output ONLY valid JSON. No extra text.

    """

    if qst != None:
        user_question = qst
    else:
        user_question = input("Input your question: ")

    retrieved = retrieve(user_question)
    # print(retrieved)
    # print("###########################")

    if not retrieved:
        return {
            "retrieved": False,
            "answered": False,
            "answer": "I don't know based on the provided documents.",
            "citations": []
        }
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

        # print(response.output_text)
        return response.output_text