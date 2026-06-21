import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    # Hide default Streamlit sidebar navigation
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            .sidebar-title {font-size: 28px; font-weight: 800; color: #00d2ff; text-align: center; margin-bottom: 0px; letter-spacing: 1px;}
            .sidebar-tagline {font-size: 13px; color: #aaaaaa; text-align: center; margin-bottom: 25px; font-style: italic;}
        </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-title">⚛️ Q-Refine</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-tagline">Quantum Robustness Platform</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        # Determine current page
        current_page = st.session_state.get("current_page", "Benchmark Pipeline")
        
        selected = option_menu(
            menu_title=None,
            options=["Benchmark Pipeline", "Hardware Settings"],
            icons=["bar-chart-line-fill", "gear-fill"],
            default_index=["Benchmark Pipeline", "Hardware Settings"].index(current_page) if current_page in ["Benchmark Pipeline", "Hardware Settings"] else 0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#00d2ff", "font-size": "18px"}, 
                "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px", "--hover-color": "#262730"},
                "nav-link-selected": {"background-color": "#ff4b4b", "color": "white", "font-weight": "bold"},
            }
        )
        
        if selected != current_page:
            st.session_state["current_page"] = selected
            if selected == "Benchmark Pipeline":
                st.switch_page("app.py")
            elif selected == "Hardware Settings":
                st.switch_page("pages/3_Settings.py")
