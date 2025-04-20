import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def get_bond_data():
    """Return sample bond data for demonstration purposes."""
    # This would typically come from an API or database in a real application
    
    # Treasury bonds data
    treasury_bonds = [
        {"name": "U.S. Treasury 2-Year Note", "type": "Government", "yield": 4.95, "risk": "Very Low", "min_investment": 1000, "duration": 2, "credit_rating": "AAA"},
        {"name": "U.S. Treasury 5-Year Note", "type": "Government", "yield": 4.73, "risk": "Very Low", "min_investment": 1000, "duration": 5, "credit_rating": "AAA"},
        {"name": "U.S. Treasury 10-Year Note", "type": "Government", "yield": 4.68, "risk": "Very Low", "min_investment": 1000, "duration": 10, "credit_rating": "AAA"},
        {"name": "U.S. Treasury 30-Year Bond", "type": "Government", "yield": 4.80, "risk": "Low", "min_investment": 1000, "duration": 30, "credit_rating": "AAA"},
    ]
    
    # Corporate bonds data
    corporate_bonds = [
        {"name": "Apple Inc. Corporate Bond", "type": "Corporate", "yield": 5.05, "risk": "Low", "min_investment": 1000, "duration": 5, "credit_rating": "AA+"},
        {"name": "Microsoft Corp Bond", "type": "Corporate", "yield": 5.15, "risk": "Low", "min_investment": 1000, "duration": 7, "credit_rating": "AAA"},
        {"name": "Amazon.com Inc Bond", "type": "Corporate", "yield": 5.30, "risk": "Low", "min_investment": 1000, "duration": 10, "credit_rating": "AA"},
        {"name": "Johnson & Johnson Bond", "type": "Corporate", "yield": 5.10, "risk": "Low", "min_investment": 1000, "duration": 5, "credit_rating": "AAA"},
        {"name": "Verizon Communications Bond", "type": "Corporate", "yield": 5.75, "risk": "Medium", "min_investment": 1000, "duration": 10, "credit_rating": "BBB+"},
        {"name": "Walmart Inc. Bond", "type": "Corporate", "yield": 5.25, "risk": "Low", "min_investment": 1000, "duration": 7, "credit_rating": "AA"},
        {"name": "Coca-Cola Company Bond", "type": "Corporate", "yield": 5.20, "risk": "Low", "min_investment": 1000, "duration": 5, "credit_rating": "A+"},
        {"name": "AT&T Inc. Bond", "type": "Corporate", "yield": 6.00, "risk": "Medium", "min_investment": 1000, "duration": 15, "credit_rating": "BBB"},
    ]
    
    # Municipal bonds data
    municipal_bonds = [
        {"name": "New York City Municipal Bond", "type": "Municipal", "yield": 4.00, "risk": "Low", "min_investment": 5000, "duration": 10, "credit_rating": "AA"},
        {"name": "California State Municipal Bond", "type": "Municipal", "yield": 4.10, "risk": "Low", "min_investment": 5000, "duration": 15, "credit_rating": "AA-"},
        {"name": "Texas Municipal Bond", "type": "Municipal", "yield": 3.90, "risk": "Low", "min_investment": 5000, "duration": 7, "credit_rating": "AAA"},
        {"name": "Florida Municipal Bond", "type": "Municipal", "yield": 3.95, "risk": "Low", "min_investment": 5000, "duration": 10, "credit_rating": "AA+"},
    ]
    
    # High yield bonds data
    high_yield_bonds = [
        {"name": "Energy Sector High Yield Bond", "type": "High Yield", "yield": 7.50, "risk": "High", "min_investment": 10000, "duration": 7, "credit_rating": "BB"},
        {"name": "Retail Sector High Yield Bond", "type": "High Yield", "yield": 7.80, "risk": "High", "min_investment": 10000, "duration": 5, "credit_rating": "BB-"},
        {"name": "Technology Sector High Yield Bond", "type": "High Yield", "yield": 7.20, "risk": "High", "min_investment": 10000, "duration": 6, "credit_rating": "BB+"},
        {"name": "Healthcare Sector High Yield Bond", "type": "High Yield", "yield": 7.00, "risk": "Medium-High", "min_investment": 10000, "duration": 8, "credit_rating": "BB+"},
    ]
    
    # Combine all bonds
    all_bonds = treasury_bonds + corporate_bonds + municipal_bonds + high_yield_bonds
    
    # Create DataFrame
    bond_df = pd.DataFrame(all_bonds)
    
    return bond_df

