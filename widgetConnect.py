import os, sys, csv, fnmatch
import serial.tools.list_ports
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QColor
from device_info import DeviceInfo

class WidgetConnect(QWidget):
    def __init__(self, switch_to_options_callback):
        super().__init__()
        self.firmware_erase = ""
        self.firmware_update = ""
        self.device = ""
        self.tty_files = ""
        self.switch_to_options_callback = switch_to_options_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('')
        self.label.setStyleSheet("background: rgba(0, 0, 0, 100); color: white; font-size: 24px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 200))
        shadow_effect.setOffset(3,3)
        self.label.setGraphicsEffect(shadow_effect)
        layout.addWidget(self.label)

        self.btn = QPushButton("Next")
        self.btn.setStyleSheet("font-size: 24px")
        self.btn.clicked.connect(self.goto_options)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def goto_options(self):
        self.get_device_tty()
        self.switch_to_options_callback()

    def get_firmware_file(self):
        directory = "./firmware/"
        meshtastic_version = "2.7.3"

        for filename in os.listdir(directory):
            if ("firmware-" + DeviceInfo.get_data("firmware_name") + "-" + meshtastic_version) in filename:
                if "update" in filename:
                    DeviceInfo.set_data("firmware_update", filename)
                else:
                    DeviceInfo.set_data("firmware_erase", filename)

    def get_device_tty(self):
        ports = serial.tools.list_ports.comports()
        acm_usb_ports = [port.device for port in ports if 'ttyACM' in port.device or 'ttyUSB' in port.device]
        acm_usb_ports.sort()
        DeviceInfo.set_data("tty_port",acm_usb_ports[-1])

    # Used to update individual widget on screen switch
    def showEvent(self, event: QEvent):
        super().showEvent(event)
        
        self.get_firmware_file()

        if DeviceInfo.get_data("flash_mode") == "true":
            self.label.setText("You have selected the following device:\n\nMake: " + str(DeviceInfo.get_data("make")) + "\n" +
                "Model: " + str(DeviceInfo.get_data("model")) + 
                "\n\nFlashing mode required, please use the following instructions to while connecting the device:\n" +
                str(DeviceInfo.get_data("flash_instructions")) + "\nOnce connected, click next")
        else:
            self.label.setText("You have selected the following device:\n\nMake: " + str(DeviceInfo.get_data("make")) + "\n" +
                "Model: " + str(DeviceInfo.get_data("model")) + "\n\nYou may connect your Meshtastic device now\nOnce connected, click next")
