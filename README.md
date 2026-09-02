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


# 🧠 How It Works

The AI Data Analyst Agent follows a structured multi-step workflow instead of sending every question directly to an LLM.

```text
User Question
      │
      ▼
Conversation Memory
      │
      ▼
Question Router
      │
      ▼
SQL Generation
      │
      ▼
SQL Validation
      │
      ▼
SQL Execution
      │
      ▼
Data Analysis
      │
      ├───────────────┐
      ▼               ▼
Visualization    Business Insight
      │               │
      └───────┬───────┘
              ▼
       Final Response
```

## 1️⃣ User Question

Users ask business questions using natural language.

**Example:**

```text
What are the top 5 products by revenue?
```

No SQL knowledge is required from the user.

---

## 2️⃣ 🧠 Conversation Memory

The agent maintains context across follow-up questions.

For example:

```text
User: Show revenue by category.

User: What about 2025?

User: What about Laptop?

User: Show it as a chart.
```

The system resolves these follow-ups into meaningful analytical questions while preserving the previous context.

---

## 3️⃣ 🔀 Question Routing

The router determines which capabilities are required for the user's question.

| Route | Purpose |
|---|---|
| `SQL` | Retrieve data |
| `SQL + Analysis` | Retrieve and analyze data |
| `SQL + Chart` | Retrieve and visualize data |
| `SQL + Analysis + Chart` | Retrieve, analyze, and visualize data |

This prevents unnecessary processing when a question only requires a database query.

---

## 4️⃣ 📝 SQL Generation

Qwen3:8b generates SQL based on:

- User's question
- Database schema
- Available columns
- Required filters
- Analytical requirements

The generated query is then passed to the validation layer before execution.

---

## 5️⃣ 🛡️ SQL Validation

Generated SQL is validated before reaching the database.

The system allows analytical `SELECT` queries while blocking operations that could modify the database or its schema.

**Blocked operations include:**

```text
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE
```

This provides an additional safety layer around LLM-generated SQL.

---

## 6️⃣ 🗄️ SQL Execution

Validated SQL queries are executed against the SQLite e-commerce database.

The query result is converted into a structured Pandas DataFrame for downstream analysis and visualization.

---

## 7️⃣ 📊 Data Analysis

Numerical and analytical operations are handled deterministically using Python rather than relying entirely on the LLM.

Supported operations include:

- ➕ Sum
- 📐 Average
- 🔝 Maximum
- 🔻 Minimum
- 🔢 Count
- ↕️ Sorting
- 🏆 Top-N analysis
- 📊 Percentage calculations
- ⚖️ Comparisons
- 📅 Year-over-year analysis

This separation helps keep numerical calculations consistent and reproducible.

---

## 8️⃣ 📈 Visualization

When a question requires a visualization, the agent generates a Plotly chart based on the returned data and analytical intent.

Examples include:

- Bar charts
- Line charts
- Category comparisons
- Revenue trends
- Top-N visualizations

---

## 9️⃣ 💡 Business Insight

The system converts analytical results into concise business-oriented explanations.

**Example:**

```text
Gaming Laptop generated the highest revenue at ₹71.63M,
followed by Laptop Pro at ₹52.125M.
```

This makes the output easier to understand than returning raw SQL results alone.

---

## 🔟 Final Response

The Streamlit interface presents the complete analytical response:

```text
💡 AI Insight
📊 Data Result
📈 Visualization
🔍 Generated SQL
🔀 Agent Route
📥 CSV Export
```

---

# 💬 Example Questions

The agent supports a range of natural-language business questions.

## 💰 Basic Analysis

```text
What is the total revenue?
```

```text
What is the total number of orders?
```

```text
Which product generated the highest revenue?
```

---

## 🏆 Product Analysis

```text
What are the top 5 products by revenue?
```

```text
Which product sold the most units?
```

---

## 📦 Category Analysis

```text
Show revenue by category.
```

```text
Compare Laptop and Smartphone revenue.
```

---

## 📅 Time-Based Analysis

```text
Show monthly revenue trend.
```

```text
What was the revenue in 2025?
```

```text
Compare revenue between 2025 and 2026.
```

---

## 📊 Percentage Analysis

```text
What percentage of total revenue comes from Laptop?
```

---

## 🧠 Conversational Analysis

The agent can maintain context across multiple questions:

```text
Show revenue by category.

What about 2025?

What about Laptop?

Show it as a chart.
```

Instead of repeating the complete question, users can naturally refine their analysis.

