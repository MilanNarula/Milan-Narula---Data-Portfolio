"""
F1 analytics functions for data processing and visualization
Handles FastF1 API integration, telemetry processing, and chart generation
"""
import streamlit as st
import fastf1
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial import KDTree
import tempfile
import os
from datetime import datetime

# Setup FastF1 cache
@st.cache_resource
def setup_f1_cache():
    """Initialize FastF1 cache directory"""
    cache_dir = tempfile.mkdtemp()
    fastf1.Cache.enable_cache(cache_dir)
    return cache_dir

def load_session_data(year, grand_prix, session_type):
    """
    Load F1 session data from FastF1 API
    
    Args:
        year (int): Championship year
        grand_prix (str): Grand Prix name
        session_type (str): Session type (FP1, FP2, FP3, Q, S, R)
    
    Returns:
        tuple: (session_object, error_message)
    """
    try:
        with st.spinner(f"Loading {year} {grand_prix} {session_type} session..."):
            session = fastf1.get_session(year, grand_prix, session_type)
            session.load(telemetry=True, weather=False, messages=False)
            return session, None
    except Exception as e:
        return None, str(e)

@st.cache_data
def get_available_events(year):
    """
    Get available F1 events for a given year
    
    Args:
        year (int): Championship year
    
    Returns:
        list: Available event names
    """
    try:
        schedule = fastf1.get_event_schedule(year)
        # Filter for events that have already occurred or are current
        current_date = datetime.now()
        events = []
        
        for _, event in schedule.iterrows():
            event_date = pd.to_datetime(event['EventDate'])
            if event_date <= current_date:
                events.append(event['EventName'])
        
        return events if events else schedule['EventName'].tolist()[:10]
    except:
        # Fallback list of common events
        return [
            'Bahrain Grand Prix', 'Saudi Arabian Grand Prix', 'Australian Grand Prix',
            'Japanese Grand Prix', 'Chinese Grand Prix', 'Miami Grand Prix',
            'Emilia Romagna Grand Prix', 'Monaco Grand Prix', 'Canadian Grand Prix',
            'Spanish Grand Prix', 'Austrian Grand Prix', 'British Grand Prix',
            'Hungarian Grand Prix', 'Belgian Grand Prix', 'Dutch Grand Prix',
            'Italian Grand Prix', 'Azerbaijan Grand Prix', 'Singapore Grand Prix',
            'United States Grand Prix', 'Mexico City Grand Prix', 'São Paulo Grand Prix'
        ]

@st.cache_data
def process_driver_data(_session, drivers):
    """
    Process telemetry data for selected drivers
    
    Args:
        _session: FastF1 session object (underscore to avoid hashing)
        drivers (list): List of driver codes
    
    Returns:
        tuple: (driver_data_dict, combined_telemetry_df)
    """
    driver_data = {}
    all_laps_telemetry = []
    
    progress_bar = st.progress(0, text="Processing driver data...")
    
    for idx, driver_code in enumerate(drivers):
        progress_bar.progress((idx + 1) / len(drivers), 
                            text=f"Processing {driver_code} data...")
        
        try:
            driver_laps = _session.laps.pick_drivers(driver_code)
            if driver_laps.empty:
                continue
            
            # Filter for valid laps only
            valid_laps = driver_laps.loc[
                (driver_laps['IsAccurate'] == True) &
                (driver_laps['LapTime'].notna()) &
                (driver_laps['PitOutTime'].isna()) &
                (driver_laps['PitInTime'].isna())
            ].reset_index(drop=True)
            
            if valid_laps.empty:
                continue
                
            driver_telemetry_laps = []
            
            # Process each valid lap
            for lap_number in valid_laps['LapNumber'].unique():
                lap = valid_laps.loc[valid_laps['LapNumber'] == lap_number].iloc[0]
                try:
                    telemetry = lap.get_telemetry()
                    if telemetry.empty:
                        continue
                    
                    # Add distance calculation
                    telemetry = telemetry.add_distance()
                    
                    # Select required columns
                    required_cols = ['Distance', 'Speed', 'RPM', 'Throttle', 
                                   'Brake', 'DRS', 'nGear', 'X', 'Y']
                    telemetry = telemetry[required_cols].copy()
                    telemetry['LapNumber'] = lap_number
                    telemetry['Driver'] = driver_code
                    telemetry['LapTime'] = lap['LapTime'].total_seconds()
                    
                    driver_telemetry_laps.append(telemetry)
                    all_laps_telemetry.append(telemetry)
                    
                except Exception as e:
                    continue
            
            if driver_telemetry_laps:
                driver_data[driver_code] = pd.concat(
                    driver_telemetry_laps, ignore_index=True
                )
                
        except Exception as e:
            st.warning(f"Error processing {driver_code}: {str(e)}")
            continue
    
    progress_bar.empty()
    
    if all_laps_telemetry:
        all_telemetry_df = pd.concat(all_laps_telemetry, ignore_index=True)
        return driver_data, all_telemetry_df
    else:
        return {}, pd.DataFrame()

