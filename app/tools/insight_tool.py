import re
import pandas as pd


# ==========================================
# 1. FORMAT VALUES
# ==========================================

def format_value(value, column_name=""):
    """
    Format numeric values based on the column name.
    """

    if pd.isna(value):
        return "N/A"

    if pd.api.types.is_number(value):

        column_lower = column_name.lower()

        monetary_words = [
            "revenue",
            "price",
            "sales",
            "amount",
            "income",
            "profit"
        ]

        count_words = [
            "count",
            "orders",
            "quantity",
            "units",
            "number"
        ]

        # --------------------------------------
        # Percentage
        # --------------------------------------

        if (
            "percentage" in column_lower
            or "percent" in column_lower
            or column_lower.endswith("_pct")
            or column_lower.endswith("_percentage")
        ):

            return f"{value:.2f}%"

        # --------------------------------------
        # Monetary values
        # --------------------------------------

        if any(
            word in column_lower
            for word in monetary_words
        ):

            return f"₹{value:,.0f}"

        # --------------------------------------
        # Counts / units
        # --------------------------------------

        if any(
            word in column_lower
            for word in count_words
        ):

            return f"{value:,.0f}"

        # --------------------------------------
        # Other numeric values
        # --------------------------------------

        if float(value).is_integer():

            return f"{value:,.0f}"

        return f"{value:,.2f}"

    return str(value)


# ==========================================
# 2. DETECT QUESTION TYPE
# ==========================================

def get_question_type(question):
    """
    Detect the type of analytical question.
    """

    q = question.lower()

    # --------------------------------------
    # Comparison
    # --------------------------------------

    if (
        "compare" in q
        or "versus" in q
        or " vs " in f" {q} "
    ):

        return "comparison"

    # --------------------------------------
    # Percentage / Share
    # --------------------------------------

    if (
        "percentage" in q
        or "percent" in q
        or "share" in q
        or "proportion" in q
    ):

        return "percentage"

    # --------------------------------------
    # Growth / Change
    # --------------------------------------

    if (
        "growth" in q
        or "grew" in q
        or "increase" in q
        or "increased" in q
        or "decrease" in q
        or "decreased" in q
        or "change" in q
        or "changed" in q
        or "year over year" in q
        or "year-over-year" in q
        or "yoy" in q
    ):

        return "growth"

    # --------------------------------------
    # Total
    # --------------------------------------

    if (
        "total revenue" in q
        or "total sales" in q
        or "total amount" in q
    ):

        return "total"

    # --------------------------------------
    # Average
    # --------------------------------------

    if (
        "average" in q
        or "mean" in q
    ):

        return "average"

    # --------------------------------------
    # Count
    # --------------------------------------

    if (
        "how many" in q
        or "number of" in q
        or "count" in q
    ):

        return "count"

    # --------------------------------------
    # Highest / Best
    # --------------------------------------

    if (
        "highest" in q
        or "best" in q
        or "maximum" in q
        or "most" in q
    ):

        return "highest"

    # --------------------------------------
    # Lowest
    # --------------------------------------

    if (
        "lowest" in q
        or "minimum" in q
        or "least" in q
    ):

        return "lowest"

    # --------------------------------------
    # Top N
    # --------------------------------------

    if (
        "top " in q
        or q.startswith("top")
    ):

        return "top_n"

    return "general"


# ==========================================
# 3. COMPARISON INSIGHT
# ==========================================

