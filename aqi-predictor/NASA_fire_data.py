import pandas as pd
import glob

# Define the path to the directory containing your CSV files
csv_file_path = "fire_sat_data/*txt"  # Update this path

# Use glob to find all CSV files in the directory
csv_files = glob.glob(csv_file_path)

# Check if any files were found
if not csv_files:
    print("No CSV files found. Please check the file path.")

# Create an empty list to hold DataFrames
all_data = []

# Loop through each CSV file and read it into a DataFrame
for file in csv_files:
    try:
        print(f"Reading file: {file}")  # Debugging line
        df = pd.read_csv(file)

        # Optionally, add a column to indicate the source file (if needed)
        df['source_file'] = file

        # Append the DataFrame to the list
        all_data.append(df)

    except Exception as e:
        print(f"Error reading {file}: {e}")

# Check if any data was loaded
if not all_data:
    print("No data was loaded. Please check the CSV files.")
else:
    # Concatenate all DataFrames into a single DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)

    # Define the boundaries for Haryana and Punjab
    haryana_lat_range = (28, 31)  # Latitude range for Haryana
    haryana_lon_range = (75, 77)  # Longitude range for Haryana

    punjab_lat_range = (30, 32)  # Latitude range for Punjab
    punjab_lon_range = (73, 77)  # Longitude range for Punjab

    # Filter data for Haryana
    haryana_data = combined_data[
        (combined_data['latitude'] >= haryana_lat_range[0]) & (combined_data['latitude'] <= haryana_lat_range[1]) &
        (combined_data['longitude'] >= haryana_lon_range[0]) & (combined_data['longitude'] <= haryana_lon_range[1])]

    # Filter data for Punjab
    punjab_data = combined_data[
        (combined_data['latitude'] >= punjab_lat_range[0]) & (combined_data['latitude'] <= punjab_lat_range[1]) &
        (combined_data['longitude'] >= punjab_lon_range[0]) & (combined_data['longitude'] <= punjab_lon_range[1])]

    # Combine data for both Haryana and Punjab
    combined_haryana_punjab_data = pd.concat([haryana_data, punjab_data])

    # Optionally: Save filtered data to CSV
    combined_haryana_punjab_data.to_csv("filtered_haryana_punjab_fire_data.csv", index=False)

    # Display filtered data
    print(combined_haryana_punjab_data.head())
