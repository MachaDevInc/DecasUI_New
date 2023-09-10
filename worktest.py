from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenuBar,
    QStatusBar,
    QPushButton,
    QMainWindow,
    QScrollArea,
    QTextEdit,
    QTextBrowser,
    QFrame,
    QTableWidget,
    QApplication,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt5.QtCore import QSize, QRect, QCoreApplication, Qt
from PyQt5 import QtGui
import json

class CustomWidget(QWidget):
    def __init__(
        self,
        job_id,
        data,
        central_widget,
        button_needed=False,
        work_window=None,
        parent=None,
    ):
        super(CustomWidget, self).__init__(parent)
        self.central_widget = central_widget

        self.job_id = job_id
        self.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.work_window = work_window

        self.layout_obj = QHBoxLayout()
        self.layout_obj.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout_obj)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(60)

        self.table = QTableWidget(self)
        self.table.setRowCount(1)  # Added rows
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Invoice Number', 'User ID', 'Date and Time', 'Status'])

        # Style the header
        font = QtGui.QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)

        # Hide the vertical headers
        self.table.verticalHeader().setVisible(False)

        # Fix the column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFixedWidth(810)
        self.layout_obj.setStretchFactor(self.table, 1)
        self.table.setColumnWidth(0, 160)  # 800 / 5 = 160
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 280)
        # self.table.setColumnWidth(4, 160)
        self.setFixedWidth(810)
        self.setFixedHeight(100)

        self.table.horizontalHeader().setStyleSheet('::section { background-color: #9decd4 }')
        # self.table.verticalHeader().setStyleSheet('::section { background-color: transparent }')

        self.table.setItem(0, 0, QTableWidgetItem("123456789"))
        self.table.setItem(0, 1, QTableWidgetItem("Bilal"))
        self.table.setItem(0, 2, QTableWidgetItem("2023-07-10 16:42:31"))
        self.table.setItem(0, 3, QTableWidgetItem("Success"))
        self.table.item(0, 3).setFont(font)

        self.layout_obj.addWidget(self.table)

        if button_needed:
            self.button = QPushButton()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("pics/retry.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            self.button.setIcon(icon)
            self.button.setIconSize(QSize(80, 40))
            self.button.setFixedSize(QSize(80, 40))
            self.button.setFlat(True)
            if self.work_window is not None:
                self.button.clicked.connect(
                    lambda: self.work_window.on_button_clicked(self.job_id)
                )

            button_layout = QHBoxLayout()
            button_layout.addStretch(1)
            button_layout.setAlignment(Qt.AlignBottom)
            button_layout.addWidget(self.button)

            self.layout_obj.addLayout(button_layout)


class JobsMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(JobsMainWindow, self).__init__(parent)
        self.setStyleSheet(
            """
            QMainWindow {
                background-image: url(pics/Standby.png);
                background-repeat: no-repeat
            }
        """
        )

        self.resize(1024, 600)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, 1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pics/Standby.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(20, 0, 250, 100))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.central_widget = QWidget(self.centralwidget)
        self.central_widget.setGeometry(QRect(30, 70, 994, 400))

        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.back = QPushButton(self.centralwidget)
        self.back.setGeometry(QRect(50, 480, 75, 75))
        self.back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("pics/1 (400 × 400 px).png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.back.setIcon(icon)
        self.back.setIconSize(QSize(75, 75))
        self.back.setFlat(True)
        self.back.setObjectName("back")
        self.textEdit1 = QTextEdit(self.centralwidget)
        self.textEdit1.setGeometry(QRect(570, 20, 271, 60))
        self.textEdit1.setObjectName("textEdit1")
        self.textBrowser_2 = QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QRect(850, 20, 140, 60))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBrowser_2.setPalette(palette)
        self.textBrowser_2.setFrameShape(QFrame.Box)
        self.textBrowser_2.setFrameShadow(QFrame.Raised)
        self.textBrowser_2.setLineWidth(4)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.search = QPushButton(self.centralwidget)
        self.search.setGeometry(QRect(850, 20, 140, 60))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.search.setPalette(palette)
        self.search.setLayoutDirection(Qt.LeftToRight)
        self.search.setAutoFillBackground(False)
        self.search.setStyleSheet('font: 75 24pt "MS Shell Dlg 2";')
        self.search.setText("")
        self.search.setIconSize(QSize(100, 100))
        self.search.setAutoDefault(False)
        self.search.setDefault(False)
        self.search.setFlat(True)
        self.search.setObjectName("search")
        self.search1 = QPushButton(self.centralwidget)
        self.search1.setGeometry(QRect(570, 20, 271, 60))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.search1.setPalette(palette)
        self.search1.setLayoutDirection(Qt.LeftToRight)
        self.search1.setAutoFillBackground(False)
        self.search1.setStyleSheet('font: 75 24pt "MS Shell Dlg 2";')
        self.search1.setText("")
        self.search1.setIconSize(QSize(100, 100))
        self.search1.setAutoDefault(False)
        self.search1.setDefault(False)
        self.search1.setFlat(True)
        self.search1.setObjectName("search1")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("JobsMainWindow", "JobsMainWindow"))
        self.label_2.setText(
            _translate(
                "JobsMainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">RECENT JOBS</span></p></body></html>',
            )
        )
        self.textEdit1.setHtml(
            _translate(
                "JobsMainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.textBrowser_2.setHtml(
            _translate(
                "JobsMainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:22pt; font-weight:600;">Search</span></p></body></html>',
            )
        )
        
class workWindow(JobsMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.search_keyword = ""
        self.resize(1024, 600)
        self.show_jobs()

    def show_jobs(self):
        self.clear_layout(self.scroll_layout)

        jobs = {}

        try:
            with open("my_jobs.json", "r") as f:
                jobs = json.load(f)
                size = len(jobs)
                print(f"The dictionary contains {size} key-value pairs.")
        except json.JSONDecodeError:
            print("File is not valid JSON")
        except FileNotFoundError:
            print("File 'my_jobs.json' not found.")

        if jobs:
            for key, value in jobs.items():
                if self.search_keyword == "":
                    data = value["job_title"]
                    if value["data_sent"] is True:
                        widget = CustomWidget(key, data, self.central_widget, False, self)
                    else:
                        widget = CustomWidget(key, data, self.central_widget, True, self)
                    self.scroll_layout.addWidget(widget)
                else:
                    if self.search_keyword in value["receiver"]:
                        data = value["job_title"]
                        if value["data_sent"] is True:
                            widget = CustomWidget(key, data, self.central_widget, False, self)
                        else:
                            widget = CustomWidget(key, data, self.central_widget, True, self)
                        self.scroll_layout.addWidget(widget)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = workWindow(None)
    window.show()
    sys.exit(app.exec_())
