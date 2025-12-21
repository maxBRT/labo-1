from datetime import datetime
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QComboBox,
    QDateEdit,
)
from PySide6.QtCore import QDate
from location.database.database_manager import DatabaseManager


class AddLocationForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une location")

        # Create the database manager
        self.db_manager = DatabaseManager()

        # Get clients and equipments from the database
        self.clients = self.db_manager.get_clients()
        self.equipments = self.db_manager.get_available_equipments()

        # Layout
        layout = QVBoxLayout()

        # Add Input Fields
        self.client_label = QLabel("Client:")
        self.client_input = QComboBox()
        for client in self.clients:
            # Create a display text for the client
            display_text = f"{client.name} ({client.email})"

            # Add the client data to the combo box
            self.client_input.addItem(display_text, client)

        self.equipment_label = QLabel("Equipement:")
        self.equipment_input = QComboBox()
        for equipment in self.equipments:
            # Create a display text for the equipment
            display_text = f"{equipment.name} ({equipment.cost_per_day} $/jour)"

            # Add the equipment data to the combo box
            self.equipment_input.addItem(display_text, equipment)

        # Set up the date inputs
        self.start_date_label = QLabel("Date de début:")
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("dd/MM/yyyy")

        self.end_date_label = QLabel("Date de fin:")
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("dd/MM/yyyy")

        # Add the widgets to the layout
        layout.addWidget(self.client_label)
        layout.addWidget(self.client_input)
        layout.addWidget(self.equipment_label)
        layout.addWidget(self.equipment_input)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)

        # Add total cost display
        self.total_cost_label = QLabel("Coût total estimé: 0.00 $")
        self.total_cost_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.total_cost_label)

        # Connect signals to update cost calculation
        self.equipment_input.currentIndexChanged.connect(self.update_total_cost)
        self.start_date_input.dateChanged.connect(self.update_total_cost)
        self.end_date_input.dateChanged.connect(self.update_total_cost)

        # Initial cost calculation
        self.update_total_cost()

        # Add Standard Buttons (Ok / Cancel)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect internal signals to QDialog's accept/reject slots
        self.buttons.accepted.connect(self.accept)  # Closes dialog with result=1
        self.buttons.rejected.connect(self.reject)  # Closes dialog with result=0

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_data(self):
        """Helper to return the data entered by the user"""
        return {
            "client": self.client_input.currentData(),
            "equipment": self.equipment_input.currentData(),
            "start_date": self.start_date_input.date().toPython(),
            "end_date": self.end_date_input.date().toPython(),
        }

    def update_total_cost(self):
        """Calculate and display the estimated total cost"""
        # Get the selected equipment
        equipment = self.equipment_input.currentData()

        if equipment is None:
            self.total_cost_label.setText("Coût total estimé: 0.00 $")
            return

        # Get the dates
        start_date = self.start_date_input.date().toPython()
        end_date = self.end_date_input.date().toPython()

        # Calculate number of days
        duration = (end_date - start_date).days

        # Make sure duration is at least 1 day
        if duration < 1:
            duration = 1

        # Calculate total cost
        total_cost = equipment.cost_per_day * duration

        # Update the label
        self.total_cost_label.setText(
            f"Coût total estimé: {total_cost:.2f} $ ({duration} jour{'s' if duration > 1 else ''})"
        )
