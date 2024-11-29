import os
import sys
import shutil
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from functions import start_organizing as so, find_undo as fu

class SceneTransferApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.selected_paths = []
        self.selected_docs = []
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("PSM Scene Transfer App")
        self.resize(800, 225)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                font-family: 'Tahoma';
            }
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 10px; /* Rounded edges for buttons */
                background-color: #FEB2C9;
            }
            QPushButton:hover {
                background-color: #FD6593; /* Hover effect */
            }
            QPushButton:pressed {
                background-color: #FEB2C9; /* Pressed effect */
            }
            QPushButton:checked {
                background-color: #be4c6e;
            }
            QLabel {
                background-color: #DDDDDD;
                padding: 10px;
            }
        """)

        # Create layout
        layout = QtWidgets.QGridLayout(self)

        body_div = QtWidgets.QWidget(self)
        body_layout = QtWidgets.QGridLayout(body_div)
        body_layout.setColumnStretch(0, 16)
        body_layout.setColumnStretch(1, 1)
        body_layout.setColumnStretch(2, 1)

        start_div = QtWidgets.QWidget(self)
        start_layout = QtWidgets.QGridLayout(start_div)
        start_layout.setColumnStretch(0, 16)
        start_layout.setColumnStretch(1, 1)

        # Label for selected paths
        self.selected_paths_label = QtWidgets.QLabel("No folder selected", body_div)
        body_layout.addWidget(self.selected_paths_label, 0, 0)

        # Folder selection button
        select_button = QtWidgets.QPushButton(QtGui.QIcon("icons/folder_white.png"), "", body_div)
        select_button.setIconSize(QtCore.QSize(24, 24))
        select_button.clicked.connect(self.select_folder())
        body_layout.addWidget(select_button, 0, 1)

        def multicam():
            print(multicam_button.isChecked())
            return multicam_button.isChecked()

        # Multicam button
        multicam_button = QtWidgets.QPushButton(QtGui.QIcon("icons/multicam_white.png"), "", body_div)
        multicam_button.setIconSize(QtCore.QSize(24, 24))
        multicam_button.setCheckable(True)
        multicam_button.toggled.connect(multicam)
        body_layout.addWidget(multicam_button, 0, 3)

        def multiImg():
            print(multiImg_button.isChecked())
            return multiImg_button.isChecked()

        # Multiple image folders button
        multiImg_button = QtWidgets.QPushButton(QtGui.QIcon("icons/imageFolders_white.png"), "", body_div)
        multiImg_button.setIconSize(QtCore.QSize(24, 24))
        multiImg_button.setCheckable(True)
        multiImg_button.toggled.connect(multiImg)
        body_layout.addWidget(multiImg_button, 0, 4)

        # Clear selection button
        clear_scene_button = QtWidgets.QPushButton(QtGui.QIcon("icons/backspace_white.png"), "", body_div)
        clear_scene_button.setIconSize(QtCore.QSize(24, 24))
        clear_scene_button.clicked.connect(lambda: self.clear_selection(True))
        body_layout.addWidget(clear_scene_button, 0, 2)

        # Label for selected documents
        self.selected_docs_label = QtWidgets.QLabel("No documents folder selected", body_div)
        body_layout.addWidget(self.selected_docs_label, 1, 0)

        # Select documents folder button
        docs_button = QtWidgets.QPushButton(QtGui.QIcon("icons/folder_white.png"), "", body_div)
        docs_button.setIconSize(QtCore.QSize(24, 24))
        docs_button.clicked.connect(self.docs_folder)
        body_layout.addWidget(docs_button, 1, 1)

        # Clear documents button
        clear_docs_button = QtWidgets.QPushButton(QtGui.QIcon("icons/backspace_white.png"), "", body_div)
        clear_docs_button.setIconSize(QtCore.QSize(24, 24))
        clear_docs_button.clicked.connect(lambda: self.clear_selection(False))
        body_layout.addWidget(clear_docs_button, 1, 2)

        layout.addWidget(body_div, 1, 0, 1, 3)

        # Start button
        start_button = QtWidgets.QPushButton("Start", start_div)
        start_button.clicked.connect(lambda: so.start_organizing(self.selected_paths, self.selected_docs))
        start_layout.addWidget(start_button, 0, 0)

        undo_button = QtWidgets.QPushButton(QtGui.QIcon("icons/undo_white.png"), "", start_div)
        undo_button.setIconSize(QtCore.QSize(24, 24))
        undo_button.clicked.connect(lambda: fu.undo_reorganization(self.selected_paths))
        start_layout.addWidget(undo_button, 0, 1)

        layout.addWidget(start_div, 3, 0, 1, 3)

        self.setLayout(layout)

        '''
        # Site code entry
        site_code_label = QtWidgets.QLabel("Site code:", self)
        #layout.addWidget(site_code_label, 3, 0)

        self.site_code_entry = QtWidgets.QLineEdit(self)
        #layout.addWidget(self.site_code_entry, 3, 1)
        '''

        '''
        def get_restricted_path(self):
            with open("settings/restricted_path.txt", "r") as file:
                return file.readline().strip()


        def is_valid_selection(self, folder_selected, base_path):
            base_depth = base_path.count(os.sep)
            selected_depth = folder_selected.count(os.sep)
            commonPath = os.path.commonpath([folder_selected, base_path])
            if commonPath != base_path or folder_selected == base_path:
                return False
            elif selected_depth >= base_depth + 3:
                return True
            else:
                return False
        '''

        def select_folder(self):
            # base_path = os.path.abspath(self.get_restricted_path())
            folder_selected = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder_selected:
                # folder_selected = os.path.abspath(folder_selected)
                #if not self.is_valid_selection(folder_selected, base_path):
                #    QtWidgets.QMessageBox.critical(self, "Invalid Selection", "Folder selection not allowed at this folder hierarchy. If you wish to select a folder at or above this hierarchy, please change Settings.")
                #else:
                self.selected_paths.append(folder_selected)
                self.selected_paths_label.setText(", ".join(self.selected_paths))

        def docs_folder(self):
            docFolder_selected = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Docs Folder")
            if docFolder_selected:
                self.selected_docs.append(docFolder_selected)
                self.selected_docs_label.setText(", ".join(self.selected_docs))

        def clear_selection(self, clear_scene):
            if clear_scene:
                self.selected_paths.clear()
                self.selected_paths_label.setText("No folder selected")
            else:
                self.selected_docs.clear()
                self.selected_docs_label.setText("No documents folder selected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SceneTransferApp()
    window.show()
    sys.exit(app.exec_())
