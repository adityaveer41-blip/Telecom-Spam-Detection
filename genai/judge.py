#LLM as judge
#LLM apni hi explaination evaluate karega 

import requests
import json
import os 
import sys 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from explainer import get_fraud_score, explain_fraud

#JUDGE FUNCTION
def judge_explanation(raw_data: dict) -> dict:
    """
    Fraud explanation ki quality check karo
    Input: dict with raw CDR values
    Output: dict with score + feedback
    """
    #Step 1- Fraud score nikalo
    result= get_fraud_score(raw_data)
    fraud_pct= round(result['fraud_probability']*100,1)
    top_features= result['top_features']

    #Step 2- Explanation generate karo
    explanation= explain_fraud(raw_data)

    #Step 3- Judge prompt karo
    judge_prompt= f""" You are a quality evaluator for a telecom fraud detection system.judge_explanation.

A fraud detetction model produced the following results:
- Fraud Probability: {fraud_pct}%
- Status: {"FRAUD" if result['is_fraud'] else "LEGIT"}
- Top Contributing Features: {json.dumps(top_features, indent=2)}

The system then generated this explanation for a telecom analyst:
"{explanation}"

Please evaluate this explanation on the following crieteria:
1. ACCURACY - Does it correctly reflect the fraud probability and features?
2. CLARITY - Is it easy for a non-technical analyst to understand?
3. SPECIFICITY - Does it mention specific features. and their values?
4. ACTIONABILITY - Does it help the analyst decide what to do next?

Respond ONLY in this exact format:
SCORE: X/5
ACCURACY: [Good/Poor] - [one line reason]
CLARITY: [Good/Poor] - [one line reason]
SPECIFICITY: [Good/Poor] - [one line reason]
ACTIONABILITY: [Good/Poor] - [one line reason]
SUMMARY: [one sentence overall verdict]
"""
    
    #Step 4- LLM ko judge promt bhejo
    response= requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'llama3',
            'prompt': judge_prompt,
            'stream': False
        }
    )

    if response.status_code== 200:
        verdict= response.json()['response']
    else:
        verdict= f"Error: {response.status_code}"

    return{
        'fraud_probability':result['fraud_probability'],
        'is_fraud': result['is_fraud'],
        'explanation': explanation,
        'judge_verdict': verdict

    }

#TESTING 
if __name__ == "__main__":
    fraud_case= {
        'Account Length':82,
        'VMail Message':0,
        'Day Mins':300.3,
        'Day Calls':109,
        'Day Charge':51.05,
        'Eve Mins':181.0,
        'Eve Calls':100,
        'Eve Charge':15.39,
        'Night Mins':270.1,
        'Night Calls':73,
        'Night Charge':12.15,
        'Intl Mins':11.7,
        'Intl Calls':4,
        'Intl Charge':3.16,
        'CustServ Calls':0
    }

print("\n" + "="* 50)
print("LLM-AS-JUDGE - EXPLANATIONQUALITY CHECK")
print("="*50)

result= judge_explanation(fraud_case)

print(f"\nFraud Probability : {result['fraud_probability']*100:.1f}%")
print(f"Is Fraud: {result['is_fraud']}")
print(f"\nGenerated Explanation:\n {result['explanation']}")
print(f"\nJudge Verdict:\n{result['judge_verdict']}")


