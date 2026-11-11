    import time
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch

app = FastAPI(title="Low-Latency Semantic Caching Proxy for LLMs")

# Load a lightweight, high-performance local embedding model (~80MB)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory cache store: list of dicts { "prompt": str, "embedding": torch.Tensor, "response": str }
cache_store = []
SIMILARITY_THRESHOLD = 0.88


class QueryRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_response(payload: QueryRequest):
    start_time = time.time()
    user_prompt = payload.prompt.strip()

    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # 1. Generate embedding for the incoming query
    query_embedding = model.encode(user_prompt, convert_to_tensor=True)

    # 2. Check cache if items exist
    if cache_store:
        stored_embeddings = torch.stack([item["embedding"] for item in cache_store])
        # Compute cosine similarities
        similarities = util.cos_sim(query_embedding, stored_embeddings)[0]
        best_match_idx = int(torch.argmax(similarities))
        best_score = float(similarities[best_match_idx])

        if best_score >= SIMILARITY_THRESHOLD:
            latency = (time.time() - start_time) * 1000
            return {
                "response": cache_store[best_match_idx]["response"],
                "cache_hit": True,
                "similarity_score": round(best_score, 4),
                "latency_ms": round(latency, 2),
            }

    # 3. Cache Miss: Simulate upstream LLM call
    time.sleep(0.4) # Simulating 400ms network latency
    upstream_response = f"AI Generated response for: '{user_prompt}' (Processed via upstream model)"

    # 4. Store in cache
    cache_store.append(
        {
            "prompt": user_prompt,
            "embedding": query_embedding,
            "response": upstream_response,
        }
    )

    latency = (time.time() - start_time) * 1000
    return {
        "response": upstream_response,
        "cache_hit": False,
        "similarity_score": 1.0,
        "latency_ms": round(latency, 2),
    }