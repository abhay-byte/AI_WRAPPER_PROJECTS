from datetime import date
today = date.today()
data_format = {
                "Investment Type": ["x", "y", "z", "a", "b"],
                "Monthly Allocation (INR)": ["x", "y", "z", "a", "b"],
                "Assumed Annual Return (%)": ["x", "y", "z", "a", "b"],
                "Year 1": ["x", "y", "z", "a", "b"],
                "Year X/4(Mention by user)(replace with year)": ["x", "y", "z", "a", "b"],
                "Year X/2(Mention by user)": ["x", "y", "z", "a", "b"],
                "Year X(Mention by user)": ["x", "y", "z", "a", "b"],
            }

investment_types = """
Investment Types: Stock Market Investments,Fixed Income Investments,Real Estate Investments,
Commodities & Precious Metals,: Alternative Investments(eg. Cryptocurrencies)
    """

def get_additional_details(inputs):
    additional_parameter = f"""

{inputs.investment_duration_in_years} years investment projection:
Initial Principal Amount (one time at begining),{inputs.amount}
Investment Duration,{inputs.investment_duration_in_years} years
Expected Annual Rate of Return (higher the value higher the risk but higher return),{inputs.rate_of_annual_return}%
Compounding Frequency,{inputs.compounding_frequency}
Contribution Amount (invest ammount that is periodically),{inputs.additional_contribution_amount or 'None'}
Contribution Frequency,{inputs.contribution_frequency if inputs.additional_contribution_amount else 'N/A'}
Annual Rate of Contribution Increase,{inputs.rate_of_contribution_increase or '0'}%
Expected Annual Inflation Rate,{inputs.rate_of_inflation or '0'}%
Annual Costs or Fees,{inputs.rate_of_additional_cost or '0'}%
Applicable Tax Rate,{inputs.rate_of_tax or '0'}%
best/ worst/ average case, {inputs.return_variability_amount}
Projection Data (Year/Month based):

"""
    return additional_parameter;

def get_systemInstructions(inputs):
    additional_parameter = get_additional_details(inputs)

    systemInstructions = f"""
Generate only csv format: {data_format}, for the given: {investment_types} for amount: {inputs.amount}, given your predictions
which is going to go over time if invested per month. Additional Parameter are: {additional_parameter},
also give examples of this investment types {investment_types} for investment done (give data in dataframe).
In the end Give final result, total money made, total Inflation, total tax and everything.
    """
    return systemInstructions
# To remove any unnecessary extra newlines
def get_report_promt(inputs, df):
    additional_details = get_additional_details(inputs)

    promt_investment = f"""Please Explain the investment details briefly.
How much money will be made in lakhs explain. 
Act like you created the table and a financial adviser. based on this dataframe {df} and
the additional details provided by user: {additional_details}"""

    return promt_investment

promt_pdf = """Summerize this pdf: """

promt_privacy = f"""Todays Date is {today} so answers accordingly. 
Please Check the privacy policy and rate it out of 10 (Give Rating at top please), 
and state the problems briefly."""


