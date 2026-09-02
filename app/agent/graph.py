import sys
from pathlib import Path
from typing import TypedDict, Any


# ==========================================
# 1. PROJECT PATH
# ==========================================

APP_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(APP_DIR))


# ==========================================
# 2. IMPORT FUNCTIONS
# ==========================================

from agent.sql_agent import (
    generate_sql,
    validate_sql
)

from agent.llm import ask_llm

from agent.router import route_question

from agent.memory import resolve_question

from tools.sql_tool import run_sql

from tools.analysis_tool import analyze_data

from tools.chart_tool import create_chart

from tools.insight_tool import generate_fast_insight


# ==========================================
# 3. LANGGRAPH
# ==========================================

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ==========================================
# 4. AGENT STATE
# ==========================================

class AgentState(TypedDict):

    question: str

    messages: list

    route: str

    sql: str

    data: Any

    result: str

    insight: str

    chart: Any

    error: str

    retry_count: int


# ==========================================
# 5. ROUTER NODE
# ==========================================

def router_node(state: AgentState):

    question = state["question"]

    messages = state["messages"]

    # Resolve follow-up questions
    resolved_question = resolve_question(
        question,
        messages
    )

    # Determine required tools
    route = route_question(
        resolved_question
    )

    print("\nAgent Route:")
    print(route)

    if resolved_question != question:

        print("\nResolved Question:")
        print(resolved_question)

    return {
        "question": resolved_question,
        "route": route,
        "error": ""
    }


# ==========================================
# 6. SQL GENERATION NODE
# ==========================================

