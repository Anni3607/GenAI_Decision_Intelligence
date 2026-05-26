
from modules.ai_reasoning import (
    generate_reasoning
)

from modules.fact_engine import (
    generate_fact_summary
)


def generate_intelligent_narrative(
    context,
    ranked_results,
    conflicts,
    confidence
):

    best = ranked_results.iloc[0]

    second = ranked_results.iloc[1]

    fact_summary = generate_fact_summary(
        ranked_results
    )

    prompt = f"""

You are an expert AI decision strategist.

IMPORTANT RULES:

- NEVER invent numerical facts
- NEVER change factual labels
- ONLY interpret the provided facts
- DO NOT claim low stress if stress is high
- DO NOT hallucinate metrics
- ONLY discuss implications
- Focus on psychological fit
- Focus on tradeoffs
- Focus on sustainability
- Maximum 250 words

====================================
FACTUAL PROFILE
====================================

Top Option:
{best['name']}

Deterministic Facts:
{fact_summary}

====================================
SECOND OPTION
====================================

{second.to_dict()}

====================================
USER CONTEXT
====================================

{context}

====================================
CONFLICTS
====================================

{conflicts}

====================================
CONFIDENCE
====================================

{confidence}

====================================
TASK
====================================

Generate a grounded recommendation narrative.

ONLY interpret implications from the deterministic facts.

DO NOT invent or alter factual attributes.

"""

    narrative = generate_reasoning(
        prompt
    )

    return narrative
