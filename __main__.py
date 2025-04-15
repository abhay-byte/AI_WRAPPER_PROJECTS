import generate_genai as gemini
import investment as invest
import data
from io import StringIO
import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
import inspect

st.set_page_config(layout="wide")

def get_function_code(func):
    return inspect.getsource(func)

def add_markdown(text):
    st.markdown(text)    

def home_page():
    st.title("Home")
    st.subheader("Financial Details")

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
                    
                #display_investment_growth(df,inputs)
            with st.spinner("Generating further details...",show_time=True):
                st.header("Investment Details")
                add_markdown(gemini.generate(data.get_report_promt(inputs,df)))
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
    st.title("Types of Investment")

def invest_analysis():
    st.title("Investment Analysis")

def invest_chatbot():
    st.title("Investment Advisor")
    st.subheader("Talk to our Investment Analyser Chatbot.")

def data_constants():
    st.title("Data Constants Used in the Project")
    st.code(get_function_code(data), language="python")

def settings():
    st.title("Settings")

def logout():
    pass


pages = {
    "Account":[
        st.Page(home_page, title="Home", icon=":material/home:"),
        st.Page(finance_manager, title="Finance Manager", icon=":material/savings:"),
        st.Page(settings, title="Settings", icon=":material/settings:"),
        ],

    "AI Tools": [
        st.Page(investment_growth_prediction, title="Investment Growth Prediction", icon=":material/monitoring:"),
        st.Page(invest_type_guide, title="Asset Types", icon=":material/format_list_bulleted:"),
        st.Page(invest_analysis, title="Portfolio Analysis", icon=":material/analytics:"),
        st.Page(invest_chatbot, title="Financial Advisor", icon=":material/smart_toy:"),                                                                                              
        ],

    "Logout": [st.Page(logout, title="Logout", icon=":material/logout:"),],
}

pg = st.navigation(pages)

if __name__ == "__main__":
    pg.run()

