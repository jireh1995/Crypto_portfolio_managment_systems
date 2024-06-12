import pandas as pd
import numpy as np
from scipy.optimize import minimize
import time

def merge_all_data(all_data):
    merged_df = pd.DataFrame()
    for symbol, df in all_data.items():
        df = df.rename(columns={df.columns[1]: f'{symbol}_price'})
        df[f'{symbol}_price'] = df[f'{symbol}_price'].astype(float)  # Ensure price column is float
        if merged_df.empty:
            merged_df = df
        else:
            print(f"Merging data for {symbol}. Columns: {df.columns}")
            if 'date' not in df.columns:
                print(f"Error: 'date' column not found in data for {symbol}")
                continue
            merged_df = pd.merge(merged_df, df, on='date', how='outer')
    if 'date' not in merged_df.columns:
        print("Error: 'date' column not found in merged data")
        print(f"Merged Data Columns: {merged_df.columns}")
    return merged_df

def ensure_datetime(df, date_column='date'):
    if df[date_column].dtype != 'datetime64[ns]':
        df[date_column] = pd.to_datetime(df[date_column])
    return df

def calculate_daily_returns(df):
    if 'date' not in df.columns:
        print("Error: 'date' column not found in data")
        return pd.DataFrame()
    df.set_index('date', inplace=True)
    returns = df.pct_change().dropna()
    returns.reset_index(inplace=True)
    return returns

def calculate_annual_metrics(returns):
    print("Calculating annual metrics...")
    # Ensure 'date' column is excluded from the calculation
    numeric_returns = returns.select_dtypes(include=[np.number])
    mean_daily_returns = numeric_returns.mean()
    expected_returns = mean_daily_returns * 252
    cov_matrix = numeric_returns.cov() * 252

    # Drop columns with NaN or infinite values
    expected_returns = expected_returns.replace([np.inf, -np.inf], np.nan).dropna()
    cov_matrix = cov_matrix.replace([np.inf, -np.inf], np.nan).dropna(how='all').fillna(0)

    # Ensure expected_returns and cov_matrix are consistent
    valid_assets = expected_returns.index.intersection(cov_matrix.columns)
    expected_returns = expected_returns[valid_assets]
    cov_matrix = cov_matrix.loc[valid_assets, valid_assets]

    time.sleep(1)  # Delay 1 second
    return expected_returns, cov_matrix

def optimize_portfolio(expected_returns, cov_matrix, target_return=0.20):
    print("Optimizing portfolio...")
    num_assets = len(expected_returns)
    
    print(f"Number of assets: {num_assets}")
    print(f"Shape of expected_returns: {expected_returns.shape}")
    print(f"Shape of cov_matrix: {cov_matrix.shape}")
    
    def portfolio_variance(weights):
        return weights.T @ cov_matrix @ weights
    
    constraints = ({
        'type': 'eq',
        'fun': lambda weights: expected_returns @ weights - target_return
    }, {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights) - 1
    })
    
    bounds = [(0, 1) for _ in range(num_assets)]
    initial_weights = np.array([1 / num_assets] * num_assets)
    
    result = minimize(portfolio_variance, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    time.sleep(1)  # Delay 1 second
    return result.x
