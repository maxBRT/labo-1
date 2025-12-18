from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QPushButton,
    QTableWidgetItem,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtGui import QShowEvent
from schema import LocationRead, LocationCreate
from database_manager import DatabaseManager
from .add_location_form import AddLocationForm


class LocationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Set up buttons
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_layout)

        self.add_button = QPushButton("Nouvelle location")
        self.delete_button = QPushButton("Supprimer")
        self.return_button = QPushButton("Marquer comme retourné")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.return_button)

        # Set up the table
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnCount(7)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(
            ["Index", "Client", "Équipment", "Début", "Fin", "Retourné", "Coût"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set up the layouts
        layout.addWidget(self.button_container)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Connect the buttons
        self.add_button.clicked.connect(self.show_add_location)
        self.delete_button.clicked.connect(self.delete_location)
        self.return_button.clicked.connect(self.return_location)

        # Create the database manager
        self.db_manager = DatabaseManager()

    def show_add_location(self):
        add_form = AddLocationForm()
        if add_form.exec():
            data = add_form.get_data()
            self.create_location(data)

    def create_location(self, data: dict):
        try:
            # Create the location
            location = LocationCreate(
                start_date=data["start_date"],
                end_date=data["end_date"],
                is_returned=False,
                id_client=data["client"].id,
                id_equipment=data["equipment"].id,
            )
            self.db_manager.create_location(location)
            self.showEvent(QShowEvent())
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors de la création",
                f"La location n'a pas pu être créée: {e}",
            )

    def delete_location(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row == -1:
                return

            # Get the location to delete
            location_id = self.table.item(selected_row, 0).text()

            # Delete the location
            self.db_manager.delete_location(location_id)

            # Refresh the table
            self.showEvent(QShowEvent())

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors de la suppresion",
                f"La location n'a pas pu être supprimée: {e}",
            )

    def return_location(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row == -1:
                return

            # Get the location to return
            location_id = self.table.item(selected_row, 0).text()

            # Return the location
            self.db_manager.return_location(location_id)

            # Refresh the table
            self.showEvent(QShowEvent())

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors du retour",
                f"La location n'a pas pu être retournée: {e}",
            )

    def showEvent(self, event: QShowEvent):
        """
        When the page is shown, get the locations from the database and add them to the table
        """

        # Clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

        # Get the locations
        locations = self.db_manager.get_locations()

        # Add the locations to the table
        for loc in locations:
            self.add_item(loc)

        super().showEvent(event)

    def add_item(self, data: LocationRead):
        # Add a new row to the table
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        # Calculate the total cost of the location
        duration = data.end_date - data.start_date
        total_cost = data.equipment.cost_per_day * duration.days

        # Model the data to display in the table
        columns = [
            str(data.id),
            data.client.name,
            data.equipment.name,
            data.start_date.strftime("%Y-%m-%d"),
            data.end_date.strftime("%Y-%m-%d"),
            "Oui" if data.is_returned else "Non",
            f"{total_cost:.2f} $",
        ]

        # Add the data to the table
        for col_index, value in enumerate(columns):
            item = QTableWidgetItem(value)
            self.table.setItem(row_index, col_index, item)
