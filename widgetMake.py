import sys, csv
from PyQt6.QtCore import QEvent, pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QToolButton
from PyQt6.QtGui import QIcon, QPixmap
from deviceButton import deviceButton
from device_info import DeviceInfo

class WidgetMake(QWidget):

    def __init__(self, switch_to_model_callback):
        super().__init__()
        self.switch_to_model_callback = switch_to_model_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout_btns = QGridLayout()
        
        with open("devices.csv", newline='') as file:
            reader = csv.DictReader(file)

            btn_index = 0
            device_btn = []
            display_row = 0
            display_column = 0

            for row in reader:
                device_btn.append(deviceButton(row["display_name"], row["device_image"], row["firmware_name"], self.device_select))
                layout_btns.addWidget(device_btn[btn_index], display_column, display_row)

                btn_index += 1
                
                if display_row == 0:
                    display_row = 1
                else:
                    display_column = 1
                    display_row = 0
                

        widget_btns = QWidget()
        widget_btns.setLayout(layout_btns)

        layout.addWidget(widget_btns, 8)

        connect_warn = QLabel("Do not connect device yet")
        connect_warn.setStyleSheet("color: white; font-size: 24px;")
        connect_warn.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        connect_warn.resize(1024,80)
        layout.addWidget(connect_warn)

        #self.label = QLabel('Make Widget', self)
        #layout.addWidget(self.label)

        #self.btn = QPushButton("Test")
        #self.btn.clicked.connect(self.btn_click)
        #layout.addWidget(self.btn)
        self.setLayout(layout)

    def device_select(self):
        self.switch_to_model_callback()

    # Used to update individual widget on screen switch
    def showEvent(self, event: QEvent):
        #self.label.setText("Updated Make Text")
        super().showEvent(event)
