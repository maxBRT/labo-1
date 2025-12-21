from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel


class EquipmentPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Equipment Page"))
        self.setLayout(layout)
