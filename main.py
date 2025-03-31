#gemini
import base64
from io import StringIO
import os
from google import genai
from pandas.core.dtypes.dtypes import re
from google.genai import types

#pp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from datetime import date

#investmentGuide
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#ui
import streamlit as st
import pandas as pd

#pdf paser
import PyPDF2

def generate(input,return_data):
    client = genai.Client(
        api_key="AIzaSyD4hyc2jk__cdLLx2flYbc44-SE_s3unpw",
    )

    model = "gemini-2.5-pro-exp-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    chunk = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    if return_data:
        return chunk.text
    st.markdown(chunk.text)
         
def side_bar():
    add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
    )   

    # Using "with" notation
    with st.sidebar:
        add_radio = st.radio(
            "Choose a shipping method",
            ("Standard (5-15 days)", "Express (2-5 days)")
        )

def parse_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def privacy_policy_checker():
    st.title("Privacy Policy Checker")
    url = st.text_input("Enter The Website Privacy Policy Link","example.com/privacy")
    if url and url != "example.com/privacy":
        with st.spinner("Checking the Privacy Policy..."):
            # Set up headless Chrome
            options = Options()
            options.add_argument("--headless")  # Run in headless mode
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

        # Launch WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        # Open the URL
            driver.get(url)
            time.sleep(5)  # Wait for JavaScript to load

        # Extract page source
            html = driver.page_source
            driver.quit() 

        # Save to file
            with open('file.html', "w", encoding="utf-8") as f:
                f.write(html)

        # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()

        # Display extracted text
        #st.text_area("Extracted Privacy Policy Text", text, height=300)
            today = date.today()
            generate(f"Todays Date is {today} so answers accordingly. "+"Check the privacy policy and rate it out of 10 (Give Rating at top please), and state the problems briefly: "
                + text.strip(),True)

def investment_guide():
    st.title("Investment Growth Projection")

    amount = st.text_input("Enter The Amount to be Invested Per Month", value="")

    if amount:
        with st.spinner("Plotting Graph..."):

            data_format = {
                "Investment Type": ["x", "y", "z", "a", "b"],
                "Monthly Allocation (INR)": ["x", "y", "z", "a", "b"],
                "Assumed Annual Return (%)": ["x", "y", "z", "a", "b"],
                "Year 1": ["x", "y", "z", "a", "b"],
                "Year 3": ["x", "y", "z", "a", "b"],
                "Year 5": ["x", "y", "z", "a", "b"],
                "Year 10": ["x", "y", "z", "a", "b"]
            }

            investment_types = """
Investment Types: Stock Market Investments,Fixed Income Investments,Real Estate Investments,
Commodities & Precious Metals,Alternative Investments(eg. Cryptocurrencies)
    """
            systemInstructions = f"""
Generate only csv format: {data_format}, for the given: {investment_types} for amount: {amount}, given your predictions
which is going to go over time if invested per month.
    """
            data = str(generate(systemInstructions,True))
            clean_data_str = data.replace("```csv", "").replace("```", "").strip()  
            df = pd.read_csv(StringIO(clean_data_str), sep=",")
            
            st.header("Investment Growth Over Time") 

            df_long = df.melt(id_vars=["Investment Type"], 
                               var_name="Year", 
                               value_name="Projected Value (INR)")

            fig = px.line(df_long, x="Year", y="Projected Value (INR)", 
                          color="Investment Type",
                          markers=True,
                          labels={"Projected Value (INR)": "Projected Value (INR)", "Year": "Investment Year"})

            st.plotly_chart(fig, use_container_width=True)
            promt = "Explain the investment details briefly. act like you created the table and a financial adviser"
            
        with st.spinner("Generating further details..."):
            st.header("Investment Details")
            generate(promt + investment_types + clean_data_str , False)

def format_checker():
    st.title("Project Format Checker")

def document_summarizer():
    st.title("Document Summarizer")
    st.write("Upload the Document which you want to get analized")
    document_file = st.file_uploader("Choose a file to upload")
    if document_file is not None:
        pdf_text = parse_pdf(document_file)
        with st.spinner("Generating Summary..."):
            generate("Summerize this pdf: " +pdf_text,False)
            
pg = st.navigation([document_summarizer,format_checker,privacy_policy_checker
                    ,investment_guide])

if __name__ == "__main__":
    pg.run()

