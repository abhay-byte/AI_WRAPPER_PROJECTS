import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from io import BytesIO

# Sample DataFrame (replace with your own data)
def load_sample_data():
    return pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Score": [85, 90, 95],
        "Passed": [True, True, True]
    })

# Function to generate PDF from DataFrame
def create_pdf_from_df(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Data Report", ln=True, align='C')
    pdf.ln(10)

    # Header
    for col in df.columns:
        pdf.cell(40, 10, col, border=1)
    pdf.ln()

    # Rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(40, 10, str(item), border=1)
        pdf.ln()

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Function to create download link
def download_button(pdf_file, filename):
    b64 = base64.b64encode(pdf_file.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Download PDF Report</a>'
    return href

# Streamlit app layout
def main():
    st.title("📊 PDF Report Generator")
    df = load_sample_data()
    st.dataframe(df)

    if st.button("Generate PDF"):
        pdf_file = create_pdf_from_df(df)
        st.markdown(download_button(pdf_file, "report.pdf"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
