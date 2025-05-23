import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'backend', 'data')
    EMBEDDING_MODEL='BAAI/bge-base-en-v1.5'     #'all-MiniLM-L6-v2':0.37 accuracy
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
