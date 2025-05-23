
from app.services.vectorstore import VectorStoreManager
from app.models.gemini_out import model_output

def process_query(query): # filenames
    method=VectorStoreManager()
    docs_out=method.search(query)
    query_ans=model_output(docs_out,query)
    return query_ans
