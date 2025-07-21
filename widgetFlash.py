import os, sys, csv, fnmatch
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QTextEdit
from PyQt6.QtCore import QEvent, Qt, QProcess
from PyQt6.QtGui import QColor
from device_info import DeviceInfo

class WidgetFlash(QWidget):
    def __init__(self, switch_to_make_callback):
        super().__init__()
        self.switch_to_make_callback = switch_to_make_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Flashing")
        self.label.setStyleSheet("background: rgba(0, 0, 0, 100); font-size: 24px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 200))
        shadow_effect.setOffset(3,3)
        self.label.setGraphicsEffect(shadow_effect)
        self.label.setMaximumSize(1024,80)
        layout.addWidget(self.label)

        self.outputDisplay = QTextEdit()
        self.outputDisplay.setReadOnly(True)
        self.outputDisplay.setStyleSheet("color: white;")
        layout.addWidget(self.outputDisplay)

        self.btn = QPushButton("Flash")
        self.btn.setStyleSheet("font-size: 24px")
        self.btn.clicked.connect(self.runCommand)
        layout.addWidget(self.btn)

        self.setLayout(layout)

        self.process = QProcess()
        self.process.setWorkingDirectory('./firmware/')
        self.process.readyReadStandardOutput.connect(self.handleOutput)
        self.process.readyReadStandardError.connect(self.handleError)

    def runCommand(self):
        print("I'm running")
        if DeviceInfo.get_data('erase') == 'true':
            flash_command = './device-install.sh -p ' + DeviceInfo.get_data("tty_port") + ' -f ' + DeviceInfo.get_data("firmware_erase")
        else:
            flash_command = './device-update.sh -p ' + DeviceInfo.get_data("tty_port") + ' -f ' + DeviceInfo.get_data("firmware_update")
        print(flash_command)
        self.process.start(flash_command)
        print("I ran?")

    def handleOutput(self):
        output = self.process.readAllStandardOutput().data().decode()
        print(output)
        self.outputDisplay.append(output)

    def handleError(self):
        error = self.process.readAllStandardError().data().decode()
        print(error)
        self.outputDisplay.append(f"Error: {error}")

    def goto_make(self):
        self.switch_to_make_callback()

    # Used to update individual widget on screen switch
    def showEvent(self, event: QEvent):
        super().showEvent(event)
