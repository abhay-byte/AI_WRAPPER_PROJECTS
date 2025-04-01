from datetime import date
today = date.today()
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
Commodities & Precious Metals,: Alternative Investments(eg. Cryptocurrencies)
    """
def get_systemInstructions(amount):
    systemInstructions = f"""
Generate only csv format: {data_format}, for the given: {investment_types} for amount: {amount}, given your predictions
which is going to go over time if invested per month.
    """
    return systemInstructions

promt_investment = """Please Explain the investment details briefly.
How much money will be made in lakhs explain. 
Act like you created the table and a financial adviser.
Also explain how much money you have when retired. assume 21 year of age.
At begining give how much you will have at 1,3,5,10 years and at retirement."""

promt_pdf = """Summerize this pdf: """

promt_privacy = f"""Todays Date is {today} so answers accordingly. 
Please Check the privacy policy and rate it out of 10 (Give Rating at top please), 
and state the problems briefly."""