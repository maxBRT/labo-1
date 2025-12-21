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
from location.database.schema import ClientRead, ClientCreate
from location.database.database_manager import DatabaseManager
from location.ui.widgets import SortableItem
from location.ui.add_client_form import AddClientForm


class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Set up buttons
        self.button_container = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_layout)

        self.add_button = QPushButton("Nouveau client")
        self.edit_button = QPushButton("Modifier le client")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)

        # Set up the search bar
        self.search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un client")
        self.search_bar.textChanged.connect(self.search_client)
        self.search_layout.addWidget(self.search_bar)

        # Set up the table
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(["Index", "Nom", "Email", "Téléphone"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set up the layouts
        layout.addWidget(self.button_container)
        layout.addLayout(self.search_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Connect the buttons
        self.add_button.clicked.connect(self.show_add_client)
        self.edit_button.clicked.connect(self.show_edit_client)

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

            item = self.table.item(row, 1)

            if item and search_text in item.text().lower():
                match_found = True

            self.table.setRowHidden(row, not match_found)

    def show_add_client(self):
        """
        Show the add client form
        """
        add_form = AddClientForm()
        if add_form.exec():
            data = add_form.get_data()
            self.create_client(data)

    def create_client(self, data: dict):
        """
        Create a client in the database and refresh the table
        """
        try:
            # Create the client
            client = ClientCreate(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
            )

            self.db_manager.create_client(client)
            self.showEvent(QShowEvent())
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors de la création",
                f"Le client n'a pas pu être créé: {e}",
            )

    def update_client(self, client_id: int, data: dict):
        """
        Update a client in the database and refresh the table
        """
        try:
            # Update the client
            client = ClientCreate(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
            )

            self.db_manager.update_client(client_id, client)
            self.showEvent(QShowEvent())
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur lors de la modification",
                f"Le client n'a pas pu être modifié: {e}",
            )

    def show_edit_client(self):
        """
        Show the edit client form
        """
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un client à modifier.",
            )
            return

        # Get the client ID from the selected row
        client_id = self.table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)

        # Get the client data by ID
        client = self.db_manager.get_client_by_id(client_id)

        if client is None:
            QMessageBox.critical(
                self,
                "Erreur",
                "Client introuvable.",
            )
            return

        # Show the edit form with client data
        edit_form = AddClientForm(client=client)
        if edit_form.exec():
            data = edit_form.get_data()
            self.update_client(client_id, data)

    def showEvent(self, event: QShowEvent):
        """
        When the page is shown, get the clients from the database and add them to the table
        """

        # Disable sorting while populating to avoid race conditions
        self.table.setSortingEnabled(False)

        # Clear the table
        self.table.clearContents()
        self.table.setRowCount(0)

        # Get the clients
        clients = self.db_manager.get_clients()

        # Add the clients to the table
        for client in clients:
            self.add_item(client)

        # Re-enable sorting after all items are added
        self.table.setSortingEnabled(True)

        super().showEvent(event)

    def add_item(self, data: ClientRead):
        """
        Add a client to the table
        """
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        # Column 0
        id_item = SortableItem(str(data.id))
        id_item.setData(Qt.ItemDataRole.UserRole, data.id)
        self.table.setItem(row_index, 0, id_item)

        # Column 1
        self.table.setItem(row_index, 1, QTableWidgetItem(data.name))

        # Column 2
        self.table.setItem(row_index, 2, QTableWidgetItem(data.email))

        # Column 3
        self.table.setItem(row_index, 3, QTableWidgetItem(data.phone))
