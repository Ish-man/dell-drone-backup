
from PyQt5 import Qt, QtCore
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox, QSizePolicy, QScrollArea
from gnuradio import uhd
from gnuradio.fft import window
import sys
import signal
import sip
from gnuradio import network
import csv
import subprocess
import time
import iridium
import serial
# import firebase_reader
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# from gnuradio import uhd
from PyQt5 import QtWidgets, QtGui

import random
from PyQt5.QtWidgets import QTableWidgetItem

import openpyxl
import shutil


new_freq = 40e6
from PyQt5.QtCore import QTimer




class DarkPalette:
    def __init__(self):
        self.primary_color = Qt.QColor(53, 53, 53)
        self.secondary_color = Qt.QColor(35, 35, 35)
        self.tertiary_color = Qt.QColor(42, 130, 218)
        self.text_color = Qt.QColor(255, 255, 255)
        self.disabled_text_color = Qt.QColor(127, 127, 127)
        self.background_color = Qt.QColor(25, 25, 25)
        self.disabled_background_color = Qt.QColor(45, 45, 45)
        self.highlight_color = Qt.QColor(42, 130, 218)

    def apply(self, app):
        app.setStyle("Fusion")
        dark_palette = Qt.QPalette()
        dark_palette.setColor(Qt.QPalette.Window, self.background_color)
        dark_palette.setColor(Qt.QPalette.WindowText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Base, self.secondary_color)
        dark_palette.setColor(Qt.QPalette.AlternateBase, self.background_color)
        dark_palette.setColor(Qt.QPalette.ToolTipBase, self.secondary_color)
        dark_palette.setColor(Qt.QPalette.ToolTipText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Text, self.text_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.Text, self.disabled_text_color)
        dark_palette.setColor(Qt.QPalette.Button, self.secondary_color)
        dark_palette.setColor(Qt.QPalette.ButtonText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.ButtonText, self.disabled_text_color)
        dark_palette.setColor(Qt.QPalette.BrightText, self.highlight_color)
        dark_palette.setColor(Qt.QPalette.Link, self.tertiary_color)
        dark_palette.setColor(Qt.QPalette.Highlight, self.highlight_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.Highlight, self.disabled_background_color)
        dark_palette.setColor(Qt.QPalette.HighlightedText, self.text_color)
        dark_palette.setColor(Qt.QPalette.Disabled, Qt.QPalette.HighlightedText, self.disabled_text_color)

        app.setPalette(dark_palette)


