import pandas as pd
import seaborn as sns
import plotly.express as px
import generate_genai as gemini
import data as constant
from io import StringIO


from datetime import datetime
now = datetime.now()


class InvestmentInputs:
    def __init__(self, st):
        self.amount = st.text_input("Enter the principal amount you are starting with, *", placeholder="₹5000")
        self.investment_duration_in_years = st.text_input("Enter the Investment Time Horizon (Duration of investment), *", placeholder="10 years")
        self.rate_of_annual_return = st.text_input("Enter the expected rate of return (Before fees and taxes), *", placeholder="12% (Average) or 100% (High Risk)")

        st.subheader("Additional Investment Details")
        with st.expander("Show Details"):
            self.additional_contribution_amount = st.text_input("Enter the Regular Contribution Amount (e.g., monthly, yearly),", placeholder="₹1,000")
            self.contribution_frequency = st.selectbox("Select the Contribution Frequency:", ["Annually", "Monthly", "Quarterly"])
            self.rate_of_contribution_increase = st.text_input("Enter the Annual Rate of Increase in Contribution (%),", placeholder="5")
            self.rate_of_inflation = st.text_input("Enter the Expected Annual Inflation Rate (%),", placeholder="6")
            self.rate_of_additional_cost = st.text_input("Enter any other Annual Costs or Fees (%),", placeholder="1")
            self.compounding_frequency = st.selectbox("Select the Compounding Frequency:", ["Annually", "Semi-Annually", "Quarterly", "Monthly"])
            self.rate_of_tax = st.text_input("Enter the rate of Tax applicable, (or enter Country Name)", placeholder="10")
            self.return_variability_amount = st.selectbox("Show Scenario Analysis (Best, Average, Worst)?", ["Best","Average","Worst"])
            self.expected_target_amount = st.text_input("Goal Amount to be achieved till specified duration,", placeholder="₹120,000")


def get_csv_data(inputs):
            data = str(gemini.generate(constant.get_systemInstructions(inputs)))
            clean_data_str = data.replace("```csv", "").replace("```", "").strip()  
            return StringIO(clean_data_str)

def get_graph(df):
        df_long = df.melt(id_vars=["Investment Type"], 
                               var_name="Year", 
                               value_name="Projected Value (INR)")
        fig = px.line(df_long, x="Year", y="Projected Value (INR)", 
                          color="Investment Type",
                          markers=True,
                          labels={"Projected Value (INR)": "Projected Value (INR)", "Year": "Investment Year"})
        return fig
