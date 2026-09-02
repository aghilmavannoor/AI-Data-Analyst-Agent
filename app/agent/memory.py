# app/agent/memory.py

import re


# ==========================================
# 1. E-COMMERCE CATEGORIES
# ==========================================

CATEGORIES = [
    "laptop",
    "smartphone",
    "tablet",
    "accessories",
    "audio",
    "wearable",
    "storage",
    "networking",
    "office"
]


# ==========================================
# 2. REGIONS
# ==========================================

REGIONS = [
    "north",
    "south",
    "east",
    "west",
    "central"
]


# ==========================================
# 3. GET PREVIOUS USER QUESTION
# ==========================================

def get_previous_question(messages):

    if not messages:
        return None

    for message in reversed(messages):

        if message.get("role") == "user":

            content = message.get(
                "content",
                ""
            ).strip()

            if content:
                return content

    return None


# ==========================================
# 4. GET PREVIOUS ASSISTANT ANSWER
# ==========================================

def get_previous_answer(messages):

    if not messages:
        return None

    for message in reversed(messages):

        if message.get("role") == "assistant":

            content = message.get(
                "content",
                ""
            ).strip()

            if content:
                return content

    return None


# ==========================================
# 5. EXTRACT YEAR
# ==========================================

def extract_year(question):

    if not question:
        return None

    match = re.search(
        r"\b(20\d{2})\b",
        question
    )

    if match:
        return match.group(1)

    return None


# ==========================================
# 6. EXTRACT CATEGORY
# ==========================================

def extract_category(question):

    if not question:
        return None

    question_lower = question.lower()

    for category in CATEGORIES:

        if re.search(
            rf"\b{re.escape(category)}\b",
            question_lower
        ):
            return category

    return None


# ==========================================
# 7. EXTRACT REGION
# ==========================================

def extract_region(question):

    if not question:
        return None

    question_lower = question.lower()

    for region in REGIONS:

        if re.search(
            rf"\b{re.escape(region)}\b",
            question_lower
        ):
            return region

    return None


# ==========================================
# 8. EXTRACT TOP N
# ==========================================

def extract_top_n(question):

    if not question:
        return None

    match = re.search(
        r"\btop\s+(\d+)\b",
        question.lower()
    )

    if match:
        return int(
            match.group(1)
        )

    return None


# ==========================================
# 9. DETECT CHART REQUEST
# ==========================================

def is_chart_request(question):

    if not question:
        return False

    q = question.lower()

    chart_phrases = [
        "chart",
        "graph",
        "plot",
        "visualize",
        "visualization",
        "as a chart",
        "as a graph",
        "show it as",
        "display it"
    ]

    return any(
        phrase in q
        for phrase in chart_phrases
    )


# ==========================================
# 10. DETECT FOLLOW-UP
# ==========================================

def is_follow_up(question):

    if not question:
        return False

    q = question.lower().strip()

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        q
    )


    # --------------------------------------
    # Pronouns
    # --------------------------------------

    pronouns = [
        "it",
        "its",
        "they",
        "them",
        "their",
        "that",
        "those",
        "this",
        "these",
        "same"
    ]

    if any(
        word in words
        for word in pronouns
    ):
        return True


    # --------------------------------------
    # Follow-up phrases
    # --------------------------------------

    phrases = [
        "what about",
        "how about",
        "and what about",
        "and how about",
        "show it",
        "display it",
        "plot it",
        "chart it",
        "make it a chart",
        "make that a chart",
        "as a chart",
        "as a graph",
        "last year",
        "previous year",
        "next year",
        "same for",
        "same with"
    ]

    for phrase in phrases:

        if phrase in q:
            return True


    # --------------------------------------
    # Top N
    # --------------------------------------

    if re.search(
        r"\btop\s+\d+\b",
        q
    ):
        return True


    # --------------------------------------
    # Short contextual questions
    # --------------------------------------

    if len(words) <= 4:

        if (
            extract_year(question)
            or extract_category(question)
            or extract_region(question)
            or extract_top_n(question)
            or "chart" in words
            or "graph" in words
            or "compare" in words
        ):
            return True


    return False


