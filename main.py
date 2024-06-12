# Ensure you have the correct import statements
from coin_data_fetcher import get_top_coins_by_market_cap, get_all_coins_historical_data
from data_processing import merge_all_data, calculate_daily_returns, calculate_annual_metrics, optimize_portfolio, ensure_datetime
import time

def main():
    try:
        # Input total investment and ensure it's an integer
        total_investment = int(input("请输入您的资产总额（例如20000000）："))
        
        # Get the top 10 cryptocurrencies by market cap
        top_coins = get_top_coins_by_market_cap(20)
        print(f"Top 20 coins by market cap:")
        for coin in top_coins:
            print(f"{coin['CoinInfo']['FullName']} ({coin['CoinInfo']['Name']})")
        
        # Set the historical data limit (days)
        limit = 365
        
        # Get historical data for all cryptocurrencies
        all_coin_data = get_all_coins_historical_data(top_coins, 'USD', limit)
        for symbol, df in all_coin_data.items():
            print(f"Data for {symbol}:")
            print(df.head())
        
        # Merge all cryptocurrency data
        merged_data = merge_all_data(all_coin_data)
        merged_data = ensure_datetime(merged_data)
        print("Merged Data:")
        print(merged_data.head())
        
        # Check if 'date' column exists
        if 'date' not in merged_data.columns:
            print("Error: 'date' column not found in merged data")
            print("Merged Data Columns:", merged_data.columns)
            return None
        
        # Calculate daily returns
        daily_returns = calculate_daily_returns(merged_data)
        print("Daily Returns:")
        print(daily_returns.head())
        
        # Calculate annual metrics
        expected_returns, cov_matrix = calculate_annual_metrics(daily_returns)
        
        print("预期年化收益率:\n", expected_returns)
        print("年化协方差矩阵:\n", cov_matrix)
        
        # Delay 1 second to avoid timing conflicts
        time.sleep(1)
        
        # Optimize portfolio
        optimal_weights = optimize_portfolio(expected_returns, cov_matrix)
        
        print("最优权重:\n", optimal_weights)
        
        # Calculate portfolio allocation
        allocations = optimal_weights * total_investment
        print("投资组合分配:\n", allocations)
        
        results = {
            "total_investment": total_investment,
            "optimal_weights": optimal_weights,
            "allocations": allocations
        }
        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    results = main()
    if results:
        print("\n计算结果：")
        print(f"资产总额：{results['total_investment']}")
        for i, (weight, allocation) in enumerate(zip(results['optimal_weights'], results['allocations'])):
            print(f"资产{i+1} 权重：{weight:.4f}, 分配金额：{allocation:.2f}")
    else:
        print("无法计算投资组合分配，请检查输入和数据。")
