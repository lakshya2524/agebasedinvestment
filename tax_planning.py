import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_tax_questionnaire():
    """Display comprehensive tax planning questionnaire for personalized recommendations."""
    st.subheader("Personalized Tax Planning Questionnaire")
    
    st.markdown("""
    Answer the questions below to receive tailored tax-saving recommendations based on your specific financial situation.
    """)
    
    # Create form for better user experience
    with st.form("tax_questionnaire_form"):
        # Basic information
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            filing_status = st.selectbox(
                "Filing Status", 
                ["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"]
            )
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            annual_income = st.number_input("Annual Income ($)", min_value=0, max_value=1000000, value=75000, step=5000)
        
        with col2:
            spouse_age = st.number_input("Spouse Age (if applicable)", min_value=18, max_value=100, value=35)
            spouse_income = st.number_input("Spouse Annual Income (if applicable) ($)", min_value=0, max_value=1000000, value=0, step=5000)
            num_dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
        
        # Investment information
        st.subheader("Investment Information")
        col1, col2 = st.columns(2)
        
        with col1:
            taxable_investments = st.number_input("Taxable Investments Value ($)", min_value=0, max_value=10000000, value=50000, step=10000)
            retirement_accounts = st.number_input("Retirement Accounts Value ($)", min_value=0, max_value=10000000, value=100000, step=10000)
            annual_contribution = st.number_input("Annual Retirement Contribution ($)", min_value=0, max_value=30000, value=6000, step=500)
        
        with col2:
            has_401k = st.checkbox("Have access to employer 401(k)")
            has_employer_match = st.checkbox("Employer offers 401(k) match")
            has_hsa_access = st.checkbox("Have access to Health Savings Account (HSA)")
        
        # Other tax-relevant information
        st.subheader("Additional Tax Factors")
        col1, col2 = st.columns(2)
        
        with col1:
            homeowner = st.checkbox("Own a home")
            mortgage_interest = st.number_input("Annual Mortgage Interest ($)", min_value=0, max_value=50000, value=0, step=1000)
            property_taxes = st.number_input("Annual Property Taxes ($)", min_value=0, max_value=50000, value=0, step=1000)
            state_local_taxes = st.number_input("State & Local Income Taxes ($)", min_value=0, max_value=50000, value=5000, step=1000)
        
        with col2:
            has_self_employment = st.checkbox("Have self-employment income")
            has_rental_property = st.checkbox("Own rental property")
            college_expenses = st.checkbox("Have educational expenses (self or dependent)")
            medical_expenses = st.number_input("Annual Medical Expenses ($)", min_value=0, max_value=50000, value=0, step=1000)
        
        # Tax concerns and goals
        st.subheader("Tax Planning Goals")
        col1, col2 = st.columns(2)
        
        with col1:
            goals = st.multiselect(
                "Select your top tax planning goals",
                [
                    "Reduce current tax bill",
                    "Tax-efficient retirement planning",
                    "Estate/inheritance planning",
                    "Education funding",
                    "Charitable giving strategy",
                    "Business tax optimization",
                    "Real estate tax strategy"
                ],
                ["Reduce current tax bill", "Tax-efficient retirement planning"]
            )
        
        with col2:
            time_horizon = st.radio(
                "Investment Time Horizon",
                ["Short-term (< 5 years)", "Medium-term (5-15 years)", "Long-term (> 15 years)"]
            )
            risk_tolerance = st.select_slider(
                "Tax Strategy Risk Tolerance",
                options=["Conservative", "Moderate", "Aggressive"]
            )
        
        # Submit button
        submitted = st.form_submit_button("Generate Tax-Saving Recommendations")
    
    # Process form submission
    if submitted:
        st.subheader("Your Personalized Tax-Saving Recommendations")
        
        # Calculate tax bracket
        tax_bracket = calculate_tax_bracket(filing_status, annual_income, spouse_income)
        
        # Display tax bracket information
        st.markdown(f"**Current Federal Tax Bracket: {tax_bracket}%**")
        
        # Generate personalized recommendations
        recommendations = generate_tax_recommendations(
            filing_status=filing_status,
            age=age,
            spouse_age=spouse_age,
            annual_income=annual_income,
            spouse_income=spouse_income,
            num_dependents=num_dependents,
            taxable_investments=taxable_investments,
            retirement_accounts=retirement_accounts,
            annual_contribution=annual_contribution,
            has_401k=has_401k,
            has_employer_match=has_employer_match,
            has_hsa_access=has_hsa_access,
            homeowner=homeowner,
            mortgage_interest=mortgage_interest,
            property_taxes=property_taxes,
            state_local_taxes=state_local_taxes,
            has_self_employment=has_self_employment,
            has_rental_property=has_rental_property,
            college_expenses=college_expenses,
            medical_expenses=medical_expenses,
            goals=goals,
            time_horizon=time_horizon,
            risk_tolerance=risk_tolerance,
            tax_bracket=tax_bracket
        )
        
        # Display personalized recommendations
        st.markdown("### Key Tax-Saving Recommendations")
        
        # Create columns for recommendation categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Priority Recommendations")
            for i, rec in enumerate(recommendations['priority'][:5]):
                st.markdown(f"{i+1}. {rec}")
            
            st.markdown("#### Retirement Tax Strategies")
            for i, rec in enumerate(recommendations['retirement'][:3]):
                st.markdown(f"{i+1}. {rec}")
        
        with col2:
            st.markdown("#### Investment Tax Strategies")
            for i, rec in enumerate(recommendations['investment'][:3]):
                st.markdown(f"{i+1}. {rec}")
            
            st.markdown("#### Deduction Strategies")
            for i, rec in enumerate(recommendations['deduction'][:3]):
                st.markdown(f"{i+1}. {rec}")
        
        # Display potential tax savings
        st.subheader("Potential Tax Savings")
        st.markdown(f"By implementing these recommendations, you could potentially save **${calculate_potential_savings(recommendations, annual_income, spouse_income, tax_bracket):,.2f}** in taxes annually.")
        
        # Display next steps
        st.subheader("Recommended Next Steps")
        st.markdown("""
        1. **Review your current tax withholdings** to ensure you're not over or under withholding
        2. **Maximize contributions to tax-advantaged accounts** before year-end
        3. **Consult with a tax professional** to implement these strategies for your specific situation
        4. **Revisit your tax plan quarterly** to make adjustments as needed
        """)
        
        # Visualization of current vs. optimized tax situation
        create_tax_savings_chart(recommendations, annual_income, spouse_income, tax_bracket)

