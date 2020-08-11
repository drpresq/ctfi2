import sys
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.api.constants import VERSION

# Import Plugins
from ctfi2.gui import CTFi2GUI

# Handle high resolution displays:
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class MainApp(QWidget):
    # GUI Main Window
    def __init__(self, parent=None):
        logging.debug("MainApp:init() instantiated")
        super().__init__()
        self.baseWidgets = {}
        self.vmWidgets = {}
        self.materialWidgets = {}
        self.statusBar = QStatusBar()

        self.setFixedSize(670, 565)
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.setWindowTitle("ctfi2")

        self.tabWidget = QTabWidget()
        self.tabWidget.setGeometry(QRect(0, 15, 668, 565))
        self.tabWidget.setObjectName("tabWidget")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)

        self.setLayout(self.mainLayout)
        self.tabWidget.setCurrentIndex(0)

        # Import Plugins
        plugin_item: QWidget = CTFi2GUI()
        self.tabWidget.addTab(plugin_item, plugin_item.__repr__())


def run(log_level: int) -> None:
    logging.basicConfig(level=log_level)
    app = QApplication(sys.argv)
    mainapp = MainApp()

    window = QMainWindow()
    window.show()
    window.setWindowTitle("ctfi2 {}".format(VERSION))
    window.setCentralWidget(mainapp)

    # Start the event loop.
    app.exec_()