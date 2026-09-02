# 🤖 AI Data Analyst Agent

An AI-powered data analysis agent that allows users to explore e-commerce sales data using natural language.

Instead of writing SQL queries manually, users can ask questions such as:

> What are the top 5 products by revenue?

The agent understands the question, routes it through a LangGraph workflow, generates and validates SQL, executes it against a SQLite database, performs data analysis, creates visualizations when required, and returns concise business insights.

---

## 🚀 Features

- 💬 Natural Language Data Analysis
- 🤖 Ollama + Qwen3:8b
- 🧠 LangGraph Agent Workflow
- 🔀 Intelligent Question Routing
- 📝 Natural Language → SQL Generation
- ✅ SQL Validation and Safety Checks
- 🔄 SQL Error Recovery and Retry
- 🧮 Deterministic Data Analysis
- 📊 Dynamic Chart Generation
- 💡 Business Insight Generation
- 🧠 Conversational Follow-up Memory
- 🎛️ Interactive Dashboard Filters
- 📥 CSV Data Export
- 🗄️ SQLite E-commerce Database
- 🌐 Streamlit Web Interface

---

# 📸 Demo

## 📊 Interactive Dashboard

![Dashboard](screenshots/dashboard.png)

Interactive dashboard with KPIs, filters, revenue analysis, and natural-language querying.

---

## 💰 Revenue by Category

![Revenue by Category](screenshots/revenue-by-category.png)

Visualize revenue distribution across different e-commerce product categories.

---

## 📈 Monthly Revenue Trend

![Monthly Revenue](screenshots/monthly-revenue.png)

Analyze monthly revenue patterns across 2025 and 2026.

---

## 🤖 AI Data Analysis

![AI Analysis](screenshots/ai-analysis.png)

Ask business questions in natural language and receive structured data results and AI-generated insights.

---

## 🧠 Conversational Memory

![Conversational Memory](screenshots/conversational-memory.png)

The agent maintains context across follow-up questions, allowing users to refine their analysis naturally.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         │ Natural Language    │
                         │      Question       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         │ Dashboard + Chat    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Conversation Memory │
                         │ Follow-up Context   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     LangGraph       │
                         │   Agent Workflow    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Question Router    │
                         │ SQL / Analysis /    │
                         │      Chart          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Qwen3:8b /        │
                         │      Ollama         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    SQL Generator    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    SQL Validator    │
                         │ SELECT-only Safety  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     SQLite DB       │
                         │  E-commerce Data    │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
             ┌────────────┐ ┌────────────┐ ┌────────────┐
             │  Analysis  │ │   Charts   │ │  Insights  │
             │    Tool    │ │    Tool    │ │    Tool    │
             └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    Final Response   │
                         │ Data + Insight +     │
                         │ Visualization       │
                         └─────────────────────┘


🧠 How It Works

The agent follows a structured multi-step workflow instead of sending every question directly to an LLM.

1. User Question

The user asks a business question using natural language.

What are the top 5 products by revenue?
2. Conversation Memory

Previous questions and answers are used to understand contextual follow-up questions.

Show revenue by category.

What about 2025?

What about Laptop?

Show it as a chart.

The system resolves these follow-ups into meaningful analytical questions.

3. Question Routing

The router determines which capabilities are required:

SQL
SQL + Analysis
SQL + Chart
SQL + Analysis + Chart
4. SQL Generation

Qwen3:8b generates SQL based on the user's question and database schema.

5. SQL Validation

Generated SQL is validated before execution.

Analytical SELECT queries are allowed, while database modification and schema-changing operations are blocked.

6. SQL Execution

The validated query is executed against the SQLite e-commerce database.

7. Data Analysis

Deterministic Python-based analysis handles operations such as:

Sum
Average
Minimum
Maximum
Count
Sorting
Top-N analysis
Percentage calculations
Comparisons
Year-over-year analysis
8. Visualization

When required, the system generates a Plotly visualization based on the returned data and question.

9. Business Insight

The result is converted into a concise business-oriented explanation.

10. Final Response

The Streamlit interface presents:

AI insight
Data result
Visualization
Generated SQL
Agent routing decision
CSV download
💬 Example Questions
Basic Analysis
What is the total revenue?
What is the total number of orders?
Which product generated the highest revenue?
Product Analysis
What are the top 5 products by revenue?
Which product sold the most units?
Category Analysis
Show revenue by category.
Compare Laptop and Smartphone revenue.
Time-Based Analysis
Show monthly revenue trend.
What was the revenue in 2025?
Compare revenue between 2025 and 2026.
Percentage Analysis
What percentage of total revenue comes from Laptop?
Conversational Analysis
Show revenue by category.

What about 2025?

What about Laptop?

Show it as a chart.

The agent maintains analytical context across the conversation.

🎛️ Dashboard

The Streamlit dashboard provides interactive filtering by:

📅 Year
📦 Category
🌍 Region

These filters are also passed into AI questions.

For example:

Year: 2025
Category: Laptop
Region: North

The user can then ask:

What is the revenue?

The generated SQL incorporates the active dashboard filters.

