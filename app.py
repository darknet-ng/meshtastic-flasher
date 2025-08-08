#!/bin/python3

import sys#, subprocess, os, time
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from widgetMake import WidgetMake
from widgetConnect import WidgetConnect
#from widgetOptions import WidgetOptions
from widgetFlash import WidgetFlash

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window themeing and size
        self.setWindowTitle("DEF CON Meshtastic Flasher")
        self.setMinimumSize(QSize(1024, 600))
        window = QWidget(self)
        self.setCentralWidget(window)

        layout_main = QVBoxLayout()

        title = QLabel("Meshtastic Flasher for DEF CON 33")
        title.setStyleSheet("background: rgba(0, 0, 0, 100); color: white; font-size: 36px")
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 200))
        shadow_effect.setOffset(3,3)
        title.setGraphicsEffect(shadow_effect)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        title.resize(1024, 80)
        layout_main.addWidget(title)

        # Set up stacked widget to handle each screen
        self.stacked_widget =  QStackedWidget()

        # Create each page of the flasher, pass callbacks for back and forward switching
        self.widget_make = WidgetMake(self.switch_to_connect)
        self.widget_connect = WidgetConnect(self.switch_to_make, self.switch_to_flash)
        #self.widget_options = WidgetOptions(self.switch_to_flash)
        self.widget_flash = WidgetFlash(self.switch_to_connect, self.switch_to_make)

        # Add each page to the stacked widget
        self.stacked_widget.addWidget(self.widget_make)
        self.stacked_widget.addWidget(self.widget_connect)
        #self.stacked_widget.addWidget(self.widget_options)
        self.stacked_widget.addWidget(self.widget_flash)

        # Set starting widget
        self.stacked_widget.setCurrentWidget(self.widget_make)

        layout_main.addWidget(self.stacked_widget)
        window.setLayout(layout_main)

    # Callback functions for each subwidget to switch to the next
    def switch_to_make(self):
        self.stacked_widget.setCurrentWidget(self.widget_make)

    def switch_to_connect(self):
        self.stacked_widget.setCurrentWidget(self.widget_connect)

    #def switch_to_options(self):
    #    self.stacked_widget.setCurrentWidget(self.widget_options)

    def switch_to_flash(self):
        self.stacked_widget.setCurrentWidget(self.widget_flash)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Addtional Window theming, may need applied to each widget
    stylesheet = """
        MainWindow {
            background-image: url("./ui_images/dc-33-header.png");
            background-repeat: no-repeat;
            background-position: center;
        }
    """

    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
