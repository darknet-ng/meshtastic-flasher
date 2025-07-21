import os, sys, csv, fnmatch
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QCheckBox
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QColor
from device_info import DeviceInfo

class WidgetOptions(QWidget):
    def __init__(self, switch_to_flash_callback):
        super().__init__()
        self.switch_to_flash_callback = switch_to_flash_callback
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Options")
        self.label.setStyleSheet("background: rgba(0, 0, 0, 100); color: white; font-size: 24px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 200))
        shadow_effect.setOffset(3,3)
        self.label.setGraphicsEffect(shadow_effect)
        self.label.setMaximumSize(1024, 80)
        layout.addWidget(self.label)

        layoutBody = QHBoxLayout()
        layoutLeft = QVBoxLayout()
        layoutRight = QVBoxLayout()

        self.erase = QCheckBox("Erase device?")
        self.erase.setStyleSheet("font-size: 24px; color: white;")
        self.erase.setChecked(False)

        layoutLeft.addWidget(self.erase)

        layoutBody.addLayout(layoutLeft)
        layoutBody.addLayout(layoutRight)

        layout.addLayout(layoutBody)

        self.btn = QPushButton("Flash")
        self.btn.setStyleSheet("font-size: 24px")
        self.btn.clicked.connect(self.goto_flash)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def goto_flash(self):
        if self.erase.isChecked():
            DeviceInfo.set_data("erase", "true")
        else:
            DeviceInfo.set_data("erase", "false")
        self.switch_to_flash_callback()

    # Used to update individual widget on screen switch
    def showEvent(self, event: QEvent):
        super().showEvent(event)
