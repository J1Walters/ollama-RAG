import psycopg2
from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore

class VectorDB():
    def __init__(self, db_name='vector_db', db_url=None):
        self.db_name = db_name
        self.db_url = db_url

    def make(self):
        """Make the new database and turn it into a vector store"""
        # Create new database
        self.__create_db()
        # Create vector store and return
        return self.__create_vector_store()


    def __create_db(self):
        """Create the new database"""
        conn = psycopg2.connect(self.db_url)
        conn.autocommit = True

        with conn.cursor() as c:
            c.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
            c.execute(f'CREATE DATABASE {self.db_name}')

    def __create_vector_store(self):
        """Create the vector store from the new database"""
        url = make_url(self.db_url)
        vector_store = PGVectorStore.from_params(
            database=self.db_name,
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            table_name='my_rag',
            embed_dim=8192
        )
        return vector_store
