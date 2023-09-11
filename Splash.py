from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QProgressBar, QLabel, QMenuBar, QStatusBar, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap
import sys
import serial
import time

from MainFile import create_main_app, run_main_app

app = QApplication([])  # Initialize just one QApplication instance
main_app = create_main_app(app)  # Pass the QApplication instance to MyApp

# Configure the serial port and baud rate
serial_port = "/dev/ttySC0"
baud_rate = 9600

# Barcode Commands to be sent
uart_output_command = "7E000801000D00ABCD"
single_scanning_time_command = "7E000801000600ABCD"
command_mode_command = "7E0008010000D5ABCD"
reset_command = "7E00080100D950ABCD"

def Setup_barcode():
    try:
        scanned = False
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print(f"Connected to {serial_port} at {baud_rate} baud rate.")

            # Send the command
            print(f"Sending command: {command_mode_command}")
            ser.write(bytes.fromhex(command_mode_command))

            while True:
                # Read data from the serial port
                data = ser.readline().decode("utf-8").strip()
                # If data is received, print it
                if data:
                    print(f"Received data: {data}")
                    break

                # Wait for a short period before reading the next data
                time.sleep(0.1)

            # Send the command
            print(f"Sending command: {single_scanning_time_command}")
            ser.write(bytes.fromhex(single_scanning_time_command))

            while True:
                # Read data from the serial port
                data = ser.readline().decode("utf-8").strip()
                # If data is received, print it
                if data:
                    print(f"Received data: {data}")
                    break

                # Wait for a short period before reading the next data
                time.sleep(0.1)

            # Send the command
            print(f"Sending command: {uart_output_command}")
            ser.write(bytes.fromhex(uart_output_command))

            while True:
                # Read data from the serial port
                data = ser.readline().decode("utf-8").strip()
                # If data is received, print it
                if data:
                    print(f"Received data: {data}")
                    break

                # Wait for a short period before reading the next data
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting the program.")

    except Exception as e:
        print(f"Error: {e}")

Setup_barcode()

# Main window setup
window = QMainWindow()
window.setObjectName("window")
window.resize(1024, 600)

# Central Widget setup
centralwidget = QWidget()
centralwidget.setObjectName("centralwidget")

# Label setup
label = QLabel(centralwidget)
label.setGeometry(QRect(0, 0, 1024, 600))
label.setText("")
label.setPixmap(QPixmap("/home/decas/ui/DecasUI_New/pics/Standby.png"))
label.setScaledContents(True)
label.setObjectName("label")

# Progress Bar setup
progressBar = QProgressBar(centralwidget)
progressBar.setGeometry(QRect(270, 480, 521, 41))
progressBar.setProperty("value", 0)
progressBar.setObjectName("progressBar")

# Change the color of the progress bar to green
progressBar.setStyleSheet("""
    QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
        # color: white;
    }
    
    QProgressBar::chunk {
        background-color: green;
    }
""")
progressBar.update()

# Second Label setup
label_2 = QLabel(centralwidget)
label_2.setGeometry(QRect(310, 170, 400, 271))
label_2.setText("")
label_2.setPixmap(QPixmap("/home/decas/ui/DecasUI_New/pics/Decas_Logo.png"))
label_2.setObjectName("label_2")

# Set centralwidget, menubar and statusbar to window
window.setCentralWidget(centralwidget)

# Timer function to update progress
def update_progress():
    current_value = progressBar.value()
    # os.system("/usr/bin/python3 /home/decas/ui/DecasUI_New/MainFile.py")  # Launch main application here
    if current_value >= 100:
        # window.close()
        # os.system("/usr/bin/python3 /home/decas/ui/DecasUI_New/MainFile.py")  # Launch main application here
        timer.stop()
        window.close()
        # sys.exit(run_main_app(main_app))  # Run the already-initialized MyApp instance
    progressBar.setValue(current_value + 1)

# Timer setup
timer = QTimer()
timer.timeout.connect(update_progress)
timer.start(100)  # 100 milliseconds

# Show window
window.showFullScreen()

# Start application
sys.exit(app.exec_())
