# Pydantic Models — Input/Output Schemas
from pydantic import BaseModel, Field
from typing import Optional

# INPUT SCHEMAS

class CDRInput(BaseModel):
    """
    Raw CDR data — ye analyst API ko bhejega
    Har field ka type aur description defined hai
    """
    Account_Length: float = Field(..., description="Account age in days")
    VMail_Message: float = Field(..., description="Number of voicemail messages")
    Day_Mins: float = Field(..., description="Total daytime minutes")
    Day_Calls: float = Field(..., description="Total daytime calls")
    Day_Charge: float = Field(..., description="Total daytime charge")
    Eve_Mins: float = Field(..., description="Total evening minutes")
    Eve_Calls: float = Field(..., description="Total evening calls")
    Eve_Charge: float = Field(..., description="Total evening charge")
    Night_Mins: float = Field(..., description="Total night minutes")
    Night_Calls: float = Field(..., description="Total night calls")
    Night_Charge: float = Field(..., description="Total night charge")
    Intl_Mins: float = Field(..., description="Total international minutes")
    Intl_Calls: float = Field(..., description="Total international calls")
    Intl_Charge: float = Field(..., description="Total international charge")
    CustServ_Calls: float = Field(..., description="Number of customer service calls")

    def to_raw_dict(self) -> dict:
        """
        Pydantic model ko raw CDR dict mein convert karo
        Underscore → Space (model ke feature names match karne ke liye)
        """
        return {
            'Account Length': self.Account_Length,
            'VMail Message': self.VMail_Message,
            'Day Mins': self.Day_Mins,
            'Day Calls': self.Day_Calls,
            'Day Charge': self.Day_Charge,
            'Eve Mins': self.Eve_Mins,
            'Eve Calls': self.Eve_Calls,
            'Eve Charge': self.Eve_Charge,
            'Night Mins': self.Night_Mins,
            'Night Calls': self.Night_Calls,
            'Night Charge': self.Night_Charge,
            'Intl Mins': self.Intl_Mins,
            'Intl Calls': self.Intl_Calls,
            'Intl Charge': self.Intl_Charge,
            'CustServ Calls': self.CustServ_Calls,
        }


class QueryInput(BaseModel):
    """
    RAG query input — analyst ka question
    """
    question: str = Field(..., description="Natural language question about fraud or TRAI regulations")
    n_results: Optional[int] = Field(3, description="Number of documents to retrieve")


# OUTPUT SCHEMAS

class ScoreResponse(BaseModel):
    """
    /score endpoint ka output
    """
    fraud_probability: float = Field(..., description="Fraud probability 0-1")
    fraud_percentage: float = Field(..., description="Fraud probability as percentage")
    is_fraud: bool = Field(..., description="True if fraud probability > 0.3")
    risk_level: str = Field(..., description="LOW / MEDIUM / HIGH / CRITICAL")
    top_features: dict = Field(..., description="Top 5 contributing features")
    message: str = Field(..., description="Human readable status message")


class ExplainResponse(BaseModel):
    """
    /explain endpoint ka output
    """
    fraud_probability: float
    fraud_percentage: float
    is_fraud: bool
    risk_level: str
    top_features: dict
    explanation: str = Field(..., description="LLM generated plain English explanation")
    judge_score: Optional[str] = Field(None, description="LLM-as-Judge quality verdict")


class QueryResponse(BaseModel):
    """
    /query endpoint ka output
    """
    question: str
    answer: str = Field(..., description="RAG grounded answer from knowledge base")
    sources: list = Field(..., description="Document titles used to answer")


class HealthResponse(BaseModel):
    """
    /health endpoint ka output
    """
    status: str
    model_loaded: bool
    chromadb_documents: int
    ollama_status: str
    message: str