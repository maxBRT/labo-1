from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from location.database.database import Base, engine
from location.ui.client_page import ClientPage
from location.ui.equipment_page import EquipmentPage
from location.ui.location_page import LocationPage
from location.database.models import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logiciel de location")

        # Set up the main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Set up the sidebar
        self.sidebar_layout = QVBoxLayout()
        self.btn_clients = QPushButton("Clients")
        self.btn_equipments = QPushButton("Equipments")
        self.btn_locations = QPushButton("Locations")

        # Add the buttons to the sidebar
        self.sidebar_layout.addWidget(self.btn_clients)
        self.sidebar_layout.addWidget(self.btn_equipments)
        self.sidebar_layout.addWidget(self.btn_locations)
        self.sidebar_layout.addStretch()

        # Add the sidebar to the main layout
        self.sidebar_container = QWidget()
        self.sidebar_container.setLayout(self.sidebar_layout)
        self.main_layout.addWidget(self.sidebar_container)

        # Set up the content
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Add the pages to the stack
        self.client_page = ClientPage()
        self.equipment_page = EquipmentPage()
        self.location_page = LocationPage()
        self.stack.addWidget(self.client_page)  # Index 0
        self.stack.addWidget(self.equipment_page)  # Index 1
        self.stack.addWidget(self.location_page)  # Index 2

        # Set up the navigation
        self.btn_clients.clicked.connect(lambda: self.switch_page(0))
        self.btn_equipments.clicked.connect(lambda: self.switch_page(1))
        self.btn_locations.clicked.connect(lambda: self.switch_page(2))

        # Set the initial page
        self.switch_page(2)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)


def main():
    # Initialize the database
    Base.metadata.create_all(bind=engine)

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
