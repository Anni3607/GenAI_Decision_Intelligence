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

    try:

        top_option = ranked_results.iloc[0]["name"]

        if len(ranked_results) > 1:

            second_option = ranked_results.iloc[1]["name"]

            score_gap = round(
                ranked_results.iloc[0]["final_score"]
                -
                ranked_results.iloc[1]["final_score"],
                2
            )

        else:

            second_option = "N/A"

            score_gap = 0

        prompt = f"""
You are an objective decision analyst.

USER GOAL:
{user_input}

TOP RECOMMENDATION:
{top_option}

SECOND BEST OPTION:
{second_option}

SCORE GAP:
{score_gap}

DETECTED CONFLICTS:
{conflicts}

CONFIDENCE:
{confidence}

====================================================

RULES

1. Use ONLY the information provided.

2. Do NOT invent:
- salaries
- statistics
- percentages
- studies
- reports
- surveys
- benchmarks

3. Do NOT mention:
- Glassdoor
- LinkedIn
- Forbes
- McKinsey
- external websites
- external research

4. Be realistic.

5. Mention both strengths and weaknesses.

6. Explain tradeoffs clearly.

7. Explain why the recommendation won.

8. Keep the explanation concise.

9. Never claim facts not present in the provided information.

If the user says:

"I want stability"

then job_security should strongly influence scoring.

If the user says:

"I want a safe career"

then job_security should strongly influence scoring.

If the user says:

"I want long-term security"

then job_security should strongly influence scoring.

====================================================

OUTPUT FORMAT

Strategic Explanation:
(2-4 sentences)

Tradeoff Analysis:
(2-4 sentences)

Why It Ranked Highest:
(2-4 sentences)

Practical Interpretation:
(2-4 sentences)
"""

        response = generate_reasoning(
            prompt
        )

        return response

    except Exception as e:

        return (
            f"Unable to generate narrative. "
            f"Reason: {str(e)}"
        )
