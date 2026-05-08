import pandas as pd
import folium
from folium.plugins import HeatMap

# Load dataset
df = pd.read_csv("data/US_Accidents_March23.csv", nrows=5000)

# Drop missing coordinates
df = df.dropna(subset=['Start_Lat', 'Start_Lng'])

# Create base map
map_center = [df['Start_Lat'].mean(), df['Start_Lng'].mean()]

m = folium.Map(location=map_center, zoom_start=4)

# Heatmap data
heat_data = list(zip(df['Start_Lat'], df['Start_Lng']))

# Add heatmap
HeatMap(heat_data).add_to(m)

# Save map
m.save("heatmap.html")

print("Heatmap created successfully!")
