
def generate_recommendation_report(
    ranked_results,
    context
):

    best = ranked_results.iloc[0]

    second = ranked_results.iloc[1]

    report = f"""
========================================
FINAL DECISION REPORT
========================================

RECOMMENDED OPTION:
{best['name']}

FINAL SCORE:
{round(best['final_score'], 4)}

========================================
WHY THIS OPTION WON
========================================
"""

    # =====================================
    # CONTRIBUTIONS
    # =====================================

    for column in ranked_results.columns:

        if column not in ["name", "final_score"]:

            value = round(best[column], 4)

            report += f"\n- {column}: {value}"

    # =====================================
    # TRADEOFFS
    # =====================================

    report += """

========================================
KEY TRADEOFFS
========================================
"""

    priorities = context.get(
        "priorities",
        {}
    )

    if "salary" in priorities:

        report += "\n- Higher salary may reduce work-life balance."

    if "career_growth" in priorities:

        report += "\n- Aggressive growth environments may increase stress."

    if "flexibility" in priorities:

        report += "\n- High flexibility roles may grow slower."

    # =====================================
    # WHY NOT SECOND OPTION
    # =====================================

    report += f"""

========================================
WHY NOT {second['name'].upper()}
========================================
"""

    differences = {}

    for column in ranked_results.columns:

        if column not in ["name", "final_score"]:

            diff = (
                best[column]
                -
                second[column]
            )

            differences[column] = diff

    weakest = min(
        differences,
        key=differences.get
    )

    report += (
        f"\n{second['name']} performed worse mainly in: "
        f"{weakest}"
    )

    # =====================================
    # OPPORTUNITY COST
    # =====================================

    report += """

========================================
OPPORTUNITY COST ANALYSIS
========================================
"""

    report += (
        "\nChoosing this option may require sacrificing "
        "certain benefits offered by alternative options."
    )

    # =====================================
    # RISK ANALYSIS
    # =====================================

    report += """

========================================
RISK ANALYSIS
========================================
"""

    burnout = context.get(
        "burnout_sensitivity",
        ""
    )

    risk = context.get(
        "risk_tolerance",
        ""
    )

    if burnout == "high":

        report += (
            "\n- Burnout risk should be monitored carefully."
        )

    if risk == "low":

        report += (
            "\n- High uncertainty environments may reduce comfort."
        )

    return report
