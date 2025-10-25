import streamlit as st
from utils.styling import load_all_styles, inject_page_config, create_navbar

# Configure page
inject_page_config()
load_all_styles()
st.markdown("""
        <style>
        [data-testid="stHeaderActionElements"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

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
            Your gateway into my analytical intersts and my passion for Formula 1!
        </p>
        <p class="fs-5 text-muted mb-5">
            Explore my interactive projects, take a look at my resume if you're a recruiter
            and read about my journey in the world of data analytics. Use the quick links below
            or use the navigation tab to the left to explore the site. 
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Navigation Cards
st.markdown("""
<div class="container mt-3">
    <h2 class="text-center mb-3" style="color: var(--f1-primary);">
        Quick Navigation
    </h2>
    <div class="row g-4">
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
                    <a href="/Resume" class="btn btn-f1-primary">
                        View Resume →
                    </a>
                </div>
            </div>
        </div>
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
                    <a href="/F1_Telemetry_Analysis" class="btn btn-f1-primary">
                        Launch Analysis →
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
    <h2 class="text-center mb-5" style="color: var(--f1-primary);">
        Portfolio Metrics
    </h2>
    <div class="row g-4 text-center">
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">15+</div>
                <h5 class="text-light">Projects</h5>
                <p class="text-light mb-0">Data science & analytics</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">10+</div>
                <h5 class="text-light">Technologies</h5>
                <p class="text-light mb-0">Programming languages</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">100+</div>
                <h5 class="text-light">Data Sources</h5>
                <p class="text-light mb-0">APIs and databases</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <div class="metric-number">5+</div>
                <h5 class="text-light">Years of Experience</h5>
                <p class="text-light mb-0">Data Analytics & Science</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Technology Stack
st.markdown("""
<div class="container mt-5">
    <h2 class="text-center mb-5" style="color: var(--f1-primary);">
        Technology Stack
    </h2>
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="project-card">
                <div class="row">
                    <div class="col-md-4 mb-3 text-center">
                        <h5 class="text-secondary mb-3">Backend & Analysis</h5>
                        <div class="mb-2"><span class="badge bg-primary">Python</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">Pandas</span></div>
                        <div class="mb-2"><span class="badge bg-success">FastF1 API</span></div>
                        <div class="mb-2"><span class="badge bg-info">NumPy</span></div>
                        <div class="mb-2"><span class="badge bg-info">R</span></div>
                        <div class="mb-2"><span class="badge bg-info">SQL</span></div>
                    </div>
                    <div class="col-md-4 mb-3 text-center">
                        <h5 class="text-secondary mb-3">Frontend & Visualization</h5>
                        <div class="mb-2"><span class="badge bg-warning text-dark">Streamlit</span></div>
                        <div class="mb-2"><span class="badge bg-danger">Plotly</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Bootstrap 5</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">CSS3</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">R Shiny</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">Tableau</span></div>
                        <div class="mb-2"><span class="badge bg-secondary">Power BI</span></div>
                    </div>
                    <div class="col-md-4 mb-3 text-center">
                        <h5 class="text-secondary mb-3">Deployment & Tools</h5>
                        <div class="mb-2"><span class="badge bg-success">Streamlit Cloud</span></div>
                        <div class="mb-2"><span class="badge bg-info">Git</span></div>
                        <div class="mb-2"><span class="badge bg-warning text-dark">LaTeX</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Docker</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Posit</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Cloudera</span></div>
                        <div class="mb-2"><span class="badge bg-primary">Azure DevOps</span></div>
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
        <div class="row align-items-center">
            <div class="col-md-4">
                <h5 class="text-primary">MN Analytics Portfolio</h5>
                <p class="text-light">
                    Showcasing modern data analytics technologies for advanced insights.
                </p>
            </div>
            <div class="col-md-4 d-flex justify-content-center gap-3 flex-wrap">
                <a href="mailto:narulamilan@gmail.com" class="btn btn-outline-light">
                    <i class="bi bi-envelope"></i> Email Me
                </a>
                <a href="https://linkedin.com/in/milan-narula-aa97957b/" class="btn btn-outline-light">
                    <i class="bi bi-linkedin"></i> LinkedIn
                </a>
                <a href="https://github.com/yourusername" class="btn btn-outline-light">
                    <i class="bi bi-github"></i> GitHub
                </a>
            </div>
            <div class="col-md-4 text-md-end text-light">
                <p>
                    Designed and Built by Milan Narula.
                </p>
                <p>
                    © 2025 Milan Narula. All rights reserved.
                </p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
