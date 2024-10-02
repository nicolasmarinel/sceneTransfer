import os
import sys
import shutil
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from functions import start_organizing as so

class SceneTransferApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.selected_paths = []
        self.selected_docs = []
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Scene Transfer App")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 10px; /* Rounded edges for buttons */
                background-color: white;
            }
            QPushButton:hover {
                background-color: #FD6593; /* Hover effect */
            }
            QPushButton:pressed {
                background-color: #FEB2C9; /* Pressed effect */
            }
            QLabel {
                background-color: white;
            }
        """)

        # Create layout
        layout = QtWidgets.QVBoxLayout(self)

        # Add widgets
        label = QtWidgets.QLabel("Organize Scene Files", self)
        layout.addWidget(label)

        # Folder selection button
        select_button = QtWidgets.QPushButton(QtGui.QIcon("icons/folder_white.png"), "", self)
        select_button.clicked.connect(self.select_folder)
        layout.addWidget(select_button)

        # Label for selected paths
        self.selected_paths_label = QtWidgets.QLabel("No folder selected", self)
        layout.addWidget(self.selected_paths_label)

        # Clear selection button
        clear_scene_button = QtWidgets.QPushButton("Clear Selection", self)
        clear_scene_button.clicked.connect(lambda: self.clear_selection(True))
        layout.addWidget(clear_scene_button)

        # Document folder selection
        docs_label = QtWidgets.QLabel("Select Documents Folder", self)
        layout.addWidget(docs_label)

        docs_button = QtWidgets.QPushButton("Select Docs Folder", self)
        docs_button.clicked.connect(self.docs_folder)
        layout.addWidget(docs_button)

        # Label for selected documents
        self.selected_docs_label = QtWidgets.QLabel("No documents folder selected", self)
        layout.addWidget(self.selected_docs_label)

        # Clear documents button
        clear_docs_button = QtWidgets.QPushButton("Clear Selection", self)
        clear_docs_button.clicked.connect(lambda: self.clear_selection(False))
        layout.addWidget(clear_docs_button)

        # Site code entry
        site_code_label = QtWidgets.QLabel("Enter site code", self)
        layout.addWidget(site_code_label)

        self.site_code_entry = QtWidgets.QLineEdit(self)
        layout.addWidget(self.site_code_entry)

        # Start button
        start_button = QtWidgets.QPushButton("Start", self)
        start_button.clicked.connect(lambda: so.start_organizing(self.selected_paths, self.selected_docs, self.site_code_entry))
        layout.addWidget(start_button)

        self.setLayout(layout)

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

    def select_folder(self):
        base_path = os.path.abspath(self.get_restricted_path())
        folder_selected = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_selected:
            folder_selected = os.path.abspath(folder_selected)
            if not self.is_valid_selection(folder_selected, base_path):
                QtWidgets.QMessageBox.critical(self, "Invalid Selection", "Folder selection not allowed at this folder hierarchy. If you wish to select a folder at or above this hierarchy, please change Settings.")
            else:
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
