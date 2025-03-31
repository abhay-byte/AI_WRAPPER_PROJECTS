import pandas as pd
import seaborn as sns
import plotly.express as px
import generate_genai as gemini
import data as constant
from io import StringIO

def get_csv_data(amount):
            print(constant.get_systemInstructions(amount))  
            data = str(gemini.generate(constant.get_systemInstructions(amount)))
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