# ==========================================
# 11. FIND BASE QUESTION
# ==========================================

def get_base_question(messages):

    """
    Find the most recent substantive question.

    Example:

        Show revenue by category.
        What about 2025?
        What about Laptop?

    Base question remains:

        Show revenue by category.
    """

    if not messages:
        return None

    user_questions = []

    for message in messages:

        if message.get("role") != "user":
            continue

        content = message.get(
            "content",
            ""
        ).strip()

        if content:
            user_questions.append(
                content
            )


    if not user_questions:
        return None


    # --------------------------------------
    # Search backwards for a non-follow-up
    # --------------------------------------

    for question in reversed(
        user_questions
    ):

        if not is_follow_up(question):

            return question


    # --------------------------------------
    # If everything is a follow-up,
    # use the oldest user question.
    # --------------------------------------

    return user_questions[0]


# ==========================================
# 12. GET CONVERSATION CONTEXT
# ==========================================

def get_conversation_context(messages):

    """
    Extract the accumulated context from
    the conversation.

    Returns:

        base_question
        year
        category
        region
        top_n
    """

    base_question = get_base_question(
        messages
    )

    if not base_question:

        return {
            "base_question": None,
            "year": None,
            "category": None,
            "region": None,
            "top_n": None
        }


    # --------------------------------------
    # Start with values from base question
    # --------------------------------------

    year = extract_year(
        base_question
    )

    category = extract_category(
        base_question
    )

    region = extract_region(
        base_question
    )

    top_n = extract_top_n(
        base_question
    )


    # --------------------------------------
    # Apply later follow-up information
    # --------------------------------------

    for message in messages:

        if message.get("role") != "user":
            continue

        question = message.get(
            "content",
            ""
        ).strip()

        if not question:
            continue

        # Ignore the base question itself
        if question == base_question:
            continue


        current_year = extract_year(
            question
        )

        current_category = extract_category(
            question
        )

        current_region = extract_region(
            question
        )

        current_top_n = extract_top_n(
            question
        )


        # ----------------------------------
        # Update accumulated context
        # ----------------------------------

        if current_year:
            year = current_year

        if current_category:
            category = current_category

        if current_region:
            region = current_region

        if current_top_n:
            top_n = current_top_n


    return {
        "base_question": base_question,
        "year": year,
        "category": category,
        "region": region,
        "top_n": top_n
    }


# ==========================================
# 13. CLEAN QUESTION
# ==========================================

def clean_question(question):

    if not question:
        return ""

    question = re.sub(
        r"\s+",
        " ",
        question
    )

    question = question.strip()

    question = re.sub(
        r"\s+\.",
        ".",
        question
    )

    return question


# ==========================================
# 14. RESOLVE FOLLOW-UP
# ==========================================