📊 Supported Analysis
Analysis	Example
Total	Total revenue
Average	Average order value
Maximum	Highest revenue product
Minimum	Lowest revenue
Count	Number of orders
Top-N	Top 5 products
Grouping	Revenue by category
Comparison	Laptop vs Smartphone
Percentage	Laptop revenue share
Time Series	Monthly revenue
YoY	2025 vs 2026
Filtering	Year / Category / Region
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Ollama	Local LLM runtime
Qwen3:8b	Natural-language reasoning and SQL generation
LangGraph	Agent workflow orchestration
LangChain	LLM application components
SQLite	E-commerce database
SQLAlchemy	Database connectivity
Pandas	Data processing and analysis
NumPy	Numerical operations
Plotly	Interactive visualizations
Streamlit	Web application and dashboard
📁 Project Structure
AI-Data-Analyst-Agent/
│
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── router.py
│   │   ├── sql_agent.py
│   │   ├── llm.py
│   │   └── memory.py
│   │
│   ├── tools/
│   │   ├── sql_tool.py
│   │   ├── analysis_tool.py
│   │   ├── chart_tool.py
│   │   └── insight_tool.py
│   │
│   ├── database/
│   │   └── schema.py
│   │
│   └── ui/
│       ├── app.py
│       └── dashboard.py
│
├── data/
│   └── ecommerce.db
│
├── screenshots/
│   ├── dashboard.png
│   ├── revenue-by-category.png
│   ├── monthly-revenue.png
│   ├── ai-analysis.png
│   └── conversational-memory.png
│
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/aghilmavannoor/AI-Data-Analyst-Agent.git
cd AI-Data-Analyst-Agent
2. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
🤖 Ollama Setup

This project uses Qwen3:8b locally through Ollama.

After installing Ollama, pull the model:

ollama pull qwen3:8b

Verify the model:

ollama list

Make sure Ollama is running before starting the application.

▶️ Run the Application

From the project root:

streamlit run app/ui/app.py

The application will be available at:

http://localhost:8501
🔐 SQL Safety

The application validates LLM-generated SQL before execution.

The validation layer:

Allows analytical SELECT statements
Blocks data modification queries
Blocks schema modification queries
Prevents accidental database changes
Supports SQL recovery when generated queries fail

Blocked operations include:

INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE

Note: This project is designed for a controlled local/demo environment. Additional security hardening would be required before exposing it to untrusted users or production databases.

🔄 SQL Error Recovery

LLM-generated SQL can occasionally contain syntax or schema errors.

The agent includes a controlled recovery loop:

Generate SQL
     │
     ▼
Validate SQL
     │
     ▼
Execute SQL
     │
     ├── Success ───────► Continue
     │
     └── Error
          │
          ▼
       Fix SQL
          │
          ▼
    Validate Again

This allows the agent to recover from certain SQL generation failures without immediately terminating the workflow.

🧠 Conversational Memory

The agent supports contextual follow-up questions.

Example:

User:
Show revenue by category.

Agent:
Revenue by category...

User:
What about 2025?

Agent:
Revenue by category for 2025...

User:
What about Laptop?

Agent:
Laptop revenue for 2025...

Users can refine their analysis without repeatedly writing the complete question.

📥 Data Export

Analysis results can be downloaded as CSV files directly from the Streamlit interface.

This allows users to continue working with the results in:

Excel
Power BI
Tableau
Python
Pandas
📌 Example Results

The included sample e-commerce dataset produces results such as:

Total Revenue
₹343,451,000
Total Orders
5,000
Highest Revenue Product
Gaming Laptop
₹71,630,000
Top 5 Products by Revenue
1. Gaming Laptop     ₹71,630,000
2. Laptop Pro        ₹52,125,000
3. Laptop Air        ₹48,685,000
4. Smartphone Pro    ₹36,905,000
5. Smartphone X      ₹31,185,000
Revenue Comparison
2025: ₹205,370,000
2026: ₹138,081,000
Decrease: ₹67,289,000

These values are based on the included sample dataset.

🔍 Technical Highlights
Agentic Workflow

LangGraph is used to orchestrate the multi-step analytical workflow.

Local LLM

Qwen3:8b runs locally through Ollama, allowing the application to perform natural-language analysis without requiring a paid cloud LLM API.

Hybrid AI + Deterministic Analysis

The project separates LLM responsibilities from numerical computation:

LLM
 │
 ├── Understand question
 ├── Generate SQL
 └── Generate business explanation

Python
 │
 ├── Execute SQL
 ├── Analyze data
 ├── Calculate metrics
 └── Generate charts

This approach keeps numerical calculations in deterministic Python logic rather than relying entirely on LLM-generated calculations.

Modular Architecture

The application separates:

Agent orchestration
SQL generation
SQL validation
Database execution
Data analysis
Visualization
Insight generation
Conversation memory
User interface
⚠️ Limitations
Uses a local SQLite database
Qwen3:8b runs locally through Ollama
Performance depends on local hardware
SQL generation quality depends on the selected LLM
The included dataset is an e-commerce sample dataset
Production deployment would require additional authentication and security controls
Stronger query sandboxing would be recommended for untrusted users
🔮 Future Improvements
☁️ Cloud deployment with a hosted LLM
🗄️ PostgreSQL / MySQL support
📄 CSV and Excel file uploads
📚 RAG-based business documentation
🔐 User authentication
🛡️ Advanced SQL sandboxing
📊 More advanced visualization recommendations
📈 Forecasting and predictive analytics
💬 Multi-user conversation sessions
⚡ Query caching
📋 Automated report generation
🧪 Expanded unit and integration testing
📡 Production monitoring and logging
🎯 Project Goal

The goal of this project is to demonstrate how modern AI techniques can be combined with traditional data engineering and analytics tools to build a practical AI-powered data analyst.

Natural Language
       ↓
LLM Reasoning
       ↓
SQL Generation
       ↓
SQL Validation
       ↓
Database Query
       ↓
Data Analysis
       ↓
Visualization
       ↓
Business Insight
👨‍💻 Author

Aghil

Aspiring Data Scientist / AI Engineer interested in:

Artificial Intelligence
Generative AI
LLM Applications
AI Agents
Data Science
Machine Learning
Data Analytics
Python
