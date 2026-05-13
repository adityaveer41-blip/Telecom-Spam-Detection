#/query endpoint - RAG pipeline se knowledge base query karo 
from fastapi import APIRouter, HTTPException
import sys 
import os 

# genai/rag/folder path add karo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'genai', 'rag'))

#api/folder path add karo 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pipeline import rag_query, load_documents, query_knowldege_base
from models import QueryInput, QueryResponse

# Router
router = APIRouter()

# App start hote hi documents load karo
load_documents()

@router.post("/query", response_model= QueryResponse)
async def query_rag(query: QueryInput):
    """
    Analyst ka question lo aur RAG pipeline se answer do.
    ChromaDB se relevant documents dhundh ke LLM se answer generate hota hai.
    """
    try:
        #Step 1 - LLM se answer lo
        answer = rag_query(query.question)

        #Step 2 - Sources bhi nikalao(konse documents use hue)
        chunks = query_knowldege_base(query.question, query.n_results)
        sources = [chunk['title'] for chunk in chunks]

        #Step 3 - QueryResponse return karo
        return QueryResponse(
            question = query.question,
            answer = answer,
            sources = sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))
    
