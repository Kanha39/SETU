import os
import requests
import pandas as pd
import chromadb

from chatbot.config import BASE_DIR, DATA_PATH

EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://localhost:11434/api/embed")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "bge-m3")
CHROMA_PATH = BASE_DIR / "database" / "chroma_store"
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "projects_semantic_index")

client = chromadb.PersistentClient(str(CHROMA_PATH))
collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

def create_embeddings(text_list, batch_size=16):
    all_embeddings = []

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        response = requests.post(
            EMBEDDING_URL,
            json={
                "model": EMBEDDING_MODEL,
                "input": batch
            },
            timeout=120
        )

        data = response.json()

        if "embeddings" not in data:
            raise RuntimeError(f"Embedding failed: {data}")

        all_embeddings.extend(data["embeddings"])

    return all_embeddings


def build_project_text(row):
    # Build one searchable text field from the project row
    text_parts = [
        row.get("project_name", ""),
        row.get("agency", ""),
        row.get("state", ""),
        row.get("ministry", ""),
        row.get("sector", ""),
        row.get("status", ""),
        row.get("project_code", ""),
        f"Original cost: {row.get('original_cost_cr', '')}",
        f"Revised cost: {row.get('revised_cost_cr', '')}",
        f"Cost overrun pct: {row.get('cost_overrun_pct', '')}",
        f"Delay actual days: {row.get('delay_actual_days', '')}",
        f"Cumulative expenditure: {row.get('cumulative expenditure in rs. crore', '')}",
        f"Physical progress: {row.get('physical progress (in percentage)', '')}",
    ]

    return " ".join(str(p) for p in text_parts if p not in ("", None))


def sync_projects_to_chroma():
    df = pd.read_csv(DATA_PATH, low_memory=False)

    # Optional: normalize/clean columns if needed
    for col in ["date_of_approval", "start_date", "actual_doc", "target_doc", "revised_doc"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").fillna("")

    documents = []
    metadatas = []
    ids = []

    for idx, row in df.iterrows():
        project_text = build_project_text(row)

        if not project_text.strip():
            continue

        project_id = str(row.get("project_code") or f"project_{idx}")
        documents.append(project_text)
        ids.append(project_id)

        metadatas.append({
            "project_code": str(row.get("project_code", "")),
            "project_name": str(row.get("project_name", "")),
            "agency": str(row.get("agency", "")),
            "state": str(row.get("state", "")),
            "ministry": str(row.get("ministry", "")),
            "sector": str(row.get("sector", "")),
            "status": str(row.get("status", "")),
            "row_index": int(idx),
        })

    embeddings = create_embeddings(documents)

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Indexed {len(documents)} projects into Chroma collection '{CHROMA_COLLECTION_NAME}'.")


def semantic_search(query, top_k=5):
    query_embedding = create_embeddings([query])[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return result


if __name__ == "__main__":
    sync_projects_to_chroma()

    query = "Which projects in Maharashtra had high delay risk?"
    result = semantic_search(query, top_k=5)
    print(result)