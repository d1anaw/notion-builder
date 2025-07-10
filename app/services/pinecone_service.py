from pinecone import Pinecone, ServerlessSpec
from app.services.openai_service import get_embedding
import os

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
pinecone = Pinecone(api_key=PINECONE_API_KEY)

EMBEDDING_DIMENSION = 1536

def embed_chunks_and_upload(chunks, index_name):
    print("Creating a new index:", index_name)
    if pinecone.has_index(index_name):
        print("Index already exists. Deleting index...")
        pinecone.delete_index(name=index_name)
    pinecone.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            vector_type="dense",
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    index = pinecone.Index(index_name)
    print("Embedding chunks using OpenAI...")

    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))
    print("Uploading chunks to Pinecone")
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text
               in embeddings_with_ids]
    index.upsert(vectors=upserts)

    print(f"Uploaded {len(chunks)} chunks to pinecone index {index_name}")

def get_most_similar_chunks(query, index_name):
    question_embedding = get_embedding(query)
    index = pinecone.Index(index_name)
    query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True)
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks

