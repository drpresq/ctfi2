from collections import OrderedDict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory

COUNTRIES_LIST = [
    ("", ""),
    ("AF", "Afghanistan"),
    ("AX", "Åland Islands"),
    ("AL", "Albania"),
    ("DZ", "Algeria"),
    ("AS", "American Samoa"),
    ("AD", "Andorra"),
    ("AO", "Angola"),
    ("AI", "Anguilla"),
    ("AQ", "Antarctica"),
    ("AG", "Antigua & Barbuda"),
    ("AR", "Argentina"),
    ("AM", "Armenia"),
    ("AW", "Aruba"),
    ("AC", "Ascension Island"),
    ("AU", "Australia"),
    ("AT", "Austria"),
    ("AZ", "Azerbaijan"),
    ("BS", "Bahamas"),
    ("BH", "Bahrain"),
    ("BD", "Bangladesh"),
    ("BB", "Barbados"),
    ("BY", "Belarus"),
    ("BE", "Belgium"),
    ("BZ", "Belize"),
    ("BJ", "Benin"),
    ("BM", "Bermuda"),
    ("BT", "Bhutan"),
    ("BO", "Bolivia"),
    ("BA", "Bosnia & Herzegovina"),
    ("BW", "Botswana"),
    ("BR", "Brazil"),
    ("IO", "British Indian Ocean Territory"),
    ("VG", "British Virgin Islands"),
    ("BN", "Brunei"),
    ("BG", "Bulgaria"),
    ("BF", "Burkina Faso"),
    ("BI", "Burundi"),
    ("KH", "Cambodia"),
    ("CM", "Cameroon"),
    ("CA", "Canada"),
    ("IC", "Canary Islands"),
    ("CV", "Cape Verde"),
    ("BQ", "Caribbean Netherlands"),
    ("KY", "Cayman Islands"),
    ("CF", "Central African Republic"),
    ("EA", "Ceuta & Melilla"),
    ("TD", "Chad"),
    ("CL", "Chile"),
    ("CN", "China"),
    ("CX", "Christmas Island"),
    ("CC", "Cocos (Keeling) Islands"),
    ("CO", "Colombia"),
    ("KM", "Comoros"),
    ("CG", "Congo - Brazzaville"),
    ("CD", "Congo - Kinshasa"),
    ("CK", "Cook Islands"),
    ("CR", "Costa Rica"),
    ("CI", "Côte d’Ivoire"),
    ("HR", "Croatia"),
    ("CU", "Cuba"),
    ("CW", "Curaçao"),
    ("CY", "Cyprus"),
    ("CZ", "Czechia"),
    ("DK", "Denmark"),
    ("DG", "Diego Garcia"),
    ("DJ", "Djibouti"),
    ("DM", "Dominica"),
    ("DO", "Dominican Republic"),
    ("EC", "Ecuador"),
    ("EG", "Egypt"),
    ("SV", "El Salvador"),
    ("GQ", "Equatorial Guinea"),
    ("ER", "Eritrea"),
    ("EE", "Estonia"),
    ("ET", "Ethiopia"),
    ("EZ", "Eurozone"),
    ("FK", "Falkland Islands"),
    ("FO", "Faroe Islands"),
    ("FJ", "Fiji"),
    ("FI", "Finland"),
    ("FR", "France"),
    ("GF", "French Guiana"),
    ("PF", "French Polynesia"),
    ("TF", "French Southern Territories"),
    ("GA", "Gabon"),
    ("GM", "Gambia"),
    ("GE", "Georgia"),
    ("DE", "Germany"),
    ("GH", "Ghana"),
    ("GI", "Gibraltar"),
    ("GR", "Greece"),
    ("GL", "Greenland"),
    ("GD", "Grenada"),
    ("GP", "Guadeloupe"),
    ("GU", "Guam"),
    ("GT", "Guatemala"),
    ("GG", "Guernsey"),
    ("GN", "Guinea"),
    ("GW", "Guinea-Bissau"),
    ("GY", "Guyana"),
    ("HT", "Haiti"),
    ("HN", "Honduras"),
    ("HK", "Hong Kong SAR China"),
    ("HU", "Hungary"),
    ("IS", "Iceland"),
    ("IN", "India"),
    ("ID", "Indonesia"),
    ("IR", "Iran"),
    ("IQ", "Iraq"),
    ("IE", "Ireland"),
    ("IM", "Isle of Man"),
    ("IL", "Israel"),
    ("IT", "Italy"),
    ("JM", "Jamaica"),
    ("JP", "Japan"),
    ("JE", "Jersey"),
    ("JO", "Jordan"),
    ("KZ", "Kazakhstan"),
    ("KE", "Kenya"),
    ("KI", "Kiribati"),
    ("XK", "Kosovo"),
    ("KW", "Kuwait"),
    ("KG", "Kyrgyzstan"),
    ("LA", "Laos"),
    ("LV", "Latvia"),
    ("LB", "Lebanon"),
    ("LS", "Lesotho"),
    ("LR", "Liberia"),
    ("LY", "Libya"),
    ("LI", "Liechtenstein"),
    ("LT", "Lithuania"),
    ("LU", "Luxembourg"),
    ("MO", "Macau SAR China"),
    ("MK", "Macedonia"),
    ("MG", "Madagascar"),
    ("MW", "Malawi"),
    ("MY", "Malaysia"),
    ("MV", "Maldives"),
    ("ML", "Mali"),
    ("MT", "Malta"),
    ("MH", "Marshall Islands"),
    ("MQ", "Martinique"),
    ("MR", "Mauritania"),
    ("MU", "Mauritius"),
    ("YT", "Mayotte"),
    ("MX", "Mexico"),
    ("FM", "Micronesia"),
    ("MD", "Moldova"),
    ("MC", "Monaco"),
    ("MN", "Mongolia"),
    ("ME", "Montenegro"),
    ("MS", "Montserrat"),
    ("MA", "Morocco"),
    ("MZ", "Mozambique"),
    ("MM", "Myanmar (Burma)"),
    ("NA", "Namibia"),
    ("NR", "Nauru"),
    ("NP", "Nepal"),
    ("NL", "Netherlands"),
    ("NC", "New Caledonia"),
    ("NZ", "New Zealand"),
    ("NI", "Nicaragua"),
    ("NE", "Niger"),
    ("NG", "Nigeria"),
    ("NU", "Niue"),
    ("NF", "Norfolk Island"),
    ("KP", "North Korea"),
    ("MP", "Northern Mariana Islands"),
    ("NO", "Norway"),
    ("OM", "Oman"),
    ("PK", "Pakistan"),
    ("PW", "Palau"),
    ("PS", "Palestinian Territories"),
    ("PA", "Panama"),
    ("PG", "Papua New Guinea"),
    ("PY", "Paraguay"),
    ("PE", "Peru"),
    ("PH", "Philippines"),
    ("PN", "Pitcairn Islands"),
    ("PL", "Poland"),
    ("PT", "Portugal"),
    ("PR", "Puerto Rico"),
    ("QA", "Qatar"),
    ("RE", "Réunion"),
    ("RO", "Romania"),
    ("RU", "Russia"),
    ("RW", "Rwanda"),
    ("WS", "Samoa"),
    ("SM", "San Marino"),
    ("ST", "São Tomé & Príncipe"),
    ("SA", "Saudi Arabia"),
    ("SN", "Senegal"),
    ("RS", "Serbia"),
    ("SC", "Seychelles"),
    ("SL", "Sierra Leone"),
    ("SG", "Singapore"),
    ("SX", "Sint Maarten"),
    ("SK", "Slovakia"),
    ("SI", "Slovenia"),
    ("SB", "Solomon Islands"),
    ("SO", "Somalia"),
    ("ZA", "South Africa"),
    ("GS", "South Georgia & South Sandwich Islands"),
    ("KR", "South Korea"),
    ("SS", "South Sudan"),
    ("ES", "Spain"),
    ("LK", "Sri Lanka"),
    ("BL", "St. Barthélemy"),
    ("SH", "St. Helena"),
    ("KN", "St. Kitts & Nevis"),
    ("LC", "St. Lucia"),
    ("MF", "St. Martin"),
    ("PM", "St. Pierre & Miquelon"),
    ("VC", "St. Vincent & Grenadines"),
    ("SD", "Sudan"),
    ("SR", "Suriname"),
    ("SJ", "Svalbard & Jan Mayen"),
    ("SZ", "Swaziland"),
    ("SE", "Sweden"),
    ("CH", "Switzerland"),
    ("SY", "Syria"),
    ("TW", "Taiwan"),
    ("TJ", "Tajikistan"),
    ("TZ", "Tanzania"),
    ("TH", "Thailand"),
    ("TL", "Timor-Leste"),
    ("TG", "Togo"),
    ("TK", "Tokelau"),
    ("TO", "Tonga"),
    ("TT", "Trinidad & Tobago"),
    ("TA", "Tristan da Cunha"),
    ("TN", "Tunisia"),
    ("TR", "Turkey"),
    ("TM", "Turkmenistan"),
    ("TC", "Turks & Caicos Islands"),
    ("TV", "Tuvalu"),
    ("UM", "U.S. Outlying Islands"),
    ("VI", "U.S. Virgin Islands"),
    ("UG", "Uganda"),
    ("UA", "Ukraine"),
    ("AE", "United Arab Emirates"),
    ("GB", "United Kingdom"),
    ("US", "United States"),
    ("UY", "Uruguay"),
    ("UZ", "Uzbekistan"),
    ("VU", "Vanuatu"),
    ("VA", "Vatican City"),
    ("VE", "Venezuela"),
    ("VN", "Vietnam"),
    ("WF", "Wallis & Futuna"),
    ("EH", "Western Sahara"),
    ("YE", "Yemen"),
    ("ZM", "Zambia"),
    ("ZW", "Zimbabwe"),
]

