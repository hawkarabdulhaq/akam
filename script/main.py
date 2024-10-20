import pandas as pd
import folium

def filter_data(file_path):
    """Filters the data into two sets: below 25°C and above 25°C. Saves them into new sheets."""
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Filter the data where temperature ('Temp') is below and above 25°C
    filtered_below_df = df[df['Temp'] < 25]
    filtered_above_df = df[df['Temp'] > 25]

    # Create the output file name by adding '_Filtered' before the file extension
    output_file_name = file_path.split('.')[0] + '_Filtered.xlsx'

    # Save the filtered data into two new sheets "Below_25" and "Above_25"
    with pd.ExcelWriter(output_file_name, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Original_Data', index=False)  # Save original sheet
        filtered_below_df.to_excel(writer, sheet_name='Below_25', index=False)  # Save below 25°C
        filtered_above_df.to_excel(writer, sheet_name='Above_25', index=False)  # Save above 25°C

    print(f"Filtered data saved to: {output_file_name}")
    return output_file_name

def visualize_data(file_path):
    """Creates a map visualizing the data points from the 'Below_25' and 'Above_25' sheets."""
    # Load the Excel file
    df_below_25 = pd.read_excel(file_path, sheet_name='Below_25')
    df_above_25 = pd.read_excel(file_path, sheet_name='Above_25')

    # Create a base map centered at the average coordinates
    avg_lat = (df_below_25['latitude'].mean() + df_above_25['latitude'].mean()) / 2
    avg_lon = (df_below_25['longitude'].mean() + df_above_25['longitude'].mean()) / 2
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

    # Add markers for "Below_25" data points (blue)
    for idx, row in df_below_25.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"Temp: {row['Temp']}°C"
        ).add_to(m)

    # Add markers for "Above_25" data points (red)
    for idx, row in df_above_25.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup=f"Temp: {row['Temp']}°C"
        ).add_to(m)

    # Save the map as an HTML file
    map_file_name = 'output/temperature_map.html'
    m.save(map_file_name)
    print(f"Map saved to: {map_file_name}")

def main():
    # Step 1: Specify the path of your Excel file
    file_path = 'data/sample_data.xlsx'  # Replace with your file path

    # Step 2: Filter the data and save to new sheets
    filtered_file_name = filter_data(file_path)

    # Step 3: Visualize the filtered data on a map
    visualize_data(filtered_file_name)

if __name__ == "__main__":
    main()
