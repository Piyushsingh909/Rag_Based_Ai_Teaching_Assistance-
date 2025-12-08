# processing_incoming.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests
import os
from dotenv import load_dotenv
from groq import Groq

# ========= ENV (OPTIONAL) =========
load_dotenv()

# ========= GROQ SETUP (DIRECT KEY) =========
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # ⚠️ don't push this to GitHub

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is empty. Please paste your actual key.")

groq_client = Groq(api_key=GROQ_API_KEY)

# Choose a Groq model
GROQ_MODEL_ID = "llama-3.3-70b-versatile"

# ========= LOAD EMBEDDINGS ONCE =========
# Make sure embeddings.joblib is in the same folder
df = joblib.load("embeddings.joblib")


# ========= OLLAMA EMBEDDING / INFERENCE =========
def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )
    r.raise_for_status()
    embedding = r.json()["embeddings"]
    return embedding


# (Optional: not used by Flask, but kept if you still want it)
def interference_ollama(prompt):
    r = requests.post(
        "http://localhost:11434/api/inference",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    r.raise_for_status()
    response = r.json()
    print("Raw Ollama response:", response)
    return response


# ========= GROQ CHAT INFERENCE =========
def interference_groq(prompt: str) -> str:
    """
    Call Groq chat model and return plain text response.
    """
    try:
        chat_completion = groq_client.chat.completions.create(
            model=GROQ_MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Optical Communication teacher helping a student."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.4,
            max_tokens=400,
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Error during Groq inference:", e)
        return "Sorry, I ran into an error while generating the answer."


# ========= RAG PIPELINE AS A FUNCTION =========
def answer_question(incoming_query: str) -> str:
    """
    Given a user question string, run RAG + Groq and return answer text.
    """

    # Create embedding for user query
    question_embedding = create_embedding([incoming_query])[0]

    # Compute cosine similarities with stored embeddings
    similarities = cosine_similarity(
        np.vstack(df["embedding"]),
        [question_embedding]
    ).flatten()

    top_results = 5
    max_indx = similarities.argsort()[::-1][0:top_results]
    new_df = df.loc[max_indx]

    prompt = f'''I am teaching Optical Communication in this subject course. Here are video subtitle chunks containing video title, video number, start time in
seconds, end time in seconds, and the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

------------------------------
User question: "{incoming_query}"

You are an expert Optical Communication teacher helping a student.
You must answer in a human, friendly way.
Tell clearly and concisely:
- In which video number(s)
- At what timestamps (start–end seconds)
- Briefly what is covered there related to the question.

If the question is unrelated to Optical Communication, say that you can answer only questions related to these Optical Communication videos and you don't have any knowledge beyond that.
'''

    # Optional: save prompt (debug)
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    response_text = interference_groq(prompt)

    # Optional: save response (debug)
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(response_text)

    return response_text


# Optional CLI usage (for testing in terminal)
if __name__ == "__main__":
    q = input("Ask a question: ")
    print(answer_question(q))
