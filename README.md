## AI WRAPPER PROJECT

**Live App**: [https://aiwrapper.streamlit.app](https://aiwrapper.streamlit.app)

AI Wrapper Project is a powerful, modular AI-driven platform that brings together financial tools, news aggregation, and generative AI in a clean and user-friendly interface. Built using **Streamlit**, it aims to simplify complex decision-making by leveraging real-time data and AI insights.

---

## 🔍 Features

### 📈 Investment Growth Projection
Predict how your investments could grow over time. Enter:
- Initial principal amount
- Investment time horizon (duration)
- Expected annual rate of return

Get a projected growth chart and insights using AI tools for smarter long-term planning.

### 🤖 Generative AI Insights
Utilize LLM-based tools for:
- Automated report generation
- Summarizing financial data
- Interpreting market trends

### 💼 Portfolio & Asset Analysis
Track and analyze different asset types using integrated modules:
- Real-time price fetcher
- Asset comparison
- Portfolio performance metrics

### 🧮 Financial Advisor (AI-Assisted)
Get suggestions and AI-backed insights for:
- Diversification
- Asset allocation
- Risk management

---

## 🧰 Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python
- **AI Tools**: OpenAI or similar LLM APIs
- **Data Analysis**: Pandas, Numpy, Plotly
- **News Source**: News API

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abhay-byte/AI_WRAPPER_PROJECTS.git
   cd AI_WRAPPER_PROJECTS
   ```

3. Install dependencies using Poetry:
   ```bash
   pip install poetry
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Launch the app:
   ```bash
   poetry run streamlit run __main__.py
   ```

---

## 📁 Project Structure

```bash
AI_WRAPPER_PROJECTS/
│
├── main.py                  # Entry point for the Streamlit app
├── fetch_asset_price.py     # Module to fetch real-time asset prices
├── get_news.py              # Module to fetch and process news
├── generate_genai.py        # Handles LLM-based AI generation
├── investment.py            # Core logic for investment projections
├── parser.py                # Helper for parsing data
├── style.css                # Custom UI styling
├── pyproject.toml           # Poetry config file
├── poetry.lock              # Dependency lock file
└── requirements.txt         # Optional: pip requirements
```

---

## 🎯 Purpose of Investment Growth Projection

This module helps users visualize potential future investment outcomes based on:
- Starting capital
- Duration (years)
- Expected annual returns

It assists in understanding compound growth and the impact of long-term investing. The AI tools also add personalized analysis and projections to make decisions more data-driven.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/) for the app framework  
- [OpenAI](https://openai.com/) for generative capabilities  
- [News API](https://newsapi.org/) for real-time updates  
- [Python](https://www.python.org/) for everything behind the scenes
