import generate_genai as gemini
import investment as invest
import data
from io import StringIO
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import streamlit as st
import pandas as pd
import inspect
import parser

st.set_page_config(layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

DB_FILE = "expenses.db"
# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'], 
    cookie_name="finance_cookie", 
    key="unique_key", 
    cookie_expiry_days=30
)
authenticator.login()

# App content
if st.session_state.authentication_status:

    def get_function_code(func):
        return inspect.getsource(func)

    def add_markdown(text):
        st.markdown(text)    

    def go_to(page_name):
        st.session_state.page = page_name
        st.rerun()


    def dashboard():
        st.title(f"Hello, {st.session_state.name} 👋")
        st.write("You are successfully logged in.")
        st.header("Dashboard")
        st.subheader("Welcome Back!")
        
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Balance", "₹48,920")
            st.metric("Monthly Income", "₹5,800")
            st.metric("Monthly Expenses", "₹3,200")

        with col2:
            st.success("📅 Last Update: April 16, 2025")
            st.info("💡 Tip: You can optimize your spending to save $400 more per month.")
            st.markdown("### Quick Access")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Investment Growth Prediction"):
                    go_to(investment_growth_prediction)
                if st.button("Financial Advisor"):
                    go_to(invest_chatbot)

            with col2:
                if st.button("Asset Types"):
                    go_to(invest_type_guide)
                if st.button("Portfolio Analysis"):
                    go_to(invest_analysis)

        st.markdown("---")
        st.subheader("Financial Overview")
        st.bar_chart({
            "Income": [5000, 5200, 5300, 5500, 5800],
            "Expenses": [3200, 3100, 3300, 3400, 3200]
        })

    def init_db():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                title TEXT NOT NULL,
                amount INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    DB='income.db'
    def init_income_db():
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_income (
                email TEXT PRIMARY KEY,
                monthly_income INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_user_income(email):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute('SELECT monthly_income FROM user_income WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0
    
    def save_or_update_user_income(email, income):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_income (email, monthly_income)
            VALUES (?, ?)
            ON CONFLICT(email) DO UPDATE SET monthly_income = excluded.monthly_income
        ''', (email, income))
        conn.commit()
        conn.close()



    def add_expense(email, title, amount):
        now = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (email, title, amount, date)
            VALUES (?, ?, ?, ?)
        ''', (email, title, amount, now))
        conn.commit()
        conn.close()

    def get_current_month_expenses(email):
        now = datetime.now()
        current_year = now.strftime("%Y")
        current_month = now.strftime("%m")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title, amount, date FROM expenses
            WHERE email = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ''', (email, current_year, current_month))
        rows = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(rows, columns=["Title", "Amount", "Date"])
        total = df["Amount"].sum() if not df.empty else 0
        return df, total

    def finance_manager():
        st.title("💼 Personal Finance Manager")

        init_db()
        init_income_db()

        user_email = st.session_state.get("email", "test@example.com")

        if 'monthly_income' not in st.session_state:
            st.session_state.monthly_income = get_user_income(user_email)

        df, total_expense = get_current_month_expenses(user_email)
        remaining = st.session_state.monthly_income - total_expense

        # Summary
        st.subheader("1. 💹 Financial Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Remaining Balance", f"₹{remaining}")
        with col2:
            st.metric("Total Expenses", f"₹{total_expense}")

        st.markdown("---")

        # Add Expense
        st.subheader("2. ➕ Add an Expense")
        with st.form("expense_form"):
            title = st.text_input("Expense Title")
            amount = st.number_input("Amount Spent (₹)", min_value=0, step=100)
            submitted = st.form_submit_button("Add Expense")
            if submitted and title and amount > 0:
                add_expense(user_email, title, amount)
                st.success(f"✅ Added: {title} - ₹{amount}")
                st.rerun()

        st.markdown("---")

        # Expense List
        st.subheader("3. 📒 Expense List (This Month)")
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No expenses recorded for this month yet.")

        st.markdown("---")

        # Monthly Income Field
        st.subheader("4. 💸 Set Monthly Income")
        income = st.number_input("Enter your monthly income (₹):", min_value=0, step=500, value=st.session_state.monthly_income)
        if income != st.session_state.monthly_income:
            st.session_state.monthly_income = income
            save_or_update_user_income(user_email, income)
            st.success("✅ Monthly income updated!")

    def investment_growth_prediction():
        st.title("Investment Growth Projection")
        inputs = invest.InvestmentInputs(st)

        if st.button("Calculate Investment"):
            basic_info_filled = bool(inputs.amount and inputs.investment_duration_in_years and inputs.rate_of_annual_return)
            if basic_info_filled:
                with st.spinner("Plotting Graph...",show_time=True):
                    csv_data = invest.get_csv_data(inputs)
                    df = pd.read_csv(csv_data,on_bad_lines='skip')
                    st.header("Investment Growth Over Time") 
                    st.plotly_chart(invest.get_graph(df), use_container_width=True)

                    show_dataframe = st.toggle("Show Dataframe", True)            
                    if show_dataframe:
                        st.dataframe(df)
                with st.spinner("Getting suggestions on what to invest in...",show_time=True):
                    st.header("Suggested Investments Details")
                    add_markdown(gemini.generate(data.get_suggested_investement(df,inputs)))
                with st.spinner("Generating Report...",show_time=True):
                    st.header("Detailed Investments Report")
                    add_markdown(gemini.generate(data.get_report_promt(df,inputs)))
            else:
                st.error("Fill all required fields.")

        show_code = st.toggle("Show Code", True)
        if show_code:
            st.code(get_function_code(investment_growth_prediction), language="python")
            st.code(get_function_code(invest.get_csv_data), language="python")
            st.code(get_function_code(invest.get_graph), language="python")
            st.code(get_function_code(gemini.generate), language="python")
            st.code(get_function_code(data), language="python")

    def invest_type_guide():
        st.title("Investment Type Overview")
        st.markdown("---")
        st.info("""
        **Important Considerations:**
        *   **Growth Potential is Not Guaranteed:** Past performance doesn't predict future results.
        *   **Risk vs. Reward:** Higher potential growth usually comes with higher risk.
        *   **Time Horizon:** Growth often depends on the investment duration.
        *   **Diversification:** Spreading investments across types helps manage risk.
        """)
        st.write("Click on each category below to see details, examples, and suggested growth potential.")
        st.markdown("---") 

        for investment in data.investment_data:
            with st.expander(f"**{investment['name']}**", expanded=False):
                st.markdown(f"**Description:** {investment['description']}")
                st.markdown("---")
                st.subheader("Examples:")
                for example in investment['examples']:
                    st.markdown(f"- {example}") 
                st.markdown("---")
                st.subheader("Suggested Growth Potential & Risk Profile:")
                st.markdown(investment['growth_potential'])

        st.markdown("---")
        with st.spinner("Best Investment Type for Current Market Scenario",show_time=True):
            st.header("Suggested Asset Types To Invest")
            add_markdown(gemini.generate(data.get_assest_type_selection()))

    def invest_analysis():
        st.title("Portfolio Analysis")
        st.write("Get your portfolio analysed, Upload In PDF format, .pdf")
        document_file = st.file_uploader("Choose a file to upload")
        if document_file is not None:
            pdf_text = parser.parse_pdf(document_file)
            with st.spinner("Generating Summary...",show_time=True):
                add_markdown(gemini.generate(data.promt_pdf + pdf_text))

        show_code = st.toggle("Show Code", True)
        if show_code:
            st.code(get_function_code(invest_analysis), language="python")
            st.code(get_function_code(parser.parse_pdf), language="python")
            st.code(get_function_code(gemini.generate), language="python")
            st.code(get_function_code(data), language="python")

    def invest_chatbot():
        st.title("Financial Adviser")
        st.subheader("Talk to our Investment Analyser Chatbot.")

        if "past" not in st.session_state:
            st.session_state.past = []
        if "generated" not in st.session_state:
            st.session_state.generated = []

        def chatbot_response(user_input):
            return gemini.generate(data.chatbot + "User Promt: " + user_input)

        def on_input_change():
            user_input = st.session_state.user_input
            st.session_state.past.append(user_input)
            bot_reply = chatbot_response(user_input)
            st.session_state.generated.append(bot_reply)
            st.session_state.user_input = ""

        def on_btn_click():
            st.session_state.past.clear()
            st.session_state.generated.clear()

        chat_placeholder = st.empty()
        with chat_placeholder.container():
            for i in range(len(st.session_state.generated)):
                st.markdown(f"**🧑 You:** {st.session_state.past[i]}")
                st.markdown(f"**🤖 Advisor:** {st.session_state.generated[i]}")

        st.text_input("💬 Your message:", on_change=on_input_change, key="user_input")
        st.button("🧹 Clear Messages", on_click=on_btn_click)

    def logout():
        st.title(f'Hey {st.session_state.name}')
        st.markdown('#### Do you want to log out ?😢')
        authenticator.logout('Logout')

    pages = {
        "Account": [
            st.Page(dashboard, title="Dashboard", icon=":material/home:"),
            st.Page(finance_manager, title="Finance Manager", icon=":material/savings:"),
        ],
        "AI Tools": [
            st.Page(investment_growth_prediction, title="Investment Growth Prediction", icon=":material/monitoring:"),
            st.Page(invest_type_guide, title="Investment Asset Types", icon=":material/format_list_bulleted:"),
            st.Page(invest_analysis, title="Portfolio Analysis", icon=":material/analytics:"),
            st.Page(invest_chatbot, title="Financial Advisor", icon=":material/smart_toy:"),                                                                                              
        ],
        "Logout": [
            st.Page(logout, title="Logout", icon=":material/logout:"),
        ],
    }

    pg = st.navigation(pages)

    if __name__ == "__main__":
        pg.run()

elif st.session_state.authentication_status is False:
    st.error("Invalid username or password.")
elif st.session_state.authentication_status is None:
    st.warning("Please enter your credentials.")