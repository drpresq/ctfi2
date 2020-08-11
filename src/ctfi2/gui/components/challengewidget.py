from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctfi2.gui.components.componentfactory import ComponentFactory
from ctfi2.gui.components.requirementwidget import RequirementWidget


class ChallengeWidget(QDialog):
    value_updated: pyqtSignal = pyqtSignal(dict)

    def __init__(self, dialog: bool = True):
        super(ChallengeWidget, self).__init__()
        self.fields: dict = {}
        self.dialog: bool = dialog

        self.setWindowTitle("New Challenge")
        self.setGeometry(200, 200, 400, 100)

        self.update_pause = True

        name_box, self.name_line = ComponentFactory.box_line_edit(text="Name",
                                                                  place_holder="Challenge Name",
                                                                  alignment=None,
                                                                  orientation=Qt.AlignHorizontal_Mask)

        description_box, self.description_text = ComponentFactory.box_text_edit(text="Description",
                                                                                place_holder="Challenge Description",
                                                                                alignment=None,
                                                                                orientation=Qt.AlignHorizontal_Mask)
        self.description_text.setMaximumHeight(250)

        category_box, self.category_line = ComponentFactory.box_line_edit(text="Category",
                                                                          place_holder="Challenge Category (Optional)",
                                                                          alignment=None,
                                                                          orientation=Qt.AlignHorizontal_Mask)

        value_box, self.value_spin = ComponentFactory.box_spin_box(text="Value",
                                                                   minimum=0,
                                                                   maximum=255,
                                                                   step=1,
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        attempts_box, self.attempts_spin = ComponentFactory.box_spin_box(text="Max Attempts",
                                                                         minimum=0,
                                                                         maximum=255,
                                                                         step=1,
                                                                         alignment=None,
                                                                         orientation=Qt.AlignHorizontal_Mask)

        country_box, self.country_combo = ComponentFactory.box_combo_box(text="Country",
                                                                         choices=list(),
                                                                         alignment=None,
                                                                         orientation=Qt.AlignHorizontal_Mask)

        type_box, self.type_combo = ComponentFactory.box_combo_box(text="Type",
                                                                   choices=["standard"],
                                                                   alignment=None,
                                                                   orientation=Qt.AlignHorizontal_Mask)

        state_box, self.state_combo = ComponentFactory.box_combo_box(text="Visibility",
                                                                     choices=['visible', 'hidden'],
                                                                     alignment=None,
                                                                     orientation=Qt.AlignHorizontal_Mask)

        requirements_box, self.requirements_tree = ComponentFactory.box_tree_view(text='Prerequisites',
                                                                                  alignment=None,
                                                                                  orientation=Qt.AlignHorizontal_Mask)

        requirement_button_box, requirement_buttons = ComponentFactory.box_buttons(button_names=['Add',
                                                                                                 'Remove'],
                                                                                   alignment=None,
                                                                                   orientation=Qt.AlignHorizontal_Mask)
        requirement_buttons['Add'].clicked.connect(self.requirement_add)
        requirement_buttons['Remove'].clicked.connect(self.requirement_remove)

        value_box.setAlignment(Qt.AlignLeft)
        attempts_box.setAlignment(Qt.AlignRight)
        value_attempts_box = QHBoxLayout()
        value_attempts_box.setAlignment(Qt.AlignTop)
        for layout in [value_box, attempts_box]:
            value_attempts_box.addLayout(layout)

        type_box.setAlignment(Qt.AlignLeft)
        state_box.setAlignment(Qt.AlignRight)
        type_state_box = QHBoxLayout()
        type_state_box.setAlignment(Qt.AlignTop)
        for layout in [type_box, state_box]:
            type_state_box.addLayout(layout)

        self.outer_box: QVBoxLayout = QVBoxLayout()
        self.outer_box.setAlignment(Qt.AlignTop)
        for layout in [name_box, description_box, category_box, value_attempts_box,
                       type_state_box, requirements_box, requirement_button_box]:
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
            self.description_text.textChanged.connect(self.update)
            self.category_line.textEdited.connect(self.update)
            self.value_spin.valueChanged.connect(self.update)
            self.attempts_spin.valueChanged.connect(self.update)
            self.type_combo.currentIndexChanged.connect(self.update)
            self.state_combo.currentIndexChanged.connect(self.update)

        self.new_requirement_dialog = RequirementWidget()
        self.requirements_tree.setHeaderHidden(True)

    def requirement_tree_fill(self):
        self.requirements_tree.clear()
        for requirement in self.fields['requirements']['prerequisites']:
            node = QTreeWidgetItem()
            try:
                name = next(iter([item['name'] for item in self.fields['challenges'] if item['id'] == requirement]))
            except:
                break
            node.setText(0, name)
            self.requirements_tree.addTopLevelItem(node)

    def requirement_add(self):
        self.fields['requirements'] = {'prerequisites': []} if 'requirements' not in self.fields.keys() else self.fields['requirements']
        if 'id' in self.fields.keys():
            challenges = [item['name'] for item in self.fields['challenges']
                          if item['id'] != self.fields['id']
                          and item['id'] not in self.fields['requirements']['prerequisites']]
        else:
            challenges = [item['name'] for item in self.fields['challenges']
                          if item['id'] not in self.fields['requirements']['prerequisites']]

        self.new_requirement_dialog.prereq_combo.addItems(challenges)
        self.new_requirement_dialog.exec_()

        new_requirement: dict = self.new_requirement_dialog.read()
        if new_requirement['prerequisites']:
            if not isinstance(self.fields['requirements']['prerequisites'], list):
                self.fields['requirements']['prerequisites'] = []
            self.fields['requirements']['prerequisites'].append(next(iter([item['id'] for item in self.fields['challenges']
                                                          if item['name'] == new_requirement['prerequisites']])))
            self.requirement_tree_fill()
            self.update()

    def requirement_remove(self):
        selected = self.requirements_tree.selectedItems()
        if selected:
            for item in selected:
                self.fields['requirements']['prerequisites'].pop(self.fields['requirements']['prerequisites'].index(next(iter([chal['id'] for chal in self.fields['challenges'] if item.text(0) == chal['name']]))))
        self.requirement_tree_fill()

    def cancelled(self) -> None:
        for text_line in [self.name_line, self.description_text, self.category_line]:
            text_line.setText('')
        for combo_box in [self.state_combo, self.type_combo]:
            combo_box.setCurrentIndex(0)
        for spin_box in [self.attempts_spin, self.value_spin]:
            spin_box.setValue(0)
        self.requirements_tree.clear()
        self.close()

    def ok_clicked(self) -> None:
        self.close()

    def clear(self) -> None:
        self.cancelled()

    def read(self) -> dict:
        desc_text = self.description_text.toPlainText().replace(',', '')

        self.fields.update({'name': self.name_line.text(),
                            'description': desc_text,
                            'category': self.category_line.text(),
                            'max_attempts': self.attempts_spin.value() if self.attempts_spin.value() else 0,
                            'value': self.value_spin.value() if self.value_spin.value() else 0,
                            'type': self.type_combo.currentText(),
                            'state': self.state_combo.currentText()})
        ret_dict: dict = self.fields
        if self.dialog:
            self.clear()
        return ret_dict

    def update(self) -> None:
        """ Signals that a data field value was changed """
        # This is the set_fields function in reverse where we write data from the user edited widget into our fields
        # dict
        if not self.update_pause:
            self.value_updated.emit({"challenges": self.read()})

    def write(self, fields: dict) -> None:
        self.update_pause = True

        self.fields = fields
        if 'requirements' in self.fields.keys() and not isinstance(self.fields['requirements'], (list, dict)) and len(self.fields['requirements']) >= 1:
            self.fields['requirements'] = {'prerequisites': self.fields['requirements'].split('[')[1].split(']')[0].split(',')}
        elif 'requirements' in self.fields.keys() and isinstance(self.fields['requirements'], list):
            self.fields['requirements'] = {'prerequisites': self.fields['requirements']}
        elif 'requirements' in self.fields.keys() and isinstance(self.fields['requirements'], dict):
            pass
        else:
            self.fields['requirements'] = {'prerequisites': []}
        self.name_line.setText(fields['name'])
        self.description_text.setText(fields['description'])
        self.category_line.setText(fields['category'])
        self.value_spin.setValue(int(fields['value']))
        self.attempts_spin.setValue(int(fields['max_attempts']))
        self.type_combo.setCurrentIndex(self.type_combo.findText(fields['type'], Qt.MatchExactly))
        self.state_combo.setCurrentIndex(self.state_combo.findText(fields['state'], Qt.MatchExactly))
        self.requirement_tree_fill()

        self.update_pause = False