def get_bond_etf_data():
    """Return sample bond ETF data for demonstration purposes."""
    # This would typically come from an API or database in a real application
    
    bond_etfs = [
        {"name": "Vanguard Total Bond Market ETF", "ticker": "BND", "type": "Aggregate Bond", "yield": 4.80, "expense_ratio": 0.03, "risk": "Low", "avg_duration": 6.5, "aum_billions": 300.5},
        {"name": "iShares Core U.S. Aggregate Bond ETF", "ticker": "AGG", "type": "Aggregate Bond", "yield": 4.85, "expense_ratio": 0.04, "risk": "Low", "avg_duration": 6.2, "aum_billions": 85.3},
        {"name": "Vanguard Short-Term Bond ETF", "ticker": "BSV", "type": "Short-Term Bond", "yield": 4.90, "expense_ratio": 0.04, "risk": "Very Low", "avg_duration": 2.7, "aum_billions": 38.6},
        {"name": "iShares TIPS Bond ETF", "ticker": "TIP", "type": "Inflation-Protected", "yield": 4.20, "expense_ratio": 0.19, "risk": "Low", "avg_duration": 7.6, "aum_billions": 21.1},
        {"name": "iShares iBoxx $ Investment Grade Corporate Bond ETF", "ticker": "LQD", "type": "Corporate Bond", "yield": 5.50, "expense_ratio": 0.14, "risk": "Medium", "avg_duration": 8.3, "aum_billions": 33.5},
        {"name": "Vanguard Intermediate-Term Corporate Bond ETF", "ticker": "VCIT", "type": "Corporate Bond", "yield": 5.40, "expense_ratio": 0.04, "risk": "Medium", "avg_duration": 6.1, "aum_billions": 47.8},
        {"name": "SPDR Bloomberg High Yield Bond ETF", "ticker": "JNK", "type": "High Yield Bond", "yield": 7.10, "expense_ratio": 0.40, "risk": "High", "avg_duration": 3.7, "aum_billions": 9.2},
        {"name": "iShares J.P. Morgan USD Emerging Markets Bond ETF", "ticker": "EMB", "type": "Emerging Market Bond", "yield": 6.90, "expense_ratio": 0.39, "risk": "High", "avg_duration": 7.2, "aum_billions": 14.7},
        {"name": "iShares MBS ETF", "ticker": "MBB", "type": "Mortgage-Backed", "yield": 4.70, "expense_ratio": 0.06, "risk": "Medium", "avg_duration": 5.8, "aum_billions": 24.5},
        {"name": "Vanguard Tax-Exempt Bond ETF", "ticker": "VTEB", "type": "Municipal Bond", "yield": 3.80, "expense_ratio": 0.05, "risk": "Low", "avg_duration": 5.9, "aum_billions": 28.3},
    ]
    
    # Create DataFrame
    etf_df = pd.DataFrame(bond_etfs)
    
    return etf_df

