#/SCORE ENDPOINT — CDR data leke, fraud score dena
from fastapi import APIRouter, HTTPException
import sys
import os

# genai/ folder path add karo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'genai'))

# api/ folder path add karo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from explainer import get_fraud_score
from models import CDRInput, ScoreResponse

#ROUTER
router = APIRouter()
def get_risk_level(probability: float) -> str:
    """
    Fraud Probability -> risk level string
    """
    if probability < 0.3:
        return "LOW"
    elif probability < 0.5:
        return"MEDIUM"
    elif probability < 0.7:
        return "HIGH"
    else:
        return "CRITICAL"
    

def get_message(is_fraud: bool, risk_level: str) -> str:
    """
    is_fraud + risk_level -> human readable message
    """
    if not is_fraud:
        return "No fraud indicators detected. Account appears Legitimate."
    else:
        return f"Fraud indicators detected. Risk level: {risk_level}. Manual review recommended."
    

@router.post("/score", response_model= ScoreResponse)
async def score_cdr(cdr: CDRInput):
    """
    CDR data lo aur fraud probability return karo.
    explainer.py ka get_fraud_score() call hota hai yahan.
    """
    try:
        # Step 1 - CDRInput ko raw dict mein convert karo
        # (models.py mein yo_raw_dict() method banaya tha)
        raw_data= cdr.to_raw_dict()

        # Step 2 - fraud score nikalo
        result= get_fraud_score(raw_data)

        # Step 3 - risk level aur message banao
        risk_level= get_risk_level(result['fraud_probability'])
        message= get_message(result['is_fraud'], risk_level)

        # Step 4 - ScoreResponse return karo
        return ScoreResponse(
            fraud_probability= result['fraud_probability'],
            fraud_percentage= round(result['fraud_probability'] * 100,1),
            is_fraud= result['is_fraud'],
            risk_level= risk_level,
            top_features= result['top_features'],
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))

