"""
Main landing page for F1 Analytics Portfolio
Provides navigation and overview of all portfolio sections
"""
import streamlit as st
from utils.styling import load_all_styles, inject_page_config, create_navbar

# Configure page
inject_page_config()
load_all_styles()

# Create navigation
create_navbar("Home")

# Hero Section
st.markdown("""
<div class="container-fluid">
    <div class="f1-hero">
        <h1 class="display-3 fw-bold mb-4">
            Welcome to Milan Narula's Data Analytics Portfolio
        </h1>
        <p class="lead fs-4 mb-4">
            Your gateway to advanced data analytics and visualization
        </p>
        <p class="fs-5 text-muted mb-5">
            Explore interactive projects, real-time data analysis, and modern technologies
            that drive insights in the world of Formula 1 racing and beyond.
        </p>
        <div class="d-grid gap-3 d-md-flex justify-content-md-center">
            <a href="pages/1_🏎️_F1_Telemetry" class="btn btn-f1-primary btn-lg px-4">
                🚀 Launch F1 Analysis
            </a>
            <a href="Resume" class="btn btn-f1-primary btn-lg px-4">
                📄 View Resume
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Navigation Cards
st.markdown("""
<div class="container mt-3">
    <h2 class="text-center mb-3" style="color: var(--f1-primary);">
        🎯 Quick Navigation
    </h2>
    <div class="row g-4">
        <div class="col-lg-6">
            <div class="project-card h-100">
                <div class="d-flex align-items-center mb-3">
                    <span class="fs-1 me-3">🏎️</span>
                    <div>
                        <h4 class="text-primary mb-1">F1 Telemetry Analysis</h4>
                        <p class="text-muted mb-0">Interactive racing data exploration</p>
                    </div>
                </div>
                <p class="text-light mb-4">
                    Dive deep into Formula 1 telemetry data with real-time analysis, 
                    driver comparisons, and interactive track visualizations. 
                    Powered by the FastF1 API with live data updates.
                </p>
                <div class="mb-3">
                    <span class="badge bg-primary me-2">Python</span>
                    <span class="badge bg-secondary me-2">Streamlit</span>
                    <span class="badge bg-warning text-dark me-2">FastF1 API</span>
                    <span class="badge bg-info">Plotly</span>
                </div>
                <div class="d-grid">
                    <a href="pages/1_🏎️_F1_Telemetry" class="btn btn-f1-primary">
                        Launch Analysis →
                    </a>
                </div>
            </div>
        </div>
        
<div class="col-lg-6">
    <div class="project-card h-100">
        <div class="d-flex align-items-center mb-3">
            <span class="fs-1 me-3">📄</span>
            <div> 
                <h4 class="text-primary mb-1">Professional Resume</h4>
                <p class="text-muted mb-0">Interactive CV and experience</p>
            </div>
        </div>
        <p class="text-light mb-4">
            Comprehensive professional profile with interactive elements, 
            downloadable PDF, and LaTeX source. Showcases technical skills, 
            experience, and project portfolio.
        </p>
        <div class="mb-3">
            <span class="badge bg-success me-2">Interactive</span>
            <span class="badge bg-danger me-2">PDF Export</span>
            <span class="badge bg-warning text-dark me-2">LaTeX</span>
            <span class="badge bg-info">Bootstrap</span>
        </div>
        <div class="d-grid">
            <a href="pages/2_📄_Resume" class="btn btn-f1-primary">
                View Resume →
            </a>
        </div>
    </div>
</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Portfolio Metrics
st.markdown("""
<div class="container mt-5">
    <h2 class="text-center mb-5" style="color: var(--f1-secondary);">
        📊 Portfolio Metrics
    </h2>
    <div class="row g-4 text-center">
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">15+</div>
                <h5 class="text-light">Projects</h5>
                <p class="text-muted mb-0">Data science & analytics</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">8</div>
                <h5 class="text-light">Technologies</h5>
                <p class="text-muted mb-0">Programming languages</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">25+</div>
                <h5 class="text-light">Data Sources</h5>
                <p class="text-muted mb-0">APIs and databases</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">200+</div>
                <h5 class="text-light">Visualizations</h5>
                <p class="text-muted mb-0">Charts and dashboards</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Technology Stack
st.markdown("""
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="control-panel">
                <h3 class="text-primary mb-4 text-center">
                    🛠️ Technology Stack
                </h3>
                <div class="row">
                    <div class="col-md-4 mb-3 text-center">
                        <h5 class="text-secondary mb-3">Backend & Analysis</h5>
                        <div class="mb-2"><span class="badge bg-primary">Python</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">Pandas</span></div>
                        <div class="mb-2"><span class="badge bg-success">FastF1 API</span></div>
                        <div class="mb-2"><span class="badge bg-info">NumPy</span></div>
                    </div>
                    <div class="col-md-4 mb-3 text-center">
                        <h5 class="text-secondary mb-3">Frontend & Visualization</h5>
                        <div class="mb-2"><span class="badge bg-warning text-dark">Streamlit</span></div>
                        <div class="mb-2"><span class="badge bg-danger">Plotly</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Bootstrap 5</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">CSS3</span></div>
                    </div>
                    <div class="col-md-4 mb-3 text-center">
                        <h5 class="text-secondary mb-3">Deployment & Tools</h5>
                        <div class="mb-2"><span class="badge bg-success">Streamlit Cloud</span></div>
                        <div class="mb-2"><span class="badge bg-info">Git</span></div>
                        <div class="mb-2"><span class="badge bg-warning text-dark">LaTeX</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Docker</span></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="container-fluid footer-f1 mt-5">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6">
                <h5 class="text-primary">MN Analytics Portfolio</h5>
                <p class="text-light">
                    Showcasing modern data analytics technologies for advanced insights.
                </p>
            </div>
            <div class="d-flex gap-3 justify-content-center flex-wrap">
            <a href="mailto:your.email@gmail.com" class="btn btn-outline">
                <i class="bi bi-envelope"></i> Email Me
            </a>
            <a href="https://linkedin.com/in/yourprofile" class="btn btn-outline-light">
                <i class="bi bi-linkedin"></i> LinkedIn
            </a>
            <a href="https://github.com/yourusername" class="btn btn-outline-light">
                <i class="bi bi-github"></i> GitHub
            </a>
            </div>
            <div class="col-md-6 text-md-end">
                <p class="text-muted">
                    Designed and Built by Milan Narula using Streamlit, FastF1 API, Bootstrap and Python. 
                </p>
                <p class="text-muted">
                    © 2025 Milan Narula. All rights reserved.
                </p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
