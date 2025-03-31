import generate_genai as gemini
import parser 
import investment as invest
import data
from io import StringIO

import streamlit as st
import pandas as pd


def add_markdown(text):
    st.markdown(text)    

def privacy_policy_checker():
    st.title("Privacy Policy Checker")
    url = st.text_input("Enter The Website Privacy Policy Link","example.com/privacy")
    if url and url != "example.com/privacy":
        with st.spinner("Getting the Privacy Policy...", show_time=True):
            website_content = parser.parse_website(url).strip()
        with st.spinner("Checking the Privacy Policy..."):
            add_markdown(gemini.generate(data.promt_privacy + website_content))


def investment_guide():
    st.title("Investment Growth Projection")
    amount = st.text_input("Enter The Amount to be Invested Per Month", value="")
    if amount:
        with st.spinner("Plotting Graph...",show_time=True):
            csv_data = invest.get_csv_data(amount)
            df = pd.read_csv(csv_data, sep=",")
            st.header("Investment Growth Over Time") 
            st.plotly_chart(invest.get_graph(df), use_container_width=True)
            
        with st.spinner("Generating further details...",show_time=True):
            st.header("Investment Details")
            add_markdown(gemini.generate(data.promt_investment + 
                                         data.investment_types + 
                                         csv_data.getvalue()))

def format_checker():
    st.title("Project Format Checker")

def document_summarizer():
    st.title("Document Summarizer")
    st.write("Upload the Document which you want to get analized")
    document_file = st.file_uploader("Choose a file to upload")
    if document_file is not None:
        pdf_text = parser.parse_pdf(document_file)
        with st.spinner("Generating Summary..."):
            add_markdown(gemini.generate(data.promt_pdf+pdf_text))
            
pg = st.navigation([document_summarizer,privacy_policy_checker
                    ,investment_guide])

if __name__ == "__main__":
    pg.run()

