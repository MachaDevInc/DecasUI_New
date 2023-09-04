from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QProgressBar, QLabel, QMenuBar, QStatusBar, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap
import sys

app = QApplication([])

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
label.setPixmap(QPixmap("d:\\DecasUI\\DecasUI_V2\\pics/Standby.png"))
label.setScaledContents(True)
label.setObjectName("label")

# Progress Bar setup
progressBar = QProgressBar(centralwidget)
progressBar.setGeometry(QRect(270, 480, 521, 41))
progressBar.setProperty("value", 50)
progressBar.setObjectName("progressBar")

# Second Label setup
label_2 = QLabel(centralwidget)
label_2.setGeometry(QRect(310, 170, 400, 271))
label_2.setText("")
label_2.setPixmap(QPixmap("d:\\DecasUI\\DecasUI_V2\\pics/Decas_Logo.png"))
label_2.setObjectName("label_2")

# Menu Bar setup
menubar = QMenuBar()
menubar.setGeometry(QRect(0, 0, 1024, 21))
menubar.setObjectName("menubar")

# Status Bar setup
statusbar = QStatusBar()
statusbar.setObjectName("statusbar")

# Set centralwidget, menubar and statusbar to window
window.setCentralWidget(centralwidget)
window.setMenuBar(menubar)
window.setStatusBar(statusbar)

# Timer function to update progress
def update_progress():
    current_value = progressBar.value()
    if current_value >= 100:
        window.close()
    progressBar.setValue(current_value + 1)

# Timer setup
timer = QTimer()
timer.timeout.connect(update_progress)
timer.start(100)  # 100 milliseconds

# Show window
window.showFullScreen()

# Start application
sys.exit(app.exec_())