# Nicely titled (and translatable) country names.
COUNTRIES_DICT = OrderedDict(COUNTRIES_LIST)


class UserWidget(QDialog):
    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(UserWidget, self).__init__()
        self.fields: dict = {}
        self.dialog: bool = dialog

        self.setWindowTitle("New User")
        self.setGeometry(200, 200, 400, 100)

        self.update_pause: bool = True

        name_box, self.name_line = ComponentFactory.box_line_edit(text="Username",
                                                                  place_holder="Enter a Username",
                                                                  alignment=None,
                                                                  orientation=Qt.AlignHorizontal_Mask)

        email_box, self.email_line = ComponentFactory.box_line_edit(text="Email Address",
                                                                    place_holder="user@domain.net",
                                                                    alignment=None,
                                                                    orientation=Qt.AlignHorizontal_Mask)

        password_box, self.password_line = ComponentFactory.box_line_edit(text="Password",
                                                                          place_holder="Enter Password",
                                                                          alignment=None,
                                                                          orientation=Qt.AlignHorizontal_Mask)
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_button = ComponentFactory.push_button("show", (40, 30))
        self.password_button.clicked.connect(self.toggle_password)
        password_box.addWidget(self.password_button)

        website_box, self.website_line = ComponentFactory.box_line_edit(text="Website",
                                                                        place_holder="http://mysite.io",
                                                                        alignment=None,
                                                                        orientation=Qt.AlignHorizontal_Mask)

        affiliation_box, self.affiliation_line = ComponentFactory.box_line_edit(text="Affiliation",
                                                                                place_holder=None,
                                                                                alignment=None,
                                                                                orientation=Qt.AlignHorizontal_Mask)

        country_box, self.country_combo = ComponentFactory.box_combo_box(text="Country",
                                                                         choices=list(COUNTRIES_DICT.values()),
                                                                         alignment=None,
                                                                         orientation=Qt.AlignHorizontal_Mask)

        type_box, self.type_combo = ComponentFactory.box_combo_box(text="Type",
                                                                   choices=["user", "admin"],
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        verified_box, self.verified_check = ComponentFactory.box_check_box(text="Verified",
                                                                           default=False,
                                                                           alignment=None,
                                                                           orientation=Qt.AlignVertical_Mask)

        hidden_box, self.hidden_check = ComponentFactory.box_check_box(text="Hidden",
                                                                       default=False,
                                                                       alignment=None,
                                                                       orientation=Qt.AlignVertical_Mask)

        banned_box, self.banned_check = ComponentFactory.box_check_box(text="Banned",
                                                                       default=False,
                                                                       alignment=None,
                                                                       orientation=Qt.AlignVertical_Mask)
        check_box_box = QHBoxLayout()
        check_box_box.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        for layout in [verified_box, hidden_box, banned_box]:
            check_box_box.addLayout(layout)

        self.outer_box: QVBoxLayout = QVBoxLayout()
        for layout in [name_box, email_box, password_box, website_box,
                       affiliation_box, country_box, type_box, check_box_box]:
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
            self.name_line.textEdited.connect(self.update)
            self.email_line.textEdited.connect(self.update)
            self.password_line.textEdited.connect(self.update)
            self.website_line.textEdited.connect(self.update)
            self.affiliation_line.textEdited.connect(self.update)
            self.country_combo.currentIndexChanged.connect(self.update)
            self.type_combo.currentIndexChanged.connect(self.update)
            self.verified_check.stateChanged.connect(self.update)
            self.hidden_check.stateChanged.connect(self.update)
            self.banned_check.stateChanged.connect(self.update)

    def toggle_password(self) -> None:
        if self.password_line.echoMode() == QLineEdit.Password:
            self.password_line.setEchoMode(QLineEdit.Normal)
            self.password_button.setText("hide")
        else:
            self.password_line.setEchoMode(QLineEdit.Password)
            self.password_button.setText("show")

    def cancelled(self) -> None:
        for text_line in [self.name_line, self.email_line, self.password_line,
                          self.website_line, self.affiliation_line]:
            text_line.setText('')
        for combo_box in [self.country_combo, self.type_combo]:
            combo_box.setCurrentIndex(0)
        for check_box in [self.verified_check, self.hidden_check, self.banned_check]:
            check_box.setChecked(False)
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def clear(self) -> None:
        self.cancelled()

    def read(self) -> dict:
        self.fields.update({'name': self.name_line.text(),
                            'email': self.email_line.text() if self.email_line.text()
                            else '{}@ctfd.io'.format(self.name_line.text()),
                            'password': self.password_line.text(),
                            'website': self.website_line.text(),
                            'affiliation': self.affiliation_line.text(),
                            'country': [key for key, value in COUNTRIES_DICT.items()
                                        if value == self.country_combo.currentText()][0]
                            if self.country_combo.currentText() else '',
                            'type': self.type_combo.currentText(),
                            'verified': True if self.verified_check.checkState() > 0 else False,
                            'hidden': True if self.hidden_check.checkState() > 0 else False,
                            'banned': True if self.banned_check.checkState() > 0 else False})
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
        self.name_line.setText(fields['name'])
        self.email_line.setText(fields['email'])
        self.password_line.setText(fields['password'])
        self.website_line.setText(fields['website'])
        self.affiliation_line.setText(fields['affiliation'])
        self.country_combo.setCurrentIndex(self.country_combo.findText(COUNTRIES_DICT[fields['country']], Qt.MatchExactly)) if fields['country'] else None
        self.type_combo.setCurrentIndex(self.type_combo.findText(fields['type'], Qt.MatchExactly))
        self.verified_check.setChecked(True if fields['verified'] and int(fields['verified']) > 0 else False)
        self.hidden_check.setChecked(True if fields['hidden'] and int(fields['hidden']) > 0 else False)
        self.banned_check.setChecked(True if fields['banned'] and int(fields['banned']) > 0 else False)

        self.update_pause = False
