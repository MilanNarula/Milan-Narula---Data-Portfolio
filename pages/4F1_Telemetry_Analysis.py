"""
F1 Telemetry Analysis Page
Main F1 data analysis application with interactive telemetry comparison
"""
import time
import streamlit as st
from utils.styling import load_all_styles, inject_page_config, create_navbar
from utils.f1_functions import (
    setup_f1_cache, load_session_data, get_available_events, 
    process_driver_data, create_track_plot, create_telemetry_plots,
    update_track_marker, get_lap_summary_stats
)

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

# Setup F1 cache
setup_f1_cache()

# Create navigation
create_navbar("F1")

# Initialize session state
if 'session_loaded' not in st.session_state:
    st.session_state.session_loaded = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'available_events' not in st.session_state:
    st.session_state.available_events = []

st.title("🏎️ F1 Telemetry Analysis Dashboard")

# Create tabs[1][4]
tab1, tab2, tab3 = st.tabs(["⚙️ Configuration", "📊 Analysis", "🏁 Driver Stats"])

# Tab 1: Configuration (formerly sidebar content)
with tab1:
    st.markdown("""
    <div class="control-panel">
        <h3 class="text-primary text-center mb-4">🔧 Analysis Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Step 1: Session Selection
        st.markdown("""
        <div class="control-section">
            <h4 class="text-secondary">1️⃣ Select F1 Session</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Year selection
        current_year = 2025
        year = st.selectbox(
            "Championship Year", 
            list(range(2020, current_year + 1))[::-1], 
            index=0,
            help="Select the F1 championship year to analyze"
        )
        
        # Load available events
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            if st.button("🔄 Load Events", type="secondary", use_container_width=True):
                with st.spinner("Loading available events..."):
                    events = get_available_events(year)
                    st.session_state.available_events = events
                    st.success(f"✅ Loaded {len(events)} events")
        
        with subcol2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Cache cleared!")
        
        # Event selection
        if st.session_state.available_events:
            grand_prix = st.selectbox(
                "Grand Prix", 
                st.session_state.available_events,
                help="Select the Grand Prix event to analyze"
            )
        else:
            st.info("👆 Click 'Load Events' to see available races")
            grand_prix = st.text_input(
                "Or enter Grand Prix name manually:", 
                placeholder="e.g., Hungarian Grand Prix"
            )
        
        # Session type selection
        session_type_options = {
            '🏃‍♂️ Practice 1': 'FP1',
            '🏃‍♂️ Practice 2': 'FP2', 
            '🏃‍♂️ Practice 3': 'FP3',
            '⚡ Sprint Qualifying': 'SQ',
            '🏁 Sprint': 'S',
            '🎯 Qualifying': 'Q',
            '🏆 Race': 'R'
        }
        
        session_display = st.selectbox(
            "Session Type", 
            list(session_type_options.keys()), 
            index=6,
            help="Select the session type to analyze"
        )
        session_type = session_type_options[session_display]
        
        # Load session button
        if st.button("🚀 Load Session", type="primary", use_container_width=True):
            if grand_prix:
                with st.spinner("Loading session data from FastF1 API..."):
                    session, error = load_session_data(year, grand_prix, session_type)
                    if session:
                        st.session_state.session = session
                        st.session_state.session_loaded = True
                        st.session_state.year = year
                        st.session_state.grand_prix = grand_prix
                        st.session_state.session_display = session_display
                        st.success("✅ Session loaded successfully!")
                    else:
                        st.error(f"❌ Error: {error}")
                        st.info("💡 Try adjusting the Grand Prix name format")
            else:
                st.warning("Please select or enter a Grand Prix name")
    
    with col2:
        # Step 2: Driver Selection
       # In Tab 1 - Driver Selection Section
        if st.session_state.session_loaded:
            st.markdown("""
            <div class="control-section">
                <h4 class="text-secondary">2️⃣ Select Drivers</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Get available drivers
            available_drivers = sorted(st.session_state.session.laps['Driver'].unique().tolist())
            
            st.markdown(f"""
            <div class="alert alert-info">
                <strong>Available Drivers:</strong><br>
                {', '.join(available_drivers)}
            </div>
            """, unsafe_allow_html=True)
            
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                driver1 = st.selectbox("🏎️ Driver 1", available_drivers, index=0)
            with subcol2:
                driver2 = st.selectbox("🏎️ Driver 2", available_drivers, 
                                    index=1 if len(available_drivers) > 1 else 0)
            
            # Custom progress container (initially hidden)
            progress_placeholder = st.empty()
            
            # Run analysis button
            if st.button("🔥 Run Analysis", type="primary", use_container_width=True):
                if driver1 != driver2:
                    # Show custom progress bar
                    progress_placeholder.markdown("""
                    <div class="custom-progress-container">
                        <div class="progress-header">
                            <h5 class="text-primary mb-2">🔄 Processing Telemetry Data</h5>
                            <p class="text-muted mb-3">Analyzing driver performance data...</p>
                        </div>
                        <div class="custom-progress">
                            <div class="custom-progress-bar" id="analysisProgress"></div>
                        </div>
                        <div class="progress-steps mt-3">
                            <div class="step-item active" id="step1">
                                <span class="step-icon">📥</span>
                                <span class="step-text">Loading Data</span>
                            </div>
                            <div class="step-item" id="step2">
                                <span class="step-icon">⚡</span>
                                <span class="step-text">Processing</span>
                            </div>
                            <div class="step-item" id="step3">
                                <span class="step-icon">📊</span>
                                <span class="step-text">Generating Charts</span>
                            </div>
                            <div class="step-item" id="step4">
                                <span class="step-icon">✅</span>
                                <span class="step-text">Complete</span>
                            </div>
                        </div>
                    </div>
                    <script>
                    function updateProgress(step) {
                        const progressBar = document.getElementById('analysisProgress');
                        const steps = document.querySelectorAll('.step-item');
                        const percentage = (step / 4) * 100;
                        
                        if (progressBar) {
                            progressBar.style.width = percentage + '%';
                        }
                        
                        steps.forEach((stepEl, index) => {
                            if (index < step) {
                                stepEl.classList.add('active');
                                stepEl.classList.add('completed');
                            } else if (index === step) {
                                stepEl.classList.add('active');
                            }
                        });
                    }
                    </script>
                    """, unsafe_allow_html=True)
                    
                    # Simulate progress steps
                    selected_drivers = [driver1, driver2]
                    
                    # Step 1: Loading
                    time.sleep(0.5)
                    progress_placeholder.markdown("""
                    <div class="custom-progress-container">
                        <div class="progress-header">
                            <h5 class="text-primary mb-2">🔄 Processing Telemetry Data</h5>
                            <p class="text-muted mb-3">Loading session data...</p>
                        </div>
                        <div class="custom-progress">
                            <div class="custom-progress-bar" style="width: 25%;"></div>
                        </div>
                        <div class="progress-steps mt-3">
                            <div class="step-item active completed">
                                <span class="step-icon">📥</span>
                                <span class="step-text">Loading Data</span>
                            </div>
                            <div class="step-item active">
                                <span class="step-icon">⚡</span>
                                <span class="step-text">Processing</span>
                            </div>
                            <div class="step-item">
                                <span class="step-icon">📊</span>
                                <span class="step-text">Generating Charts</span>
                            </div>
                            <div class="step-item">
                                <span class="step-icon">✅</span>
                                <span class="step-text">Complete</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Step 2: Processing
                    driver_data, all_telemetry_df = process_driver_data(
                        st.session_state.session, selected_drivers
                    )
                    
                    progress_placeholder.markdown("""
                    <div class="custom-progress-container">
                        <div class="progress-header">
                            <h5 class="text-primary mb-2">🔄 Processing Telemetry Data</h5>
                            <p class="text-muted mb-3">Generating visualizations...</p>
                        </div>
                        <div class="custom-progress">
                            <div class="custom-progress-bar" style="width: 75%;"></div>
                        </div>
                        <div class="progress-steps mt-3">
                            <div class="step-item active completed">
                                <span class="step-icon">📥</span>
                                <span class="step-text">Loading Data</span>
                            </div>
                            <div class="step-item active completed">
                                <span class="step-icon">⚡</span>
                                <span class="step-text">Processing</span>
                            </div>
                            <div class="step-item active">
                                <span class="step-icon">📊</span>
                                <span class="step-text">Generating Charts</span>
                            </div>
                            <div class="step-item">
                                <span class="step-icon">✅</span>
                                <span class="step-text">Complete</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(0.5)
                    
                    if driver_data:
                        # Step 4: Complete
                        progress_placeholder.markdown("""
                        <div class="custom-progress-container">
                            <div class="progress-header">
                                <h5 class="text-success mb-2">✅ Analysis Complete!</h5>
                                <p class="text-muted mb-3">Ready to explore telemetry data</p>
                            </div>
                            <div class="custom-progress">
                                <div class="custom-progress-bar" style="width: 100%;"></div>
                            </div>
                            <div class="progress-steps mt-3">
                                <div class="step-item active completed">
                                    <span class="step-icon">📥</span>
                                    <span class="step-text">Loading Data</span>
                                </div>
                                <div class="step-item active completed">
                                    <span class="step-icon">⚡</span>
                                    <span class="step-text">Processing</span>
                                </div>
                                <div class="step-item active completed">
                                    <span class="step-icon">📊</span>
                                    <span class="step-text">Generating Charts</span>
                                </div>
                                <div class="step-item active completed">
                                    <span class="step-icon">✅</span>
                                    <span class="step-text">Complete</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.driver_data = driver_data
                        st.session_state.all_telemetry_df = all_telemetry_df
                        st.session_state.selected_drivers = selected_drivers
                        st.session_state.analysis_complete = True
                        
                        # Clear progress after 2 seconds
                        time.sleep(2)
                        progress_placeholder.empty()
                        st.balloons()
                        
                    else:
                        progress_placeholder.markdown("""
                        <div class="custom-progress-container">
                            <div class="progress-header">
                                <h5 class="text-danger mb-2">❌ Analysis Failed</h5>
                                <p class="text-muted mb-3">No valid telemetry data found</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(2)
                        progress_placeholder.empty()
                else:
                    st.error("Please select two different drivers")

# Tab 2: Analysis
with tab2:
    if st.session_state.analysis_complete:
        # Session information
        st.markdown(f"""
        <div class="session-info">
            📊 <strong>Session:</strong> {st.session_state.year} {st.session_state.grand_prix} {st.session_state.session_display}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="driver-comparison">
            👥 <strong>Comparing:</strong> {' 🆚 '.join(st.session_state.selected_drivers)}
        </div>
        """, unsafe_allow_html=True)
        
        # Get available laps
        if st.session_state.selected_drivers[0] in st.session_state.driver_data:
            available_laps = sorted(
                st.session_state.driver_data[st.session_state.selected_drivers[0]]['LapNumber'].unique().tolist()
            )
        else:
            available_laps = []
        
        if available_laps:
            # Analysis controls
            control_col1, control_col2 = st.columns(2)
            with control_col1:
                selected_lap = st.selectbox(
                    "📍 Select Lap", 
                    available_laps, 
                    index=0,
                    help="Choose which lap to analyze"
                )
            
            with control_col2:
                max_distance = int(st.session_state.all_telemetry_df['Distance'].max())
                selected_distance = st.slider(
                    "🎯 Track Position (m)", 
                    min_value=0, 
                    max_value=max_distance, 
                    value=0, 
                    step=25,
                    help="Move the slider to explore different track positions"
                )
            
            # Main visualization layout
            viz_col1, viz_col2 = st.columns([1, 1])
            
            with viz_col1:
                st.markdown("""
                <div class="track-container">
                    <h3 class="text-center text-primary mb-3">🗺️ Track Map</h3>
                </div>
                """, unsafe_allow_html=True)
                
                fig_track = create_track_plot(
                    st.session_state.driver_data, 
                    st.session_state.selected_drivers,
                    height=600
                )
                update_track_marker(
                    fig_track, 
                    st.session_state.driver_data, 
                    st.session_state.selected_drivers, 
                    selected_distance
                )
                st.plotly_chart(fig_track, use_container_width=True, key="track_plot")
                
                            # Additional insights
                st.markdown("""
                <div class="container mt-4">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="control-panel">
                                <h4 class="text-primary mb-3">💡 Analysis Insights</h4>
                                <div class="row">
                                    <div class="col-md-4 text-center">
                                        <h5 class="text-secondary">Track Position</h5>
                                        <p class="text-light">Use the distance slider to explore different sections of the track and see how driver performance varies.</p>
                                    </div>
                                    <div class="col-md-4 text-center">
                                        <h5 class="text-secondary">Telemetry Comparison</h5>
                                        <p class="text-light">Compare speed, throttle, brake, and other metrics between drivers at any point on the track.</p>
                                    </div>
                                    <div class="col-md-4 text-center">
                                        <h5 class="text-secondary">Performance Analysis</h5>
                                        <p class="text-light">Identify braking points, acceleration zones, and overtaking opportunities.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with viz_col2:
                st.markdown("""
                <div class="telemetry-container">
                    <h3 class="text-center text-secondary mb-3">📊 Telemetry Data</h3>
                </div>
                """, unsafe_allow_html=True)
                
                fig_telemetry = create_telemetry_plots(
                    st.session_state.driver_data, 
                    st.session_state.selected_drivers, 
                    selected_lap, 
                    selected_distance
                )
                st.plotly_chart(fig_telemetry, use_container_width=True, key="telemetry_plot")
        
        else:
            st.error("❌ No lap data available for analysis")
            st.info("Try selecting different drivers or a different session in the Configuration tab")
    
    else:
        # Welcome section when no analysis is loaded
        st.markdown("""
        <div class="welcome-section">
            <h2>🏁 Welcome to F1 Telemetry Analysis</h2>
            <p class="lead">
                Dive deep into Formula 1 telemetry data with this interactive analysis platform
            </p>
        </div>
        
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="project-card">
                        <h4 class="text-primary mb-3">📊 Features</h4>
                        <ul class="feature-list">
                            <li>🗺️ Interactive track maps with position markers</li>
                            <li>📈 Real-time telemetry comparison charts</li>
                            <li>🎯 Distance-based track exploration</li>
                            <li>📱 Responsive design for all devices</li>
                            <li>⚡ Live data from FastF1 API</li>
                            <li>🔄 Cached processing for better performance</li>
                        </ul>
                        <div class="text-center mt-4">
                            <p><strong>👆 Go to the Configuration tab to get started!</strong></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tab 3: Driver Statistics (formerly sidebar stats + lap time)
with tab3:
    if st.session_state.analysis_complete:
        # Get available laps for lap selection
        if st.session_state.selected_drivers[0] in st.session_state.driver_data:
            available_laps = sorted(
                st.session_state.driver_data[st.session_state.selected_drivers[0]]['LapNumber'].unique().tolist()
            )
            
            # Lap selection for stats
            stat_col1, stat_col2 = st.columns([1, 2])
            with stat_col1:
                stats_lap = st.selectbox(
                    "📍 Select Lap for Statistics", 
                    available_laps, 
                    index=0,
                    help="Choose which lap to show statistics for",
                    key="stats_lap_selector"
                )
            
            st.markdown("""
            <div class="control-panel">
                <h3 class="text-primary text-center mb-4">🏁 Driver Performance Statistics</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Get lap summary stats
            stats = get_lap_summary_stats(
                st.session_state.driver_data, 
                st.session_state.selected_drivers, 
                stats_lap
            )
            
            if stats:
                # Display statistics for each driver
                for i, (driver, data) in enumerate(stats.items()):
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4 class="text-primary text-center mb-3">🏎️ {driver} - Lap {stats_lap}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get lap time for THIS specific driver
                    lap_time_str = "No Time"
                    
                    try:
                        driver_lap_data = st.session_state.driver_data[driver]
                        lap_time_data = driver_lap_data[driver_lap_data['LapNumber'] == stats_lap]
                        
                        # Debug: Check what columns are available
                        # st.write(f"Debug - Columns for {driver}:", list(driver_lap_data.columns))
                        
                        if not lap_time_data.empty:
                            # Try different possible column names for lap time
                            lap_time_col = None
                            possible_columns = ['LapTime', 'laptime', 'Laptime', 'Time', 'lap_time']
                            
                            for col in possible_columns:
                                if col in lap_time_data.columns:
                                    lap_time_col = col
                                    break
                            
                            if lap_time_col:
                                lap_time = lap_time_data[lap_time_col].iloc[0]
                                
                                # Check if it's null/NaN using different methods
                                if lap_time is None or str(lap_time).lower() in ['nan', 'nat', 'none']:
                                    lap_time_str = "No Time"
                                elif hasattr(lap_time, 'total_seconds'):
                                    # It's a timedelta object
                                    total_seconds = lap_time.total_seconds()
                                    minutes = int(total_seconds // 60)
                                    seconds = total_seconds % 60
                                    lap_time_str = f"{minutes}:{seconds:06.3f}"
                                elif isinstance(lap_time, (int, float)):
                                    # It's already in seconds
                                    minutes = int(lap_time // 60)
                                    seconds = lap_time % 60
                                    lap_time_str = f"{minutes}:{seconds:06.3f}"
                                else:
                                    # Try to convert to string
                                    lap_time_str = str(lap_time)
                            else:
                                lap_time_str = "Column Not Found"
                        else:
                            lap_time_str = "No Data"
                            
                    except Exception as e:
                        lap_time_str = f"Debug: {str(e)[:20]}"  # Show first 20 chars of error for debugging
                    
                    # Create metrics in columns (including lap time)
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric(
                            label="Lap Time",
                            value=lap_time_str,
                            help=f"Lap time for {driver} on lap {stats_lap}"
                        )
                    
                    with metric_col2:
                        st.metric(
                            label="Max Speed",
                            value=f"{data['max_speed']:.0f} km/h",
                            help="Maximum speed achieved during the lap"
                        )
                    
                    with metric_col3:
                        st.metric(
                            label="Avg Speed", 
                            value=f"{data['avg_speed']:.0f} km/h",
                            help="Average speed throughout the lap"
                        )
                    
                    with metric_col4:
                        st.metric(
                            label="Max RPM", 
                            value=f"{data['max_rpm']:.0f}",
                            help="Maximum engine RPM during the lap"
                        )
                    
                    # Second row of metrics
                    metric2_col1, metric2_col2, metric2_col3, metric2_col4 = st.columns(4)
                    
                    with metric2_col1:
                        st.metric(
                            label="DRS Usage", 
                            value=f"{data['drs_usage']:.1f}%",
                            help="Percentage of lap where DRS was active"
                        )
                    
                    # Add spacing between drivers
                    if i < len(stats) - 1:
                        st.markdown("---")
            
            else:
                st.warning("No statistics available for the selected lap")
                st.info("Try selecting a different lap or ensure the analysis has been completed")
        
        else:
            st.warning("No driver data available for statistics")
            st.info("Please run an analysis first in the Configuration tab")
    
    else:
        st.markdown("""
        <div class="welcome-section">
            <h2>📊 Driver Statistics</h2>
            <p class="lead">
                View detailed performance metrics and statistics for each driver
            </p>
            <div class="text-center mt-4">
                <p><strong>👈 Complete your analysis setup in the Configuration tab to see driver statistics here!</strong></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
