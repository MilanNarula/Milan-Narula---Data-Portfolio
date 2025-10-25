# """
# F1 Telemetry Analysis Page
# Main F1 data analysis application with interactive telemetry comparison
# """
# import time
# import streamlit as st
# from utils.styling import load_all_styles, inject_page_config, create_navbar
# from utils.f1_functions import (
#     setup_f1_cache, load_session_data, get_available_events, 
#     process_driver_data, create_track_plot, create_telemetry_plots,
#     update_track_marker, get_lap_summary_stats
# )

# # Configure page
# inject_page_config()
# load_all_styles()
# st.markdown("""
#         <style>
#         [data-testid="stHeaderActionElements"] {
#             display: none;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# # Setup F1 cache
# setup_f1_cache()

# # Create navigation
# create_navbar("F1")

# # Initialize session state
# if 'session_loaded' not in st.session_state:
#     st.session_state.session_loaded = False
# if 'analysis_complete' not in st.session_state:
#     st.session_state.analysis_complete = False
# if 'available_events' not in st.session_state:
#     st.session_state.available_events = []

# st.title("🏎️ F1 Telemetry Analysis Dashboard")

# # Create tabs[1][4]
# tab1, tab2, tab3 = st.tabs(["⚙️ Configuration", "📊 Analysis", "🏁 Driver Stats"])

# # Tab 1: Configuration (formerly sidebar content)
# with tab1:
#     st.markdown("""
#     <div class="control-panel">
#         <h3 class="text-primary text-center mb-4">🔧 Analysis Configuration</h3>
#     </div>
#     """, unsafe_allow_html=True)
    
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         # Step 1: Session Selection
#         st.markdown("""
#         <div class="control-section">
#             <h4 class="text-secondary">1️⃣ Select F1 Session</h4>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Year selection
#         current_year = 2025
#         year = st.selectbox(
#             "Championship Year", 
#             list(range(2020, current_year + 1))[::-1], 
#             index=0,
#             help="Select the F1 championship year to analyze"
#         )
        
#         # Load available events
#         subcol1, subcol2 = st.columns(2)
#         with subcol1:
#             if st.button("🔄 Load Events", type="secondary", use_container_width=True):
#                 with st.spinner("Loading available events..."):
#                     events = get_available_events(year)
#                     st.session_state.available_events = events
#                     st.success(f"✅ Loaded {len(events)} events")
        
#         with subcol2:
#             if st.button("🗑️ Clear Cache", use_container_width=True):
#                 st.cache_data.clear()
#                 st.success("Cache cleared!")
        
#         # Event selection
#         if st.session_state.available_events:
#             grand_prix = st.selectbox(
#                 "Grand Prix", 
#                 st.session_state.available_events,
#                 help="Select the Grand Prix event to analyze"
#             )
#         else:
#             st.info("👆 Click 'Load Events' to see available races")
#             grand_prix = st.text_input(
#                 "Or enter Grand Prix name manually:", 
#                 placeholder="e.g., Hungarian Grand Prix"
#             )
        
#         # Session type selection
#         session_type_options = {
#             '🏃‍♂️ Practice 1': 'FP1',
#             '🏃‍♂️ Practice 2': 'FP2', 
#             '🏃‍♂️ Practice 3': 'FP3',
#             '⚡ Sprint Qualifying': 'SQ',
#             '🏁 Sprint': 'S',
#             '🎯 Qualifying': 'Q',
#             '🏆 Race': 'R'
#         }
        
#         session_display = st.selectbox(
#             "Session Type", 
#             list(session_type_options.keys()), 
#             index=6,
#             help="Select the session type to analyze"
#         )
#         session_type = session_type_options[session_display]
        
#         # Load session button
#         if st.button("🚀 Load Session", type="primary", use_container_width=True):
#             if grand_prix:
#                 with st.spinner("Loading session data from FastF1 API..."):
#                     session, error = load_session_data(year, grand_prix, session_type)
#                     if session:
#                         st.session_state.session = session
#                         st.session_state.session_loaded = True
#                         st.session_state.year = year
#                         st.session_state.grand_prix = grand_prix
#                         st.session_state.session_display = session_display
#                         st.success("✅ Session loaded successfully!")
#                     else:
#                         st.error(f"❌ Error: {error}")
#                         st.info("💡 Try adjusting the Grand Prix name format")
#             else:
#                 st.warning("Please select or enter a Grand Prix name")
    
#     with col2:
#         # Step 2: Driver Selection
#        # In Tab 1 - Driver Selection Section
#         if st.session_state.session_loaded:
#             st.markdown("""
#             <div class="control-section">
#                 <h4 class="text-secondary">2️⃣ Select Drivers</h4>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Get available drivers
#             available_drivers = sorted(st.session_state.session.laps['Driver'].unique().tolist())
            
#             st.markdown(f"""
#             <div class="alert alert-info">
#                 <strong>Available Drivers:</strong><br>
#                 {', '.join(available_drivers)}
#             </div>
#             """, unsafe_allow_html=True)
            
#             subcol1, subcol2 = st.columns(2)
#             with subcol1:
#                 driver1 = st.selectbox("🏎️ Driver 1", available_drivers, index=0)
#             with subcol2:
#                 driver2 = st.selectbox("🏎️ Driver 2", available_drivers, 
#                                     index=1 if len(available_drivers) > 1 else 0)
            
#             # Custom progress container (initially hidden)
#             progress_placeholder = st.empty()
            
