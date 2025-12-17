from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QPushButton,
    QTableWidgetItem,
)
from PySide6.QtGui import QShowEvent
from schema import LocationRead
from database_manager import DatabaseManager


class LocationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Set up add button
        self.add_button = QPushButton("Nouvelle location")
        layout.addWidget(self.add_button)

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

        # Set up the layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Create the database manager
        self.DbManager = DatabaseManager()

    def showEvent(self, event: QShowEvent):
        """
        When the page is shown, get the locations from the database and add them to the table
        """

        # Clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

        # Get the locations
        locations = self.DbManager.get_locations()

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
