import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def calculate_retirement_savings(current_age, retirement_age, life_expectancy, current_savings, 
                                 monthly_contribution, annual_return, inflation_rate, 
                                 retirement_income_need):
    """
    Calculate retirement savings and determine if goals can be met.
    
    Parameters:
    - current_age: Current age of the individual
    - retirement_age: Expected retirement age
    - life_expectancy: Expected life expectancy
    - current_savings: Current retirement savings
    - monthly_contribution: Monthly contribution to retirement savings
    - annual_return: Expected annual investment return (pre-retirement)
    - inflation_rate: Expected annual inflation rate
    - retirement_income_need: Annual income needed during retirement
    
    Returns:
    - Dictionary containing calculation results
    """
    # Convert percentages to decimals
    annual_return_decimal = annual_return / 100
    inflation_rate_decimal = inflation_rate / 100
    
    # Post-retirement investment return (typically more conservative)
    post_retirement_return = max(annual_return_decimal - 0.02, 0.03)  # 2% less than pre-retirement, min 3%
    
    # Time periods
    years_to_retirement = retirement_age - current_age
    retirement_years = life_expectancy - retirement_age
    
    # Calculate future value of current savings at retirement
    future_value_current_savings = current_savings * (1 + annual_return_decimal) ** years_to_retirement
    
    # Calculate future value of monthly contributions at retirement
    # Formula: PMT * (((1 + r)^n - 1) / r)
    annual_contribution = monthly_contribution * 12
    future_value_contributions = annual_contribution * ((1 + annual_return_decimal) ** years_to_retirement - 1) / annual_return_decimal
    if annual_return_decimal > 0:
        future_value_contributions *= (1 + annual_return_decimal)
    
    # Total savings at retirement
    total_retirement_savings = future_value_current_savings + future_value_contributions
    
    # Adjust retirement income need for inflation at retirement age
    inflation_adjusted_income = retirement_income_need * (1 + inflation_rate_decimal) ** years_to_retirement
    
    # Calculate sustainable withdrawal rate (4% rule adjusted for shorter/longer retirements)
    base_withdrawal_rate = 0.04  # 4% rule as baseline
    adjustment_factor = 25 / retirement_years  # 25 years is the standard for 4% rule
    adjusted_withdrawal_rate = base_withdrawal_rate * adjustment_factor
    capped_withdrawal_rate = max(min(adjusted_withdrawal_rate, 0.05), 0.03)  # Cap between 3% and 5%
    
    # Calculate sustainable annual withdrawal
    sustainable_withdrawal = total_retirement_savings * capped_withdrawal_rate
    
    # Check if retirement savings are adequate
    income_gap = inflation_adjusted_income - sustainable_withdrawal
    is_sufficient = income_gap <= 0
    
    # Calculate additional savings needed (if there's a gap)
    additional_monthly_savings = 0
    if not is_sufficient and years_to_retirement > 0:
        additional_total_needed = income_gap / capped_withdrawal_rate
        # Calculate the PMT formula in reverse to find required additional monthly contribution
        r = annual_return_decimal
        n = years_to_retirement
        additional_annual_savings = additional_total_needed / (((1 + r) ** n - 1) / r * (1 + r))
        additional_monthly_savings = additional_annual_savings / 12
    
    # Generate yearly projection data
    projection_data = []
    
    # Pre-retirement projection
    current_balance = current_savings
    for year in range(years_to_retirement + 1):
        age = current_age + year
        projection_data.append({
            "Age": age,
            "Year": datetime.now().year + year,
            "Balance": current_balance,
            "Phase": "Accumulation"
        })
        if year < years_to_retirement:  # Don't compound after the last accumulation year
            current_balance = current_balance * (1 + annual_return_decimal) + annual_contribution
    
    # Post-retirement projection
    for year in range(1, retirement_years + 1):
        age = retirement_age + year
        withdrawal = inflation_adjusted_income * (1 + inflation_rate_decimal) ** (year - 1)
        current_balance = max(0, (current_balance - withdrawal) * (1 + post_retirement_return))
        projection_data.append({
            "Age": age,
            "Year": datetime.now().year + years_to_retirement + year,
            "Balance": current_balance,
            "Phase": "Distribution"
        })
    
    return {
        "total_retirement_savings": total_retirement_savings,
        "inflation_adjusted_income": inflation_adjusted_income,
        "sustainable_withdrawal": sustainable_withdrawal,
        "income_gap": income_gap,
        "is_sufficient": is_sufficient,
        "withdrawal_rate": capped_withdrawal_rate * 100,  # Convert back to percentage
        "additional_monthly_savings": additional_monthly_savings,
        "projection_data": projection_data
    }

