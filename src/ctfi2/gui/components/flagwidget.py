from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory


class FlagWidget(QDialog):
    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(QDialog, self).__init__()

        self.fields: dict = {}
        self.dialog: bool = dialog

        self.setWindowTitle("New Flag")
        self.setGeometry(200, 200, 400, 100)

        self.update_pause = True

        type_box, self.type_combo = ComponentFactory.box_combo_box(text="Type",
                                                                   choices=["static", "regex"],
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        content_box, self.content_line = ComponentFactory.box_line_edit(text="Flag",
                                                                        place_holder="Enter Flag Value",
                                                                        alignment=None,
                                                                        orientation=Qt.AlignHorizontal_Mask)

        data_box, self.data_combo = ComponentFactory.box_combo_box(text='',
                                                                   choices=['case sensitive', 'case insensitive'],
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        self.outer_box = QVBoxLayout()
        self.outer_box.setAlignment(Qt.AlignTop)

        for layout in [type_box, content_box, data_box]:
            self.outer_box.addLayout(layout)

        self.setLayout(self.outer_box)

        if dialog:
            button_box, buttons = ComponentFactory.box_buttons(button_names=["Ok", "Cancel"],
                                                               alignment=Qt.AlignRight,
                                                               orientation=Qt.AlignHorizontal_Mask)
            buttons['Ok'].clicked.connect(self.ok_clicked)
            buttons['Cancel'].clicked.connect(self.cancelled)
            self.outer_box.addLayout(button_box)

        elif not dialog:
            self.type_combo.currentIndexChanged.connect(self.update)
            self.content_line.textEdited.connect(self.update)
            self.data_combo.currentIndexChanged.connect(self.update)

    def cancelled(self) -> None:
        self.type_combo.setCurrentIndex(0)
        self.content_line.setText('')
        self.data_combo.setCurrentIndex(0)
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def clear(self) -> None:
        self.cancelled()

    def read(self) -> dict:
        self.fields.update({'type': self.type_combo.currentText(),
                            'content': self.content_line.text(),
                            'data': '' if self.data_combo.currentIndex() == 0 else 'case insensitive'})
        ret_dict: dict = self.fields
        if self.dialog:
            self.clear()
        return ret_dict

    def update(self) -> None:
        """ Signals that a data field value was changed """
        # This is the set_fields function in reverse where we write data from the user edited widget into our fields
        # dict
        if not self.update_pause:
            self.value_updated.emit({"flags": self.read()})

    def write(self, fields: dict) -> None:
        self.update_pause = True

        self.fields = fields
        self.type_combo.findText(fields['type'], Qt.MatchFixedString)
        self.content_line.setText(fields['content'])
        self.data_combo.setCurrentIndex(self.data_combo.findText('case sensitive' if fields['data'] == '' else 'case insensitive', Qt.MatchFixedString))

        self.update_pause = False
