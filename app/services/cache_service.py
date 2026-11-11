import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import settings


class SemanticCacheService:

    def __init__(self):
        print("Initializing enhanced semantic cache service...")
        # Use analyzer='word' with ngram range to capture phrases and variations better
        self.vectorizer = TfidfVectorizer(
            stop_words="english", ngram_range=(1, 2), lowercase=True
        )
        self.cache_store = []  # List of dicts: prompt, response

    def process_query(self, user_prompt: str) -> dict:
        start_time = time.time()
        user_prompt = user_prompt.strip()

        # 1. Check Cache if items exist
        if self.cache_store:
            try:
                corpus = [item["prompt"] for item in self.cache_store] + [
                    user_prompt
                ]
                tfidf_matrix = self.vectorizer.fit_transform(corpus)
                # Compare the latest prompt (last row) against all previous prompts
                similarity_matrix = cosine_similarity(
                    tfidf_matrix[-1], tfidf_matrix[:-1]
                )
                similarities = similarity_matrix[0]

                if len(similarities) > 0:
                    best_match_idx = int(np.argmax(similarities))
                    best_score = float(similarities[best_match_idx])

                    print(
                        f"Comparing '{user_prompt}' -> Best match: '{self.cache_store[best_match_idx]['prompt']}' | Score: {best_score}"
                    )

                    if best_score >= settings.similarity_threshold:
                        latency_ms = round(
                            (time.time() - start_time) * 1000, 2
                        )
                        return {
                            "response": self.cache_store[best_match_idx][
                                "response"
                            ],
                            "cache_hit": True,
                            "similarity_score": round(best_score, 4),
                            "latency_ms": latency_ms,
                            "total_cached_queries": len(self.cache_store),
                        }
            except Exception as e:
                print(f"Vector calculation error: {e}")

        # 2. Cache Miss: Simulate Upstream LLM Processing
        time.sleep(settings.upstream_delay_sec)
        upstream_response = f"AI Response for: '{user_prompt}' (Generated via upstream model execution)"

        # 3. Store in cache
        self.cache_store.append(
            {"prompt": user_prompt, "response": upstream_response}
        )

        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "response": upstream_response,
            "cache_hit": False,
            "similarity_score": 1.0,
            "latency_ms": latency_ms,
            "total_cached_queries": len(self.cache_store),
        }

    def get_stats(self) -> dict:
        return {
            "total_cached_queries": len(self.cache_store),
            "similarity_threshold": settings.similarity_threshold,
            "model": "Enhanced TF-IDF Cosine Engine",
        }


# Singleton instance
cache_service = SemanticCacheService()