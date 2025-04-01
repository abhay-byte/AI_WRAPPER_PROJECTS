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

def get_graph(df, ax):
    df_long = df.melt(id_vars=["Investment Type"], 
                      var_name="Year", 
                      value_name="Projected Value (INR)")
    
    sns.lineplot(data=df_long, x="Year", y="Projected (INR)", 
                 hue="Investment Type", marker="o", ax=ax)
    
    ax.set_title("Investment Growth Over Time")
    ax.set_xlabel("Investment Year")
    ax.set_ylabel("Projected (INR)")
    ax.legend(title="Investment Type")
