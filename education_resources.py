import streamlit as st
import pandas as pd

def show():
    """Display the investment education resources page."""
    st.title("Investment Education Resources")
    
    st.markdown("""
    Education is key to making informed investment decisions. This page provides basic resources 
    to help you understand investment principles, strategies, and best practices.
    """)
    
    # Create tabs for different educational topics
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Investment Basics", 
        "Age-Based Strategies", 
        "Stocks & Bonds", 
        "Retirement Planning",
        "Glossary"
    ])
    
    with tab1:
        st.subheader("Investment Basics")
        
        st.markdown("""
        ### Key Investment Principles
        
        #### 1. Start Early
        The power of compounding means the earlier you start investing, the more time your money has to grow.
        
        #### 2. Diversification
        Spreading investments across different asset classes helps reduce risk. Don't put all your eggs in one basket.
        
        #### 3. Risk vs. Return
        Higher potential returns typically come with higher risk. Understanding your risk tolerance is crucial.
        
        #### 4. Regular Investing
        Consistent, regular investments over time can help smooth out market volatility through dollar-cost averaging.
        
        #### 5. Long-Term Perspective
        Successful investing requires patience. Short-term market movements should not derail long-term strategies.
        
        ### Understanding Asset Classes
        
        **Stocks (Equities)**: Represent ownership in a company. Historically provide higher returns with higher volatility.
        
        **Bonds (Fixed Income)**: Loans to companies or governments. Generally more stable than stocks but with lower returns.
        
        **Cash and Equivalents**: Includes savings accounts, fixed deposits, and money market funds. Lowest risk but also lowest returns.
        
        **Alternative Investments**: Real estate, commodities, cryptocurrencies, etc. May offer diversification benefits but often with unique risks.
        """)
        
        st.info("""
        **The Rule of 72**
        
        A simple way to estimate how long it will take for an investment to double:
        
        Years to Double = 72 ÷ Annual Return Rate
        
        Example: At a 7% annual return, an investment will double in approximately 10.3 years (72 ÷ 7 = 10.3)
        """)
    
    with tab2:
        st.subheader("Age-Based Investment Strategies")
        
        st.markdown("""
        ### How Age Affects Investment Strategy
        
        Your age is one of the most important factors in determining your investment strategy. As you age, your financial goals, risk tolerance, and time horizon typically change.
        
        ### Investment Approach by Age Group
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### Young Investors (18-25)
            
            **Time Horizon:** Very long (40+ years)
            
            **Risk Tolerance:** High
            
            **Recommended Allocation:**
            * 80-90% Stocks
            * 10-15% Bonds
            * 0-5% Cash
            
            **Focus On:**
            * Aggressive growth
            * Maximum contributions
            * Building financial habits
            * Human capital development
            """)
        
        with col2:
            st.markdown("""
            #### Mid-Career Investors (26-40)
            
            **Time Horizon:** Long (25-40 years)
            
            **Risk Tolerance:** Moderate to High
            
            **Recommended Allocation:**
            * 70-80% Stocks
            * 15-25% Bonds
            * 5-10% Cash
            
            **Focus On:**
            * Balance between growth and stability
            * Increasing contribution amounts
            * Emergency fund establishment
            * Family financial planning
            """)
        
        with col3:
            st.markdown("""
            #### Mature Investors (40+)
            
            **Time Horizon:** Moderate (5-25 years)
            
            **Risk Tolerance:** Moderate to Low
            
            **Recommended Allocation:**
            * 50-70% Stocks
            * 25-40% Bonds
            * 5-20% Cash
            
            **Focus On:**
            * Capital preservation
            * Income generation
            * Retirement readiness
            * Risk management
            """)
        
        st.markdown("""
        ### The Importance of Rebalancing
        
        As you age, regularly rebalancing your portfolio becomes increasingly important:
        
        1. **Annual Review**: Review your portfolio at least once a year
        2. **Gradual Shifts**: Make gradual adjustments as you age rather than sudden changes
        3. **Life Events**: Major life events (marriage, children, job change) may warrant portfolio reassessment
        4. **Market Conditions**: Significant market changes might create rebalancing opportunities
        
        ### Beyond Age: Other Factors to Consider
        
        While age is important, other factors also influence your optimal investment strategy:
        
        * **Financial Goals**: Specific goals might require different strategies
        * **Income Stability**: More stable income might allow for higher risk tolerance
        * **Other Assets**: Home ownership and other assets affect overall portfolio allocation
        * **Personal Risk Tolerance**: Individual comfort with volatility varies significantly
        """)
    
    with tab3:
        st.subheader("Understanding Stocks and Bonds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Stocks (Equities)
            
            **What They Are:** Partial ownership in a company
            
            **How Returns Are Generated:**
            * Capital appreciation (stock price increases)
            * Dividends (share of company profits)
            
            **Types of Stocks:**
            * **Growth Stocks**: Companies expected to grow faster than average
            * **Value Stocks**: Companies trading below their intrinsic value
            * **Dividend Stocks**: Companies that pay regular dividends
            * **Blue Chip Stocks**: Large, well-established companies
            * **Small/Mid/Large Cap**: Based on company size
            
            **Key Stock Metrics:**
            * **P/E Ratio**: Price-to-earnings ratio
            * **EPS**: Earnings per share
            * **Dividend Yield**: Annual dividends as percentage of price
            * **Market Cap**: Total value of all shares
            * **Beta**: Measure of volatility compared to market
            
            **Stock Investment Vehicles:**
            * Individual stocks
            * Mutual funds
            * ETFs (Exchange-Traded Funds)
            * Index funds
            """)
        
        with col2:
            st.markdown("""
            ### Bonds (Fixed Income)
            
            **What They Are:** Loans to companies or governments
            
            **How Returns Are Generated:**
            * Interest payments (coupons)
            * Price appreciation if interest rates fall
            
            **Types of Bonds:**
            * **Government Bonds**: Issued by federal governments
            * **Municipal Bonds**: Issued by states or local governments
            * **Corporate Bonds**: Issued by companies
            * **High-Yield Bonds**: Higher risk, higher return corporate bonds
            * **Treasury Inflation-Protected Securities (TIPS)**: Protected against inflation
            
            **Key Bond Metrics:**
            * **Yield**: Annual return from coupon payments
            * **Duration**: Sensitivity to interest rate changes
            * **Credit Rating**: Assessment of default risk (AAA to D)
            * **Maturity**: When the principal is returned
            * **Coupon Rate**: Interest payment as percentage of face value
            
            **Bond Investment Vehicles:**
            * Individual bonds
            * Bond mutual funds
            * Bond ETFs
            * Bond ladders (staggered maturities)
            """)
        
        st.markdown("""
        ### Comparing Stocks and Bonds
        
        | Feature | Stocks | Bonds |
        |---------|--------|-------|
        | Risk Level | Higher | Lower |
        | Potential Return | Higher | Lower |
        | Income | Variable (dividends) | Fixed (interest) |
        | Volatility | Higher | Lower |
        | Ownership | Ownership stake | Creditor relationship |
        | Protection in Bankruptcy | Last to get paid | Paid before stockholders |
        | Voting Rights | Usually yes | No |
        
        ### How They Work Together
        
        Stocks and bonds often move in different directions, which is why they work well together in a portfolio:
        
        * During economic expansion: Stocks typically outperform
        * During recession or uncertainty: Bonds typically outperform
        * A mix of both helps smooth overall portfolio returns
        """)
        
        st.info("""
        **The Bond Price-Interest Rate Relationship**
        
        Bond prices and interest rates have an inverse relationship:
        * When interest rates rise, bond prices fall
        * When interest rates fall, bond prices rise
        
        This is why bonds can lose value even though they're considered "safer" investments.
        """)
    
    with tab4:
        st.subheader("Retirement Planning Fundamentals")
        
        st.markdown("""
        ### The Three Pillars of Retirement Income
        
        1. **Social Security/Government Benefits**
           * Government-provided retirement income
           * Dependent on your earnings history and claiming age
           * Typically replaces about 40% of pre-retirement income
        
        2. **Employer-Sponsored Plans**
           * 401(k)s, 403(b)s, pensions
           * Often include employer matching contributions
           * Tax-advantaged growth
        
        3. **Personal Savings and Investments**
           * IRAs (Traditional and Roth)
           * Taxable investment accounts
           * Other savings vehicles
        
        ### Key Retirement Planning Concepts
        
        #### The Power of Tax-Advantaged Accounts
        
        | Account Type | Tax Advantage | Early Withdrawal Penalty | Required Minimum Distributions |
        |--------------|---------------|--------------------------|--------------------------------|
        | Traditional 401(k)/IRA | Tax-deferred contributions and growth | Yes (typically 10% before age 59½) | Yes (typically age 72) |
        | Roth 401(k)/IRA | Tax-free growth and withdrawals | On earnings only, before age 59½ | Only for Roth 401(k), not Roth IRA |
        
        #### Retirement Income Needs
        
        Most financial advisors suggest aiming to replace 70-80% of pre-retirement income.
        
        Factors affecting your personal number:
        * Healthcare costs
        * Housing situation (mortgage paid off?)
        * Expected lifestyle and travel
        * Location and cost of living
        * Longevity in your family
        
        #### The 4% Rule
        
        A general guideline suggesting that retirees can withdraw 4% of their initial retirement portfolio value each year (adjusted for inflation) with low risk of running out of money over a 30-year retirement.
        
        Example: $1,000,000 retirement portfolio × 4% = $40,000 first-year withdrawal
        
        #### Sequence of Returns Risk
        
        The risk that the order of investment returns can significantly impact portfolio longevity, especially in early retirement years.
        
        Mitigation strategies:
        * Maintain 2-3 years of expenses in cash/short-term bonds
        * Dynamic withdrawal strategies
        * Diversification across asset classes
        """)
        
        st.warning("""
        **Common Retirement Planning Mistakes**
        
        1. **Starting too late**: Each decade delay can require doubling monthly contributions
        2. **Underestimating longevity**: Many people live 20-30+ years in retirement
        3. **Ignoring inflation**: Even 3% inflation cuts purchasing power in half in 24 years
        4. **Inadequate healthcare planning**: Medicare doesn't cover all expenses
        5. **Taking Social Security too early**: Benefits increase approximately 8% per year if delayed
        """)
    
    with tab5:
        st.subheader("Investment Glossary")
        
        # Create a dataframe with terms and definitions
        terms = [
            {"Term": "Asset Allocation", "Definition": "The mix of different asset classes (stocks, bonds, cash) in an investment portfolio."},
            {"Term": "Bull Market", "Definition": "A market condition where prices are rising or expected to rise."},
            {"Term": "Bear Market", "Definition": "A market condition where prices are falling, typically by 20% or more from recent highs."},
            {"Term": "Capital Gain", "Definition": "The profit from selling an asset for more than its purchase price."},
            {"Term": "Compound Interest", "Definition": "Interest calculated on the initial principal and accumulated interest over time."},
            {"Term": "Diversification", "Definition": "Spreading investments across various assets to reduce risk."},
            {"Term": "Dividend", "Definition": "A portion of a company's earnings distributed to shareholders."},
            {"Term": "ETF (Exchange-Traded Fund)", "Definition": "A basket of securities that trades on an exchange like a stock."},
            {"Term": "Inflation", "Definition": "The rate at which the general level of prices for goods and services rises."},
            {"Term": "Liquidity", "Definition": "How easily an asset can be converted to cash without affecting its market price."},
            {"Term": "Market Capitalization", "Definition": "The total value of a company's outstanding shares."},
            {"Term": "Mutual Fund", "Definition": "A professionally managed investment fund that pools money from many investors."},
            {"Term": "Portfolio", "Definition": "A collection of investments owned by an individual or organization."},
            {"Term": "Risk Tolerance", "Definition": "An investor's ability and willingness to endure fluctuations in the value of their investments."},
            {"Term": "Volatility", "Definition": "The degree of variation in trading prices over time, often measured by standard deviation."},
            {"Term": "Yield", "Definition": "The income return on an investment, such as interest or dividends."},
            {"Term": "Dollar-Cost Averaging", "Definition": "The practice of investing a fixed amount regularly, regardless of market conditions."},
            {"Term": "Index Fund", "Definition": "A mutual fund or ETF designed to track a specific market index."},
            {"Term": "Rebalancing", "Definition": "The process of realigning portfolio assets to maintain the desired asset allocation."},
            {"Term": "Expense Ratio", "Definition": "The annual fee charged by a fund, expressed as a percentage of assets."}
        ]
        
        # Convert to DataFrame
        terms_df = pd.DataFrame(terms)
        
        # Add a search box for terms
        search_term = st.text_input("Search for a term", "")
        
        if search_term:
            filtered_terms = terms_df[terms_df["Term"].str.lower().str.contains(search_term.lower()) | 
                                     terms_df["Definition"].str.lower().str.contains(search_term.lower())]
            if not filtered_terms.empty:
                st.dataframe(filtered_terms, use_container_width=True, hide_index=True)
            else:
                st.write("No matching terms found.")
        else:
            st.dataframe(terms_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ### Additional Resources
        
        #### Books
        * "A Random Walk Down Wall Street" by Burton Malkiel
        * "The Intelligent Investor" by Benjamin Graham
        * "Common Sense on Mutual Funds" by John C. Bogle
        * "The Four Pillars of Investing" by William Bernstein
        
        #### Websites
        * [Investopedia](https://www.investopedia.com/) - Comprehensive investment education
        * [Bogleheads](https://www.bogleheads.org/) - Investment philosophy inspired by Vanguard founder
        * [Khan Academy: Personal Finance](https://www.khanacademy.org/college-careers-more/personal-finance) - Free educational videos
        * [SEC Investor.gov](https://www.investor.gov/) - U.S. Securities and Exchange Commission resources
        """)
