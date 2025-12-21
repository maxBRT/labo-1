from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel


class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Client Page"))
        self.setLayout(layout)
