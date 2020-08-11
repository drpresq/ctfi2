from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory


class FileWidget(QDialog):
    """File selector widget with tweaks stolen from the Reproducible Experiment System (
    https://github.com/raistlinj/res) """

    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(QWidget, self).__init__()

        self.dialog = dialog
        self.fields: dict = {}

        self.setWindowTitle("Add a new File")
        self.setGeometry(200, 200, 400, 100)

        self.update_pause: bool = True

        file_box, self.file_line = ComponentFactory.box_line_edit(text="",
                                                                  place_holder="Choose a File",
                                                                  alignment=None,
                                                                  orientation=Qt.AlignHorizontal_Mask)

        select_file_button = ComponentFactory.push_button("...", (30, 30))
        select_file_button.clicked.connect(self.open_file_dialog)
        file_box.addWidget(select_file_button)

        location_box, self.location_line = ComponentFactory.box_line_edit(text="",
                                                                          place_holder=None,
                                                                          alignment=None,
                                                                          orientation=Qt.AlignHorizontal_Mask)
        self.file_line.setReadOnly(True)
        self.location_line.setReadOnly(True)

        self.outer_box = QVBoxLayout()
        self.outer_box.setAlignment(Qt.AlignTop)
        self.outer_box.addLayout(file_box)

        self.setLayout(self.outer_box)

        if dialog:
            button_box, buttons = ComponentFactory.box_buttons(button_names=["Ok", "Cancel"],
                                                               alignment=Qt.AlignRight,
                                                               orientation=Qt.AlignHorizontal_Mask)
            buttons['Ok'].clicked.connect(self.ok_clicked)
            buttons['Cancel'].clicked.connect(self.cancelled)
            self.outer_box.addLayout(button_box)

        elif not dialog:
            self.outer_box.addLayout(location_box)
            self.file_line.textEdited.connect(self.update)

            button_copy_box, buttons_copy = ComponentFactory.box_buttons(button_names=['Copy MD',
                                                                                       'Copy HTML',
                                                                                       'Copy Text'],
                                                                         alignment=Qt.AlignCenter,
                                                                         orientation=Qt.AlignHorizontal_Mask)
            self.clipboard = QGuiApplication.clipboard()
            buttons_copy['Copy MD'].clicked.connect(self.copy_md)
            buttons_copy['Copy HTML'].clicked.connect(self.copy_html)
            buttons_copy['Copy Text'].clicked.connect(self.copy_text)
            self.outer_box.addLayout(button_copy_box)

    def copy_md(self) -> None:
        self.clipboard.setText('![{}](/files/{})'.format(self.location_line.text().split('/')[-1],self.location_line.text()))

    def copy_html(self) -> None:
        self.clipboard.setText('\r\n<html><img src="/files/{}" /img><html>\r\n'.format(self.location_line.text()))

    def copy_text(self) -> None:
        self.clipboard.setText('/files/{}'.format(self.location_line.text()))

    def open_file_dialog(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(QFileDialog(),
                                                  directory=self.file_line.text() if self.file_line.text() else None,
                                                  caption="Select a file",
                                                  filter="",
                                                  initialFilter="All (*.*)")
        self.file_line.setText(filename if filename else self.file_line.text() if self.file_line.text() else None)

    def read(self) -> dict:
        self.fields.update({'path': self.file_line.text()})
        ret_dict: dict = self.fields
        if self.dialog:
            self.clear()
        return ret_dict

    def clear(self):
        self.cancelled()

    def cancelled(self) -> None:
        self.fields = {}
        self.file_line.setText('')
        self.location_line.setText('')
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def update(self) -> None:
        """ Signals that a data field value was changed """
        # This is the set_fields function in reverse where we write data from the user edited widget into our fields
        # dict
        if not self.update_pause:
            self.value_updated.emit({"files": self.read()})

    def write(self, fields: dict) -> None:
        self.update_pause = True
        self.fields = fields
        self.file_line.setText(fields['path'] if fields['path'] else '')
        self.location_line.setText(fields['location'] if fields['location'] else '')

        self.update_pause = False
