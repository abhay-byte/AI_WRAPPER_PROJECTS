import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

def fetch_top_trending_companies():
    url = 'https://stockanalysis.com/trending/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        trending_stocks = []
        rows = soup.find_all('tr')[1:21]  # Skip header and get top 10 rows
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                company_name = cols[2].get_text(strip=True)
                company_views = cols[3].get_text(strip=True)
                market_cap = cols[4].get_text(strip=True)
                growth = cols[5].get_text(strip=True)
                
                trending_stocks.append({
                    'Company': company_name,
                    'Price': company_views,
                    'Market Cap': market_cap,
                    'Growth': growth
                })
        return pd.DataFrame(trending_stocks)
    else:
        print(f"Failed to retrieve data: HTTP {response.status_code}")
        return []

def fetch_top_ipos():
    url = 'https://stockanalysis.com/ipos/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ipo_list = []
        rows = soup.find_all('tr')[1:21]  # Skip header and get top 10 rows
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                company_name = cols[2].get_text(strip=True)
                ipo_price = cols[3].get_text(strip=True)
                current_price = cols[4].get_text(strip=True)
                growth = cols[5].get_text(strip=True)
                
                ipo_list.append({
                    'Company': company_name,
                    'IPO Price': ipo_price,
                    'Current Price': current_price,
                    'Growth': growth
                })
        return pd.DataFrame(ipo_list)
    else:
        print(f"Failed to retrieve data: HTTP {response.status_code}")
        return []

def fetch_other_types_investement():
    def get_data(ticker):
        try:
            data = yf.Ticker(ticker).history(period="2d")
            price = data['Close'].iloc[-1]
            if len(data['Close']) > 1:
                change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
            else:
                change = None
        except:
            price, change = None, None
        return price, change

    assets = [
        {"name": "SENSEX (Nifty 50)", "ticker": "^NSEI"},
        {"name": "S&P 500", "ticker": "^GSPC"},
        {"name": "Gold (GLD)", "ticker": "GLD"},
        {"name": "Oil (USO)", "ticker": "USO"},
        {"name": "Bitcoin", "ticker": "BTC-USD"},
        {"name": "Ethereum", "ticker": "ETH-USD"},
        {"name": "Property (REIT)", "ticker": "VNQ"},
        {"name": "U.S. Treasury Bond ETF (GOVT)", "ticker": "GOVT"},
        {"name": "U.S. 20+ Yr Treasury Bond (TLT)", "ticker": "TLT"},
    ]

    rows = []
    for asset in assets:
        price, change = get_data(asset["ticker"])
        rows.append({
            "Asset": asset["name"],
            "Price": round(price, 2) if price else "N/A",
            "1-Day Change (%)": round(change, 2) if change else "N/A"
        })

    # Manually add Indian bond & FD & Mutual Fund (no reliable real-time source for these)
    rows.append({
        "Asset": "Indian Govt Bond ETF (BHARAT Bond 2033)",
        "Price": 1190.55,
        "1-Day Change (%)": "N/A"
    })
    rows.append({
        "Asset": "Fixed Deposit (RBI)",
        "Price": "N/A",
        "1-Day Change (%)": "N/A"
    })
    rows.append({
        "Asset": "Navi Nifty 50 Index Fund",
        "Price": 14.62,
        "1-Day Change (%)": "N/A"
    })

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Display
    return pd.DataFrame(df)
def fetch_bond_price():
    govt_price = 22.79  # As of April 16, 2025
    govt_change = None  # Change data not available

    # Fetching data for Indian Government Bond ETF (BHARAT Bond ETF April 2033)
    bharat_bond_price = 1190.55  # As of January 28, 2025
    bharat_bond_change = None  # Change data not available

    # Creating a DataFrame to display the data
    # Fetching data for Navi Nifty 50 Index Fund
    navi_nifty_price = 14.62  # As of March 17, 2025
    navi_nifty_change = None  # Change data not available

    # Creating a DataFrame to display the data
    data2 = {
        "Asset": [
            "U.S. Treasury Bond ETF (GOVT)",
            "Indian Government Bond ETF (BHARAT Bond ETF April 2033)",
            "Navi Nifty 50 Index Fund"
        ],
        "Price": [govt_price, bharat_bond_price, navi_nifty_price],
        "1-Day Change (%)": [govt_change, bharat_bond_change, navi_nifty_change],
    }

    df2 = pd.DataFrame(data2)
    return(df2)