---

# 🎛️ Interactive Dashboard

The Streamlit dashboard provides interactive filtering capabilities.

### Available Filters

| Filter | Description |
|---|---|
| 📅 Year | Filter sales by year |
| 📦 Category | Filter products by category |
| 🌍 Region | Filter customers by region |

These dashboard filters are also passed into AI-generated questions.

### Example

```text
Year:     2025
Category: Laptop
Region:   North
```

The user can then ask:

```text
What is the revenue?
```

The generated SQL incorporates the active dashboard filters so that the AI analysis is consistent with the selected dashboard context.

---

# 📊 Supported Analysis

| Analysis | Example |
|---|---|
| **Total** | Total revenue |
| **Average** | Average order value |
| **Maximum** | Highest revenue product |
| **Minimum** | Lowest revenue |
| **Count** | Number of orders |
| **Top-N** | Top 5 products |
| **Grouping** | Revenue by category |
| **Comparison** | Laptop vs Smartphone |
| **Percentage** | Laptop revenue share |
| **Time Series** | Monthly revenue |
| **YoY** | 2025 vs 2026 |
| **Filtering** | Year / Category / Region |

---

# 🛠️ Tech Stack

| Technology | Role |
|---|---|
| 🐍 **Python** | Core programming language |
| 🦙 **Ollama** | Local LLM runtime |
| 🤖 **Qwen3:8b** | Natural-language reasoning and SQL generation |
| 🧠 **LangGraph** | Agent workflow orchestration |
| 🔗 **LangChain** | LLM application components |
| 🗄️ **SQLite** | E-commerce database |
| 🔌 **SQLAlchemy** | Database connectivity |
| 🐼 **Pandas** | Data processing and analysis |
| 🔢 **NumPy** | Numerical operations |
| 📈 **Plotly** | Interactive visualizations |
| 🌐 **Streamlit** | Web application and dashboard |

---

# 📁 Project Structure

```text
AI-Data-Analyst-Agent/
│
├── app/
│   │
│   ├── agent/
│   │   ├── graph.py              # LangGraph workflow
│   │   ├── router.py             # Question routing
│   │   ├── sql_agent.py          # SQL generation & validation
│   │   ├── llm.py                # Ollama / Qwen3 interface
│   │   └── memory.py             # Conversation context
│   │
│   ├── tools/
│   │   ├── sql_tool.py           # SQL execution
│   │   ├── analysis_tool.py      # Deterministic analysis
│   │   ├── chart_tool.py         # Dynamic visualizations
│   │   └── insight_tool.py       # Business insights
│   │
│   ├── database/
│   │   └── schema.py             # Database schema
│   │
│   └── ui/
│       ├── app.py                # Streamlit application
│       └── dashboard.py          # Dashboard logic
│
├── data/
│   └── ecommerce.db              # SQLite database
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
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/aghilmavannoor/AI-Data-Analyst-Agent.git
cd AI-Data-Analyst-Agent
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

This project uses **Qwen3:8b locally through Ollama**.

After installing Ollama, download the model:

```bash
ollama pull qwen3:8b
```

Verify that the model is available:

```bash
ollama list
```

You should see:

```text
qwen3:8b
```

Make sure Ollama is running before starting the application.

---

# ▶️ Run the Application

From the project root:

```bash
streamlit run app/ui/app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 🔐 SQL Safety

The application validates LLM-generated SQL before execution.

### Safety Layer

- ✅ Allows analytical `SELECT` queries
- 🚫 Blocks data modification queries
- 🚫 Blocks schema modification queries
- 🛡️ Prevents accidental database changes
- 🔄 Supports SQL recovery when generated queries fail

### Blocked Operations

```text
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
TRUNCATE
```

> **Note:** This project is designed for a controlled local/demo environment. Additional security hardening would be required before exposing it to untrusted users or production databases.

---

# 🔄 SQL Error Recovery

LLM-generated SQL can occasionally contain syntax or schema errors.

The agent includes a controlled recovery workflow:

```text
┌─────────────────┐
│  Generate SQL   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate SQL    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute SQL     │
└────────┬────────┘
         │
     ┌───┴───┐
     │       │
 Success   Error
     │       │
     ▼       ▼
 Continue  Fix SQL
             │
             ▼
        Validate Again
```

This allows the agent to recover from certain SQL generation failures without immediately terminating the workflow.

---

# 🧠 Conversational Memory

The agent supports contextual follow-up questions.

### Example

```text
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
```

