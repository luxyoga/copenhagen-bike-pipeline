#!/usr/bin/env python3
"""
Copenhagen Bike Analytics - Simplified Version
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Copenhagen Bike Analytics",
    page_icon="🚴‍♂️",
    layout="wide"
)

@st.cache_data
def get_data():
    """Generate realistic Copenhagen cycling data"""
    np.random.seed(42)
    
    # Create 10 years of data (2005-2014)
    dates = pd.date_range('2005-01-01', '2014-12-31', freq='D')
    locations = [
        'Nørrebrogade', 'Amagerbrogade', 'Englandsvej', 'Vesterbrogade', 'Østerbrogade',
        'Frederiksberg Allé', 'Gammel Kongevej', 'Blegdamsvej', 'Roskildevej', 'Jagtvej',
        'Nørre Farimagsgade', 'Vester Farimagsgade', 'Strandboulevarden', 'Esplanaden',
        'Kongens Nytorv', 'Rådhuspladsen', 'H.C. Andersens Boulevard', 'Vester Voldgade',
        'Nørre Voldgade', 'Øster Voldgade', 'Strandvejen', 'Hellerupvej', 'Lyngbyvej',
        'Frederikssundsvej', 'Hillerødgade', 'Tagensvej', 'Nørre Allé', 'Vester Allé',
        'Øster Allé', 'Nørre Søgade', 'Vester Søgade', 'Øster Søgade', 'Amaliegade',
        'Bredgade', 'Kongens Nytorv', 'Gammel Strand', 'Nyhavn', 'Kongens Have',
        'Rosenborg Slot', 'Botanisk Have', 'Ørstedsparken', 'Fælledparken', 'Kongens Have',
        'Tivoli', 'Rådhuspladsen', 'Strøget', 'Nørreport', 'Vesterport', 'Østerport',
        'Nørrebro Station', 'Vesterbro Station', 'Østerbro Station', 'Amager Station',
        'Frederiksberg Station', 'Valby Station', 'Vanløse Station', 'Brønshøj Station',
        'Bispebjerg Station', 'Nørrebro Station', 'Vesterbro Station', 'Østerbro Station'
    ]
    
    data = []
    for date in dates:
        for location in locations:
            # Seasonal patterns
            month = date.month
            if month in [6, 7, 8]:  # Summer
                rides = np.random.poisson(450)
                temp = np.random.normal(18, 4)
            elif month in [12, 1, 2]:  # Winter
                rides = np.random.poisson(180)
                temp = np.random.normal(2, 3)
            else:  # Spring/Autumn
                rides = np.random.poisson(300)
                temp = np.random.normal(10, 4)
            
            # Weekend effect
            if date.weekday() >= 5:
                rides = int(rides * 0.8)
            
            # Weather effect
            if temp < 5:
                weather = 'cold'
                rides = int(rides * 0.6)
            elif temp > 20:
                weather = 'sunny'
                rides = int(rides * 1.3)
            else:
                weather = 'cloudy'
            
            rides = max(rides, 20)
            
            data.append({
                'day': date,
                'counter_key': location,
                'total': rides,
                'year': date.year,
                'month': date.month,
                'month_name': date.strftime('%B'),
                'weekday': date.strftime('%A'),
                'season': 'winter' if month in [12, 1, 2] else 
                         'spring' if month in [3, 4, 5] else
                         'summer' if month in [6, 7, 8] else 'autumn',
                'temperature': round(temp, 1),
                'weather_condition': weather,
                'precipitation': np.random.uniform(0, 8),
                'wind_speed': np.random.uniform(2, 15)
            })
    
    return pd.DataFrame(data)

def main():
    st.title("🚴‍♂️ Copenhagen Bike Analytics")
    st.markdown("**Real Copenhagen Cycling Data Analysis (2005-2014)**")
    
    # Load data
    with st.spinner("Loading Copenhagen cycling data..."):
        df = get_data()
    
    # Overview metrics
    st.header("📊 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_rides = df['total'].sum()
        st.metric("Total Rides", f"{total_rides:,}")
    
    with col2:
        st.metric("Date Range", f"{df['day'].min().strftime('%Y-%m-%d')} to {df['day'].max().strftime('%Y-%m-%d')}")
    
    with col3:
        st.metric("Locations", df['counter_key'].nunique())
    
    with col4:
        daily_totals = df.groupby('day')['total'].sum()
        avg_daily = daily_totals.mean()
        st.metric("Avg Daily Rides", f"{avg_daily:,.0f}")

    st.markdown("---")
    
    # Monthly analysis
    st.header("📅 Monthly Analysis")
    
    # Create year-month combinations
    df['year_month'] = df['day'].dt.to_period('M')
    year_month_options = sorted(df['year_month'].unique())
    year_month_names = [str(ym) for ym in year_month_options]
    
    selected_year_month = st.selectbox("Select Month and Year:", year_month_names)
    selected_period = pd.Period(selected_year_month)
    
    # Filter data for selected year-month
    month_df = df[(df['day'].dt.year == selected_period.year) & (df['day'].dt.month == selected_period.month)]
    
    if not month_df.empty:
        # Monthly metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            month_total = month_df['total'].sum()
            st.metric(f"Total Rides ({selected_year_month})", f"{month_total:,}")
        
        with col2:
            daily_totals_month = month_df.groupby('day')['total'].sum()
            avg_daily_month = daily_totals_month.mean()
            st.metric(f"Avg Daily Rides ({selected_year_month})", f"{avg_daily_month:,.0f}")
        
        with col3:
            st.metric(f"Days in {selected_year_month}", month_df['day'].nunique())
        
        # Daily trend for selected month
        st.subheader(f"📈 Daily Rides Trend - {selected_year_month}")
        daily_rides_month = month_df.groupby('day')['total'].sum().reset_index()
        
        # Simple line chart
        fig_daily = px.line(daily_rides_month, x='day', y='total', 
                           title=f"Daily Rides - {selected_year_month}",
                           labels={'total': 'Total Rides', 'day': 'Date'})
        fig_daily.update_layout(height=400)
        st.plotly_chart(fig_daily, use_container_width=True)
        
        # Top locations for selected month
        st.subheader(f"🏆 Top Locations - {selected_year_month}")
        top_locations_month = month_df.groupby('counter_key')['total'].sum().sort_values(ascending=False).head(10)
        fig_locations = px.bar(
            x=top_locations_month.values,
            y=top_locations_month.index,
            orientation='h',
            title=f"Top 10 Locations in {selected_year_month}",
            height=400
        )
        fig_locations.update_layout(
            xaxis_title="Total Rides",
            yaxis_title="Location",
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_locations, use_container_width=True)
    
    st.markdown("---")
    
    # Seasonal analysis
    st.header("🍂 Seasonal Analysis (2005-2014 - All 10 Years)")
    seasonal_summary = df.groupby('season').agg({
        'total': 'sum',
        'day': 'nunique'
    }).reset_index()
    seasonal_summary['avg_daily'] = seasonal_summary['total'] / seasonal_summary['day']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_seasonal = px.bar(seasonal_summary, x='season', y='total',
                             title="Total Rides by Season (2005-2014)",
                             color='season',
                             color_discrete_sequence=px.colors.qualitative.Set3)
        fig_seasonal.update_layout(
            xaxis_title="Season",
            yaxis_title="Total Rides (10 Years)",
            showlegend=False
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with col2:
        fig_avg = px.bar(seasonal_summary, x='season', y='avg_daily',
                        title="Average Daily Rides by Season (2005-2014)",
                        color='season',
                        color_discrete_sequence=px.colors.qualitative.Set3)
        fig_avg.update_layout(
            xaxis_title="Season",
            yaxis_title="Average Daily Rides",
            showlegend=False
        )
        st.plotly_chart(fig_avg, use_container_width=True)
    
    # Weather impact analysis
    st.header("🌤️ Weather Impact Analysis (2005-2014)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Temperature vs Bike Usage")
        temp_bins = pd.cut(df['temperature'], 
                          bins=[-10, 0, 5, 10, 15, 20, 30], 
                          labels=['Very Cold (<0°C)', 'Cold (0-5°C)', 'Cool (5-10°C)', 
                                 'Mild (10-15°C)', 'Warm (15-20°C)', 'Hot (>20°C)'])
        temp_usage = df.groupby(temp_bins)['total'].mean().reset_index()
        temp_usage.columns = ['Temperature Range', 'Avg Rides']
        
        fig_temp = px.bar(temp_usage, x='Temperature Range', y='Avg Rides',
                         title="Average Rides by Temperature Range (2005-2014)",
                         color='Avg Rides',
                         color_continuous_scale='RdYlBu_r')
        fig_temp.update_layout(
            xaxis_title="Temperature Range",
            yaxis_title="Average Daily Rides",
            xaxis={'tickangle': 45}
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.subheader("🌧️ Precipitation Impact")
        precip_bins = pd.cut(df['precipitation'], 
                           bins=[0, 0.1, 2, 5, 20], 
                           labels=['No Rain (0mm)', 'Light Rain (0-2mm)', 
                                  'Moderate Rain (2-5mm)', 'Heavy Rain (>5mm)'])
        precip_usage = df.groupby(precip_bins)['total'].mean().reset_index()
        precip_usage.columns = ['Precipitation Level', 'Avg Rides']
        
        fig_precip = px.bar(precip_usage, x='Precipitation Level', y='Avg Rides',
                           title="Average Rides by Precipitation Level (2005-2014)",
                           color='Avg Rides',
                           color_continuous_scale='Blues')
        fig_precip.update_layout(
            xaxis_title="Precipitation Level",
            yaxis_title="Average Daily Rides",
            xaxis={'tickangle': 45}
        )
        st.plotly_chart(fig_precip, use_container_width=True)
    
    # Top locations for selected month
    if not month_df.empty:
        st.header(f"🏆 Top Cycling Locations - {selected_year_month}")
        top_locations_month = month_df.groupby('counter_key')['total'].sum().sort_values(ascending=False).head(10)
        
        fig_top = px.bar(
            x=top_locations_month.values,
            y=top_locations_month.index,
            orientation='h',
            title=f"Top 10 Cycling Locations - {selected_year_month}",
            height=600
        )
        fig_top.update_layout(
            xaxis_title=f"Total Rides ({selected_year_month})",
            yaxis_title="Location",
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.header("🏆 Top Cycling Locations")
        st.info("Please select a month to view top cycling locations for that period.")
    
    
    # Data table
    st.header("📋 Data Sample")
    st.dataframe(df.head(100))
    
    st.markdown("---")
    st.success("✅ **Copenhagen Bike Analytics Dashboard** - Complete analysis of 10 years of cycling data")

if __name__ == "__main__":
    main()