def recommend_bonds_by_age(age):
    """Recommend bonds based on investor age."""
    bond_df = get_bond_data()
    etf_df = get_bond_etf_data()
    
    # Define recommendation logic based on age
    if 18 <= age <= 25:
        # Young investors: High risk tolerance, long time horizon
        recommendations = {
            "bond_types": ["Corporate", "High Yield"],
            "etf_types": ["High Yield Bond", "Corporate Bond", "Emerging Market Bond"],
            "duration_range": (7, 30),  # Longer duration appropriate for younger investors
            "allocation": {
                "government": 10,
                "corporate": 25,
                "high_yield": 65,
                "municipal": 0
            },
            "strategy": "Growth-Oriented",
            "description": """
            **Young Investor Bond Strategy (18-25):**
            
            With a long investment horizon, you can take more risk and potentially earn higher yields.
            * Focus on longer-duration bonds for higher yields
            * Consider higher allocation to corporate and high-yield bonds
            * Lower allocation to government bonds
            * Consider emerging market bond exposure
            * Prioritize growth over current income
            """
        }
    elif 26 <= age <= 40:
        # Mid-career investors: Moderate risk tolerance, balanced approach
        recommendations = {
            "bond_types": ["Government", "Corporate", "High Yield"],
            "etf_types": ["Aggregate Bond", "Corporate Bond", "High Yield Bond"],
            "duration_range": (5, 15),  # Medium duration for balanced approach
            "allocation": {
                "government": 30,
                "corporate": 45,
                "high_yield": 20,
                "municipal": 5
            },
            "strategy": "Balanced Growth and Income",
            "description": """
            **Mid-Career Investor Bond Strategy (26-40):**
            
            Balance growth potential with some income and stability.
            * Mix of intermediate-term government and corporate bonds
            * Moderate allocation to high-yield for growth
            * Begin introducing municipal bonds if in a high tax bracket
            * Consider TIPS for inflation protection
            * Balance risk and reward with a diversified bond portfolio
            """
        }
    else:  # age > 40
        # Older investors: Lower risk tolerance, income focus
        recommendations = {
            "bond_types": ["Government", "Corporate", "Municipal"],
            "etf_types": ["Aggregate Bond", "Corporate Bond", "Municipal Bond", "Short-Term Bond"],
            "duration_range": (2, 10),  # Shorter duration for reduced interest rate risk
            "allocation": {
                "government": 45,
                "corporate": 30,
                "high_yield": 5,
                "municipal": 20
            },
            "strategy": "Income and Capital Preservation",
            "description": """
            **Mature Investor Bond Strategy (40+):**
            
            Focus on preserving capital while generating reliable income.
            * Higher allocation to government and municipal bonds
            * Consider tax implications with greater municipal bond exposure
            * Reduce exposure to higher-risk bonds
            * Shorter duration bonds to reduce interest rate risk
            * Focus on quality investment-grade issues
            """
        }
    
    # Filter bonds based on recommendations
    recommended_bonds = bond_df[bond_df['type'].isin(recommendations['bond_types']) & 
                                (bond_df['duration'] >= recommendations['duration_range'][0]) & 
                                (bond_df['duration'] <= recommendations['duration_range'][1])]
    
    # Filter ETFs based on recommendations
    recommended_etfs = etf_df[etf_df['type'].isin(recommendations['etf_types'])]
    
    # Sort by yield (descending)
    recommended_bonds = recommended_bonds.sort_values('yield', ascending=False)
    recommended_etfs = recommended_etfs.sort_values('yield', ascending=False)
    
    return {
        "recommendations": recommendations,
        "bonds": recommended_bonds,
        "etfs": recommended_etfs
    }

