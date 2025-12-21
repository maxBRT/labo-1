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
    QLineEdit,
)
from PySide6.QtGui import QShowEvent
from PySide6.QtCore import Qt
from location.database.schema import LocationRead, LocationCreate
from location.database.database_manager import DatabaseManager
from location.ui.add_location_form import AddLocationForm
from location.ui.widgets import SortableItem


class LocationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Set up buttons
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_layout)

        self.add_button = QPushButton("Nouvelle location")
        self.return_button = QPushButton("Marquer comme retourné")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.return_button)

        # Set up the search bar
        self.search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un client ou un équipement")
        self.search_bar.textChanged.connect(self.search_client)
        self.search_layout.addWidget(self.search_bar)

        # Set up the table
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnCount(6)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(
            ["Index", "Client", "Équipment", "Début", "Fin", "Retourné"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set up the layouts
        layout.addWidget(self.button_container)
        layout.addLayout(self.search_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Connect the buttons
        self.add_button.clicked.connect(self.show_add_location)
        self.return_button.clicked.connect(self.return_location)

        # Create the database manager
        self.db_manager = DatabaseManager()

    def search_client(self, text: str):
        """
        Search for a client in the table
        """
        search_text = text.lower()

        # Hide all rows that don't match the search text
        for row in range(self.table.rowCount()):
            match_found = False

            client = self.table.item(row, 1)
            equipment = self.table.item(row, 2)

            if client and search_text in client.text().lower():
                match_found = True
            if equipment and search_text in equipment.text().lower():
                match_found = True

            self.table.setRowHidden(row, not match_found)

    def show_add_location(self):
        """
        Show the add location form
        """
        add_form = AddLocationForm()
        if add_form.exec():
            data = add_form.get_data()
            self.create_location(data)

    def create_location(self, data: dict):
        """
        Create a location in the database and refresh the table
        """
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

    def return_location(self):
        """
        Return the selected location
        """
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

        # Disable sorting while populating to avoid race conditions
        self.table.setSortingEnabled(False)

        # Clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

        # Get the locations
        locations = self.db_manager.get_locations()

        # Add the locations to the table
        for loc in locations:
            self.add_item(loc)

        # Re-enable sorting after all items are added
        self.table.setSortingEnabled(True)

        super().showEvent(event)

    def add_item(self, data: LocationRead):
        """
        Add a location to the table
        """
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        # Column 0
        id_item = SortableItem(str(data.id))
        id_item.setData(Qt.ItemDataRole.UserRole, data.id)
        self.table.setItem(row_index, 0, id_item)

        # Column 1
        self.table.setItem(row_index, 1, QTableWidgetItem(data.client.name))

        # Column 2
        self.table.setItem(row_index, 2, QTableWidgetItem(data.equipment.name))

        # Column 3 & 4
        self.table.setItem(
            row_index, 3, QTableWidgetItem(data.start_date.strftime("%Y-%m-%d"))
        )
        self.table.setItem(
            row_index, 4, QTableWidgetItem(data.end_date.strftime("%Y-%m-%d"))
        )

        # Column 5
        self.table.setItem(
            row_index, 5, QTableWidgetItem("Oui" if data.is_returned else "Non")
        )
