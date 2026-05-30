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

        ranking_data = ranked_results.to_dict(
            orient="records"
        )

        prompt = f"""
You are a practical decision advisor.

USER GOAL:
{user_input}

RANKED RESULTS:
{ranking_data}

TOP OPTION:
{top_option}

SECOND OPTION:
{second_option}

CONFLICTS:
{conflicts}

CONFIDENCE:
{confidence}

=====================================================

RULES

1. Write for normal humans.

2. Be concise.

3. Do NOT sound like:
- consultants
- analysts
- MBA reports
- research papers

4. Use markdown formatting.

5. Use BOLD for important ideas.

6. Use bullet points heavily.

7. Mention:
- strengths
- weaknesses
- tradeoffs

8. Explain WHY the winner won.

9. Explain WHY the others lost.

10. Use ONLY information available in rankings.

11. NEVER invent:
- salaries
- percentages
- studies
- statistics
- market reports
- external facts

12. NEVER mention:
- score gap
- weighted scoring
- algorithms
- calculations

13. If useful, include ONE simple analogy.

Examples:

Career:
"Choosing a government job over a startup is like choosing a stable highway over an adventurous mountain road."

Investment:
"This is like choosing steady progress instead of chasing the highest possible return."

Food:
"This is like choosing long-term health over short-term taste."

Only use an analogy if it genuinely improves understanding.

14. Keep every section short.

15. Maximum:
- 5 bullets per section
- 2-3 sentences per paragraph

=====================================================

OUTPUT FORMAT

# Recommendation

- **Winner:** <option>
- 3-5 bullet points explaining why it won.

# Key Strengths

- Bullet points
- Use bold keywords

# Main Trade-Offs

- Bullet points
- Explain what the user sacrifices

# Why Other Options Ranked Lower

For each remaining option:

### Option Name

- Why it lost
- Where it is still better

# Simple Analogy

(Only if useful)

# Final Verdict

2-4 bullet points.

Focus on helping the user make the decision,
not describing the ranking process.
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
