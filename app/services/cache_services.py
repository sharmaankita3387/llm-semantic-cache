import time
import torch
import numpy as np
from sentence_transformers import SentenceTransformer, util
from app.config import settings


class SemanticCacheService:

    def __init__(self):
        print(f"Loading embedding model: {settings.embedding_model_name}...")
        self.model = SentenceTransformer(settings.embedding_model_name)
        self.cache_store = []  # List of dicts: prompt, embedding, response

    def process_query(self, user_prompt: str) -> dict:
        start_time = time.time()
        query_embedding = self.model.encode(
            user_prompt, convert_to_tensor=True
        )

        # 1. Check Cache
        if self.cache_store:
            stored_embeddings = torch.stack(
                [item["embedding"] for item in self.cache_store]
            )
            similarities = util.cos_sim(query_embedding, stored_embeddings)[0]
            best_match_idx = int(torch.argmax(similarities))
            best_score = float(similarities[best_match_idx])

            if best_score >= settings.similarity_threshold:
                latency_ms = round((time.time() - start_time) * 1000, 2)
                return {
                    "response": self.cache_store[best_match_idx]["response"],
                    "cache_hit": True,
                    "similarity_score": round(best_score, 4),
                    "latency_ms": latency_ms,
                    "total_cache_entries": len(self.cache_store),
                }

        # 2. Cache Miss: Simulate Upstream LLM Processing
        time.sleep(settings.upstream_delay_sec)
        upstream_response = f"Synthesized LLM response for: '{user_prompt}' (Generated via upstream model execution)"

        # 3. Store in cache
        self.cache_store.append(
            {
                "prompt": user_prompt,
                "embedding": query_embedding,
                "response": upstream_response,
            }
        )

        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "response": upstream_response,
            "cache_hit": False,
            "similarity_score": 1.0,
            "latency_ms": latency_ms,
            "total_cache_entries": len(self.cache_store),
        }

    def get_stats(self) -> dict:
        return {
            "total_cached_queries": len(self.cache_store),
            "similarity_threshold": settings.similarity_threshold,
            "model": settings.embedding_model_name,
        }


# Singleton instance
cache_service = SemanticCacheService()