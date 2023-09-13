from PyQt5.QtCore import QObject, pyqtSignal, QThread, QEventLoop, QDateTime, QMetaObject, Q_ARG, Qt, pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import sys
import os
import subprocess
import tkinter as tk
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QLabel,
)
from PyQt5.uic import loadUi
import time
from PyQt5.QtCore import QTimer, QTime, QDate
import subprocess

from Ui_Work import JobsMainWindow
from Ui_Work import CustomWidget
from w3 import Ui_MainWindow3

from unittest.mock import Mock, patch

# Mock the board and busio modules if they're not available
# try:
import board
import busio
import serial
from adafruit_pn532.i2c import PN532_I2C
from escpos.printer import Serial
# except (ModuleNotFoundError, NotImplementedError):
#     board = Mock()
#     busio = Mock()
#     serial = Mock()
#     PN532_I2C = Mock()

import re
import json
import requests
from datetime import datetime
from dateutil.parser import parse

import sys
import pdfplumber

import uuid
import socket

# Mock the bluetooth module if it's not available
try:
    import bluetooth
except ModuleNotFoundError:
    bluetooth = Mock()
from ntplib import NTPClient

import xml.etree.ElementTree as ET

# proc1 = subprocess.Popen(["python", "/home/decas/ui/DecasUI_New/progress bar.py"])
# time.sleep(1)
# proc1.terminate()


