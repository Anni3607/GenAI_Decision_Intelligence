
from modules.system_logger import (
    log_event,
    log_error
)

from modules.validator import (
    validate_context
)

from modules.narrative_engine import (
    generate_intelligent_narrative
)

from modules.ai_reasoning import (
    extract_decision_context
)

from modules.confidence_engine import (
    analyze_conflicts
)

from modules.adaptive_questions import (
    generate_adaptive_questions
)

from modules.scoring import (
    map_priorities_to_weights
)

from modules.decision_engine import (
    DecisionEngine
)

from modules.recommendation_engine import (
    generate_recommendation_report
)

import importlib.util
import os


# ==========================================
# LOAD CONFIDENCE MODULE
# ==========================================

PROJECT_ROOT = "/content/drive/MyDrive/GenAI_Decision_Intelligence"

module_path = os.path.join(
    PROJECT_ROOT,
    "modules/confidence_score.py"
)

spec = importlib.util.spec_from_file_location(
    "confidence_score",
    module_path
)

confidence_module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(confidence_module)

estimate_decision_confidence = (
    confidence_module.estimate_decision_confidence
)


# ==========================================
# FILTER VALID CRITERIA
# ==========================================

def filter_valid_priorities(
    priorities,
    valid_criteria
):

    log_event("Decision analysis pipeline started.")

    filtered = {}

    for key, value in priorities.items():

        if key in valid_criteria:

            filtered[key] = value

    return filtered


# ==========================================
# MASTER PIPELINE
# ==========================================

def run_decision_analysis(
    user_input,
    options,
    benefit_criteria,
    cost_criteria
):

    # ======================================
    # VALID CRITERIA
    # ======================================

    valid_criteria = (
        benefit_criteria
        +
        cost_criteria
    )

    # ======================================
    # STEP 1: AI EXTRACTION
    # ======================================

    context = extract_decision_context(
        user_input
    )

    # ======================================
    # VALIDATION LAYER
    # ======================================

    context = validate_context(
        context
    )

    # ======================================
    # FILTER PRIORITIES
    # ======================================

    context["priorities"] = (
        filter_valid_priorities(
            context.get(
                "priorities",
                {}
            ),
            valid_criteria
        )
    )

    # ======================================
    # STEP 2: CONFLICT ANALYSIS
    # ======================================

    conflicts = analyze_conflicts(
        context
    )

    context["decision_conflicts"] = conflicts

    # ======================================
    # STEP 3: ADAPTIVE QUESTIONS
    # ======================================

    questions = generate_adaptive_questions(
        context
    )

    # ======================================
    # STEP 4: WEIGHT GENERATION
    # ======================================

    weights = map_priorities_to_weights(
        context["priorities"]
    )

    # ======================================
    # STEP 5: MCDA ENGINE
    # ======================================

    engine = DecisionEngine(

        options=options,

        weights=weights,

        benefit_criteria=benefit_criteria,

        cost_criteria=cost_criteria
    )

    ranked_results = engine.rank_options()

    # ======================================
    # STEP 6: CONFIDENCE
    # ======================================

    confidence = estimate_decision_confidence(
        context
    )

    # ======================================
    # STEP 7: FINAL REPORT
    # ======================================

    report = generate_recommendation_report(
        ranked_results,
        context
    )

    # ======================================
    # STEP 8: NARRATIVE SYNTHESIS
    # ======================================

    narrative = generate_intelligent_narrative(

        context=context,

        ranked_results=ranked_results,

        conflicts=conflicts,

        confidence=confidence
    )

    # ======================================
    # RETURN OUTPUT
    # ======================================

    return {

        "context": context,

        "conflicts": conflicts,

        "questions": questions,

        "weights": weights,

        "ranked_results": ranked_results,

        "confidence": confidence,

        "report": report,

        "narrative": narrative
    }