Users can refine their analysis without repeatedly writing the complete question.

---

# 📥 Data Export

Analysis results can be downloaded as CSV files directly from the Streamlit interface.

This allows users to continue working with the results in:

- 📗 Excel
- 📊 Power BI
- 📈 Tableau
- 🐍 Python
- 🐼 Pandas

---

# 📌 Example Results

The included sample e-commerce dataset produces results such as:

## 💰 Total Revenue

```text
₹343,451,000
```

## 🧾 Total Orders

```text
5,000
```

## 🏆 Highest Revenue Product

```text
Gaming Laptop
₹71,630,000
```

## 🥇 Top 5 Products by Revenue

| Rank | Product | Revenue |
|---:|---|---:|
| 1 | Gaming Laptop | ₹71,630,000 |
| 2 | Laptop Pro | ₹52,125,000 |
| 3 | Laptop Air | ₹48,685,000 |
| 4 | Smartphone Pro | ₹36,905,000 |
| 5 | Smartphone X | ₹31,185,000 |

## 📉 Revenue Comparison

| Year | Revenue |
|---|---:|
| 2025 | ₹205,370,000 |
| 2026 | ₹138,081,000 |
| **Decrease** | **₹67,289,000** |

> These values are based on the included sample e-commerce dataset.

---

# 🔍 Technical Highlights

## 🧠 Agentic Workflow

LangGraph orchestrates the multi-step analytical workflow, allowing different operations to be conditionally executed depending on the user's question.

---

## 🦙 Local LLM

Qwen3:8b runs locally through Ollama.

This allows the application to perform natural-language understanding and SQL generation without requiring a paid cloud LLM API.

---

## ⚡ Hybrid AI + Deterministic Analysis

The system separates LLM responsibilities from numerical computation.

```text
             LLM
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 Understand  Generate  Explain
 Question     SQL     Results


           Python
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
   Execute   Analyze  Generate
     SQL      Data     Charts
```

This approach keeps numerical calculations in deterministic Python logic rather than relying entirely on LLM-generated calculations.

---

## 🧩 Modular Architecture

The project separates responsibilities into independent modules:

```text
Agent Orchestration
        │
        ├── SQL Generation
        ├── SQL Validation
        ├── Database Execution
        ├── Data Analysis
        ├── Visualization
        ├── Insight Generation
        ├── Conversation Memory
        └── User Interface
```

This makes the application easier to maintain, test, and extend.

---

# ⚠️ Limitations

- Uses a local SQLite database
- Qwen3:8b runs locally through Ollama
- Performance depends on local hardware
- SQL generation quality depends on the selected LLM
- The included dataset is an e-commerce sample dataset
- Production deployment would require additional authentication and security controls
- Stronger SQL sandboxing would be recommended for untrusted users
- The current application is primarily designed for local demonstration and portfolio use

---

# 🔮 Future Improvements

The project can be extended with:

- ☁️ Cloud deployment with a hosted LLM
- 🗄️ PostgreSQL / MySQL support
- 📄 CSV and Excel file uploads
- 📚 RAG-based business documentation
- 🔐 User authentication
- 🛡️ Advanced SQL sandboxing
- 📊 More advanced visualization recommendations
- 📈 Forecasting and predictive analytics
- 💬 Multi-user conversation sessions
- ⚡ Query caching
- 📋 Automated report generation
- 🧪 Expanded unit and integration testing
- 📡 Production monitoring and logging

---

# 🎯 Project Goal

The goal of this project is to demonstrate how modern AI techniques can be combined with traditional data engineering and analytics tools to build a practical **AI-powered Data Analyst**.

The complete pipeline is:

```text
Natural Language
       │
       ▼
LLM Reasoning
       │
       ▼
SQL Generation
       │
       ▼
SQL Validation
       │
       ▼
Database Query
       │
       ▼
Data Analysis
       │
       ▼
Visualization
       │
       ▼
Business Insight
```

The project combines **Generative AI, agentic workflows, SQL, data analysis, and visualization** into a practical end-to-end application.

---

# 👨‍💻 Author

## Aghil

Aspiring **Data Scientist / AI Engineer** with an interest in:

- 🤖 Artificial Intelligence
- ✨ Generative AI
- 🧠 LLM Applications
- 🔀 AI Agents
- 📊 Data Science
- 🤖 Machine Learning
- 📈 Data Analytics
- 🐍 Python

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

**Built with Python, LangGraph, Ollama, Qwen3, SQL, and Streamlit.**
