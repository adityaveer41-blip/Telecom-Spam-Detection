# Explain endpoint - fraud score + LLM Explanation + judge verdict

from fastapi import APIRouter, HTTPException
import sys
import os

#genai/folder path add karo
sys.path.append(os.path.join(os.path.dirname(__file__),'..', '..', 'genai'))

#api/ foldee path add karo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from explainer import get_fraud_score, explain_fraud
from judge import judge_explanation
from models import CDRInput, ExplainResponse

#Router
router = APIRouter()

def get_risk_level(probability: float) -> str:
    """
    Fraud Probability -> risk revel string
    """
    if probability <0.3:
        return "LOW"
    elif probability <0.5:
        return "MEDIUM"
    elif probability <0.7:
        return "HIGH"
    else:
        return "CRITICAL"
    
@router.post("/explain", response_model= ExplainResponse)
async def explain_cdr(cdr: CDRInput):
    """
    CDR data lo aur fraud score + LLM explanation + Judge verdict return karo.
    """
    try:
        #Step 1 - CDRInput ko raw dict mein convert karo
        raw_data = cdr.to_raw_dict()

        #Step 2 - fraud score nikalo
        result = get_fraud_score(raw_data)
        risk_level = get_risk_level(result['fraud_probability'])

        #Step 3 - LLM se explanation lo
        explanation = explain_fraud(raw_data)

        #Step 4 - Judge se quality verdict lo
        judge_result = judge_explanation(raw_data)
        judge_verdict = judge_result.get('judge_verdict', None)

        #STep 5 - ExplainResponse return karo
        return ExplainResponse(
            fraud_probability = result['fraud_probability'],
            fraud_percentage = round(result['fraud_probability']* 100,1),
            is_fraud = result['is_fraud'],
            risk_level = risk_level,
            top_features = result['top_features'],
            explanation =explanation,
            judge_score = judge_verdict
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    