def calculate_tax_bracket(filing_status, annual_income, spouse_income=0):
    """Calculate the marginal tax bracket based on filing status and income."""
    total_income = annual_income
    
    if filing_status == "Married Filing Jointly":
        total_income += spouse_income
        
        # 2023 tax brackets for married filing jointly
        if total_income <= 22000:
            return 10
        elif total_income <= 89450:
            return 12
        elif total_income <= 190750:
            return 22
        elif total_income <= 364200:
            return 24
        elif total_income <= 462500:
            return 32
        elif total_income <= 693750:
            return 35
        else:
            return 37
    
    elif filing_status == "Single" or filing_status == "Married Filing Separately":
        # 2023 tax brackets for single filers
        if total_income <= 11000:
            return 10
        elif total_income <= 44725:
            return 12
        elif total_income <= 95375:
            return 22
        elif total_income <= 182100:
            return 24
        elif total_income <= 231250:
            return 32
        elif total_income <= 578125:
            return 35
        else:
            return 37
    
    elif filing_status == "Head of Household":
        # 2023 tax brackets for head of household
        if total_income <= 15700:
            return 10
        elif total_income <= 59850:
            return 12
        elif total_income <= 95350:
            return 22
        elif total_income <= 182100:
            return 24
        elif total_income <= 231250:
            return 32
        elif total_income <= 578100:
            return 35
        else:
            return 37
    
    # Default fallback
    return 22

