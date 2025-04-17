import generate_genai as gemini
import investment as invest
import data
from io import StringIO
import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
import inspect
import parser

st.set_page_config(layout="wide")

def get_function_code(func):
    return inspect.getsource(func)

def add_markdown(text):
    st.markdown(text)    

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()


def dashboard():
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




def finance_manager():
    st.title("Finance Manager")


def display_investment_growth(df,inputs):
    # Get the CSV data
    csv_data = invest.get_csv_data(inputs)
    df = pd.read_csv(csv_data, on_bad_lines='skip')
    
    # Extract available years
    if "Year" in df.columns:
        years = sorted(df["Year"].unique())
    elif "Investment Type" in df.columns:
        df["Year"] = df["Investment Type"].str.extract(r"(\d+)").astype(int)
        years = sorted(df["Year"].unique())
    else:
        st.error("Year information is missing in the data.")
        return

    # Header
    st.header("Investment Growth Over Time")

    # Selection options
    selected_year = st.selectbox("Select Year to View:", years)
    selected_projection = st.selectbox("Select Projection Scenario:", ["Best Case", "Average Case", "Worst Case"])

    # Plot graph with passed selections
    st.plotly_chart(invest.get_graph(df), use_container_width=True)

def investment_growth_prediction():
    st.title("Investment Growth Projection")

    inputs = invest.InvestmentInputs(st)

    if st.button("Calculate Investment"):
        basic_info_filled = bool(inputs.amount and inputs.investment_duration_in_years and inputs.rate_of_annual_return)
        if (basic_info_filled):
            with st.spinner("Plotting Graph...",show_time=True):
                csv_data = invest.get_csv_data(inputs)
                df = pd.read_csv(csv_data,on_bad_lines='skip')

                st.header("Investment Growth Over Time") 
                st.plotly_chart(invest.get_graph(df), use_container_width=True)
                
                show_dataframe = st.toggle("Show Dataframe",True)            
                if show_dataframe:
                    st.dataframe(df)
                    
            with st.spinner("Getting suggestions on what to invest in...",show_time=True):
                st.header("Suggested Investments")
                add_markdown(gemini.generate(data.get_suggested_investement(df,inputs)))

            # with st.spinner("Generating further details...",show_time=True):
            #     st.header("Detailed Investment Information")
            #     add_markdown(gemini.generate(data.get_report_promt(inputs,df)))
        else:
            st.error("Fill all required fields.")

    else:
        pass
        #st.error("Fill all required fields.")

    show_code = st.toggle("Show Code",True)
    
    if show_code:
        st.code(get_function_code(investment_growth_prediction), language="python")
        st.code(get_function_code(invest.get_csv_data), language="python")
        st.code(get_function_code(invest.get_graph), language="python")
        st.code(get_function_code(gemini.generate), language="python")
        st.code(get_function_code(data), language="python")
    

def invest_type_guide():
    """Displays investment type information using Streamlit expanders."""
    st.title("Investment Type Overview")
    st.markdown("---") # Add a horizontal rule

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
            add_markdown(gemini.generate(data.promt_pdf+pdf_text))
    
    show_code = st.toggle("Show Code",True)
    if show_code:
        st.code(get_function_code(invest_analysis), language="python")
        st.code(get_function_code(parser.parse_pdf), language="python")
        st.code(get_function_code(gemini.generate), language="python")
        st.code(get_function_code(data), language="python")

def invest_chatbot():
    st.title("Financial Adviser")
    st.subheader("Talk to our Investment Analyser Chatbot.")

    # Initialize session state variables if not already set
    if "past" not in st.session_state:
        st.session_state.past = []

    if "generated" not in st.session_state:
        st.session_state.generated = []

    # Simulated chatbot reply (replace with real model/API later)
    def fake_chatbot_response(user_input):
        return (gemini.generate(data.chatbot+"User Promt: "+user_input))

    # When user submits input
    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.past.append(user_input)
        bot_reply = fake_chatbot_response(user_input)
        st.session_state.generated.append(bot_reply)
        st.session_state.user_input = ""  # clear input field

    # Clear chat history
    def on_btn_click():
        st.session_state.past.clear()
        st.session_state.generated.clear()

    # Chat messages layout
    chat_placeholder = st.empty()
    with chat_placeholder.container():
        for i in range(len(st.session_state.generated)):
            st.markdown(f"**🧑 You:** {st.session_state.past[i]}")
            st.markdown(f"**🤖 Advisor:** {st.session_state.generated[i]}")

    # Input field
    st.text_input("💬 Your message:", on_change=on_input_change, key="user_input")

    # Clear button
    st.button("🧹 Clear Messages", on_click=on_btn_click)

def data_constants():
    st.title("Data Constants Used in the Project")
    st.code(get_function_code(data), language="python")

def settings():
    st.title("Settings")

def logout():
    pass


pages = {
    "Account":[
        st.Page(dashboard, title="Dashboard", icon=":material/home:"),
        st.Page(finance_manager, title="Finance Manager", icon=":material/savings:"),
        #st.Page(settings, title="Settings", icon=":material/settings:"),
        ],

    "AI Tools": [
        st.Page(investment_growth_prediction, title="Investment Growth Prediction", icon=":material/monitoring:"),
        st.Page(invest_type_guide, title="Investment Asset Types", icon=":material/format_list_bulleted:"),
        st.Page(invest_analysis, title="Portfolio Analysis", icon=":material/analytics:"),
        st.Page(invest_chatbot, title="Financial Advisor", icon=":material/smart_toy:"),                                                                                              
        ],

    "Logout": [st.Page(logout, title="Logout", icon=":material/logout:"),],
}

pg = st.navigation(pages)

if __name__ == "__main__":
    pg.run()

