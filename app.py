import streamlit as st
import time
import investment_allocator
import retirement_calculator
import stock_analyzer
import bond_recommender
import portfolio_visualizer
import education_resources
import tax_planning
import ui_components

# Set page config
st.set_page_config(
    page_title="Age-Based Investment Management Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
ui_components.apply_custom_css()
ui_components.add_font_awesome()

# Sidebar for navigation with improved UI
st.sidebar.title("Investment Dashboard")

# Add profile section to sidebar
if 'age' in st.session_state:
    st.sidebar.markdown(f"""
    <div style="padding: 10px; background-color: rgba(255,255,255,0.1); border-radius: 8px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #4B5563; 
                        display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <i class="fas fa-user" style="color: white;"></i>
            </div>
            <div>
                <div style="font-weight: bold; color: white;">Your Profile</div>
                <div style="font-size: 0.9rem; color: #D1D5DB;">Age: {st.session_state['age']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Navigation with icons
st.sidebar.markdown("### Navigate")
page = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "📊 Age-Based Allocation",
        "🔄 Retirement Calculator",
        "📈 Stock Analyzer",
        "💼 Bond Recommendations",
        "💰 Portfolio Visualizer",
        "📑 Tax Planning",
        "📚 Education Resources"
    ],
    format_func=lambda x: x[2:]  # Remove emoji from the label
)

# Extract page name without emoji
page_name = page[2:]

# Home page
if page_name == "Home":
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Smart Investment Management</h1>", unsafe_allow_html=True)
    
    # Banner with animation
    ui_components.animated_text("""
    <div style="text-align: center; padding: 20px; margin-bottom: 30px; background: linear-gradient(90deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 10px;">
        <h2 style="color: #1E3A8A; margin-bottom: 10px;">Your Age-Based Investment Platform</h2>
        <p style="font-size: 18px; color: #4B5563;">Personalized investment strategies for every stage of life</p>
    </div>
    """, 0)
    
    # Feature highlights as cards
    st.markdown("<h2 style='margin-top: 30px;'>What We Offer</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui_components.dashboard_card(
            "Personalized Allocations", 
            """
            <p>Get age-optimized investment allocations across stocks, bonds, and fixed deposits.</p>
            <a href="#" style="color: #2563EB; text-decoration: none;">
                Learn more <i class="fas fa-arrow-right" style="font-size: 0.8em;"></i>
            </a>
            """, 
            icon="chart-pie"
        )
            
    with col2:
        ui_components.dashboard_card(
            "Financial Planning", 
            """
            <p>Plan for retirement, analyze stocks, and get bond recommendations tailored to your needs.</p>
            <a href="#" style="color: #2563EB; text-decoration: none;">
                Explore tools <i class="fas fa-arrow-right" style="font-size: 0.8em;"></i>
            </a>
            """, 
            icon="coins"
        )
            
    with col3:
        ui_components.dashboard_card(
            "Tax Optimization", 
            """
            <p>Optimize your tax strategy based on marital status and specific financial situation.</p>
            <a href="#" style="color: #2563EB; text-decoration: none;">
                Tax planning <i class="fas fa-arrow-right" style="font-size: 0.8em;"></i>
            </a>
            """, 
            icon="file-invoice-dollar"
        )
    
    # User input section with improved styling
    ui_components.add_section_divider()
    
    st.markdown("<h2 style='margin-top: 30px;'>Get Started</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        ui_components.styled_container(
            """
            <h3 style='margin-top: 0;'>Your Information</h3>
            """, 
            shadow=True
        )
        
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True) # Spacer
        
        if st.button("Generate Recommendations", key="home_recommendations"):
            with st.spinner("Analyzing your financial profile..."):
                time.sleep(1)  # Simulate loading
                st.session_state['age'] = age
                ui_components.success_card("<b>Profile Updated!</b> Your age information has been saved. Navigate to specific tools using the sidebar for detailed recommendations.")
    
    with col2:
        if 'age' in st.session_state:
            user_age = st.session_state['age']
            # Get allocation based on age
            stocks, bonds, fd = investment_allocator.get_allocation_percentages(user_age)
            risk_level = investment_allocator.get_risk_level(user_age)
            
            ui_components.styled_container(
                f"""
                <h3 style='margin-top: 0;'>Investment Snapshot</h3>
                <p>Based on your age ({user_age}), here's your personalized investment profile:</p>
                """, 
                shadow=True
            )
            
            # Metrics in a row
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                ui_components.create_metric_display("Stocks Allocation", f"{stocks}%")
            
            with metric_col2:
                ui_components.create_metric_display("Bonds & Mutual Funds", f"{bonds}%")
                
            with metric_col3:
                ui_components.create_metric_display("Fixed Deposits", f"{fd}%")
            
            # Risk assessment
            ui_components.styled_container(
                f"""
                <h4 style='margin-top: 0;'>Risk Tolerance Profile: <span style='color: #2563EB;'>{risk_level}</span></h4>
                <p>{investment_allocator.get_risk_description(risk_level)}</p>
                """, 
                background_color="#F3F4F6", 
                shadow=False
            )
            
            # Quick navigation links
            st.markdown("<h4>Explore Personalized Tools:</h4>", unsafe_allow_html=True)
            
            quick_nav_col1, quick_nav_col2 = st.columns(2)
            
            with quick_nav_col1:
                ui_components.add_icon_link("Retirement Calculator", "#", "calculator")
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                ui_components.add_icon_link("Stock Analysis", "#", "chart-line")
            
            with quick_nav_col2:
                ui_components.add_icon_link("Portfolio Visualization", "#", "pie-chart")
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                ui_components.add_icon_link("Tax Planning", "#", "file-invoice")
            
        else:
            ui_components.info_card("""
            <h4 style='margin-top: 0;'>Welcome to Smart Investment Management</h4>
            <p>Enter your age and click 'Generate Recommendations' to receive personalized investment advice based on your life stage.</p>
            <p>Our platform uses age-based allocation strategies to help you make informed investment decisions.</p>
            """)
    
    # Testimonials section
    if 'age' in st.session_state:
        ui_components.add_section_divider()
        
        st.markdown("<h2 style='margin-top: 30px;'>Why Age-Based Investing Works</h2>", unsafe_allow_html=True)
        
        testimonial_col1, testimonial_col2 = st.columns(2)
        
        with testimonial_col1:
            ui_components.styled_container(
                """
                <div style='display: flex; align-items: center;'>
                    <div style='flex-shrink: 0; width: 50px; height: 50px; border-radius: 50%; background-color: #E0E7FF; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;'>
                        <i class="fas fa-quote-left" style="color: #4F46E5; font-size: 20px;"></i>
                    </div>
                    <div>
                        <p style='font-style: italic;'>Age-based investing helped me balance growth and security as I approached retirement.</p>
                        <p style='margin-bottom: 0; font-weight: bold;'>Michael R.</p>
                        <p style='margin-top: 0; font-size: 0.9em; color: #6B7280;'>Age 58, Financial Analyst</p>
                    </div>
                </div>
                """,
                background_color="#F9FAFB"
            )
        
        with testimonial_col2:
            ui_components.styled_container(
                """
                <div style='display: flex; align-items: center;'>
                    <div style='flex-shrink: 0; width: 50px; height: 50px; border-radius: 50%; background-color: #E0F2FE; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;'>
                        <i class="fas fa-quote-left" style="color: #0284C7; font-size: 20px;"></i>
                    </div>
                    <div>
                        <p style='font-style: italic;'>Starting early with the right allocation strategy has maximized my long-term growth potential.</p>
                        <p style='margin-bottom: 0; font-weight: bold;'>Sarah T.</p>
                        <p style='margin-top: 0; font-size: 0.9em; color: #6B7280;'>Age 29, Software Engineer</p>
                    </div>
                </div>
                """,
                background_color="#F9FAFB"
            )
    
    # Add footer
    ui_components.add_footer()

elif page_name == "Age-Based Allocation":
    investment_allocator.show()
    ui_components.add_footer()
    
elif page_name == "Retirement Calculator":
    retirement_calculator.show()
    ui_components.add_footer()
    
elif page_name == "Stock Analyzer":
    stock_analyzer.show()
    ui_components.add_footer()
    
elif page_name == "Bond Recommendations":
    bond_recommender.show()
    ui_components.add_footer()
    
elif page_name == "Portfolio Visualizer":
    portfolio_visualizer.show()
    ui_components.add_footer()
    
elif page_name == "Tax Planning":
    tax_planning.show()
    ui_components.add_footer()
    
elif page_name == "Education Resources":
    education_resources.show()
    ui_components.add_footer()