#             # Run analysis button
#             if st.button("🔥 Run Analysis", type="primary", use_container_width=True):
#                 if driver1 != driver2:
#                     # Show custom progress bar
#                     progress_placeholder.markdown("""
#                     <div class="custom-progress-container">
#                         <div class="progress-header">
#                             <h5 class="text-primary mb-2">🔄 Processing Telemetry Data</h5>
#                             <p class="text-muted mb-3">Analyzing driver performance data...</p>
#                         </div>
#                         <div class="custom-progress">
#                             <div class="custom-progress-bar" id="analysisProgress"></div>
#                         </div>
#                         <div class="progress-steps mt-3">
#                             <div class="step-item active" id="step1">
#                                 <span class="step-icon">📥</span>
#                                 <span class="step-text">Loading Data</span>
#                             </div>
#                             <div class="step-item" id="step2">
#                                 <span class="step-icon">⚡</span>
#                                 <span class="step-text">Processing</span>
#                             </div>
#                             <div class="step-item" id="step3">
#                                 <span class="step-icon">📊</span>
#                                 <span class="step-text">Generating Charts</span>
#                             </div>
#                             <div class="step-item" id="step4">
#                                 <span class="step-icon">✅</span>
#                                 <span class="step-text">Complete</span>
#                             </div>
#                         </div>
#                     </div>
#                     <script>
#                     function updateProgress(step) {
#                         const progressBar = document.getElementById('analysisProgress');
#                         const steps = document.querySelectorAll('.step-item');
#                         const percentage = (step / 4) * 100;
                        
#                         if (progressBar) {
#                             progressBar.style.width = percentage + '%';
#                         }
                        
#                         steps.forEach((stepEl, index) => {
#                             if (index < step) {
#                                 stepEl.classList.add('active');
#                                 stepEl.classList.add('completed');
#                             } else if (index === step) {
#                                 stepEl.classList.add('active');
#                             }
#                         });
#                     }
#                     </script>
#                     """, unsafe_allow_html=True)
                    
#                     # Simulate progress steps
#                     selected_drivers = [driver1, driver2]
                    
#                     # Step 1: Loading
#                     time.sleep(0.5)
#                     progress_placeholder.markdown("""
#                     <div class="custom-progress-container">
#                         <div class="progress-header">
#                             <h5 class="text-primary mb-2">🔄 Processing Telemetry Data</h5>
#                             <p class="text-muted mb-3">Loading session data...</p>
#                         </div>
#                         <div class="custom-progress">
#                             <div class="custom-progress-bar" style="width: 25%;"></div>
#                         </div>
#                         <div class="progress-steps mt-3">
#                             <div class="step-item active completed">
#                                 <span class="step-icon">📥</span>
#                                 <span class="step-text">Loading Data</span>
#                             </div>
#                             <div class="step-item active">
#                                 <span class="step-icon">⚡</span>
#                                 <span class="step-text">Processing</span>
#                             </div>
#                             <div class="step-item">
#                                 <span class="step-icon">📊</span>
#                                 <span class="step-text">Generating Charts</span>
#                             </div>
#                             <div class="step-item">
#                                 <span class="step-icon">✅</span>
#                                 <span class="step-text">Complete</span>
#                             </div>
#                         </div>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     # Step 2: Processing
#                     driver_data, all_telemetry_df = process_driver_data(
#                         st.session_state.session, selected_drivers
#                     )
                    
#                     progress_placeholder.markdown("""
#                     <div class="custom-progress-container">
#                         <div class="progress-header">
#                             <h5 class="text-primary mb-2">🔄 Processing Telemetry Data</h5>
#                             <p class="text-muted mb-3">Generating visualizations...</p>
#                         </div>
#                         <div class="custom-progress">
#                             <div class="custom-progress-bar" style="width: 75%;"></div>
#                         </div>
#                         <div class="progress-steps mt-3">
#                             <div class="step-item active completed">
#                                 <span class="step-icon">📥</span>
#                                 <span class="step-text">Loading Data</span>
#                             </div>
#                             <div class="step-item active completed">
#                                 <span class="step-icon">⚡</span>
#                                 <span class="step-text">Processing</span>
#                             </div>
#                             <div class="step-item active">
#                                 <span class="step-icon">📊</span>
#                                 <span class="step-text">Generating Charts</span>
#                             </div>
#                             <div class="step-item">
#                                 <span class="step-icon">✅</span>
#                                 <span class="step-text">Complete</span>
#                             </div>
#                         </div>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     time.sleep(0.5)
                    
#                     if driver_data:
#                         # Step 4: Complete
#                         progress_placeholder.markdown("""
#                         <div class="custom-progress-container">
#                             <div class="progress-header">
#                                 <h5 class="text-success mb-2">✅ Analysis Complete!</h5>
#                                 <p class="text-muted mb-3">Ready to explore telemetry data</p>
#                             </div>
#                             <div class="custom-progress">
#                                 <div class="custom-progress-bar" style="width: 100%;"></div>
#                             </div>
#                             <div class="progress-steps mt-3">
#                                 <div class="step-item active completed">
#                                     <span class="step-icon">📥</span>
#                                     <span class="step-text">Loading Data</span>
#                                 </div>
#                                 <div class="step-item active completed">
#                                     <span class="step-icon">⚡</span>
#                                     <span class="step-text">Processing</span>
#                                 </div>
#                                 <div class="step-item active completed">
#                                     <span class="step-icon">📊</span>
#                                     <span class="step-text">Generating Charts</span>
#                                 </div>
#                                 <div class="step-item active completed">
#                                     <span class="step-icon">✅</span>
#                                     <span class="step-text">Complete</span>
#                                 </div>
#                             </div>
#                         </div>
#                         """, unsafe_allow_html=True)
                        
#                         st.session_state.driver_data = driver_data
#                         st.session_state.all_telemetry_df = all_telemetry_df
#                         st.session_state.selected_drivers = selected_drivers
#                         st.session_state.analysis_complete = True
                        
#                         # Clear progress after 2 seconds
#                         time.sleep(2)
#                         progress_placeholder.empty()
#                         st.balloons()
                        
