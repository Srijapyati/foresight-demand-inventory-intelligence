import streamlit as st

def apply_custom_css(theme="Dark Luxury"):
    if theme == "Navy Blue":
        bg_css = """
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: #f1f5f9;
        """
        sidebar_css = """
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        """
        accent_color = "#0ea5e9"
        card_bg = "rgba(30, 41, 59, 0.7)"
        banner_bg = "linear-gradient(90deg, #0284c7 0%, #0369a1 100%)"
        text_color = "#f8fafc"
    elif theme == "Light Corporate":
        bg_css = """
            background: #f8fafc;
            color: #0f172a;
        """
        sidebar_css = """
            background: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        """
        accent_color = "#2563eb"
        card_bg = "#ffffff"
        banner_bg = "linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%)"
        text_color = "#0f172a"
    else: # Dark Luxury (Default)
        bg_css = """
            background: linear-gradient(135deg, #0f1026 0%, #1a1b3a 50%, #14152e 100%);
            color: #e2e8f0;
        """
        sidebar_css = """
            background: linear-gradient(180deg, #181938 0%, #0d0e22 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        """
        accent_color = "#ff6b00"
        card_bg = "rgba(255, 255, 255, 0.04)"
        banner_bg = "linear-gradient(90deg, #ff6b00 0%, #e65100 100%)"
        text_color = "#ffffff"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        {bg_css}
    }}

    [data-testid="stSidebar"] {{
        {sidebar_css}
    }}

    .brand-header {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {text_color};
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 2px;
    }}

    .brand-sub {{
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 25px;
    }}

    .metric-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .metric-card:hover {{
        transform: translateY(-2px);
        border-color: {accent_color};
    }}

    .metric-label {{
        font-size: 0.82rem;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
    }}

    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {text_color};
    }}

    .metric-delta {{
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 4px;
    }}

    .delta-positive {{ color: #10b981; }}
    .delta-negative {{ color: #ef4444; }}
    .delta-warning {{ color: #f59e0b; }}

    .page-title-banner {{
        background: {banner_bg};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}

    .section-header {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {text_color};
        margin-top: 20px;
        margin-bottom: 12px;
        border-left: 4px solid {accent_color};
        padding-left: 10px;
    }}

    .status-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }}

    .login-box {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, delta=None, delta_type="positive"):
    delta_class = f"delta-{delta_type}"
    delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ''
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def plotly_dark_theme(theme="Dark Luxury"):
    if theme == "Light Corporate":
        return {
            "layout": {
                "paper_bgcolor": "rgba(255,255,255,0)",
                "plot_bgcolor": "rgba(255,255,255,0)",
                "font": {"color": "#1e293b", "family": "Inter"},
                "xaxis": {"gridcolor": "#e2e8f0", "zerolinecolor": "#cbd5e1"},
                "yaxis": {"gridcolor": "#e2e8f0", "zerolinecolor": "#cbd5e1"},
                "colorway": ["#2563eb", "#0284c7", "#16a34a", "#9333ea", "#db2777", "#d97706"]
            }
        }
    elif theme == "Navy Blue":
        return {
            "layout": {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "#f1f5f9", "family": "Inter"},
                "xaxis": {"gridcolor": "rgba(255,255,255,0.08)", "zerolinecolor": "rgba(255,255,255,0.12)"},
                "yaxis": {"gridcolor": "rgba(255,255,255,0.08)", "zerolinecolor": "rgba(255,255,255,0.12)"},
                "colorway": ["#0ea5e9", "#38bdf8", "#34d399", "#a855f7", "#f43f5e", "#fbbf24"]
            }
        }
    else: # Dark Luxury
        return {
            "layout": {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "#cbd5e1", "family": "Inter"},
                "xaxis": {"gridcolor": "rgba(255,255,255,0.06)", "zerolinecolor": "rgba(255,255,255,0.08)"},
                "yaxis": {"gridcolor": "rgba(255,255,255,0.06)", "zerolinecolor": "rgba(255,255,255,0.08)"},
                "colorway": ["#ff6b00", "#3b82f6", "#10b981", "#8b5cf6", "#ec4899", "#f59e0b"]
            }
        }