def generate_comparison_insight(df):
    """
    Generate a business insight for
    comparison questions.
    """

    if df is None or df.empty:

        return (
            "No data was found for this comparison."
        )

    if len(df.columns) < 2:

        return (
            "There is not enough data "
            "for a comparison."
        )

    name_column = df.columns[0]

    value_column = df.columns[1]

    # --------------------------------------
    # Check numeric values
    # --------------------------------------

    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):

        return (
            "The comparison values "
            "are not numeric."
        )

    # --------------------------------------
    # Sort highest first
    # --------------------------------------

    sorted_df = df.sort_values(
        by=value_column,
        ascending=False
    ).reset_index(drop=True)

    if len(sorted_df) < 2:

        return (
            "At least two values are required "
            "for a comparison."
        )

    first = sorted_df.iloc[0]

    second = sorted_df.iloc[1]

    first_name = first[name_column]

    second_name = second[name_column]

    first_value = first[value_column]

    second_value = second[value_column]

    difference = (
        first_value - second_value
    )

    first_formatted = format_value(
        first_value,
        value_column
    )

    second_formatted = format_value(
        second_value,
        value_column
    )

    difference_formatted = format_value(
        abs(difference),
        value_column
    )

    # ======================================
    # REVENUE COMPARISON
    # ======================================

    if "revenue" in value_column.lower():

        if difference > 0:

            return (
                f"{first_name} generated "
                f"{first_formatted} in revenue, "
                f"compared with "
                f"{second_formatted} for "
                f"{second_name}. "
                f"{first_name} generated "
                f"{difference_formatted} more revenue."
            )

        if difference < 0:

            return (
                f"{second_name} generated "
                f"{second_formatted} in revenue, "
                f"compared with "
                f"{first_formatted} for "
                f"{first_name}. "
                f"{second_name} generated "
                f"{difference_formatted} more revenue."
            )

        return (
            f"{first_name} and {second_name} "
            f"generated the same revenue of "
            f"{first_formatted}."
        )

    # ======================================
    # UNITS COMPARISON
    # ======================================

    if (
        "unit" in value_column.lower()
        or "quantity" in value_column.lower()
    ):

        if difference > 0:

            return (
                f"{first_name} sold "
                f"{first_formatted} units, "
                f"compared with "
                f"{second_formatted} units for "
                f"{second_name}. "
                f"{first_name} sold "
                f"{difference_formatted} more units."
            )

        if difference < 0:

            return (
                f"{second_name} sold "
                f"{second_formatted} units, "
                f"compared with "
                f"{first_formatted} units for "
                f"{first_name}. "
                f"{second_name} sold "
                f"{difference_formatted} more units."
            )

        return (
            f"{first_name} and {second_name} "
            f"sold the same number of units: "
            f"{first_formatted}."
        )

    # ======================================
    # GENERIC COMPARISON
    # ======================================

    if difference > 0:

        return (
            f"{first_name} had the higher "
            f"{value_column.replace('_', ' ')}, "
            f"at {first_formatted}, compared "
            f"with {second_name} at "
            f"{second_formatted}. "
            f"The difference was "
            f"{difference_formatted}."
        )

    if difference < 0:

        return (
            f"{second_name} had the higher "
            f"{value_column.replace('_', ' ')}, "
            f"at {second_formatted}, compared "
            f"with {first_name} at "
            f"{first_formatted}. "
            f"The difference was "
            f"{difference_formatted}."
        )

    return (
        f"{first_name} and {second_name} "
        f"had the same "
        f"{value_column.replace('_', ' ')}, "
        f"at {first_formatted}."
    )


# ==========================================
# 4. PERCENTAGE INSIGHT
# ==========================================

def generate_percentage_insight(
    question,
    df
):
    """
    Generate an insight for percentage/share
    questions.
    """

    if df is None or df.empty:

        return (
            "No data was found for "
            "this percentage calculation."
        )

    if len(df.columns) < 1:

        return (
            "No percentage result was found."
        )

    # --------------------------------------
    # Find numeric column
    # --------------------------------------

    numeric_columns = (
        df.select_dtypes(
            include="number"
        ).columns.tolist()
    )

    if not numeric_columns:

        return (
            "No numeric percentage result "
            "was found."
        )

    value_column = numeric_columns[-1]

    value = df.iloc[0][value_column]

    # --------------------------------------
    # Try to identify entity
    # --------------------------------------

    match = re.search(
        r"(?:from|for|of)\s+"
        r"(?:the\s+)?"
        r"([A-Za-z][A-Za-z\s]*)"
        r"(?:\?|$)",
        question,
        re.IGNORECASE
    )

    if match:

        entity = match.group(1).strip()

        # Remove common trailing words
        entity = re.sub(
            r"\s+(category|product|region)$",
            "",
            entity,
            flags=re.IGNORECASE
        ).strip()

        return (
            f"{entity} contributed "
            f"{value:.2f}% of total revenue."
        )

    return (
        f"The requested share is "
        f"{value:.2f}% of total revenue."
    )


# ==========================================
# 5. GROWTH / CHANGE INSIGHT
# ==========================================

