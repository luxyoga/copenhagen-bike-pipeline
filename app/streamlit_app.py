import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Copenhagen Bike Analytics", layout="wide")

# Add CSS to force full width
st.markdown("""
<style>
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    .stPlotlyChart {
        width: 100% !important;
    }
    .stPlotlyChart > div {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Try to use real data with weather first, fallback to other data
REAL_DATASET_WITH_WEATHER_FIXED = Path("/data/curated/real_copenhagen_data_with_weather_fixed.csv")
REAL_DATASET_WITH_WEATHER = Path("/data/curated/real_copenhagen_data_with_weather.csv")
REAL_DATASET = Path("/data/curated/clean_real_copenhagen_data.csv")
SYNTHETIC_DATASET = Path("/data/curated/real_daily_counts.csv")

if REAL_DATASET_WITH_WEATHER_FIXED.exists():
    DATASET = REAL_DATASET_WITH_WEATHER_FIXED
    DATA_TYPE = "Real Copenhagen Cycling Data + Real Weather (2005-2014)"
elif REAL_DATASET_WITH_WEATHER.exists():
    DATASET = REAL_DATASET_WITH_WEATHER
    DATA_TYPE = "Real Copenhagen Cycling Data + Real Weather (2005-2014)"
elif REAL_DATASET.exists():
    DATASET = REAL_DATASET
    DATA_TYPE = "Real Copenhagen Cycling Data (2005-2014)"
else:
    DATASET = SYNTHETIC_DATASET
    DATA_TYPE = "Synthetic Data"

st.title("🚴‍♂️ Copenhagen Bike Analytics - Real Data (2005-2014)")

# Data type indicator
if REAL_DATASET_WITH_WEATHER_FIXED.exists():
    st.success(f"📊 Using {DATA_TYPE} - Real Copenhagen cycling data with real weather!")
elif REAL_DATASET_WITH_WEATHER.exists():
    st.success(f"📊 Using {DATA_TYPE} - Real Copenhagen cycling data with real weather!")
elif REAL_DATASET.exists():
    st.success(f"📊 Using {DATA_TYPE} - Real Copenhagen cycling data")
else:
    st.info(f"📊 Using {DATA_TYPE} - Simulated data for demonstration")

st.markdown("---")

if not DATASET.exists():
    st.info("No data yet. Trigger the Airflow DAG once.")
else:
    # Read the data based on file format
    if str(DATASET).endswith('.csv'):
        df = pd.read_csv(DATASET)
    else:
        # For parquet files, use pandas directly
        df = pd.read_parquet(DATASET)
    
    df['day'] = pd.to_datetime(df['day'])
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Unique Locations", f"{df['counter_key'].nunique():,}")
    with col3:
        st.metric("Date Range", f"{df['day'].min().strftime('%Y-%m-%d')} to {df['day'].max().strftime('%Y-%m-%d')}")
    with col4:
        st.metric("Total Rides (10 Years)", f"{df['total'].sum():,.0f}")

    # Year and season overview
    if 'year' in df.columns and 'season' in df.columns:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Years Covered", f"{df['year'].nunique()}")
        with col2:
            st.metric("Seasons", f"{df['season'].nunique()}")
        with col3:
            st.metric("Months", f"{df['month'].nunique()}")
        with col4:
            # Calculate average daily rides correctly (sum by day, then average)
            daily_totals = df.groupby('day')['total'].sum()
            avg_daily_rides = daily_totals.mean()
            st.metric("Avg Daily Rides (10 Years)", f"{avg_daily_rides:.0f}")
    
    st.markdown("---")
    
    # Month selector
    if 'month' in df.columns and 'year' in df.columns:
        st.header("📅 Monthly Data Analysis")
        
        # Create month selector
        available_months = sorted(df[['year', 'month', 'month_name']].drop_duplicates().values.tolist())
        month_options = [f"{year} - {month_name}" for year, month, month_name in available_months]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_month = st.selectbox(
                "Select a month to analyze:",
                options=month_options,
                index=len(month_options) - 1  # Default to most recent month
            )
        
        with col2:
            show_all_months = st.checkbox("Show all months", value=False)
        
        if not show_all_months and selected_month:
            # Filter data for selected month
            selected_year, selected_month_name = selected_month.split(" - ")
            selected_year = int(selected_year)
            
            # Get month number from month name
            month_mapping = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            selected_month_num = month_mapping[selected_month_name]
            
            month_df = df[(df['year'] == selected_year) & (df['month'] == selected_month_num)]
            
            if len(month_df) > 0:
                st.subheader(f"📊 {selected_month_name} {selected_year} Analysis")
                
                # Monthly metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Rides (Month)", f"{month_df['total'].sum():,.0f}")
                with col2:
                    # Calculate average daily rides correctly (sum by day, then average)
                    daily_totals = month_df.groupby('day')['total'].sum()
                    avg_daily_rides = daily_totals.mean()
                    st.metric("Avg Daily Rides (Month)", f"{avg_daily_rides:.0f}")
                with col3:
                    st.metric("Days in Month", f"{len(month_df['day'].unique())}")
                with col4:
                    st.metric("Top Location", f"{month_df.groupby('counter_key')['total'].sum().idxmax()}")
                
                # Daily trends for the month
                st.subheader("📈 Daily Trends")
                daily_trends = month_df.groupby('day')['total'].sum().reset_index()
                daily_trends['day'] = pd.to_datetime(daily_trends['day'])
                
                fig_daily = px.line(
                    daily_trends,
                    x='day',
                    y='total',
                    title=f"Daily Bike Rides - {selected_month_name} {selected_year}",
                    labels={'total': 'Daily Rides', 'day': 'Date'}
                )
                st.plotly_chart(fig_daily, use_container_width=True)
                
                # Top locations for the month
                st.subheader("🏆 Top Locations This Month")
                top_locations_month = month_df.groupby('counter_key')['total'].sum().nlargest(10)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_top = px.bar(
                        x=top_locations_month.values,
                        y=top_locations_month.index,
                        orientation='h',
                        title=f"Top 10 Locations - {selected_month_name} {selected_year}",
                        labels={'x': 'Total Rides', 'y': 'Location'}
                    )
                    fig_top.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_top, use_container_width=True)
                
                with col2:
                    st.subheader("📊 Monthly Statistics")
                    month_stats = month_df.groupby('counter_key').agg({
                        'total': ['sum', 'mean', 'std', 'count']
                    }).round(0)
                    month_stats.columns = ['Total Rides', 'Avg Daily', 'Std Dev', 'Days']
                    month_stats = month_stats.sort_values('Total Rides', ascending=False)
                    st.dataframe(month_stats.head(10), use_container_width=True)
                
                # Weather analysis for the month
                if 'weather_condition' in month_df.columns:
                    st.subheader("🌤️ Weather Impact This Month")
                    weather_month = month_df.groupby('weather_condition').agg({
                        'total': ['mean', 'sum'],
                        'day': 'nunique'
                    }).round(0)
                    weather_month.columns = ['Avg Daily Rides', 'Total Rides', 'Days with This Weather']
                    st.dataframe(weather_month, use_container_width=True)
            else:
                st.warning(f"No data found for {selected_month_name} {selected_year}")
        else:
            # Show all months analysis
            st.subheader("📊 All Months Overview")
            
            # Monthly summary
            monthly_summary = df.groupby(['year', 'month', 'month_name']).agg({
                'total': ['sum', 'mean'],
                'day': 'nunique'
            }).round(0)
            monthly_summary.columns = ['Total Rides', 'Avg Daily', 'Days in Month']
            monthly_summary = monthly_summary.reset_index()
            monthly_summary['year_month'] = monthly_summary['year'].astype(str) + '-' + monthly_summary['month'].astype(str).str.zfill(2)
            
            st.dataframe(monthly_summary, use_container_width=True)
    
    st.markdown("---")
    
    # Seasonal analysis
    if 'season' in df.columns:
        st.header("🍂 Seasonal Analysis (2005-2014)")
        
        col1, col2 = st.columns(2)
        
        with col1:
                st.subheader("📊 Seasonal Patterns (10-Year Totals)")
                # Calculate seasonal data correctly
                seasonal_data = []
                for season in df['season'].unique():
                    season_df = df[df['season'] == season]
                    daily_totals = season_df.groupby('day')['total'].sum()
                    total_rides = season_df['total'].sum()
                    days_in_season = season_df['day'].nunique()
                    avg_daily_rides = daily_totals.mean()
                    
                    seasonal_data.append({
                        'season': season,
                        'Avg Daily Rides': round(avg_daily_rides, 0),
                        'Total Rides': round(total_rides, 0),
                        'Days in This Season': days_in_season
                    })
                
                seasonal_summary = pd.DataFrame(seasonal_data)
                seasonal_summary = seasonal_summary.set_index('season')
                st.dataframe(seasonal_summary, use_container_width=True)
        
        with col2:
            st.subheader("📈 Monthly Trends (Average per Month)")
            seasonal_trends = df.groupby(['season', 'month_name'])['total'].mean().reset_index()
            fig_seasonal = px.bar(
                seasonal_trends,
                x='month_name',
                y='total',
                color='season',
                title="Average Daily Rides by Month and Season",
                labels={'total': 'Avg Daily Rides', 'month_name': 'Month'}
            )
            fig_seasonal.update_xaxes(tickangle=45)
            st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Monthly trends
        st.subheader("📅 Monthly Trends Over Time")
        monthly_trends = df.groupby(['year', 'month', 'month_name'])['total'].sum().reset_index()
        monthly_trends['year_month'] = monthly_trends['year'].astype(str) + '-' + monthly_trends['month'].astype(str).str.zfill(2)
        
        fig_monthly = px.line(
            monthly_trends,
            x='year_month',
            y='total',
            title="Total Monthly Rides Over Time",
            labels={'total': 'Total Monthly Rides', 'year_month': 'Year-Month'}
        )
        fig_monthly.update_xaxes(tickangle=45)
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    st.markdown("---")
    
    # Weather analysis
    if 'weather_condition' in df.columns:
        st.header("🌤️ Weather Impact Analysis (2005-2014)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌦️ Weather Conditions Impact (10-Year Totals)")
            # Calculate weather data correctly
            weather_data = []
            for weather in df['weather_condition'].unique():
                weather_df = df[df['weather_condition'] == weather]
                daily_totals = weather_df.groupby('day')['total'].sum()
                total_rides = weather_df['total'].sum()
                days_with_weather = weather_df['day'].nunique()
                avg_daily_rides = daily_totals.mean()
                
                weather_data.append({
                    'weather_condition': weather,
                    'Avg Daily Rides': round(avg_daily_rides, 0),
                    'Total Rides': round(total_rides, 0),
                    'Days with This Weather': days_with_weather
                })
            
            weather_summary = pd.DataFrame(weather_data)
            weather_summary = weather_summary.set_index('weather_condition')
            st.dataframe(weather_summary, use_container_width=True)
        
        with col2:
            if 'temperature' in df.columns:
                st.subheader("🌡️ Temperature vs Bike Usage")
                temp_analysis = df.groupby(pd.cut(df['temperature'], bins=5))['total'].mean()
                temp_df = pd.DataFrame({
                    'Temperature Range': temp_analysis.index.astype(str),
                    'Avg Rides': temp_analysis.values
                })
                st.dataframe(temp_df, use_container_width=True)
        
                
                # Add a clean summary table
                st.subheader("📋 Weather Impact Summary")
                weather_summary = df.groupby('weather_condition').agg({
                    'total': ['mean', 'std'],
                    'temperature': 'mean',
                    'precipitation': 'mean'
                }).round(1)
                weather_summary.columns = ['Avg Daily Rides', 'Std Dev', 'Avg Temp (°C)', 'Avg Precipitation (mm)']
                st.dataframe(weather_summary, use_container_width=True)
    
    st.markdown("---")
    
    # Location analysis
    st.header("📍 Top Cycling Locations")
    
    # Top 20 locations by total rides
    top_locations = df.groupby('counter_key')['total'].sum().nlargest(20)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 20 Busiest Locations")
        fig_bar = px.bar(
            x=top_locations.values,
            y=top_locations.index,
            orientation='h',
            title="Total Bike Rides by Location",
            labels={'x': 'Total Rides', 'y': 'Location'},
            height=600,  # Make it taller
            width=1200   # Make it wider
        )
        
        # Update layout for better readability
        fig_bar.update_layout(
            height=600,
            xaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                categoryorder='total ascending'
            ),
            title_font=dict(size=16)
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("📊 Location Statistics")
        location_stats = df.groupby('counter_key').agg({
            'total': ['count', 'sum', 'mean', 'std']
        }).round(0)
        location_stats.columns = ['Days', 'Total Rides', 'Avg Daily', 'Std Dev']
        location_stats = location_stats.sort_values('Total Rides', ascending=False)
        st.dataframe(location_stats.head(15), use_container_width=True)
    
    st.markdown("---")
    
    # Interactive location selector
    st.header("🔍 Interactive Location Analysis")
    
    # Location selector
    all_locations = sorted(df['counter_key'].unique())
    selected_locations = st.multiselect(
        "Select locations to analyze:",
        options=all_locations,
        default=top_locations.head(5).index.tolist()
    )
    
    if selected_locations:
        filtered_df = df[df['counter_key'].isin(selected_locations)]
        
        # Make the graph full width and larger
        st.subheader("📈 Daily Rides Comparison")
        pivot_data = filtered_df.pivot(index='day', columns='counter_key', values='total')
        
        # Create a larger, more readable line chart
        fig_line = px.line(
            pivot_data.reset_index(),
            x='day',
            y=[col for col in pivot_data.columns],
            title="Daily Bike Rides Over Time",
            labels={'value': 'Daily Rides', 'day': 'Date'},
            height=600,  # Make it taller
            width=1200   # Make it wider
        )
        
        # Update layout for better readability
        fig_line.update_layout(
            height=600,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.01
            ),
            xaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            title_font=dict(size=16)
        )
        
        # Make lines thicker for better visibility
        for trace in fig_line.data:
            trace.line.width = 3
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Summary statistics in a separate section
        st.subheader("📊 Summary Statistics")
        summary_stats = filtered_df.groupby('counter_key')['total'].agg([
            'count', 'sum', 'mean', 'min', 'max'
        ]).round(0)
        summary_stats.columns = ['Days', 'Total', 'Avg Daily', 'Min', 'Max']
        st.dataframe(summary_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Weather analysis - moved to same section as other working charts
    if 'temperature' in df.columns:
        st.header("🌤️ Weather Impact Analysis")
        
        # Create temperature bins for better visualization
        df['temp_bin'] = pd.cut(df['temperature'], bins=8, precision=0)
        temp_analysis = df.groupby(['temp_bin', 'weather_condition'])['total'].mean().reset_index()
        
        # Convert interval objects to strings for JSON serialization
        temp_analysis['temp_bin_str'] = temp_analysis['temp_bin'].astype(str)
        
        # Temperature chart - exactly like other working charts
        st.subheader("🌡️ Temperature vs Bike Usage")
        fig_temp = px.bar(
            temp_analysis,
            x='temp_bin_str',
            y='total',
            color='weather_condition',
            title="Average Bike Rides by Temperature Range",
            labels={'total': 'Avg Daily Rides', 'temp_bin_str': 'Temperature Range (°C)'}
        )
        fig_temp.update_xaxes(tickangle=45)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        st.markdown("---")
        
        # Create precipitation bins
        df['precip_bin'] = pd.cut(df['precipitation'], bins=5, precision=1)
        precip_analysis = df.groupby(['precip_bin', 'weather_condition'])['total'].mean().reset_index()
        
        # Convert interval objects to strings for JSON serialization
        precip_analysis['precip_bin_str'] = precip_analysis['precip_bin'].astype(str)
        
        # Precipitation chart - exactly like other working charts
        st.subheader("🌧️ Precipitation Impact")
        fig_precip = px.bar(
            precip_analysis,
            x='precip_bin_str',
            y='total',
            color='weather_condition',
            title="Average Bike Rides by Precipitation",
            labels={'total': 'Avg Daily Rides', 'precip_bin_str': 'Precipitation Range (mm)'}
        )
        fig_precip.update_xaxes(tickangle=45)
        st.plotly_chart(fig_precip, use_container_width=True)
    
    st.markdown("---")
    
    # Insights section
    st.header("💡 Key Insights")
    
    # Calculate insights
    insights = []
    
    # Top location
    top_location = df.groupby('counter_key')['total'].sum().idxmax()
    top_location_rides = df.groupby('counter_key')['total'].sum().max()
    insights.append(f"🏆 **Busiest Location**: {top_location} with {top_location_rides:,.0f} total rides")
    
    # Average rides
    avg_rides = df['total'].mean()
    insights.append(f"📊 **Average Daily Rides**: {avg_rides:.0f} rides per location per day")
    
    # Most consistent location
    consistency = df.groupby('counter_key')['total'].std()
    most_consistent = consistency.idxmin()
    insights.append(f"🎯 **Most Consistent**: {most_consistent} (lowest variation in daily rides)")
    
    # Total system usage
    total_rides = df['total'].sum()
    insights.append(f"🚴‍♂️ **Total System Usage**: {total_rides:,.0f} bike rides across all locations")
    
    for insight in insights:
        st.markdown(insight)
    
    st.markdown("---")
    
    # Raw data section
    st.header("📋 Raw Data")
    st.dataframe(df.head(100), use_container_width=True)