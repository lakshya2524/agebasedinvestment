import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period='1y'):
    """
    Fetch stock data for a given ticker symbol.
    
    Args:
        ticker (str): The stock ticker symbol
        period (str): Period to fetch data for (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        DataFrame: Historical stock data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return pd.DataFrame()

def calculate_stock_metrics(hist_data):
    """
    Calculate common stock metrics from historical data.
    
    Args:
        hist_data (DataFrame): Historical stock price data
    
    Returns:
        dict: Dictionary of calculated metrics
    """
    if hist_data.empty:
        return {}
        
    # Calculate daily returns
    hist_data['Daily_Return'] = hist_data['Close'].pct_change()
    
    # Calculate metrics
    total_return = ((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[0]) - 1) * 100
    annual_return = total_return * (252 / len(hist_data)) if len(hist_data) > 0 else 0
    volatility = hist_data['Daily_Return'].std() * np.sqrt(252) * 100 if len(hist_data) > 0 else 0
    max_drawdown = ((hist_data['Close'] / hist_data['Close'].cummax()) - 1).min() * 100 if len(hist_data) > 0 else 0
    
    # Calculate Sharpe ratio (assuming risk-free rate of 2%)
    risk_free_rate = 2.0
    sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio
    }

def get_bond_data(duration='all'):
    """
    Get current Treasury bond yield data.
    
    Note: In a real application, this would fetch from an API or database.
    This function provides sample data for demonstration purposes.
    
    Args:
        duration (str): Filter by duration ('short', 'medium', 'long', or 'all')
    
    Returns:
        DataFrame: Bond yield data
    """
    # Sample Treasury yield data
    treasury_yields = {
        '1 Month': 5.30,
        '3 Month': 5.25,
        '6 Month': 5.22,
        '1 Year': 5.10,
        '2 Year': 4.95,
        '3 Year': 4.80,
        '5 Year': 4.73,
        '7 Year': 4.70,
        '10 Year': 4.68,
        '20 Year': 4.78,
        '30 Year': 4.80
    }
    
    df = pd.DataFrame(list(treasury_yields.items()), columns=['Duration', 'Yield'])
    df['Yield'] = df['Yield'] / 100  # Convert to decimal format
    
    # Filter by duration if requested
    if duration == 'short':
        return df[df['Duration'].isin(['1 Month', '3 Month', '6 Month', '1 Year', '2 Year'])]
    elif duration == 'medium':
        return df[df['Duration'].isin(['3 Year', '5 Year', '7 Year'])]
    elif duration == 'long':
        return df[df['Duration'].isin(['10 Year', '20 Year', '30 Year'])]
    else:
        return df

def calculate_retirement_needs(current_age, retirement_age, life_expectancy, current_savings, 
                              monthly_contribution, annual_return, inflation_rate, annual_expenses):
    """
    Calculate retirement needs and project savings.
    
    Args:
        current_age (int): Current age of the individual
        retirement_age (int): Planned retirement age
        life_expectancy (int): Expected life expectancy
        current_savings (float): Current retirement savings
        monthly_contribution (float): Monthly contribution to retirement
        annual_return (float): Expected annual return (decimal)
        inflation_rate (float): Expected inflation rate (decimal)
        annual_expenses (float): Annual expenses needed in retirement (today's dollars)
    
    Returns:
        dict: Retirement projections and analysis
    """
    # Key time periods
    years_to_retirement = retirement_age - current_age
    retirement_years = life_expectancy - retirement_age
    
    # Future value of current savings at retirement
    future_savings = current_savings * ((1 + annual_return) ** years_to_retirement)
    
    # Future value of monthly contributions
    future_contributions = 0
    for i in range(years_to_retirement):
        annual_contribution = monthly_contribution * 12
        future_contributions += annual_contribution * ((1 + annual_return) ** (years_to_retirement - i))
    
    # Total retirement savings
    total_retirement_savings = future_savings + future_contributions
    
    # Expenses adjusted for inflation at retirement
    retirement_annual_expenses = annual_expenses * ((1 + inflation_rate) ** years_to_retirement)
    
    # Total expenses through retirement (continuing to adjust for inflation)
    total_retirement_expenses = 0
    for i in range(retirement_years):
        year_expense = retirement_annual_expenses * ((1 + inflation_rate) ** i)
        total_retirement_expenses += year_expense
    
    # Simple withdrawal calculation (not accounting for continued growth in retirement)
    # This is a simplified calculation - a more complex model would account for portfolio growth during retirement
    simple_annual_withdrawal = total_retirement_savings / retirement_years
    
    # Determine if savings are adequate
    is_adequate = simple_annual_withdrawal >= retirement_annual_expenses
    
    # Generate year-by-year projection
    projection = []
    balance = current_savings
    
    # Pre-retirement projection
    for year in range(years_to_retirement + 1):
        age = current_age + year
        projection.append({
            'Age': age,
            'Year': datetime.now().year + year,
            'Balance': balance,
            'Phase': 'Accumulation'
        })
        if year < years_to_retirement:  # Don't add for the last year in accumulation phase
            balance = balance * (1 + annual_return) + (monthly_contribution * 12)
    
    # Retirement phase projection
    retirement_balance = balance
    for year in range(1, retirement_years + 1):
        age = retirement_age + year
        # Calculate withdrawal adjusted for inflation
        year_expense = retirement_annual_expenses * ((1 + inflation_rate) ** (year - 1))
        # Remaining balance continues to grow
        retirement_balance = max(0, (retirement_balance - year_expense) * (1 + annual_return * 0.7))  # Assuming more conservative return in retirement
        
        projection.append({
            'Age': age,
            'Year': datetime.now().year + years_to_retirement + year,
            'Balance': retirement_balance,
            'Phase': 'Withdrawal'
        })
    
    return {
        'years_to_retirement': years_to_retirement,
        'retirement_years': retirement_years,
        'future_savings': future_savings,
        'future_contributions': future_contributions,
        'total_retirement_savings': total_retirement_savings,
        'retirement_annual_expenses': retirement_annual_expenses,
        'total_retirement_expenses': total_retirement_expenses,
        'simple_annual_withdrawal': simple_annual_withdrawal,
        'is_adequate': is_adequate,
        'projection': projection
    }
