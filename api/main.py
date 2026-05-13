# main.py — FastAPI app ka entry point
# Saare routes yahan jodenge aur app start karenge

from fastapi import FastAPI
from api.routes import scoring_router, explain_router, rag_router

# App banao
app = FastAPI(
    title="Telecom Fraud Detection API",
    description="CDR data se fraud detect karo + RAG knowledge base query karo",
    version="1.0.0"
)

# Saare routers register karo
app.include_router(scoring_router, tags=["Scoring"])
app.include_router(explain_router, tags=["Explanation"])
app.include_router(rag_router,     tags=["RAG Query"])


# Health check
@app.get("/")
async def root():
    return {"message": "Telecom Fraud Detection API is running!"}