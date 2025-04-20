import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the app."""
    # Load custom CSS
    with open('.streamlit/custom_style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def dashboard_card(title, content, icon=None):
    """
    Create a styled dashboard card.
    
    Args:
        title (str): Card title
        content (str): HTML content to display in the card
        icon (str, optional): Icon class (Font Awesome)
    """
    icon_html = f'<i class="fas fa-{icon}"></i> ' if icon else ''
    st.markdown(
        f"""
        <div class="dashboard-card animate-fade-in">
            <h3>{icon_html}{title}</h3>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_metric_display(label, value, delta=None, delta_color="normal"):
    """
    Create a styled metric display.
    
    Args:
        label (str): Metric label
        value (str): Metric value
        delta (str, optional): Change indicator
        delta_color (str, optional): Color for delta ("normal", "inverse", "off")
    """
    delta_html = ""
    if delta:
        icon = "↑" if delta.startswith("+") else "↓"
        color = ""
        if delta_color == "normal":
            color = "color: #10B981;" if delta.startswith("+") else "color: #EF4444;"
        elif delta_color == "inverse":
            color = "color: #EF4444;" if delta.startswith("+") else "color: #10B981;"
        
        delta_html = f'<div style="{color} font-size: 14px;">{icon} {delta}</div>'
    
    st.markdown(
        f"""
        <div class="metric-container animate-fade-in">
            <div class="metric-value">{value}</div>
            {delta_html}
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def info_card(content):
    """Create an info card with styled content."""
    st.markdown(
        f"""
        <div class="info-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def success_card(content):
    """Create a success card with styled content."""
    st.markdown(
        f"""
        <div class="success-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def warning_card(content):
    """Create a warning card with styled content."""
    st.markdown(
        f"""
        <div class="warning-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def add_section_divider():
    """Add a visual divider between sections."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

def add_footer():
    """Add a footer to the page."""
    st.markdown(
        """
        <div class="footer">
            <p>Age-Based Investment Management Platform © 2025</p>
            <p>Disclaimer: This is an educational tool. Consult with a financial advisor before making investment decisions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def add_icon_link(text, url, icon):
    """Create a link with an icon."""
    st.markdown(
        f"""
        <a href="{url}" target="_blank" style="text-decoration: none; color: #2563EB; display: flex; align-items: center;">
            <i class="fas fa-{icon}" style="margin-right: 5px;"></i> {text}
        </a>
        """,
        unsafe_allow_html=True
    )

def add_tooltip(text, tooltip_text):
    """Add text with a tooltip on hover."""
    st.markdown(
        f"""
        <div class="tooltip">{text}
            <span class="tooltiptext">{tooltip_text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def animated_text(text, animation_delay=0):
    """Create animated text with fade-in effect."""
    st.markdown(
        f"""
        <div class="animate-fade-in" style="animation-delay: {int(animation_delay)}s;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def format_currency(amount):
    """Format a number as currency."""
    return f"${amount:,.2f}"

def format_percentage(value):
    """Format a decimal as percentage."""
    return f"{value:.2f}%"

def loading_animation(text="Loading..."):
    """Display a loading animation with text."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin: 1rem 0;">
            <div class="stSpinner">
                <div></div>
            </div>
            <span style="margin-left: 10px;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def styled_container(content, background_color="#FFFFFF", border_radius="10px", padding="20px", margin="10px 0", shadow=True):
    """Create a styled container for content."""
    shadow_style = "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" if shadow else ""
    
    st.markdown(
        f"""
        <div style="background-color: {background_color}; 
                    border-radius: {border_radius}; 
                    padding: {padding}; 
                    margin: {margin}; 
                    {shadow_style}">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def add_font_awesome():
    """Add Font Awesome for icons."""
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        """,
        unsafe_allow_html=True
    )