def create_track_plot(driver_data, selected_drivers, height=600):
    """
    Create interactive track map visualization
    
    Args:
        driver_data (dict): Driver telemetry data
        selected_drivers (list): Selected driver codes
        height (int): Plot height
    
    Returns:
        plotly.graph_objects.Figure: Track map figure
    """
    fig = go.Figure()
    
    if not selected_drivers or selected_drivers[0] not in driver_data:
        return fig
        
    # Use first driver's first lap for track outline
    first_driver_data = driver_data[selected_drivers[0]]
    first_lap = first_driver_data['LapNumber'].min()
    track_data = first_driver_data[first_driver_data['LapNumber'] == first_lap]
    
    if track_data.empty:
        return fig
    
    # Add track outline
    fig.add_trace(go.Scatter(
        x=track_data['X'],
        y=track_data['Y'],
        mode='lines',
        name='Track Layout',
        line=dict(color='#666666', width=4),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Add position marker
    fig.add_trace(go.Scatter(
        x=[track_data['X'].iloc[0]],
        y=[track_data['Y'].iloc[0]],
        mode='markers',
        marker=dict(
            size=15,
            color='#FF6B35',
            symbol='circle',
            line=dict(width=3, color='white')
        ),
        name='Current Position',
        hovertemplate='<b>Current Position</b><br>Distance: 0m<extra></extra>',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='🏁 Track Map - Interactive Position Control',
            font=dict(size=18, color='#FF6B35'),
            x=0.5
        ),
        xaxis=dict(
            title='X Coordinate (m)',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        yaxis=dict(
            title='Y Coordinate (m)',
            scaleanchor="x",
            scaleratio=1,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white'
        ),
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font=dict(color='white'),
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='closest'
    )
    
    return fig

def create_telemetry_plots(driver_data, selected_drivers, selected_lap, selected_distance):
    """
    Create telemetry comparison plots
    
    Args:
        driver_data (dict): Driver telemetry data
        selected_drivers (list): Selected driver codes
        selected_lap (int): Selected lap number
        selected_distance (float): Selected track distance
    
    Returns:
        plotly.graph_objects.Figure: Telemetry plots figure
    """
    telemetry_metrics = ['Speed', 'RPM', 'Throttle', 'Brake', 'DRS', 'nGear']
    metric_titles = ['Speed (km/h)', 'RPM', 'Throttle (%)', 'Brake', 'DRS', 'Gear']
    num_metrics = len(telemetry_metrics)
    
    # Create subplots
    fig = make_subplots(
        rows=num_metrics,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=metric_titles
    )
    
    # Driver colors
    driver_colors = {
        selected_drivers[0]: '#00D4FF',  # Cyan
        selected_drivers[1]: '#FF6B35' if len(selected_drivers) > 1 else '#F7931E'  # Orange
    }
    
    for driver_code in selected_drivers:
        if driver_code not in driver_data or driver_data[driver_code].empty:
            continue
            
        # Filter data for selected lap
        lap_telemetry = driver_data[driver_code][
            driver_data[driver_code]['LapNumber'] == selected_lap
        ].copy()
        
        if lap_telemetry.empty:
            continue
            
        lap_telemetry = lap_telemetry.sort_values(by='Distance').reset_index(drop=True)
        
        # Add traces for each metric
        for i, metric in enumerate(telemetry_metrics):
            fig.add_trace(
                go.Scatter(
                    x=lap_telemetry['Distance'],
                    y=lap_telemetry[metric],
                    mode='lines',
                    name=driver_code,
                    line=dict(
                        color=driver_colors.get(driver_code, 'white'),
                        width=2
                    ),
                    legendgroup=driver_code,
                    showlegend=(i == 0),
                    hovertemplate=f'<b>{driver_code}</b><br>' +
                                f'Distance: %{{x:.0f}}m<br>' +
                                f'{metric_titles[i]}: %{{y}}<extra></extra>'
                ),
                row=i + 1, col=1
            )
        
        # Add reference line at selected distance
        for i in range(num_metrics):
            fig.add_vline(
                x=selected_distance,
                line_width=2,
                line_dash="dash",
                line_color="#FFCD3C",
                annotation_text=f"{selected_distance:.0f}m",
                annotation_position="top",
                row=i + 1, col=1
            )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'📊 Telemetry Analysis - Lap {selected_lap}',
            font=dict(size=18, color='#FF6B35'),
            x=0.5
        ),
        height=150 * num_metrics,
        plot_bgcolor='#262730',
        paper_bgcolor='#262730',
        font=dict(color='white'),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        ),
        margin=dict(l=60, r=20, t=80, b=60)
    )
    
    # Update axis labels
    for i, title in enumerate(metric_titles):
        fig.update_yaxes(
            title_text=title,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='white',
            row=i + 1, col=1
        )
    
    fig.update_xaxes(
        title_text='Distance (m)',
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.1)',
        color='white',
        row=num_metrics, col=1
    )
    
    return fig

