import glob
import pymupdf4llm
import re
from config import EMBEDDING_MODEL
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode

class PDFParser():
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.parsed_nodes = None

    def parse(self):
        """Parse all PDF files in directory and convert to markdown"""
        # Get list of files in directory
        files = self.__get_files()

        # Parse and convert every file in directory to markdown
        markdown = self.__convert_to_md(files)

        # Create llamaindex documents from markdown
        docs = self.__make_documents(markdown)

        # Split into nodes
        nodes = self.__split_md_to_nodes(docs)

        # Set parsed nodes attribute
        self.parsed_nodes = nodes

    def embed(self):
        """Make embeddings for parsed nodes and save them to vector storage"""
        if self.parsed_nodes is not None:
            print('Embedding Nodes...')

            for node in self.parsed_nodes:
                node_embedding = EMBEDDING_MODEL.get_text_embedding(node.get_content(metadata_mode='all'))
                node.embedding = node_embedding

        else:
            raise TypeError('Please use the .parse() method first.')

    def __save_embeddings(self):
        """Save embeddings to vector store"""
        

    def __get_files(self):
        """Get list of files in directory"""
        files_to_parse = glob.glob(self.directory_path + '/*.pdf')
        print(files_to_parse)
        return files_to_parse

    def __convert_to_md(self, file_list):
        """Convert files in list to markdown and store content in list"""
        markdown = []

        for file in file_list:
            md_text = pymupdf4llm.to_markdown(file)
            re.sub(r'\\n', ' ', md_text)
            markdown.append(md_text)

        return markdown

    def __make_documents(self, markdown):
        """Create documents from markdown"""
        return [Document(text=t) for t in markdown]

    def __split_md_to_nodes(self, docs):
        """Split documents into nodes"""
        chunks = []
        idxs = []
        nodes = []
        # Split text into chunks and put into list
        splitter = SentenceSplitter(chunk_size=512)

        for idx, doc in enumerate(docs):
            current_chunks = splitter.split_text(doc.text)
            chunks.extend(current_chunks)
            idxs.extend([idx] * len(current_chunks))
        
        # Turn text chunks into nodes
        for idx, chunk in enumerate(chunks):
            node = TextNode(text=chunk)
            src_doc = docs[idxs[idx]]
            node.metadata = src_doc.metadata
            nodes.append(node)

        return nodes

