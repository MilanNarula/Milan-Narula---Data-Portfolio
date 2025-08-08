"""
About Page
Information about the developer and the platform
"""
import streamlit as st
from utils.styling import load_all_styles, inject_page_config, create_navbar

# Configure page
inject_page_config()
load_all_styles()

# Create navigation
create_navbar("About")

st.title("ℹ️ About")

# Hero Section
st.markdown("""
<div class="f1-hero">
    <h2 class="display-5 fw-bold mb-4">👋 Hello, I'm Milan</h2>
    <p class="lead fs-5 mb-4">
        Passionate data scientist and analytics professional specialising in motorsport data analysis, 
        interactive visualizations, and real-time data processing.
    </p>
</div>
""", unsafe_allow_html=True)

# About sections
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="project-card">
        <h3 class="text-primary mb-4">🎯 My Mission</h3>
        <p class="text-light mb-4">
            I believe in the power of data to tell compelling stories and drive meaningful decisions. 
            My work focuses on transforming complex datasets into accessible, interactive experiences 
            that provide actionable insights.
        </p>
        <h4 class="text-secondary mb-3">🌟 What I Do</h4>
        <ul class="text-light">
            <li><strong>Sports Analytics:</strong> Specializing in Formula 1 telemetry analysis and performance optimization</li>
            <li><strong>Data Visualization:</strong> Creating interactive dashboards and compelling visual narratives</li>
            <li><strong>Web Development:</strong> Building responsive, user-friendly data applications</li>
            <li><strong>Machine Learning:</strong> Developing predictive models and automated analysis systems</li>
            <li><strong>Business Intelligence:</strong> Translating data insights into strategic business value</li>
        </ul>
        <h4 class="text-secondary mb-3 mt-4">💡 My Approach</h4>
        <p class="text-light">
            I combine technical expertise with domain knowledge to create solutions that are not just 
            statistically sound, but also practical and user-friendly. Every project is an opportunity 
            to push the boundaries of what's possible with data.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h3 class="text-primary mb-4">🛠️ Tech Stack</h3>
        <p class="text-light mb-4">
        <h5 class="text-secondary mb-2">Languages</h5>
        <div class="mb-3">
            <span class="badge bg-primary me-1 mb-1">Python</span>
            <span class="badge bg-secondary me-1 mb-1">SQL</span>
            <span class="badge bg-info me-1 mb-1">R</span>
            <span class="badge bg-warning text-dark me-1 mb-1">JavaScript</span>
        </div>
        <h5 class="text-secondary mb-2">Data & Analytics</h5>
        <div class="mb-3">
            <span class="badge bg-success me-1 mb-1">Pandas</span>
            <span class="badge bg-danger me-1 mb-1">NumPy</span>
            <span class="badge bg-primary me-1 mb-1">Plotly</span>
            <span class="badge bg-secondary me-1 mb-1">FastF1</span>
        </div>
        <h5 class="text-secondary mb-2">Web & Deployment</h5>
        <div class="mb-3">
            <span class="badge bg-info me-1 mb-1">Streamlit</span>
            <span class="badge bg-warning text-dark me-1 mb-1">Bootstrap</span>
            <span class="badge bg-success me-1 mb-1">Docker</span>
            <span class="badge bg-danger me-1 mb-1">AWS</span>
        </div>
        <h5 class="text-secondary mb-2">Machine Learning</h5>
        <div class="mb-3">
            <span class="badge bg-primary me-1 mb-1">Scikit-learn</span>
            <span class="badge bg-secondary me-1 mb-1">TensorFlow</span>
            <span class="badge bg-info me-1 mb-1">PyTorch</span>
        </div>
    </div>
    
    <div class="project-card mt-4">
        <h3 class="text-primary mb-4">📈 Experience</h3>
        <div class="mb-3">
            <h6 class="text-secondary">Data Science</h6>
            <div class="progress mb-2">
                <div class="progress-bar" style="width: 85%">5+ years</div>
            </div>
        </div>
        <div class="mb-3">
            <h6 class="text-secondary">F1 Analytics</h6>
            <div class="progress mb-2">
                <div class="progress-bar bg-secondary" style="width: 75%">3+ years</div>
            </div>
        </div>
        <div class="mb-3">
            <h6 class="text-secondary">Web Development</h6>
            <div class="progress mb-2">
                <div class="progress-bar bg-info" style="width: 70%">4+ years</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Featured Project Deep Dive
