import pandas as pd
import plotly.express as px


def detect_chart_type(question: str, df: pd.DataFrame) -> str:
    """
    Automatically select the most appropriate chart type
    based on the user's question and returned data.
    """

    question_lower = question.lower()

    if df is None or df.empty:
        return "none"

    # ---------------------------------------------------------
    # 1. KPI / SINGLE VALUE
    # ---------------------------------------------------------

    if len(df) == 1 and len(df.columns) <= 2:
        return "kpi"

    # ---------------------------------------------------------
    # 2. SCATTER PLOT
    # ---------------------------------------------------------

    scatter_keywords = [
        "relationship",
        "correlation",
        "vs",
        "versus",
        "compare",
        "comparison",
        "relationship between",
    ]

    numeric_columns = df.select_dtypes(include="number").columns

    if (
        any(keyword in question_lower for keyword in scatter_keywords)
        and len(numeric_columns) >= 2
    ):
        return "scatter"

    # ---------------------------------------------------------
    # 3. PIE CHART
    # ---------------------------------------------------------

    pie_keywords = [
        "share",
        "percentage",
        "proportion",
        "distribution",
        "contribution",
    ]

    if any(keyword in question_lower for keyword in pie_keywords):
        if len(df) <= 10:
            return "pie"

    # ---------------------------------------------------------
    # 4. LINE CHART
    # ---------------------------------------------------------

    line_keywords = [
        "monthly",
        "month",
        "trend",
        "over time",
        "daily",
        "weekly",
        "yearly",
        "growth",
        "timeline",
    ]

    if any(keyword in question_lower for keyword in line_keywords):

        date_columns = []

        for column in df.columns:
            if (
                "date" in column.lower()
                or "month" in column.lower()
                or "year" in column.lower()
            ):
                date_columns.append(column)

        if date_columns:
            return "line"

        # If the question explicitly asks for a trend,
        # use line chart even if the column name is generic.
        if any(
            keyword in question_lower
            for keyword in ["trend", "over time", "monthly", "daily", "weekly"]
        ):
            return "line"

    # ---------------------------------------------------------
    # 5. HORIZONTAL BAR FOR TOP / RANKING QUESTIONS
    # ---------------------------------------------------------

    ranking_keywords = [
        "top",
        "highest",
        "lowest",
        "best",
        "worst",
        "most",
        "least",
        "rank",
        "ranking",
    ]

    if any(keyword in question_lower for keyword in ranking_keywords):
        return "bar_horizontal"

    # ---------------------------------------------------------
    # 6. DEFAULT BAR CHART
    # ---------------------------------------------------------

    if len(df.columns) >= 2:
        return "bar"

    return "none"


def create_chart(df: pd.DataFrame, question: str):
    """
    Create a Plotly chart automatically based on
    the question and dataframe.
    """

    if df is None or df.empty:
        return None, "none"

    chart_type = detect_chart_type(question, df)

    # ---------------------------------------------------------
    # KPI
    # ---------------------------------------------------------

    if chart_type == "kpi":

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) == 0:
            return None, "none"

        value_column = numeric_columns[0]

        value = df[value_column].iloc[0]

        fig = px.bar(
            x=[value],
            y=["Value"],
            orientation="h",
            title=f"{value_column.replace('_', ' ').title()}",
        )

        fig.update_layout(
            xaxis_title="Value",
            yaxis_title="",
            showlegend=False,
        )

        return fig, "kpi"

    # ---------------------------------------------------------
    # PIE
    # ---------------------------------------------------------

    if chart_type == "pie":

        category_column = df.columns[0]
        value_column = df.select_dtypes(include="number").columns[0]

        fig = px.pie(
            df,
            names=category_column,
            values=value_column,
            title="Revenue Distribution",
        )

        return fig, "pie"

    # ---------------------------------------------------------
    # LINE
    # ---------------------------------------------------------

    if chart_type == "line":

        x_column = df.columns[0]

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) == 0:
            return None, "none"

        y_column = numeric_columns[0]

        fig = px.line(
            df,
            x=x_column,
            y=y_column,
            markers=True,
            title=y_column.replace("_", " ").title(),
        )

        fig.update_layout(
            xaxis_title=x_column.replace("_", " ").title(),
            yaxis_title=y_column.replace("_", " ").title(),
        )

        return fig, "line"

    # ---------------------------------------------------------
    # SCATTER
    # ---------------------------------------------------------

    if chart_type == "scatter":

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) < 2:
            return None, "none"

        x_column = numeric_columns[0]
        y_column = numeric_columns[1]

        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{x_column.replace('_', ' ').title()} vs "
                  f"{y_column.replace('_', ' ').title()}",
        )

        fig.update_layout(
            xaxis_title=x_column.replace("_", " ").title(),
            yaxis_title=y_column.replace("_", " ").title(),
        )

        return fig, "scatter"

    # ---------------------------------------------------------
    # HORIZONTAL BAR
    # ---------------------------------------------------------

    if chart_type == "bar_horizontal":

        category_column = df.columns[0]

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) == 0:
            return None, "none"

        value_column = numeric_columns[0]

        sorted_df = df.sort_values(
            by=value_column,
            ascending=True
        )

        fig = px.bar(
            sorted_df,
            x=value_column,
            y=category_column,
            orientation="h",
            title=value_column.replace("_", " ").title(),
        )

        fig.update_layout(
            xaxis_title=value_column.replace("_", " ").title(),
            yaxis_title=category_column.replace("_", " ").title(),
        )

        return fig, "bar_horizontal"

    # ---------------------------------------------------------
    # STANDARD BAR
    # ---------------------------------------------------------

    if chart_type == "bar":

        category_column = df.columns[0]

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) == 0:
            return None, "none"

        value_column = numeric_columns[0]

        fig = px.bar(
            df,
            x=category_column,
            y=value_column,
            title=value_column.replace("_", " ").title(),
        )

        fig.update_layout(
            xaxis_title=category_column.replace("_", " ").title(),
            yaxis_title=value_column.replace("_", " ").title(),
        )

        return fig, "bar"

    return None, "none"