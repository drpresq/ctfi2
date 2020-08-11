from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory


class UserImportWidget(QDialog):
    """File selector widget with tweaks stolen from the Reproducible Experiment System
    (https://github.com/raistlinj/res) """

    def __init__(self):
        super(QWidget, self).__init__()

        self.setWindowTitle("Import Users")
        self.setGeometry(200, 200, 400, 100)

        file_box, self.file_line = ComponentFactory.box_line_edit(text="",
                                                                  place_holder="Select CSV file containing your users",
                                                                  alignment=None,
                                                                  orientation=Qt.AlignHorizontal_Mask)
        select_file_button = ComponentFactory.push_button("...", (30, 30))
        select_file_button.clicked.connect(self.open_file_dialog)
        file_box.addWidget(select_file_button)

        generic_box, self.generic_spin = ComponentFactory.box_spin_box(text='Number of additional generic users',
                                                                       minimum=0,
                                                                       maximum=50,
                                                                       step=1,
                                                                       alignment=None,
                                                                       orientation=Qt.AlignHorizontal_Mask)

        button_box, buttons = ComponentFactory.box_buttons(button_names=["Ok", "Cancel"],
                                                           alignment=Qt.AlignRight,
                                                           orientation=Qt.AlignHorizontal_Mask)
        buttons['Ok'].clicked.connect(self.ok_clicked)
        buttons['Cancel'].clicked.connect(self.cancelled)

        self.outer_box = QVBoxLayout()
        for layout in [file_box, generic_box, button_box]:
            self.outer_box.addLayout(layout)

        self.setLayout(self.outer_box)

    def open_file_dialog(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(QFileDialog(), "Choose a File", "", "CSV/TXT (*.csv *.txt)")
        self.file_line.setText(filename if filename else None)

    def read(self) -> (str, int):
        filename: str = self.file_line.text()
        generic_quantity: int = self.generic_spin.value()
        self.clear()
        return filename if filename and isinstance(filename, str) and filename.strip() != "" else '', \
            generic_quantity

    def clear(self) -> None:
        self.cancelled()

    def cancelled(self) -> None:
        self.file_line.setText('')
        self.generic_spin.setValue(0)
        self.close()

    def ok_clicked(self) -> None:
        self.close()
