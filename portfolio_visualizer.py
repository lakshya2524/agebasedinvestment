import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_portfolio_metrics(allocation, investment_amount):
    """Calculate portfolio metrics based on allocation and investment amount."""
    # This would typically involve more complex calculations with actual returns
    # For demonstration, using simplified estimates
    
    # Sample annual returns and volatility by asset class
    asset_metrics = {
        "Large Cap Stocks": {"return": 9.0, "volatility": 15.0},
        "Mid Cap Stocks": {"return": 10.0, "volatility": 18.0},
        "Small Cap Stocks": {"return": 11.0, "volatility": 22.0},
        "International Stocks": {"return": 8.5, "volatility": 17.0},
        "Government Bonds": {"return": 4.0, "volatility": 5.0},
        "Corporate Bonds": {"return": 5.0, "volatility": 7.0},
        "High Yield Bonds": {"return": 6.5, "volatility": 12.0},
        "Municipal Bonds": {"return": 3.5, "volatility": 4.5},
        "Fixed Deposits": {"return": 3.0, "volatility": 0.5}
    }
    
    # Calculate weighted metrics
    total_return = 0
    total_volatility_squared = 0  # For simplicity, assuming zero correlation
    
    for asset, percentage in allocation.items():
        if asset in asset_metrics:
            decimal_percentage = percentage / 100
            total_return += asset_metrics[asset]["return"] * decimal_percentage
            total_volatility_squared += (asset_metrics[asset]["volatility"] * decimal_percentage) ** 2
    
    # Calculate portfolio volatility
    portfolio_volatility = np.sqrt(total_volatility_squared)
    
    # Estimated 1-year projection
    projected_value = investment_amount * (1 + total_return / 100)
    
    # Calculate potential range based on volatility
    lower_range = investment_amount * (1 + (total_return - portfolio_volatility) / 100)
    upper_range = investment_amount * (1 + (total_return + portfolio_volatility) / 100)
    
    return {
        "expected_return": total_return,
        "volatility": portfolio_volatility,
        "projected_value": projected_value,
        "lower_range": lower_range,
        "upper_range": upper_range,
        "sharpe_ratio": total_return / portfolio_volatility if portfolio_volatility > 0 else 0
    }

def generate_portfolio_projection(allocation, investment_amount, years=30):
    """Generate a long-term projection of portfolio value."""
    metrics = calculate_portfolio_metrics(allocation, investment_amount)
    
    annual_return = metrics["expected_return"] / 100
    annual_volatility = metrics["volatility"] / 100
    
    # Generate yearly projections
    projection_data = []
    current_value = investment_amount
    
    for year in range(years + 1):
        # Calculate expected value
        expected_value = investment_amount * (1 + annual_return) ** year
        
        # Calculate confidence intervals (simplified)
        lower_confidence = investment_amount * np.exp((annual_return - 0.5 * annual_volatility**2) * year - 
                                                 annual_volatility * np.sqrt(year) * 1.645)  # 90% lower bound
        upper_confidence = investment_amount * np.exp((annual_return - 0.5 * annual_volatility**2) * year + 
                                                 annual_volatility * np.sqrt(year) * 1.645)  # 90% upper bound
        
        projection_data.append({
            "Year": year,
            "Expected Value": expected_value,
            "Lower Bound": lower_confidence,
            "Upper Bound": upper_confidence
        })
    
    return pd.DataFrame(projection_data)

def get_default_allocation_by_age(age):
    """Get default allocation based on age."""
    if 18 <= age <= 25:
        return {
            "Large Cap Stocks": 30,
            "Mid Cap Stocks": 20,
            "Small Cap Stocks": 15,
            "International Stocks": 15,
            "Government Bonds": 5,
            "Corporate Bonds": 7,
            "High Yield Bonds": 3,
            "Municipal Bonds": 0,
            "Fixed Deposits": 5
        }
    elif 26 <= age <= 40:
        return {
            "Large Cap Stocks": 30,
            "Mid Cap Stocks": 15,
            "Small Cap Stocks": 10,
            "International Stocks": 15,
            "Government Bonds": 10,
            "Corporate Bonds": 10,
            "High Yield Bonds": 0,
            "Municipal Bonds": 0,
            "Fixed Deposits": 10
        }
    else:  # age > 40
        return {
            "Large Cap Stocks": 25,
            "Mid Cap Stocks": 10,
            "Small Cap Stocks": 5,
            "International Stocks": 10,
            "Government Bonds": 15,
            "Corporate Bonds": 15,
            "High Yield Bonds": 0,
            "Municipal Bonds": 0,
            "Fixed Deposits": 20
        }