def generate_tax_recommendations(**kwargs):
    """Generate personalized tax recommendations based on questionnaire responses."""
    # Extract key parameters from kwargs
    filing_status = kwargs.get('filing_status')
    age = kwargs.get('age')
    spouse_age = kwargs.get('spouse_age')
    annual_income = kwargs.get('annual_income')
    spouse_income = kwargs.get('spouse_income')
    num_dependents = kwargs.get('num_dependents')
    taxable_investments = kwargs.get('taxable_investments')
    retirement_accounts = kwargs.get('retirement_accounts')
    annual_contribution = kwargs.get('annual_contribution')
    has_401k = kwargs.get('has_401k')
    has_employer_match = kwargs.get('has_employer_match')
    has_hsa_access = kwargs.get('has_hsa_access')
    homeowner = kwargs.get('homeowner')
    mortgage_interest = kwargs.get('mortgage_interest')
    property_taxes = kwargs.get('property_taxes')
    state_local_taxes = kwargs.get('state_local_taxes')
    has_self_employment = kwargs.get('has_self_employment')
    has_rental_property = kwargs.get('has_rental_property')
    college_expenses = kwargs.get('college_expenses')
    medical_expenses = kwargs.get('medical_expenses')
    goals = kwargs.get('goals')
    time_horizon = kwargs.get('time_horizon')
    risk_tolerance = kwargs.get('risk_tolerance')
    tax_bracket = kwargs.get('tax_bracket')
    
    # Initialize recommendation lists
    priority_recs = []
    retirement_recs = []
    investment_recs = []
    deduction_recs = []
    
    # ----- Priority Recommendations -----
    
    # 401(k) match recommendations
    if has_401k and has_employer_match and annual_contribution < 22500:
        priority_recs.append("**Maximize 401(k) employer match** - Make sure you're contributing at least enough to get the full employer match, which is essentially free money")
    
    # HSA recommendations
    if has_hsa_access:
        priority_recs.append("**Maximize HSA contributions** - HSAs offer triple tax benefits: tax-deductible contributions, tax-free growth, and tax-free withdrawals for qualified medical expenses")
    
    # Tax bracket recommendations
    if tax_bracket >= 24:
        priority_recs.append("**Consider municipal bonds** for taxable accounts to receive tax-free interest income")
        priority_recs.append("**Explore tax loss harvesting** to offset capital gains and reduce taxable income")
    
    # Age-based recommendations
    if age >= 50 or spouse_age >= 50:
        priority_recs.append("**Make catch-up contributions** to retirement accounts (additional $7,500 for 401(k) and $1,000 for IRA in 2023)")
    
    # Self-employment recommendations
    if has_self_employment:
        priority_recs.append("**Consider a SEP IRA or Solo 401(k)** for higher contribution limits and tax deductions")
        priority_recs.append("**Track business expenses diligently** to maximize deductions")
    
    # Family-based recommendations
    if num_dependents > 0:
        priority_recs.append("**Claim Child Tax Credit** for dependents under 17")
        if college_expenses:
            priority_recs.append("**Utilize education tax credits** such as the American Opportunity Credit or Lifetime Learning Credit")
    
    # Homeowner recommendations
    if homeowner:
        total_salt = property_taxes + state_local_taxes
        if total_salt > 10000:
            priority_recs.append("**Be aware of SALT deduction limits** - State and local tax deductions are capped at $10,000")
    
    # ----- Retirement Recommendations -----
    
    # Basic retirement recommendations
    retirement_recs.append("**Maximize tax-advantaged retirement accounts** (401(k), IRA, etc.) before investing in taxable accounts")
    
    # Roth vs. Traditional recommendations
    if tax_bracket <= 22:
        retirement_recs.append("**Consider Roth contributions** which may be more beneficial at your current tax bracket, providing tax-free growth and withdrawals")
    else:
        retirement_recs.append("**Traditional pre-tax contributions** may be more beneficial to reduce your current tax bill, particularly in your higher tax bracket")
    
    # Backdoor Roth recommendations
    if annual_income > 153000 and filing_status == "Single" or (annual_income + spouse_income) > 228000 and filing_status == "Married Filing Jointly":
        retirement_recs.append("**Consider backdoor Roth IRA contribution** if you exceed income limits for direct Roth contributions")
    
    # Tax diversification
    retirement_recs.append("**Create tax diversification** by having a mix of pre-tax (Traditional), tax-free (Roth), and taxable accounts")
    
    # ----- Investment Recommendations -----
    
    # Tax-efficient placement
    investment_recs.append("**Strategic asset location**: Hold tax-inefficient investments (bonds, REITs) in tax-advantaged accounts and tax-efficient investments (index funds, growth stocks) in taxable accounts")
    
    # Long-term investing
    investment_recs.append("**Hold investments for more than one year** to qualify for lower long-term capital gains rates")
    
    # Tax-efficient funds
    investment_recs.append("**Consider tax-managed funds or ETFs** which tend to be more tax-efficient than actively managed mutual funds")
    
    # Dividend strategies
    if tax_bracket >= 24:
        investment_recs.append("**Focus on qualified dividends** which are taxed at lower capital gains rates rather than ordinary income rates")
    
    # ----- Deduction Recommendations -----
    
    # Itemized vs. standard deduction
    total_itemized = mortgage_interest + min(10000, property_taxes + state_local_taxes)
    standard_deduction = 27700 if filing_status == "Married Filing Jointly" else 13850  # 2023 standard deduction
    
    if total_itemized > standard_deduction:
        deduction_recs.append(f"**Itemize deductions** as your potential itemized deductions (${total_itemized:,.2f}) exceed the standard deduction (${standard_deduction:,.2f})")
    else:
        deduction_recs.append(f"**Take the standard deduction** as it exceeds your potential itemized deductions (${standard_deduction:,.2f} vs. ${total_itemized:,.2f})")
    
    # Charitable giving strategies
    if "Charitable giving strategy" in goals:
        deduction_recs.append("**Consider bunching charitable contributions** in alternate years to exceed the standard deduction threshold")
        deduction_recs.append("**Donate appreciated securities** instead of cash to avoid capital gains taxes while still receiving a deduction")
    
    # Medical expense deductions
    if medical_expenses > 0:
        deduction_recs.append(f"**Medical expenses** may be deductible if they exceed 7.5% of your adjusted gross income")
    
    # Combine all recommendations
    recommendations = {
        'priority': priority_recs,
        'retirement': retirement_recs,
        'investment': investment_recs,
        'deduction': deduction_recs,
    }
    
    # Ensure we have at least some recommendations in each category
    if not priority_recs:
        priority_recs.append("**Review your withholding** to ensure you're not overpaying throughout the year")
    
    return recommendations

