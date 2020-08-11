from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory


class HintWidget(QDialog):
    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(QDialog, self).__init__()

        self.fields: dict = {}
        self.dialog: bool = dialog

        self.setWindowTitle("New Hint")
        self.setGeometry(200, 200, 400, 100)

        self.update_pause: bool = True

        content_box, self.content_line = ComponentFactory.box_line_edit(text="Hint",
                                                                        place_holder="Enter Hint",
                                                                        alignment=None,
                                                                        orientation=Qt.AlignHorizontal_Mask)

        cost_box, self.cost_line = ComponentFactory.box_line_edit(text='Cost',
                                                                  place_holder='Enter Hint Cost',
                                                                  alignment=None,
                                                                  orientation=Qt.AlignHorizontal_Mask)

        self.outer_box = QVBoxLayout()
        self.outer_box.setAlignment(Qt.AlignTop)

        for layout in [content_box, cost_box]:
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
            self.content_line.textEdited.connect(self.update)
            self.cost_line.textEdited.connect(self.update)

    def cancelled(self) -> None:
        self.content_line.setText('')
        self.cost_line.setText('')
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def clear(self) -> None:
        self.cancelled()

    def read(self) -> dict:
        self.fields.update({'content': self.content_line.text()})
        try:
            self.fields.update({'cost': int(self.cost_line.text())})
        except:
            self.fields.update({'cost': 0})
        ret_dict: dict = self.fields
        if self.dialog:
            self.clear()
        return ret_dict

    def update(self) -> None:
        """ Signals that a data field value was changed """
        # This is the set_fields function in reverse where we write data from the user edited widget into our fields
        # dict
        if not self.update_pause:
            self.value_updated.emit({"users": self.read()})

    def write(self, fields: dict) -> None:
        self.update_pause = True

        self.fields = fields
        self.fields.update({'challenge': fields['challenge_id']})
        self.content_line.setText(fields['content'])
        self.cost_line.setText(str(fields['cost']))

        self.update_pause = False
