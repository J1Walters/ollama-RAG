import os
from dotenv import load_dotenv
from vector_store import VectorDB
from parser import PDFParser
from config import PDF_DIR_PATH

def main():
    # Load environment variables
    load_dotenv()

    # Get database URL
    DB_URL = os.getenv('DATABASE_URL')

    # Make vector store
    vector_db = VectorDB(db_name='vector_db', db_url=DB_URL).make()


    parser = PDFParser(PDF_DIR_PATH)
    parser.parse()
    parser.embed()
    parser.save(vector_store=vector_db)

if __name__ == '__main__':
    main()
