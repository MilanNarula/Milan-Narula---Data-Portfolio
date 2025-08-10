import streamlit as st
from utils.styling import load_all_styles, inject_page_config, create_navbar
from utils.pdf_utils import (
    display_pdf_viewer, create_pdf_download_button, 
    compile_latex_resume, save_latex_template, get_latex_template
)
import os
import base64
from pathlib import Path



# Configure page
inject_page_config()
load_all_styles()

# Create navigation
create_navbar("Resume")

st.title("Professional Resume")

# Resume format selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    resume_format = st.radio(
        "Choose Resume Format:",
        ["📱 Interactive View", "📄 PDF View", "⚡ LaTeX Source"],
        horizontal=True
    )

def display_interactive_resume():
    """Display interactive HTML resume with Bootstrap styling"""
     
    # Headshot Image Import  
    img_path = Path(__file__).parent.parent / "static" / "images" / "NarulaM_Photo.jpg"
    with open(img_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
        
    # Path to the logo image
    logo_path = Path(__file__).parent.parent / "static" / "images" / "Reserve_Bank_of_Australia_logo.svg.png"
    with open(logo_path, "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
        
     # Path to the logo image
    kpmg_path = Path(__file__).parent.parent / "static" / "images" / "kpmg.D-f0ee9cf2.png"
    with open(kpmg_path, "rb") as logo_file:
        kpmg_base64 = base64.b64encode(logo_file.read()).decode()
  
    # Profile header
    st.markdown(f"""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <!-- Profile Header -->
                <div class="text-center mb-5">
                    <div class="mb-4">
                        <div style="width: 350px; height: 350px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 4px solid #FF6B35;">
                            <img src="data:image/jpeg;base64,{img_base64}" alt="Your Profile Photo" style="width: 100%; height: 100%; object-fit: cover;  object-position: center 30%">
                        </div>
                    </div>
                    <h1 class="display-4 text-primary fw-bold">Milan Narula</h1>
                    <h3 class="text-secondary mb-4">Data Scientist & Analytics Professional</h3>
                    <div class="row justify-content-center">
                        <div class="col-auto">
                            <div class="d-flex gap-3 justify-content-center flex-wrap">
                                <span class="badge bg-primary fs-6 px-3 py-2">
                                    <i class="bi bi-envelope"></i> narulamilan@gmail.com
                                </span>
                                <span class="badge bg-secondary fs-6 px-3 py-2">
                                    <i class="bi bi-phone"></i> +61 0424 043 792
                                </span>
                                <span class="badge bg-info fs-6 px-3 py-2">
                                    <i class="bi bi-linkedin"></i> LinkedIn
                                </span>
                                <span class="badge bg-success fs-6 px-3 py-2">
                                    <i class="bi bi-github"></i> GitHub
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Summary
    st.markdown("""
    <div class="container mb-5">
        <div class="card" style="border-radius: 10px;">
            <div class="card-header" style="border-radius: 10px;">
                <h3 class="mb-0"><i class="bi bi-person-circle"></i> Professional Summary</h3>
            </div>
            <div class="card-body">
                <p class="lead text-light" style="text-align: justify; font-size: 20px"> 
                    Senior Analytics Leader with 5+ years delivering measurable impact across commercial, 
                    operational, and real-time analytics. Combines advanced statistical modeling, machine 
                    learning, and AI/GenAI with business pragmatism to convert complex data into strategies that 
                    drive revenue, optimize costs, reduce risk, and improve efficiency. Proven record building and 
                    scaling cross-functional teams, architecting real-time data pipelines and event-driven analytics, 
                    and delivering decision-ready insights in fast-paced, highly regulated environments. 
                    Experience spans real-time operations (anomaly detection, predictive maintenance), finance and 
                    pricing (forecasting, dynamic pricing), risk and compliance (fraud, model governance), product and engineering (experimentation, telemetry), supply chain and workforce analytics, and ESG reporting. 
                    Strong in data governance, MLOps/ModelOps, and operationalizing analytics for continuous improvement. 
                    <br><br>Tools: SQL, Python, R, Alteryx, Azure, Tableau, Power BI.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Experience Section
    st.markdown(f"""
    <div class="container mb-5">
        <div class="card">
            <div class="card-header">
                <h3 class="mb-0"><i class="bi bi-briefcase"></i> Professional Experience</h3>
            </div>
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-md-8">
                        <h4 class="text-primary">Manager - Data Analytics</h4>
                        <h5 class="text-secondary mb-3">Reserve Bank of Australia</h5>
                        <ul class="text-light">
                            <li>Developed interactive F1 telemetry analysis dashboard serving 10,000+ users globally</li>
                            <li>Implemented real-time data pipelines processing 1M+ telemetry records daily with 99.9% uptime</li>
                            <li>Created automated reporting systems reducing manual analysis work by 75%</li>
                            <li>Led cross-functional team of 5 data professionals in delivering analytics solutions</li>
                            <li>Optimized database queries resulting in 40% faster dashboard loading times</li>
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <div class="bg-dark p-3 rounded">
                             <img src="data:image/png;base64,{logo_base64}" alt="RBA Logo" style="width: 90px; height: auto; margin-bottom: 10px; border-radius: 3px; float: right;">
                            <p class="text-primary mb-2"><strong>July 2023 - Present</strong></p>
                            <p class="text-muted mb-2">Sydney, Australia</p>
                            <div>
                                <span class="badge bg-primary me-1 mb-1">R</span>
                                <span class="badge bg-secondary me-1 mb-1">SQL</span>
                                <span class="badge bg-warning text-dark me-1 mb-1">Power BI</span>
                                <span class="badge bg-info me-1 mb-1">Tableau</span>
                                <span class="badge bg-success me-1 mb-1">Alteryx</span>
                            </div>
                        </div>
                    </div>
                </div>
                <hr class="my-4" style="border-color: var(--f1-primary); border-width: 2px;">
                <div class="row">
                    <div class="col-md-8">
                        <h4 class="text-primary">Lead Data Analyst</h4>
                        <h5 class="text-secondary mb-3">Reserve Bank of Australia</h5>
                        <ul class="text-light">
                            <li>Built predictive models for customer behavior analysis using machine learning</li>
                            <li>Designed and maintained ETL pipelines for multi-source data integration</li>
                            <li>Created executive dashboards using Tableau and Power BI</li>
                            <li>Improved data processing efficiency by 60% through optimization</li>
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <div class="bg-dark p-3 rounded">
                            <p class="text-primary mb-2"><strong>2020 - 2022</strong></p>
                            <p class="text-muted mb-2">Boston, MA</p>
                            <div>
                                <span class="badge bg-danger me-1 mb-1">R</span>
                                <span class="badge bg-warning text-dark me-1 mb-1">Tableau</span>
                                <span class="badge bg-info me-1 mb-1">SQL</span>
                                <span class="badge bg-success me-1 mb-1">Excel</span>
                            </div>
                        </div>
                    </div>
                </div>
                <hr class="my-4" style="border-color: var(--f1-primary); border-width: 2px;">
                <div class="row">
                    <div class="col-md-8">
                        <h4 class="text-primary">Senior Consultant - Data Analytics</h4>
                        <h5 class="text-secondary mb-3">KPMG</h5>
                        <ul class="text-light">
                            <li>Built predictive models for customer behavior analysis using machine learning</li>
                            <li>Designed and maintained ETL pipelines for multi-source data integration</li>
                            <li>Created executive dashboards using Tableau and Power BI</li>
                            <li>Improved data processing efficiency by 60% through optimization</li>
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <div class="bg-dark p-3 rounded">
                        <img src="data:image/png;base64,{kpmg_base64}" alt="RBA Logo" style="width: 90px; height: auto; margin-bottom: 10px; border-radius: 3px; float: right;">
                            <p class="text-primary mb-2"><strong>2020 - 2022</strong></p>
                            <p class="text-muted mb-2">Boston, MA</p>
                            <div>
                                <span class="badge bg-danger me-1 mb-1">Alteryx</span>
                                <span class="badge bg-warning text-dark me-1 mb-1">SQL</span>
                                <span class="badge bg-info me-1 mb-1">Power BI</span>
                                <span class="badge bg-success me-1 mb-1">Tableau Prep</span>
                            </div>
                        </div>
                    </div>
                </div>
                <hr class="my-4" style="border-color: var(--f1-primary); border-width: 2px;">
                <div class="row">
                    <div class="col-md-8">
                        <h4 class="text-primary">Senior Consultant - Data Analytics</h4>
                        <h5 class="text-secondary mb-3">KPMG</h5>
                        <ul class="text-light">
                            <li>Built predictive models for customer behavior analysis using machine learning</li>
                            <li>Designed and maintained ETL pipelines for multi-source data integration</li>
                            <li>Created executive dashboards using Tableau and Power BI</li>
                            <li>Improved data processing efficiency by 60% through optimization</li>
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <div class="bg-dark p-3 rounded">
                            <p class="text-primary mb-2"><strong>2020 - 2022</strong></p>
                            <p class="text-muted mb-2">Boston, MA</p>
                            <div>
                                <span class="badge bg-danger me-1 mb-1">R</span>
                                <span class="badge bg-warning text-dark me-1 mb-1">Tableau</span>
                                <span class="badge bg-info me-1 mb-1">SQL</span>
                                <span class="badge bg-success me-1 mb-1">Excel</span>
                            </div>
                        </div>
                    </div>
                </div>
                <hr class="my-4" style="border-color: var(--f1-primary); border-width: 2px;">
                <div class="row">
                    <div class="col-md-8">
                        <h4 class="text-primary">Senior Consultant - Data Analytics</h4>
                        <h5 class="text-secondary mb-3">KPMG</h5>
                        <ul class="text-light">
                            <li>Built predictive models for customer behavior analysis using machine learning</li>
                            <li>Designed and maintained ETL pipelines for multi-source data integration</li>
                            <li>Created executive dashboards using Tableau and Power BI</li>
                            <li>Improved data processing efficiency by 60% through optimization</li>
                        </ul>
                    </div>
                    <div class="col-md-4">
                        <div class="bg-dark p-3 rounded">
                            <p class="text-primary mb-2"><strong>2020 - 2022</strong></p>
                            <p class="text-muted mb-2">Boston, MA</p>
                            <div>
                                <span class="badge bg-danger me-1 mb-1">R</span>
                                <span class="badge bg-warning text-dark me-1 mb-1">Tableau</span>
                                <span class="badge bg-info me-1 mb-1">SQL</span>
                                <span class="badge bg-success me-1 mb-1">Excel</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills Section with animated progress bars
    skills_left = {
        "Python": 95,
        "SQL": 90,
        "R": 80,
        "JavaScript": 75
    }

    skills_right = {
        "Streamlit": 95,
        "Plotly": 90,
        "Pandas": 95,
        "FastF1 API": 90
    }

    # Build the HTML for skills in one string
    skills_html = """<div class="container mb-5">
        <div class="card">
            <div class="card-header">
                <h3 class="mb-0"><i class="bi bi-tools"></i> Technical Skills</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h5 class="text-secondary mb-3">Programming & Analysis</h5>
    """

    for skill, level in skills_left.items():
        skills_html += f"""<strong>{skill}</strong>
        <div class="progress mb-3">
            <div class="progress-bar bg-success" role="progressbar" style="width: {level}%;"
                aria-valuenow="{level}" aria-valuemin="0" aria-valuemax="100">{level}%
            </div>
        </div>
        """

    skills_html += """</div>
                    <div class="col-md-6">
                        <h5 class="text-secondary mb-3">Tools & Frameworks</h5>
    """

    for skill, level in skills_right.items():
        skills_html += f"""<strong>{skill}</strong>
        <div class="progress mb-3">
            <div class="progress-bar bg-info" role="progressbar" style="width: {level}%;"
                aria-valuenow="{level}" aria-valuemin="0" aria-valuemax="100">{level}%
            </div>
        </div>
        """

    skills_html += """</div>
                </div>
                <div class="mt-4">
                    <h5 class="text-secondary mb-3">Additional Technologies</h5>
                    <span class="badge bg-primary me-2 mb-2">Docker</span>
                    <span class="badge bg-secondary me-2 mb-2">Git</span>
                    <span class="badge bg-success me-2 mb-2">AWS</span>
                    <span class="badge bg-danger me-2 mb-2">Redis</span>
                    <span class="badge bg-warning text-dark me-2 mb-2">MongoDB</span>
                    <span class="badge bg-info me-2 mb-2">PostgreSQL</span>
                    <span class="badge bg-dark me-2 mb-2">LaTeX</span>
                    <span class="badge bg-primary me-2 mb-2">Bootstrap</span>
                </div>
            </div>
        </div>
    </div>
    """

    st.markdown(skills_html, unsafe_allow_html=True)

    # Projects Section
    st.markdown("""
    <div class="container mb-5">
        <div class="card">
            <div class="card-header">
                <h3 class="mb-0"><i class="bi bi-code-square"></i> Featured Projects</h3>
            </div>
            <div class="card-body">
                <div class="project-card mb-4">
                    <div class="d-flex align-items-start">
                        <span class="fs-1 me-3">🏎️</span>
                        <div class="flex-grow-1">
                            <h4 class="text-primary mb-2">F1 Telemetry Analysis Dashboard</h4>
                            <p class="text-light mb-3">
                                Comprehensive web application for Formula 1 data analysis featuring real-time telemetry 
                                comparison, interactive track visualization, and driver performance metrics. 
                                Built with modern web technologies and connected to live FastF1 API.
                            </p>
                            <div class="mb-3">
                                <span class="badge bg-primary me-1">Python</span>
                                <span class="badge bg-secondary me-1">Streamlit</span>
                                <span class="badge bg-warning text-dark me-1">FastF1 API</span>
                                <span class="badge bg-info me-1">Plotly</span>
                                <span class="badge bg-success me-1">Bootstrap</span>
                            </div>
                            <p class="text-success mb-0">
                                <strong>Impact:</strong> 10,000+ users, featured in motorsport analytics communities
                            </p>
                        </div>
                    </div>
                </div>
                <div class="project-card">
                    <div class="d-flex align-items-start">
                        <span class="fs-1 me-3">📊</span>
                        <div class="flex-grow-1">
                            <h4 class="text-primary mb-2">Multi-Page Analytics Portfolio</h4>
                            <p class="text-light mb-3">
                                Professional portfolio website showcasing data science projects, interactive resume, 
                                and technical capabilities. Features responsive design, PDF generation, and 
                                modern UI/UX principles.
                            </p>
                            <div class="mb-3">
                                <span class="badge bg-danger me-1">HTML/CSS</span>
                                <span class="badge bg-warning text-dark me-1">Bootstrap 5</span>
                                <span class="badge bg-info me-1">Streamlit</span>
                                <span class="badge bg-success me-1">LaTeX</span>
                            </div>
                            <p class="text-success mb-0">
                                <strong>Features:</strong> Interactive elements, PDF export, responsive design
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Education Section
    st.markdown("""
    <div class="container mb-5">
        <div class="card">
            <div class="card-header">
                <h3 class="mb-0"><i class="bi bi-mortarboard"></i> Education & Certifications</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h5 class="text-primary">Education</h5>
                        <div class="mb-3">
                            <h6 class="text-secondary">Master of Science in Data Science</h6>
                            <p class="text-light mb-1">University of Technology</p>
                            <p class="text-muted">Boston, MA • 2020</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="text-secondary">Bachelor of Science in Computer Science</h6>
                            <p class="text-light mb-1">State University</p>
                            <p class="text-muted">Boston, MA • 2018</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h5 class="text-primary">Certifications</h5>
                        <div class="mb-2">
                            <span class="badge bg-warning text-dark me-2">AWS</span>
                            <span class="text-light">Solutions Architect (2023)</span>
                        </div>
                        <div class="mb-2">
                            <span class="badge bg-info me-2">GCP</span>
                            <span class="text-light">Professional Data Engineer (2022)</span>
                        </div>
                        <div class="mb-2">
                            <span class="badge bg-success me-2">Tableau</span>
                            <span class="text-light">Desktop Specialist (2021)</span>
                        </div>
                        <div class="mb-2">
                            <span class="badge bg-primary me-2">Python</span>
                            <span class="text-light">Data Science Certification (2020)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_pdf_resume():
    """Display PDF version of resume"""
    st.markdown("""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="text-center mb-4">
                    <h3 class="text-primary">📄 PDF Resume</h3>
                    <p class="text-light">Professional resume in PDF format</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if PDF exists
    pdf_path = "assets/Milan Narula Resume 2025.pdf"
    if os.path.exists(pdf_path):
        # Display PDF
        if display_pdf_viewer(pdf_path, height=800):
            # Create download button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                create_pdf_download_button(pdf_path, "Your_Name_Resume.pdf")
    else:
        st.markdown("""
        <div class="alert alert-warning text-center">
            <h4>📄 PDF Resume Not Found</h4>
            <p>The PDF resume hasn't been generated yet. You can create it from the LaTeX source.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔧 Generate PDF from LaTeX", type="primary", use_container_width=True):
                if compile_latex_resume():
                    st.success("✅ PDF generated successfully!")
                    st.rerun()
                else:
                    st.error("❌ PDF generation failed")

def display_latex_source():
    """Display and edit LaTeX source"""
    st.markdown("""
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="text-center mb-4">
                    <h3 class="text-primary">⚡ LaTeX Resume Source</h3>
                    <p class="text-light">Edit the LaTeX source code and compile to PDF</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    latex_path = "assets/resume_latex/resume.tex"
    
    # Check if LaTeX file exists
    if os.path.exists(latex_path):
        with open(latex_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
    else:
        # Create default template if it doesn't exist
        latex_content = get_latex_template()
        save_latex_template(latex_content)
        st.info("Created default LaTeX template")
    
    # Editable LaTeX source
    edited_latex = st.text_area(
        "LaTeX Source Code:",
        value=latex_content,
        height=500,
        help="Edit the LaTeX source and compile to generate PDF"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Changes", type="secondary", use_container_width=True):
            if save_latex_template(edited_latex):
                st.success("✅ LaTeX source saved!")
            else:
                st.error("❌ Error saving LaTeX source")
    
    with col2:
        if st.button("🔧 Compile to PDF", type="primary", use_container_width=True):
            try:
                # Save current content first
                save_latex_template(edited_latex)
                
                if compile_latex_resume():
                    st.success("✅ PDF compiled successfully!")
                    st.info("Switch to PDF view to see the result")
                else:
                    st.error("❌ LaTeX compilation failed")
            except Exception as e:
                st.error(f"Compilation error: {e}")
    
    with col3:
        if st.button("🔄 Reset to Default", use_container_width=True):
            if save_latex_template(get_latex_template()):
                st.success("✅ Reset to default template")
                st.rerun()

# Display selected format
if resume_format == "📱 Interactive View":
    display_interactive_resume()
elif resume_format == "📄 PDF View":
    display_pdf_resume()
else:
    display_latex_source()

# Footer with additional links
st.markdown("""
<div class="container mt-5">
    <div class="text-center">
        <div class="control-panel">
            <h4 class="text-primary mb-3">🔗 Connect With Me</h4>
            <div class="row justify-content-center">
                <div class="col-auto">
                    <a href="mailto:your.email@gmail.com" class="btn btn-outline-primary me-2 mb-2">
                        <i class="bi bi-envelope"></i> Email
                    </a>
                    <a href="https://linkedin.com/in/yourprofile" class="btn btn-outline-primary me-2 mb-2">
                        <i class="bi bi-linkedin"></i> LinkedIn
                    </a>
                    <a href="https://github.com/yourusername" class="btn btn-outline-primary me-2 mb-2">
                        <i class="bi bi-github"></i> GitHub
                    </a>
                    <a href="pages/3_📊_Projects" class="btn btn-outline-primary mb-2">
                        <i class="bi bi-folder"></i> View All Projects
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
