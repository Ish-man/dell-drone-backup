


# import csv
# import tkinter
# from tkintermapview import TkinterMapView
# import threading
# import argparse

# def plot_csv_locations_on_map(csv_file_path):
#     # Global variables
#     lat = 31.2831274
#     lon = 75.6465185
#     prev_marker = None  # Store the reference to the previous marker
#     count = 0

#     # Create tkinter window
#     root_tk = tkinter.Tk()
#     root_tk.geometry("800x600")
#     root_tk.title("Map View Example")

#     # Create map widget
#     map_widget = TkinterMapView(root_tk, width=800, height=600, corner_radius=0, use_database_only=False, max_zoom=17)
#     map_widget.pack(fill="both", expand=True)
#     map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

#     # Function to add markers periodically
#     def add_marker_periodically():
#         nonlocal lat, lon, prev_marker, count
#         map_widget.set_zoom(15)
#         last_lat, last_lon = lat, lon  # Initialize with the starting coordinates
#         with open(csv_file_path, 'r', newline='') as csvfile:
#             csv_reader = csv.reader(csvfile)
#             data = list(csv_reader)
#             for row in data:
#                 if len(row) == 5 and len(row[0]) == 23:
#                     coordinates = row[1]  # Read the latest coordinates from CSV
#                     lat, lon = [float(i) for i in coordinates.split(',')]
#                     if (lat, lon) != (last_lat, last_lon):  # Only add marker if coordinates have changed
#                         # Set a position marker with updated latitude and longitude
#                         marker = map_widget.set_marker(lat, lon, text=f"{count}")
#                         if prev_marker:
#                             # Draw a line between the current marker and the previous one
#                             path = map_widget.set_path([(prev_marker.position), marker.position])
#                         prev_marker = marker
#                         if count % 20 == 0 or count == 1:
#                             map_widget.set_position(lat, lon)

#                         last_lat, last_lon = lat, lon  # Update the last coordinates
#                         count += 1

#     # Start a separate thread to add markers periodically
#     marker_thread = threading.Thread(target=add_marker_periodically)
#     marker_thread.daemon = True
#     marker_thread.start()

#     root_tk.mainloop()

# if __name__ == "__main__":
#     # Set up argument parser
#     parser = argparse.ArgumentParser(description="Plot CSV locations on a map.")
#     parser.add_argument("csv_file_path", type=str, help="Path to the CSV file")
#     args = parser.parse_args()
    
#     # Call the function with the provided CSV file path
#     plot_csv_locations_on_map(args.csv_file_path)

import csv
import tkinter
from tkintermapview import TkinterMapView
import threading
import argparse

def plot_csv_locations_on_map(csv_file_path):
    # Global variables
    lat = 31.2831274
    lon = 75.6465185
    prev_marker = None  # Store the reference to the previous marker
    count = 0

    # Create tkinter window
    root_tk = tkinter.Tk()
    screen_width = root_tk.winfo_screenwidth()
    screen_height = root_tk.winfo_screenheight()
    window_width = (screen_width // 2)-80
    window_height = screen_height

    # Calculate the position to place the window on the right side
    x_position = screen_width - window_width
    y_position = 0

    # Set the window geometry
    root_tk.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root_tk.title("Map View Example")

    # Create map widget
    map_widget = TkinterMapView(root_tk, width=window_width, height=window_height, corner_radius=0, use_database_only=False, max_zoom=17)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    # Function to add markers periodically
    def add_marker_periodically():
        nonlocal lat, lon, prev_marker, count
        map_widget.set_zoom(15)
        last_lat, last_lon = lat, lon  # Initialize with the starting coordinates
        with open(csv_file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)
            for row in data:
                if len(row) == 5 and len(row[0]) == 23:
                    coordinates = row[1]  # Read the latest coordinates from CSV
                    lat, lon = [float(i) for i in coordinates.split(',')]
                    if (lat, lon) != (last_lat, last_lon):  # Only add marker if coordinates have changed
                        # Set a position marker with updated latitude and longitude
                        marker = map_widget.set_marker(lat, lon, text=f"{count}")
                        if prev_marker:
                            # Draw a line between the current marker and the previous one
                            path = map_widget.set_path([(prev_marker.position), marker.position])
                        prev_marker = marker
                        if count % 20 == 0 or count == 1:
                            map_widget.set_position(lat, lon)

                        last_lat, last_lon = lat, lon  # Update the last coordinates
                        count += 1

    # Start a separate thread to add markers periodically
    marker_thread = threading.Thread(target=add_marker_periodically)
    marker_thread.daemon = True
    marker_thread.start()

    root_tk.mainloop()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Plot CSV locations on a map.")
    parser.add_argument("csv_file_path", type=str, help="Path to the CSV file")
    args = parser.parse_args()
    
    # Call the function with the provided CSV file path
    plot_csv_locations_on_map(args.csv_file_path)
