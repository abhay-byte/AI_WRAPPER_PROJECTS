from datetime import date
import fetch_asset_price
import get_news
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
Latest News (Use it to judge in where to invest would be best): {get_news.get_current_financial_news()}
Top Trending Companies (Use it to judge in where to invest would be best): {fetch_asset_price.fetch_top_trending_companies()}
Top IPO (Use it to judge in where to invest would be best): {fetch_asset_price.fetch_top_ipos()}
Other Types of Investment(Use it to judge in where to invest would be best): {fetch_asset_price.fetch_other_types_investement()}
Bond Prices: {fetch_asset_price.fetch_bond_price()}
"""
    return additional_parameter

def get_systemInstructions(inputs):
    additional_parameter = get_additional_details(inputs)

    systemInstructions = f"""
Generate only csv format(STRICTLY DONOT SENT ANYTHING ELSE): {data_format}, for the given: {investment_types} for amount: {inputs.amount}, given your predictions
which is going to go over time if invested per month. Additional Parameter are: {additional_parameter},
also give examples of this investment types {investment_types} for investment done (give data in dataframe).
In the end Give final result, total money made, total Inflation, total tax and everything (in lahks and crores).
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

def get_suggested_investement(df,inputs):
    additional_details = get_additional_details(inputs)
    promt_for_suggestion = f"""
Based on this Dataframe {df}, suggest proper table, for what to invest in based on the following data:
Latest News (Use it to judge in where to invest would be best): {get_news.get_current_financial_news()}
Top Trending Companies (Use it to judge in where to invest would be best): {fetch_asset_price.fetch_top_trending_companies()}
Top IPO (Use it to judge in where to invest would be best): {fetch_asset_price.fetch_top_ipos()}
Other Types of Investment(Use it to judge in where to invest would be best): {fetch_asset_price.fetch_other_types_investement()}
Bond Prices: {fetch_asset_price.fetch_bond_price()}
currency in rupees, in lakhs and crore
GIVE COMPLETE DIRECT SUGGESTIONS ON WHICH STOCK TO BUY OR TO INVEST IN CRYPTO OR GOLD IN A TABULAR FORM, PUT SUMMARY OF MARKET FINANCIAL NEWS
now these are other parameter for investment: {additional_details}
"""
    print(promt_for_suggestion)
    return promt_for_suggestion

promt_pdf = f"""Do a Financial Portfolio Analysis: rate it out of 10 (Give Rating at top please), based on 
Latest News (Use it to judge in where to further invest would be best): {get_news.get_current_financial_news()}
Top Trending Companies (Use it to judge in where to further invest would be best): {fetch_asset_price.fetch_top_trending_companies()}
Top IPO (Use it to judge in where to further invest would be best): {fetch_asset_price.fetch_top_ipos()}
Other Types of Investment(Use it to judge in where to further invest would be best): {fetch_asset_price.fetch_other_types_investement()}
Bond Prices: {fetch_asset_price.fetch_bond_price()}
"""

promt_privacy = f"""Todays Date is {today} so answers accordingly. 
Please Check the privacy policy and rate it out of 10 (Give Rating at top please), 
and state the problems briefly."""

chatbot = f"""You are a financial advisor, help the user solve his financial problems, system provided
data -->
{fetch_asset_price.fetch_top_trending_companies()}
{fetch_asset_price.fetch_other_types_investement()}
"""


