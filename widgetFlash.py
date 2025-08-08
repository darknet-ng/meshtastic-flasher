import os, sys, csv, fnmatch 
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QTextEdit, QMessageBox
from PyQt6.QtCore import QEvent, Qt, QProcess
from PyQt6.QtGui import QColor
from device_info import DeviceInfo

class WidgetFlash(QWidget):
    def __init__(self, back_to_connect_callback, switch_to_make_callback):
        super().__init__()
        self.back_to_connect_callback = back_to_connect_callback
        self.switch_to_make_callback = switch_to_make_callback
        self.config_backup = 'config_backup.yaml'
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
        self.outputDisplay.setStyleSheet("background: rgba( 0, 0, 0, 255); color: white;")
        layout.addWidget(self.outputDisplay)
        
        layout_buttons = QHBoxLayout()

        self.backbtn = QPushButton("Back")
        self.backbtn.setStyleSheet("font-size: 24px")
        self.backbtn.clicked.connect(self.back_to_connect_callback)
        layout_buttons.addWidget(self.backbtn)

        self.forwardbtn = QPushButton("Flash")
        self.forwardbtn.setStyleSheet("font-size: 24px")
        self.forwardbtn.clicked.connect(self.runCommand)
        layout_buttons.addWidget(self.forwardbtn)

        layout.addLayout(layout_buttons)
        self.setLayout(layout)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handleOutput)
        self.process.readyReadStandardError.connect(self.handleError)
        self.process.finished.connect(self.processFinished)

    def runCommand(self):
        self.forwardbtn.setEnabled(False)
        self.backbtn.setEnabled(False)

        # Disabled for now, needs moved elsewhere to not clash with flashing process
        #self.backup_security_keys()

        if DeviceInfo.get_data('erase') == 'true':
            flash_command = './device-install.sh'
            flash_arguments = ['-p', DeviceInfo.get_data("tty_port"), '-f', DeviceInfo.get_data("firmware_erase")]
        else:
            flash_command = './device-update.sh'
            flash_arguments = ['-p', DeviceInfo.get_data("tty_port"), '-f', DeviceInfo.get_data("firmware_update")]

        self.process.setWorkingDirectory('./firmware')
        try:
            self.process.start(flash_command, flash_arguments)
        except Exception as e:
            self.processFinished(1, 1)


    # Disabled for DC33, more thought needs to go into how to handle backing up security keys
    # and adding channels or any other configuration. Leaving this to attendees to handle
    #def backup_security_keys(self):
    #    self.backup_arguments = ['--export-config', '>', self.config_backup]
    #    self.backup_command = 'meshtastic'
    #    if DeviceInfo.get_data('backup') == 'true':
    #        self.process.start(self.backup_command, self.backup_arguments)


    #def restore_security_keys(self):
    #    self.restore_arguments = ['--configure', self.config_backup]
    #    self.restore_command = 'meshtastic'
    #    if DeviceInfo.get_data('backup') == 'true':
    #        self.process.start(self.restore_command, self.restore_arguments)
    #        self.process.start('rm -f', self.config_backup)

    #def configureDevice(self):
    #    region_command = ['-m', 'meshtastic', '--port', DeviceInfo.get_data('tty_port'), '--set', 'lora.region', 'US']
    #    self.process.start('python3', region_command) 

    #def addDarknet(self):
    #    darknet_command = ['-m', 'meshtastic', '--port', DeviceInfo.get_data('tty_port'), '--ch-set', 'name', 'Darknet-NG', '--ch-set', 'psk', 'iwXq4FC8fIxprWKPq663DRq6IYI3LsQ4uct3Y2e4Ukw=', '--ch-index', '3']
    #    self.process.start('python3', darknet_command)

    def handleOutput(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.outputDisplay.append(output)

    def handleError(self):
        error = self.process.readAllStandardError().data().decode()
        print(error)
        self.outputDisplay.append(f"Error: {error}")

    def processFinished(self, exitCode, exitStatus):
        #self.restore_security_keys()
        self.forwardbtn.disconnect()
        self.forwardbtn.setText("Restart")
        self.forwardbtn.clicked.connect(self.goto_make)
        self.forwardbtn.setEnabled(True)

    def goto_make(self):
        self.switch_to_make_callback()

    # Used to update individual widget on screen switch
    def showEvent(self, event: QEvent):
        super().showEvent(event)
        self.outputDisplay.clear()
        self.backbtn.setEnabled(True)
        self.forwardbtn.setText("Flash")
        self.forwardbtn.disconnect()
        self.forwardbtn.clicked.connect(self.runCommand)
