import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period='1y'):
    """Fetch stock data for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info, True
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None, None, False

def calculate_metrics(hist_data):
    """Calculate important stock metrics from historical data."""
    if hist_data is None or len(hist_data) == 0:
        return None
    
    # Calculate returns
    hist_data['Daily_Return'] = hist_data['Close'].pct_change()
    
    # Calculate metrics
    metrics = {}
    metrics['Total_Return'] = ((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[0]) - 1) * 100
    metrics['Annualized_Return'] = metrics['Total_Return'] * (252 / len(hist_data))
    metrics['Volatility'] = hist_data['Daily_Return'].std() * np.sqrt(252) * 100
    metrics['Max_Drawdown'] = ((hist_data['Close'] / hist_data['Close'].cummax()) - 1).min() * 100
    metrics['Sharpe_Ratio'] = metrics['Annualized_Return'] / metrics['Volatility'] if metrics['Volatility'] > 0 else 0
    
    # Calculate moving averages
    hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
    hist_data['MA200'] = hist_data['Close'].rolling(window=200).mean()
    
    # Recent performance
    metrics['1M_Return'] = ((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[-22]) - 1) * 100 if len(hist_data) >= 22 else None
    metrics['3M_Return'] = ((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[-66]) - 1) * 100 if len(hist_data) >= 66 else None
    metrics['6M_Return'] = ((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[-126]) - 1) * 100 if len(hist_data) >= 126 else None
    
    return metrics, hist_data

def get_top_stocks_by_country():
    """Get predefined list of top stocks by country."""
    # This is a limited list for demonstration purposes
    return {
        "United States": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM", "V"],
        "China": ["BABA", "TCEHY", "PDD", "JD", "BIDU", "NIO"],
        "Japan": ["7203.T", "6758.T", "6861.T", "6501.T", "7751.T"],
        "United Kingdom": ["BP.L", "HSBA.L", "GSK.L", "ULVR.L", "RIO.L"],
        "Germany": ["VOW3.DE", "BAS.DE", "ALV.DE", "SAP.DE", "SIE.DE"],
        "India": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS"],
        "Brazil": ["VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "B3SA3.SA"],
        "Australia": ["BHP.AX", "CBA.AX", "CSL.AX", "NAB.AX", "WBC.AX"]
    }

def create_stock_price_chart(hist_data, ticker, company_name):
    """Create a stock price chart with moving averages."""
    if hist_data is None or len(hist_data) == 0:
        return None
    
    fig = go.Figure()
    
    # Add Close price
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#636EFA', width=2)
    ))
    
    # Add moving averages if available
    if 'MA50' in hist_data.columns:
        fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data['MA50'],
            mode='lines',
            name='50-Day MA',
            line=dict(color='#EF553B', width=1.5, dash='dash')
        ))
    
    if 'MA200' in hist_data.columns:
        fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data['MA200'],
            mode='lines',
            name='200-Day MA',
            line=dict(color='#00CC96', width=1.5, dash='dash')
        ))
    
    # Set layout
    fig.update_layout(
        title=f"{company_name} ({ticker}) - Stock Price History",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig

def create_returns_chart(hist_data, ticker):
    """Create a chart showing the returns distribution."""
    if hist_data is None or 'Daily_Return' not in hist_data.columns:
        return None
    
    # Filter out NaN values
    returns = hist_data['Daily_Return'].dropna() * 100  # Convert to percentage
    
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=50,
        name='Daily Returns',
        marker_color='#636EFA',
        opacity=0.7
    ))
    
    # Set layout
    fig.update_layout(
        title=f"{ticker} - Daily Returns Distribution",
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig

def show():
    """Display the stock analyzer page."""
    st.title("Stock Analyzer")
    
    st.markdown("""
    Analyze top stocks from different countries and evaluate their performance metrics.
    
    Choose from the pre-selected list of top stocks by country or enter your own ticker symbol.
    """)
    
    # Create tabs for different analysis modes
    tab1, tab2 = st.tabs(["Global Stock Explorer", "Custom Stock Analysis"])
    
    with tab1:
        st.subheader("Explore Top Global Stocks")
        
        # Get top stocks by country
        stocks_by_country = get_top_stocks_by_country()
        countries = list(stocks_by_country.keys())
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_country = st.selectbox("Select Country", countries)
        
        with col2:
            available_stocks = stocks_by_country[selected_country]
            stock_options = []
            
            # Fetch basic info for display
            for ticker in available_stocks:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    if 'shortName' in info:
                        stock_options.append(f"{info['shortName']} ({ticker})")
                    else:
                        stock_options.append(ticker)
                except:
                    stock_options.append(ticker)
            
            selected_stock_option = st.selectbox("Select Stock", stock_options)
            selected_ticker = selected_stock_option.split("(")[-1].split(")")[0] if "(" in selected_stock_option else selected_stock_option
        
        time_period = st.radio("Select Time Period", ["1 Month", "3 Months", "6 Months", "1 Year", "5 Years"], index=3, horizontal=True)
        period_map = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo", "1 Year": "1y", "5 Years": "5y"}
        
        if st.button("Analyze Selected Stock", key="global_stock_button"):
            with st.spinner(f"Analyzing {selected_ticker}..."):
                # Fetch stock data
                hist_data, info, success = fetch_stock_data(selected_ticker, period=period_map[time_period])
                
                if success and hist_data is not None and len(hist_data) > 0:
                    # Calculate metrics
                    metrics, hist_data = calculate_metrics(hist_data)
                    
                    # Display company info
                    company_name = info.get('shortName', selected_ticker)
                    sector = info.get('sector', 'N/A')
                    industry = info.get('industry', 'N/A')
                    
                    st.subheader(f"{company_name} ({selected_ticker})")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Sector", sector)
                    col2.metric("Industry", industry)
                    col3.metric("Country", selected_country)
                    
                    # Current price and change
                    current_price = hist_data['Close'].iloc[-1]
                    price_change = hist_data['Close'].iloc[-1] - hist_data['Close'].iloc[-2]
                    price_change_pct = price_change / hist_data['Close'].iloc[-2] * 100
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Current Price", f"${current_price:.2f}", f"{price_change_pct:+.2f}%")
                    col2.metric("Total Return", f"{metrics['Total_Return']:.2f}%")
                    
                    # Price chart
                    price_chart = create_stock_price_chart(hist_data, selected_ticker, company_name)
                    if price_chart:
                        st.plotly_chart(price_chart, use_container_width=True)
                    
                    # Key metrics
                    st.subheader("Performance Metrics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    if metrics['1M_Return'] is not None:
                        col1.metric("1 Month Return", f"{metrics['1M_Return']:.2f}%")
                    if metrics['3M_Return'] is not None:
                        col2.metric("3 Month Return", f"{metrics['3M_Return']:.2f}%")
                    if metrics['6M_Return'] is not None:
                        col3.metric("6 Month Return", f"{metrics['6M_Return']:.2f}%")
                    col4.metric("Annualized Return", f"{metrics['Annualized_Return']:.2f}%")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Volatility", f"{metrics['Volatility']:.2f}%")
                    col2.metric("Max Drawdown", f"{metrics['Max_Drawdown']:.2f}%")
                    col3.metric("Sharpe Ratio", f"{metrics['Sharpe_Ratio']:.2f}")
                    
                    # Returns distribution
                    returns_chart = create_returns_chart(hist_data, selected_ticker)
                    if returns_chart:
                        st.plotly_chart(returns_chart, use_container_width=True)
                    
                    # Additional company info with expandable sections
                    if info:
                        with st.expander("Company Information"):
                            st.markdown(f"**Business Summary:**")
                            st.write(info.get('longBusinessSummary', 'No business summary available.'))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Financial Information:**")
                                st.markdown(f"- Market Cap: ${info.get('marketCap', 'N/A'):,}")
                                st.markdown(f"- P/E Ratio: {info.get('trailingPE', 'N/A')}")
                                st.markdown(f"- Forward P/E: {info.get('forwardPE', 'N/A')}")
                                st.markdown(f"- Dividend Yield: {info.get('dividendYield', 0) * 100:.2f}%")
                            
                            with col2:
                                st.markdown("**Trading Information:**")
                                st.markdown(f"- 52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
                                st.markdown(f"- 52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
                                st.markdown(f"- Average Volume: {info.get('averageVolume', 'N/A'):,}")
                                st.markdown(f"- Beta: {info.get('beta', 'N/A')}")
                else:
                    st.error(f"Could not retrieve data for {selected_ticker}. Please try another stock.")
    
    with tab2:
        st.subheader("Custom Stock Analysis")
        
        ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL for Apple)", value="AAPL")
        
        custom_time_period = st.radio("Select Time Period", ["1 Month", "3 Months", "6 Months", "1 Year", "5 Years"], 
                                     index=3, horizontal=True, key="custom_period")
        
        if st.button("Analyze Stock", key="custom_stock_button"):
            with st.spinner(f"Analyzing {ticker}..."):
                # Fetch stock data
                hist_data, info, success = fetch_stock_data(ticker, period=period_map[custom_time_period])
                
                if success and hist_data is not None and len(hist_data) > 0:
                    # Calculate metrics
                    metrics, hist_data = calculate_metrics(hist_data)
                    
                    # Display company info
                    company_name = info.get('shortName', ticker)
                    
                    st.subheader(f"{company_name} ({ticker})")
                    
                    # Current price and change
                    current_price = hist_data['Close'].iloc[-1]
                    price_change = hist_data['Close'].iloc[-1] - hist_data['Close'].iloc[-2]
                    price_change_pct = price_change / hist_data['Close'].iloc[-2] * 100
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Current Price", f"${current_price:.2f}", f"{price_change_pct:+.2f}%")
                    col2.metric("Total Return", f"{metrics['Total_Return']:.2f}%")
                    
                    # Price chart
                    price_chart = create_stock_price_chart(hist_data, ticker, company_name)
                    if price_chart:
                        st.plotly_chart(price_chart, use_container_width=True)
                    
                    # Same metrics and charts as in the global analysis tab
                    st.subheader("Performance Metrics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    if metrics['1M_Return'] is not None:
                        col1.metric("1 Month Return", f"{metrics['1M_Return']:.2f}%")
                    if metrics['3M_Return'] is not None:
                        col2.metric("3 Month Return", f"{metrics['3M_Return']:.2f}%")
                    if metrics['6M_Return'] is not None:
                        col3.metric("6 Month Return", f"{metrics['6M_Return']:.2f}%")
                    col4.metric("Annualized Return", f"{metrics['Annualized_Return']:.2f}%")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Volatility", f"{metrics['Volatility']:.2f}%")
                    col2.metric("Max Drawdown", f"{metrics['Max_Drawdown']:.2f}%")
                    col3.metric("Sharpe Ratio", f"{metrics['Sharpe_Ratio']:.2f}")
                    
                    # Returns distribution
                    returns_chart = create_returns_chart(hist_data, ticker)
                    if returns_chart:
                        st.plotly_chart(returns_chart, use_container_width=True)
                    
                    # Company info as in the global analysis
                    if info:
                        with st.expander("Company Information"):
                            st.markdown(f"**Business Summary:**")
                            st.write(info.get('longBusinessSummary', 'No business summary available.'))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Financial Information:**")
                                st.markdown(f"- Market Cap: ${info.get('marketCap', 'N/A'):,}")
                                st.markdown(f"- P/E Ratio: {info.get('trailingPE', 'N/A')}")
                                st.markdown(f"- Forward P/E: {info.get('forwardPE', 'N/A')}")
                                st.markdown(f"- Dividend Yield: {info.get('dividendYield', 0) * 100:.2f}%")
                            
                            with col2:
                                st.markdown("**Trading Information:**")
                                st.markdown(f"- 52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
                                st.markdown(f"- 52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
                                st.markdown(f"- Average Volume: {info.get('averageVolume', 'N/A'):,}")
                                st.markdown(f"- Beta: {info.get('beta', 'N/A')}")
                else:
                    st.error(f"Could not retrieve data for {ticker}. Please check the ticker symbol and try again.")
    
    # Investment considerations based on age
    if 'age' in st.session_state:
        st.subheader("Age-Based Stock Investment Considerations")
        age = st.session_state['age']
        
        if 18 <= age <= 25:
            st.info("""
            **Young Investor (18-25):**
            
            With a long investment horizon, you can afford to take more risk:
            * Consider growth stocks that may have higher volatility but greater long-term potential
            * Technology, renewable energy, and emerging market stocks may be appropriate
            * Focus on companies with strong growth prospects rather than dividend yield
            """)
        elif 26 <= age <= 40:
            st.info("""
            **Early/Mid-Career Investor (26-40):**
            
            Balance growth with some stability:
            * Mix of growth stocks and established blue-chip companies
            * Begin adding some dividend stocks to your portfolio
            * Consider sector diversification to reduce overall portfolio risk
            """)
        else:  # age > 40
            st.info("""
            **Mid/Late-Career Investor (40+):**
            
            Focus increasingly on capital preservation and income:
            * Greater emphasis on established companies with strong balance sheets
            * Dividend-paying stocks become more important
            * Consider defensive sectors like consumer staples, healthcare, and utilities
            * Reduce exposure to highly volatile or speculative stocks
            """)
