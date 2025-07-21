import csv
from PyQt6.QtCore import QEvent, pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon
from device_info import DeviceInfo

class deviceButton(QToolButton):
    firmware_name = ""

    def __init__(self, display_name, icon_file, firmware_name, device_select_callback):
        super().__init__()
        self.device_select_callback = device_select_callback

        BUTTON_SIZE = QSize(300, 170);
        BTN_ICON_SIZE = QSize(100, 100);
        BTN_STYLESHEET = "background: rgba(0, 0, 0, 100); border: none; color: white; font-size: 24px;"

        self.setText(display_name)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon);
        self.setIcon(QIcon("./device_images/" + icon_file))
        self.setIconSize(BTN_ICON_SIZE)
        self.setFixedSize(BUTTON_SIZE)
        self.setStyleSheet(BTN_STYLESHEET)
        self.firmware_name = firmware_name
        self.clicked.connect(self.buttonClick)

    def buttonClick(self):
        DeviceInfo.set_data("firmware_name", self.firmware_name)
        
        with open('devices.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row["firmware_name"] == self.firmware_name:
                    DeviceInfo.set_data("make", row["make"])
                    DeviceInfo.set_data("model", row["model"])
                    DeviceInfo.set_data("display_name", row["display_name"])
                    DeviceInfo.set_data("device_image", row["device_image"])
                    DeviceInfo.set_data("chip", row["chip"])
                    DeviceInfo.set_data("flash_mode", row["flash_mode"])
                    DeviceInfo.set_data("flash_instructions", row["flash_instructions"])
        self.device_select_callback()
