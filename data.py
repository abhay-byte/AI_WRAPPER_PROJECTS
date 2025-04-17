from datetime import date
import fetch_asset_price
import get_news
today = date.today()

investment_data = [
    {
        "name": "Stock Market Investments",
        "description": "Buying ownership shares (stock or equity) in publicly traded companies. You profit if the company's value increases (capital appreciation) or if it pays out profits (dividends).",
        "examples": [
            "**Individual Stocks:** Buying shares of specific companies like Apple (AAPL), Microsoft (MSFT), Tesla (TSLA), or Johnson & Johnson (JNJ).",
            "**Mutual Funds:** Pooled investments where a manager buys a portfolio of stocks (e.g., a Growth Fund, a Value Fund, an S&P 500 Index Fund).",
            "**Exchange-Traded Funds (ETFs):** Similar to mutual funds but trade like individual stocks on an exchange (e.g., SPY tracks the S&P 500, QQQ tracks the Nasdaq 100)."
        ],
        "growth_potential": "**Potentially High** over the long term (e.g., 10+ years). However, it's also **Volatile**, meaning significant ups and downs (market corrections or crashes) can occur in the short-to-medium term. Higher potential than fixed income, but also higher risk."
    },
    {
        "name": "Fixed Income Investments",
        "description": "Lending money to an entity (government or corporation) in exchange for regular interest payments and the return of the principal amount at a future date (maturity). Focuses more on capital preservation and generating predictable income.",
        "examples": [
            "**Government Bonds:** U.S. Treasury Bonds/Notes/Bills, UK Gilts, German Bunds (considered very safe).",
            "**Corporate Bonds:** Issued by companies (risk varies based on the company's financial health).",
            "**Municipal Bonds:** Issued by states or cities (often offer tax advantages).",
            "**Certificates of Deposit (CDs):** Issued by banks, fixed interest rate for a fixed term.",
            "**Bond Funds/ETFs:** Diversified portfolios of various bonds."
        ],
        "growth_potential": "**Low to Moderate**. Primarily provides *income* rather than significant price appreciation. Generally less volatile and lower risk than stocks, but sensitive to interest rate changes (when rates rise, existing bond prices tend to fall). Aims to preserve capital and often outpace inflation modestly."
    },
    {
        "name": "Real Estate Investments",
        "description": "Investing in physical property or land. Can generate income through rent and profit through appreciation in property value.",
        "examples": [
            "**Rental Properties:** Buying residential homes, apartments, or commercial buildings to rent out.",
            "**Real Estate Investment Trusts (REITs):** Companies that own and operate income-producing real estate. You can buy shares in REITs on stock exchanges, offering liquidity and diversification.",
            "**House Flipping:** Buying undervalued properties, renovating them, and selling for a profit (more active, higher risk).",
            "**Land:** Buying undeveloped land hoping its value increases."
        ],
        "growth_potential": "**Moderate to High**, depending heavily on location, market conditions, and management. Can provide both income (rent) and capital appreciation. Often seen as an inflation hedge. Less liquid than stocks (harder to sell quickly). Can require significant capital and effort (if direct ownership)."
    },
    {
        "name": "Commodities & Precious Metals",
        "description": "Investing in raw materials or basic goods. Precious metals are often seen as a store of value or a hedge against inflation and economic uncertainty.",
        "examples": [
            "**Precious Metals:** Gold, Silver, Platinum (can be held physically as bars/coins, or through ETFs like GLD for gold).",
            "**Energy:** Crude Oil, Natural Gas (often invested in via futures contracts or energy-focused ETFs).",
            "**Agriculture:** Corn, Wheat, Soybeans (often via futures contracts)."
        ],
        "growth_potential": "**Highly Volatile and Speculative**. Growth is driven purely by supply and demand dynamics, geopolitical events, and investor sentiment. They do not generate income (like dividends or interest). Gold/Silver might hold value or increase during crises but don't have inherent growth like a growing company. Often used for diversification or hedging rather than primary growth."
    },
    {
        "name": "Alternative Investments (e.g., Cryptocurrencies)",
        "description": "Investments outside the traditional categories (stocks, bonds, cash). Often less regulated, less liquid, and more complex.",
        "examples": [
            "**Cryptocurrencies:** Bitcoin (BTC), Ethereum (ETH), and thousands of others (altcoins). Decentralized digital or virtual currencies secured by cryptography.",
            "**Private Equity:** Investing directly in private companies (not publicly traded).",
            "**Venture Capital:** Funding startups and early-stage businesses.",
            "**Hedge Funds:** Pooled funds using complex strategies (often for accredited investors only).",
            "**Collectibles:** Art, wine, classic cars, stamps."
        ],
        "growth_potential": "**Potentially Very High, but Extremely Volatile and Speculative**. Especially true for cryptocurrencies and venture capital. The potential for significant gains comes with an equally significant risk of substantial or total loss. Their value can fluctuate wildly based on sentiment, adoption rates, regulatory news, and technological developments. Require a high-risk tolerance and often specialized knowledge."
    }
]


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
def get_assest_type_selection():

    promt_for_asset_selection = f""" 
Types of assets: {investment_types},
Latest News: {get_news.get_current_financial_news()}
Top Trending Companies: {fetch_asset_price.fetch_top_trending_companies()}
Top IPO: {fetch_asset_price.fetch_top_ipos()}
Other Types of Investment: {fetch_asset_price.fetch_other_types_investement()}
Bond Prices: {fetch_asset_price.fetch_bond_price()}
Genereate what asset types would be the best to invest in right now????
Generate a small answers with your reason.
Break down to points please. 
"""
    return promt_for_asset_selection