def generate_growth_insight(df):
    """
    Calculate percentage growth/change between
    two periods.
    """

    if df is None or df.empty:

        return (
            "No data was found for the "
            "growth calculation."
        )

    if len(df.columns) < 2:

        return (
            "There is not enough data to "
            "calculate growth."
        )

    name_column = df.columns[0]

    value_column = df.columns[1]

    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):

        return (
            "The values required for growth "
            "calculation are not numeric."
        )

    # --------------------------------------
    # Need at least two periods
    # --------------------------------------

    if len(df) < 2:

        return (
            "At least two periods are required "
            "to calculate growth."
        )

    # --------------------------------------
    # Keep original chronological order
    # --------------------------------------

    growth_df = df.copy()

    # Try chronological sorting for years/months
    try:

        growth_df = growth_df.sort_values(
            by=name_column
        ).reset_index(drop=True)

    except Exception:
        pass

    previous = growth_df.iloc[0]

    current = growth_df.iloc[-1]

    previous_period = previous[name_column]

    current_period = current[name_column]

    previous_value = float(
        previous[value_column]
    )

    current_value = float(
        current[value_column]
    )

    absolute_change = (
        current_value - previous_value
    )

    # --------------------------------------
    # Avoid division by zero
    # --------------------------------------

    if previous_value == 0:

        return (
            f"Revenue changed from "
            f"{format_value(previous_value, value_column)} "
            f"in {previous_period} to "
            f"{format_value(current_value, value_column)} "
            f"in {current_period}. "
            f"Percentage growth cannot be calculated "
            f"because the earlier value was zero."
        )

    percentage_change = (
        absolute_change
        / previous_value
        * 100
    )

    previous_formatted = format_value(
        previous_value,
        value_column
    )

    current_formatted = format_value(
        current_value,
        value_column
    )

    absolute_formatted = format_value(
        abs(absolute_change),
        value_column
    )

    # ======================================
    # INCREASE
    # ======================================

    if percentage_change > 0:

        return (
            f"Revenue increased from "
            f"{previous_formatted} in "
            f"{previous_period} to "
            f"{current_formatted} in "
            f"{current_period}, an increase of "
            f"{absolute_formatted} "
            f"({percentage_change:.2f}%)."
        )

    # ======================================
    # DECREASE
    # ======================================

    if percentage_change < 0:

        return (
            f"Revenue decreased from "
            f"{previous_formatted} in "
            f"{previous_period} to "
            f"{current_formatted} in "
            f"{current_period}, a decrease of "
            f"{absolute_formatted} "
            f"({abs(percentage_change):.2f}%)."
        )

    # ======================================
    # NO CHANGE
    # ======================================

    return (
        f"Revenue remained unchanged at "
        f"{current_formatted} between "
        f"{previous_period} and "
        f"{current_period}."
    )


# ==========================================
# 6. MAIN INSIGHT FUNCTION
# ==========================================

