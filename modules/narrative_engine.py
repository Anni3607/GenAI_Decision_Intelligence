from modules.ai_reasoning import (
    generate_reasoning
)

# =====================================================
# NARRATIVE GENERATION
# =====================================================

def generate_intelligent_narrative(
    user_input,
    ranked_results,
    conflicts,
    confidence
):

    top_option = ranked_results.iloc[0]["name"]

    prompt = f"""
You are an advanced AI decision strategist.

User Context:
{user_input}

Top Recommended Option:
{top_option}

Detected Conflicts:
{conflicts}

Confidence Level:
{confidence}

Generate:
1. A strategic explanation
2. Tradeoff analysis
3. Why this option ranks highest
4. Practical real-world interpretation
"""

    response = generate_reasoning(
        prompt
    )

    return response
