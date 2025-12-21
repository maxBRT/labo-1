import re
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QDialogButtonBox,
    QLineEdit,
    QMessageBox,
)
from location.database.schema import ClientRead


class AddClientForm(QDialog):
    def __init__(self, parent=None, client: ClientRead = None):
        super().__init__(parent)
        self.client = client
        self.setWindowTitle("Modifier un client" if client else "Ajouter un client")

        # Layout
        layout = QVBoxLayout()

        # Add Input Fields
        self.name_label = QLabel("Nom:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du client")

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")

        self.phone_label = QLabel("Téléphone:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("5141112222")

        # Add the widgets to the layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        # If editing, populate the fields with existing data
        if self.client:
            self.name_input.setText(self.client.name)
            self.email_input.setText(self.client.email)
            self.phone_input.setText(self.client.phone)

        # Add Standard Buttons (Ok / Cancel)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect internal signals to custom validation method
        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email) is not None

    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format (10 digits: 5141112222)"""
        phone_pattern = r"^\d{10}$"
        return re.match(phone_pattern, phone) is not None

    def validate_and_accept(self):
        """Validate form data before accepting"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        # Validate name
        if not name:
            QMessageBox.warning(
                self, "Validation Error", "Le nom du client est requis."
            )
            self.name_input.setFocus()
            return

        # Validate email
        if not email:
            QMessageBox.warning(
                self, "Validation Error", "L'adresse email est requise."
            )
            self.email_input.setFocus()
            return

        if not self.validate_email(email):
            QMessageBox.warning(
                self,
                "Validation Error",
                "L'adresse email n'est pas valide.\nFormat attendu: email@example.com",
            )
            self.email_input.setFocus()
            return

        # Validate phone
        if not phone:
            QMessageBox.warning(
                self, "Validation Error", "Le numéro de téléphone est requis."
            )
            self.phone_input.setFocus()
            return

        if not self.validate_phone(phone):
            QMessageBox.warning(
                self,
                "Validation Error",
                "Le numéro de téléphone n'est pas valide.\nFormat attendu: 10 chiffres (ex: 5141112222)",
            )
            self.phone_input.setFocus()
            return

        # All validation passed
        self.accept()

    def get_data(self):
        """Helper to return the data entered by the user"""
        return {
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
        }