st.markdown("""
<div class="container mt-5">
    <div class="project-card">
        <h3 class="text-primary text-center mb-4">🏎️ Featured Project: F1 Telemetry Analysis Dashboard</h3>        
        <div class="row">
            <div class="col-md-6">
                <h4 class="text-secondary mb-3">🚀 Project Overview</h4>
                <p class="text-light mb-3">
                    The F1 Telemetry Analysis Dashboard represents the culmination of my passion for motorsport 
                    and data science. This comprehensive platform provides racing enthusiasts, analysts, and 
                    teams with unprecedented access to Formula 1 telemetry data through an intuitive, 
                    interactive interface.
                </p>
                <h5 class="text-secondary mb-2">Key Innovations:</h5>
                <ul class="text-light">
                    <li>Real-time integration with FastF1 API for live data access</li>
                    <li>Advanced caching system for optimal performance</li>
                    <li>Interactive track visualization with position tracking</li>
                    <li>Comprehensive telemetry comparison across multiple metrics</li>
                    <li>Responsive design supporting all device types</li>
                </ul>
            </div>
            <div class="col-md-6">
                <h4 class="text-secondary mb-3">📊 Technical Architecture</h4>
                <div class="bg-dark p-3 rounded mb-3">
                    <h6 class="text-primary">Frontend Layer</h6>
                    <p class="text-light mb-2">Streamlit + Bootstrap 5 + Custom CSS</p>
                    <h6 class="text-primary">Data Processing</h6>
                    <p class="text-light mb-2">Pandas + NumPy + SciPy</p>
                    <h6 class="text-primary">Visualization</h6>
                    <p class="text-light mb-2">Plotly + Interactive Charts</p>
                    <h6 class="text-primary">Data Source</h6>
                    <p class="text-light mb-0">FastF1 API + Live F1 Data</p>
                </div>
                <div class="text-center">
                    <a href="pages/1_🏎️_F1_Telemetry" class="btn btn-f1-primary">
                        🚀 Try the Dashboard
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Development Journey
st.markdown("""
<div class="container mt-5">
    <div class="control-panel">
        <h3 class="text-primary text-center mb-4">🛣️ Development Journey</h3>
        <div class="row">
            <div class="col-md-4 text-center mb-4">
                <div class="metric-card">
                    <span class="fs-1 mb-3 d-block">🎓</span>
                    <h4 class="text-secondary">Education</h4>
                    <p class="text-light">
                        Master's in Data Science, continuous learning through 
                        online courses and certifications
                    </p>
                </div>
            </div>
            <div class="col-md-4 text-center mb-4">
                <div class="metric-card">
                    <span class="fs-1 mb-3 d-block">💼</span>
                    <h4 class="text-secondary">Professional</h4>
                    <p class="text-light">
                        5+ years in data science roles, from analyst 
                        to senior positions in various industries
                    </p>
                </div>
            </div>
            <div class="col-md-4 text-center mb-4">
                <div class="metric-card">
                    <span class="fs-1 mb-3 d-block">🏎️</span>
                    <h4 class="text-secondary">Passion</h4>
                    <p class="text-light">
                        Motorsport enthusiast combining hobby with 
                        professional skills to create unique solutions
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Platform Information
st.markdown("""
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6">
            <div class="project-card">
                <h3 class="text-primary mb-4">🌐 About This Platform</h3>
                <p class="text-light mb-3">
                    This portfolio website is built entirely with modern web technologies, 
                    showcasing both technical skills and creative design capabilities.
                </p>
                <h5 class="text-secondary mb-2">Platform Features:</h5>
                <ul class="text-light">
                    <li>Multi-page architecture with seamless navigation</li>
                    <li>Responsive Bootstrap 5 design system</li>
                    <li>Custom CSS with F1-themed color scheme</li>
                    <li>Interactive resume with PDF export capabilities</li>
                    <li>Live F1 data integration and analysis tools</li>
                    <li>Optimized performance with caching strategies</li>
                </ul>
            </div>
        </div>
        <div class="col-md-6">
            <div class="project-card">
                <h3 class="text-primary mb-4">🚀 Deployment & Performance</h3>
                <p class="text-light mb-3">
                    Deployed on Streamlit Cloud with optimized performance, 
                    security best practices, and continuous integration.
                </p>
                <div class="row text-center mt-4">
                    <div class="col-6">
                        <div class="metric-card">
                            <div class="metric-number" style="font-size: 2rem;">99.9%</div>
                            <p class="text-muted">Uptime</p>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="metric-card">
                            <div class="metric-number" style="font-size: 2rem;"><2s</div>
                            <p class="text-muted">Load Time</p>
                        </div>
                    </div>
                </div>
                <div class="mt-3">
                    <h6 class="text-secondary">Tech Stack:</h6>
                    <span class="badge bg-primary me-1">Streamlit</span>
                    <span class="badge bg-warning text-dark me-1">Bootstrap 5</span>
                    <span class="badge bg-success me-1">FastF1 API</span>
                    <span class="badge bg-info me-1">Plotly</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Contact and Connect
st.markdown("""
<div class="container mt-5">
    <div class="f1-hero text-center">
        <h3 class="text-primary mb-4">🤝 Let's Connect</h3>
        <p class="lead mb-4">
            I'm always interested in discussing new opportunities, collaborations, 
            or just talking about data science and Formula 1!
        </p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
            <a href="mailto:your.email@gmail.com" class="btn btn-f1-primary">
                <i class="bi bi-envelope"></i> Email Me
            </a>
            <a href="https://linkedin.com/in/yourprofile" class="btn btn-outline-light">
                <i class="bi bi-linkedin"></i> LinkedIn
            </a>
            <a href="https://github.com/yourusername" class="btn btn-outline-light">
                <i class="bi bi-github"></i> GitHub
            </a>
            <a href="pages/2_📄_Resume" class="btn btn-outline-light">
                <i class="bi bi-file-text"></i> Resume
            </a>
        </div>
        <div class="mt-4">
            <p class="text-muted">
                Response time: Usually within 24 hours
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
