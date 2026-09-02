# app/agent/router.py

import re


# ==========================================
# 1. CHART KEYWORDS
# ==========================================

CHART_KEYWORDS = [
    "chart",
    "graph",
    "plot",
    "visualize",
    "visualization",
    "visualisation",
    "display",
    "show as",
    "show it as",
    "trend",
    "over time",
    "monthly trend",
    "line chart",
    "bar chart",
    "pie chart",
    "scatter",
]


# ==========================================
# 2. ANALYSIS KEYWORDS
# ==========================================

ANALYSIS_KEYWORDS = [
    "highest",
    "lowest",
    "best",
    "worst",
    "maximum",
    "minimum",
    "max",
    "min",
    "average",
    "mean",
    "total",
    "sum",
    "count",
    "most",
    "least",
    "top",
    "bottom",
    "rank",
    "ranking",
    "compare",
    "comparison",
    "difference",
    "increase",
    "decrease",
    "growth",
    "decline",
    "percentage",
    "percent",
    "share",
    "proportion",
    "contribution",
]


# ==========================================
# 3. PURE DATA / SQL QUESTIONS
# ==========================================

SQL_KEYWORDS = [
    "show",
    "list",
    "get",
    "give me",
    "display",
    "what is",
    "what are",
    "how many",
    "how much",
    "revenue",
    "sales",
    "orders",
    "customers",
    "products",
    "quantity",
    "units",
]


# ==========================================
# 4. HELPER
# ==========================================

def contains_keyword(question, keywords):
    """
    Check whether the question contains
    any keyword or phrase.
    """

    question = question.lower().strip()

    for keyword in keywords:

        if keyword in question:
            return True

    return False


# ==========================================
# 5. DETECT CHART REQUEST
# ==========================================

def is_chart_question(question):
    """
    Determine whether the user explicitly
    requests a visualization.
    """

    return contains_keyword(
        question,
        CHART_KEYWORDS
    )


# ==========================================
# 6. DETECT ANALYSIS REQUEST
# ==========================================

def is_analysis_question(question):
    """
    Determine whether the question requires
    analytical processing.
    """

    question = question.lower().strip()

    # --------------------------------------
    # Comparison
    # --------------------------------------

    if (
        "compare" in question
        or "comparison" in question
        or "versus" in question
        or re.search(r"\bvs\.?\b", question)
    ):
        return True


    # --------------------------------------
    # Ranking / Top N
    # --------------------------------------

    if re.search(
        r"\btop\s+\d+",
        question
    ):
        return True

    if re.search(
        r"\bbottom\s+\d+",
        question
    ):
        return True


    # --------------------------------------
    # Analytical keywords
    # --------------------------------------

    return contains_keyword(
        question,
        ANALYSIS_KEYWORDS
    )


# ==========================================
# 7. DETECT SQL QUESTION
# ==========================================

def is_sql_question(question):
    """
    Determine whether the question requires
    database retrieval.
    """

    return contains_keyword(
        question,
        SQL_KEYWORDS
    )


# ==========================================
# 8. MAIN ROUTER
# ==========================================

def route_question(question):
    """
    Route a natural-language question
    through the appropriate agent tools.

    Possible routes:

        SQL
        SQL,ANALYSIS
        SQL,CHART
        SQL,ANALYSIS,CHART
    """

    if not question:

        return "SQL"


    question = question.strip()

    if not question:

        return "SQL"


    # ======================================
    # CHART
    # ======================================

    chart_required = is_chart_question(
        question
    )


    # ======================================
    # ANALYSIS
    # ======================================

    analysis_required = is_analysis_question(
        question
    )


    # ======================================
    # BUILD ROUTE
    # ======================================

    route = ["SQL"]


    if analysis_required:

        route.append("ANALYSIS")


    if chart_required:

        route.append("CHART")


    return ",".join(route)


# ==========================================
# 9. DEBUG HELPER
# ==========================================

def explain_route(question):
    """
    Return routing information useful for
    debugging and testing.
    """

    return {
        "question": question,
        "sql": True,
        "analysis": is_analysis_question(
            question
        ),
        "chart": is_chart_question(
            question
        ),
        "route": route_question(
            question
        )
    }


# ==========================================
# 10. TEST
# ==========================================

if __name__ == "__main__":

    test_questions = [

        "What is the total revenue?",

        "Show revenue by category.",

        "Which category generated the highest revenue?",

        "Which product sold the most units?",

        "Show monthly revenue.",

        "Show monthly revenue as a chart.",

        "Show the top 5 products by revenue as a chart.",

        "Compare Laptop and Smartphone revenue.",

        "Compare Laptop and Smartphone revenue as a chart.",

        "What percentage of total revenue came from Laptop?",

    ]


    print("=" * 60)

    print("ROUTER TEST")

    print("=" * 60)


    for question in test_questions:

        result = explain_route(
            question
        )

        print()

        print(
            f"Question: {question}"
        )

        print(
            f"Route: {result['route']}"
        )

    print()

    print("=" * 60)