import tkinter
from tkinter import ttk
import os
from tkintermapview import TkinterMapView
import threading
import time
import csv

# Global variables
lat = 31.2831274
lon = 75.6465185
prev_marker = None  # Store the reference to the previous marker
count = 0

# Path to the CSV file
csv_file_path = "output.csv"  # Update with the correct path to your CSV file

# Function to read the CSV file and extract the latest latitude and longitude
# def read_csv_and_update_coordinates():
def read_csv_and_update_coordinates():
    global lat, lon
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 1:  # Check if the row has more than one column
                location = row[1]
                if ',' in location and len(location) == 21:  # Ensure the location contains a comma
                    try:
                        lat, lon = map(float, location.split(','))
                    except ValueError as e:
                        print(f"Error converting location to float: {e}")
                        continue  # Skip this row if there is an error

# Create tkinter window
root_tk = tkinter.Tk()
screen_width = root_tk.winfo_screenwidth()
screen_height = root_tk.winfo_screenheight()
desired_width = screen_width // 2  # Half of the screen width
desired_height = screen_height
x_offset = screen_width - desired_width  # Align to the right side
root_tk.geometry(f"{desired_width}x{desired_height}+{x_offset}+0")
root_tk.title("Map View Example")

# Path for the database to use
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "offline_punjab.db")

# Create map widget
map_widget = TkinterMapView(root_tk, width=desired_width, height=desired_height, corner_radius=0, use_database_only=False, max_zoom=17, database_path=database_path)
map_widget.pack(fill="both", expand=True)
map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

# Function to handle marker click
def marker_click(marker, file_path='output.csv'):
    location = marker.position  # Get the marker's position
    location = f"{location[0]},{location[1]}"

    # Read the CSV file
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        data = list(csv_reader)

    # Filter rows based on the location
    filtered_data = [row for row in data if len(row) > 1 and is_70_percent_match(location, row[1])]
    # print(filtered_data, location)
#
    # Open a new Tkinter window to display the filtered data
    show_filtered_data(filtered_data)


# Function to check if two strings match by at least 70%
def is_70_percent_match(s1, s2):
    if len(s1) != len(s2):
        return False
    matches = sum(1 for a, b in zip(s1, s2) if a == b)
    return matches / len(s1) >= 0.9

# Function to display filtered data in a new window
def show_filtered_data(filtered_data):
    root = tkinter.Tk()
    root.title("Filtered Data")

    tree = ttk.Treeview(root)
    tree.pack(side='left', fill='both', expand=True)

    # Define columns
    columns = ["time", "location", "frequency", "channel magnitude", "channel bandwidth"]
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='w')

    # Insert data into treeview
    for row in filtered_data:
        tree.insert("", "end", values=row)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    root.mainloop()

# Function to add markers periodically
def add_marker_periodically():
    global lat, lon, prev_marker, count
    map_widget.set_zoom(15)
    last_lat, last_lon = lat, lon  # Initialize with the starting coordinates
    while True:
        read_csv_and_update_coordinates()  # Read the latest coordinates from CSV

        if (lat, lon) != (last_lat, last_lon):  # Only add marker if coordinates have changed
            # Set a position marker with updated latitude and longitude
            marker = map_widget.set_marker(lat, lon, text=f"{count}", command=marker_click)
            if prev_marker:
                # Draw a line between the current marker and the previous one
                path = map_widget.set_path([(prev_marker.position), marker.position])
            prev_marker = marker
            if count % 20 == 0 or count == 1:
                map_widget.set_position(lat, lon)

            last_lat, last_lon = lat, lon  # Update the last coordinates
            count += 1

        time.sleep(1)  # Wait for 1 second before checking again

# Start a separate thread to add markers periodically
marker_thread = threading.Thread(target=add_marker_periodically)
marker_thread.daemon = True
marker_thread.start()

root_tk.mainloop()
