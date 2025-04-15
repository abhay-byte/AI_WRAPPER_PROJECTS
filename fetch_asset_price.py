
import requests
from bs4 import BeautifulSoup
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
        return trending_stocks
    else:
        print(f"Failed to retrieve data: HTTP {response.status_code}")
        return []

def fetch_top_ipos():
    url = 'https://stockanalysis.com/ipos/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ipo_list = []
        rows = soup.find_all('tr')[1:11]  # Skip header and get top 10 rows
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
        return ipo_list
    else:
        print(f"Failed to retrieve data: HTTP {response.status_code}")
        return []

# Fetch and print top trending companies as DataFrame
top_companies = fetch_top_trending_companies()
df_trending = pd.DataFrame(top_companies)
print("Top Trending Companies:")
print(df_trending)

# Fetch and print top IPOs as DataFrame
top_ipos = fetch_top_ipos()
df_ipos = pd.DataFrame(top_ipos)
print("\nTop IPOs:")
print(df_ipos)

