from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel


class LocationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Location Page"))
        self.setLayout(layout)
