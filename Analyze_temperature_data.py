import os
import csv
import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

# === Function to choose a folder ===
def get_folder_path():
    folder = filedialog.askdirectory(title="Select Folder with CSV Files")
    if not folder:
        messagebox.showerror("Error", "No folder selected. Program will exit.")
        exit()
    return folder

# === Function to read and organize temperature data ===
def read_temperature_data(folder_path):
    # Define months for each season
    seasons = {
        'Summer': ['December', 'January', 'February'],
        'Autumn': ['March', 'April', 'May'],
        'Winter': ['June', 'July', 'August'],
        'Spring': ['September', 'October', 'November']
    }

    season_temps = defaultdict(list)   # Temperatures by season
    station_temps = defaultdict(list)  # Temperatures by station

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    station = row.get("STATION_NAME", "").strip()
                    for month_num in range(1, 13):
                        month_name = datetime.datetime(1900, month_num, 1).strftime('%B')
                        temp = row.get(month_name, "").strip()
                        try:
                            temp = float(temp)
                            station_temps[station].append(temp)
                            # Add temperature to the correct season
                            for season, months in seasons.items():
                                if month_name in months:
                                    season_temps[season].append(temp)
                        except:
                            continue  # If data is missing or wrong, just skip
    return station_temps, season_temps

# === Task 1: Calculate Average Seasonal Temperatures ===
def calculate_average_seasonal_temps(season_temps, output_file):
    with open(output_file, "w") as f:
        f.write("Average Temperatures by Season (1986–2005):\n")
        for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
            temps = season_temps.get(season, [])
            if temps:
                avg_temp = sum(temps) / len(temps)
                f.write(f"{season}: {avg_temp:.2f}°C\n")

# === Task 2: Find Station with Largest Temperature Range ===
def calculate_largest_temp_range(station_temps, output_file):
    largest_range = 0
    stations = []

    for station, temps in station_temps.items():
        if temps:
            temp_range = max(temps) - min(temps)
            if temp_range > largest_range:
                largest_range = temp_range
                stations = [station]
            elif temp_range == largest_range:
                stations.append(station)

    with open(output_file, "w") as f:
        f.write(f"Largest Temperature Range: {largest_range:.2f}°C\n")
        f.write("Station(s):\n")
        for station in stations:
            f.write(f"{station}\n")

# === Task 3: Find Warmest and Coolest Stations ===
def calculate_extreme_stations(station_temps, output_file):
    averages = {station: sum(temps) / len(temps) for station, temps in station_temps.items() if temps}

    max_avg = max(averages.values())
    min_avg = min(averages.values())

    warmest_stations = [station for station, avg in averages.items() if avg == max_avg]
    coolest_stations = [station for station, avg in averages.items() if avg == min_avg]

    with open(output_file, "w") as f:
        f.write(f"Warmest Station(s) Avg Temp: {max_avg:.2f}°C\n")
        for station in warmest_stations:
            f.write(f"{station}\n")
        f.write(f"\nCoolest Station(s) Avg Temp: {min_avg:.2f}°C\n")
        for station in coolest_stations:
            f.write(f"{station}\n")

# === Function to open a file when clicked ===
def open_file(filepath):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(filepath)
        elif os.name == 'posix':  # MacOS/Linux
            subprocess.call(['open', filepath])
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file: {e}")

# === Function to run all tasks ===
def run_analysis():
    try:
        folder_path = get_folder_path()
        station_temps, season_temps = read_temperature_data(folder_path)

        # Output files
        avg_file = os.path.join(folder_path, "average_temp.txt")
        range_file = os.path.join(folder_path, "largest_temp_range_station.txt")
        extremes_file = os.path.join(folder_path, "warmest_and_coolest_station.txt")

        # Perform calculations
        calculate_average_seasonal_temps(season_temps, avg_file)
        calculate_largest_temp_range(station_temps, range_file)
        calculate_extreme_stations(station_temps, extremes_file)

        # Success message
        messagebox.showinfo("Done!", "🎉 Reports created successfully!\nClick buttons below to view them.")

        # Show buttons to open created files
        show_file_buttons([avg_file, range_file, extremes_file])

    except Exception as e:
        messagebox.showerror("Error", str(e))

# === Function to create file-opening buttons ===
def show_file_buttons(file_list):
    for widget in file_frame.winfo_children():
        widget.destroy()

    for filepath in file_list:
        filename = os.path.basename(filepath)
        btn = tk.Button(file_frame, text=f"📄 View {filename}", font=("Arial", 12),
                        bg="lightgreen", command=lambda path=filepath: open_file(path))
        btn.pack(pady=5)

# === Main GUI Window ===
window = tk.Tk()
window.title("🌡️ Temperature Data Analyzer")
window.geometry("550x450")
window.configure(bg="lightyellow")

# Heading
title_label = tk.Label(window, text="Temperature Data Analyzer", font=("Arial", 22, "bold"), bg="lightyellow")
title_label.pack(pady=20)

# Instructions
instruction_label = tk.Label(window, text="Click below to select your CSV folder\nand generate temperature reports.", font=("Arial", 14), bg="lightyellow")
instruction_label.pack(pady=10)

# Analyze Button
analyze_button = tk.Button(window, text="📂 Select Folder and Start Analysis", font=("Arial", 16), bg="green", fg="white", command=run_analysis)
analyze_button.pack(pady=20)

# Frame to hold file buttons after analysis
file_frame = tk.Frame(window, bg="lightyellow")
file_frame.pack(pady=10)

# Run the app
window.mainloop()
