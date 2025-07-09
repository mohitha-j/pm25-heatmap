import streamlit as st
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.title("City PM2.5 Heatmap Demo")

city = st.text_input("Enter a city name:")

if city:
    geolocator = Nominatim(user_agent="pm25-demo-app")
    location = geolocator.geocode(city)
    if location:
        lat, lon = location.latitude, location.longitude
        st.success(f"Found {city}: ({lat:.4f}, {lon:.4f})")
        # Generate random points around the city center
        np.random.seed(42)
        n_points = 200
        lats = lat + 0.05 * (np.random.rand(n_points) - 0.5)
        lons = lon + 0.05 * (np.random.rand(n_points) - 0.5)
        pm25 = np.random.uniform(20, 150, n_points)
        df = pd.DataFrame({"lat": lats, "lon": lons, "pm25": pm25})
        # Create Folium map
        m = folium.Map(location=[lat, lon], zoom_start=11)
        heat_data = [[row["lat"], row["lon"], row["pm25"]] for idx, row in df.iterrows()]
        HeatMap(heat_data, radius=18, blur=15, max_zoom=13, min_opacity=0.4).add_to(m)
        st_folium(m, width=700, height=500)
        st.write("Sample PM2.5 data:")
        st.dataframe(df.head(10))
    else:
        st.error("City not found. Please try another name.")
else:
    st.info("Enter a city name to see the PM2.5 heatmap.")
