"""
PDF utilities for resume handling and LaTeX compilation
Handles PDF generation, viewing, and LaTeX processing
"""
import streamlit as st
import subprocess
import os
import base64
from pathlib import Path
import tempfile

def get_base_path():
    """Get the base path of the project"""
    return Path(__file__).parent.parent

def compile_latex_resume():
    """
    Compile LaTeX resume to PDF
    
    Returns:
        bool: Success status
    """
    latex_dir = get_base_path() / "assets" / "resume_latex"
    latex_file = "resume.tex"
    
    if not (latex_dir / latex_file).exists():
        st.error("LaTeX resume template not found")
        return False
    
    try:
        # Change to LaTeX directory
        original_dir = os.getcwd()
        os.chdir(latex_dir)
        
        # Compile LaTeX (run twice for proper cross-references)
        with st.spinner("Compiling LaTeX resume..."):
            result1 = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", latex_file],
                capture_output=True,
                text=True
            )
            
            if result1.returncode != 0:
                st.error(f"LaTeX compilation failed: {result1.stderr}")
                os.chdir(original_dir)
                return False
            
            # Second compilation for cross-references
            result2 = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", latex_file],
                capture_output=True,
                text=True
            )
        
        # Copy PDF to assets folder
        pdf_source = latex_dir / "resume.pdf"
        pdf_target = get_base_path() / "assets" / "resume.pdf"
        
        if pdf_source.exists():
            import shutil
            shutil.copy2(pdf_source, pdf_target)
        
        # Clean up auxiliary files
        aux_extensions = ['.aux', '.log', '.out', '.fls', '.fdb_latexmk']
        for ext in aux_extensions:
            aux_file = latex_dir / f"resume{ext}"
            if aux_file.exists():
                aux_file.unlink()
        
        os.chdir(original_dir)
        return True
        
    except subprocess.CalledProcessError as e:
        os.chdir(original_dir)
        st.error(f"LaTeX compilation failed: {e}")
        return False
    except Exception as e:
        os.chdir(original_dir)
        st.error(f"Error during compilation: {e}")
        return False

