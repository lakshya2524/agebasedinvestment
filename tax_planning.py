import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    """Display the tax planning page for married and unmarried investors."""
    st.title("Tax Planning for Investors")
    
    st.markdown("""
    Effective tax planning can significantly impact your investment returns. This tool helps you understand 
    tax-efficient investment strategies based on your marital status and income level.
    """)
    
    # Create tabs for married and unmarried investors
    tab1, tab2 = st.tabs(["Married Filing Jointly", "Single/Unmarried"])
    
    with tab1:
        show_married_tax_planning()
    
    with tab2:
        show_single_tax_planning()
    
    # General tax planning advice
    st.subheader("Universal Tax-Efficient Investment Strategies")
    
    st.markdown("""
    ### Key Tax-Efficient Investment Strategies
    
    1. **Maximize Tax-Advantaged Accounts**
       * 401(k)s and traditional IRAs offer tax-deferred growth
       * Roth accounts provide tax-free growth and withdrawals
       * HSAs offer triple tax advantages for healthcare expenses
       
    2. **Strategic Asset Location**
       * Hold tax-inefficient investments (bonds, REITs) in tax-advantaged accounts
       * Keep tax-efficient investments (index funds, growth stocks) in taxable accounts
       
    3. **Tax-Loss Harvesting**
       * Offset capital gains by selling investments at a loss
       * Be mindful of wash-sale rules when repurchasing similar investments
       
    4. **Qualified Dividend Income**
       * Qualified dividends are taxed at lower capital gains rates
       * Hold dividend-paying stocks for required periods to qualify
       
    5. **Municipal Bonds**
       * Interest from municipal bonds is often exempt from federal taxes
       * Local municipal bonds may also be exempt from state and local taxes
    """)
    
    # Disclaimer
    st.warning("""
    **Disclaimer:** This information is for educational purposes only and should not be considered tax advice. 
    Tax laws change frequently and vary by location. Consult with a qualified tax professional for advice 
    specific to your situation.
    """)

