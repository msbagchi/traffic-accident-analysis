import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/US_Accidents_March23.csv", nrows=100000)

# Basic information
print(df.head())
print(df.shape)

# Convert datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'])

# Create hour column
df['Hour'] = df['Start_Time'].dt.hour

# Accidents by hour
hourly_accidents = df['Hour'].value_counts().sort_index()

plt.figure(figsize=(10,5))
hourly_accidents.plot(kind='bar')

plt.title("Accidents by Hour")
plt.xlabel("Hour")
plt.ylabel("Number of Accidents")

plt.show()