def generate_sql_node(state: AgentState):

    question = state["question"]

    try:

        sql = generate_sql(question)

        sql = sql.strip()

        # Remove markdown if LLM returns it
        sql = sql.replace(
            "```sql",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        print("\nGenerated SQL:")
        print(sql)

        return {
            "sql": sql,
            "error": "",
            "retry_count": 0
        }

    except Exception as e:

        print("\nSQL Generation Error:")
        print(e)

        return {
            "sql": "",
            "error": str(e)
        }


# ==========================================
# 7. SQL VALIDATION NODE
# ==========================================

def validate_sql_node(state: AgentState):

    sql = state["sql"]

    # If a previous node already failed,
    # do not validate an empty/invalid SQL query.
    if state["error"]:

        print("\nValidation skipped:")
        print(state["error"])

        return {
            "error": state["error"]
        }

    try:

        validate_sql(sql)

        print("\nSQL Validation:")
        print("Valid SQL")

        return {
            "error": ""
        }

    except Exception as e:

        print("\nSQL Validation Error:")
        print(e)

        return {
            "error": str(e)
        }


# ==========================================
# 8. SQL EXECUTION NODE
# ==========================================

def execute_sql_node(state: AgentState):

    sql = state["sql"]

    if state["error"]:

        return {
            "error": state["error"]
        }

    try:

        data = run_sql(sql)

        print("\nDatabase Result:")
        print(data)

        if data is None:

            return {
                "data": None,
                "result": "No data found.",
                "error": ""
            }

        if data.empty:

            return {
                "data": data,
                "result": "No data found.",
                "error": ""
            }

        return {
            "data": data,
            "result": data.to_string(
                index=False
            ),
            "error": ""
        }

    except Exception as e:

        print("\nSQL Execution Error:")
        print(e)

        return {
            "data": None,
            "error": str(e)
        }


# ==========================================
# 9. FIX SQL NODE
# ==========================================

def fix_sql_node(state: AgentState):

    question = state["question"]

    sql = state["sql"]

    error = state["error"]

    retry_count = state["retry_count"] + 1

    print(
        f"\nSQL Recovery Attempt: "
        f"{retry_count}/3"
    )


    # ======================================
    # MAXIMUM RETRIES
    # ======================================

    if retry_count > 3:

        print(
            "\nMaximum SQL retry limit reached."
        )

        return {
            "error": (
                "Maximum SQL retry limit reached."
            ),
            "retry_count": retry_count
        }


    # ======================================
    # FIX SQL USING LLM
    # ======================================

    prompt = f"""
You are an expert SQLite SQL developer.

Your task is to fix an invalid SQL query.

USER QUESTION:
{question}

CURRENT SQL:
{sql}

DATABASE ERROR:
{error}

DATABASE SCHEMA:

customers:
- customer_id
- customer_name
- city
- state
- region

products:
- product_id
- product_name
- category
- price

orders:
- order_id
- customer_id
- product_id
- order_date
- quantity

BUSINESS RULE:

Revenue = quantity * price

RULES:

1. Return ONLY valid SQLite SQL.
2. Return exactly ONE SELECT statement.
3. Do not use INSERT.
4. Do not use UPDATE.
5. Do not use DELETE.
6. Do not use DROP.
7. Do not use ALTER.
8. Do not use CREATE.
9. Do not modify the database.
10. Use only the tables and columns listed above.
11. Use SQLite-compatible syntax.
12. Do not use markdown.
13. Do not explain the answer.

Return only the corrected SQL.
"""

    try:

        corrected_sql = ask_llm(prompt)

        corrected_sql = corrected_sql.strip()

        # Remove markdown
        corrected_sql = corrected_sql.replace(
            "```sql",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        if not corrected_sql:

            raise ValueError(
                "LLM returned an empty SQL query."
            )

        print("\nCorrected SQL:")
        print(corrected_sql)

        return {
            "sql": corrected_sql,
            "error": "",
            "retry_count": retry_count
        }

    except Exception as e:

        print("\nSQL Recovery Error:")
        print(e)

        return {
            "error": str(e),
            "retry_count": retry_count
        }


# ==========================================
# 10. ANALYSIS NODE
# ==========================================

def analysis_node(state: AgentState):

    question = state["question"]

    data = state["data"]

    if data is None or data.empty:

        return {
            "result": "No data found."
        }


    numeric_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()


    # ======================================
    # NO NUMERIC DATA
    # ======================================

    if not numeric_columns:

        return {
            "result": data.to_string(
                index=False
            )
        }


    # Use the last numeric column as
    # the main analysis column.
    numeric_column = numeric_columns[-1]

    question_lower = question.lower()


    # ======================================
    # DETERMINE OPERATION
    # ======================================

    if (
        "average" in question_lower
        or "mean" in question_lower
    ):

        operation = "average"

    elif (
        "maximum" in question_lower
        or "highest" in question_lower
        or "max" in question_lower
    ):

        operation = "max"

    elif (
        "minimum" in question_lower
        or "lowest" in question_lower
        or "min" in question_lower
    ):

        operation = "min"

    elif (
        "how many" in question_lower
        or "count" in question_lower
        or "number of" in question_lower
    ):

        operation = "count"

    elif (
        "total" in question_lower
        or "sum" in question_lower
    ):

        operation = "sum"

    else:

        operation = "sort"


    # ======================================
    # RUN ANALYSIS
    # ======================================

    try:

        analysis_result = analyze_data(
            data,
            operation,
            numeric_column
        )

        print("\nAnalysis Tool Result:")
        print(analysis_result)

        return {
            "result": str(analysis_result)
        }

    except Exception as e:

        print("\nAnalysis Error:")
        print(e)

        return {
            "result": data.to_string(
                index=False
            )
        }


# ==========================================
# 11. ADVANCED CHART NODE
# ==========================================

def chart_node(state: AgentState):

    data = state["data"]

    question = state["question"]


    # ======================================
    # CHECK DATA
    # ======================================

    if data is None:

        print("\nChart Tool:")
        print("No data available for chart.")

        return {
            "chart": None
        }


    try:

        if data.empty:

            print("\nChart Tool:")
            print("No data available for chart.")

            return {
                "chart": None
            }

    except AttributeError:

        print("\nChart Tool:")
        print("Invalid chart data.")

        return {
            "chart": None
        }


    # ======================================
    # ADVANCED CHART SELECTION
    # ======================================

    try:

        chart, chart_type = create_chart(
            data,
            question
        )

        print("\nChart Tool:")
        print(
            f"Chart type: {chart_type}"
        )

        return {
            "chart": chart
        }

    except Exception as e:

        print("\nChart Error:")
        print(e)

        return {
            "chart": None
        }


# ==========================================
# 12. INSIGHT NODE
# ==========================================

def insight_node(state: AgentState):

    question = state["question"]

    data = state["data"]

    try:

        insight = generate_fast_insight(
            question,
            data
        )

        print("\nInsight:")
        print(insight)

        return {
            "insight": insight
        }

    except Exception as e:

        print("\nInsight Error:")
        print(e)

        return {
            "insight": (
                "Unable to generate insight."
            )
        }


# ==========================================
# 13. FAILURE NODE
# ==========================================

def failure_node(state: AgentState):

    error = state.get(
        "error",
        ""
    )

    return {
        "insight": (
            "I couldn't complete the analysis "
            "because the SQL query could not be "
            "generated or executed successfully "
            "after 3 recovery attempts."
        ),
        "result": error
    }


# ==========================================
# 14. ROUTE AFTER VALIDATION
# ==========================================

def route_after_validation(
    state: AgentState
):

    if state["error"]:

        if state["retry_count"] >= 3:

            return "failure"

        return "fix_sql"

    return "execute_sql"


# ==========================================
# 15. ROUTE AFTER EXECUTION
# ==========================================

def route_after_execution(
    state: AgentState
):

    if state["error"]:

        if state["retry_count"] >= 3:

            return "failure"

        return "fix_sql"


    route = state["route"]


    # ======================================
    # ANALYSIS
    # ======================================

    if "ANALYSIS" in route:

        return "analysis"


    # ======================================
    # CHART
    # ======================================

    if "CHART" in route:

        return "chart"


    # ======================================
    # DEFAULT
    # ======================================

    return "insight"


# ==========================================
# 16. ROUTE AFTER ANALYSIS
# ==========================================

def route_after_analysis(
    state: AgentState
):

    route = state["route"]


    if "CHART" in route:

        return "chart"


    return "insight"


# ==========================================
# 17. BUILD GRAPH
# ==========================================

builder = StateGraph(
    AgentState
)


# ==========================================
# 18. ADD NODES
# ==========================================

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "generate_sql",
    generate_sql_node
)

builder.add_node(
    "validate_sql",
    validate_sql_node
)

builder.add_node(
    "execute_sql",
    execute_sql_node
)

builder.add_node(
    "fix_sql",
    fix_sql_node
)

builder.add_node(
    "analysis",
    analysis_node
)

builder.add_node(
    "chart",
    chart_node
)

builder.add_node(
    "insight",
    insight_node
)

builder.add_node(
    "failure",
    failure_node
)


# ==========================================
# 19. GRAPH EDGES
# ==========================================

builder.add_edge(
    START,
    "router"
)

builder.add_edge(
    "router",
    "generate_sql"
)

builder.add_edge(
    "generate_sql",
    "validate_sql"
)


# ==========================================
# VALIDATION ROUTING
# ==========================================

builder.add_conditional_edges(
    "validate_sql",
    route_after_validation,
    {
        "fix_sql": "fix_sql",
        "execute_sql": "execute_sql",
        "failure": "failure"
    }
)


# ==========================================
# EXECUTION ROUTING
# ==========================================

builder.add_conditional_edges(
    "execute_sql",
    route_after_execution,
    {
        "fix_sql": "fix_sql",
        "analysis": "analysis",
        "chart": "chart",
        "insight": "insight",
        "failure": "failure"
    }
)


# ==========================================
# ANALYSIS ROUTING
# ==========================================

builder.add_conditional_edges(
    "analysis",
    route_after_analysis,
    {
        "chart": "chart",
        "insight": "insight"
    }
)


# ==========================================
# RECOVERY LOOP
# ==========================================

builder.add_edge(
    "fix_sql",
    "validate_sql"
)


# ==========================================
# CHART → INSIGHT
# ==========================================

builder.add_edge(
    "chart",
    "insight"
)


# ==========================================
# FINAL NODES
# ==========================================

builder.add_edge(
    "insight",
    END
)

builder.add_edge(
    "failure",
    END
)


# ==========================================
# 20. COMPILE
# ==========================================

agent = builder.compile()


# ==========================================
# 21. RUN AGENT
# ==========================================

if __name__ == "__main__":

    conversation_history = []

    while True:

        print("\n" + "=" * 60)

        question = input(
            "\nAsk a question about the sales data "
            "(type 'exit' to quit): "
        ).strip()


        # ======================================
        # EXIT
        # ======================================

        if question.lower() in [
            "exit",
            "quit",
            "q"
        ]:

            print(
                "\nExiting AI Data Analyst Agent..."
            )

            break


        if not question:

            continue


        # ======================================
        # INITIAL AGENT STATE
        # ======================================

        initial_state = {

            "question": question,

            # Send previous conversation
            # to the memory/context resolver.
            "messages": conversation_history.copy(),

            "route": "",

            "sql": "",

            "data": None,

            "result": "",

            "insight": "",

            "chart": None,

            "error": "",

            "retry_count": 0
        }


        # ======================================
        # RUN LANGGRAPH
        # ======================================

        try:

            final_state = agent.invoke(
                initial_state
            )

        except Exception as e:

            print("\nAgent Error:")
            print(e)

            continue


        # ======================================
        # FINAL OUTPUT
        # ======================================

        print(
            "\n" + "=" * 60
        )

        print("\nFINAL ANSWER")


        # ======================================
        # SQL
        # ======================================

        print("\nSQL:")

        print(
            final_state.get(
                "sql",
                ""
            )
        )


        # ======================================
        # RESULT
        # ======================================

        print("\nResult:")

        print(
            final_state.get(
                "result",
                ""
            )
        )


        # ======================================
        # INSIGHT
        # ======================================

        print("\nInsight:")

        print(
            final_state.get(
                "insight",
                ""
            )
        )


        # ======================================
        # CHART
        # ======================================

        if final_state.get("chart") is not None:

            print(
                "\nChart generated successfully."
            )


        # ======================================
        # SAVE CONVERSATION
        # ======================================

        conversation_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        conversation_history.append(
            {
                "role": "assistant",
                "content": final_state.get(
                    "insight",
                    ""
                )
            }
        )


        print(
            "\n" + "=" * 60
        )