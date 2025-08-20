# Copilot Instructions for Milan Narula Data Portfolio

## Project Overview
This is a multi-page data analytics portfolio built with Python and Streamlit. It showcases interactive dashboards, real-time Formula 1 telemetry analysis, customer/property analytics, and a resume viewer. The UI is heavily customized with Bootstrap 5, custom CSS, and responsive design for both desktop and mobile.

## Architecture & Key Components
- **Home.py**: Main landing page, sets up navigation and global styles.
- **pages/**: Contains individual Streamlit apps for each portfolio section (e.g., F1 Telemetry, Resume, About, Analytics).
- **utils/**: Shared Python utilities for data processing, PDF handling, and custom styling.
- **assets/**: Static files, datasets, images, and LaTeX resume source.
- **styles/**: Custom CSS themes (`f1_theme.css`, `components.css`) for branding and advanced UI effects.
- **config/**: TOML config for Streamlit settings.

## Developer Workflows
- **Run Locally**: Launch with `streamlit run Home.py` from the workspace root.
- **Add Pages**: Place new `.py` files in `pages/` and update navigation in `Home.py` and/or `utils/styling.py`.
- **Custom Styling**: Edit CSS in `styles/` and use utility functions from `utils/styling.py` to inject styles.
- **Data Caching**: F1 telemetry uses SQLite cache in `pages/cache/` for fast repeated analysis.
- **PDF Resume**: Source is in `assets/resume_latex/`; PDF is generated externally and displayed via Streamlit.

## Project-Specific Patterns
- **Streamlit UI**: Uses HTML/CSS in `st.markdown` for advanced layouts (cards, hero sections, control panels).
- **Navigation**: Custom navbar via `create_navbar()` in `utils/styling.py`.
- **Telemetry Analysis**: Data loaded and cached per session/year; interactive controls for driver/lap selection and track position.
- **Plotly Integration**: Track maps and telemetry charts styled via custom CSS classes.
- **Responsive Design**: All major UI components adapt for mobile via CSS media queries.

## External Dependencies
- **FastF1**: For F1 telemetry data (see `requirements.txt`).
- **Plotly**: For interactive charts.
- **Bootstrap 5**: Used via custom CSS, not via CDN.

## Conventions & Integration Points
- **Page Structure**: Each page is a self-contained Streamlit app, but shares styles/utilities.
- **Session State**: Use `st.session_state` for cross-component data (e.g., selected drivers, loaded sessions).
- **Custom Components**: Use CSS classes defined in `styles/` for consistent look/feel.
- **Cache**: Place large or repeated data in `pages/cache/`.

## Example Patterns
- To add a new analytics dashboard:
  1. Create `pages/7NewDashboard.py`.
  2. Add navigation link in `Home.py` and/or `utils/styling.py`.
  3. Use `st.markdown` with custom CSS for layout.
  4. Store any large data in `pages/cache/`.

- To update the resume:
  1. Edit `assets/resume_latex/resume.tex` and recompile to PDF.
  2. Replace PDF in `assets/Milan Narula Resume 2025.pdf`.

## References
- See `README.md` for high-level project description.
- See `utils/` for reusable code and styling patterns.
- See `styles/` for all UI conventions.

---
For questions or unclear patterns, ask the user for clarification or examples from existing pages.
