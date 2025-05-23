# embedding.py
import time
import os
from app.core.build_faiss import prepare_pagewise_text,build_faiss_index
from app.core.pdf_to_text import extract_from_pdf
from app.services.vectorstore import VectorStoreManager


def run_embedding_monitor(upload_folder):
    print("📡 Embedding monitor started...")

    processed_files = set()

    while True:
        try:
            all_files = set(os.listdir(upload_folder))
            new_files = all_files - processed_files

            for file in new_files:
                if file.lower().endswith('.pdf'):
                    print(f"🧠 Processing new file: {file}")
                    file_path = os.path.join(upload_folder, file)

                    method=VectorStoreManager()


                    result = extract_from_pdf(file_path)
                    # page_texts = prepare_pagewise_text(result)

                    embedding, metadata = build_faiss_index(f'doc_{file[:-4]}',result)
                    method.add_document(f'doc_{file[:-4]}',embedding,metadata)

                    # method.add_document(f'doc_{file[:-4]}',page_texts)

                    processed_files.add(file)
        except Exception as e:
            print(f"❌ Error in embedding monitor: {e}")
        
        time.sleep(5)  # wait 5 seconds before next check
