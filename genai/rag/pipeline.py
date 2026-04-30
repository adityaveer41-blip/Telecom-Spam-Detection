import os 
import sys
import requests
import chromadb
from chromadb.utils import embedding_functions

#Importing Knowledge Base
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from knowledge_base import DOCUMENTS

#STEP 1 - ChromaDB Setup

BASE_DIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_PATH= os.path.join(BASE_DIR, 'data', 'chromadb')

#Sentence Transformer - text to vectors me conversion
embedding_fn= embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client= chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="telecom_fraud_knowledge",
    embedding_function=embedding_fn,
)

print(f" ChromaDB initialized at: {CHROMA_PATH}")

#STEP 2- Documents Load Karo
def load_documents():
    """
    Knowldege Base documents ChromaDB me store karo
    Agar already stored hai toh skip karo
    """
    existing = collection.count()
    if existing > 0:
        print(f" Knowledge base alrady loaded:{existing}documents")
        return
    
    #Documents add karo
    print("Loading knowledge base into ChromaDB...")

    ids= [doc['id'] for doc in DOCUMENTS]
    texts= [doc['content'] for doc in DOCUMENTS]
    metadatas= [{'title': doc['title'], 'id': doc['id']} for doc in DOCUMENTS]

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )
    print(f"LOADED{len(DOCUMENTS)} documents into ChromaDB")


#STEP 3 - QUERY FUNCTION
def query_knowldege_base(question: str, n_results:int=3) -> list:
    """
    Question ke basis pe relevant documents dhundo
    Input: analyst ka question
    Qutput: list of relevant document chunks
    """
    results= collection.query(
        query_texts= [question],
        n_results=n_results
    )

    #Results format karo
    documents= results['documents'][0]
    metadatas= results['metadatas'][0]

    relevant_chunks =[]
    for doc, meta in zip(documents, metadatas):
        relevant_chunks.append({
            'title': meta['title'],
            'content': doc.strip()
        })
    return relevant_chunks

#STEP 4 - RAG Query Function
def rag_query(question:str) -> str:
    """
    Full RAG pipeline - question se accurate answer
    Input: analyst ka question
    Output: llama 3 ka answer(grounded in documents)
    """
    #Step 4a - relevant documents dhundo
    relevant_chunks = query_knowldege_base(question)

    #Step 4b - Context banao
    context=""
    for i, chunk in enumerate(relevant_chunks):
        context += f"\n[Document {i+1}: {chunk['title']}]\n"
        context += chunk['content']
        context += "\n"

    #Step 4c - RAG Prompt banao
    rag_prompt= f""" You are a telecom fraud detection expert with knowledge of TRAI regulations and fraud patterns.
Use ONLY the following documents to answer the question.
If the answer is not in the documents, say "I don't have enough information on this topic."

DOCUMENTS:
{context}

QUESTION: {question}

ANSWER(based on the documents above):"""
    #Step 4c m- llama 3 ko bhejo
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model' : 'llama3',
            'prompt': rag_prompt,
            'stream' : False
        }
    )
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: {response.status_code}"
    

#STEP 5 - Testing

if __name__ == "__main__":
    load_documents()

    print("\n" + "="*50)
    print("RAG PIPELINE - TELECOM FRAUD KNOWLEDGE BASE")
    print("="*50)

    test_questions= [
        "What happens after third TRAI violation?",
        "How to detect robocall fraud from CDR data?",
        "What is International Revenue Share fraud?",
        "What does high CustServ calls indicate in fraud detection?"
    ]

    for question in test_questions:
        print(f"\nQ: {question}")
        print("-"*40)
        answer = rag_query(question)
        print(f"A: {answer}")
        print()


    


