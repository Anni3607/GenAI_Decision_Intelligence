import json
import re
from groq import Groq
import streamlit as st

# =====================================================
# API CONFIG
# =====================================================

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "llama-3.3-70b-versatile"

# =====================================================
# AI OPTION EVALUATION
# =====================================================

def evaluate_options(domain, options, criteria, user_input="", **kwargs):

    # Standardize the input criteria structure to match exactly
    criteria_list = [c.lower().strip() for c in criteria]

    prompt = f"""
You are a realistic decision intelligence engine.

Your job is to evaluate options realistically,
comparatively,
and according to the user's priorities.

=====================================================

DOMAIN:
{domain}

USER PRIORITIES:
{user_input}

OPTIONS:
{options}

CRITERIA:
{criteria_list}

=====================================================

IMPORTANT RULES

1. Use scores from 1-10.

2. Compare options AGAINST EACH OTHER.

3. Do NOT evaluate options independently.

4. Every option must have strengths.

5. Every option must have weaknesses.

6. User priorities matter.

If the user explicitly states a goal,
that goal should strongly influence evaluation.

=====================================================

ANTI-BIAS RULES
Do NOT assume brand premium always wins. Evaluate purely on merit.

=====================================================

SCORING GUIDELINES
1-3 = poor
4-6 = average
7-8 = strong
9 = exceptional
10 = extremely rare

=====================================================

Return VALID JSON ONLY. Do not wrap it in anything other than clean JSON structures.
The object keys for the criteria MUST exactly match this exact list lowercase: {criteria_list}

FORMAT:
{{
    "Option Name": {{
        "criterion_key": score
    }}
}}
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.15,
            max_tokens=1500
        )

        response = completion.choices[0].message.content.strip()

        # Robustly extract JSON even if enclosed in markdown code fences ```json ... ```
        if "```" in response:
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        
        # Clean regex to find the primary outermost JSON bounding bracket
        json_match = re.search(r"\{.*\}", response, re.DOTALL)

        if json_match:
            parsed = json.loads(json_match.group())
            cleaned_parsed = {}

            for option_name, scores in parsed.items():
                cleaned_scores = {}
                
                # Normalize keys to lowercase so app.py doesn't miss match variables
                for criterion, score in scores.items():
                    norm_criterion = criterion.lower().strip()
                    
                    try:
                        score_val = float(score)
                    except:
                        score_val = 5

                    score_val = max(1, min(10, score_val))
                    cleaned_scores[norm_criterion] = round(score_val)
                
                # Backfill any missing metrics just in case LLM missed one
                for orig_criterion in criteria:
                    if orig_criterion.lower().strip() not in cleaned_scores:
                        cleaned_scores[orig_criterion.lower().strip()] = 5

                cleaned_parsed[option_name] = cleaned_scores

            return cleaned_parsed

        return {}

    except Exception as e:
        # Also print to Streamlit logs for debugging clarity
        st.sidebar.error(f"Groq API Call Error: {str(e)}")
        return {}
