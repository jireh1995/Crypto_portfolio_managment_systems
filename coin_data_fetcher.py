# fetch_data.py
import requests
import pandas as pd
import time

# 请将 YOUR_CRYPTOCOMPARE_API_KEY 替换为您的 CryptoCompare API 密钥
API_KEY = "YOUR CRYPTOCOMPARE API KEY"

def get_top_coins_by_market_cap(n=20):
    url = "https://min-api.cryptocompare.com/data/top/mktcapfull"
    params = {
        'limit': n,
        'tsym': 'USD',
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['Data']

def get_historical_data(coin_symbol, vs_currency, limit=365):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': coin_symbol,
        'tsym': vs_currency,
        'limit': limit,
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'Data' in data and 'Data' in data['Data']:
        historical_data = data['Data']['Data']
        return [{'timestamp': day['time'], 'close': float(day['close'])} for day in historical_data if not pd.isna(day['close'])]  # Ensure 'close' is not NaN
    else:
        print(f"No historical data found for {coin_symbol}. Response: {data}")
        return []

def get_all_coins_historical_data(coins, vs_currency, limit=365):
    all_data = {}
    for coin in coins:
        coin_symbol = coin['CoinInfo']['Name']
        try:
            prices = get_historical_data(coin_symbol, vs_currency, limit)
            if prices:
                df = pd.DataFrame(prices)
                df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
                df = df[['date', 'close']]
                df.columns = ['date', f'{coin_symbol}_price']
                df[f'{coin_symbol}_price'] = df[f'{coin_symbol}_price'].astype(float)  # 确保价格列为浮点数
                all_data[coin_symbol] = df
                print(f"Fetched data for {coin_symbol}:")
                print(df.head())
            else:
                print(f"No data found for {coin_symbol}")
        except Exception as e:
            print(f"Failed to fetch data for {coin_symbol}: {e}")
        time.sleep(1)  # 延迟1秒以避免触发API限制
    return all_data