def calculate_potential_savings(recommendations, annual_income, spouse_income=0, tax_bracket=22):
    """Estimate potential tax savings from implementing recommendations."""
    # This is a simplified estimation model
    total_income = annual_income + spouse_income
    savings = 0
    
    # Count the number of significant recommendations
    num_priority_recs = len(recommendations['priority'])
    num_total_recs = (len(recommendations['priority']) + 
                      len(recommendations['retirement']) + 
                      len(recommendations['investment']) + 
                      len(recommendations['deduction']))
    
    # Base savings on income and tax bracket
    base_savings_pct = 0.005  # 0.5% of income as base savings
    
    # Adjust based on tax bracket - higher brackets have more savings potential
    bracket_multiplier = 1.0
    if tax_bracket >= 32:
        bracket_multiplier = 2.0
    elif tax_bracket >= 24:
        bracket_multiplier = 1.5
    
    # Calculate potential savings
    savings = total_income * base_savings_pct * bracket_multiplier * min(num_priority_recs, 5)
    
    # Add impact from retirement recommendations
    for rec in recommendations['retirement']:
        if "maximize" in rec.lower():
            savings += 1000  # Simplified estimate for maximizing retirement accounts
        if "backdoor roth" in rec.lower():
            savings += 500
    
    # Add impact from investment recommendations
    for rec in recommendations['investment']:
        if "tax-managed funds" in rec.lower():
            savings += 300
        if "strategic asset location" in rec.lower():
            savings += 400
    
    # Add impact from deduction recommendations
    for rec in recommendations['deduction']:
        if "itemize deductions" in rec.lower():
            savings += 800
        if "bunch" in rec.lower():
            savings += 600
    
    # Cap the savings at a reasonable percentage of income
    max_savings = total_income * 0.05  # Max 5% savings
    savings = min(savings, max_savings)
    
    return round(savings)  # Round to nearest dollar

