import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import ui_components

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
    st.markdown("<h1 style='color: #1E3A8A;'>Age-Based Investment Allocation</h1>", unsafe_allow_html=True)
    
    # Introduction with styled container
    ui_components.styled_container(
        """
        <p style="font-size: 16px; line-height: 1.6;">
        Your age is a critical factor in determining how your investments should be allocated across different asset classes.
        The general rule is: <strong>the younger you are, the more risk you can afford to take</strong>.
        </p>
        <p style="font-size: 16px; line-height: 1.6;">
        Use this interactive tool to determine the recommended allocation for your age and life stage.
        </p>
        """,
        background_color="#F3F4F6",
        padding="25px",
        shadow=False
    )
    
    # User input section with enhanced styling
    ui_components.add_section_divider()
    st.markdown("<h2>Your Profile</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        ui_components.styled_container(
            """
            <h3 style="margin-top: 0; font-size: 1.2rem;">Enter Your Information</h3>
            """,
            background_color="#FFFFFF",
            shadow=True
        )
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
        
        if st.button("Calculate Allocation", key="calculate_allocation_btn"):
            with st.spinner("Analyzing optimal allocation..."):
                stocks, bonds, fd = get_allocation_percentages(age)
                risk_level = get_risk_level(age)
                
                # Store in session state for potential use in other pages
                st.session_state['age'] = age
                st.session_state['allocation'] = {'stocks': stocks, 'bonds': bonds, 'fd': fd}
    
    with col2:
        ui_components.styled_container(
            """
            <h3 style="margin-top: 0; font-size: 1.2rem;">Age-Based Investment Strategy</h3>
            <p>Our algorithm considers your age to determine an optimal balance between growth and security in your investment portfolio.</p>
            <ul>
                <li><strong>18-25:</strong> Maximum growth potential, higher risk tolerance</li>
                <li><strong>26-40:</strong> Growth-focused with increasing stability</li>
                <li><strong>41-55:</strong> Balanced growth and income</li>
                <li><strong>56+:</strong> Income and wealth preservation focus</li>
            </ul>
            """,
            background_color="#EFF6FF",
            shadow=False
        )
    
    # Results section
    if 'allocation' in st.session_state:
        ui_components.add_section_divider()
        
        user_age = st.session_state['age']
        stocks = st.session_state['allocation']['stocks']
        bonds = st.session_state['allocation']['bonds']
        fd = st.session_state['allocation']['fd']
        risk_level = get_risk_level(user_age)
        
        st.markdown(f"<h2>Investment Allocation for Age {user_age}</h2>", unsafe_allow_html=True)
        
        # Main allocation display with enhanced styling
        col1, col2 = st.columns([1, 1])
        
        with col1:
            ui_components.styled_container(
                f"""
                <h3 style="margin-top: 0; color: #1E3A8A; font-size: 1.2rem;">Recommended Asset Allocation</h3>
                """,
                shadow=True
            )
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                ui_components.create_metric_display("Stocks", f"{stocks}%")
            
            with metric_col2:
                ui_components.create_metric_display("Bonds/Mutual Funds", f"{bonds}%")
                
            with metric_col3:
                ui_components.create_metric_display("Fixed Deposits", f"{fd}%")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            ui_components.styled_container(
                f"""
                <h4 style="margin-top: 0; color: #1E3A8A;">Risk Tolerance Profile: <span style="color: #2563EB;">{risk_level}</span></h4>
                <p style="line-height: 1.6;">{get_risk_description(risk_level)}</p>
                """,
                background_color="#F9FAFB",
                shadow=False
            )
            
        with col2:
            pie_chart = create_allocation_pie_chart(stocks, bonds, fd)
            st.plotly_chart(pie_chart, use_container_width=True)
        
        # Detailed breakdown section
        ui_components.add_section_divider()
        st.markdown("<h2>Detailed Asset Breakdown</h2>", unsafe_allow_html=True)
        
        ui_components.styled_container(
            """
            <p>Here's a more detailed breakdown of the recommended allocations within each asset class:</p>
            """,
            background_color="#F9FAFB",
            shadow=False
        )
        
        # Detailed breakdown charts
        stock_breakdown, bond_breakdown = create_breakdown_charts(stocks, bonds, fd, user_age)
        
        tab1, tab2 = st.tabs(["Stock Breakdown", "Bond Breakdown"])
        
        with tab1:
            st.plotly_chart(stock_breakdown, use_container_width=True)
            
        with tab2:
            st.plotly_chart(bond_breakdown, use_container_width=True)
        
        # Allocation explanation section
        ui_components.add_section_divider()
        st.markdown("<h2>Your Investment Strategy Explained</h2>", unsafe_allow_html=True)
        
        if 18 <= user_age <= 25:
            ui_components.styled_container(
                """
                <h3 style="margin-top: 0; color: #1E3A8A;">Young Investors (18-25)</h3>
                <p style="line-height: 1.6;">At this age, you have the longest time horizon, allowing you to:</p>
                <ul style="line-height: 1.8;">
                    <li><strong>Take on more risk</strong> for potentially higher returns</li>
                    <li><strong>Weather market volatility</strong> and downturns</li>
                    <li><strong>Focus on capital appreciation</strong> rather than income</li>
                </ul>
                <p style="line-height: 1.6;">That's why we recommend a higher allocation to stocks, particularly growth-oriented investments.</p>
                """,
                background_color="#EFF6FF",
                shadow=True
            )
        elif 26 <= user_age <= 40:
            ui_components.styled_container(
                """
                <h3 style="margin-top: 0; color: #1E3A8A;">Early to Mid-Career Investors (26-40)</h3>
                <p style="line-height: 1.6;">At this stage, you're likely:</p>
                <ul style="line-height: 1.8;">
                    <li><strong>Building your career</strong> and increasing income</li>
                    <li><strong>Taking on more financial responsibilities</strong> like home ownership or family</li>
                    <li><strong>Still have a long time horizon</strong>, but beginning to think about future goals</li>
                </ul>
                <p style="line-height: 1.6;">We recommend maintaining a strong allocation to stocks while gradually increasing more stable investments.</p>
                """,
                background_color="#EFF6FF",
                shadow=True
            )
        else:  # age > 40
            ui_components.styled_container(
                """
                <h3 style="margin-top: 0; color: #1E3A8A;">Mid to Late Career Investors (40+)</h3>
                <p style="line-height: 1.6;">As you approach retirement:</p>
                <ul style="line-height: 1.8;">
                    <li><strong>Capital preservation</strong> becomes increasingly important</li>
                    <li><strong>Income generation</strong> starts to become a priority</li>
                    <li><strong>Recovery time</strong> from market downturns is shorter</li>
                </ul>
                <p style="line-height: 1.6;">We recommend a more balanced portfolio with increased allocation to bonds and fixed income investments.</p>
                """,
                background_color="#EFF6FF",
                shadow=True
            )
        
        # Additional guidance note
        ui_components.info_card("""
        <h4 style="margin-top: 0;">Important Note</h4>
        <p style="line-height: 1.6;">This is a general guideline based on age alone. Your actual investment allocation should consider other factors like:</p>
        <ul style="line-height: 1.8;">
            <li>Financial goals (education, home purchase, retirement)</li>
            <li>Personal risk tolerance</li>
            <li>Current financial situation (debt, emergency savings)</li>
            <li>Existing investments</li>
            <li>Time horizon for specific goals</li>
        </ul>
        <p style="line-height: 1.6;">Consider consulting with a financial advisor for personalized investment advice.</p>
        """)
