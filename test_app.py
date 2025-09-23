#!/usr/bin/env python3
"""
Simple test app for Streamlit Cloud deployment
"""

import streamlit as st

st.title("🚴‍♂️ Copenhagen Bike Analytics - Test")
st.write("This is a simple test to verify Streamlit Cloud deployment works.")

st.success("✅ If you can see this, the deployment is working!")

# Simple data
import pandas as pd
import numpy as np

# Generate some test data
np.random.seed(42)
data = {
    'Location': ['Nørrebrogade', 'Amagerbrogade', 'Englandsvej'],
    'Rides': [450, 380, 320]
}

df = pd.DataFrame(data)
st.dataframe(df)

st.bar_chart(df.set_index('Location'))

st.markdown("---")
st.markdown("**Test successful!** 🎉")
