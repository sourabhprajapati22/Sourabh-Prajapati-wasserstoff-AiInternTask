from app.core.pdf_to_text import extract_from_pdf
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.config import Config


def build_faiss_index(doc_number, page_texts, model_name=Config.EMBEDDING_MODEL):
    model = SentenceTransformer(model_name)
    embeddings = []
    metadata = []

    for page_num, text in page_texts.items():
        if not text.strip():
            continue
        paragraphs = text.split('\n\n')
        for para_idx, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                continue
            emb = model.encode(paragraph)
            embeddings.append(emb)
            metadata.append({
                'doc_id': doc_number,
                'page_idx': page_num,
                'para_idx': para_idx,
                'text': paragraph
            })

    # Convert to numpy array
    if not embeddings:
        raise ValueError("No valid paragraphs found to encode.")
    embedding_matrix = np.vstack(embeddings)

    # Create FAISS index
    dim = embedding_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embedding_matrix)

    # return index, metadata
    return embedding_matrix,metadata


def prepare_pagewise_text(result):
    page_texts = []

    for page_num, data in result.items():
        combined = f"Page {page_num}:\n"
        combined += data['text'][0] if data['text'] else ""

        for table in data.get('tables', []):
            table_string = "\n".join(["\t".join(row) for row in table])
            combined += f"\n{table_string}\n"

        page_texts.append((page_num, combined.strip()))

    return page_texts



def search_faiss_index(query, index, metadata, model_name='all-MiniLM-L6-v2', top_k=3):
    model = SentenceTransformer(model_name)
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results



# if __name__=='__main__':
#     result = extract_from_pdf("backend/data/EJ1172284.pdf")
#     index, metadata = build_faiss_index('doc001',result)
#     print(len(metadata))
#     print(search_faiss_index(query="what research on mobile done?",index=index,metadata=metadata))