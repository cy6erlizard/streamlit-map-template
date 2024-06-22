import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# State management for map center coordinates
if "map_center" not in st.session_state:
    st.session_state["map_center"] = [50, 8]  # Initial center coordinates

st.set_page_config(layout="wide")

st.title("Interactive CO2 Emission Heatmap")

# Load CSV data into a Pandas DataFrame
df = pd.read_csv("https://raw.githubusercontent.com/cy6erlizard/c_chain_files/main/heatmap.csv")
df['start_time'] = pd.to_datetime(df['start_time'])

# Extract unique years from the DataFrame
unique_years = df['start_time'].dt.year.unique()

# Create a slider to select the year
selected_year = st.slider("Select Year:", min_value=unique_years.min(), max_value=unique_years.max(), value=unique_years[0])

# Filter DataFrame based on the selected year
df_filtered = df[df['start_time'].dt.year == selected_year]

# Define the heatmap configuration
m = leafmap.Map(center=st.session_state["map_center"], zoom=5.5)
m.add_heatmap(
    data=df_filtered,
    latitude="lat",
    longitude="lon",
    value="pop_max",  # Assuming "pop_max" represents CO2 emission values
    name="CO2 Emission Heatmap",
    radius=40,
)
m.add_basemap("SATELLITE")
m.to_streamlit(height=700)
