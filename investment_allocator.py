import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def get_allocation_percentages(age):
    """Calculate investment allocation percentages based on age."""
    if 18 <= age <= 25:
        stocks = 80
        bonds = 15
        fd = 5
    elif 26 <= age <= 40:
        stocks = 70
        bonds = 20
        fd = 10
    else:  # age > 40
        stocks = 50
        bonds = 30
        fd = 20
    
    return stocks, bonds, fd

def get_risk_level(age):
    """Determine risk tolerance level based on age."""
    if 18 <= age <= 25:
        return "High"
    elif 26 <= age <= 40:
        return "Medium-High"
    elif 41 <= age <= 55:
        return "Medium"
    else:  # age > 55
        return "Low-Medium"

def get_risk_description(risk_level):
    """Provide description for the risk level."""
    descriptions = {
        "High": """
        You can afford to take more risks with your investments as you have a longer time horizon to recover from potential market downturns.
        Focus on growth-oriented assets like stocks and high-growth mutual funds.
        """,
        
        "Medium-High": """
        You still have time to recover from market fluctuations, but should begin introducing some stability to your portfolio.
        A predominantly growth-focused portfolio with some defensive assets is appropriate.
        """,
        
        "Medium": """
        Balance becomes more important at this stage. You should have a mix of growth and income-producing investments.
        Begin transitioning towards more stable investments while maintaining some growth elements.
        """,
        
        "Low-Medium": """
        Capital preservation becomes a priority as retirement approaches or has begun.
        Focus on income-generating investments with lower volatility, while maintaining some exposure to growth assets to combat inflation.
        """
    }
    
    return descriptions.get(risk_level, "")

def create_allocation_pie_chart(stocks, bonds, fd):
    """Create a pie chart for investment allocation."""
    labels = ['Stocks', 'Bonds/Mutual Funds', 'Fixed Deposits']
    values = [stocks, bonds, fd]
    colors = ['#636EFA', '#EF553B', '#00CC96']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title_text="Recommended Investment Allocation",
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    return fig

def create_breakdown_charts(stocks, bonds, fd, age):
    """Create detailed breakdown charts for each investment category."""
    
    # Stock allocation breakdown
    if 18 <= age <= 25:
        stock_breakdown = {
            'Large Cap': 30,
            'Mid Cap': 30,
            'Small Cap': 25,
            'International': 15
        }
    elif 26 <= age <= 40:
        stock_breakdown = {
            'Large Cap': 40,
            'Mid Cap': 25,
            'Small Cap': 20,
            'International': 15
        }
    else:  # age > 40
        stock_breakdown = {
            'Large Cap': 50,
            'Mid Cap': 20,
            'Small Cap': 15,
            'International': 15
        }
    
    # Bond allocation breakdown
    if 18 <= age <= 25:
        bond_breakdown = {
            'Government Bonds': 30,
            'Corporate Bonds': 40,
            'Municipal Bonds': 10,
            'High-Yield Bonds': 20
        }
    elif 26 <= age <= 40:
        bond_breakdown = {
            'Government Bonds': 40,
            'Corporate Bonds': 35,
            'Municipal Bonds': 15,
            'High-Yield Bonds': 10
        }
    else:  # age > 40
        bond_breakdown = {
            'Government Bonds': 50,
            'Corporate Bonds': 30,
            'Municipal Bonds': 15,
            'High-Yield Bonds': 5
        }
    
    # Create dataframes for plotting
    stock_df = pd.DataFrame(list(stock_breakdown.items()), columns=['Category', 'Percentage'])
    bond_df = pd.DataFrame(list(bond_breakdown.items()), columns=['Category', 'Percentage'])
    
    stock_fig = px.bar(
        stock_df, 
        x='Category', 
        y='Percentage',
        title="Stock Allocation Breakdown",
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    bond_fig = px.bar(
        bond_df, 
        x='Category', 
        y='Percentage',
        title="Bond/Mutual Fund Allocation Breakdown",
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    return stock_fig, bond_fig

def show():
    """Display the age-based investment allocation page."""
    st.title("Age-Based Investment Allocation")
    
    st.markdown("""
    Your age is a critical factor in determining how your investments should be allocated across different asset classes. 
    The general rule is: the younger you are, the more risk you can afford to take.
    
    Use this tool to determine the recommended allocation for your age.
    """)
    
    age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
    
    if st.button("Calculate Allocation"):
        stocks, bonds, fd = get_allocation_percentages(age)
        risk_level = get_risk_level(age)
        
        # Store in session state for potential use in other pages
        st.session_state['age'] = age
        st.session_state['allocation'] = {'stocks': stocks, 'bonds': bonds, 'fd': fd}
        
        st.subheader(f"Investment Allocation for Age {age}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            * **Stocks: {stocks}%**
            * **Bonds/Mutual Funds: {bonds}%**
            * **Fixed Deposits: {fd}%**
            
            **Risk Tolerance Level: {risk_level}**
            """)
            st.markdown(get_risk_description(risk_level))
            
        with col2:
            pie_chart = create_allocation_pie_chart(stocks, bonds, fd)
            st.plotly_chart(pie_chart, use_container_width=True)
        
        st.subheader("Detailed Breakdown")
        st.markdown("Here's a more detailed breakdown of the recommended allocations within each asset class:")
        
        # Detailed breakdown charts
        stock_breakdown, bond_breakdown = create_breakdown_charts(stocks, bonds, fd, age)
        
        st.plotly_chart(stock_breakdown, use_container_width=True)
        st.plotly_chart(bond_breakdown, use_container_width=True)
        
        st.subheader("Allocation Explanation")
        
        if 18 <= age <= 25:
            st.markdown("""
            **Young Investors (18-25)**
            
            At this age, you have the longest time horizon, allowing you to:
            * Take on more risk for potentially higher returns
            * Weather market volatility and downturns
            * Focus on capital appreciation rather than income
            
            That's why we recommend a higher allocation to stocks, particularly growth-oriented investments.
            """)
        elif 26 <= age <= 40:
            st.markdown("""
            **Early to Mid-Career Investors (26-40)**
            
            At this stage, you're likely:
            * Building your career and increasing income
            * Starting to have more financial responsibilities
            * Still have a long time horizon, but beginning to think about future goals
            
            We recommend maintaining a strong allocation to stocks while gradually increasing more stable investments.
            """)
        else:  # age > 40
            st.markdown("""
            **Mid to Late Career Investors (40+)**
            
            As you approach retirement:
            * Capital preservation becomes increasingly important
            * Income generation starts to become a priority
            * Recovery time from market downturns is shorter
            
            We recommend a more balanced portfolio with increased allocation to bonds and fixed income investments.
            """)
            
        st.info("""
        **Note:** This is a general guideline based on age alone. Your actual investment allocation should consider other factors like:
        * Financial goals
        * Risk tolerance
        * Current financial situation
        * Existing investments
        * Time horizon for specific goals
        """)
