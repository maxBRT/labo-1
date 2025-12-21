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
from decimal import Decimal
from location.database.schema import EquipmentRead, EquipmentCreate
from location.database.database_manager import DatabaseManager
from location.ui.widgets import SortableItem
from location.ui.add_equipment_form import AddEquipmentForm


class EquipmentPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Set up buttons
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_layout)

        self.add_button = QPushButton("Nouvel équipement")
        self.edit_button = QPushButton("Modifier l'équipement")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)

        # Set up the search bar
        self.search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un équipement")
        self.search_bar.textChanged.connect(self.search_equipment)
        self.search_layout.addWidget(self.search_bar)

        # Set up the table
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(
            ["Index", "Nom", "Disponible", "Coût par jour"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set up the layouts
        layout.addWidget(self.button_container)
        layout.addLayout(self.search_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Connect the buttons
        self.add_button.clicked.connect(self.show_add_equipment)
        self.edit_button.clicked.connect(self.show_edit_equipment)

        # Create the database manager
        self.db_manager = DatabaseManager()

    def search_equipment(self, text: str):
        """
        Search for an equipment in the table
        """
        search_text = text.lower()

        # Hide all rows that don't match the search text
        for row in range(self.table.rowCount()):
            match_found = False

            item = self.table.item(row, 1)

            if item and search_text in item.text().lower():
                match_found = True

            self.table.setRowHidden(row, not match_found)

    def show_add_equipment(self):
        """
        Show the add equipment form
        """
        add_form = AddEquipmentForm()
        if add_form.exec():
            data = add_form.get_data()
            self.create_equipment(data)

    def create_equipment(self, data: dict):
        """
        Create an equipment in the database and refresh the table
        """
        try:
            equipment = EquipmentCreate(
                name=data["name"],
                cost_per_day=Decimal(str(data["cost_per_day"])),
                is_available=data["is_available"],
            )

            self.db_manager.create_equipment(equipment)
            self.showEvent(QShowEvent())
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors de la création",
                f"L'équipement n'a pas pu être créé: {e}",
            )

    def update_equipment(self, equipment_id: int, data: dict):
        """
        Update an equipment in the database and refresh the table
        """
        try:
            equipment = EquipmentCreate(
                name=data["name"],
                cost_per_day=Decimal(str(data["cost_per_day"])),
                is_available=data["is_available"],
            )

            self.db_manager.update_equipment(equipment_id, equipment)
            self.showEvent(QShowEvent())
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors de la modification",
                f"L'équipement n'a pas pu être modifié: {e}",
            )

    def show_edit_equipment(self):
        """
        Show the edit equipment form
        """
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un équipement à modifier.",
            )
            return

        # Get the equipment ID from the selected row
        equipment_id = self.table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)

        # Get the equipment data by ID
        equipment = self.db_manager.get_equipment_by_id(equipment_id)

        if equipment is None:
            QMessageBox.critical(
                self,
                "Erreur",
                "Équipement introuvable.",
            )
            return

        # Show the edit form with equipment data
        edit_form = AddEquipmentForm(equipment=equipment)
        if edit_form.exec():
            data = edit_form.get_data()
            self.update_equipment(equipment_id, data)

    def showEvent(self, event: QShowEvent):
        """
        When the page is shown, get the equipments from the database and add them to the table
        """

        # Disable sorting while populating to avoid race conditions
        self.table.setSortingEnabled(False)

        # Clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

        # Get the equipments
        equipments = self.db_manager.get_equipments()

        # Add the equipments to the table
        for equipment in equipments:
            self.add_item(equipment)

        # Re-enable sorting after all items are added
        self.table.setSortingEnabled(True)

        super().showEvent(event)

    def add_item(self, data: EquipmentRead):
        """
        Add an equipment to the table
        """
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        try:
            # Column 0
            id_item = SortableItem(str(data.id))
            id_item.setData(Qt.ItemDataRole.UserRole, data.id)
            self.table.setItem(row_index, 0, id_item)

            # Column 1
            self.table.setItem(row_index, 1, QTableWidgetItem(data.name))

            # Column 2
            if data.is_available is not None:
                self.table.setItem(
                    row_index,
                    2,
                    QTableWidgetItem("Oui" if data.is_available else "Non"),
                )

            # Column 3
            if data.cost_per_day is not None:
                cost_item = SortableItem(f"{data.cost_per_day:.2f} $")
                cost_item.setData(Qt.ItemDataRole.UserRole, data.cost_per_day)
                self.table.setItem(row_index, 3, cost_item)
        except Exception as e:
            print(f"Error adding equipment row: {e}, data: {data}")
