

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

PURPOSE_CATEGORIES = {
    "Official Work": "Attending an official meeting, office inspection, "
                      "audit, documentation work, training session or conference",
    "Employee Visit": "Employee or staff member joining duty, reporting for "
                       "work, or an official employee movement",
    "Contractor": "Contractor, vendor or technician coming for maintenance, "
                  "repair, installation, fixing equipment or servicing",
    "Material Delivery": "Delivery of material, goods, supply, dispatch, "
                          "courier or shipment into the plant",
    "Family Visit": "Visiting family or relatives staying in the quarters, "
                     "a personal or family visit",
    "Interview": "Attending an interview, recruitment process, walk-in "
                 "selection, or a candidate visiting for a job",
    "Medical": "Medical visit, going to the hospital, health checkup, "
               "seeing a doctor, or a medical emergency",
}

_CATEGORY_NAMES = list(PURPOSE_CATEGORIES.keys())
_CATEGORY_DESCRIPTIONS = list(PURPOSE_CATEGORIES.values())

SIMILARITY_THRESHOLD = 0.35


_model = SentenceTransformer("all-MiniLM-L6-v2")
_category_embeddings = _model.encode(_CATEGORY_DESCRIPTIONS, normalize_embeddings=True)


def classify_dataframe(df: pd.DataFrame, purpose_col: str = "Purpose of Visit") -> pd.DataFrame:
    """
    Adds 'Purpose_Category' and 'Category_Confidence' columns using
    semantic similarity instead of keyword matching.
    """
    df = df.copy()
    purposes = df[purpose_col].fillna("").astype(str).tolist()

    # Batch-encode all rows at once — much faster than one-by-one.
    purpose_embeddings = _model.encode(purposes, normalize_embeddings=True)

    sims = cosine_similarity(purpose_embeddings, _category_embeddings)
    best_idx = sims.argmax(axis=1)
    best_score = sims.max(axis=1)

    categories = [
        _CATEGORY_NAMES[i] if score >= SIMILARITY_THRESHOLD else "Other"
        for i, score in zip(best_idx, best_score)
    ]

    df["Purpose_Category"] = categories
    df["Category_Confidence"] = best_score.round(3)
    return df


def analyze_other_cluster(df: pd.DataFrame, purpose_col: str = "Purpose of Visit",
                           n_clusters: int = 5) -> pd.DataFrame:
    """
    Real unsupervised analysis: clusters whatever fell into 'Other' so you
    can discover NEW hidden categories instead of dumping everything into
    one bucket. Prints a few representative examples per cluster so you
    can name each one.
    """
    if "Purpose_Category" not in df.columns:
        df = classify_dataframe(df, purpose_col)

    other_df = df[df["Purpose_Category"] == "Other"].copy()
    if len(other_df) < n_clusters:
        other_df["Cluster"] = -1
        return other_df

    texts = other_df[purpose_col].fillna("").astype(str).tolist()
    embeddings = _model.encode(texts, normalize_embeddings=True)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    other_df["Cluster"] = km.fit_predict(embeddings)

    print(f"Discovered {n_clusters} sub-patterns inside 'Other' "
          f"({len(other_df)} rows):")
    for c in range(n_clusters):
        sample = other_df.loc[other_df["Cluster"] == c, purpose_col].head(3).tolist()
        print(f"  Cluster {c} ({(other_df['Cluster'] == c).sum()} rows): {sample}")

    return other_df


def purpose_summary(df: pd.DataFrame, purpose_col: str = "Purpose of Visit") -> pd.DataFrame:
    """
    Category counts, same output shape as before — drop-in replacement.
    """
    classified_df = classify_dataframe(df, purpose_col)
    summary = classified_df["Purpose_Category"].value_counts().reset_index()
    summary.columns = ["Category", "Count"]
    return summary


if __name__ == "__main__":
    # Quick smoke test with the kind of messy phrasing real gate-pass logs have
    sample = pd.DataFrame({
        "Purpose of Visit": [
            "came to meet doctor for fever",
            "attending walk-in for junior engineer post",
            "here to fix the AC unit in C&IT block",
            "official meeting with GM",
            "bringing cement bags for construction",
            "visiting my brother staying in quarters",
            "joining as new staff today",
        ]
    })
    result = classify_dataframe(sample)
    print(result)