#                     else:
#                         progress_placeholder.markdown("""
#                         <div class="custom-progress-container">
#                             <div class="progress-header">
#                                 <h5 class="text-danger mb-2">❌ Analysis Failed</h5>
#                                 <p class="text-muted mb-3">No valid telemetry data found</p>
#                             </div>
#                         </div>
#                         """, unsafe_allow_html=True)
#                         time.sleep(2)
#                         progress_placeholder.empty()
#                 else:
#                     st.error("Please select two different drivers")

# # Tab 2: Analysis
# with tab2:
#     if st.session_state.analysis_complete:
#         # Session information
#         st.markdown(f"""
#         <div class="session-info">
#             📊 <strong>Session:</strong> {st.session_state.year} {st.session_state.grand_prix} {st.session_state.session_display}
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div class="driver-comparison">
#             👥 <strong>Comparing:</strong> {' 🆚 '.join(st.session_state.selected_drivers)}
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Get available laps
#         if st.session_state.selected_drivers[0] in st.session_state.driver_data:
#             available_laps = sorted(
#                 st.session_state.driver_data[st.session_state.selected_drivers[0]]['LapNumber'].unique().tolist()
#             )
#         else:
#             available_laps = []
        
#         if available_laps:
#             # Analysis controls
#             control_col1, control_col2 = st.columns(2)
#             with control_col1:
#                 selected_lap = st.selectbox(
#                     "📍 Select Lap", 
#                     available_laps, 
#                     index=0,
#                     help="Choose which lap to analyze"
#                 )
            
#             with control_col2:
#                 max_distance = int(st.session_state.all_telemetry_df['Distance'].max())
#                 selected_distance = st.slider(
#                     "🎯 Track Position (m)", 
#                     min_value=0, 
#                     max_value=max_distance, 
#                     value=0, 
#                     step=25,
#                     help="Move the slider to explore different track positions"
#                 )
            
#             # Main visualization layout
#             viz_col1, viz_col2 = st.columns([1, 1])
            
#             with viz_col1:
#                 st.markdown("""
#                 <div class="track-container">
#                     <h3 class="text-center text-primary mb-3">🗺️ Track Map</h3>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 fig_track = create_track_plot(
#                     st.session_state.driver_data, 
#                     st.session_state.selected_drivers,
#                     height=600
#                 )
#                 update_track_marker(
#                     fig_track, 
#                     st.session_state.driver_data, 
#                     st.session_state.selected_drivers, 
#                     selected_distance
#                 )
#                 st.plotly_chart(fig_track, use_container_width=True, key="track_plot")
                
#                 # Additional insights
#                 st.markdown("""
#                 <div class="container mt-4">
#                     <div class="row">
#                         <div class="col-md-12">
#                             <div class="control-panel">
#                                 <h4 class="text-primary mb-3">💡 Analysis Insights</h4>
#                                 <div class="row">
#                                     <div class="col-md-4 text-center">
#                                         <h5 class="text-secondary">Track Position</h5>
#                                         <p class="text-light">Use the distance slider to explore different sections of the track and see how driver performance varies.</p>
#                                     </div>
#                                     <div class="col-md-4 text-center">
#                                         <h5 class="text-secondary">Telemetry Comparison</h5>
#                                         <p class="text-light">Compare speed, throttle, brake, and other metrics between drivers at any point on the track.</p>
#                                     </div>
#                                     <div class="col-md-4 text-center">
#                                         <h5 class="text-secondary">Performance Analysis</h5>
#                                         <p class="text-light">Identify braking points, acceleration zones, and overtaking opportunities.</p>
#                                     </div>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             with viz_col2:
#                 st.markdown("""
#                 <div class="telemetry-container">
#                     <h3 class="text-center text-secondary mb-3">📊 Telemetry Data</h3>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 fig_telemetry = create_telemetry_plots(
#                     st.session_state.driver_data, 
#                     st.session_state.selected_drivers, 
#                     selected_lap, 
#                     selected_distance
#                 )
#                 st.plotly_chart(fig_telemetry, use_container_width=True, key="telemetry_plot")
        
#         else:
#             st.error("❌ No lap data available for analysis")
#             st.info("Try selecting different drivers or a different session in the Configuration tab")
    
#     else:
#         # Welcome section when no analysis is loaded
#         st.markdown("""
#         <div class="welcome-section">
#             <h2>🏁 Welcome to F1 Telemetry Analysis</h2>
#             <p class="lead">
#                 Dive deep into Formula 1 telemetry data with this interactive analysis platform
#             </p>
#         </div>
        
#         <div class="container">
#             <div class="row">
#                 <div class="col-md-12">
#                     <div class="project-card">
#                         <h4 class="text-primary mb-3">📊 Features</h4>
#                         <ul class="feature-list">
#                             <li>🗺️ Interactive track maps with position markers</li>
#                             <li>📈 Real-time telemetry comparison charts</li>
#                             <li>🎯 Distance-based track exploration</li>
#                             <li>📱 Responsive design for all devices</li>
#                             <li>⚡ Live data from FastF1 API</li>
#                             <li>🔄 Cached processing for better performance</li>
#                         </ul>
#                         <div class="text-center mt-4">
#                             <p><strong>👆 Go to the Configuration tab to get started!</strong></p>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

# # Tab 3: Driver Statistics (formerly sidebar stats + lap time)
# with tab3:
#     if st.session_state.analysis_complete:
#         # Get available laps for lap selection
#         if st.session_state.selected_drivers[0] in st.session_state.driver_data:
#             available_laps = sorted(
#                 st.session_state.driver_data[st.session_state.selected_drivers[0]]['LapNumber'].unique().tolist()
#             )
            
#             # Lap selection for stats
#             stat_col1, stat_col2 = st.columns([1, 2])
#             with stat_col1:
#                 stats_lap = st.selectbox(
#                     "📍 Select Lap for Statistics", 
#                     available_laps, 
#                     index=0,
#                     help="Choose which lap to show statistics for",
#                     key="stats_lap_selector"
#                 )
            