def generate_fast_insight(question, df):
    """
    Generate a deterministic business insight
    directly from the DataFrame.
    """

    if df is None or df.empty:

        return (
            "No data was found for this question."
        )

    columns = df.columns.tolist()

    question_type = get_question_type(
        question
    )

    # ==========================================
    # COMPARISON
    # ==========================================

    if question_type == "comparison":

        return generate_comparison_insight(
            df
        )

    # ==========================================
    # PERCENTAGE
    # ==========================================

    if question_type == "percentage":

        return generate_percentage_insight(
            question,
            df
        )

    # ==========================================
    # GROWTH / CHANGE
    # ==========================================

    if question_type == "growth":

        return generate_growth_insight(
            df
        )

    # ==========================================
    # SINGLE VALUE
    # ==========================================

    if (
        len(df) == 1
        and len(columns) == 1
    ):

        column = columns[0]

        value = df.iloc[0, 0]

        formatted = format_value(
            value,
            column
        )

        # --------------------------------------
        # Total
        # --------------------------------------

        if question_type == "total":

            if "revenue" in column.lower():

                return (
                    f"The total revenue is "
                    f"{formatted}."
                )

            if "sales" in column.lower():

                return (
                    f"The total sales are "
                    f"{formatted}."
                )

            return (
                f"The total is {formatted}."
            )

        # --------------------------------------
        # Average
        # --------------------------------------

        if question_type == "average":

            return (
                f"The average "
                f"{column.replace('_', ' ')} "
                f"is {formatted}."
            )

        # --------------------------------------
        # Count
        # --------------------------------------

        if question_type == "count":

            if column.lower() == "count(*)":

                return (
                    f"There are {formatted} "
                    f"orders in total."
                )

            if column.lower() in [
                "num_orders",
                "order_count"
            ]:

                return (
                    f"There are {formatted} "
                    f"orders in total."
                )

            return (
                f"There are {formatted} "
                f"{column.replace('_', ' ')}."
            )

        # --------------------------------------
        # Generic
        # --------------------------------------

        return (
            f"The result is {formatted}."
        )

    # ==========================================
    # SINGLE ROW
    # ==========================================

    if (
        len(df) == 1
        and len(columns) >= 2
    ):

        name_column = columns[0]

        value_column = columns[1]

        name = df.iloc[0][name_column]

        value = df.iloc[0][value_column]

        formatted = format_value(
            value,
            value_column
        )

        # --------------------------------------
        # Units
        # --------------------------------------

        if (
            "unit" in value_column.lower()
            or "quantity" in value_column.lower()
        ):

            return (
                f"{name} sold the most units, "
                f"with {formatted} units."
            )

        # --------------------------------------
        # Revenue
        # --------------------------------------

        if "revenue" in value_column.lower():

            # Best month
            if (
                name_column.lower()
                in ["month", "date"]
            ):

                return (
                    f"{name} was the "
                    f"highest-revenue month, "
                    f"generating {formatted}."
                )

            return (
                f"{name} generated the "
                f"highest revenue, "
                f"at {formatted}."
            )

        # --------------------------------------
        # Generic
        # --------------------------------------

        return (
            f"{name} has the highest "
            f"{value_column.replace('_', ' ')}, "
            f"at {formatted}."
        )

    # ==========================================
    # MULTIPLE ROWS
    # ==========================================

    if (
        len(df) > 1
        and len(columns) >= 2
    ):

        name_column = columns[0]

        value_column = columns[1]

        # --------------------------------------
        # Numeric column
        # --------------------------------------

        if pd.api.types.is_numeric_dtype(
            df[value_column]
        ):

            sorted_df = df.sort_values(
                by=value_column,
                ascending=False
            ).reset_index(drop=True)

            top = sorted_df.iloc[0]

            # ==================================
            # TOP N
            # ==================================

            if question_type == "top_n":

                n = min(
                    len(sorted_df),
                    5
                )

                lines = []

                for i in range(n):

                    row = sorted_df.iloc[i]

                    formatted_value = (
                        format_value(
                            row[value_column],
                            value_column
                        )
                    )

                    lines.append(
                        f"{i + 1}. "
                        f"{row[name_column]} — "
                        f"{formatted_value}"
                    )

                return (
                    "Top results:\n"
                    + "\n".join(lines)
                )

            # ==================================
            # MONTHLY / DATE TREND
            # ==================================

            if (
                name_column.lower()
                in ["month", "date"]
            ):

                highest_name = (
                    top[name_column]
                )

                highest_value = (
                    format_value(
                        top[value_column],
                        value_column
                    )
                )

                if (
                    "revenue"
                    in value_column.lower()
                ):

                    return (
                        f"{highest_name} had the "
                        f"highest revenue, "
                        f"generating "
                        f"{highest_value}."
                    )

                return (
                    f"{highest_name} had the "
                    f"highest "
                    f"{value_column.replace('_', ' ')}, "
                    f"at {highest_value}."
                )

            # ==================================
            # GENERAL RANKING
            # ==================================

            second = (
                sorted_df.iloc[1]
                if len(sorted_df) > 1
                else None
            )

            third = (
                sorted_df.iloc[2]
                if len(sorted_df) > 2
                else None
            )

            top_formatted = format_value(
                top[value_column],
                value_column
            )

            message = (
                f"{top[name_column]} generated "
                f"the highest "
                f"{value_column.replace('_', ' ')}, "
                f"at {top_formatted}"
            )

            if second is not None:

                second_formatted = (
                    format_value(
                        second[value_column],
                        value_column
                    )
                )

                message += (
                    f", followed by "
                    f"{second[name_column]} at "
                    f"{second_formatted}"
                )

            if third is not None:

                third_formatted = (
                    format_value(
                        third[value_column],
                        value_column
                    )
                )

                message += (
                    f", and "
                    f"{third[name_column]} at "
                    f"{third_formatted}"
                )

            return message + "."

    # ==========================================
    # GENERIC RESULT
    # ==========================================

    return (
        f"The analysis returned "
        f"{len(df)} rows of data."
    )