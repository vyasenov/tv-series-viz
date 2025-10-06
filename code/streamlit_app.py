import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import statsmodels.api as sm
import os
import plotly.express as px  # NEW

st.set_page_config(  # NEW
    page_title="TV Series IMDB Ratings",
    page_icon="📺",
    layout="wide",
)

st.markdown("""
    <style>
    /* Round and clip Plotly chart container */
    div[data-testid="stPlotlyChart"] > div {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08); /* optional subtle border */
        background: transparent; /* let Plotly control its own bg */
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions from your existing code
def lowess_smooth(group, frac=0.8, it=3):
    x = group['episode']
    y = group['rating']
    group['rating_lowess'] = sm.nonparametric.lowess(y, x, frac=frac, return_sorted=False, it=it)
    group['season'] = group.name  # add back the grouping key
    return group

def normalize_episode(group):
    n = len(group)
    if n == 1:
        return pd.Series([1.0], index=group.index)
    return pd.Series(1 + (group['episode'] - 1) / (n - 1), index=group.index)

def load_show_data(show_name):
    # Use absolute path to ensure we find the data files
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', f'{show_name}_ratings.csv')
    data = pd.read_csv(data_path)
    
    # Debug: print columns to see what's available
    print(f"Loading {show_name}, columns: {data.columns.tolist()}")
    
    # Normalize episodes within each season
    episode_norm_values = []
    for season in data['season'].unique():
        season_data = data[data['season'] == season]
        n = len(season_data)
        if n == 1:
            norm_values = [1.0]
        else:
            norm_values = 1 + (season_data['episode'] - 1) / (n - 1)
        episode_norm_values.extend(norm_values)
    
    data['episode_norm'] = episode_norm_values + data['season'] - 1
    data = data.groupby('season', group_keys=False).apply(lowess_smooth, include_groups=False)
    return data

def get_available_shows():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('_ratings.csv')]
    return sorted([f.replace('_ratings.csv', '') for f in csv_files])

# Main app
#st.title("📺 TV Series Ratings")
st.caption('Created by <a href="https://vyasenov.github.io/" target="_blank">Vasco Yasenov</a> | <a href="https://github.com/vyasenov/tv-series-viz" target="_blank">GitHub</a>', unsafe_allow_html=True)

# Get available shows
available_shows = get_available_shows()

# Multi-select dropdown
selected_shows = st.multiselect(
    "Select shows to compare:",
    options=available_shows,
    #default=available_shows[3:5] if len(available_shows) >= 2 else available_shows,
    default=['succession', 'westworld'],
    format_func=lambda x: x.replace('_', ' ').title()
)

if selected_shows:
    # Create plot
    fig = go.Figure()
    
    # Calmer palette that works on dark backgrounds
    colors = px.colors.qualitative.Bold
        
    for i, show in enumerate(selected_shows):
        data = load_show_data(show)
        color = colors[i % len(colors)]
        show_name = show.replace('_', ' ').title()
        
        # Plot each season
        for season in sorted(data['season'].unique()):
            season_data = data[data['season'] == season]
            
            # Show legend only for the first season of each show
            show_legend = bool(season == sorted(data['season'].unique())[0])
            
            fig.add_trace(go.Scatter(
                x=season_data['episode_norm'],
                y=season_data['rating_lowess'],
                mode='lines+markers',
                name=show_name if show_legend else None,
                legendgroup=show_name,  # Group all seasons of the same show
                line=dict(color=color, width=3),
                marker=dict(size=3),
                showlegend=show_legend,
                hovertemplate=show_name + ": %{y:.2f}<extra></extra>"
            ))
    
    # Add season boundaries
    if selected_shows:
        max_season = max([load_show_data(show)['season'].max() for show in selected_shows])
        for boundary in range(2, max_season + 1):
            fig.add_vline(x=boundary, line_dash="dash", line_color="gray", opacity=0.7, line_width=1)
    
    # Update layout with better styling
    fig.update_layout(
        xaxis=dict(
            title="Season",
            title_font=dict(size=20),
            tickmode='array',
            tickvals=[i + 0.5 for i in range(1, max_season + 1)],
            ticktext=[str(i) for i in range(1, max_season + 1)],
            tickfont=dict(size=16),
            showgrid=False
        ),
        yaxis=dict(
            title="IMDB Rating",
            title_font=dict(size=20),
            tickfont=dict(size=16),
            showgrid=False
        ),
        height=700,
        width=1000,
        paper_bgcolor="#1B2230",  # soft gray to match secondary background
        plot_bgcolor="#1B2230",   # same soft gray within plot area
        font=dict(color="#EAEAEA"),  # match app text color
        hoverlabel=dict(font=dict(color="white", size=18), bgcolor="#1B2230"),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=18)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please select at least one show to visualize.")