def resolve_question(question, messages):

    """
    Resolve a follow-up question while preserving
    accumulated conversation context.
    """

    if not question:

        return ""


    question = question.strip()


    # ======================================
    # NO HISTORY
    # ======================================

    if not messages:

        return question


    # ======================================
    # NOT FOLLOW-UP
    # ======================================

    if not is_follow_up(question):

        return question


    # ======================================
    # GET ACCUMULATED CONTEXT
    # ======================================

    context = get_conversation_context(
        messages
    )


    base_question = context[
        "base_question"
    ]

    year = context[
        "year"
    ]

    category = context[
        "category"
    ]

    region = context[
        "region"
    ]

    top_n = context[
        "top_n"
    ]


    if not base_question:

        return question


    # ======================================
    # CURRENT VALUES
    # ======================================

    current_year = extract_year(
        question
    )

    current_category = extract_category(
        question
    )

    current_region = extract_region(
        question
    )

    current_top_n = extract_top_n(
        question
    )


    # ======================================
    # UPDATE CONTEXT
    # ======================================

    if current_year:

        year = current_year


    if current_category:

        category = current_category


    if current_region:

        region = current_region


    if current_top_n:

        top_n = current_top_n


    # ======================================
    # LAST YEAR
    # ======================================

    q_lower = question.lower()

    if (
        "last year" in q_lower
        or "previous year" in q_lower
    ):

        if year:

            try:

                year = str(
                    int(year) - 1
                )

            except ValueError:

                pass


    # ======================================
    # NEXT YEAR
    # ======================================

    if "next year" in q_lower:

        if year:

            try:

                year = str(
                    int(year) + 1
                )

            except ValueError:

                pass


    # ======================================
    # BUILD RESOLVED QUESTION
    # ======================================

    resolved = clean_question(
        base_question
    )


    # --------------------------------------
    # Add year
    # --------------------------------------

    if year:

        if not extract_year(resolved):

            resolved = (
                f"{resolved.rstrip('.!? ')} "
                f"for {year}."
            )


        else:

            resolved = re.sub(
                r"\b20\d{2}\b",
                year,
                resolved
            )


    # --------------------------------------
    # Add category
    # --------------------------------------

    if category:

        existing_category = (
            extract_category(resolved)
        )

        if existing_category:

            if existing_category != category:

                resolved = re.sub(
                    rf"\b{re.escape(existing_category)}\b",
                    category,
                    resolved,
                    flags=re.IGNORECASE
                )

        else:

            resolved = (
                f"{resolved.rstrip('.!? ')} "
                f"for the {category} category."
            )


    # --------------------------------------
    # Add region
    # --------------------------------------

    if region:

        existing_region = (
            extract_region(resolved)
        )

        if not existing_region:

            resolved = (
                f"{resolved.rstrip('.!? ')} "
                f"for the {region} region."
            )


    # --------------------------------------
    # Add top N
    # --------------------------------------

    if top_n:

        existing_top_n = extract_top_n(
            resolved
        )

        if existing_top_n:

            resolved = re.sub(
                r"\btop\s+\d+\b",
                f"top {top_n}",
                resolved,
                flags=re.IGNORECASE
            )

        else:

            resolved = (
                f"{resolved.rstrip('.!? ')} "
                f"showing the top {top_n} results."
            )


    # ======================================
    # CHART REQUEST
    # ======================================

    if is_chart_request(question):

        resolved = (
            f"{resolved.rstrip('.!? ')} "
            f"and display the result as a chart."
        )


    # ======================================
    # FINAL CLEANUP
    # ======================================

    return clean_question(
        resolved
    )


# ==========================================
# 15. TEST MEMORY
# ==========================================

if __name__ == "__main__":

    print("=" * 70)
    print("CONVERSATION MEMORY TEST")
    print("=" * 70)


    # --------------------------------------
    # Step 1
    # --------------------------------------

    messages = []

    q1 = "Show revenue by category."

    print()
    print("USER:")
    print(q1)

    resolved = resolve_question(
        q1,
        messages
    )

    print("RESOLVED:")
    print(resolved)

    messages.append(
        {
            "role": "user",
            "content": q1
        }
    )


    # --------------------------------------
    # Step 2
    # --------------------------------------

    q2 = "What about 2025?"

    print()
    print("USER:")
    print(q2)

    resolved = resolve_question(
        q2,
        messages
    )

    print("RESOLVED:")
    print(resolved)

    messages.append(
        {
            "role": "user",
            "content": q2
        }
    )


    # --------------------------------------
    # Step 3
    # --------------------------------------

    q3 = "What about Laptop?"

    print()
    print("USER:")
    print(q3)

    resolved = resolve_question(
        q3,
        messages
    )

    print("RESOLVED:")
    print(resolved)

    messages.append(
        {
            "role": "user",
            "content": q3
        }
    )


    # --------------------------------------
    # Step 4
    # --------------------------------------

    q4 = "Show it as a chart."

    print()
    print("USER:")
    print(q4)

    resolved = resolve_question(
        q4,
        messages
    )

    print("RESOLVED:")
    print(resolved)


    print()
    print("=" * 70)