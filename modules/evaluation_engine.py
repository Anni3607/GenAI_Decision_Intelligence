
import json
import pandas as pd

from modules.master_pipeline import (
    run_decision_analysis
)


def evaluate_system(

    test_cases,
    options,
    benefit_criteria,
    cost_criteria
):

    evaluations = []

    for case in test_cases:

        try:

            results = run_decision_analysis(

                user_input=case["input"],

                options=options,

                benefit_criteria=benefit_criteria,

                cost_criteria=cost_criteria
            )

            evaluation = {

                "test_case": case["name"],

                "recommended_option":
                    results["ranked_results"].iloc[0]["name"],

                "confidence":
                    results["confidence"],

                "num_conflicts":
                    len(results["conflicts"]),

                "num_questions":
                    len(results["questions"]),

                "narrative_length":
                    len(results["narrative"])
            }

            evaluations.append(
                evaluation
            )

        except Exception as e:

            evaluations.append({

                "test_case": case["name"],

                "error": str(e)
            })

    return pd.DataFrame(
        evaluations
    )
