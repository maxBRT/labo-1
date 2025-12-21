from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt


class SortableItem(QTableWidgetItem):
    """
    A table item that can be sorted as a number
    """

    def __lt__(self, other):
        role = Qt.ItemDataRole.UserRole

        value1 = self.data(role)
        value2 = other.data(role)

        return (value1 or 0) < (value2 or 0)