def show():
    """Display the retirement calculator page."""
    st.title("Retirement Calculator")
    
    st.markdown("""
    Plan for your retirement by estimating how much you need to save and whether you're on track to meet your goals.
    
    Enter your information below to calculate your retirement readiness.
    """)
    
    # Get age from session state if available, otherwise default to 30
    default_age = st.session_state.get('age', 30)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        current_age = st.number_input("Current Age", min_value=18, max_value=80, value=default_age)
        retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, max_value=90, value=65)
        life_expectancy = st.number_input("Life Expectancy", min_value=retirement_age + 1, max_value=120, value=85)
        
        st.subheader("Financial Information")
        current_savings = st.number_input("Current Retirement Savings ($)", min_value=0, value=50000)
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0, value=500)
    
    with col2:
        st.subheader("Retirement Goals")
        retirement_income_need = st.number_input("Annual Income Needed in Retirement ($)", min_value=0, value=60000)
        
        st.subheader("Assumptions")
        annual_return = st.slider("Expected Annual Investment Return (%)", min_value=1.0, max_value=12.0, value=7.0, step=0.1)
        inflation_rate = st.slider("Expected Annual Inflation Rate (%)", min_value=1.0, max_value=7.0, value=2.5, step=0.1)
    
    if st.button("Calculate Retirement Plan"):
        with st.spinner("Calculating retirement projections..."):
            # Calculate retirement projections
            results = calculate_retirement_savings(
                current_age=current_age,
                retirement_age=retirement_age,
                life_expectancy=life_expectancy,
                current_savings=current_savings,
                monthly_contribution=monthly_contribution,
                annual_return=annual_return,
                inflation_rate=inflation_rate,
                retirement_income_need=retirement_income_need
            )
            
            # Display results
            st.subheader("Retirement Projection")
            
            # Summary metrics
            st.markdown(f"""
            **Summary at Retirement (Age {retirement_age}):**
            * Estimated savings at retirement: **${results['total_retirement_savings']:,.2f}**
            * Annual income needed (inflation-adjusted): **${results['inflation_adjusted_income']:,.2f}**
            * Sustainable annual withdrawal: **${results['sustainable_withdrawal']:,.2f}**
            * Sustainable withdrawal rate: **{results['withdrawal_rate']:.2f}%**
            """)
            
            # Outcome visualization
            if results['is_sufficient']:
                st.success(f"✅ Your retirement plan is on track! Your projected savings should be sufficient for your retirement needs.")
            else:
                st.error(f"⚠️ Retirement income gap detected: **${abs(results['income_gap']):,.2f}** per year")
                st.warning(f"To close this gap, consider increasing your monthly contribution by **${results['additional_monthly_savings']:,.2f}**")
            
            # Create projection chart
            projection_df = pd.DataFrame(results['projection_data'])
            
            fig = px.area(
                projection_df, 
                x="Age", 
                y="Balance",
                color="Phase",
                title="Projected Retirement Savings Over Time",
                color_discrete_map={"Accumulation": "#636EFA", "Distribution": "#EF553B"}
            )
            
            # Add vertical line at retirement age
            fig.add_vline(x=retirement_age, line_dash="dash", line_color="gray", 
                         annotation_text="Retirement", annotation_position="top right")
            
            # Format y-axis as currency
            fig.update_layout(
                yaxis_tickprefix='$',
                yaxis_tickformat=',.0f',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed projection table
            with st.expander("View Detailed Projection Table"):
                # Format the table for display
                display_df = projection_df.copy()
                display_df["Balance"] = display_df["Balance"].map("${:,.2f}".format)
                st.dataframe(display_df)
            
            st.subheader("Retirement Planning Insights")
            
            # Provide age-specific insights
            if current_age <= 25:
                st.info("""
                **Young Investor Advantage:**
                Starting early gives you a tremendous advantage due to compound interest. Even small contributions now can grow significantly over time.
                Consider maximizing growth-oriented investments given your long time horizon.
                """)
            elif current_age <= 40:
                st.info("""
                **Mid-Career Strategy:**
                This is typically when your earning power increases. Consider increasing your retirement contributions as your income grows.
                Balance growth with some more stable investments as your portfolio size increases.
                """)
            else:
                st.info("""
                **Pre-Retirement Adjustments:**
                As you get closer to retirement, consider moving some investments to more conservative options to protect your savings.
                Catch-up contributions are available for many retirement accounts for those over 50.
                """)
            
            # General retirement planning tips
            st.markdown("""
            **Key Retirement Planning Tips:**
            
            1. **Consider tax-advantaged accounts** like 401(k), IRAs, or Roth accounts to maximize savings
            2. **Review and adjust your plan annually** as circumstances change
            3. **Account for healthcare costs** which typically increase during retirement
            4. **Social Security benefits** can supplement your retirement income (not included in this calculator)
            5. **Consider working with a financial advisor** for personalized retirement planning
            """)
