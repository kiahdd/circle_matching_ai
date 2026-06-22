"""Matching, clustering, and circle formation helpers for CircleMatch."""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def generate_profile_embeddings(df, profile_column="profile_text", model_name="BAAI/bge-small-en-v1.5"):
    """Generate normalized sentence embeddings for each user profile."""
    if profile_column not in df.columns:
        raise ValueError(f"DataFrame must contain '{profile_column}' column")

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        df[profile_column].tolist(),
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    if isinstance(embeddings, np.ndarray):
        return embeddings

    return np.array(embeddings)


def compute_similarity_matrix(embeddings):
    """Compute cosine similarity matrix for user embeddings."""
    return cosine_similarity(embeddings)


def show_neighbors(df, sim, user_idx, top_k=5):
    """Print the nearest neighbors for a target user index."""
    print("=" * 100)
    print("TARGET USER:", df.loc[user_idx, "user_id"])
    print(df.loc[user_idx, "profile_text"])
    print("\nTOP NEIGHBORS\n")

    neighbor_idxs = np.argsort(sim[user_idx])[::-1][1:top_k + 1]

    for idx in neighbor_idxs:
        print("-" * 80)
        print("Neighbor:", df.loc[idx, "user_id"])
        print("Similarity:", round(sim[user_idx, idx], 3))
        print(df.loc[idx, "profile_text"][:1200])
        print()
