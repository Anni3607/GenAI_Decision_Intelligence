from modules.ai_reasoning import generate_reasoning


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
        else:
            second_option = "None"

        ranking_table = ranked_results.to_dict(
            orient="records"
        )

        prompt = f"""
You are an intelligent decision advisor.

USER GOAL:
{user_input}

RANKED RESULTS:
{ranking_table}

TOP OPTION:
{top_option}

SECOND OPTION:
{second_option}

CONFLICTS:
{conflicts}

CONFIDENCE:
{confidence}

====================================================

RULES

1. Write naturally.

2. Sound like a smart advisor,
not a corporate consultant.

3. Explain the decision in plain English.

4. Use ONLY information from the ranking data.

5. Never invent:
- salaries
- statistics
- studies
- percentages
- benchmarks
- market reports

6. Never mention:
- score gap
- weighted scoring
- algorithm
- confidence calculations

7. Mention both strengths and weaknesses.

8. Mention what the user gains.

9. Mention what the user sacrifices.

10. Make the recommendation easy to understand.

11. Adapt to ANY domain:
- career
- education
- investment
- food
- fitness
- technology
- fashion
- lifestyle
- travel
- products

12. Keep it concise.

====================================================

OUTPUT FORMAT

## Recommendation

Explain in 3-5 sentences why the top option is the best match.

## Main Advantages

- point
- point
- point

## Trade-Offs

- point
- point
- point

## When You Should Choose It

2-4 sentences.

## When You Should Avoid It

2-4 sentences.
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
