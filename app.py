import streamlit as st
import time
import investment_allocator
import retirement_calculator
import stock_analyzer
import bond_recommender
import portfolio_visualizer
import education_resources
import tax_planning

# Set page config
st.set_page_config(
    page_title="Age-Based Investment Management Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Age-Based Allocation",
        "Retirement Calculator",
        "Stock Analyzer",
        "Bond Recommendations",
        "Portfolio Visualizer",
        "Tax Planning",
        "Education Resources"
    ]
)

# Home page
if page == "Home":
    st.title("Age-Based Investment Management Platform")
    st.markdown("""
    Welcome to your personalized investment management platform. This tool helps you:
    
    * Determine optimal investment allocation based on your age
    * Plan for retirement
    * Analyze stocks across global markets
    * Find recommended bonds/fixed income instruments
    * Visualize your portfolio
    * Optimize tax planning based on marital status
    * Learn investment basics
    
    **Get started by entering your age below:**
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
        if st.button("Get Recommendations"):
            with st.spinner("Analyzing ideal allocations..."):
                time.sleep(1)  # Simulate loading
                st.session_state['age'] = age
                st.success(f"Age information stored. Navigate to specific tools for detailed recommendations.")
    
    with col2:
        st.subheader("Investment Snapshot")
        if 'age' in st.session_state:
            user_age = st.session_state['age']
            st.info(f"Based on your age ({user_age}), here's a quick overview:")
            
            # Get allocation based on age
            stocks, bonds, fd = investment_allocator.get_allocation_percentages(user_age)
            
            st.markdown(f"""
            * **Recommended Stock Allocation:** {stocks}%
            * **Recommended Bonds/Mutual Funds:** {bonds}%
            * **Recommended Fixed Deposits:** {fd}%
            
            *Navigate to specific sections using the sidebar for detailed information and tools.*
            """)
        else:
            st.info("Enter your age and click 'Get Recommendations' to see personalized investment advice.")
    
    # Risk assessment based on age
    if 'age' in st.session_state:
        st.subheader("Risk Assessment")
        risk_level = investment_allocator.get_risk_level(st.session_state['age'])
        st.markdown(f"**Risk Tolerance Level:** {risk_level}")
        st.markdown(investment_allocator.get_risk_description(risk_level))

elif page == "Age-Based Allocation":
    investment_allocator.show()
    
elif page == "Retirement Calculator":
    retirement_calculator.show()
    
elif page == "Stock Analyzer":
    stock_analyzer.show()
    
elif page == "Bond Recommendations":
    bond_recommender.show()
    
elif page == "Portfolio Visualizer":
    portfolio_visualizer.show()
    
elif page == "Tax Planning":
    tax_planning.show()
    
elif page == "Education Resources":
    education_resources.show()