class Testing(gr.top_block, Qt.QWidget):
    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        screen_resolution = Qt.QDesktopWidget().screenGeometry()
        width = screen_resolution.width() // 2
        height = screen_resolution.height() // 2
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        self.setGeometry(0, 0, width, height)
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "testing")

        self.settings = Qt.QSettings("GNU Radio", "simple")
        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frequency)
        self.toggle_frequency = False  # Flag to toggle between two frequencies
        self.timer.start(5)



        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################


       
        ##################################################
        # Blocks
        ##################################################

        # Create a new frame
        self.new_frame = Qt.QFrame()
        self.new_layout = Qt.QHBoxLayout(self.new_frame)
        
        # Logo
        self.logo_label = Qt.QLabel(self)
        pixmap = Qt.QPixmap('logo.png')  # Replace 'logo.png' with your logo file
        pixmap_scaled = pixmap.scaledToWidth(200)  # Adjust the width as needed
        self.logo_label.setPixmap(pixmap_scaled)
        self.new_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignRight)
        # Heading Text
        # self.heading_label = Qt.QLabel("RF DRISTI MAP", self)
        # self.heading_label.setStyleSheet("font-size: 25px; font-weight: bold;")  # Adjust font size and style as needed
        # self.new_layout.addWidget(self.heading_label, 0, QtCore.Qt.AlignLeft)
        # self.top_layout.addWidget(self.new_frame)

        # Heading Text
        self.heading_label = Qt.QLabel(self)
        # self.heading_label.setStyleSheet("font-size: 25px; font-weight: bold;")  # Adjust font size and style as needed
        pixmap1 = Qt.QPixmap('drone.png')  # Replace 'logo.png' with your logo file
        pixmap_scaled1 = pixmap1.scaledToWidth(200)  # Adjust the width as needed
        self.heading_label.setPixmap(pixmap_scaled1)
        self.new_layout.addWidget(self.heading_label, 0, QtCore.Qt.AlignLeft)

        self.top_layout.addWidget(self.new_frame)
        self.button_layout = Qt.QHBoxLayout()

        
        # # Input Fields
        # self.input_label1 = Qt.QLabel("FREQUENCY RANGE:", self)
        # self.input_field1 = Qt.QLineEdit(self)
        # self.input_label2 = Qt.QLabel("SUB FREQUENCY RANGE:", self)
        # self.input_field2 = Qt.QLineEdit(self)
        # self.input_label3 = Qt.QLabel("RESOLUTION:", self)
        # self.input_field3 = Qt.QLineEdit(self)

        # self.top_layout.addWidget(self.input_label1)
        # self.top_layout.addWidget(self.input_field1)
        # self.top_layout.addWidget(self.input_label2)
        # self.top_layout.addWidget(self.input_field2)
        # self.top_layout.addWidget(self.input_label3)
        # self.top_layout.addWidget(self.input_field3)


        # Start/Stop Button
        self.start_stop_button = QtWidgets.QPushButton("Stop", self)
        self.start_stop_button.setStyleSheet("background-color: red; color: white; font-size: 16px;")
        self.start_stop_button.clicked.connect(self.handle_start_stop)
        self.start_stop_button.setFixedHeight(80)
        self.button_layout.addWidget(self.start_stop_button)

        # Pause Button
        self.pause_button = QtWidgets.QPushButton("Pause", self)
        self.pause_button.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        self.pause_button.clicked.connect(self.handle_pause)
        self.pause_button.setFixedHeight(80)
        self.button_layout.addWidget(self.pause_button)

        # Load Mission Button
        self.load_mission_button = QtWidgets.QPushButton("Load Mission", self)
        self.load_mission_button.setStyleSheet("background-color: purple; color: white; font-size: 16px;")
        self.load_mission_button.clicked.connect(self.handle_load_mission)
        self.load_mission_button.setFixedHeight(80)
        self.button_layout.addWidget(self.load_mission_button)

        # Save Mission Button
        self.save_mission_button = QtWidgets.QPushButton("Save Mission", self)
        self.save_mission_button.setStyleSheet("background-color: green; color: white; font-size: 16px;")
        self.save_mission_button.clicked.connect(self.handle_save_mission)
        self.save_mission_button.setFixedHeight(80)
        self.button_layout.addWidget(self.save_mission_button)

        # Add the button layout to the main layout
        self.top_layout.addLayout(self.button_layout)

        # After adding input fields, create a new frame for displaying .csv data
        self.csv_frame = Qt.QFrame()
       
        
       
        self.csv_layout = QVBoxLayout(self.csv_frame)
        self.top_layout.addWidget(self.csv_frame)

        # Create a table widget to display .csv data
        self.csv_table = Qt.QTableWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.csv_table)
        self.scroll_area.setWidgetResizable(True)
        self.csv_layout.addWidget(self.scroll_area)

        # Function to load .csv file
        # self.load_excel('file.xlsx')
        # self.load_csv('/home/usrp/Documents/usrp_python_codes/output.csv')
        self.csv_timer = Qt.QTimer()
        # self.csv_timer.timeout.connect(self.update_csv_column)
        self.csv_timer.timeout.connect(self.load_csv)
        self.csv_timer.start(1000)

        # Waterfall Sink
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            350000000, #fc
            640000000, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)

        ##################################################
        # Connections
        ##################################################


        # self.connect((self.iridium_iuchar_to_complex_2, 0), (self.qtgui_waterfall_sink_x_0, 0))

        self.include_drone_detection_checkbox = Qt.QCheckBox("Include Drone Detection")
        self.include_drone_detection_checkbox.setChecked(False)  
        self.top_layout.addWidget(self.include_drone_detection_checkbox)


        # self.run_python_script("off_mark.py") 

        ##################################################
        # Connections
        ##################################################

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()
        self.process.kill()
        event.accept()



    # def handle_start_stop(self):
    # # Logic to start or stop the process
    #     if self.is_running:
    #         self.stop()
    #         self.start_stop_button.setText("Start")
    #     else:
    #         self.start()
    #         self.start_stop_button.setText("Stop")
    #     self.is_running = not self.is_running

    # def handle_start_stop(self):
    #     self.csv_timer.stop()
    #     # self.timer.stop()
    #     # self.qtgui_waterfall_sink_x_0.set_update_time(10)

    def handle_start_stop(self):
        self.process.kill()
        self.closeEvent()
        # Logic to start or stop the process
        # if self.is_running:
        #     self.csv_timer.stop()
        #     self.timer.stop()
        #     self.qtgui_waterfall_sink_x_0.set_update_time(1e9)  # Set a very high update time to effectively stop updates
        #     self.start_stop_button.setText("Start")
        # else:
        #     self.csv_timer.start()
        #     self.timer.start()
        #     self.qtgui_waterfall_sink_x_0.set_update_time(0.10)  # Set the update time back to a reasonable value to resume updates
        #     self.start_stop_button.setText("Stop")
        # self.is_running = not self.is_running


    def handle_pause(self):
        # Logic to pause the process
        if self.is_running:
            self.csv_timer.stop()
            self.timer.stop()
            self.qtgui_waterfall_sink_x_0.set_update_time(1e9)  # Set a very high update time to effectively stop updates
            self.pause_button.setText("Resume")
        else:
            self.csv_timer.start()
            self.timer.start()
            self.qtgui_waterfall_sink_x_0.set_update_time(0.10)  # Set the update time back to a reasonable value to resume updates
            self.pause_button.setText("Pause")
        self.is_running = not self.is_running

    def handle_load_mission(self):
            pass
                
    def handle_save_mission(self):
        # Path of the original file to copy
        original_file_path = '/home/usrp/Music/final_files/output.csv'
        
        # Open a save file dialog to get the desired save location and filename from the user
        file_path, _ = Qt.QFileDialog.getSaveFileName(self, "Save Mission", "", "CSV Files (*.csv)")
        
        if file_path:
            if not file_path.endswith('.csv'):
                file_path += '.csv'  # Ensure the file has a .csv extension
            
            try:
                # Copy the original file to the new location with the new name
                shutil.copy(original_file_path, file_path)
                Qt.QMessageBox.information(self, "Success", f"File saved as: {file_path}")
            except Exception as e:
                Qt.QMessageBox.critical(self, "Error", f"Failed to save the file: {e}")

        
    def load_csv(self, file_path='/home/usrp/Music/final_files/output.csv'):
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            self.data = list(csv_reader)

        self.update_table()

    def update_table(self):
        current_data = self.data[self.current_index:self.current_index + self.chunk_size]
        max_column = 0
        max_row = len(current_data)
        
        if len(current_data) > 0:
            max_column = max(len(row) for row in current_data)
        
        self.csv_table.clearContents()
        self.csv_table.setRowCount(max_row)
        self.csv_table.setColumnCount(max_column)
        
        column_headers = ["time", "location", "frequency", "channel magnitude", "channel bandwidth"]
        self.csv_table.setHorizontalHeaderLabels(column_headers[:max_column])
        
        for i, row in enumerate(current_data):
            for j, cell_value in enumerate(row):
                item = QTableWidgetItem(str(cell_value))
                self.csv_table.setItem(i, j, item)

    def scroll_forward(self):
        if self.current_index + self.chunk_size < len(self.data):
            self.current_index += self.chunk_size
            self.update_table()

    def scroll_backward(self):
        if self.current_index - self.chunk_size >= 0:
            self.current_index -= self.chunk_size
            self.update_table()


    # def load_csv(self, file_path='/home/usrp/Music/final_files/output.csv'):


    #     with open(file_path, 'r', newline='') as csvfile:
    #         csv_reader = csv.reader(csvfile)
    #         data = list(csv_reader)

    #     data = data[-50:-2]
    #     max_column = 0
    #     max_row = len(data)
    #     if len(data) > 0:
    #         max_column = max(len(row) for row in data)
        
    #     self.csv_table.clearContents()
    #     self.csv_table.setRowCount(max_row)
    #     self.csv_table.setColumnCount(max_column)
        
    #     column_headers = ["time", "location", "frequency", "channel magnitude", "channel bandwidth"]
    #     self.csv_table.setHorizontalHeaderLabels(column_headers[:max_column])
        
    #     for i, row in enumerate(data):
    #         for j, cell_value in enumerate(row):
    #             item = QTableWidgetItem(str(cell_value))
    #             self.csv_table.setItem(i, j, item)








    def run_python_script(self, script_path):
        # pass
        self.process = subprocess.Popen(["python", script_path])
    

    
    

def main(top_block_cls=Testing, options=None):
    qapp = Qt.QApplication(sys.argv)
    dark_palette = DarkPalette()
    dark_palette.apply(qapp)
    tb = top_block_cls()
    tb.start()

    screen_resolution = Qt.QDesktopWidget().screenGeometry()
    width = screen_resolution.width() // 2
    height = screen_resolution.height() - 60
    # tb.resize(height, width)
    # tb.setFixedSize(height, width)
    tb.setFixedWidth(width)
    tb.setFixedHeight(height)
    left_pos = 0
    tb.move(left_pos, 0)

    # process = run_python_script("offline_marker.py")  
    
    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        
        Qt.QApplication.quit()



    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
