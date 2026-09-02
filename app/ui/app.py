import sys
from pathlib import Path

import streamlit as st
import plotly.express as px


# ==========================================
# 1. PROJECT PATH
# ==========================================

APP_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(APP_DIR)
)


# ==========================================
# 2. IMPORT AGENT
# ==========================================

from agent.graph import agent

from ui.dashboard import (
    get_filter_options,
    get_dashboard_metrics,
    get_revenue_by_category,
    get_monthly_revenue
)


# ==========================================
# 3. PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# 4. CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    .kpi-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #1f2937;
        border: 1px solid #374151;
        text-align: center;
    }

    .kpi-title {
        font-size: 15px;
        color: #9ca3af;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 5. HEADER
# ==========================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI Data Analyst Agent'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your e-commerce data using natural language.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# 6. SIDEBAR FILTERS
# ==========================================

st.sidebar.header(
    "⚙️ Dashboard Filters"
)

try:

    years, categories, regions = (
        get_filter_options()
    )

except Exception as e:

    st.sidebar.error(
        f"Could not load filters: {e}"
    )

    years = []
    categories = []
    regions = []


# ==========================================
# YEAR FILTER
# ==========================================

selected_year = st.sidebar.selectbox(
    "📅 Year",
    ["All"] + years
)


# ==========================================
# CATEGORY FILTER
# ==========================================

selected_category = st.sidebar.selectbox(
    "📦 Category",
    ["All"] + categories
)


# ==========================================
# REGION FILTER
# ==========================================

selected_region = st.sidebar.selectbox(
    "🌍 Region",
    ["All"] + regions
)


# ==========================================
# REFRESH DASHBOARD
# ==========================================

if st.sidebar.button(
    "🔄 Refresh Dashboard"
):

    st.rerun()


# ==========================================
# 7. ACTIVE FILTERS
# ==========================================

active_filters = []


if selected_year != "All":

    active_filters.append(
        f"Year: {selected_year}"
    )


if selected_category != "All":

    active_filters.append(
        f"Category: {selected_category}"
    )


if selected_region != "All":

    active_filters.append(
        f"Region: {selected_region}"
    )


# ==========================================
# 8. DASHBOARD METRICS
# ==========================================

try:

    metrics = get_dashboard_metrics(
        selected_year,
        selected_category,
        selected_region
    )

except Exception as e:

    st.error(
        f"Unable to load dashboard data: {e}"
    )

    metrics = {
        "total_revenue": 0,
        "total_orders": 0,
        "total_customers": 0,
        "total_products": 0
    }


# ==========================================
# 9. CURRENCY FORMATTER
# ==========================================

def format_currency(value):

    value = float(value)

    if value >= 1_000_000:

        return (
            f"₹{value / 1_000_000:.2f}M"
        )

    if value >= 1_000:

        return (
            f"₹{value / 1_000:.2f}K"
        )

    return f"₹{value:,.0f}"


# ==========================================
# 10. BUSINESS OVERVIEW
# ==========================================

st.subheader("📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)


# ==========================================
# REVENUE
# ==========================================

with col1:

    revenue_html = (
        '<div class="kpi-card">'
        '<div class="kpi-title">💰 Total Revenue</div>'
        '<div class="kpi-value">'
        f'{format_currency(metrics["total_revenue"])}'
        '</div>'
        '</div>'
    )

    st.markdown(
        revenue_html,
        unsafe_allow_html=True
    )


# ==========================================
# ORDERS
# ==========================================

with col2:

    orders_html = (
        '<div class="kpi-card">'
        '<div class="kpi-title">📦 Total Orders</div>'
        '<div class="kpi-value">'
        f'{metrics["total_orders"]:,}'
        '</div>'
        '</div>'
    )

    st.markdown(
        orders_html,
        unsafe_allow_html=True
    )


# ==========================================
# CUSTOMERS
# ==========================================

with col3:

    customers_html = (
        '<div class="kpi-card">'
        '<div class="kpi-title">👥 Customers</div>'
        '<div class="kpi-value">'
        f'{metrics["total_customers"]:,}'
        '</div>'
        '</div>'
    )

    st.markdown(
        customers_html,
        unsafe_allow_html=True
    )


# ==========================================
# PRODUCTS
# ==========================================

with col4:

    products_html = (
        '<div class="kpi-card">'
        '<div class="kpi-title">🛍️ Products</div>'
        '<div class="kpi-value">'
        f'{metrics["total_products"]:,}'
        '</div>'
        '</div>'
    )

    st.markdown(
        products_html,
        unsafe_allow_html=True
    )

# ==========================================
# 11. ACTIVE FILTER DISPLAY
# ==========================================

if active_filters:

    st.info(
        "🔎 Active filters: "
        + " | ".join(active_filters)
    )

else:

    st.caption(
        "Showing all available data."
    )


# ==========================================
# 12. REVENUE BY CATEGORY
# ==========================================

try:

    category_data = get_revenue_by_category(
        selected_year,
        selected_category,
        selected_region
    )

except Exception as e:

    category_data = None

    st.warning(
        f"Could not load category chart: {e}"
    )


if (
    category_data is not None
    and not category_data.empty
):

    st.subheader(
        "📊 Revenue by Category"
    )

    fig_category = px.bar(
        category_data,
        x="revenue",
        y="category",
        orientation="h",
        title="Revenue by Category",
        text="revenue"
    )

    fig_category.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig_category.update_layout(
        xaxis_title="Revenue",
        yaxis_title="",
        yaxis={
            "categoryorder": "total ascending"
        },
        height=500
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ==========================================
# 13. MONTHLY REVENUE
# ==========================================

try:

    monthly_data = get_monthly_revenue(
        selected_year,
        selected_category,
        selected_region
    )

except Exception as e:

    monthly_data = None

    st.warning(
        f"Could not load monthly chart: {e}"
    )


if (
    monthly_data is not None
    and not monthly_data.empty
):

    st.subheader(
        "📈 Monthly Revenue Trend"
    )

    fig_monthly = px.line(
        monthly_data,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue"
    )

    fig_monthly.update_traces(
        hovertemplate=(
            "%{x}<br>"
            "Revenue: ₹%{y:,.0f}"
            "<extra></extra>"
        )
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue",
        height=500
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


st.divider()


# ==========================================
# 14. CONVERSATION MEMORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# 15. CLEAR CHAT
# ==========================================

if st.button(
    "🗑️ Clear Conversation"
):

    st.session_state.messages = []

    st.rerun()


# ==========================================
# 16. AI ANALYST
# ==========================================

st.subheader(
    "💬 Ask the AI Analyst"
)

st.caption(
    "Ask questions about your sales data."
)


# ==========================================
# 17. EXAMPLE QUESTIONS
# ==========================================

example_col1, example_col2 = st.columns(2)


with example_col1:

    st.markdown(
        """
        **Try asking:**

        • Which category generated the highest revenue?

        • Which product sold the most units?

        • Show monthly revenue as a chart.
        """
    )


with example_col2:

    st.markdown(
        """
        **Or ask:**

        • Compare Laptop and Smartphone revenue.

        • What percentage of total revenue came from Laptop?

        • Show the top 5 products by revenue as a chart.
        """
    )


st.divider()


# ==========================================
# 18. DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # Display stored chart
        if (
            message["role"] == "assistant"
            and message.get("chart") is not None
        ):

            st.plotly_chart(
                message["chart"],
                use_container_width=True
            )


# ==========================================
# 19. CHAT INPUT
# ==========================================

question = st.chat_input(
    "Ask about your sales data..."
)


# ==========================================
# 20. PROCESS QUESTION
# ==========================================

if question:

    # ======================================
    # SAVE PREVIOUS CONVERSATION
    # ======================================

    conversation_history = (
        st.session_state.messages.copy()
    )


    # ======================================
    # BUILD FILTER CONTEXT
    # ======================================

    if active_filters:

        filter_context = (
            "\n\n"
            "ACTIVE DASHBOARD FILTERS:\n"
            + "\n".join(
                f"- {item}"
                for item in active_filters
            )
            + "\n\n"
            "IMPORTANT: Analyze ONLY data "
            "matching these dashboard filters."
        )

        agent_question = (
            question
            + filter_context
        )

    else:

        agent_question = question


    # ======================================
    # DISPLAY USER MESSAGE
    # ======================================

    with st.chat_message("user"):

        st.markdown(
            question
        )


    # ======================================
    # SAVE USER MESSAGE
    # ======================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ======================================
    # RUN AGENT
    # ======================================

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Analyzing your data..."
        ):

            try:

                # ==================================
                # INITIAL STATE
                # ==================================

                initial_state = {

                    "question": agent_question,

                    "messages": (
                        conversation_history
                    ),

                    "route": "",

                    "sql": "",

                    "data": None,

                    "result": "",

                    "insight": "",

                    "chart": None,

                    "error": "",

                    "retry_count": 0
                }


                # ==================================
                # RUN LANGGRAPH
                # ==================================

                final_state = agent.invoke(
                    initial_state
                )


                # ==================================
                # CHECK FOR AGENT ERROR
                # ==================================

                if final_state.get("error"):

                    st.error(
                        f"❌ {final_state['error']}"
                    )

                else:

                    # ==================================
                    # AI INSIGHT
                    # ==================================

                    st.subheader(
                        "💡 AI Insight"
                    )

                    st.success(
                        final_state["insight"]
                    )


                    # ==================================
                    # CHART
                    # ==================================

                    if (
                        final_state["chart"]
                        is not None
                    ):

                        st.subheader(
                            "📊 Visualization"
                        )

                        st.plotly_chart(
                            final_state["chart"],
                            use_container_width=True
                        )


                    # ==================================
                    # DATA RESULT
                    # ==================================

                    if (
                        final_state["data"]
                        is not None
                    ):

                        st.subheader(
                            "📋 Data Result"
                        )

                        st.dataframe(
                            final_state["data"],
                            use_container_width=True
                        )


                        # ==================================
                        # CSV EXPORT
                        # ==================================

                        csv_data = (
                            final_state["data"]
                            .to_csv(
                                index=False
                            )
                        )

                        st.download_button(
                            label=(
                                "⬇️ Download "
                                "Results as CSV"
                            ),
                            data=csv_data,
                            file_name=(
                                "analysis_result.csv"
                            ),
                            mime="text/csv"
                        )


                    # ==================================
                    # GENERATED SQL
                    # ==================================

                    with st.expander(
                        "🔎 View Generated SQL"
                    ):

                        st.code(
                            final_state["sql"],
                            language="sql"
                        )


                    # ==================================
                    # AGENT ROUTE
                    # ==================================

                    with st.expander(
                        "🧠 View Agent Decision"
                    ):

                        st.write(
                            final_state["route"]
                        )


                    # ==================================
                    # FILTER CONTEXT
                    # ==================================

                    if active_filters:

                        with st.expander(
                            "⚙️ Active Filters Used"
                        ):

                            for item in active_filters:

                                st.write(
                                    f"• {item}"
                                )


                    # ==================================
                    # SAVE ASSISTANT MESSAGE
                    # ==================================

                    st.session_state.messages.append(
                        {
                            "role": "assistant",

                            "content": (
                                final_state["insight"]
                            ),

                            "chart": (
                                final_state["chart"]
                            )
                        }
                    )


            except Exception as e:

                st.error(
                    f"❌ Analysis failed: {e}"
                )