def show_married_tax_planning():
    """Display tax planning content for married couples filing jointly."""
    st.subheader("Tax Planning for Married Couples")
    
    st.markdown("""
    Married couples filing jointly have unique tax planning opportunities and considerations 
    that can significantly impact their investment strategy.
    """)
    
    # Income input for tax bracket calculation
    col1, col2 = st.columns([1, 1])
    
    with col1:
        joint_income = st.number_input("Annual Household Income ($)", min_value=0, max_value=2000000, value=100000, step=5000)
        
        # Determine tax bracket based on 2023 rates for married filing jointly
        if joint_income <= 22000:
            tax_bracket = "10%"
            marginal_rate = 10
        elif joint_income <= 89450:
            tax_bracket = "12%"
            marginal_rate = 12
        elif joint_income <= 190750:
            tax_bracket = "22%"
            marginal_rate = 22
        elif joint_income <= 364200:
            tax_bracket = "24%"
            marginal_rate = 24
        elif joint_income <= 462500:
            tax_bracket = "32%"
            marginal_rate = 32
        elif joint_income <= 693750:
            tax_bracket = "35%"
            marginal_rate = 35
        else:
            tax_bracket = "37%"
            marginal_rate = 37
        
        st.markdown(f"**Current Federal Tax Bracket: {tax_bracket}**")
        
        # Additional inputs
        has_children = st.checkbox("Do you have dependent children?")
        own_home = st.checkbox("Do you own a home?")
        both_working = st.checkbox("Are both spouses employed?")
        age_over_50 = st.checkbox("Is either spouse over 50?")
    
    with col2:
        # Visualize tax brackets
        brackets = ["10%", "12%", "22%", "24%", "32%", "35%", "37%"]
        incomes = [22000, 89450, 190750, 364200, 462500, 693750, 1000000]
        rates = [10, 12, 22, 24, 32, 35, 37]
        
        fig = go.Figure()
        
        # Create bar chart of tax brackets
        fig.add_trace(go.Bar(
            x=brackets,
            y=rates,
            marker_color=['#636EFA', '#636EFA', '#636EFA', '#636EFA', '#636EFA', '#636EFA', '#636EFA'],
            text=rates,
            textposition='auto',
            name='Marginal Tax Rate'
        ))
        
        # Highlight current bracket
        bracket_colors = ['#636EFA'] * 7
        current_index = brackets.index(tax_bracket)
        bracket_colors[current_index] = '#EF553B'
        
        fig.update_traces(marker_color=bracket_colors)
        
        fig.update_layout(
            title="2023 Married Filing Jointly Tax Brackets",
            xaxis_title="Tax Brackets",
            yaxis_title="Marginal Rate (%)",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommended strategies based on inputs
    st.subheader("Recommended Tax Strategies")
    
    # Base recommendations for all married couples
    strategies = [
        "**Income Splitting**: Balance investments between spouses to optimize tax efficiency",
        "**Joint Contributions**: Maximize both spouses' retirement account contributions",
        "**Gift Tax Exclusion**: Utilize the annual gift tax exclusion for wealth transfer",
        "**Estate Planning**: Consider joint trusts and estate tax exemptions"
    ]
    
    # Add conditional recommendations
    if marginal_rate >= 24:
        strategies.append("**Municipal Bonds**: Consider tax-exempt municipal bonds to reduce taxable income")
        strategies.append("**Tax Loss Harvesting**: Actively manage investment losses to offset gains")
    
    if has_children:
        strategies.append("**529 Plans**: Utilize education savings plans for tax-free growth for children's education")
        strategies.append("**Child Tax Credits**: Factor in available credits in your tax planning")
    
    if own_home:
        strategies.append("**Mortgage Interest**: Deduct mortgage interest to reduce taxable income")
        strategies.append("**Home Equity**: Consider strategic use of home equity within allowed tax deduction limits")
    
    if both_working:
        strategies.append("**Spousal IRAs**: Consider spousal IRAs to double retirement contribution limits")
        strategies.append("**Coordinate Benefits**: Optimize health insurance and other benefits across both employers")
    
    if age_over_50:
        strategies.append("**Catch-up Contributions**: Take advantage of catch-up contributions to retirement accounts")
        strategies.append("**Social Security Planning**: Coordinate when each spouse claims Social Security benefits")
    
    # Display strategies as bullet points
    for strategy in strategies:
        st.markdown(f"* {strategy}")
    
    # Tax-advantaged account comparison
    st.subheader("Tax-Advantaged Investment Options for Married Couples")
    
    # Simplified comparison table
    tax_accounts = {
        "Account Type": [
            "Joint Taxable Account", 
            "Traditional IRA (each spouse)", 
            "Roth IRA (each spouse)", 
            "401(k) (each spouse)", 
            "HSA (family)"
        ],
        "2023 Contribution Limit": [
            "Unlimited", 
            "$6,500 ($7,500 if 50+)", 
            "$6,500 ($7,500 if 50+)", 
            "$22,500 ($30,000 if 50+)", 
            "$7,750"
        ],
        "Tax Benefit": [
            "Capital gains rates on long-term gains",
            "Tax-deductible contributions, tax-deferred growth",
            "Tax-free growth and qualified withdrawals",
            "Tax-deductible contributions, tax-deferred growth",
            "Triple tax advantage: deductible contributions, tax-free growth, tax-free withdrawals for healthcare"
        ]
    }
    
    account_df = pd.DataFrame(tax_accounts)
    st.table(account_df)
    
    # Show income-splitting advantage
    st.subheader("Benefits of Income Splitting Between Spouses")
    
    # Example calculation
    st.markdown("""
    ### Example: Tax-Efficient Asset Location Between Spouses
    
    Consider a married couple with the following investments:
    
    * $200,000 in dividend-paying stocks (4% annual dividend yield)
    * $200,000 in corporate bonds (5% interest yield)
    * $100,000 in growth stocks (minimal dividends)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Inefficient Allocation")
        st.markdown("""
        **Spouse 1 (Higher Income):**
        * $200,000 in corporate bonds
        * $100,000 in growth stocks
        
        **Spouse 2 (Lower Income):**
        * $200,000 in dividend-paying stocks
        """)
    
    with col2:
        st.markdown("#### Efficient Allocation")
        st.markdown("""
        **Spouse 1 (Higher Income):**
        * $100,000 in growth stocks
        * $100,000 in municipal bonds (tax-free)
        
        **Spouse 2 (Lower Income):**
        * $200,000 in dividend-paying stocks
        * $100,000 in corporate bonds
        """)
    
    st.info("""
    By placing income-generating investments (bonds, dividend stocks) with the spouse in a lower tax bracket, 
    and tax-efficient investments (growth stocks, municipal bonds) with the spouse in a higher tax bracket, 
    the couple can minimize their overall tax burden.
    """)

def show_single_tax_planning():
    """Display tax planning content for single/unmarried individuals."""
    st.subheader("Tax Planning for Single/Unmarried Investors")
    
    st.markdown("""
    Single filers have different tax brackets and considerations compared to married couples. 
    Effective tax planning can help maximize your investment returns.
    """)
    
    # Income input for tax bracket calculation
    col1, col2 = st.columns([1, 1])
    
    with col1:
        single_income = st.number_input("Annual Income ($)", min_value=0, max_value=1000000, value=70000, step=5000, key="single_income")
        
        # Determine tax bracket based on 2023 rates for single filers
        if single_income <= 11000:
            tax_bracket = "10%"
            marginal_rate = 10
        elif single_income <= 44725:
            tax_bracket = "12%"
            marginal_rate = 12
        elif single_income <= 95375:
            tax_bracket = "22%"
            marginal_rate = 22
        elif single_income <= 182100:
            tax_bracket = "24%"
            marginal_rate = 24
        elif single_income <= 231250:
            tax_bracket = "32%"
            marginal_rate = 32
        elif single_income <= 578125:
            tax_bracket = "35%"
            marginal_rate = 35
        else:
            tax_bracket = "37%"
            marginal_rate = 37
        
        st.markdown(f"**Current Federal Tax Bracket: {tax_bracket}**")
        
        # Additional inputs
        has_dependents = st.checkbox("Do you have dependents?", key="single_depends")
        own_home = st.checkbox("Do you own a home?", key="single_home")
        age_over_50 = st.checkbox("Are you over 50?", key="single_age")
        has_business = st.checkbox("Do you have self-employment income?")
    
    with col2:
        # Visualize tax brackets
        brackets = ["10%", "12%", "22%", "24%", "32%", "35%", "37%"]
        incomes = [11000, 44725, 95375, 182100, 231250, 578125, 1000000]
        rates = [10, 12, 22, 24, 32, 35, 37]
        
        fig = go.Figure()
        
        # Create bar chart of tax brackets
        fig.add_trace(go.Bar(
            x=brackets,
            y=rates,
            marker_color=['#636EFA', '#636EFA', '#636EFA', '#636EFA', '#636EFA', '#636EFA', '#636EFA'],
            text=rates,
            textposition='auto',
            name='Marginal Tax Rate'
        ))
        
        # Highlight current bracket
        bracket_colors = ['#636EFA'] * 7
        current_index = brackets.index(tax_bracket)
        bracket_colors[current_index] = '#EF553B'
        
        fig.update_traces(marker_color=bracket_colors)
        
        fig.update_layout(
            title="2023 Single Filer Tax Brackets",
            xaxis_title="Tax Brackets",
            yaxis_title="Marginal Rate (%)",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommended strategies based on inputs
    st.subheader("Recommended Tax Strategies")
    
    # Base recommendations for all single filers
    strategies = [
        "**Tax-Advantaged Accounts**: Maximize contributions to 401(k), IRA, and HSA",
        "**Tax-Efficient Fund Placement**: Keep tax-efficient investments in taxable accounts",
        "**Long-term Investing**: Hold investments for 1+ years for lower capital gains rates",
        "**Tax-Loss Harvesting**: Offset capital gains with capital losses"
    ]
    
    # Add conditional recommendations
    if marginal_rate >= 24:
        strategies.append("**Municipal Bonds**: Consider tax-exempt municipal bonds to reduce taxable income")
        strategies.append("**Tax-Managed Funds**: Invest in funds designed to minimize taxable distributions")
    
    if has_dependents:
        strategies.append("**Head of Household Status**: File as head of household if eligible for better tax rates")
        strategies.append("**Dependent Care FSA**: Utilize pre-tax dollars for qualifying dependent care expenses")
    
    if own_home:
        strategies.append("**Mortgage Interest**: Deduct mortgage interest to reduce taxable income")
        strategies.append("**Home Office Deduction**: Consider if you work from home regularly")
    
    if age_over_50:
        strategies.append("**Catch-up Contributions**: Make additional catch-up contributions to retirement accounts")
        strategies.append("**Social Security Strategy**: Plan optimal timing for claiming benefits")
    
    if has_business:
        strategies.append("**Solo 401(k)/SEP IRA**: Consider self-employed retirement plans with higher contribution limits")
        strategies.append("**Qualified Business Income Deduction**: Take advantage of the 20% pass-through deduction if eligible")
    
    # Display strategies as bullet points
    for strategy in strategies:
        st.markdown(f"* {strategy}")
    
    # Compare Traditional vs. Roth retirement accounts
    st.subheader("Traditional vs. Roth: Which is Better for Single Filers?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Consider Traditional If:")
        st.markdown("""
        * You expect to be in a **lower** tax bracket in retirement
        * You want to reduce your current taxable income
        * You're in your peak earning years
        * You want to diversify your tax exposure with a mix of accounts
        """)
    
    with col2:
        st.markdown("#### Consider Roth If:")
        st.markdown("""
        * You expect to be in a **higher** tax bracket in retirement
        * You're early in your career with lower income
        * You want tax-free withdrawals in retirement
        * You want to leave tax-free assets to heirs
        """)
    
    # Calculator for Traditional vs. Roth comparison
    st.subheader("Traditional vs. Roth Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment_amount = st.number_input("Annual Contribution ($)", min_value=100, max_value=30000, value=6000, step=500)
        years_to_retirement = st.number_input("Years Until Retirement", min_value=1, max_value=50, value=25)
        current_tax_rate = st.slider("Current Tax Rate (%)", min_value=10, max_value=37, value=marginal_rate)
        retirement_tax_rate = st.slider("Expected Retirement Tax Rate (%)", min_value=10, max_value=37, value=marginal_rate-5)
        annual_return = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=12.0, value=7.0, step=0.5)
    
    # Calculate outcomes
    annual_return_decimal = annual_return / 100
    current_tax_decimal = current_tax_rate / 100
    retirement_tax_decimal = retirement_tax_rate / 100
    
    # Traditional IRA (pre-tax contribution, taxed withdrawal)
    traditional_annual = investment_amount  # Pre-tax amount
    traditional_annual_after_tax = traditional_annual  # No tax on contribution
    traditional_future_value = traditional_annual * ((1 + annual_return_decimal) ** years_to_retirement - 1) / annual_return_decimal * (1 + annual_return_decimal)
    traditional_after_tax = traditional_future_value * (1 - retirement_tax_decimal)
    
    # Roth IRA (post-tax contribution, tax-free withdrawal)
    roth_annual = investment_amount  # Post-tax amount
    roth_annual_after_tax = roth_annual * (1 - current_tax_decimal)  # Pay tax now
    roth_future_value = roth_annual_after_tax * ((1 + annual_return_decimal) ** years_to_retirement - 1) / annual_return_decimal * (1 + annual_return_decimal)
    roth_after_tax = roth_future_value  # No tax on withdrawal
    
    # Equal after-tax contribution comparison
    equal_contribution_traditional = investment_amount / (1 - current_tax_decimal)
    equal_contribution_traditional_future = equal_contribution_traditional * ((1 + annual_return_decimal) ** years_to_retirement - 1) / annual_return_decimal * (1 + annual_return_decimal)
    equal_contribution_traditional_after_tax = equal_contribution_traditional_future * (1 - retirement_tax_decimal)
    
    with col2:
        # Display results
        st.markdown("#### Results")
        st.markdown(f"**Future Value (Traditional):** ${traditional_future_value:,.2f}")
        st.markdown(f"**After-Tax Value (Traditional):** ${traditional_after_tax:,.2f}")
        st.markdown(f"**Future Value (Roth):** ${roth_future_value:,.2f}")
        st.markdown(f"**After-Tax Value (Roth):** ${roth_after_tax:,.2f}")
        
        # Add recommendation based on results
        if traditional_after_tax > roth_after_tax:
            st.success(f"**Recommendation:** Traditional account may be better. You could have ${traditional_after_tax - roth_after_tax:,.2f} more in retirement.")
        elif roth_after_tax > traditional_after_tax:
            st.success(f"**Recommendation:** Roth account may be better. You could have ${roth_after_tax - traditional_after_tax:,.2f} more in retirement.")
        else:
            st.info("**Recommendation:** Both account types provide similar benefits. Consider diversifying with both types.")
    
    # Add bar chart to compare
    results_df = pd.DataFrame({
        'Account Type': ['Traditional', 'Roth'],
        'After-Tax Value': [traditional_after_tax, roth_after_tax]
    })
    
    fig = px.bar(
        results_df, 
        x='Account Type', 
        y='After-Tax Value',
        color='Account Type',
        text_auto='.2s',
        title="Projected After-Tax Retirement Value",
        color_discrete_map={'Traditional': '#636EFA', 'Roth': '#EF553B'}
    )
    
    fig.update_layout(
        yaxis_tickprefix='$',
        yaxis_tickformat=',.0f'
    )
    
    st.plotly_chart(fig, use_container_width=True)