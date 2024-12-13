import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QComboBox, QTextEdit, QFileDialog, QWidget
)
import sqlite3

DB_FILE = "gestures.db"

class GestureConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Configuration")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        # Dropdown for gestures
        self.gesture_dropdown = QComboBox()
        self.gesture_dropdown.addItems([
            "one_finger_up", "one_finger_down", "fist_closed", "fist_opened", 
            "hand_up", "hand_down"
        ])
        self.layout.addWidget(QLabel("Select Gesture:"))
        self.layout.addWidget(self.gesture_dropdown)

        # Dropdown for action type
        self.action_type_dropdown = QComboBox()
        self.action_type_dropdown.addItems(["Open App", "Accessibility Option"])
        self.action_type_dropdown.currentIndexChanged.connect(self.update_action_options)
        self.layout.addWidget(QLabel("Select Action Type:"))
        self.layout.addWidget(self.action_type_dropdown)

        # Action options (either app path or predefined accessibility option)
        self.action_dropdown = QComboBox()
        self.layout.addWidget(QLabel("Select/Enter Action:"))
        self.layout.addWidget(self.action_dropdown)

        # File picker for "Open App" actions
        self.pick_app_button = QPushButton("Pick an App")
        self.pick_app_button.clicked.connect(self.pick_app)
        self.layout.addWidget(self.pick_app_button)

        # Predefined app picker
        self.predefined_app_dropdown = QComboBox()
        self.predefined_app_dropdown.addItems(["Select a predefined app", "Browser", "Terminal", "File Manager", "Editor"])
        self.predefined_app_dropdown.currentIndexChanged.connect(self.add_predefined_app_to_dropdown)
        self.layout.addWidget(QLabel("Predefined Applications:"))
        self.layout.addWidget(self.predefined_app_dropdown)

        # Add Gesture Button
        self.add_button = QPushButton("Add/Update Gesture")
        self.add_button.clicked.connect(self.add_gesture)
        self.layout.addWidget(self.add_button)

        # Reset Configuration Button
        self.reset_button = QPushButton("Reset Configuration")
        self.reset_button.clicked.connect(self.reset_configuration)
        self.layout.addWidget(self.reset_button)

        # Set the layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Initialize DB
        self.init_db()

        # Update action options based on initial selection
        self.update_action_options()

    def init_db(self):
        """Initialize the SQLite database."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gestures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gesture_name TEXT UNIQUE,
                    action_type TEXT,
                    action TEXT
                )
            """)

    def update_action_options(self):
        """Update the action options based on the selected action type."""
        self.action_dropdown.clear()
        action_type = self.action_type_dropdown.currentText()
        if action_type == "Open App":
            self.pick_app_button.setEnabled(True)
            self.action_dropdown.addItem("Select an app or pick one")
        elif action_type == "Accessibility Option":
            self.pick_app_button.setEnabled(False)
            self.action_dropdown.addItems([
                "Scroll Up", "Scroll Down", "Zoom In", "Zoom Out", "Volume Up", "Volume Down"
            ])

    def pick_app(self):
        """Open a file dialog to pick an application."""
        app_path, _ = QFileDialog.getOpenFileName(self, "Pick an App", "/usr/bin/")
        if app_path:
            self.action_dropdown.addItem(app_path)
            self.action_dropdown.setCurrentText(app_path)

    def add_predefined_app_to_dropdown(self):
        """Add a predefined application to the action dropdown."""
        app_name = self.predefined_app_dropdown.currentText()
        if app_name == "Browser":
            app_path = "/usr/bin/firefox"  # Adjust for your preferred browser
        elif app_name == "Terminal":
            app_path = "/usr/bin/gnome-terminal"  # Adjust for your terminal emulator
        elif app_name == "File Manager":
            app_path = "/usr/bin/nautilus"  # Adjust for your file manager
        elif app_name == "Editor":
            app_path = "/usr/bin/code"  # Adjust for your preferred editor
        else:
            return

        self.action_dropdown.addItem(app_path)
        self.action_dropdown.setCurrentText(app_path)

    def add_gesture(self):
        """Save gesture configuration to the database."""
        gesture_name = self.gesture_dropdown.currentText()
        action_type = self.action_type_dropdown.currentText()
        action = self.action_dropdown.currentText().strip()

        if gesture_name and action:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO gestures (gesture_name, action_type, action)
                    VALUES (?, ?, ?)
                    ON CONFLICT(gesture_name) DO UPDATE SET action_type = excluded.action_type, action = excluded.action
                """, (gesture_name, action_type, action))
                conn.commit()
            self.action_dropdown.setCurrentText("")
            print(f"Gesture '{gesture_name}' set to action '{action}'")

    def reset_configuration(self):
        """Reset the database by clearing all gesture-action mappings."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM gestures")
            conn.commit()
        print("All gesture configurations have been reset.")

if __name__ == "__main__":
    app = QApplication([])
    window = GestureConfigApp()
    window.show()
    app.exec_()