#             st.markdown("""
#             <div class="control-panel">
#                 <h3 class="text-primary text-center mb-4">🏁 Driver Performance Statistics</h3>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Get lap summary stats
#             stats = get_lap_summary_stats(
#                 st.session_state.driver_data, 
#                 st.session_state.selected_drivers, 
#                 stats_lap
#             )
            
#             if stats:
#                 # Display statistics for each driver
#                 for i, (driver, data) in enumerate(stats.items()):
#                     st.markdown(f"""
#                     <div class="metric-card">
#                         <h4 class="text-primary text-center mb-3">🏎️ {driver} - Lap {stats_lap}</h4>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     # Get lap time for THIS specific driver
#                     lap_time_str = "No Time"
                    
#                     try:
#                         driver_lap_data = st.session_state.driver_data[driver]
#                         lap_time_data = driver_lap_data[driver_lap_data['LapNumber'] == stats_lap]
                        
#                         # Debug: Check what columns are available
#                         # st.write(f"Debug - Columns for {driver}:", list(driver_lap_data.columns))
                        
#                         if not lap_time_data.empty:
#                             # Try different possible column names for lap time
#                             lap_time_col = None
#                             possible_columns = ['LapTime', 'laptime', 'Laptime', 'Time', 'lap_time']
                            
#                             for col in possible_columns:
#                                 if col in lap_time_data.columns:
#                                     lap_time_col = col
#                                     break
                            
#                             if lap_time_col:
#                                 lap_time = lap_time_data[lap_time_col].iloc[0]
                                
#                                 # Check if it's null/NaN using different methods
#                                 if lap_time is None or str(lap_time).lower() in ['nan', 'nat', 'none']:
#                                     lap_time_str = "No Time"
#                                 elif hasattr(lap_time, 'total_seconds'):
#                                     # It's a timedelta object
#                                     total_seconds = lap_time.total_seconds()
#                                     minutes = int(total_seconds // 60)
#                                     seconds = total_seconds % 60
#                                     lap_time_str = f"{minutes}:{seconds:06.3f}"
#                                 elif isinstance(lap_time, (int, float)):
#                                     # It's already in seconds
#                                     minutes = int(lap_time // 60)
#                                     seconds = lap_time % 60
#                                     lap_time_str = f"{minutes}:{seconds:06.3f}"
#                                 else:
#                                     # Try to convert to string
#                                     lap_time_str = str(lap_time)
#                             else:
#                                 lap_time_str = "Column Not Found"
#                         else:
#                             lap_time_str = "No Data"
                            
#                     except Exception as e:
#                         lap_time_str = f"Debug: {str(e)[:20]}"  # Show first 20 chars of error for debugging
                    
#                     # Create metrics in columns (including lap time)
#                     metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
#                     with metric_col1:
#                         st.metric(
#                             label="Lap Time",
#                             value=lap_time_str,
#                             help=f"Lap time for {driver} on lap {stats_lap}"
#                         )
                    
#                     with metric_col2:
#                         st.metric(
#                             label="Max Speed",
#                             value=f"{data['max_speed']:.0f} km/h",
#                             help="Maximum speed achieved during the lap"
#                         )
                    
#                     with metric_col3:
#                         st.metric(
#                             label="Avg Speed", 
#                             value=f"{data['avg_speed']:.0f} km/h",
#                             help="Average speed throughout the lap"
#                         )
                    
#                     with metric_col4:
#                         st.metric(
#                             label="Max RPM", 
#                             value=f"{data['max_rpm']:.0f}",
#                             help="Maximum engine RPM during the lap"
#                         )
                    
#                     # Second row of metrics
#                     metric2_col1, metric2_col2, metric2_col3, metric2_col4 = st.columns(4)
                    
#                     with metric2_col1:
#                         st.metric(
#                             label="DRS Usage", 
#                             value=f"{data['drs_usage']:.1f}%",
#                             help="Percentage of lap where DRS was active"
#                         )
                    
#                     # Add spacing between drivers
#                     if i < len(stats) - 1:
#                         st.markdown("---")
            
#             else:
#                 st.warning("No statistics available for the selected lap")
#                 st.info("Try selecting a different lap or ensure the analysis has been completed")
        
#         else:
#             st.warning("No driver data available for statistics")
#             st.info("Please run an analysis first in the Configuration tab")
    
#     else:
#         st.markdown("""
#         <div class="welcome-section">
#             <h2>📊 Driver Statistics</h2>
#             <p class="lead">
#                 View detailed performance metrics and statistics for each driver
#             </p>
#             <div class="text-center mt-4">
#                 <p><strong>👈 Complete your analysis setup in the Configuration tab to see driver statistics here!</strong></p>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