def show():
    """Display the bond recommendation page."""
    st.title("Bond Recommendations")
    
    st.markdown("""
    Bonds are an essential part of a well-diversified investment portfolio, especially as you get older.
    This tool provides personalized bond recommendations based on your age and investment goals.
    """)
    
    # Get age from session state if available, otherwise default to 30
    default_age = st.session_state.get('age', 30)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Your Information")
        age = st.number_input("Your Age", min_value=18, max_value=100, value=default_age)
        
        # Additional preferences
        st.subheader("Investment Preferences")
        tax_bracket = st.select_slider("Tax Bracket", options=["Low", "Medium", "High"], value="Medium")
        interest_rate_view = st.radio("Interest Rate Outlook", ["Rising", "Stable", "Falling"])
        income_need = st.select_slider("Income Need", options=["Low", "Medium", "High"], value="Medium")
    
    with col2:
        st.subheader("Bond Market Overview")
        
        # Create a simple yield curve visualization
        maturities = [1, 2, 5, 10, 20, 30]
        yields = [4.90, 4.95, 4.73, 4.68, 4.75, 4.80]  # Example current Treasury yields
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=maturities,
            y=yields,
            mode='lines+markers',
            name='Current Yield Curve',
            line=dict(color='#636EFA', width=3)
        ))
        
        fig.update_layout(
            title="U.S. Treasury Yield Curve",
            xaxis_title="Maturity (Years)",
            yaxis_title="Yield (%)",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Current bond market conditions
        st.markdown("""
        **Current Bond Market Conditions:**
        
        * Treasury yields remain elevated compared to historical averages
        * Corporate bond spreads are relatively tight, suggesting lower perceived risk
        * Municipal bonds offer tax advantages for investors in higher tax brackets
        * High-yield bonds provide higher income but with increased risk
        * International bonds offer diversification but with currency risk
        """)
    
    if st.button("Get Bond Recommendations"):
        with st.spinner("Analyzing bond recommendations..."):
            # Get recommendations based on age
            results = recommend_bonds_by_age(age)
            
            # Display recommendations
            st.subheader(f"Bond Strategy: {results['recommendations']['strategy']}")
            
            # Description based on age
            st.markdown(results['recommendations']['description'])
            
            # Recommended allocation
            st.subheader("Recommended Bond Allocation")
            
            # Create allocation chart
            allocation = results['recommendations']['allocation']
            allocation_df = pd.DataFrame({
                'Type': list(allocation.keys()),
                'Percentage': list(allocation.values())
            })
            
            fig = px.pie(
                allocation_df,
                values='Percentage',
                names='Type',
                title="Recommended Bond Allocation",
                color_discrete_sequence=px.colors.qualitative.Plotly,
                hole=0.4
            )
            
            # Update layout
            fig.update_layout(
                showlegend=True,
                height=350,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tax considerations based on tax bracket
            if tax_bracket == "High":
                st.info("""
                **Tax Consideration:** Since you're in a high tax bracket, consider increasing allocation to municipal bonds 
                which provide tax-exempt interest income.
                """)
            
            # Interest rate considerations
            if interest_rate_view == "Rising":
                st.info("""
                **Interest Rate Consideration:** With your expectation of rising interest rates, consider focusing on 
                shorter-duration bonds to minimize interest rate risk.
                """)
            elif interest_rate_view == "Falling":
                st.info("""
                **Interest Rate Consideration:** With your expectation of falling interest rates, consider including 
                some longer-duration bonds to potentially benefit from price appreciation.
                """)
            
            # Recommended individual bonds
            st.subheader("Top Recommended Individual Bonds")
            
            if not results['bonds'].empty:
                # Format the DataFrame for display
                display_bonds = results['bonds'].copy()
                display_bonds['yield'] = display_bonds['yield'].apply(lambda x: f"{x:.2f}%")
                display_bonds['min_investment'] = display_bonds['min_investment'].apply(lambda x: f"${x:,}")
                
                st.dataframe(
                    display_bonds[['name', 'type', 'yield', 'duration', 'risk', 'credit_rating', 'min_investment']],
                    use_container_width=True
                )
            else:
                st.write("No specific bonds match your criteria.")
            
            # Recommended bond ETFs
            st.subheader("Top Recommended Bond ETFs")
            
            if not results['etfs'].empty:
                # Format the DataFrame for display
                display_etfs = results['etfs'].copy()
                display_etfs['yield'] = display_etfs['yield'].apply(lambda x: f"{x:.2f}%")
                display_etfs['expense_ratio'] = display_etfs['expense_ratio'].apply(lambda x: f"{x:.2f}%")
                display_etfs['aum_billions'] = display_etfs['aum_billions'].apply(lambda x: f"${x:.1f}B")
                
                st.dataframe(
                    display_etfs[['name', 'ticker', 'type', 'yield', 'risk', 'expense_ratio', 'avg_duration', 'aum_billions']],
                    use_container_width=True
                )
            else:
                st.write("No specific ETFs match your criteria.")
            
            # Investment considerations based on age
            if age <= 25:
                st.markdown("""
                **Investment Tip for Young Investors:**
                
                Consider a bond ladder strategy where you invest in bonds of different maturities to provide regular 
                reinvestment opportunities while managing interest rate risk.
                """)
            elif 26 <= age <= 40:
                st.markdown("""
                **Investment Tip for Mid-Career Investors:**
                
                Consider diversifying across different bond types for a balance of yield and stability. Corporate bonds 
                can provide higher yields than government bonds with modest additional risk.
                """)
            else:  # age > 40
                st.markdown("""
                **Investment Tip for Mature Investors:**
                
                As retirement approaches, consider increasing allocation to high-quality bonds with staggered maturities 
                to provide predictable income streams while preserving capital.
                """)
            
            # Disclaimer
            st.caption("""
            **Disclaimer:** Bond recommendations are based on general investment principles and your age profile. 
            Individual bonds and bond yields change frequently. Always conduct thorough research or consult a financial 
            advisor before making investment decisions.
            """)
