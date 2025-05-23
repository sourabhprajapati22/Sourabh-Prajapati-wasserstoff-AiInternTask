import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.build_faiss import build_faiss_index
from app.core.pdf_to_text import extract_from_pdf
from app.config import Config



class VectorStoreManager:
    def __init__(self, save_dir='backend/vector_store', model_name=Config.EMBEDDING_MODEL):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

        self.model = SentenceTransformer(model_name)
        self.index_path = os.path.join(save_dir, 'index.faiss')
        self.metadata_path = os.path.join(save_dir, 'metadata.jsonl')

        self.index = None
        self.metadata = []

        self._load_or_initialize()

    def _load_or_initialize(self):
        """Load existing FAISS index and metadata if they exist, otherwise initialize new ones."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = [json.loads(line) for line in f]
            print("✅ Loaded existing FAISS index and metadata.")
        else:
            self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
            print("🆕 Initialized new FAISS index.")

    def _save_index(self):
        """Save the FAISS index to disk."""
        faiss.write_index(self.index, self.index_path)

    def _append_metadata(self, new_metadata):
        """Append new metadata to the JSONL file and in-memory list."""
        with open(self.metadata_path, 'a', encoding='utf-8') as f:
            for item in new_metadata:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        self.metadata.extend(new_metadata)

    def _rewrite_metadata(self):
        """Rewrite the entire metadata JSONL file from in-memory metadata."""
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            for item in self.metadata:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')


    def add_document(self,doc_id, embedding, metadata):
        # Check if doc_id already exists
        if any(item['doc_id'] == doc_id for item in self.metadata):
            print(f"⚠️ Document with ID {doc_id} already exists. Use update_document to modify.")
            return
        

        start_idx = self.index.ntotal
        self.index.add(embedding)
        

        # Create metadata for each page
        new_metadata = [
            {'doc_id': text['doc_id'], 'page_idx': text['para_idx'], 'vector_idx': start_idx + i,'para_idx':text['para_idx'],'text': text['text']}
            for i, text in enumerate(metadata)
        ]


        self._append_metadata(new_metadata)
        self._save_index()
        print(f"✅ Added document {doc_id} with pages.")


    def search(self, query, k=5):
        """
        Search for the top-k most similar documents to the query.

        Args:
            query: String to search for
            k: Number of results to return

        Returns:
            List of (doc_id, page_idx, text, score) tuples
        """
        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, k)
        
        # Retrieve results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1 and idx < len(self.metadata):  # Valid index
                metadata = self.metadata[idx]
                score = 1 / (1 + distance)  # Convert distance to similarity score
                results.append((
                    metadata['doc_id'],
                    metadata['page_idx'],
                    metadata['para_idx'],
                    metadata['text'],
                    score
                ))
        
        return results

    def get_document(self, doc_id):
        """
        Retrieve all pages of a document by its ID.

        Args:
            doc_id: Unique ID of the document

        Returns:
            List of (page_idx, text) tuples if found, None otherwise
        """
        pages = [
            (item['page_idx'], item['text'])
            for item in self.metadata if item['doc_id'] == doc_id
        ]
        if not pages:
            print(f"⚠️ Document with ID {doc_id} not found.")
            return None
        return sorted(pages, key=lambda x: x[0])  # Sort by page_idx
    


# if __name__=="__main__":
#     method=VectorStoreManager()
#     result = extract_from_pdf("backend/data/EJ1172284.pdf")
#     embedding, metadata = build_faiss_index('doc001',result)
#     method.add_document1('doc001',embedding,metadata)
#     print(method.search(query="what research on mobile done?"))
