import pandas as pd
import geopy.distance

# Load AQI data (assuming it has columns like timestamp, aqi, co, no, pm2_5, etc.)
aqi_data = pd.read_csv("delhi_aqi_data.csv",on_bad_lines='skip')

# Load Fire Data (assuming it has columns like latitude, longitude, confidence, frp, etc.)
fire_data = pd.read_csv("filtered_haryana_punjab_fire_data.csv")


# Function to calculate distance between two geo-coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.distance(coords_1, coords_2).km


# Combine the data by matching fire data within a certain radius (e.g., 10 km)
def combine_data(aqi_data, fire_data, radius_km=10):
    combined_data = []

    for _, aqi_row in aqi_data.iterrows():
        aqi_lat = aqi_row['latitude']  # Assuming latitude column in AQI data
        aqi_lon = aqi_row['longitude']  # Assuming longitude column in AQI data

        # Find nearby fire events (within the radius)
        nearby_fires = fire_data[
            fire_data.apply(
                lambda row: calculate_distance(aqi_lat, aqi_lon, row['latitude'], row['longitude']) <= radius_km,
                axis=1)
        ]

        # For each fire, append it with AQI data (you can decide how to aggregate data if multiple fires exist in the area)
        for _, fire_row in nearby_fires.iterrows():
            combined_record = {
                'timestamp': aqi_row['timestamp'],
                'aqi': aqi_row['aqi'],
                'co': aqi_row['co'],
                'no': aqi_row['no'],
                'no2': aqi_row['no2'],
                'o3': aqi_row['o3'],
                'so2': aqi_row['so2'],
                'pm2_5': aqi_row['pm2_5'],
                'pm10': aqi_row['pm10'],
                'nh3': aqi_row['nh3'],
                'fire_latitude': fire_row['latitude'],
                'fire_longitude': fire_row['longitude'],
                'confidence': fire_row['confidence'],
                'frp': fire_row['frp'],
                'bright_ti4': fire_row['bright_ti4'],
                'acq_date': fire_row['acq_date'],
                'acq_time': fire_row['acq_time']
            }
            combined_data.append(combined_record)

    # Convert to DataFrame
    combined_df = pd.DataFrame(combined_data)

    # Save combined data to CSV
    combined_df.to_csv("combined_aqi_fire_data.csv", index=False)
    print("Data combined and saved to combined_aqi_fire_data.csv")


# Call the function to combine the data
combine_data(aqi_data, fire_data)
