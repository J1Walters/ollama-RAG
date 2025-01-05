from llama_index.embeddings.huggingface import HuggingFaceEmbedding

PDF_DIR_PATH = './files_for_retrieval'
EMBEDDING_MODEL = HuggingFaceEmbedding(model_name='dunzhang/stella_en_400M_v5', trust_remote_code=True)
CHUNK_SIZE = 1024