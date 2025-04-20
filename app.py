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

# Apply custom CSS
with open('.streamlit/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Custom container CSS
def create_card(title, content, icon="📊"):
    st.markdown(f"""
    <div class="css-card">
        <h3>{icon} {title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)
    
# Beautiful metric display
def display_metric(label, value, delta=None, delta_color="normal"):
    delta_html = f"""<div class="metric-delta" style="color: {'green' if delta_color=='good' else 'red' if delta_color=='bad' else '#718093'}">
        {delta}
    </div>""" if delta else ""
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# Sidebar with enhanced styling
st.markdown("""
<div class='css-sidebar'>
    <div class='sidebar-title'>🧭 Navigation</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",  # Empty label since we added the title via markdown
    [
        "🏠 Home",
        "📊 Age-Based Allocation",
        "🏦 Retirement Calculator",
        "📈 Stock Analyzer",
        "💼 Bond Recommendations",
        "📊 Portfolio Visualizer",
        "💰 Tax Planning",
        "📚 Education Resources"
    ]
)

# Home page
if page == "🏠 Home":
    st.title("Age-Based Investment Management Platform")
    
    # Introduction with cards
    st.markdown("<h2>Welcome to your financial future</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_card(
            "Personalized Advice", 
            "Get tailored investment recommendations based on your age and risk profile.",
            "🎯"
        )
        
    with col2:
        create_card(
            "Smart Planning", 
            "Optimize your portfolio, plan for retirement, and save on taxes.",
            "🧠"
        )
        
    with col3:
        create_card(
            "Market Insights", 
            "Analyze stocks, bonds, and other investment vehicles across global markets.",
            "🔍"
        )
    
    st.markdown("""
    This platform helps you make informed investment decisions with tools for:
    
    * Age-based asset allocation optimization
    * Retirement planning and projections
    * Stock analysis and comparison
    * Bond recommendations and fixed income strategies
    * Portfolio visualization and optimization
    * Tax-efficient investing strategies
    * Financial education resources
    
    **Get started by entering your age below:**
    """)
    
    # Age input and snapshot in a modern layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
        if st.button("Get Recommendations", key="home_recommendations"):
            with st.spinner("Analyzing ideal allocations..."):
                time.sleep(1)  # Simulate loading
                st.session_state['age'] = age
                st.success(f"Age information stored. Navigate to specific tools for detailed recommendations.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        if 'age' in st.session_state:
            user_age = st.session_state['age']
            st.markdown("<div class='css-card'>", unsafe_allow_html=True)
            st.subheader(f"Investment Snapshot for Age {user_age}")
            
            # Get allocation based on age
            stocks, bonds, fd = investment_allocator.get_allocation_percentages(user_age)
            
            # Display metrics in a modern way
            cols = st.columns(3)
            with cols[0]:
                display_metric("Stocks Allocation", f"{stocks}%", "Growth focused")
            
            with cols[1]:
                display_metric("Bonds/Mutual Funds", f"{bonds}%", "Stability focused")
            
            with cols[2]:
                display_metric("Fixed Deposits", f"{fd}%", "Safety focused")
            
            st.markdown("<br/>*Navigate to specific sections using the sidebar for detailed information and tools.*", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='css-card'>", unsafe_allow_html=True)
            st.info("Enter your age and click 'Get Recommendations' to see personalized investment advice.")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Risk assessment in a modern card
    if 'age' in st.session_state:
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        risk_level = investment_allocator.get_risk_level(st.session_state['age'])
        
        col1, col2 = st.columns([1, 3])
        with col1:
            # Create a visual risk indicator
            if risk_level == "High":
                st.markdown("### 📈 Risk Profile")
                risk_color = "#EF553B"
            elif risk_level == "Medium-High":
                st.markdown("### 📊 Risk Profile")
                risk_color = "#FFA15A"
            elif risk_level == "Medium":
                st.markdown("### 📉 Risk Profile")
                risk_color = "#636EFA"
            else:
                st.markdown("### 📉 Risk Profile")
                risk_color = "#00CC96"
            
            st.markdown(f"""
            <div style="background-color: {risk_color}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold;">
                {risk_level}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### Risk Tolerance Assessment")
            st.markdown(investment_allocator.get_risk_description(risk_level))
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Feature showcase
    st.subheader("Explore Our Investment Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='css-card'>
            <h3>📈 Stock Analysis</h3>
            <p>Research and compare stocks across global markets with our comprehensive analyzer.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='css-card'>
            <h3>🏦 Retirement Planning</h3>
            <p>Calculate your retirement needs and see if you're on track to meet your goals.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class='css-card'>
            <h3>💰 Tax Optimization</h3>
            <p>Learn strategies to minimize taxes and maximize your investment returns.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Age-Based Allocation":
    investment_allocator.show()
    
elif page == "🏦 Retirement Calculator":
    retirement_calculator.show()
    
elif page == "📈 Stock Analyzer":
    stock_analyzer.show()
    
elif page == "💼 Bond Recommendations":
    bond_recommender.show()
    
elif page == "📊 Portfolio Visualizer":
    portfolio_visualizer.show()
    
elif page == "💰 Tax Planning":
    tax_planning.show()
    
elif page == "📚 Education Resources":
    education_resources.show()
