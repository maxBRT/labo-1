from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QLineEdit,
    QCheckBox,
    QDoubleSpinBox,
    QMessageBox,
)
from location.database.schema import EquipmentRead


class AddEquipmentForm(QDialog):
    def __init__(self, parent=None, equipment: EquipmentRead = None):
        super().__init__(parent)
        self.equipment = equipment
        self.setWindowTitle(
            "Modifier un équipement" if equipment else "Ajouter un équipement"
        )

        # Layout
        layout = QVBoxLayout()

        # Add Input Fields
        self.name_label = QLabel("Nom:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom de l'équipement")

        self.cost_label = QLabel("Coût par jour ($):")
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMinimum(0.00)
        self.cost_input.setMaximum(999999.99)
        self.cost_input.setDecimals(2)
        self.cost_input.setValue(0.00)

        self.available_label = QLabel("Disponible:")
        self.available_input = QCheckBox()
        self.available_input.setChecked(True)

        # Add the widgets to the layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.cost_label)
        layout.addWidget(self.cost_input)
        layout.addWidget(self.available_label)
        layout.addWidget(self.available_input)

        # If editing, populate the fields with existing data
        if self.equipment:
            self.name_input.setText(self.equipment.name)
            self.cost_input.setValue(float(self.equipment.cost_per_day))
            self.available_input.setChecked(self.equipment.is_available)

        # Add Standard Buttons (Ok / Cancel)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect internal signals to custom validation method
        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def validate_and_accept(self):
        """Validate form data before accepting"""
        name = self.name_input.text().strip()
        cost = self.cost_input.value()

        # Validate name
        if not name:
            QMessageBox.warning(
                self, "Validation Error", "Le nom de l'équipement est requis."
            )
            self.name_input.setFocus()
            return

        # Validate cost
        if cost <= 0:
            QMessageBox.warning(
                self, "Validation Error", "Le coût par jour doit être supérieur à 0."
            )
            self.cost_input.setFocus()
            return

        # All validation passed
        self.accept()

    def get_data(self):
        """Helper to return the data entered by the user"""
        return {
            "name": self.name_input.text().strip(),
            "cost_per_day": self.cost_input.value(),
            "is_available": self.available_input.isChecked(),
        }
