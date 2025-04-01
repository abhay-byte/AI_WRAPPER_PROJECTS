import generate_genai as gemini
import parser 
import investment as invest
import data
from io import StringIO
import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
import inspect

def get_function_code(func):
    return inspect.getsource(func)

def add_markdown(text):
    st.markdown(text)    

def privacy_policy_checker():
    st.title("Privacy Policy Checker")
    url = st.text_input("Enter The Website Privacy Policy Link","example.com/privacy")
    if url and url != "example.com/privacy":
        with st.spinner("Getting the Privacy Policy...", show_time=True):
            website_content = parser.parse_website(url).strip()
        with st.spinner("Checking the Privacy Policy...",show_time=True):
            add_markdown(gemini.generate(data.promt_privacy + website_content))
    show_code = st.toggle("Show Code",True)
    if show_code:
        st.code(get_function_code(privacy_policy_checker), language="python")
        st.code(get_function_code(parser.parse_website), language="python")
        st.code(get_function_code(gemini.generate), language="python")
        st.code(get_function_code(data), language="python")


def investment_guide():
    st.title("Investment Growth Projection")
    amount = st.text_input("Enter The Amount to be Invested Per Month", value="")
    if amount:
        with st.spinner("Plotting Graph...",show_time=True):
            csv_data = invest.get_csv_data(amount)
            df = pd.read_csv(csv_data, sep=",")
            st.header("Investment Growth Over Time") 
            
            st.plotly_chart(invest.get_graph(df), use_container_width=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            invest.get_graph(df, ax)
            st.pyplot(fig)
            
        with st.spinner("Generating further details...",show_time=True):
            st.header("Investment Details")
            add_markdown(gemini.generate(data.promt_investment + 
                                         data.investment_types + 
                                         csv_data.getvalue()))
    show_code = st.toggle("Show Code",True)
    if show_code:
        st.code(get_function_code(investment_guide), language="python")
        st.code(get_function_code(invest.get_csv_data), language="python")
        st.code(get_function_code(invest.get_graph), language="python")
        st.code(get_function_code(gemini.generate), language="python")
        st.code(get_function_code(data), language="python")


def format_checker():
    st.title("Project Format Checker")

def document_summarizer():
    st.title("Document Summarizer")
    st.write("Upload the Document which you want to get analized")
    document_file = st.file_uploader("Choose a file to upload")
    if document_file is not None:
        pdf_text = parser.parse_pdf(document_file)
        with st.spinner("Generating Summary...",show_time=True):
            add_markdown(gemini.generate(data.promt_pdf+pdf_text))
    
    show_code = st.toggle("Show Code",True)
    if show_code:
        st.code(get_function_code(document_summarizer), language="python")
        st.code(get_function_code(parser.parse_pdf), language="python")
        st.code(get_function_code(gemini.generate), language="python")
        st.code(get_function_code(data), language="python")

def data_constants():
    st.title("Data Constants Used in the Project")
    st.code(get_function_code(data), language="python")

pages = {
    "AI Apps": [
        st.Page(investment_guide, title="Investment Growth Projection"),
        st.Page(document_summarizer, title="Document Summarizer"),
        st.Page(privacy_policy_checker, title="Privacy Policy Checker"),
    ],
    "Format": [
        st.Page(data_constants, title="Constants"),
    ],
}

pg = st.navigation(pages)

if __name__ == "__main__":
    pg.run()