def update_track_marker(fig, driver_data, selected_drivers, selected_distance):
    """
    Update track map marker position based on selected distance
    
    Args:
        fig: Plotly figure object
        driver_data (dict): Driver telemetry data
        selected_drivers (list): Selected driver codes
        selected_distance (float): Selected distance
    """
    if not selected_drivers or selected_drivers[0] not in driver_data:
        return
        
    first_driver_data = driver_data[selected_drivers[0]]
    first_lap = first_driver_data['LapNumber'].min()
    track_data = first_driver_data[first_driver_data['LapNumber'] == first_lap]
    
    if track_data.empty:
        return
    
    # Find closest point to selected distance
    distances = np.abs(track_data['Distance'] - selected_distance)
    closest_idx = distances.idxmin()
    
    marker_x = track_data.loc[closest_idx, 'X']
    marker_y = track_data.loc[closest_idx, 'Y']
    actual_distance = track_data.loc[closest_idx, 'Distance']
    
    # Update marker position
    if len(fig.data) > 1:
        fig.data[1].x = [marker_x]
        fig.data[1].y = [marker_y]
        fig.data[1].hovertemplate = f'<b>Current Position</b><br>Distance: {actual_distance:.1f}m<extra></extra>'

def get_lap_summary_stats(driver_data, selected_drivers, selected_lap):
    """
    Get summary statistics for selected lap
    
    Args:
        driver_data (dict): Driver telemetry data
        selected_drivers (list): Selected driver codes
        selected_lap (int): Selected lap number
    
    Returns:
        dict: Summary statistics
    """
    stats = {}
    
    for driver in selected_drivers:
        if driver not in driver_data:
            continue
            
        lap_data = driver_data[driver][
            driver_data[driver]['LapNumber'] == selected_lap
        ]
        
        if lap_data.empty:
            continue
            
        stats[driver] = {
            'max_speed': lap_data['Speed'].max(),
            'avg_speed': lap_data['Speed'].mean(),
            'max_rpm': lap_data['RPM'].max(),
            'avg_throttle': lap_data['Throttle'].mean(),
            'avg_brake': lap_data['Brake'].mean(),
            'drs_usage': (lap_data['DRS'] > 0).sum() / len(lap_data) * 100
        }
    
    return stats
