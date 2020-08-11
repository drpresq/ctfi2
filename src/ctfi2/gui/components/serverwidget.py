from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory


class ServerWidget(QDialog):
    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(ServerWidget, self).__init__()
        self.fields: dict = {}
        self.dialog: bool = dialog

        self.setWindowTitle("Server")
        self.setGeometry(200, 200, 400, 100)

        self.update_pause: bool = True

        server_box, self.server_line = ComponentFactory.box_line_edit(text="Server Url",
                                                                      place_holder=None,
                                                                      default_value="http://localhost:8000",
                                                                      alignment=None,
                                                                      orientation=Qt.AlignHorizontal_Mask)

        admin_box, self.admin_line = ComponentFactory.box_line_edit(text="Admin Username",
                                                                    place_holder=None,
                                                                    default_value='root',
                                                                    alignment=None,
                                                                    orientation=Qt.AlignHorizontal_Mask)

        password_box, self.password_line = ComponentFactory.box_line_edit(text="Admin Password",
                                                                          place_holder=None,
                                                                          default_value='toor',
                                                                          alignment=None,
                                                                          orientation=Qt.AlignHorizontal_Mask)
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_button = ComponentFactory.push_button("show", (40, 30))
        self.password_button.clicked.connect(self.toggle_password)
        password_box.addWidget(self.password_button)

        name_box, self.name_line = ComponentFactory.box_line_edit(text="CTF Name",
                                                                  place_holder=None,
                                                                  default_value='CTFd',
                                                                  alignment=None,
                                                                  orientation=Qt.AlignHorizontal_Mask)

        description_box, self.description_text = ComponentFactory.box_text_edit(text="Description",
                                                                                place_holder=None,
                                                                                default_value='This Competition was created with ctfi2',
                                                                                alignment=None,
                                                                                orientation=Qt.AlignHorizontal_Mask)

        mode_box, self.mode_combo = ComponentFactory.box_combo_box(text="Mode",
                                                                   choices=list(['users', 'teams']),
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        theme_box, self.theme_combo = ComponentFactory.box_combo_box(text="Theme",
                                                                     choices=["core"],
                                                                     alignment=None,
                                                                     orientation=Qt.AlignHorizontal_Mask)

        start_box, self.start_date = ComponentFactory.box_date_edit(text="Start Date",
                                                                    default_value=str(
                                                                        QDateTime().currentDateTime().toSecsSinceEpoch() + 604800),
                                                                    alignment=None,
                                                                    orientation=Qt.AlignHorizontal_Mask)

        end_box, self.end_date = ComponentFactory.box_date_edit(text="End Date",
                                                                default_value=str(
                                                                    QDateTime().currentDateTime().toSecsSinceEpoch() + 1209600),
                                                                alignment=None,
                                                                orientation=Qt.AlignHorizontal_Mask)

        score_box, self.score_combo = ComponentFactory.box_combo_box(text="Score Visibility",
                                                                     choices=['public', 'private'],
                                                                     alignment=None,
                                                                     orientation=Qt.AlignHorizontal_Mask)

        user_box, self.user_combo = ComponentFactory.box_combo_box(text="User Visibility",
                                                                   choices=['public', 'private'],
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        self.outer_box: QVBoxLayout = QVBoxLayout()
        for layout in [server_box, admin_box, password_box, name_box, description_box, mode_box, theme_box,
                       start_box, end_box, score_box, user_box]:
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
            self.server_line.textEdited.connect(self.update)
            self.admin_line.textEdited.connect(self.update)
            self.password_line.textEdited.connect(self.update)
            self.description_text.textChanged.connect(self.update)
            self.mode_combo.currentIndexChanged.connect(self.update)
            self.theme_combo.currentIndexChanged.connect(self.update)
            self.start_date.dateChanged.connect(self.update)
            self.end_date.dateChanged.connect(self.update)
            self.score_combo.currentIndexChanged.connect(self.update)
            self.user_combo.currentIndexChanged.connect(self.update)

    def toggle_password(self) -> None:
        if self.password_line.echoMode() == QLineEdit.Password:
            self.password_line.setEchoMode(QLineEdit.Normal)
            self.password_button.setText("hide")
        else:
            self.password_line.setEchoMode(QLineEdit.Password)
            self.password_button.setText("show")

    def cancelled(self) -> None:
        self.server_line.setText('')
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def clear(self) -> None:
        self.cancelled()

    def read(self) -> dict:
        self.fields.update({"url_prefix": self.server_line.text(),
                            "name": self.admin_line.text(),
                            "password": self.password_line.text(),
                            "ctf_name": self.name_line.text(),
                            "ctf_description": self.description_text.toPlainText(),
                            "user_mode": self.mode_combo.currentText(),
                            "ctf_theme": self.theme_combo.currentText(),
                            "start": self.start_date.dateTime().toSecsSinceEpoch(),
                            "end": self.end_date.dateTime().toSecsSinceEpoch(),
                            "score_visibility": self.score_combo.currentText(),
                            "account_visibility": self.user_combo.currentText()})
        ret_dict: dict = self.fields
        if self.dialog:
            self.clear()
        return ret_dict

    def update(self) -> None:
        """ Signals that a data field value was changed """
        # This is the set_fields function in reverse where we write data from the user edited widget into our fields
        # dict
        if not self.update_pause:
            self.value_updated.emit({"server": self.read()})

    def write(self, fields: dict) -> None:
        self.update_pause = True

        self.fields = fields
        self.server_line.setText(fields["url_prefix"])
        self.admin_line.setText(fields["name"])
        self.password_line.setText(fields["password"])
        self.name_line.setText(fields["ctf_name"])
        self.description_text.setPlainText(fields["ctf_description"])
        self.mode_combo.setCurrentIndex(self.mode_combo.findText(fields["user_mode"], Qt.MatchExactly))
        self.theme_combo.setCurrentIndex(self.theme_combo.findText(fields["ctf_theme"], Qt.MatchExactly))
        self.start_date.setDateTime(QDateTime().fromSecsSinceEpoch(int(fields["start"])))
        self.end_date.setDateTime(QDateTime().fromSecsSinceEpoch(int(fields["end"])))
        self.score_combo.setCurrentIndex(self.score_combo.findText(fields["score_visibility"], Qt.MatchExactly))
        self.user_combo.setCurrentIndex(self.user_combo.findText(fields["account_visibility"], Qt.MatchExactly))

        self.update_pause = False