class VirtualKeyboard(tk.Tk):
    def __init__(self, on_enter_callback):
        super().__init__()

        self.overrideredirect(True)

        self.title("Virtual Keyboard")
        self.configure(bg="#92EAD1")

        self.input_var = tk.StringVar()
        self.input_label = tk.Entry(
            self, textvariable=self.input_var, width=64, font=("Helvetica", "20")
        )
        self.input_label.pack(padx=5, pady=5)

        self.keys = [
            [
                "`",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "0",
                "-",
                "=",
                "Backspace",
            ],
            ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
            [
                "Caps Lock",
                "a",
                "s",
                "d",
                "f",
                "g",
                "h",
                "j",
                "k",
                "l",
                ";",
                "'",
                "Enter",
            ],
            ["Shift", "z", "x", "c", "v", "b", "n", "m", ",", ":", ".", "/", "Shift"],
            ["Ctrl", "Alt", " ", "Alt", "Ctrl"],
        ]

        self.shift_mappings = {
            "`": "~",
            "1": "!",
            "2": "@",
            "3": "#",
            "4": "$",
            "5": "%",
            "6": "^",
            "7": "&",
            "8": "*",
            "9": "(",
            "0": ")",
            "-": "_",
            "=": "+",
            "[": "{",
            "]": "}",
            "\\": "|",
            ";": ":",
            "'": '"',
            ",": "<",
            ".": ">",
            "/": "?",
        }

        self.caps_lock_on = False
        self.shift_on = False
        self.buttons = []  # to keep track of all the buttons
        
        self.on_enter_callback = on_enter_callback

        self.create_keyboard()

        # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the keyboard window width and height
        keyboard_width = self.winfo_reqwidth()
        keyboard_height = self.winfo_reqheight()

        # Calculate the x and y coordinates to center the keyboard window
        x = (screen_width // 2) - keyboard_width
        y = (screen_height // 2) - keyboard_height

        # Set the keyboard window to fullscreen
        # self.attributes("-fullscreen", True)
        # Set the keyboard window position
        self.geometry(f"+{20}+{y+50}")

    def create_keyboard(self):
        for row_index, row in enumerate(self.keys, start=1):
            # Set the background color same as the parent
            frame = tk.Frame(self, bg="#92EAD1")
            button_row = []
            for col_index, key in enumerate(row):
                if key in ("Backspace", "Tab"):
                    width = 16
                elif key in ("Enter", "Shift", "Caps Lock"):
                    width = 14
                elif key in (" ",):
                    width = 80
                else:
                    width = 2

                button = tk.Button(
                    frame,
                    text=key,
                    width=width,
                    height=2,
                    bg="black",  # background color
                    fg="white",   # text color
                    font=("Helvetica", 12, "bold"),  # Set the font size and style here
                    command=lambda k=key: self.press_key(k),
                )
                button.grid(
                    row=0, column=col_index, padx=1, pady=1
                )  # Use grid instead of pack
                button_row.append(button)

                # Distribute extra space evenly among columns
                frame.columnconfigure(col_index, weight=1)

            # fill both directions and expand within available space
            frame.pack(side="top", fill="both", padx=1, pady=1, expand=True)
            self.buttons.append(button_row)
        self.buttons.append(button_row)

    def press_key(self, key):
        if key == "Backspace":
            self.input_var.set(self.input_var.get()[:-1])
        elif key == "Enter":
            entered_text = self.input_var.get()
            print(f"Input: {entered_text}")
            self.input_var.set("")
            self.destroy()
            self.on_enter_callback(entered_text)
        elif key == "Caps Lock":
            self.caps_lock_on = not self.caps_lock_on
            self.update_keys()
        elif key == "Shift":
            self.shift_on = not self.shift_on
            self.update_keys()
            return
        elif key not in ("Ctrl", "Alt", "Tab"):
            if self.shift_on:
                key = self.shift_mappings.get(key, key.upper())
                self.shift_on = False

            char = key.upper() if self.caps_lock_on and key.isalpha() else key
            self.input_var.set(self.input_var.get() + char)
            self.update_keys()

    def update_keys(self):
        non_alpha_keys = ["Enter", "Backspace", "Ctrl", "Alt", "Shift", "Caps Lock", "Tab"]
        for row_keys, row_buttons in zip(self.keys, self.buttons):
            for key, button in zip(row_keys, row_buttons):
                if key.isalpha() and key not in non_alpha_keys:
                    if self.caps_lock_on or self.shift_on:
                        button.config(text=key.upper())
                    else:
                        button.config(text=key.lower())

    pass


class TimerThread(QThread):
    signal_time_to_update = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = None

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.signal_time_to_update)
        self.timer.start(1000)

        # Event loop needed for QThread.
        loop = QEventLoop()
        loop.exec_()


class SharedData(QObject):
    date_updated = pyqtSignal(str)
    time_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._date = QDate.currentDate().toString("dd-MM-yyyy")
        self._time = QTime.currentTime().toString("hh:mm:ss")

        self.timer_thread = TimerThread()
        self.timer_thread.signal_time_to_update.connect(self.update_system_time)
        self.timer_thread.start()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
        self.date_updated.emit(value)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self.time_updated.emit(value)

    def set_system_time(self, date, time):
        self.date = date.toString("dd-MM-yyyy")
        self.time = time.toString("hh:mm:ss")

    def update_time(self):
        current_time = QTime.fromString(self.time, "hh:mm:ss")
        current_time = current_time.addSecs(1)
        self.time = current_time.toString("hh:mm:ss")
        
    def update_system_time(self):
        # Parse the current date and time
        current_date = QDate.fromString(self.date, "dd-MM-yyyy")
        current_time = QTime.fromString(self.time, "hh:mm:ss")

        # Add one second
        current_datetime = QDateTime(current_date, current_time).addSecs(1)

        # Update date and time
        self.date = current_datetime.date().toString("dd-MM-yyyy")
        self.time = current_datetime.time().toString("hh:mm:ss")


def update_shared_data_time():
    shared_data.update_time()


shared_data = SharedData()


import subprocess

class MonoDecasProcessManager:
    def __init__(self):
        self.process = None
        
    def start_process(self):
        if self.process is None or self.process.poll() is not None:
            self.process = subprocess.Popen(["mono", "/home/decas/DecasPi.exe", "-c"])
        
    def terminate_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
        
    def restart_process(self):
        self.terminate_process()
        self.start_process()


class ReadyWindow(QMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        loadUi("/home/decas/ui/DecasUI_New/Ready.ui", self)
        # Create an instance of ProcessManager
        self.process_manager = process_manager

        self.SettingsWindow1_window = None

        # Set the window size
        self.resize(1024, 600)

        self.stacked_widget = stacked_widget
        self.setting.clicked.connect(self.open_next)
        self.connection.clicked.connect(self.open_connection)
        self.work.clicked.connect(self.open_work)

        self.directory_checker = DirectoryChecker()
        self.directory_checker.open_settings_window1_signal.connect(
            self.open_settings_window1
        )

        self.timer = QTimer()
        self.timer.timeout.connect(self.directory_checker.check_directory)
        self.timer.start(500)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_system_time)
        self.timer1.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def open_settings_window1(self):
        file_path = self.directory_checker.path_data
        try:
            self.SettingsWindow1_window = SettingsWindow1(self.stacked_widget, file_path, self.process_manager)
            self.stacked_widget.addWidget(self.SettingsWindow1_window)
            self.stacked_widget.setCurrentWidget(self.SettingsWindow1_window)
            self.timer.stop()
            self.hide()
        except (OSError, ValueError) as e:
            print(f"Error: {e}")
            self.process_manager.terminate_process()
            time.sleep(1)
            raise e

    def open_next(self):
        self.usb_window = SettingsWindow(self.stacked_widget, self.process_manager)
        self.usb_window.showFullScreen()
        self.hide()

    def open_connection(self):
        self.connection_window = connectionWindow(self.stacked_widget, self.process_manager)
        self.connection_window.showFullScreen()
        self.hide()

    def open_work(self):
        self.work_window = workWindow(self.stacked_widget, self.process_manager)
        self.work_window.showFullScreen()
        self.hide()

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(
            lambda entered_text: self.update_text_edit(text_edit, entered_text)
        )
        virtual_keyboard.mainloop()


class connectionWindow(QMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi("/home/decas/ui/DecasUI_New/connection.ui", self)
        self._translate = QtCore.QCoreApplication.translate

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)
        self.back.clicked.connect(self.go_back)
        # Connect radio buttons to a function
        self.r1.clicked.connect(self.on_selected)
        self.r2.clicked.connect(self.on_selected)
        self.r3.clicked.connect(self.on_selected)
        self.r4.clicked.connect(self.on_selected)

        self.read_config_xml()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def go_back(self):
        self.setting_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.setting_window.showFullScreen()
        self.hide()

    def on_selected(self):
        self.process_manager.terminate_process()
        if self.r1.isChecked():
            print("selected = 'WiFi'")
            self.edit_config_xml("true", "(none)")
        elif self.r2.isChecked():
            print("selected = 'Bluetooth'")
            self.edit_config_xml("false", "/dev/rfcomm0")
        elif self.r3.isChecked():
            print("selected = 'USB'")
            self.edit_config_xml("false", "/dev/ttyS0")
        elif self.r4.isChecked():
            print("selected = 'RS232'")
            self.edit_config_xml("false", "/dev/ttyS1")

    def read_config_xml(self):

        # Load and parse the XML file
        tree = ET.parse('/home/decas/config.xml')
        root = tree.getroot()

        # Find the ListenTCP element
        listen_tcp = root.find('ListenTCP')

        # Find the ComPort element
        com_port = root.find('ComPort')

        print(listen_tcp.text)
        print(com_port.text)

        if listen_tcp.text == "true" and com_port.text == "(none)":
            self.r1.setChecked(True)
            self.wifi.setText(
            self._translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">'
                + self.get_current_network().decode("utf-8").strip()
                + "</span></p></body></html>",
            )
        )
        elif listen_tcp.text == "false" and com_port.text == "/dev/rfcomm0":
            self.r2.setChecked(True)
        elif listen_tcp.text == "false" and com_port.text == "/dev/ttyS0":
            self.r3.setChecked(True)
        elif listen_tcp.text == "false" and com_port.text == "/dev/ttyS1":
            self.r4.setChecked(True)
    
    def get_current_network(self):
        cmd = ["iwgetid", "-r"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error is not None:
            print(f"Error: {error}")
            return None

        return output.strip()
    
    def edit_config_xml(self, tcp, port):
        self.tcp = tcp
        self.port = port

        # Load and parse the XML file
        tree = ET.parse('/home/decas/config.xml')
        root = tree.getroot()

        # Find and modify the ListenTCP element
        listen_tcp = root.find('ListenTCP')
        if listen_tcp is not None:
            listen_tcp.text = self.tcp

        # Find and modify the ComPort element
        com_port = root.find('ComPort')
        if com_port is not None:
            com_port.text = self.port

        # Convert the tree to a string
        xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")

        # Manually add the XML declaration and namespaces
        final_xml = '<?xml version="1.0"?>\n<Settings xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' + xml_str.split('<Settings>', 1)[1]

        # Write the final XML string to a file
        with open('/home/decas/config.xml', 'w') as f:
            f.write(final_xml)
        
        self.process_manager.start_process()


class workWindow(JobsMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.search_keyword = ""
        self._translate = QtCore.QCoreApplication.translate

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.show_jobs()
        self.search.clicked.connect(self.show_jobs)
        self.back.clicked.connect(self.go_back)
        
        self.search1.clicked.connect(
            lambda: self.open_virtual_keyboard(self.textEdit1)
        )

    def update_text_edit(self, text_edit1, entered_text):
        self.search_keyword = entered_text
        text_edit1.setHtml(
            self._translate(
                "self",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600;">' + self.search_keyword + '</span></p></body></html>',
            )
        )

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(
            lambda entered_text: self.update_text_edit(text_edit, entered_text)
            
        )
        virtual_keyboard.mainloop()

    def go_back(self):
        self.setting_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.setting_window.showFullScreen()
        self.hide()

    def show_jobs(self):
        self.clear_layout(self.scroll_layout)

        jobs = {}

        try:
            # Read the file
            with open("/home/decas/ui/DecasUI_New/my_jobs.json", "r") as f:
                jobs = json.load(f)  # This will give you a dictionary
                # Get the size of the dictionary
                size = len(jobs)
                print(f"The dictionary contains {size} key-value pairs.")
        except json.JSONDecodeError:
            print("File is not valid JSON")
        except FileNotFoundError:
            print("File '/home/decas/ui/DecasUI_New/my_jobs.json' not found.")

        if jobs:
            for key, value in jobs.items():
                print(value["job_title"])
                print("\n\n")
                print(value)
                print("\n\n")
                # Replace this with your actual data
                if self.search_keyword == "":
                    if value["data_sent"] is True:
                        widget = CustomWidget(key, value["job_title"], self.central_widget, False, self)
                    else:
                        widget = CustomWidget(key, value["job_title"], self.central_widget, True, self)
                    self.scroll_layout.addWidget(widget)
                else:
                    if (self.search_keyword in value["job_title"]["invoice"]) or (self.search_keyword in value["job_title"]["user_id"]) or (self.search_keyword in value["job_title"]["date_time"]) or (self.search_keyword in value["job_title"]["status"]):
                        if value["data_sent"] is True:
                            widget = CustomWidget(key, value["job_title"], self.central_widget, False, self)
                        else:
                            widget = CustomWidget(key, value["job_title"], self.central_widget, True, self)
                        self.scroll_layout.addWidget(widget)
                
                # self.job_title["invoice"] = info["Invoice Number"]
                # self.job_title["user_id"] = self.userID
                # self.job_title["date_time"] = info["Date"]
                # self.job_title["status"] = status

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_button_clicked(self, text):
        print(f"Button for '{text}' clicked")
        date_time = str(shared_data.date) + str(shared_data.time)
        self.processingThread = ProcessingThread("", "", date_time, True, text)
        self.processingThread.finished_signal.connect(self.onProcessingFinished)
        self.processingThread.progress_signal.connect(self.onProgress)
        self.processingThread.start()

    def onProgress(self, notification):
        _translate = QtCore.QCoreApplication.translate
        self.notification.setText(
            _translate(
                "stacked_widget",
                '<html><head/><body><p align="center"><span style=" background-color: black; color: white; font-size:22pt; font-weight:600;">'
                + notification
                + "</span></p></body></html>",
            )
        )

    def onProcessingFinished(self, retrieval_code, data_sent, error):
        self.code = retrieval_code
        self.data_sent = data_sent

        # Refresh the screen by showing the jobs again
        self.show_jobs()


class SettingsWindow(QMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        loadUi("/home/decas/ui/DecasUI_New/setting.ui", self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)
        self.stacked_widget = stacked_widget
        self.wifi_window = WifiWindow(self.stacked_widget, self.process_manager)
        self.back.clicked.connect(self.go_back)
        # self.usb.clicked.connect(self.open_usb)
        self.bluetooth.clicked.connect(self.open_bluetooth)
        self.wifi.clicked.connect(self.open_wifi)
        self.about.clicked.connect(self.open_about)
        # self.rs.clicked.connect(self.open_rs)

        self.shared_data = shared_data
        self.dateEdit.setDate(QDate(2023, 1, 1))
        self.timeEdit.setTime(QTime(00, 00, 00))
        # Connect signals to slots
        self.dateEdit.dateChanged.connect(self.update_date)
        self.timeEdit.timeChanged.connect(self.update_time)

        self.checkBox.stateChanged.connect(self.enable_edit_date_time)

    def enable_edit_date_time(self, state):
        if state == 2:
            self.dateEdit.setEnabled(False)
            self.timeEdit.setEnabled(False)

            self.update_shared_data(shared_data)

        elif state == 0:

            self.dateEdit.setEnabled(True)
            self.timeEdit.setEnabled(True)

    def update_shared_data(self, shared_data):
        ntp_time = self.get_ntp_time()
        ntp_datetime = datetime.fromtimestamp(ntp_time)
        ntp_date = QDate(ntp_datetime.year, ntp_datetime.month, ntp_datetime.day)
        ntp_time = QTime(ntp_datetime.hour, ntp_datetime.minute, ntp_datetime.second)
        shared_data.set_system_time(ntp_date, ntp_time)

    def get_ntp_time(self, host="pool.ntp.org"):
        client = NTPClient()
        response = client.request(host)
        return response.tx_time

    def update_date(self, date):
        self.shared_data.date = date.toString("dd-MM-yyyy")

    def update_time(self, time):
        self.shared_data.time = time.toString("hh:mm:ss")

    def go_back(self):
        self.setting_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.setting_window.showFullScreen()
        self.hide()

    def open_wifi(self):
        # Pass 'self.stacked_widget' as an argument when creating a new WifiWindow instance
        self.usb_window = WifiWindow(self.stacked_widget, self.process_manager)
        self.usb_window.showFullScreen()
        self.hide()

    def open_about(self):
        self.about_window = aboutWindow(self.stacked_widget, self.process_manager)
        self.about_window.showFullScreen()
        self.hide()

    # def open_rs(self):
    #     self.rs_window = RSWindow(self.stacked_widget)
    #     self.rs_window.showFullScreen()
    #     self.hide()

    # def open_usb(self):
    #     self.usb_window = usbWindow(self.stacked_widget)
    #     self.usb_window.showFullScreen()
    #     self.hide()

    def open_bluetooth(self):
        self.usb_window = bluetoothWindow(self.stacked_widget, self.process_manager)
        self.usb_window.showFullScreen()
        self.hide()


class aboutWindow(QMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        self.stacked_widget = stacked_widget
        self._translate = QtCore.QCoreApplication.translate
        loadUi("/home/decas/ui/DecasUI_New/About.ui", self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.mac.setText(
            self._translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">'
                + self.get_mac_address()
                + "</span></p></body></html>",
            )
        )
        self.ip.setText(
            self._translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">'
                + self.get_local_ip_address("8.8.8.8")
                + "</span></p></body></html>",
            )
        )
        self.back.clicked.connect(self.go_back)
        # Google's DNS as target to get the local ip
        print(self.get_local_ip_address("8.8.8.8"))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def go_back(self):
        self.setting_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.setting_window.showFullScreen()
        self.hide()

    def get_mac_address(self):
        # mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        # mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        # return mac

        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line[0:6] == "Serial":
                    return line.split(":")[1].strip()
        return "Unknown"

    def get_local_ip_address(self, target):
        ip_address = ""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((target, 1))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception as e:
            print("Error: %s" % e)
        return ip_address


class WifiWindow(QMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        loadUi("/home/decas/ui/DecasUI_New/wifiset.ui", self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.network_ssid = ""
        self.network_password = ""
        self.stacked_widget = stacked_widget
        self._translate = QtCore.QCoreApplication.translate
        self.confirm.clicked.connect(self.done)
        self.back.clicked.connect(self.go_back)

        self.password.clicked.connect(
            lambda: self.open_virtual_keyboard(self.textEdit1)
        )
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

        self.status.setText(
            self._translate(
                "wifisetting",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">Scanning...Please wait!</span></p></body></html>',
            )
        )
        self.discovery_thread = WiFiDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(self.add_wifi_item)
        self.discovery_thread.start()

        self.network_ssid = self.ssid.itemText(0)

        self.refresh.clicked.connect(self.refresh_wifi_scan)
        # Connect the combo box's activated signal to a slot function
        self.ssid.activated[str].connect(self.on_combobox_activated)

    def refresh_wifi_scan(self):
        self.ssid.clear()
        self.status.setText(
            self._translate(
                "wifisetting",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">Scanning...Please wait!</span></p></body></html>',
            )
        )
        self.discovery_thread = WiFiDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(self.add_wifi_item)
        self.discovery_thread.start()

    def add_wifi_item(self, name, devices):
        self.status.setText(
            self._translate(
                "wifisetting",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">'
                + devices
                + " network(s) found</span></p></body></html>",
            )
        )
        self.ssid.addItem(name)

    def on_combobox_activated(self, text):
        self.network_ssid = text
        print(f"Selected option: {text}")

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def done(self):
        self.network_password = str(self.textEdit1.toPlainText())
        print(self.network_password)

        if self.network_ssid != "" and self.network_password != "":
            self.connect_wifi(self.network_ssid, self.network_password)

    def get_current_network(self):
        cmd = ["iwgetid", "-r"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error is not None:
            print(f"Error: {error}")
            return None

        return output.strip()

    def get_ssid_psk(self, config):
        ssid_pattern = 'ssid="(.+?)"'
        psk_pattern = 'psk="(.+?)"'

        ssid = re.search(ssid_pattern, config)
        psk = re.search(psk_pattern, config)

        if ssid and psk:
            return ssid.group(1), psk.group(1)
        else:
            return None, None

    def connect_wifi(self, new_network_ssid, new_network_password):
        # Save the current network configuration
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as wifi_config:
            current_config = wifi_config.read()
            current_ssid, current_psk = self.get_ssid_psk(current_config)

            new_config = current_config
            new_config = new_config.replace(current_ssid, new_network_ssid)
            new_config = new_config.replace(current_psk, new_network_password)

            print(current_config)
            print("\n")
            print(new_config)

        # Write the new network configuration to wpa_supplicant.conf
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as wifi_config:
            wifi_config.truncate(0)
            wifi_config.write(new_config)
            wifi_config.close()

        # Restart the wpa_supplicant service to connect to the new network
        # cmd = ["sudo", "systemctl", "restart", "wpa_supplicant"]
        # process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # output, error = process.communicate()

        # if error is not None:
        #     print(f"Error: {error}")

        cmd = ["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error is not None:
            print(f"Error: {error}")

        # Check if the connection was successful
        time.sleep(10)  # Wait for the connection to establish

        new_ssid = self.get_current_network().decode("utf-8").strip()

        if new_network_ssid != new_ssid:
            print(
                "Failed to connect to the new network. Reverting to the previous network configuration."
            )

            # Revert to the previous network configuration
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi_config:
                wifi_config.truncate(0)
                wifi_config.write(current_config)
                wifi_config.close()

            # Restart the wpa_supplicant service to reconnect to the previous network
            cmd = ["sudo", "systemctl", "restart", "wpa_supplicant"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                print(f"Error: {error}")

            cmd = ["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                print(f"Error: {error}")

    def go_back(self):
        self.usb_window = SettingsWindow(self.stacked_widget, self.process_manager)
        self.usb_window.showFullScreen()
        self.hide()

    def update_text_edit(self, text_edit, entered_text):
        text_edit.setPlainText(entered_text)

    def open_virtual_keyboard(self, text_edit):
        virtual_keyboard = VirtualKeyboard(
            lambda entered_text: self.update_text_edit(text_edit, entered_text)
        )
        virtual_keyboard.mainloop()


# class RSWindow(QMainWindow):
#     def __init__(self, stacked_widget):
#         super().__init__()
#         self.stacked_widget = stacked_widget
#         loadUi("RSset.ui", self)

#         # Set the window size
#         self.resize(1024, 600)

#         self.back.clicked.connect(self.go_back)
#         self.address.clicked.connect(lambda: self.open_virtual_keyboard(self.textEdit))
#         self.baudrate.addItems(["9600", "19200", "38400", "115200"])
#         self.parity.addItems(["None", "Even", "Odd"])
#         # Connect the combo box's activated signal to a slot function
#         self.baudrate.activated[str].connect(self.on_combobox_activated)

#         self.parity.activated[str].connect(self.on_combobox_activated1)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_system_time)
#         self.timer.start(1000)

#     def update_system_time(self):
#         current_time = shared_data.time
#         self.time.setPlainText(f" {current_time}")
#         self.date.setPlainText(f" {shared_data.date}")

#     def on_combobox_activated(self, text):
#         print(f"Selected option: {text}")

#     def on_combobox_activated1(self, text):
#         print(f"Selected option: {text}")

#     def go_back(self):
#         self.usb_window = SettingsWindow(self.stacked_widget, self.process_manager)
#         self.usb_window.showFullScreen()
#         self.hide()

#     def update_text_edit(self, text_edit, entered_text):
#         text_edit.setPlainText(entered_text)

#     def open_virtual_keyboard(self, text_edit):
#         virtual_keyboard = VirtualKeyboard(
#             lambda entered_text: self.update_text_edit(text_edit, entered_text)
#         )
#         virtual_keyboard.mainloop()


# class usbWindow(QMainWindow):
#     def __init__(self, stacked_widget):
#         super().__init__()
#         self.stacked_widget = stacked_widget
#         loadUi("usbset.ui", self)

#         # Set the window size
#         self.resize(1024, 600)

#         self.back.clicked.connect(self.go_back)
#         self.comport.addItems(["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"])

#         # Connect the combo box's activated signal to a slot function
#         self.comport.activated[str].connect(self.on_combobox_activated)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_system_time)
#         self.timer.start(1000)

#     def update_system_time(self):
#         current_time = shared_data.time
#         self.time.setPlainText(f" {current_time}")
#         self.date.setPlainText(f" {shared_data.date}")

#     def on_combobox_activated(self, text):
#         print(f"Selected option: {text}")

#     def go_back(self):
#         self.usb_window = SettingsWindow(self.stacked_widget, self.process_manager)
#         self.usb_window.showFullScreen()
#         self.hide()

#     def update_text_edit(self, entered_text):
#         self.textEdit.setPlainText(entered_text)

#     def open_virtual_keyboard(self):
#         virtual_keyboard = VirtualKeyboard(self.update_text_edit)
#         virtual_keyboard.mainloop()


class bluetoothWindow(QMainWindow):
    def __init__(self, stacked_widget, process_manager):
        super().__init__()
        self.stacked_widget = stacked_widget
        self._translate = QtCore.QCoreApplication.translate
        loadUi("/home/decas/ui/DecasUI_New/bluetooth.ui", self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.status.setText(
            self._translate(
                "bluetooth",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">Scanning...Please wait!</span></p></body></html>',
            )
        )
        self.discovery_thread = BluetoothDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(self.add_bluetooth_item)
        self.discovery_thread.start()

        self.refresh.clicked.connect(self.refresh_bluetooth_scan)
        self.back.clicked.connect(self.go_back)
        # Connect the combo box's activated signal to a slot function
        self.bluetooth1.activated[str].connect(self.on_combobox_activated)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def refresh_bluetooth_scan(self):
        self.bluetooth1.clear()
        self.status.setText(
            self._translate(
                "bluetooth",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">Scanning...Please wait!</span></p></body></html>',
            )
        )
        self.discovery_thread = BluetoothDiscoveryThread(self)
        self.discovery_thread.device_discovered.connect(self.add_bluetooth_item)
        self.discovery_thread.start()

    def add_bluetooth_item(self, name, devices):
        self.status.setText(
            self._translate(
                "bluetooth",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">'
                + devices
                + " devices found</span></p></body></html>",
            )
        )
        self.bluetooth1.addItem(name)

    def on_combobox_activated(self, text):
        print(f"Selected option: {text}")

    def go_back(self):
        self.usb_window = SettingsWindow(self.stacked_widget, self.process_manager)
        self.usb_window.showFullScreen()
        self.hide()

    def update_text_edit(self, entered_text):
        self.textEdit.setPlainText(entered_text)

    def open_virtual_keyboard(self):
        virtual_keyboard = VirtualKeyboard(self.update_text_edit)
        virtual_keyboard.mainloop()


class WiFiDiscoveryThread(QThread):
    device_discovered = pyqtSignal(str, str)

    def run(self):
        interface = "wlan0"  # The default interface for Raspberry Pi's WiFi
        cmd = f"iwlist {interface} scan"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        lines = output.split("\n")
        networks = []

        for line in lines:
            line = line.strip()
            if "ESSID" in line:
                networks.append(line.split(":")[1].strip('"'))
        devices = str(len(networks))

        for network in networks:
            ssid = network
            self.device_discovered.emit(ssid, devices)


class BluetoothDiscoveryThread(QThread):
    device_discovered = pyqtSignal(str, str)

    def run(self):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices = str(len(nearby_devices))
        print("Found {} devices.".format(len(nearby_devices)))
        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))
            self.device_discovered.emit(name, devices)


# Define similar classes for WifiWindow, RsWindow, and SetWindow
class Blinker(QObject):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.timer = QTimer()
        self.timer.timeout.connect(self._toggle_visibility)

    @pyqtSlot(int, int)
    def start_blinking(self, interval, duration):
        self.timer.start(interval)
        QTimer.singleShot(duration, self.stop_blinking)

    @pyqtSlot()
    def stop_blinking(self):
        self.timer.stop()
        self.label.show()  # ensure it's visible when stop

    def _toggle_visibility(self):
        if self.label.isVisible():
            self.label.hide()
        else:
            self.label.show()


class ScanThread(QThread):
    foundUserID = pyqtSignal(str)

    def __init__(
        self,
        ser,
        pn532,
        start_scan_command_bytes,
        stop_scan_command_bytes,
        rfid_label,
        qr_label,
    ):
        super().__init__()
        self.ser = ser
        self.pn532 = pn532
        self.start_scan_command_bytes = start_scan_command_bytes
        self.stop_scan_command_bytes = stop_scan_command_bytes
        self.rfid_blinker = Blinker(rfid_label)
        self.qr_blinker = Blinker(qr_label)
        self.scanned = False
        self._isScanning = True
        self._isRunning = False

        try:
            if not self.ser.isOpen():
                self.ser.open()
        except Exception as e:
            print(f"Failed to open serial port in __init__: {e}")

    def blink_and_sleep(self, blinker):
        QMetaObject.invokeMethod(
            blinker,
            "start_blinking",
            Qt.QueuedConnection,
            Q_ARG(int, 300),
            Q_ARG(int, 3000),
        )
        time.sleep(3)

    def run(self):
        if self._isRunning:
            return

        self._isRunning = True
        try:
            if not self.ser.isOpen():
                self.ser.open()
        except Exception as e:
            print(f"Failed to open serial port in __init__: {e}")
        self.ser.write(self.start_scan_command_bytes)

        while self._isScanning:
            try:
                # data = self.ser.readline().decode("utf-8").strip()
                # print("\nSerial Data: " + data + "\n")
                # if data != "31":
                data = self.ser.readline().decode("utf-8").strip()
                print("\nSerial Data: " + data + "\n")
                if data and "31" not in data:
                    print("\nSerial Data: " + data + "\n")
                    self.blink_and_sleep(self.qr_blinker)
                    self.foundUserID.emit(data)
                    self.scanned = True
                    self.ser.write(self.stop_scan_command_bytes)

                uid = self.pn532.read_passive_target(timeout=0.1)
                if uid is not None:
                    self.blink_and_sleep(self.rfid_blinker)
                    uid_string = "".join([hex(i)[2:].zfill(2) for i in uid])
                    self.foundUserID.emit(uid_string)
                    self.scanned = True
                    self.ser.write(self.stop_scan_command_bytes)

            except Exception as e:
                print(f"Error reading from serial port in run: {e}")

            if self.scanned:
                break

        self.cleanup()

    def restart(self):
        self.stop()
        self._isScanning = True
        self.scanned = False
        self.start()

    def stop(self):
        self._isScanning = False

    def cleanup(self):
        self._isRunning = False
        if self.ser.isOpen():
            try:
                self.ser.write(self.stop_scan_command_bytes)
                time.sleep(0.1)
                self.ser.close()
            except Exception as e:
                print(f"Error closing serial port in cleanup: {e}")

        QMetaObject.invokeMethod(
            self.rfid_blinker, "stop_blinking", Qt.QueuedConnection
        )
        QMetaObject.invokeMethod(self.qr_blinker, "stop_blinking", Qt.QueuedConnection)


class ProcessingThread(QThread):
    # Signal emitted when thread finishes
    finished_signal = pyqtSignal(str, bool, str)
    # Signal emitted for UI updates
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path, userID, date_time, retry=False, retry_text=""):
        super().__init__()
        self._isRunning = False
        self.file_path = file_path
        self.userID = userID
        self.date_time = date_time
        self.retry = retry
        self.retry_text = retry_text
        self.data_sent = False
        self.job_title = {}
        self.receiver = ""
        self.company_name = ""
        self.company_address = ""
        self.company_phone = ""
        self.date = ""
        self.receipt_number = ""
        self.payload = ""
        self.response = ""
        self.response_code = ""
        self.url = "http://staging.repslips.com/api/send-data"
        # self.url = "http://filesharing.n2rtech.com/api/send-data?"

    def run(self):
        if not self._isRunning:
            self._isRunning = True
            self.deviceID = self.get_mac_address()

            if self.retry is not True:
                self.progress_signal.emit("Please wait!  Processing receipt...")

                self.retrieval_code = ""

                try:
                    result = self.pdf_to_table_data(self.file_path)
                    print("\n\n")
                    print(result)
                    print("\n\n")

                    receipt_text = ""
                    for i, row in enumerate(result):
                        row['quantity'] = row['quantity'].replace(",", "")
                        row['price'] = row['price'].replace(",", "")
                        row['tax'] = row['tax'].replace(",", "")
                        row['discount'] = row['discount'].replace(",", "")
                        row['total'] = row['total'].replace(",", "")
                        print(f"item: {row['item']}, quantity: {row['quantity']}, price: {row['price']}, tax: {row['tax']}, discount: {row['discount']}, total: {row['total']}")

                        receipt_text += row['#'] + " " + row['item'] + " " + row['quantity'] + " " + row['price'] + " " + row['total'] + "\n"

                    receipt_info = self.pdf_to_text(self.file_path)
                    print("\n\n")
                    print(receipt_info)
                    print("\n\n")

                    info = self.extract_info(receipt_info)
                    if "Tax Number" in info:
                        print(f"Tax Number: {info['Tax Number']}")
                    else:
                        info['Tax Number'] = 'Nil'
                    if "Phone Number" in info:
                        print(f"Phone Number: {info['Phone Number']}")
                    else:
                        info['Phone Number'] = 'Nil'
                    if "Email" in info:
                        print(f"Email: {info['Email']}")
                    else:
                        info['Email'] = 'Nil'
                    if "Invoice Number" in info:
                        print(f"Invoice Number: {info['Invoice Number']}")
                    else:
                        info['Invoice Number'] = 'Nil'
                    if "Date" in info:
                        print(f"Date: {info['Date']}")
                    else:
                        info['Date'] = 'Nil'
                    print("\n\n")

                    address = re.findall(
                        r"^(.*(?:Street|Avenue|Road|Lane).*\d{4}?.*)$", receipt_info, re.MULTILINE
                    )
                    if address:
                        address = address[0]
                    else:
                        address = " "
                    print(address)

                    api_data = self.items_to_api_format(result)
                    print(api_data)
                    print("\n\n")

                    print(self.userID)
                    print("\n\n")

                    print(self.deviceID)
                    print("\n\n")

                    self.progress_signal.emit("Sending data to REPSLIPS server...")

                    # (data, receiver, company_name, company_address, company_phone, date, device_id, receipt_number)
                    get_response = self.send_api_data(
                        api_data,
                        self.userID,
                        "N2R Technologies3",
                        address,
                        info["Phone Number"],
                        info["Date"],
                        self.deviceID,
                        info["Invoice Number"],
                    )
                    self.decode_response(get_response)

                    if self.data_sent is True:
                        status = "Success"
                    else:
                        status = "Failed. " + str(self.parsed_data["response"])

                    self.job_title["invoice"] = info["Invoice Number"]
                    self.job_title["user_id"] = self.userID
                    self.job_title["date_time"] = info["Date"]
                    self.job_title["status"] = status
                    print("\n\n")
                    print(self.job_title)
                    print("\n\n")

                    self.update_jobs_dict()

                    # Emit signal when processing is done
                    self.finished_signal.emit(
                        self.retrieval_code, self.data_sent, self.response_message
                    )
                except Exception as e:
                    print(f"Error: {e}")
                    print("\n")
                    print("Error! Unsupported PDF")
                    raise e
                    # self.progress_signal.emit("Error! Unsupported PDF")
                    # time.sleep(3)
                    # # Emit signal when processing is done
                    # self.finished_signal.emit(
                    #     "", self.data_sent, "error_PDF"
                    # )

            else:
                try:
                    # Read the file
                    with open("/home/decas/ui/DecasUI_New/my_jobs.json", "r") as f:
                        jobs = json.load(f)  # This will give you a dictionary
                        # Get the size of the dictionary
                        size = len(jobs)
                        print(f"The dictionary contains {size} key-value pairs.")
                        print(f"Dictionary: '{jobs[self.retry_text]}'")

                        payload = jobs[self.retry_text]["payload"]

                        files = []
                        headers = {}

                        response = requests.request(
                            "POST", self.url, headers=headers, data=payload, files=files
                        )

                        self.decode_response(response.text)

                        # self.data_sent
                        self.job_title = jobs[self.retry_text]["job_title"]
                        self.receiver = jobs[self.retry_text]["receiver"]
                        self.company_name = jobs[self.retry_text]["company_name"]
                        self.company_address = jobs[self.retry_text]["company_address"]
                        self.company_phone = jobs[self.retry_text]["company_phone"]
                        self.date = jobs[self.retry_text]["date"]
                        self.receipt_number = jobs[self.retry_text]["receipt_number"]
                        self.payload = payload
                        self.response = response.text
                        # self.response_code

                        self.update_jobs_dict()

                        # Emit signal when processing is done
                        self.finished_signal.emit(
                            "", self.data_sent, self.response_message
                        )

                except json.JSONDecodeError:
                    print("File is not valid JSON")
                except FileNotFoundError:
                    print("File '/home/decas/ui/DecasUI_New/my_jobs.json' not found.")

            self._isRunning = False

    def get_mac_address(self):
        # mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        # mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        # return mac

        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line[0:6] == "Serial":
                    return line.split(":")[1].strip()
        # return "Unknown"

    def pdf_to_table_data(self, file_path):
        data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extract the tables from the page
                tables = page.extract_tables()

                for table in tables:
                    # convert headers to lowercase and replace headers containing "price" with "price"
                    headers = ['price' if 'price' in header.lower() else header.lower() for header in table[0]]
                    for row in table[1:]:
                        if len(row) >= 4:  # check if the row has at least 4 columns
                            row_data = {headers[i]: value.replace("---", "0") for i, value in enumerate(row)}
                            data.append(row_data)
            
        return data

    def pdf_to_text(self, file_path):
        data = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extract the text from the page
                data += page.extract_text()

        return data

    def extract_info(self, text_info):
        # dictionary to hold the results
        info = {}

        # patterns for each of the data
        tax_pattern = r"Tax No\.:\s(\d+)"
        phone_pattern = r"Phone:\s(\d+)"
        email_pattern = r"Email:\s(\S+)"
        invoice_pattern = r'Invoice No.:\s(.+)'
        date_pattern = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2} \w{3}, \d{4}|\d{1,2},\w{3},\d{4}|\d{1,2} \w{3} \d{4})\b"

        # search for each pattern and add to dictionary
        tax_search = re.search(tax_pattern, text_info)
        if tax_search:
            info["Tax Number"] = tax_search.group(1)

        phone_search = re.search(phone_pattern, text_info)
        if phone_search:
            info["Phone Number"] = phone_search.group(1)

        email_search = re.search(email_pattern, text_info)
        if email_search:
            info["Email"] = email_search.group(1)

        invoice_search = re.search(invoice_pattern, text_info)
        if invoice_search:
            info["Invoice Number"] = invoice_search.group(1)

            # Extract only numbers from the text
            info["Invoice Number"] = "".join(filter(str.isdigit, info["Invoice Number"]))

            # If the length of the numbers string is more than 9 characters
            if len(info["Invoice Number"]) > 9:
                # Trim the numbers string to the first 9 characters
                info["Invoice Number"] = info["Invoice Number"][:9]
        
        match = re.search(date_pattern, str(text_info))
        if match:
            try:
                date = parse(match.group())
                info["Date"] = date.date().isoformat()
            except ValueError:
                print(f"Could not parse date: {match.group()}")

        return info


    def items_to_api_format(self, result):
        api_data = {}

        for i, row in enumerate(result):
            api_data[f"products[{i}][product]"] = row["item"]
            api_data[f"products[{i}][quantity]"] = str(row["quantity"])
            api_data[f"products[{i}][price]"] = str(row["price"])
            api_data[f"products[{i}][tax]"] = row["tax"]
            api_data[f"products[{i}][total]"] = str(row["total"])
        return api_data

    def send_api_data(
        self,
        data,
        receiver,
        company_name,
        company_address,
        company_phone,
        date,
        device_id,
        receipt_number,
    ):
        payload = {
            "receiver": receiver,
            "company_name": company_name,
            "company_address": company_address,
            "company_phone": company_phone,
            "date": date,
            "device_id": device_id,
            "receipt_number": receipt_number,
        }

        payload.update(data)
        files = []
        headers = {}

        response = requests.request(
            "POST", self.url, headers=headers, data=payload, files=files
        )

        self.receiver = receiver
        self.company_name = company_name
        self.company_address = company_address
        self.company_phone = company_phone
        self.date = date
        self.receipt_number = receipt_number
        self.payload = payload
        self.response = response.text
        return response.text

    def decode_response(self, response_text):
        # Parse the JSON string into a Python dictionary
        self.parsed_data = json.loads(response_text)

        # Check if 'success' or 'error' key exists in the parsed data
        if "success" in self.parsed_data:
            self.response_code = "success"
            self.response_message = self.parsed_data["success"]
            self.data_sent = True
            print("Data uploaded successfully to API.")

        elif "error" in self.parsed_data:
            error = self.parsed_data["error"]
            self.response_code = "error: " + str(error)
            self.response_message = self.parsed_data["response"]

            # Print the error message
            print(f"Error: {error}")
            print(f"Response: {self.response_message}")

        else:
            print("Unexpected response format.")

        if "CODE" in self.parsed_data:
            code = self.parsed_data["CODE"]

            # Print the extracted values
            print(f"CODE: {code}")
            self.retrieval_code = str(code)

    def update_jobs_dict(self):
        jobs = {}
        i = 0

        try:
            # Read the file
            with open("/home/decas/ui/DecasUI_New/my_jobs.json", "r") as f:
                jobs = json.load(f)  # This will give you a dictionary
                # Get the size of the dictionary
                size = len(jobs)
                print(f"The dictionary contains {size} key-value pairs.")
        except json.JSONDecodeError:
            print("File is not valid JSON")
        except FileNotFoundError:
            print("File '/home/decas/ui/DecasUI_New/my_jobs.json' not found.")

        if jobs:
            # Get the last key-value pair added
            last_key, last_value = next(reversed(jobs.items()))
            print(f"Last key: {last_key}, last value: {last_value}")
            i = int(last_key)

        if self.retry is True:
            # Removing an item using del
            del jobs[self.retry_text]

        i += 1

        if i != 0:
            jobs[i] = {}
            jobs[i]["data_sent"] = self.data_sent
            jobs[i]["job_title"] = self.job_title
            jobs[i]["receiver"] = self.receiver
            jobs[i]["company_name"] = self.company_name
            jobs[i]["company_address"] = self.company_address
            jobs[i]["company_phone"] = self.company_phone
            jobs[i]["date"] = self.date
            jobs[i]["receipt_number"] = self.receipt_number
            jobs[i]["payload"] = self.payload
            jobs[i]["response"] = self.response
            jobs[i]["response_code"] = self.response_code

        # print(jobs)
        # Write the updated dictionary back to the file
        with open("/home/decas/ui/DecasUI_New/my_jobs.json", "w") as f:
            json.dump(jobs, f)


class SettingsWindow1(QMainWindow, Ui_MainWindow3):
    def __init__(self, stacked_widget, file_path, process_manager):
        super().__init__()
        self.setupUi(self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.stacked_widget = stacked_widget
        self.file_path = file_path
        self.next1.clicked.connect(self.open_keyboard)
        self.Retreive.clicked.connect(self.print_retrieval_code)

        # Barcode
        self.serial_port = "/dev/ttySC0"
        self.baud_rate = 9600
        start_scan_command = "7E 00 08 01 00 02 01 AB CD"
        self.start_scan_command_bytes = bytes.fromhex(
            start_scan_command.replace(" ", "")
        )
        stop_scan_command = "7E 00 08 01 00 02 00 AB CD"
        self.stop_scan_command_bytes = bytes.fromhex(stop_scan_command.replace(" ", ""))

        # PN532
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(i2c, debug=False)
        self.pn532.SAM_configuration()

        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=0.5)

        self.scanThread = ScanThread(
            self.ser,
            self.pn532,
            self.start_scan_command_bytes,
            self.stop_scan_command_bytes,
            self.RFID_Icon,
            self.QR_Icon,
        )
        self.scanThread.foundUserID.connect(self.processUserID)
        self.scanThread.start()

        self.numeric_keyboard = NumericKeyboard(
            self, self.stacked_widget, self, self.scanThread, self.file_path
        )
        self.stacked_widget.addWidget(self.numeric_keyboard)

    def update_user_id(self, user_id=""):
        if user_id != "":
            self.userID = user_id
            date_time = str(shared_data.date) + str(shared_data.time)
            self.processingThread = ProcessingThread(self.file_path, self.userID, date_time)
            self.processingThread.finished_signal.connect(self.onProcessingFinished)
            self.processingThread.progress_signal.connect(self.onProgress)
            self.processingThread.start()

    def processUserID(self, scanned_data):
        self.userID = scanned_data
        print("Found a User ID:", scanned_data)
        date_time = str(shared_data.date) + str(shared_data.time)
        self.processingThread = ProcessingThread(self.file_path, self.userID, date_time)
        self.processingThread.finished_signal.connect(self.onProcessingFinished)
        self.processingThread.progress_signal.connect(self.onProgress)
        self.processingThread.start()

    def onProgress(self, notification):
        _translate = QtCore.QCoreApplication.translate
        self.notification.setText(
            _translate(
                "stacked_widget",
                '<html><head/><body><p align="center"><span style=" background-color: black; color: white; font-size:22pt; font-weight:600;">'
                + notification
                + "</span></p></body></html>",
            )
        )
        if notification == "Sending data to REPSLIPS server...":
            self.timer = QTimer()
            self.timer.timeout.connect(self.go_home)
            self.timer.start(2000)

    def onProcessingFinished(self, retrieval_code, data_sent, error):
        self.code = retrieval_code
        self.data_sent = data_sent

        try:
            subprocess.run(["sudo", "rm", self.file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        print("Processing finished!")
        print(retrieval_code)

        if self.data_sent and error != "error_PDF":
            self.DataSentWindow_window = DataSentWindow(
                self.file_path, self.stacked_widget, self.process_manager
            )
            self.stacked_widget.addWidget(self.DataSentWindow_window)
            self.stacked_widget.setCurrentWidget(self.DataSentWindow_window)
        else:
            _translate = QtCore.QCoreApplication.translate
            self.notification.setText(
                _translate(
                    "stacked_widget",
                    '<html><head/><body><p align="center"><span style=" background-color: black; color: white; font-size:22pt; font-weight:600;">'
                    + error
                    + "</span></p></body></html>",
                )
            )
            time.sleep(3)
            self.timer = QTimer()
            self.timer.timeout.connect(self.go_home)
            self.timer.start(5000)

    def go_home(self):
        self.timer.stop()

        while self.stacked_widget.count() > 0:
            widget_to_remove = self.stacked_widget.widget(0)  # get the widget
            self.stacked_widget.removeWidget(
                widget_to_remove
            )  # remove it from stacked_widget
            widget_to_remove.setParent(
                None
            )  # optional: set its parent to None so it gets deleted

        self.ReadyWindow_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.stacked_widget.addWidget(self.ReadyWindow_window)
        self.stacked_widget.setCurrentWidget(self.ReadyWindow_window)

    def open_keyboard(self):
        self.scanThread.stop()
        index = self.stacked_widget.indexOf(self.numeric_keyboard)
        self.stacked_widget.setCurrentIndex(index)

    def print_retrieval_code(self):
        self.scanThread.stop()
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=0.5)
        self.ser.write(self.stop_scan_command_bytes)

        self.userID = ""
        date_time = str(shared_data.date) + str(shared_data.time)
        self.processingThread = ProcessingThread(self.file_path, self.userID, date_time)
        self.processingThread.finished_signal.connect(self.onProcessingFinished_Print)
        self.processingThread.progress_signal.connect(self.onProgress_Print)
        self.processingThread.start()

    def onProgress_Print(self, notification):
        _translate = QtCore.QCoreApplication.translate
        self.notification.setText(
            _translate(
                "stacked_widget",
                '<html><head/><body><p align="center"><span style=" background-color: black; color: white; font-size:22pt; font-weight:600;">'
                + notification
                + "</span></p></body></html>",
            )
        )

    def onProcessingFinished_Print(self, retrieval_code, data_sent, error):
        self.code = retrieval_code
        self.data_sent = data_sent
        try:
            subprocess.run(["sudo", "rm", self.file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

        if self.data_sent:
            print("Processing finished!")
            print(self.code)

            self.PrintRetrievalCode_window = PrintRetrievalCode(
                self.file_path, self.stacked_widget, self.code, self.process_manager
            )
            self.stacked_widget.addWidget(self.PrintRetrievalCode_window)
            self.stacked_widget.setCurrentWidget(self.PrintRetrievalCode_window)
        else:
            while self.stacked_widget.count() > 0:
                widget_to_remove = self.stacked_widget.widget(0)  # get the widget
                self.stacked_widget.removeWidget(
                    widget_to_remove
                )  # remove it from stacked_widget
                widget_to_remove.setParent(
                    None
                )  # optional: set its parent to None so it gets deleted

            self.ReadyWindow_window = ReadyWindow(self.stacked_widget, self.process_manager)
            self.stacked_widget.addWidget(self.ReadyWindow_window)
            self.stacked_widget.setCurrentWidget(self.ReadyWindow_window)


class NumericKeyboard(QMainWindow):
    userID_signal = pyqtSignal(str)  # Define signal, payload is str (userID)

    def __init__(self, parent, stacked_widget, numeric_keyboard, scanThread, file_path):
        super(NumericKeyboard, self).__init__()
        loadUi("/home/decas/ui/DecasUI_New/W4.ui", self)

        # Set the window size
        self.resize(1024, 600)

        self.parent = parent
        self.stacked_widget = stacked_widget
        self.file_path = file_path
        self.numeric_keyboard = numeric_keyboard
        self.scanThread = scanThread
        self.number_found = False
        self.saved_value = ""
        self.name = ""
        # Connect buttons to their respective functions
        self.b0.clicked.connect(lambda: self.add_number("0"))
        self.b1.clicked.connect(lambda: self.add_number("1"))
        self.b2.clicked.connect(lambda: self.add_number("2"))
        self.b3.clicked.connect(lambda: self.add_number("3"))
        self.b4.clicked.connect(lambda: self.add_number("4"))
        self.b5.clicked.connect(lambda: self.add_number("5"))
        self.b6.clicked.connect(lambda: self.add_number("6"))
        self.b7.clicked.connect(lambda: self.add_number("7"))
        self.b8.clicked.connect(lambda: self.add_number("8"))
        self.b9.clicked.connect(lambda: self.add_number("9"))

        self.Del.clicked.connect(self.delete_number)
        self.enter.clicked.connect(self.enter_pressed)
        self.Retry.clicked.connect(self.show_output)
        self.cross.clicked.connect(self.destroy)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_time)
        self.timer.start(1000)

    def update_system_time(self):
        current_time = shared_data.time
        self.time.setPlainText(f" {current_time}")
        self.date.setPlainText(f" {shared_data.date}")

    def add_number(self, number):
        current_text = self.textEdit.toPlainText()
        new_text = current_text + number
        self.textEdit.setPlainText(new_text)

    def delete_number(self):
        current_text = self.textEdit.toPlainText()
        new_text = current_text[:-1]
        self.textEdit.setPlainText(new_text)

    def enter_pressed(self):
        if self.number_found:
            self.userID = self.number
            self.numeric_keyboard.update_user_id(self.userID)

            # Switch back to the SettingsWindow1
            index = self.parent.stacked_widget.indexOf(self.numeric_keyboard)
            self.parent.stacked_widget.setCurrentIndex(index)
            self.hide()

    def show_output(self):
        self.number = self.textEdit.toPlainText()
        print(f"Saved value: {self.number}")
        self.check_number_api()

    def destroy(self):
        # Switch back to the SettingsWindow1
        index = self.parent.stacked_widget.indexOf(self.numeric_keyboard)
        self.parent.stacked_widget.setCurrentIndex(index)
        # Restart the scanThread
        self.scanThread.restart()
        self.hide()

    def check_number_api(self):
        self.myText = ""
        self.url = "http://filesharing.n2rtech.com/api/mobile-verify"
        self.payload = {"mobile": self.number}
        self.files = []
        self.headers = {}
        self.response = requests.request(
            "POST", self.url, headers=self.headers, data=self.payload, files=self.files
        )

        _translate = QtCore.QCoreApplication.translate

        # Parse the JSON string into a Python dictionary
        self.parsed_data = json.loads(self.response.text)

        # Check if 'success' or 'error' key exists in the parsed data
        if "success" in self.parsed_data:
            success = self.parsed_data["success"]
            if self.parsed_data["firstname"]:
                firstname = self.parsed_data["firstname"]
                self.name = str(firstname)
                print(f"First name: {firstname}")
            if self.parsed_data["lastname"]:
                lastname = self.parsed_data["lastname"]
                self.name += str(lastname)
                print(f"Last name: {lastname}")

            # Print the extracted values
            print(f"Success: {success}")
            print(f"Name: {self.name}")
            self.myText = self.name
            self.number_found = True

        elif "error" in self.parsed_data:
            self.error = self.parsed_data["error"]
            self.response_message = self.parsed_data["response"]
            self.myText = "Number not found!!!"

            # Print the error message
            print(f"Error: {self.error}")
            print(f"Response: {self.response_message}")
            self.number_found = False

        else:
            print("Unexpected response format.")
            self.number_found = False
        self.username.setHtml(
            _translate(
                "MainWindow4",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:24pt; font-weight:600; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:22pt;">'
                + self.myText
                + "</span></p></body></html>",
            )
        )


class DataSentWindow(QMainWindow):
    def __init__(self, file_path, stacked_widget, process_manager):
        super().__init__()
        loadUi("/home/decas/ui/DecasUI_New/w6.ui", self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.file_path = file_path
        self.stacked_widget = stacked_widget

        self.timer = QTimer()
        self.timer.timeout.connect(self.go_home)
        self.timer.start(5000)

    def go_home(self):
        self.timer.stop()
        self.ReadyWindow_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.stacked_widget.addWidget(self.ReadyWindow_window)
        self.stacked_widget.setCurrentWidget(self.ReadyWindow_window)


class PrintRetrievalCode(QMainWindow):
    def __init__(self, file_path, stacked_widget, code, process_manager):
        super().__init__()
        loadUi("/home/decas/ui/DecasUI_New/w5.ui", self)

        # Create an instance of ProcessManager
        self.process_manager = process_manager

        # Set the window size
        self.resize(1024, 600)

        self.file_path = file_path
        self.stacked_widget = stacked_widget
        self.code = code
        self.thermal_print()

        self.timer = QTimer()
        self.timer.timeout.connect(self.go_home)
        self.timer.start(5000)

    def thermal_print(self):
        # p = Serial(
        #     devfile="/dev/ttySC1",
        #     baudrate=9600,
        #     bytesize=8,
        #     parity="N",
        #     stopbits=1,
        #     timeout=1.00,
        #     dsrdtr=True,
        # )
        # p.set(
        #     align="center",
        #     font="b",
        #     width=1,
        #     height=1,
        #     density=2,
        #     invert=0,
        #     smooth=True,
        #     flip=False,
        # )
        # # Printing the image
        # # here location can be your image path in “ ”
        # p.image("/home/decas/Logo.png", impl="bitImageColumn")

        # p.set(
        #     align="center",
        #     font="a",
        #     width=2,
        #     height=2,
        #     density=2,
        #     invert=0,
        #     smooth=False,
        #     flip=False,
        # )
        # p.text(str("TOKEN: " + str(self.code) + "\n"))

        # # printing the initial data
        # p.set(
        #     align="left",
        # )
        # p.text("\n")
        # p.text(
        #     """Retrieve receipt on repslips.com\nSteps:\n1) Sign up / Log on to:  \n     repslips.com\n2) Click on menu -->RETRIVAL \n3) Type the above code and SUBMIT \n4) View on recent Receipt \nEnjoy.........\n\n\n"""
        # )
        print("done")

    def go_home(self):
        self.timer.stop()
        self.ReadyWindow_window = ReadyWindow(self.stacked_widget, self.process_manager)
        self.stacked_widget.addWidget(self.ReadyWindow_window)
        self.stacked_widget.setCurrentWidget(self.ReadyWindow_window)


class DirectoryChecker(QObject):
    open_settings_window1_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.path_data = ""  # Initialize path_data with an empty string

    def check_directory(self):
        # directory_path = "C:/Users/Bilal/Documents/Decas"
        # directory_path = "/var/spool/cups-pdf/ANONYMOUS/"
        # directory_path = "/home/decas/ui/DecasUI/Print/"
        directory_path = "/home/decas/output/"
        # directory_path = 'D:/DecasUI/DecasUI/ANONYMOUS/'

        contents = os.listdir(directory_path)

        if contents:
            for content in contents:
                file_path = os.path.join(directory_path, content)
                if os.path.isfile(file_path):
                    print(file_path)
            self.path_data = file_path  # Update path_data with the last file_path
            self.open_settings_window1_signal.emit()


class SerialManager:
    def __init__(self, port="/dev/ttySC0", baud_rate=9600):
        self.serial_port = port
        self.baud_rate = baud_rate
        
        # Barcode Commands to be sent
        self.uart_output_command = "7E000801000D00ABCD"
        self.single_scanning_time_command = "7E000801000600ABCD"
        self.command_mode_command = "7E0008010000D5ABCD"
        self.reset_command = "7E00080100D950ABCD"

    def connect(self):
        try:
            with serial.Serial(self.serial_port, self.baud_rate, timeout=1) as ser:
                print(f"Connected to {self.serial_port} at {self.baud_rate} baud rate.")
                ser.write(bytes.fromhex(self.uart_output_command))
                ser.write(bytes.fromhex(self.single_scanning_time_command))
                ser.write(bytes.fromhex(self.command_mode_command))
                ser.close()
        except Exception as e:
            print(f"Error: {e}")

class MyApp(QApplication):
    def __init__(self, app):
        super().__init__(sys.argv)
        self.process_manager = MonoDecasProcessManager()
        self.serial_manager = SerialManager()

        # Initialize serial and UI components
        self.init_serial()
        self.init_ui()

    def init_serial(self):
        self.serial_manager.connect()

    def init_ui(self):
        try:
            self.stacked_widget = QStackedWidget()
            self.process_manager.start_process()
            self.setting_window = ReadyWindow(self.stacked_widget, self.process_manager)
            self.stacked_widget.addWidget(self.setting_window)
            self.stacked_widget.showFullScreen()
            
        except (OSError, ValueError) as e:
            print(f"Error: {e}")
            self.process_manager.terminate_process()

def create_main_app(app):
    return MyApp(app)

def run_main_app(app):
    return app.exec_()

# Instructions/Commands
# sudo chmod 777 /tmp
# pip3 install pyqt5-tools adafruit-circuitpython-pn532 board pyserial escpos cryptography==36.0.0 pdfplumber ntplib requests python-dateutil

# sudo apt-get update
# sudo apt-get upgrade
# sudo apt-get install python3-pyqt5 python3-tk python3-requests python3-bluez mono-complete
# sudo pip3 install adafruit-circuitpython-pn532 board pyserial escpos pdfplumber ntplib python-dateutil
# sudo mkdir ui
# sudo chmod 777 /home/decas/output/