@st.cache_data
def load_pdf_as_base64(pdf_path):
    """
    Load PDF file and convert to base64 for embedding
    
    Args:
        pdf_path (str): Path to PDF file
    
    Returns:
        str: Base64 encoded PDF or None
    """
    try:
        full_path = get_base_path() / pdf_path
        if not full_path.exists():
            return None
            
        with open(full_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        return base64_pdf
    except Exception as e:
        st.error(f"Error loading PDF: {e}")
        return None

def display_pdf_viewer(pdf_path, height=800):
    """
    Display PDF in Streamlit using iframe
    
    Args:
        pdf_path (str): Path to PDF file
        height (int): Viewer height
    """
    base64_pdf = load_pdf_as_base64(pdf_path)
    
    if base64_pdf:
        pdf_display = f'''
        <div class="pdf-container">
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" 
                    height="{height}px" 
                    type="application/pdf"
                    style="border-radius: 10px;">
                <p>Your browser doesn't support PDF viewing. 
                   <a href="data:application/pdf;base64,{base64_pdf}" download>
                   Click here to download the PDF
                   </a>
                </p>
            </iframe>
        </div>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
        return True
    else:
        st.error("PDF file not found. Please generate the resume first.")
        return False

def create_pdf_download_button(pdf_path, filename="resume.pdf", label="📄 Download PDF Resume"):
    """
    Create download button for PDF
    
    Args:
        pdf_path (str): Path to PDF file
        filename (str): Download filename
        label (str): Button label
    
    Returns:
        bool: Success status
    """
    try:
        full_path = get_base_path() / pdf_path
        if not full_path.exists():
            st.error("PDF file not found")
            return False
            
        with open(full_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        st.download_button(
            label=label,
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )
        return True
    except Exception as e:
        st.error(f"Error creating download button: {e}")
        return False

def get_latex_template():
    """
    Get default LaTeX resume template
    
    Returns:
        str: LaTeX template content
    """
    return r"""
\documentclass[letterpaper,11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{fontawesome}
\usepackage{hyperref}
\usepackage{enumitem}

\geometry{margin=0.75in}

\definecolor{primarycolor}{RGB}{255, 107, 53}
\definecolor{secondarycolor}{RGB}{247, 147, 30}

\hypersetup{
    colorlinks=true,
    linkcolor=primarycolor,
    urlcolor=primarycolor,
    pdfborder={0 0 0}
}

\pagestyle{empty}

\begin{document}

\begin{center}
    {\huge \textbf{\textcolor{primarycolor}{Your Name}}}\\[0.3cm]
    {\large Data Scientist \& Analytics Professional}\\[0.5cm]
    
    \faEnvelope \hspace{0.1cm} your.email@gmail.com \hspace{0.5cm}
    \faPhone \hspace{0.1cm} +1 (555) 123-4567 \hspace{0.5cm}
    \faLinkedin \hspace{0.1cm} \href{https://linkedin.com/in/yourprofile}{LinkedIn} \hspace{0.5cm}
    \faGithub \hspace{0.1cm} \href{https://github.com/yourusername}{GitHub}
\end{center}

\vspace{0.5cm}

\section*{\textcolor{primarycolor}{Professional Summary}}
Experienced data scientist and analytics professional with expertise in F1 telemetry analysis, 
interactive dashboard development, and real-time data processing. Proven track record of 
delivering insights through advanced visualization and statistical modeling.

\section*{\textcolor{primarycolor}{Professional Experience}}

\textbf{Senior Data Analyst} \hfill \textit{2022 - Present}\\
\textit{Company ABC} \hfill \textit{New York, NY}
\begin{itemize}[leftmargin=0.5in]
    \item Developed interactive F1 telemetry analysis dashboard using Python and Streamlit, serving 10,000+ users
    \item Implemented real-time data processing pipelines handling 1M+ telemetry records daily with 99.9\% uptime
    \item Created automated reporting systems reducing manual analysis work by 75\%
    \item Led cross-functional team of 5 data professionals in delivering analytics solutions
    \item Optimized database queries resulting in 40\% faster dashboard loading times
\end{itemize}

\textbf{Data Analyst} \hfill \textit{2020 - 2022}\\
\textit{Data Solutions Inc.} \hfill \textit{Boston, MA}
\begin{itemize}[leftmargin=0.5in]
    \item Built predictive models for customer behavior analysis using machine learning techniques
    \item Designed and maintained ETL pipelines for multi-source data integration
    \item Created executive dashboards using Tableau and Power BI
\end{itemize}

\section*{\textcolor{primarycolor}{Technical Skills}}

\textbf{Programming Languages:} Python, SQL, R, JavaScript, HTML/CSS\\
\textbf{Data Analysis:} Pandas, NumPy, SciPy, Statsmodels, Scikit-learn\\
\textbf{Visualization:} Plotly, Streamlit, Tableau, D3.js, Matplotlib, Seaborn\\
\textbf{Machine Learning:} TensorFlow, PyTorch, XGBoost, Random Forest\\
\textbf{Databases:} PostgreSQL, MySQL, MongoDB, Redis\\
\textbf{Cloud Platforms:} AWS, Azure, Google Cloud Platform\\
\textbf{Tools:} Git, Docker, Jupyter, FastF1 API, Apache Spark

\section*{\textcolor{primarycolor}{Featured Projects}}

\textbf{F1 Telemetry Analysis Dashboard}
\begin{itemize}[leftmargin=0.5in]
    \item Interactive web application for Formula 1 data analysis and driver comparison
    \item Real-time telemetry visualization with track mapping and performance metrics
    \item Technologies: Python, Streamlit, FastF1 API, Plotly, Bootstrap
    \item Impact: 10,000+ users, featured in motorsport analytics communities
\end{itemize}

\textbf{Multi-Page Analytics Portfolio}
\begin{itemize}[leftmargin=0.5in]
    \item Comprehensive portfolio showcasing data science projects and professional experience
    \item Responsive design with custom CSS and Bootstrap integration
    \item Features: Interactive resume, project galleries, PDF generation
\end{itemize}

\section*{\textcolor{primarycolor}{Education}}

\textbf{Master of Science in Data Science} \hfill \textit{2020}\\
\textit{University of Technology} \hfill \textit{Boston, MA}

\textbf{Bachelor of Science in Computer Science} \hfill \textit{2018}\\
\textit{State University} \hfill \textit{Boston, MA}

\section*{\textcolor{primarycolor}{Certifications}}

\textbf{AWS Certified Solutions Architect} \hfill \textit{2023}\\
\textbf{Google Cloud Professional Data Engineer} \hfill \textit{2022}\\
\textbf{Tableau Desktop Specialist} \hfill \textit{2021}

\end{document}
"""

def save_latex_template(content=None):
    """
    Save LaTeX template to file
    
    Args:
        content (str): LaTeX content (uses default if None)
    
    Returns:
        bool: Success status
    """
    try:
        latex_dir = get_base_path() / "assets" / "resume_latex"
        latex_dir.mkdir(parents=True, exist_ok=True)
        
        latex_file = latex_dir / "resume.tex"
        
        if content is None:
            content = get_latex_template()
        
        with open(latex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        st.error(f"Error saving LaTeX template: {e}")
        return False
