"""
Styling utilities for loading CSS and Bootstrap components
Handles all visual theming and responsive design elements
"""
import streamlit as st
import os
from pathlib import Path

def get_base_path():
    """Get the base path of the project"""
    return Path(__file__).parent.parent

def load_css_file(file_path):
    """Load a CSS file and inject it into Streamlit"""
    try:
        full_path = get_base_path() / file_path
        with open(full_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        return True
    except FileNotFoundError:
        st.warning(f"CSS file not found: {file_path}")
        return False
    except Exception as e:
        st.error(f"Error loading CSS file {file_path}: {e}")
        return False

def load_bootstrap():
    """Load Bootstrap CSS and JS from CDN"""
    st.markdown("""
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    """, unsafe_allow_html=True)

def load_all_styles():
    """Load all CSS files in the correct order"""
    
    # Load Bootstrap first
    load_bootstrap()
    
    # Load custom CSS files
    css_files = [
        'styles/bootstrap_theme.css',
        'styles/components.css',
        'styles/f1_theme.css'
    ]
    
    for css_file in css_files:
        load_css_file(css_file)



def inject_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="F1 Analytics Portfolio",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yourusername/f1-analytics',
            'Report a bug': 'https://github.com/yourusername/f1-analytics/issues',
            'About': """
            # F1 Analytics Portfolio
            Interactive Formula 1 data analysis and visualization platform
            Built with Streamlit, FastF1 API, and modern web technologies
            """
        }
    )

def create_navbar(current_page="Home"):
    """Create Bootstrap navigation bar"""
    st.markdown(f"""
    <nav class="navbar navbar-expand-lg navbar-f1 sticky-top">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1 text-white fw-bold">
                🏎️ MN Analytics Hub
            </span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {'active' if current_page == 'Home' else ''} text-white" href="/">
                            Home
                        </a>
                    <li class="nav-item">
                        <a class="nav-link {'active' if current_page == 'About' else ''} text-white" href="/About">
                            About
                        </a>    
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {'active' if current_page == 'F1' else ''} text-white" href="/F1_Telemetry_Analysis">
                            F1 Analysis
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {'active' if current_page == 'Resume' else ''} text-white" href="/Resume">
                            Resume
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {'active' if current_page == 'Projects' else ''} text-white" href="/Projects">
                            Projects
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)


