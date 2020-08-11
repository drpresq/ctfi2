from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.api.constants import TITLE, VERSION, AUTHOR


class TitleWidget(QWidget):
    fields: dict = {}
    index: int = None
    value_updated = pyqtSignal(dict)
    item_selected = pyqtSignal(QTreeWidgetItem)

    def __init__(self, widget_type: str):
        super(TitleWidget, self).__init__()

        self.widget_type = widget_type
        self.content_layout = QVBoxLayout()
        self.content_layout.addWidget(self.generate_title_text())
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.content_layout)

    @staticmethod
    def generate_title_text():
        default_plugin_title = QLabel()
        default_plugin_title.setText("{}\n\nhttps://github.com/drpresq/ctfi2\n\nVersion: {}\n"
                                     "\nby: {}".format(TITLE, VERSION, AUTHOR))
        default_plugin_title.setAlignment(Qt.AlignCenter)
        return default_plugin_title