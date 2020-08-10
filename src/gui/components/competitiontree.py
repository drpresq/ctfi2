from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CompetitionTree(QTreeWidget):
    value_updated = pyqtSignal(dict)
    item_focus_change = pyqtSignal()
    context_menu_requested = pyqtSignal()

    def __init__(self) -> None:
        super(CompetitionTree, self).__init__()

        self.font = QFont(QFont().defaultFamily())
        self.font.setUnderline(True)

        self.itemSelectionChanged.connect(self.item_focus_change.emit)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setObjectName("TreeViewer")
        self.setEnabled(True)
        self.setMaximumSize(200, 521)
        self.setSortingEnabled(False)
        self.header().resizeSection(0, 150)
        self.headerItem().setText(0, "CTFd Competitions")

    def fill(self, config_dict: dict) -> None:
        """ This is complicated; I couldn't think of a variable naming scheme that was more clear. """
        self.clear()
        # Set Top level node of each configuration object
        for root_key, configuration_obj in iter(config_dict.items()):
            conf = configuration_obj.configuration
            conf_name = root_key
            conf_root = QTreeWidgetItem()
            conf_root.setText(0, conf_name)
            self.addTopLevelItem(conf_root)
            # Set section nodes fot the current configuration object
            for section, section_data in conf.items():
                if section in ["server", "email", "challenges", "users"]:
                    section_node = QTreeWidgetItem()
                    section_node.setText(0, section)
                    section_node.setFont(0, self.font)
                    conf_root.addChild(section_node)
                    # Set object nodes for the current section node
                    if type(section_data) is list:
                        for section_item in section_data:
                            section_item_node = QTreeWidgetItem()
                            section_item_node.id = section_item['id']
                            section_item_node.setText(0, section_item['name'])
                            section_node.addChild(section_item_node)
                            # Set all of the attribute nodes of the current challenge object node
                            if section == "challenges":
                                for sub_section in ["flags", "hints", "files", "requirements"]:
                                    if len(conf[sub_section]) > 0:
                                        if section_item['id'] in \
                                                [item['challenge_id'] for item in conf[sub_section]
                                                 if 'challenge_id' in item.keys()] \
                                                or section_item['id'] in [item['challenge'] for item in conf[sub_section]
                                                                          if 'challenge' in item.keys()]:
                                            sub_section_node = QTreeWidgetItem()
                                            sub_section_node.setText(0, sub_section)
                                            sub_section_node.setFont(0, self.font)
                                            section_item_node.addChild(sub_section_node)
                                            for sub_section_item in conf[sub_section]:
                                                for key in sub_section_item.keys():
                                                    # objects refer to challenges by 'challenge' and 'challenge_id'
                                                    if 'challenge' in key and sub_section_item[key] == section_item['id']:
                                                        sub_section_item_node: QTreeWidgetItem = QTreeWidgetItem()
                                                        if 'name' in sub_section_item.keys():
                                                            sub_section_item_node.setText(0, sub_section_item['name'])
                                                        elif 'content' in sub_section_item.keys():
                                                            sub_section_item_node.setText(0, sub_section_item['content'])
                                                        elif 'path' in sub_section_item.keys():
                                                            sub_section_item_node.setText(
                                                                0, sub_section_item['path'].split('/')[-1])
                                                        sub_section_item_node.id = str(sub_section_item['id'])
                                                        sub_section_node.addChild(sub_section_item_node)
                                                        break
        self.expandToDepth(1)

    def rename_node(self, root: str, section: str, node_id: int):
        for index in range(self.topLevelItemCount()):
            root = self.topLevelItem(index) if self.topLevelItem(index).text(0) == root else root

    @staticmethod
    def insert_node(parent_node: QTreeWidgetItem, new_node_name: str, new_node_index: int) -> None:
        new_node = QTreeWidgetItem()
        new_node.setText(0, new_node_name)
        new_node.index = new_node_index
        parent_node.addChild(new_node)

    @staticmethod
    def find_root_node(target_node: QTreeWidgetItem) -> str:
        root_node: QTreeWidgetItem
        root_node = target_node
        while root_node.parent():
            root_node = root_node.parent()
        return root_node.text(0)
