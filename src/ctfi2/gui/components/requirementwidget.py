from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory


class RequirementWidget(QDialog):
    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(QDialog, self).__init__()

        self.fields: dict = {}
        self.dialog: bool = dialog

        self.setWindowTitle("New Requirement")
        self.setGeometry(200, 200, 400, 100)

        prereq_box, self.prereq_combo = ComponentFactory.box_combo_box(text='Prerequisite',
                                                                       choices=[''],
                                                                       alignment=None,
                                                                       orientation=Qt.AlignHorizontal_Mask)

        self.outer_box = QVBoxLayout()
        self.outer_box.setAlignment(Qt.AlignTop)

        for layout in [prereq_box]:
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
            self.prereq_combo.activated.connect(self.update)

    def cancelled(self) -> None:
        self.prereq_combo.clear()
        self.prereq_combo.addItem('')
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def clear(self) -> None:
        self.cancelled()

    def read(self) -> dict:
        self.fields.update({'prerequisites': self.prereq_combo.currentText()})
        ret_dict: dict = self.fields
        if self.dialog:
            self.clear()
        return ret_dict

    def update(self) -> None:
        """ Signals that a data field value was changed """
        # This is the set_fields function in reverse where we write data from the user edited widget into our fields
        # dict
        if self.prereq_combo.currentText() != self.fields['prerequisites']:
            self.value_updated.emit({"requirements": self.read()})

    def write(self, fields: dict) -> None:
        self.fields = fields
        self.prereq_combo.activated.disconnect()
        self.prereq_combo.clear()
        self.prereq_combo.addItems([''])
        self.prereq_combo.addItems(fields['challenges'])
        self.prereq_combo.setCurrentIndex(self.prereq_combo.findText(fields['prerequisites'], Qt.MatchExactly))
        self.prereq_combo.activated.connect(self.update)
