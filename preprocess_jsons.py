import os
import json
import numpy as np
import pandas as pd
import joblib
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ========== ENV & HF CLIENT SETUP ==========
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN is not set! Please add it to your .env")

hf_client = InferenceClient(token=HF_TOKEN)
HF_EMBED_MODEL = "BAAI/bge-m3"   # same model you’re using at query time


def create_embeddings(text_list):
    """
    Create embeddings for a list of texts using Hugging Face Inference API.
    Returns a list of numpy arrays, one per text.
    """
    embeddings = []

    for text in text_list:
        vec = hf_client.feature_extraction(text, model=HF_EMBED_MODEL)
        vec = np.array(vec)

        # If output is (seq_len, dim), mean-pool over tokens
        if vec.ndim == 2:
            vec = vec.mean(axis=0)

        embeddings.append(vec)

    return embeddings


# ========== READ MERGED JSONS & BUILD DATAFRAME ==========
json_dir = "newjsons"
json_files = [f for f in os.listdir(json_dir) if f.endswith(".json")]

all_rows = []
chunk_id = 0

for json_file in json_files:
    with open(os.path.join(json_dir, json_file), "r", encoding="utf-8") as f:
        content = json.load(f)

    print(f"Creating embeddings for {json_file} (chunks: {len(content['chunks'])})")

    # Get all texts from this file’s chunks
    texts = [c["text"] for c in content["chunks"]]
    embeddings = create_embeddings(texts)

    # Attach embeddings + metadata
    for chunk, emb in zip(content["chunks"], embeddings):
        row = {
            "chunk_id": chunk_id,
            "file": json_file,
            "title": chunk.get("title", ""),
            "number": chunk.get("number", ""),
            "start": chunk.get("start", 0),
            "end": chunk.get("end", 0),
            "text": chunk.get("text", ""),
            "embedding": emb,
        }
        all_rows.append(row)
        chunk_id += 1

# Build final DataFrame ONCE
df = pd.DataFrame.from_records(all_rows)

# Save this DataFrame as embeddings.joblib ONCE
joblib.dump(df, "embeddings.joblib")
print(f"\nSaved embeddings.joblib with {len(df)} rows.")