def show():
    """Display the portfolio visualizer page."""
    st.title("Portfolio Visualizer")
    
    st.markdown("""
    Visualize and analyze your investment portfolio allocation. See how different asset allocations 
    might perform over time and understand the risk-return tradeoff.
    """)
    
    # Get age from session state if available, otherwise default to 30
    default_age = st.session_state.get('age', 30)
    
    # Determine default allocations based on age
    default_allocation = get_default_allocation_by_age(default_age)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Portfolio Inputs")
        
        # Investment amount
        investment_amount = st.number_input(
            "Investment Amount ($)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=1000
        )
        
        # Time horizon
        time_horizon = st.slider(
            "Investment Time Horizon (Years)",
            min_value=1,
            max_value=50,
            value=20
        )
        
        st.subheader("Asset Allocation")
        
        # Stock allocation
        st.markdown("**Stocks Allocation**")
        large_cap = st.slider(
            "Large Cap Stocks (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Large Cap Stocks"]
        )
        
        mid_cap = st.slider(
            "Mid Cap Stocks (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Mid Cap Stocks"]
        )
        
        small_cap = st.slider(
            "Small Cap Stocks (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Small Cap Stocks"]
        )
        
        international = st.slider(
            "International Stocks (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["International Stocks"]
        )
        
        # Bond allocation
        st.markdown("**Bonds Allocation**")
        govt_bonds = st.slider(
            "Government Bonds (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Government Bonds"]
        )
        
        corp_bonds = st.slider(
            "Corporate Bonds (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Corporate Bonds"]
        )
        
        high_yield = st.slider(
            "High Yield Bonds (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["High Yield Bonds"]
        )
        
        muni_bonds = st.slider(
            "Municipal Bonds (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Municipal Bonds"]
        )
        
        # Cash/Fixed Deposits
        st.markdown("**Cash Allocation**")
        fixed_deposits = st.slider(
            "Fixed Deposits (%)",
            min_value=0,
            max_value=100,
            value=default_allocation["Fixed Deposits"]
        )
    
    with col2:
        # Calculate total allocation
        total_allocation = (large_cap + mid_cap + small_cap + international + 
                           govt_bonds + corp_bonds + high_yield + muni_bonds + 
                           fixed_deposits)
        
        if total_allocation != 100:
            st.warning(f"Total allocation: {total_allocation}%. Please adjust to equal 100%.")
        else:
            # Create allocation dictionary
            allocation = {
                "Large Cap Stocks": large_cap,
                "Mid Cap Stocks": mid_cap,
                "Small Cap Stocks": small_cap,
                "International Stocks": international,
                "Government Bonds": govt_bonds,
                "Corporate Bonds": corp_bonds,
                "High Yield Bonds": high_yield,
                "Municipal Bonds": muni_bonds,
                "Fixed Deposits": fixed_deposits
            }
            
            # Create pie chart for allocation
            allocation_df = pd.DataFrame({
                'Asset': list(allocation.keys()),
                'Percentage': list(allocation.values())
            })
            
            # Group into categories
            allocation_df['Category'] = 'Other'
            allocation_df.loc[allocation_df['Asset'].str.contains('Stocks'), 'Category'] = 'Stocks'
            allocation_df.loc[allocation_df['Asset'].str.contains('Bonds'), 'Category'] = 'Bonds'
            allocation_df.loc[allocation_df['Asset'].str.contains('Deposits'), 'Category'] = 'Cash'
            
            # Create grouped allocation for the summary
            grouped_allocation = allocation_df.groupby('Category')['Percentage'].sum().reset_index()
            
            # Pie chart for high-level allocation
            fig1 = px.pie(
                grouped_allocation,
                values='Percentage',
                names='Category',
                title="Portfolio Allocation by Category",
                color_discrete_sequence=px.colors.qualitative.Set1,
                hole=0.4
            )
            
            fig1.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            
            st.plotly_chart(fig1, use_container_width=True)
            
            # Detailed allocation pie chart
            fig2 = px.pie(
                allocation_df,
                values='Percentage',
                names='Asset',
                title="Detailed Portfolio Allocation",
                color_discrete_sequence=px.colors.qualitative.Plotly,
                hole=0.3
            )
            
            fig2.update_layout(
                showlegend=True,
                height=450,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
    # Only proceed if allocation is valid
    if total_allocation == 100:
        st.subheader("Portfolio Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Calculate portfolio metrics
            metrics = calculate_portfolio_metrics(allocation, investment_amount)
            
            st.markdown("**Key Portfolio Metrics**")
            st.markdown(f"* Expected Annual Return: **{metrics['expected_return']:.2f}%**")
            st.markdown(f"* Portfolio Volatility: **{metrics['volatility']:.2f}%**")
            st.markdown(f"* Sharpe Ratio: **{metrics['sharpe_ratio']:.2f}**")
            
            st.markdown("**1-Year Projection**")
            st.markdown(f"* Expected Value: **${metrics['projected_value']:,.2f}**")
            st.markdown(f"* Potential Range: **${metrics['lower_range']:,.2f}** to **${metrics['upper_range']:,.2f}**")
        
        with col2:
            # Risk assessment based on volatility
            volatility = metrics['volatility']
            
            if volatility < 8:
                risk_level = "Low"
                risk_description = "This conservative portfolio has lower volatility and is suitable for investors with a shorter time horizon or lower risk tolerance."
            elif volatility < 15:
                risk_level = "Moderate"
                risk_description = "This balanced portfolio has moderate volatility and offers a good compromise between risk and return for most investors."
            else:
                risk_level = "High"
                risk_description = "This aggressive portfolio has higher volatility and is better suited for investors with a long time horizon and higher risk tolerance."
            
            st.markdown("**Risk Assessment**")
            st.markdown(f"* Risk Level: **{risk_level}**")
            st.markdown(f"* {risk_description}")
            
            # Age-based assessment
            if 'age' in st.session_state:
                age = st.session_state['age']
                st.markdown("**Age-Based Assessment**")
                
                if age <= 25:
                    if volatility < 12:
                        st.warning("Your portfolio may be too conservative for your age. Consider increasing allocation to stocks for greater growth potential.")
                    elif volatility > 25:
                        st.info("Your portfolio is very aggressive, which aligns with your young age, but ensure you're comfortable with potential volatility.")
                    else:
                        st.success("Your portfolio has an appropriate risk level for your age, balancing growth potential with reasonable risk.")
                elif 26 <= age <= 40:
                    if volatility < 8:
                        st.warning("Your portfolio may be too conservative for your age. Consider a slightly higher allocation to stocks.")
                    elif volatility > 20:
                        st.warning("Your portfolio may be too aggressive for your age. Consider moderating risk with more fixed income.")
                    else:
                        st.success("Your portfolio has an appropriate risk level for your age, balancing growth and stability.")
                else:  # age > 40
                    if volatility < 5:
                        st.info("Your portfolio is very conservative, which may be appropriate as you approach retirement.")
                    elif volatility > 15:
                        st.warning("Your portfolio may be too aggressive for your age. Consider increasing allocation to bonds and fixed income.")
                    else:
                        st.success("Your portfolio has an appropriate risk level for your age, focusing on capital preservation while maintaining some growth potential.")
        
        # Generate portfolio projection
        projection_df = generate_portfolio_projection(allocation, investment_amount, years=time_horizon)
        
        st.subheader(f"Portfolio Projection Over {time_horizon} Years")
        
        fig = go.Figure()
        
        # Add expected value line
        fig.add_trace(go.Scatter(
            x=projection_df['Year'],
            y=projection_df['Expected Value'],
            mode='lines',
            name='Expected Value',
            line=dict(color='#636EFA', width=3)
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=projection_df['Year'],
            y=projection_df['Upper Bound'],
            mode='lines',
            name='90% Confidence Interval',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=projection_df['Year'],
            y=projection_df['Lower Bound'],
            mode='lines',
            name='90% Confidence Interval',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(99, 110, 250, 0.3)',
            showlegend=True
        ))
        
        # Update layout
        fig.update_layout(
            title="Projected Portfolio Value Over Time",
            xaxis_title="Years",
            yaxis_title="Portfolio Value ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            yaxis_tickformat='$,.0f',
            height=500,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Portfolio value table
        with st.expander("View Detailed Projection Table"):
            display_df = projection_df.copy()
            display_df["Expected Value"] = display_df["Expected Value"].map("${:,.2f}".format)
            display_df["Lower Bound"] = display_df["Lower Bound"].map("${:,.2f}".format)
            display_df["Upper Bound"] = display_df["Upper Bound"].map("${:,.2f}".format)
            
            # Select specific years to display
            if time_horizon > 10:
                years_to_show = [0, 5, 10, 15, 20, 25, 30]
                years_to_show = [y for y in years_to_show if y <= time_horizon]
                display_df = display_df[display_df['Year'].isin(years_to_show)]
            
            st.dataframe(display_df, use_container_width=True)
        
        # Asset class education
        with st.expander("Learn About Asset Classes"):
            st.markdown("""
            ### Understanding Asset Classes
            
            **Stocks (Equities):**
            * **Large Cap Stocks**: Shares of companies with market capitalization typically above $10 billion. Generally more stable than smaller companies.
            * **Mid Cap Stocks**: Companies with market capitalization between $2-10 billion. May offer more growth potential than large caps with moderate risk.
            * **Small Cap Stocks**: Companies with market capitalization below $2 billion. Higher growth potential but with increased volatility.
            * **International Stocks**: Stocks from companies outside your home country. Provides geographical diversification.
            
            **Bonds (Fixed Income):**
            * **Government Bonds**: Debt securities issued by a government. Generally considered the safest bond investments.
            * **Corporate Bonds**: Debt securities issued by corporations. Higher yields than government bonds but with more risk.
            * **High Yield Bonds**: Corporate bonds with lower credit ratings. Higher yields but with significantly more risk.
            * **Municipal Bonds**: Bonds issued by state or local governments. Interest is often tax-exempt.
            
            **Cash & Equivalents:**
            * **Fixed Deposits**: Time deposits with banks that offer guaranteed returns. Very low risk with correspondingly low returns.
            """)
