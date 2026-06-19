from email.mime import text
import os
from pathlib import Path
from urllib import response
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb
from .config import CHUNK_SIZE,CHUNK_OVERLAP
from dotenv import load_dotenv
load_dotenv()

class LocalRAGPipeline:
    def __init__(self,db_dir='./chroma_db'):
        self.client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        self.chroma=chromadb.PersistentClient(path=db_dir)
        self.collection=self.chroma.get_or_create_collection('support_kb')

    def embedding(self, text):
        response = self.client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

        return response.embeddings[0].values

    def load_documents(self,data_dir='data'):
        docs=[]
        for p in Path(data_dir).glob('*'):
            if p.suffix in ['.txt','.md']:
                docs.append((p.name,p.read_text(encoding='utf-8')))
            elif p.suffix=='.pdf':
                txt=''
                reader=PdfReader(str(p))
                for page in reader.pages:
                    txt += (page.extract_text() or '') + '\n'
                docs.append((p.name,txt))
        return docs

    def ingest_all(self,data_dir='data'):
        splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
        for name,text in self.load_documents(data_dir):
            for i,chunk in enumerate(splitter.split_text(text)):
                self.collection.add(
                    ids=[f'{name}_{i}'],
                    embeddings=[self.embedding(chunk)],
                    documents=[chunk],
                    metadatas=[{'source':name}]
                )

    def retrieve(self,query,top_k=3):
        q=self.embedding(query)
        res=self.collection.query(query_embeddings=[q],n_results=top_k)
        items=[]
        for i,doc in enumerate(res['documents'][0]):
            dist=res['distances'][0][i] if res.get('distances') else 0
            items.append({
                'text':doc,
                'source':res['metadatas'][0][i]['source'],
                'score':1-dist
            })
        return items
