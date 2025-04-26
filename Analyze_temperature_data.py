import os
import csv
import datetime
from collections import defaultdict

# === Function to get folder path from user ===
def get_folder_path():
    folder = input("📁 Enter the full path to the folder containing temperature CSV files:\n> ").strip()
    if not os.path.isdir(folder):
        print("❌ Folder not found. Please check the path and try again.")
        exit()
    return folder

# === Function to read and process CSV data ===
def read_temperature_data(folder_path):
    season_months = {
        'Summer': ['December', 'January', 'February'],
        'Autumn': ['March', 'April', 'May'],
        'Winter': ['June', 'July', 'August'],
        'Spring': ['September', 'October', 'November']
    }

    season_temps = defaultdict(list)
    station_temps = defaultdict(list)

    print("🔍 Scanning CSV files...")

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            print(f"📄 Reading file: {file_name}")
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    station = row.get("STATION_NAME", "").strip()
                    for month_num in range(1, 13):
                        month_name = datetime.datetime(1900, month_num, 1).strftime('%B')
                        temp_str = row.get(month_name, "").strip()
                        try:
                            temp = float(temp_str)
                            station_temps[station].append(temp)
                            for season, months in season_months.items():
                                if month_name in months:
                                    season_temps[season].append(temp)
                        except:
                            continue  # Skip missing or invalid temperature entries
    return station_temps, season_temps

# === Task 1: Average Seasonal Temperatures ===
def calculate_average_seasonal_temps(season_temps, output_path):
    print("📊 Calculating average seasonal temperatures...")
    with open(output_path, "w") as f:
        f.write("Average Seasonal Temperatures (1986–2005):\n")
        for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
            temps = season_temps[season]
            if temps:
                avg = sum(temps) / len(temps)
                f.write(f"{season}: {avg:.2f}°C\n")
    print(f"✅ Seasonal averages saved to: {output_path}")

# === Task 2: Station with Largest Temperature Range ===
def calculate_largest_temp_range(station_temps, output_path):
    print("📊 Finding station with largest temperature range...")
    largest_range = 0
    stations_with_range = []

    for station, temps in station_temps.items():
        if temps:
            t_range = max(temps) - min(temps)
            if t_range > largest_range:
                largest_range = t_range
                stations_with_range = [station]
            elif t_range == largest_range:
                stations_with_range.append(station)

    with open(output_path, "w") as f:
        f.write(f"Largest Temperature Range: {largest_range:.2f}°C\n")
        f.write("Station(s):\n")
        for s in stations_with_range:
            f.write(f"{s}\n")
    print(f"✅ Range info saved to: {output_path}")

# === Task 3: Warmest and Coolest Stations ===
def calculate_extreme_stations(station_temps, output_path):
    print("📊 Identifying warmest and coolest stations...")
    station_averages = {s: sum(t) / len(t) for s, t in station_temps.items() if t}

    max_avg = max(station_averages.values())
    min_avg = min(station_averages.values())

    warmest = [s for s, avg in station_averages.items() if avg == max_avg]
    coolest = [s for s, avg in station_averages.items() if avg == min_avg]

    with open(output_path, "w") as f:
        f.write(f"Warmest Station(s) Avg Temp: {max_avg:.2f}°C\n")
        for s in warmest:
            f.write(f"{s}\n")
        f.write(f"\nCoolest Station(s) Avg Temp: {min_avg:.2f}°C\n")
        for s in coolest:
            f.write(f"{s}\n")
    print(f"✅ Warmest/coolest stations saved to: {output_path}")

# === Main Program ===
def main():
    print("🌡️ Welcome to the Temperature Data Analyzer!")
    folder_path = get_folder_path()

    # Output file paths inside the data folder
    avg_file = os.path.join(folder_path, "average_temp.txt")
    range_file = os.path.join(folder_path, "largest_temp_range_station.txt")
    extremes_file = os.path.join(folder_path, "warmest_and_coolest_station.txt")

    station_temps, season_temps = read_temperature_data(folder_path)

    calculate_average_seasonal_temps(season_temps, avg_file)
    calculate_largest_temp_range(station_temps, range_file)
    calculate_extreme_stations(station_temps, extremes_file)

    print("\n🎉 All tasks completed successfully!")

if __name__ == "__main__":
    main()
