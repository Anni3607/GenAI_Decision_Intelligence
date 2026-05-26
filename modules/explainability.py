
def generate_detailed_explanation(results, weights):

    best = results.iloc[0]

    text = f"""
BEST OPTION: {best['name']}

FINAL SCORE: {round(best['final_score'], 4)}

WEIGHT CONTRIBUTIONS:
"""

    total_contribution = 0

    for criterion, weight in weights.items():

        contribution = best[criterion] * weight

        total_contribution += contribution

        text += (
            f"\n- {criterion}"
            f" | normalized score: {round(best[criterion],4)}"
            f" | weight: {weight}"
            f" | contribution: {round(contribution,4)}"
        )

    text += f"\n\nTOTAL SCORE: {round(total_contribution,4)}"

    return text
