"""
F1 Telemetry Analysis Page
Main F1 data analysis application with interactive telemetry comparison
"""
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

# Sidebar Configuration
with st.sidebar:
    st.markdown("""
    <div class="control-panel">
        <h3 class="text-primary text-center mb-4">⚙️ Analysis Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Load Events", type="secondary", use_container_width=True):
            with st.spinner("Loading available events..."):
                events = get_available_events(year)
                st.session_state.available_events = events
                st.success(f"✅ Loaded {len(events)} events")
    
    with col2:
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
    
    # Step 2: Driver Selection
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
        
        col1, col2 = st.columns(2)
        with col1:
            driver1 = st.selectbox("🏎️ Driver 1", available_drivers, index=0)
        with col2:
            driver2 = st.selectbox("🏎️ Driver 2", available_drivers, 
                                 index=1 if len(available_drivers) > 1 else 0)
        
        # Run analysis button
        if st.button("🔥 Run Analysis", type="primary", use_container_width=True):
            if driver1 != driver2:
                with st.spinner("Processing telemetry data..."):
                    selected_drivers = [driver1, driver2]
                    driver_data, all_telemetry_df = process_driver_data(
                        st.session_state.session, selected_drivers
                    )
                    
                    if driver_data:
                        st.session_state.driver_data = driver_data
                        st.session_state.all_telemetry_df = all_telemetry_df
                        st.session_state.selected_drivers = selected_drivers
                        st.session_state.analysis_complete = True
                        st.success("✅ Analysis complete!")
                        st.balloons()
                    else:
                        st.error("❌ No valid telemetry data found")
            else:
                st.error("Please select two different drivers")

# Main Content Area
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
        # Analysis controls in sidebar
        with st.sidebar:
            st.markdown("""
            <div class="control-section">
                <h4 class="text-secondary">3️⃣ Analysis Controls</h4>
            </div>
            """, unsafe_allow_html=True)
            
            selected_lap = st.selectbox(
                "📍 Select Lap", 
                available_laps, 
                index=0,
                help="Choose which lap to analyze"
            )
            
            max_distance = int(st.session_state.all_telemetry_df['Distance'].max())
            selected_distance = st.slider(
                "🎯 Track Position (m)", 
                min_value=0, 
                max_value=max_distance, 
                value=0, 
                step=25,
                help="Move the slider to explore different track positions"
            )
            
            # Lap summary stats
            stats = get_lap_summary_stats(
                st.session_state.driver_data, 
                st.session_state.selected_drivers, 
                selected_lap
            )
            
            if stats:
                st.markdown("### 📈 Lap Statistics")
                for driver, data in stats.items():
                    st.markdown(f"**{driver}:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Max Speed", f"{data['max_speed']:.0f} km/h")
                        st.metric("Avg Speed", f"{data['avg_speed']:.0f} km/h")
                    with col2:
                        st.metric("Max RPM", f"{data['max_rpm']:.0f}")
                        st.metric("DRS Usage", f"{data['drs_usage']:.1f}%")
        
        # Main visualization layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
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
        
        with col2:
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
    
    else:
        st.error("❌ No lap data available for analysis")
        st.info("Try selecting different drivers or a different session")

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
            <div class="col-md-6">
                <div class="project-card">
                    <h4 class="text-primary mb-3">🚀 Getting Started</h4>
                    <ol class="feature-list">
                        <li>Select a championship year (2020-2025)</li>
                        <li>Load available events from FastF1 API</li>
                        <li>Choose a Grand Prix and session type</li>
                        <li>Load the session data</li>
                        <li>Select two drivers to compare</li>
                        <li>Run the analysis and explore!</li>
                    </ol>
                </div>
            </div>
            <div class="col-md-6">
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
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