"""
F1 Telemetry Analysis Page - GP Tempo Inspired with Multi-Driver Comparison
Enhanced F1 data analysis application with proper multi-driver telemetry comparison
"""
import time
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
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
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .session-header {
            background: linear-gradient(135deg, #FF1E00, #DC143C);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        }
        .driver-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        .comparison-summary {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid rgba(0, 255, 0, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .lap-selector {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .tire-compound-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: bold;
            margin-left: 0.5rem;
        }
        .tire-soft { background-color: #FF3333; color: white; }
        .tire-medium { background-color: #FFFF00; color: black; }
        .tire-hard { background-color: #FFFFFF; color: black; }
        .tire-intermediate { background-color: #00FF00; color: black; }
        .tire-wet { background-color: #0066CC; color: white; }
        .quick-select {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .position-slider {
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

# Setup F1 cache
setup_f1_cache()

# Create navigation
create_navbar("F1")

# Enhanced session state initialization for multi-driver comparison
if 'session_loaded' not in st.session_state:
    st.session_state.session_loaded = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'available_events' not in st.session_state:
    st.session_state.available_events = []
if 'selected_comparisons' not in st.session_state:
    st.session_state.selected_comparisons = {}  # Dict of {driver: lap_number}
if 'track_position' not in st.session_state:
    st.session_state.track_position = 0

st.title("🏎️ F1 Telemetry Analysis - GP Tempo Style")

# Enhanced helper functions
@st.cache_data
def get_session_overview(_session):
    """Get comprehensive session overview with lap times and tire data"""
    try:
        laps = _session.laps
        drivers = sorted(laps['Driver'].unique().tolist())
        
        overview = {}
        for driver in drivers:
            driver_laps = laps[laps['Driver'] == driver].copy()
            
            lap_data = []
            for _, lap in driver_laps.iterrows():
                lap_time = lap.get('LapTime')
                
                if pd.isna(lap_time) or lap_time is None:
                    continue
                
                lap_info = {
                    'lap_number': int(lap['LapNumber']),
                    'lap_time': lap_time,
                    'compound': lap.get('Compound', 'MEDIUM'),
                    'tire_life': lap.get('TyreLife', 0),
                    'position': lap.get('Position', 0),
                    'is_personal_best': False,
                    'sector_1': lap.get('Sector1Time'),
                    'sector_2': lap.get('Sector2Time'), 
                    'sector_3': lap.get('Sector3Time'),
                    'deleted': lap.get('Deleted', False)
                }
                lap_data.append(lap_info)
            
            # Find personal best lap
            valid_laps = [l for l in lap_data if not l['deleted']]
            if valid_laps:
                try:
                    best_lap = min(valid_laps, key=lambda x: x['lap_time'])
                    best_lap['is_personal_best'] = True
                except (ValueError, TypeError):
                    if valid_laps:
                        valid_laps[0]['is_personal_best'] = True
            
            overview[driver] = {
                'laps': lap_data,
                'total_laps': len(lap_data),
                'best_lap_time': best_lap['lap_time'] if valid_laps else None,
                'best_lap_number': best_lap['lap_number'] if valid_laps else None
            }
        
        return overview
    except Exception as e:
        st.error(f"Error creating session overview: {e}")
        return {}

def format_lap_time(lap_time):
    """Format lap time for display"""
    if lap_time is None or pd.isna(lap_time):
        return "No Time"
    
    try:
        if hasattr(lap_time, 'total_seconds'):
            total_seconds = lap_time.total_seconds()
        elif isinstance(lap_time, (int, float)):
            total_seconds = float(lap_time)
        else:
            total_seconds = float(lap_time)
        
        if np.isnan(total_seconds) or total_seconds <= 0:
            return "No Time"
            
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:06.3f}"
    except (ValueError, TypeError, AttributeError):
        return "Invalid"

def safe_lap_time_to_seconds(lap_time):
    """Safely convert lap time to seconds"""
    if lap_time is None or pd.isna(lap_time):
        return None
    
    try:
        if hasattr(lap_time, 'total_seconds'):
            seconds = lap_time.total_seconds()
        elif isinstance(lap_time, (int, float)):
            seconds = float(lap_time)
        else:
            seconds = float(lap_time)
        
        if np.isnan(seconds) or seconds <= 0:
            return None
        
        return seconds
    except (ValueError, TypeError, AttributeError):
        return None

def get_tire_compound_class(compound):
    """Get CSS class for tire compound"""
    if compound is None:
        compound = 'MEDIUM'
    
    compound_map = {
        'SOFT': 'tire-soft',
        'MEDIUM': 'tire-medium', 
        'HARD': 'tire-hard',
        'INTERMEDIATE': 'tire-intermediate',
        'WET': 'tire-wet'
    }
    return compound_map.get(str(compound).upper(), 'tire-medium')

def get_tire_compound_color(compound):
    """Get color for tire compound"""
    if compound is None:
        compound = 'MEDIUM'
    
    color_map = {
        'SOFT': '#FF3333',
        'MEDIUM': '#FFFF00', 
        'HARD': '#FFFFFF',
        'INTERMEDIATE': '#00FF00',
        'WET': '#0066CC'
    }
    return color_map.get(str(compound).upper(), '#FFFF00')

def create_lap_times_chart(overview_data, selected_drivers):
    """Create interactive lap times chart"""
    fig = go.Figure()
    
    colors = ['#FF1E00', '#0066CC', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF']
    
    for i, driver in enumerate(selected_drivers):
        if driver in overview_data:
            driver_data = overview_data[driver]
            laps = driver_data['laps']
            
            lap_numbers = []
            lap_times = []
            compounds = []
            formatted_times = []
            
            for lap in laps:
                if not lap['deleted']:
                    time_seconds = safe_lap_time_to_seconds(lap['lap_time'])
                    
                    if time_seconds is not None:
                        lap_numbers.append(lap['lap_number'])
                        lap_times.append(time_seconds)
                        compounds.append(lap['compound'])
                        formatted_times.append(format_lap_time(lap['lap_time']))
            
            if lap_numbers:
                fig.add_trace(go.Scatter(
                    x=lap_numbers,
                    y=lap_times,
                    mode='lines+markers',
                    name=driver,
                    line=dict(color=colors[i % len(colors)], width=2),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{driver}</b><br>' +
                                'Lap: %{x}<br>' +
                                'Time: %{text}<br>' +
                                'Compound: %{customdata}<extra></extra>',
                    text=formatted_times,
                    customdata=compounds
                ))
    
    fig.update_layout(
        title='Lap Times Comparison',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (seconds)',
        hovermode='x unified',
        height=500,
        template='plotly_dark'
    )
    
    return fig

def create_multi_driver_telemetry_comparison(session, selected_comparisons):
    """Create telemetry comparison for multiple drivers and their selected laps"""
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=['Speed (km/h)', 'Throttle (%)', 'Brake', 'RPM'],
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    colors = ['#FF1E00', '#0066CC', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF']
    color_idx = 0
    
    for driver, lap_number in selected_comparisons.items():
        try:
            # Get lap data
            lap_filter = ((session.laps['Driver'] == driver) & 
                         (session.laps['LapNumber'] == lap_number))
            matching_laps = session.laps[lap_filter]
            
            if matching_laps.empty:
                continue
            
            lap = matching_laps.iloc[0]
            telemetry = lap.get_telemetry()
            
            if telemetry.empty:
                continue
            
            color = colors[color_idx % len(colors)]
            driver_label = f"{driver} (L{lap_number})"
            
            # Speed
            fig.add_trace(go.Scatter(
                x=telemetry['Distance'], 
                y=telemetry['Speed'],
                name=f'{driver_label} Speed',
                line=dict(color=color, width=2),
                hovertemplate=f'<b>{driver_label}</b><br>' +
                            'Distance: %{x:.0f}m<br>Speed: %{y:.1f} km/h<extra></extra>'
            ), row=1, col=1)
            
            # Throttle
            fig.add_trace(go.Scatter(
                x=telemetry['Distance'], 
                y=telemetry['Throttle'],
                name=f'{driver_label} Throttle',
                line=dict(color=color, width=2, dash='dot'),
                hovertemplate=f'<b>{driver_label}</b><br>' +
                            'Distance: %{x:.0f}m<br>Throttle: %{y:.1f}%<extra></extra>'
            ), row=2, col=1)
            
            # Brake
            fig.add_trace(go.Scatter(
                x=telemetry['Distance'], 
                y=telemetry['Brake'],
                name=f'{driver_label} Brake',
                line=dict(color=color, width=2, dash='dash'),
                hovertemplate=f'<b>{driver_label}</b><br>' +
                            'Distance: %{x:.0f}m<br>Brake: %{y}<extra></extra>'
            ), row=3, col=1)
            
            # RPM
            fig.add_trace(go.Scatter(
                x=telemetry['Distance'], 
                y=telemetry['RPM'],
                name=f'{driver_label} RPM',
                line=dict(color=color, width=2, dash='dashdot'),
                hovertemplate=f'<b>{driver_label}</b><br>' +
                            'Distance: %{x:.0f}m<br>RPM: %{y:.0f}<extra></extra>'
            ), row=4, col=1)
            
            color_idx += 1
            
        except Exception as e:
            st.warning(f"Could not load telemetry for {driver} lap {lap_number}: {str(e)}")
            continue
    
    fig.update_layout(
        height=800,
        title='Multi-Driver Telemetry Comparison',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(title_text="Distance (m)", row=4, col=1)
    
    return fig

def get_session_overview_no_cache(session):
    """Non-cached version of session overview"""
    try:
        laps = session.laps
        drivers = sorted(laps['Driver'].unique().tolist())
        
        overview = {}
        for driver in drivers:
            driver_laps = laps[laps['Driver'] == driver].copy()
            
            lap_data = []
            for _, lap in driver_laps.iterrows():
                lap_time = lap.get('LapTime')
                
                if pd.isna(lap_time) or lap_time is None:
                    continue
                
                lap_info = {
                    'lap_number': int(lap['LapNumber']),
                    'lap_time': lap_time,
                    'compound': lap.get('Compound', 'MEDIUM'),
                    'tire_life': lap.get('TyreLife', 0),
                    'position': lap.get('Position', 0),
                    'is_personal_best': False,
                    'sector_1': lap.get('Sector1Time'),
                    'sector_2': lap.get('Sector2Time'), 
                    'sector_3': lap.get('Sector3Time'),
                    'deleted': lap.get('Deleted', False)
                }
                lap_data.append(lap_info)
            
            valid_laps = [l for l in lap_data if not l['deleted']]
            if valid_laps:
                try:
                    best_lap = min(valid_laps, key=lambda x: x['lap_time'])
                    best_lap['is_personal_best'] = True
                except (ValueError, TypeError):
                    if valid_laps:
                        valid_laps[0]['is_personal_best'] = True
            
            overview[driver] = {
                'laps': lap_data,
                'total_laps': len(lap_data),
                'best_lap_time': best_lap['lap_time'] if valid_laps else None,
                'best_lap_number': best_lap['lap_number'] if valid_laps else None
            }
        
        return overview
    except Exception as e:
        st.error(f"Error creating session overview: {e}")
        return {}

# Create enhanced tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Quick Session", "📊 Multi-Driver Telemetry", "🔧 Advanced Setup", "📈 Driver Stats"])

# Tab 1: Enhanced Quick Session with Multi-Driver Selection
with tab1:
    st.markdown("""
    <div class="session-header">
        <h2>🚀 Quick Session Analysis</h2>
        <p>Select multiple drivers and their laps for comprehensive comparison</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick session selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        year = st.selectbox("Year", list(range(2020, 2026))[::-1], index=0, key="quick_year")
    
    with col2:
        if f"events_{year}" not in st.session_state:
            with st.spinner(f"Loading {year} events..."):
                events = get_available_events(year)
                st.session_state[f"events_{year}"] = events
        
        events = st.session_state.get(f"events_{year}", [])
        grand_prix = st.selectbox("Grand Prix", events if events else ["Loading..."], key="quick_gp")
    
    with col3:
        session_options = {
            'Race': 'R', 'Qualifying': 'Q', 'Sprint': 'S',
            'Practice 3': 'FP3', 'Practice 2': 'FP2', 'Practice 1': 'FP1'
        }
        session_name = st.selectbox("Session", list(session_options.keys()), key="quick_session")
        session_type = session_options[session_name]
    
    # Quick load button
    if st.button("⚡ Quick Load Session", type="primary", use_container_width=True):
        if grand_prix and grand_prix != "Loading...":
            with st.spinner("Loading session..."):
                session, error = load_session_data(year, grand_prix, session_type)
                if session:
                    st.session_state.session = session
                    st.session_state.session_loaded = True
                    st.session_state.session_overview = get_session_overview_no_cache(session)
                    st.session_state.selected_comparisons = {}  # Reset comparisons
                    st.success("✅ Session loaded!")
                    st.rerun()
                else:
                    st.error(f"❌ {error}")
    
    # Session overview with multi-driver selection
    if st.session_state.session_loaded and st.session_state.session_overview:
        overview = st.session_state.session_overview
        
        st.markdown(f"""
        <div class="quick-select">
            <h3>🏁 {year} {grand_prix} - {session_name}</h3>
            <p><strong>Drivers:</strong> {len(overview)} | <strong>Session Type:</strong> {session_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Driver selection for chart display
        available_drivers = list(overview.keys())
        selected_drivers = st.multiselect(
            "Select Drivers for Lap Times Chart (up to 4)", 
            available_drivers, 
            default=available_drivers[:2] if len(available_drivers) >= 2 else available_drivers,
            max_selections=4,
            key="quick_drivers"
        )
        
        if selected_drivers:
            # Lap times chart
            has_valid_data = any(
                len([lap for lap in overview[driver]['laps'] 
                     if not lap['deleted'] and lap['lap_time'] is not None]) > 0
                for driver in selected_drivers if driver in overview
            )
            
            if has_valid_data:
                fig_laptimes = create_lap_times_chart(overview, selected_drivers)
                st.plotly_chart(fig_laptimes, use_container_width=True)
                
                # Show tire strategy summary
                st.markdown("#### 🏎️ Tire Strategy Summary")
                for driver in selected_drivers:
                    if driver in overview:
                        driver_data = overview[driver]
                        valid_laps = [lap for lap in driver_data['laps'] 
                                     if not lap['deleted'] and lap['lap_time'] is not None]
                        
                        if valid_laps:
                            compound_counts = {}
                            for lap in valid_laps:
                                compound = lap['compound']
                                compound_counts[compound] = compound_counts.get(compound, 0) + 1
                            
                            compound_summary = ", ".join([f"{comp}: {count} laps" 
                                                        for comp, count in compound_counts.items()])
                            
                            st.info(f"**{driver}**: {compound_summary}")
            
            # Multi-driver lap selection for telemetry comparison
            st.markdown("### 🔄 Select Laps for Telemetry Comparison")
            st.info("Click on lap buttons below to select specific laps for each driver. Selected laps will be compared in the Multi-Driver Telemetry tab.")
            
            # Show current selections
            if st.session_state.selected_comparisons:
                st.markdown("""
                <div class="comparison-summary">
                    <h4>🎯 Selected for Comparison:</h4>
                </div>
                """, unsafe_allow_html=True)
                
                comparison_text = []
                for driver, lap_num in st.session_state.selected_comparisons.items():
                    comparison_text.append(f"**{driver}**: Lap {lap_num}")
                
                st.markdown(" | ".join(comparison_text))
                
                # Clear selections button
                if st.button("🗑️ Clear All Selections", key="clear_comparisons"):
                    st.session_state.selected_comparisons = {}
                    st.rerun()
            
            # Driver tabs for lap selection
            driver_tabs = st.tabs([f"🏎️ {driver}" for driver in selected_drivers])
            
            for i, driver in enumerate(selected_drivers):
                with driver_tabs[i]:
                    if driver in overview:
                        driver_data = overview[driver]
                        valid_laps = [lap for lap in driver_data['laps'] 
                                    if not lap['deleted'] and lap['lap_time'] is not None]
                        
                        if valid_laps:
                            current_selection = st.session_state.selected_comparisons.get(driver, None)
                            st.info(f"**{driver}** - Total: {len(valid_laps)} laps | Best: {format_lap_time(driver_data['best_lap_time'])} (Lap #{driver_data['best_lap_number']})")
                            
                            if current_selection:
                                st.success(f"✅ Currently selected: Lap {current_selection}")
                            
                            # Show all laps in grid
                            laps_per_row = 8
                            for row_start in range(0, len(valid_laps), laps_per_row):
                                cols = st.columns(laps_per_row)
                                
                                for j, lap in enumerate(valid_laps[row_start:row_start+laps_per_row]):
                                    with cols[j]:
                                        compound_class = get_tire_compound_class(lap['compound'])
                                        is_best = lap['is_personal_best']
                                        lap_time_str = format_lap_time(lap['lap_time'])
                                        
                                        # Check if this lap is currently selected
                                        is_selected = (current_selection == lap['lap_number'])
                                        button_type = "primary" if is_selected else "secondary"
                                        
                                        button_label = f"L{lap['lap_number']}"
                                        if is_best:
                                            button_label += " 🏆"
                                        
                                        if st.button(
                                            button_label,
                                            key=f"comparison_btn_{driver}_{lap['lap_number']}",
                                            type=button_type,
                                            use_container_width=True,
                                            help=f"Time: {lap_time_str}\nTire: {lap['compound']}\nClick to select for comparison"
                                        ):
                                            # Add/update this driver's selection
                                            st.session_state.selected_comparisons[driver] = lap['lap_number']
                                            st.rerun()
                                        
                                        # Show lap details
                                        st.caption(f"{lap_time_str}")
                                        tire_badge = f'<span class="{compound_class} tire-compound-badge">{lap["compound"]}</span>'
                                        st.markdown(f"<div style='text-align: center;'>{tire_badge}</div>", 
                                                   unsafe_allow_html=True)
                        else:
                            st.info(f"No valid lap times for {driver}")

# Tab 2: Multi-Driver Telemetry Comparison
with tab2:
    if st.session_state.session_loaded:
        st.markdown("### 📊 Multi-Driver Telemetry Comparison")
        
        if st.session_state.selected_comparisons:
            st.markdown(f"""
            <div class="comparison-summary">
                <h4>🎯 Comparing:</h4>
                <p>{' vs '.join([f'{driver} (Lap {lap})' for driver, lap in st.session_state.selected_comparisons.items()])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                session = st.session_state.session
                
                # Create multi-driver telemetry comparison
                fig_comparison = create_multi_driver_telemetry_comparison(
                    session, st.session_state.selected_comparisons
                )
                
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Show comparison statistics
                st.markdown("#### 📈 Comparison Statistics")
                
                stats_cols = st.columns(len(st.session_state.selected_comparisons))
                
                for i, (driver, lap_number) in enumerate(st.session_state.selected_comparisons.items()):
                    with stats_cols[i]:
                        try:
                            lap_filter = ((session.laps['Driver'] == driver) & 
                                         (session.laps['LapNumber'] == lap_number))
                            matching_laps = session.laps[lap_filter]
                            
                            if not matching_laps.empty:
                                lap = matching_laps.iloc[0]
                                telemetry = lap.get_telemetry()
                                
                                if not telemetry.empty:
                                    st.markdown(f"**{driver} - Lap {lap_number}**")
                                    st.metric("Lap Time", format_lap_time(lap['LapTime']))
                                    st.metric("Max Speed", f"{telemetry['Speed'].max():.1f} km/h")
                                    st.metric("Avg Speed", f"{telemetry['Speed'].mean():.1f} km/h")
                                    st.metric("Max RPM", f"{telemetry['RPM'].max():.0f}")
                        
                        except Exception as e:
                            st.error(f"Error loading stats for {driver}: {str(e)}")
            
            except Exception as e:
                st.error(f"Error creating comparison: {str(e)}")
                st.info("Try selecting different laps from the Quick Session tab")
        
        else:
            st.info("👈 Select drivers and their specific laps from the Quick Session tab to see telemetry comparison")
            
            st.markdown("""
            ### 📋 How to Compare Multiple Drivers:
            
            1. **Load a session** in the Quick Session tab
            2. **Select drivers** for the lap times chart
            3. **Click on specific lap buttons** for each driver you want to compare
            4. **Return here** to see the multi-driver telemetry comparison
            
            You can select different laps for different drivers (e.g., Driver A's fastest lap vs Driver B's fastest lap).
            """)
    
    else:
        st.info("Load a session in the Quick Session tab first")

# Tab 3: Advanced Setup (Your Original Configuration)
with tab3:
    st.markdown("### 🔧 Advanced Configuration")
    
    st.markdown("""
    <div class="control-panel">
        <h3 class="text-primary text-center mb-4">🔧 Analysis Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Your original advanced configuration code here
        st.info("Your original advanced configuration features")
    
    with col2:
        st.info("Your original driver selection and analysis features")

# Tab 4: Enhanced Driver Stats
with tab4:
    if st.session_state.session_loaded and st.session_state.session_overview:
        st.markdown("### 📈 Comprehensive Driver Statistics")
        
        overview = st.session_state.session_overview
        
        # Create stats table
        stats_data = []
        for driver, data in overview.items():
            valid_laps = [lap for lap in data['laps'] 
                         if not lap['deleted'] and lap['lap_time'] is not None]
            
            if valid_laps:
                lap_times = []
                for lap in valid_laps:
                    time_seconds = safe_lap_time_to_seconds(lap['lap_time'])
                    if time_seconds is not None:
                        lap_times.append(time_seconds)
                
                if lap_times:
                    stats_data.append({
                        'Driver': driver,
                        'Total Laps': len(lap_times),
                        'Best Time': min(lap_times),
                        'Average Time': sum(lap_times) / len(lap_times),
                        'Consistency (Std Dev)': np.std(lap_times),
                        'Tire Compounds': len(set(lap['compound'] for lap in valid_laps))
                    })
        
        if stats_data:
            df_stats = pd.DataFrame(stats_data)
            
            # Format times
            df_stats['Best Time'] = df_stats['Best Time'].apply(
                lambda x: f"{int(x//60)}:{x%60:06.3f}"
            )
            df_stats['Average Time'] = df_stats['Average Time'].apply(
                lambda x: f"{int(x//60)}:{x%60:06.3f}"
            )
            df_stats['Consistency (Std Dev)'] = df_stats['Consistency (Std Dev)'].apply(
                lambda x: f"{x:.3f}s"
            )
            
            st.dataframe(df_stats, use_container_width=True)
            
            # Performance visualization
            fig_performance = go.Figure()
            
            for _, row in df_stats.iterrows():
                driver_data = overview[row['Driver']]
                valid_laps = [lap for lap in driver_data['laps'] 
                            if not lap['deleted'] and lap['lap_time'] is not None]
                
                lap_times = []
                for lap in valid_laps:
                    time_seconds = safe_lap_time_to_seconds(lap['lap_time'])
                    if time_seconds is not None:
                        lap_times.append(time_seconds)
                
                if lap_times:
                    fig_performance.add_trace(go.Box(
                        y=lap_times,
                        name=row['Driver'],
                        boxmean=True
                    ))
            
            if fig_performance.data:
                fig_performance.update_layout(
                    title='Lap Time Distribution by Driver',
                    yaxis_title='Lap Time (seconds)',
                    template='plotly_dark',
                    height=500
                )
                st.plotly_chart(fig_performance, use_container_width=True)
        else:
            st.warning("No valid driver statistics available")
    else:
        st.info("Load a session to view driver statistics")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏎️ F1 Telemetry Analysis - Multi-Driver Comparison | Powered by FastF1</p>
</div>
""", unsafe_allow_html=True)
