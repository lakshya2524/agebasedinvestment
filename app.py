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

# Streamlined sidebar navigation
st.sidebar.image("generated-icon.png", width=80)
st.sidebar.markdown("<div style='text-align: center; margin-bottom: 20px;'><h3 style='margin-top: 0;'>Investment Platform</h3></div>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",  # Label will be hidden below
    [
        "🏠 Home",
        "📊 Age-Based Allocation",
        "🏦 Retirement Calculator",
        "📈 Stock Analyzer",
        "💼 Bond Recommendations",
        "📊 Portfolio Visualizer",
        "💰 Tax Planning",
        "📚 Education Resources"
    ],
    label_visibility="collapsed"  # Hide the label but provide it for accessibility
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
                risk_icon = "📈"
            elif risk_level == "Medium-High":
                st.markdown("### 📊 Risk Profile")
                risk_color = "#FFA15A"
                risk_icon = "📊"
            elif risk_level == "Medium":
                st.markdown("### 📉 Risk Profile")
                risk_color = "#636EFA"
                risk_icon = "📉"
            else:
                st.markdown("### 📉 Risk Profile")
                risk_color = "#00CC96"
                risk_icon = "📉"
            
            st.markdown(f"""
            <div class="risk-indicator" style="background: linear-gradient(135deg, {risk_color} 0%, {risk_color}CC 100%);">
                <span style="font-size: 1.8rem;">{risk_icon}</span>
                <div style="font-size: 1.2rem; margin-top: 5px;">{risk_level}</div>
            </div>
            <div class="tooltip">
                <small style="color: #718093; cursor: help;">What does this mean?</small>
                <span class="tooltip-text">This risk assessment is based on your age and determines your recommended investment allocation strategy.</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### Risk Tolerance Assessment")
            st.markdown(investment_allocator.get_risk_description(risk_level))
            
            # Add action buttons
            st.markdown("""
            <div style="margin-top: 15px;">
                <span class="badge badge-primary" style="margin-right: 8px;">Age-Based</span>
                <span class="badge badge-success">Personalized</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Feature showcase with working links
    st.subheader("Explore Our Investment Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Navigation link to Stock Analyzer
        stock_analysis_id = "stock-analyzer-link"
        st.markdown(f"""
        <div class='feature-card' id="{stock_analysis_id}" onclick="document.querySelector('[data-value=\\'📈 Stock Analyzer\\']').click()" style="cursor: pointer;">
            <h3>📈 Stock Analysis</h3>
            <p>Research and compare stocks across global markets with our comprehensive analyzer.</p>
            <div class="divider"></div>
            <span class="badge badge-primary">Global Markets</span>
            <span class="badge badge-success">Technical Analysis</span>
        </div>
        <script>
            document.getElementById('{stock_analysis_id}').addEventListener('click', function() {{
                // Find the stock analyzer radio button and click it
                const stockAnalyzerOption = Array.from(document.querySelectorAll('[role="radio"]')).find(
                    el => el.getAttribute('data-value') === '📈 Stock Analyzer'
                );
                if (stockAnalyzerOption) stockAnalyzerOption.click();
            }});
        </script>
        """, unsafe_allow_html=True)
        
    with col2:
        # Navigation link to Retirement Calculator
        retirement_id = "retirement-link"
        st.markdown(f"""
        <div class='feature-card' id="{retirement_id}" onclick="document.querySelector('[data-value=\\'🏦 Retirement Calculator\\']').click()" style="cursor: pointer;">
            <h3>🏦 Retirement Planning</h3>
            <p>Calculate your retirement needs and see if you're on track to meet your goals.</p>
            <div class="divider"></div>
            <span class="badge badge-primary">Future Projections</span>
            <span class="badge badge-success">Goal Setting</span>
        </div>
        <script>
            document.getElementById('{retirement_id}').addEventListener('click', function() {{
                // Find the retirement calculator radio button and click it
                const retirementOption = Array.from(document.querySelectorAll('[role="radio"]')).find(
                    el => el.getAttribute('data-value') === '🏦 Retirement Calculator'
                );
                if (retirementOption) retirementOption.click();
            }});
        </script>
        """, unsafe_allow_html=True)
        
    with col3:
        # Navigation link to Tax Planning
        tax_id = "tax-link"
        st.markdown(f"""
        <div class='feature-card' id="{tax_id}" onclick="document.querySelector('[data-value=\\'💰 Tax Planning\\']').click()" style="cursor: pointer;">
            <h3>💰 Tax Optimization</h3>
            <p>Learn strategies to minimize taxes and maximize your investment returns.</p>
            <div class="divider"></div>
            <span class="badge badge-primary">Tax Savings</span>
            <span class="badge badge-warning">Custom Strategies</span>
        </div>
        <script>
            document.getElementById('{tax_id}').addEventListener('click', function() {{
                // Find the tax planning radio button and click it
                const taxOption = Array.from(document.querySelectorAll('[role="radio"]')).find(
                    el => el.getAttribute('data-value') === '💰 Tax Planning'
                );
                if (taxOption) taxOption.click();
            }});
        </script>
        """, unsafe_allow_html=True)
        
    # Add a second row of feature cards
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Add some spacing
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Navigation link to Age-Based Allocation
        allocation_id = "allocation-link"
        st.markdown(f"""
        <div class='feature-card' id="{allocation_id}" onclick="document.querySelector('[data-value=\\'📊 Age-Based Allocation\\']').click()" style="cursor: pointer;">
            <h3>📊 Asset Allocation</h3>
            <p>Get personalized investment allocation recommendations based on your age profile.</p>
            <div class="divider"></div>
            <span class="badge badge-primary">Age-Optimized</span>
            <span class="badge badge-success">Custom Portfolios</span>
        </div>
        <script>
            document.getElementById('{allocation_id}').addEventListener('click', function() {{
                // Find the age-based allocation radio button and click it
                const allocationOption = Array.from(document.querySelectorAll('[role="radio"]')).find(
                    el => el.getAttribute('data-value') === '📊 Age-Based Allocation'
                );
                if (allocationOption) allocationOption.click();
            }});
        </script>
        """, unsafe_allow_html=True)
        
    with col2:
        # Navigation link to Bond Recommendations
        bonds_id = "bonds-link"
        st.markdown(f"""
        <div class='feature-card' id="{bonds_id}" onclick="document.querySelector('[data-value=\\'💼 Bond Recommendations\\']').click()" style="cursor: pointer;">
            <h3>💼 Bond Explorer</h3>
            <p>Find suitable bonds and fixed income investments to match your risk profile.</p>
            <div class="divider"></div>
            <span class="badge badge-primary">Fixed Income</span>
            <span class="badge badge-success">Risk Assessment</span>
        </div>
        <script>
            document.getElementById('{bonds_id}').addEventListener('click', function() {{
                // Find the bond recommendations radio button and click it
                const bondsOption = Array.from(document.querySelectorAll('[role="radio"]')).find(
                    el => el.getAttribute('data-value') === '💼 Bond Recommendations'
                );
                if (bondsOption) bondsOption.click();
            }});
        </script>
        """, unsafe_allow_html=True)
        
    with col3:
        # Navigation link to Education Resources
        education_id = "education-link"
        st.markdown(f"""
        <div class='feature-card' id="{education_id}" onclick="document.querySelector('[data-value=\\'📚 Education Resources\\']').click()" style="cursor: pointer;">
            <h3>📚 Financial Education</h3>
            <p>Learn investment concepts and strategies to improve your financial knowledge.</p>
            <div class="divider"></div>
            <span class="badge badge-primary">Learning Resources</span>
            <span class="badge badge-warning">Beginners Welcome</span>
        </div>
        <script>
            document.getElementById('{education_id}').addEventListener('click', function() {{
                // Find the education resources radio button and click it
                const educationOption = Array.from(document.querySelectorAll('[role="radio"]')).find(
                    el => el.getAttribute('data-value') === '📚 Education Resources'
                );
                if (educationOption) educationOption.click();
            }});
        </script>
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
