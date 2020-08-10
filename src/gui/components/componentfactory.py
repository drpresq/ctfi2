from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ComponentFactory:
    @staticmethod
    def label(text: str) -> QLabel:
        label = QLabel()
        label.setText(text)
        return label

    @staticmethod
    def line_edit(place_holder: str, default_value: str) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(place_holder) if place_holder else None
        line_edit.setText(default_value) if default_value else None
        return line_edit

    @staticmethod
    def combo_box(choices: list) -> QComboBox:
        combo_box = QComboBox()
        combo_box.addItems(choices)
        return combo_box

    @staticmethod
    def check_box(default: bool) -> QCheckBox:
        check_box = QCheckBox()
        check_box.setChecked(default if default else False)
        return check_box

    @staticmethod
    def text_edit(place_holder: str, default_value: str) -> QTextEdit:
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(place_holder) if place_holder else None
        text_edit.setText(default_value) if default_value else None
        return text_edit 

    @staticmethod
    def push_button(label: str, size: (int, int) = None) -> QPushButton:
        push_button = QPushButton(label)
        if size:
            push_button.setMaximumSize(size[0], size[1])
        return push_button

    @staticmethod
    def spin_box(minimum: int, maximum: int, step: int) -> QSpinBox:
        spin_box = QSpinBox()
        spin_box.setMinimum(minimum) if minimum else None
        spin_box.setMaximum(maximum) if maximum else None
        spin_box.setSingleStep(step) if step else None
        return spin_box

    @staticmethod
    def date_edit(date: QDateTime) -> QDateEdit:
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDateTime(date) if date else None
        return date_edit

    @staticmethod
    def tree_view() -> QTreeWidget:
        return QTreeWidget()

    @staticmethod
    def box_line_edit(text: str, place_holder: str = None, default_value: str = None,
                      alignment: QtCore.Qt.AlignmentFlag = None,
                      orientation: QtCore.Qt.AlignmentFlag = None) -> (QHBoxLayout, QLineEdit):
        label: QLabel = ComponentFactory.label(text)
        line_edit: QLineEdit = ComponentFactory.line_edit(place_holder, default_value)
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [label, line_edit]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, line_edit

    @staticmethod
    def box_text_edit(text: str, place_holder: str = None, default_value: str = None,
                      alignment: QtCore.Qt.AlignmentFlag = None,
                      orientation: QtCore.Qt.AlignmentFlag = None) -> (QHBoxLayout, QTextEdit):
        label: QLabel = ComponentFactory.label(text)
        text_edit: QTextEdit = ComponentFactory.text_edit(place_holder, default_value)
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [label, text_edit]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, text_edit

    @staticmethod
    def box_check_box(text: str, default: bool,
                      alignment: QtCore.Qt.AlignmentFlag = None,
                      orientation: QtCore.Qt.AlignmentFlag = None) -> (QLayout, QCheckBox):
        label: QLabel = ComponentFactory.label(text)
        check_box: QCheckBox = ComponentFactory.check_box(default if default else False)
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [check_box, label] if orientation == Qt.AlignVertical_Mask else [label, check_box]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, check_box

    @staticmethod
    def box_buttons(button_names: [str],
                    alignment: QtCore.Qt.AlignmentFlag = None,
                    orientation: QtCore.Qt.AlignmentFlag = None) -> (QLayout, {str: QPushButton}):
        buttons: dict = {}
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for button in button_names:
            buttons.update({button: QPushButton(button)})
            layout.addWidget(buttons[button])
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, buttons

    @staticmethod
    def box_combo_box(text: str, choices: [str],
                      alignment: QtCore.Qt.AlignmentFlag = None,
                      orientation: QtCore.Qt.AlignmentFlag = None) -> (QLayout, QComboBox):
        label = ComponentFactory.label(text)
        combo_box = ComponentFactory.combo_box(choices)
        combo_box.setCurrentIndex(0)
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [label, combo_box]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, combo_box

    @staticmethod
    def box_spin_box(text: str, minimum: int = None, maximum: int = None, step: int = None,
                     alignment: QtCore.Qt.AlignmentFlag = None,
                     orientation: QtCore.Qt.AlignmentFlag = None) -> (QLayout, QSpinBox):
        label = ComponentFactory.label(text)
        spin_box = ComponentFactory.spin_box(minimum, maximum, step)
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [label, spin_box]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, spin_box

    @staticmethod
    def box_tree_view(text: str,
                      alignment: QtCore.Qt.AlignmentFlag = None,
                      orientation: QtCore.Qt.AlignmentFlag = None) -> (QLayout, QTreeWidget):
        label = ComponentFactory.label(text)
        tree_view = ComponentFactory.tree_view()
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [label, tree_view]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, tree_view

    @staticmethod
    def box_date_edit(text: str, default_value: str = None,
                      alignment: QtCore.Qt.AlignmentFlag = None,
                      orientation: QtCore.Qt.AlignmentFlag = None) -> (QHBoxLayout, QLineEdit):
        label: QLabel = ComponentFactory.label(text)
        date_edit: QDateEdit = ComponentFactory.date_edit(QDateTime().fromSecsSinceEpoch(int(default_value))
                                                          if default_value else None)
        layout = QVBoxLayout() if orientation == Qt.AlignVertical_Mask else QHBoxLayout()
        for widget in [label, date_edit]:
            layout.addWidget(widget)
        if isinstance(alignment, QtCore.Qt.AlignmentFlag):
            layout.setAlignment(alignment)
        return layout, date_edit
