import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import time

# Cache configuration
CACHE_TIMEOUT = 86400  # 1 day in seconds
_cache = {
    'trending': {'timestamp': 0, 'data': None},
    'ipos': {'timestamp': 0, 'data': None},
    'other_assets': {'timestamp': 0, 'data': None}
}

def fetch_top_trending_companies():
    current_time = time.time()
    if (_cache['trending']['data'] is not None 
        and not _cache['trending']['data'].empty 
        and (current_time - _cache['trending']['timestamp'] < CACHE_TIMEOUT)):
        return _cache['trending']['data']
    
    url = 'https://stockanalysis.com/trending/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        trending_stocks = []
        rows = soup.find_all('tr')[1:21]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                trending_stocks.append({
                    'Company': cols[2].get_text(strip=True),
                    'Price': cols[3].get_text(strip=True),
                    'Market Cap': cols[4].get_text(strip=True),
                    'Growth': cols[5].get_text(strip=True)
                })
        df = pd.DataFrame(trending_stocks)
        _cache['trending'] = {'timestamp': current_time, 'data': df}
        return df
    else:
        return pd.DataFrame()

def fetch_top_ipos():
    current_time = time.time()
    if (_cache['ipos']['data'] is not None 
        and not _cache['ipos']['data'].empty 
        and (current_time - _cache['ipos']['timestamp'] < CACHE_TIMEOUT)):
        return _cache['ipos']['data']
    
    url = 'https://stockanalysis.com/ipos/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ipo_list = []
        rows = soup.find_all('tr')[1:21]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                ipo_list.append({
                    'Company': cols[2].get_text(strip=True),
                    'IPO Price': cols[3].get_text(strip=True),
                    'Current Price': cols[4].get_text(strip=True),
                    'Growth': cols[5].get_text(strip=True)
                })
        df = pd.DataFrame(ipo_list)
        _cache['ipos'] = {'timestamp': current_time, 'data': df}
        return df
    else:
        return pd.DataFrame()

def fetch_other_types_investement():
    current_time = time.time()
    if (_cache['other_assets']['data'] is not None 
        and not _cache['other_assets']['data'].empty 
        and (current_time - _cache['other_assets']['timestamp'] < CACHE_TIMEOUT)):
        return _cache['other_assets']['data']

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

    # Static additions
    rows += [
        {
            "Asset": "Indian Govt Bond ETF (BHARAT Bond 2033)",
            "Price": 1190.55,
            "1-Day Change (%)": "N/A"
        },
        {
            "Asset": "Fixed Deposit (RBI)",
            "Price": "N/A",
            "1-Day Change (%)": "N/A"
        },
        {
            "Asset": "Navi Nifty 50 Index Fund",
            "Price": 14.62,
            "1-Day Change (%)": "N/A"
        }
    ]

    df = pd.DataFrame(rows)
    _cache['other_assets'] = {'timestamp': current_time, 'data': df}
    return df

def fetch_bond_price():
    data = {
        "Asset": [
            "U.S. Treasury Bond ETF (GOVT)",
            "Indian Government Bond ETF (BHARAT Bond ETF April 2033)",
            "Navi Nifty 50 Index Fund"
        ],
        "Price": [22.79, 1190.55, 14.62],
        "1-Day Change (%)": [None, None, None]
    }
    return pd.DataFrame(data)