def create_tax_savings_chart(recommendations, annual_income, spouse_income=0, tax_bracket=22):
    """Create a visualization of potential tax savings."""
    potential_savings = calculate_potential_savings(recommendations, annual_income, spouse_income, tax_bracket)
    total_income = annual_income + spouse_income
    
    # Calculate current estimated tax and optimized tax
    estimated_current_tax = estimate_tax_liability(total_income, tax_bracket)
    optimized_tax = estimated_current_tax - potential_savings
    
    # Create comparison data
    tax_comparison = pd.DataFrame({
        'Scenario': ['Current Tax Estimate', 'Optimized Tax Strategy'],
        'Amount': [estimated_current_tax, optimized_tax]
    })
    
    # Create bar chart
    fig = px.bar(
        tax_comparison, 
        x='Scenario', 
        y='Amount',
        color='Scenario',
        text_auto='.2s',
        title="Estimated Annual Tax Comparison",
        color_discrete_map={
            'Current Tax Estimate': '#EF553B', 
            'Optimized Tax Strategy': '#00CC96'
        }
    )
    
    # Add savings annotation
    fig.add_annotation(
        x=1,
        y=optimized_tax + (potential_savings / 2),
        text=f"Potential Savings: ${potential_savings:,.2f}",
        showarrow=True,
        arrowhead=1,
        font=dict(size=14, color="#00CC96")
    )
    
    # Format y-axis as currency
    fig.update_layout(
        yaxis_tickprefix='$',
        yaxis_tickformat=',.0f'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add savings breakdown
    st.markdown("### Tax Savings Breakdown")
    
    savings_breakdown = [
        {"Category": "Retirement Strategies", "Savings": potential_savings * 0.4},
        {"Category": "Investment Tax Optimization", "Savings": potential_savings * 0.25},
        {"Category": "Deduction Maximization", "Savings": potential_savings * 0.25},
        {"Category": "Other Strategies", "Savings": potential_savings * 0.1},
    ]
    
    savings_df = pd.DataFrame(savings_breakdown)
    
    fig2 = px.pie(
        savings_df,
        values='Savings',
        names='Category',
        title="Tax Savings by Strategy Category",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    st.plotly_chart(fig2, use_container_width=True)

def estimate_tax_liability(total_income, tax_bracket):
    """Make a simplified estimate of tax liability based on income and top marginal rate."""
    # This is a very simplified estimation that doesn't account for all deductions and credits
    effective_rate = tax_bracket * 0.7  # Effective rate is typically lower than marginal rate
    return total_income * (effective_rate / 100)

def show():
    """Display the tax planning page for married and unmarried investors."""
    st.title("Tax Planning for Investors")
    
    st.markdown("""
    Effective tax planning can significantly impact your investment returns. This tool helps you understand 
    tax-efficient investment strategies based on your marital status, income level, and personal situation.
    
    Answer the questions below to get personalized tax-saving recommendations.
    """)
    
    # Create tabs for different tax planning options
    tab1, tab2, tab3 = st.tabs(["Tax Questionnaire", "Married Filing Jointly", "Single/Unmarried"])
    
    with tab1:
        show_tax_questionnaire()
    
    with tab2:
        show_married_tax_planning()
    
    with tab3:
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