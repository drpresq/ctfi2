import json
import logging
import os
import random
import string

from PyQt5.QtWidgets import *
from re import match

from ctfi2.api import FILE_PATH, pattern_email
from ctfi2.gui.components import TitleWidget, CompetitionTree, FileWidget, UserWidget, \
    FlagWidget, HintWidget, UserImportWidget, ChallengeWidget, ServerWidget
from ctfi2.configuration import Configuration


class CTFi2GUI(QWidget):
    competition_config_dict: {dict} = {}

    def __init__(self, parent: QWidget = None,
                 status_bar: QStatusBar = None) -> None:
        QWidget.__init__(self, parent)

        self.log("Instantiated.")
        self.setObjectName(self.__class__.__name__)
        self.status_bar = status_bar

        # Base Widget Layout

        self.base_layout: QHBoxLayout = QHBoxLayout()
        self.base_layout.setObjectName("windowBoxHLayout")
        self.setLayout(self.base_layout)

        # Context Menus

        self.blank_context_menu = QMenu()
        self.blank_context_menu.addAction("New Competition").triggered.connect(self.new_competition)

        self.competition_menu = QMenu()
        self.competition_menu.addAction("Rename Competition").triggered.connect(self.edit_competition)
        self.competition_menu.addAction("Remove Competition").triggered.connect(self.remove_competition)

        self.server_context_menu = QMenu()
        self.server_context_menu.addAction("Reset Server").triggered.connect(self.server_reset)
        self.server_context_menu.addAction("Wipe Server").triggered.connect(self.server_wipe)

        self.challenge_root_context_menu = QMenu()
        self.challenge_root_context_menu.addAction("Add Challenge").triggered.connect(self.add_challenge)
        self.challenge_root_context_menu.addAction("Sync Challenges").triggered.connect(self.challenge_sync)

        self.challenge_node_context_menu = QMenu()
        self.challenge_node_context_menu.addAction("Remove Challenge").triggered.connect(self.remove_challenge)
        self.challenge_node_context_menu.addAction("Add Flag").triggered.connect(self.flag_add)
        self.challenge_node_context_menu.addAction("Add Hint").triggered.connect(self.hint_add)
        self.challenge_node_context_menu.addAction("Add File").triggered.connect(self.file_add)

        self.node_context_menu = QMenu()
        self.node_context_menu.addAction("Remove Item").triggered.connect(self.remove_node_item)

        self.user_context_menu = QMenu()
        self.user_context_menu.addAction("Add User").triggered.connect(self.user_add)
        self.user_context_menu.addAction("Import Users").triggered.connect(self.user_import)
        self.user_context_menu.addAction("Sync Users").triggered.connect(self.user_sync)

        # Tree Viewer

        self.competition_tree = CompetitionTree()
        self.competition_tree.item_focus_change.connect(self.on_item_focus)
        self.competition_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.base_layout.addWidget(self.competition_tree)
        if os.path.exists(FILE_PATH):
            self.load_configurations()
        else:
            os.mkdir(FILE_PATH)

        # Property Widgets for Stacked Viewing

        self.default_property_widget = TitleWidget("Title")

        self.server_property_widget = ServerWidget(dialog=False)
        self.server_property_widget.value_updated.connect(self.update_configurations)

        self.challenges_property_widget = ChallengeWidget(dialog=False)
        self.challenges_property_widget.value_updated.connect(self.update_configurations)

        self.flags_property_widget = FlagWidget(dialog=False)
        self.flags_property_widget.value_updated.connect(self.update_configurations)

        self.hints_property_widget = HintWidget(dialog=False)
        self.hints_property_widget.value_updated.connect(self.update_configurations)

        self.files_property_widget = FileWidget(dialog=False)
        self.files_property_widget.value_updated.connect(self.update_configurations)

        self.users_property_widget = UserWidget(dialog=False)
        self.users_property_widget.value_updated.connect(self.update_configurations)

        # Stacked Widget

        self.stacked_properties = QStackedWidget()
        self.stacked_properties.addWidget(self.default_property_widget)
        self.stacked_properties.addWidget(self.server_property_widget)
        self.stacked_properties.addWidget(self.challenges_property_widget)
        self.stacked_properties.addWidget(self.flags_property_widget)
        self.stacked_properties.addWidget(self.hints_property_widget)
        self.stacked_properties.addWidget(self.files_property_widget)
        self.stacked_properties.addWidget(self.users_property_widget)
        self.stacked_properties.setCurrentWidget(self.default_property_widget)
        self.base_layout.addWidget(self.stacked_properties)

        # Dialog Widgets

        self.new_file_dialog = FileWidget()
        self.new_user_dialog = UserWidget()
        self.import_users_dialog = UserImportWidget()
        self.new_flag_dialog = FlagWidget()
        self.new_hint_dialog = HintWidget()
        self.new_challenge_dialog = ChallengeWidget()
        self.new_server_dialog = ServerWidget()

    ##
    #   NON-GUI RELATED FUNCTIONS
    ##

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

    def log(self, msg: str = '') -> None:
        logging.debug("{} Plugin: {}".format(self.__class__.__name__, msg))

    def save_configurations(self) -> None:
        # TODO: Add challenge checking to ensure no duplicate challenge names.
        if os.path.exists(FILE_PATH):
            self.log("save_configurations called!")
            with open("{}competitions.ctfi".format(FILE_PATH), "w") as file:
                data: dict = {}
                for key, item in iter(self.competition_config_dict.items()):
                    data.update({key: item.configuration})
                json.dump(data, file)

    def load_configurations(self) -> None:
        self.log("load_configuration path check returned: {}".format(
            os.path.exists("{}competitions.ctfi".format(FILE_PATH))))
        if os.path.exists("{}competitions.ctfi".format(FILE_PATH)):
            with open("{}competitions.ctfi".format(FILE_PATH), "r") as file:
                data: dict = json.loads(file.read())
                for key, item in iter(data.items()):
                    self.competition_config_dict.update({key: Configuration()})
                    self.competition_config_dict[key].configuration = item
            self.competition_tree.fill(self.competition_config_dict)

    def update_configurations(self, fields: dict) -> None:
        self.log("update_configuration called with args: {}".format(fields))
        if self.competition_tree.currentItem():
            root_node = self.competition_tree.find_root_node(self.competition_tree.currentItem())
            section = list(fields.keys())[0]
            updated_item = fields[section]
            self.competition_config_dict[root_node].update(section, **updated_item)
            self.competition_tree.fill(self.competition_config_dict)
            self.save_configurations()

    ##
    #   GUI RELATED FUNCTIONS
    ##

    ##
    #   Stacked Widgets Functions
    ##

    # noinspection PyUnresolvedReferences
    def on_item_focus(self):
        self.log("on_item_focus called.")
        # Get the selected item
        self.save_configurations()

        if self.competition_tree.currentItem():
            selected_item = self.competition_tree.currentItem()
            root_node: str = self.competition_tree.find_root_node(selected_item)
            widgets: dict = {'server': self.server_property_widget,
                             'challenges': self.challenges_property_widget,
                             'flags': self.flags_property_widget,
                             'hints': self.hints_property_widget,
                             'files': self.files_property_widget,
                             'users': self.users_property_widget}

            if selected_item.parent() is None \
                    or selected_item.text(0) in ["challenges", "users", "flags", "hints", "files", "requirements"]:
                # A configuration, challenges or users root node was selected; show plugin title widget
                self.stacked_properties.setCurrentWidget(self.default_property_widget)

            elif selected_item.parent().text(0) in widgets.keys():
                obj_id = selected_item.id
                obj_parent = selected_item.parent().text(0)
                self.log("calling read item on {} id: {}".format(obj_parent, obj_id))
                if obj_parent in ['challenges']:
                    fields = self.competition_config_dict[root_node].read(obj_parent, obj_id)
                    challenges = [{'name': item['name'], 'id': item['id']} for item in
                                  self.competition_config_dict[root_node].configuration['challenges']
                                  if int(item['id']) != int(fields['id'])]
                    fields.update({'challenges': challenges})
                    widgets[obj_parent].write(fields)
                else:
                    widgets[obj_parent].write(
                        self.competition_config_dict[root_node].read(obj_parent, obj_id))

                self.stacked_properties.setCurrentWidget(widgets[obj_parent])

            elif selected_item.text(0) in widgets.keys():
                obj = selected_item.text(0)
                widgets[obj].write(self.competition_config_dict[root_node].read(obj))
                self.stacked_properties.setCurrentWidget(widgets[obj])

    ##
    #   Context Menu Functions
    ##

    def show_context_menu(self, position):
        self.log("show_context_menu called.")
        context = self.competition_tree.itemAt(position) if position else self.competition_tree.topLevelItem(0)
        menus: dict = {'server': self.server_context_menu,
                       'challenges': self.challenge_root_context_menu,
                       'challenges_node': self.challenge_node_context_menu,
                       'flags_node': self.node_context_menu,
                       'hints_node': self.node_context_menu,
                       'files_node': self.node_context_menu,
                       'users': self.user_context_menu,
                       'users_node': self.node_context_menu}

        if not context:
            self.blank_context_menu.popup(self.competition_tree.mapToGlobal(position))

        elif context.parent() is None:
            self.competition_menu.selected_item = context
            self.competition_menu.popup(self.competition_tree.mapToGlobal(position))

        elif context.text(0) in menus.keys():
            obj = context.text(0)
            menus[obj].selected_item = context
            menus[obj].popup(self.competition_tree.mapToGlobal(position))

        elif '{}_node'.format(context.parent().text(0)) in menus.keys():
            obj = '{}_node'.format(context.parent().text(0))
            menus[obj].selected_item = context
            menus[obj].popup(self.competition_tree.mapToGlobal(position))

    # noinspection PyArgumentList,PyCallByClass
    def new_competition(self):
        # TODO: Entry Point for server init
        self.log("New Competition Action Called.")
        configuration_name, success = QInputDialog.getText(self, "Create New Competition", "Enter Competition Name:")

        if success:
            self.new_server_dialog = ServerWidget()
            self.new_server_dialog.name_line.setText(configuration_name)
            self.new_server_dialog.exec_()
            new_server = self.new_server_dialog.read() if success else None

        if success and new_server:
            self.competition_config_dict[configuration_name] = Configuration()
            if not self.competition_config_dict[configuration_name].server_check(**new_server):
                response = QMessageBox().question(self, "Server Already Initialized",
                                                  "Server may contain competition data.\nDo you want to wipe it?",
                                                  buttons=QMessageBox.Yes | QMessageBox.No,
                                                  defaultButton=QMessageBox.No)
                if response == QMessageBox.Yes:
                    self.competition_config_dict[configuration_name].server_wipe()
                if response == QMessageBox.No:
                    response = QMessageBox().question(self, "Server Already Initialized",
                                                      "Would you like to synchronize the local configuration with the server?",
                                                      buttons=QMessageBox.Yes | QMessageBox.No,
                                                      defaultButton=QMessageBox.No)
                    if response == QMessageBox.Yes:
                        self.competition_config_dict[configuration_name].challenge_api("sync")
                        self.competition_config_dict[configuration_name].user_api("sync")
            self.save_configurations()
            self.competition_tree.fill(self.competition_config_dict)
        else:
            alert = QMessageBox()
            alert.setWindowTitle("Alert!")
            alert.setText("New Competition Creation Cancelled")
            alert.exec_()

    # noinspection PyCallByClass,PyArgumentList
    def edit_competition(self):
        self.log("Edit Competition Action Called.")
        selected_item = self.competition_menu.selected_item
        configuration_name, success = QInputDialog.getText(self, "Edit Competition", "Enter New Competition Name:")
        if success:
            for item in self.competition_config_dict:
                if selected_item.text(0) in item.keys():
                    item[configuration_name] = item.pop(selected_item.text(0))
                    self.competition_tree = self.competition_tree.fill(self.competition_config_dict)
                    self.competition_menu.selected_item = None
                    break
        else:
            alert = QMessageBox()
            alert.setWindowTitle("Alert!")
            alert.setText("Competition Rename Cancelled")
            alert.exec_()

    def remove_competition(self):
        # TODO: Entry Point for server wipe
        self.log("Remove Competition Action Called.")
        selected_item = self.competition_menu.selected_item
        response = QMessageBox().question(self, "Delete Competition", "Warning: This can't be undone.\nAre you sure?",
                                          buttons=QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.No)
        if response == QMessageBox.Yes:
            if selected_item.text(0) in self.competition_config_dict.keys():
                _ = self.competition_config_dict.pop(selected_item.text(0))
                self.competition_tree.fill(self.competition_config_dict)

        else:
            alert = QMessageBox()
            alert.setWindowTitle("Alert!")
            alert.setText("Competition Deletion Cancelled")
            alert.exec_()

    def server_reset(self):
        self.log("Server Reset Called.")
        root_node = self.competition_tree.find_root_node(self.server_context_menu.selected_item)
        self.competition_config_dict[root_node].server_reset()

    def server_wipe(self):
        self.log("Sync Challenge Called.")
        root_node = self.competition_tree.find_root_node(self.server_context_menu.selected_item)
        self.competition_config_dict[root_node].server_wipe()

    def challenge_sync(self):
        self.log("Sync Challenge Called.")
        root_node = self.competition_tree.find_root_node(self.challenge_root_context_menu.selected_item)
        self.competition_config_dict[root_node].challenge_api("sync")
        self.competition_tree.fill(self.competition_config_dict)

    def add_challenge(self) -> None:
        self.log("Add Challenge Called.")
        root_node = self.competition_tree.find_root_node(self.challenge_root_context_menu.selected_item)
        challenges = [{'name': item['name'], 'id': item['id']} for item in
                      self.competition_config_dict[root_node].configuration['challenges']]
        self.new_challenge_dialog.fields.update({'challenges': challenges})
        self.new_challenge_dialog.exec_()

        challenge: dict = self.new_challenge_dialog.read()
        if challenge['name']:
            self.competition_config_dict[root_node].add("challenges", **challenge)
            self.competition_tree.fill(self.competition_config_dict)

    def remove_challenge(self) -> None:
        self.log("Remove Challenge Called.")
        selected_item = self.challenge_node_context_menu.selected_item
        root_node = self.competition_tree.find_root_node(selected_item)

        if selected_item.parent().text(0) == "challenges":
            self.competition_tree.setCurrentItem(selected_item.parent())
            self.competition_config_dict[root_node].remove("challenges", selected_item.id)
            self.stacked_properties.setCurrentWidget(self.default_property_widget)
            self.competition_tree.fill(self.competition_config_dict)

    def user_add(self):
        self.log("Add User Called.")
        root_node = self.competition_tree.find_root_node(self.user_context_menu.selected_item)
        self.new_user_dialog.exec_()

        new_user: dict = self.new_user_dialog.read()
        new_user.update({'password': ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits)
            for _ in range(8))}) if 'password' not in new_user.keys() else None
        if new_user['name']:
            self.competition_config_dict[root_node].add("users", **new_user)
            self.competition_tree.fill(self.competition_config_dict)

    def user_import(self):
        self.log("User Import Called.")
        root_node = self.competition_tree.find_root_node(self.user_context_menu.selected_item)
        self.import_users_dialog.exec_()
        new_user_file, generic_quantity = self.import_users_dialog.read()

        if os.path.exists(new_user_file):
            with open(new_user_file, "r") as file:
                for line in file.read().splitlines():
                    line = line.split(' ')
                    name = line[0]
                    email = line[1] if match(pattern_email, line[1]) else '{}@ctfd.io'.format(line[0])
                    password = ''.join(
                        random.SystemRandom().choice(
                            string.ascii_uppercase + string.ascii_lowercase + string.digits)
                        for _ in range(8))
                    self.competition_config_dict[root_node].add("users", **{'name': name,
                                                                            'email': email,
                                                                            'password': password,
                                                                            'verified': True,
                                                                            'hidden': False,
                                                                            'banned': False,
                                                                            'type': 'user'})

        if generic_quantity > 0:
            number = self.competition_config_dict[root_node].next_id('users')
            for user in range(0, generic_quantity):
                number += 1
                self.competition_config_dict[root_node].add(
                    "users", **{'name': 'user_{}'.format(number),
                                'password': ''.join(
                                    random.SystemRandom().choice(
                                        string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                    for _ in range(8)),
                                'email': '{}@ctfi.io'.format('user_{}'.format(number)),
                                'verified': True,
                                'hidden': False,
                                'banned': False,
                                'type': 'user'})

        self.competition_tree.fill(self.competition_config_dict)

    def user_sync(self):
        self.log("Sync User Called.")
        root_node = self.competition_tree.find_root_node(self.user_context_menu.selected_item)
        self.competition_config_dict[root_node].user_api("sync")
        self.competition_tree.fill(self.competition_config_dict)

    def flag_add(self):
        self.log("Add Flag Called.")
        challenge_id = self.challenge_node_context_menu.selected_item.id
        root_node = self.competition_tree.find_root_node(self.challenge_node_context_menu.selected_item)
        self.new_flag_dialog.exec_()

        new_flag: dict = self.new_flag_dialog.read()
        new_flag.update({'challenge_id': challenge_id, 'challenge': challenge_id})
        if new_flag['content']:
            self.competition_config_dict[root_node].add("flags", **new_flag)
            self.competition_tree.fill(self.competition_config_dict)

    def file_add(self):
        self.log("Add File Called.")
        challenge_id = self.challenge_node_context_menu.selected_item.id
        root_node = self.competition_tree.find_root_node(self.challenge_node_context_menu.selected_item)
        self.new_file_dialog.exec_()

        new_file: dict = self.new_file_dialog.read()
        new_file.update({'challenge': challenge_id, 'type': 'challenge', 'challenge_id': challenge_id})

        folder_path = "{}/{}".format(FILE_PATH, [item['name']
                                                for item in
                                                self.competition_config_dict[root_node].configuration['challenges']
                                                if item['id'] == challenge_id][0])
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        if os.path.exists(folder_path):
            os.system('/bin/cp "{}" "{}"'.format(new_file['path'], folder_path))
            new_path = '{}/{}'.format(folder_path, new_file['path'].split('/')[-1])
            new_file['path'] = new_path if os.path.exists(new_path) else new_file['path']

        self.competition_config_dict[root_node].add('files', **new_file)
        self.competition_tree.fill(self.competition_config_dict)

    def hint_add(self):
        self.log("Add Hint Called.")
        challenge_id = self.challenge_node_context_menu.selected_item.id
        root_node = self.competition_tree.find_root_node(self.challenge_node_context_menu.selected_item)
        self.new_hint_dialog.exec_()

        new_hint: dict = self.new_hint_dialog.read()
        new_hint.update({'challenge': challenge_id, 'challenge_id': challenge_id})
        print(new_hint)
        self.competition_config_dict[root_node].add("hints", **new_hint)
        self.competition_tree.fill(self.competition_config_dict)

    def remove_node_item(self):
        self.log("Remove Item Called.")
        obj = self.node_context_menu.selected_item
        obj_parent = obj.parent().text(0)
        root_node = self.competition_tree.find_root_node(obj)

        self.competition_config_dict[root_node].remove(obj_parent, obj.id)
        self.competition_tree.setCurrentItem(self.competition_tree.currentItem().parent())
        self.competition_tree.fill(self.competition_config_dict)
        self.stacked_properties.setCurrentWidget(self.default_property_widget)
