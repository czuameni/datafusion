from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox


class MappingView(QWidget):

    STANDARD = ["name", "email", "phone", "address", "website", "notes"]

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.table = QTableWidget()

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def set_columns(self, columns, suggestions):
        self.table.setRowCount(len(columns))
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["Source Column", "Mapped To"])

        for i, col in enumerate(columns):
            self.table.setItem(i, 0, QTableWidgetItem(col))

            combo = QComboBox()
            combo.addItem("")

            for field in self.STANDARD:
                combo.addItem(field)

            if suggestions.get(col):
                combo.setCurrentText(suggestions[col])

            self.table.setCellWidget(i, 1, combo)

    def get_mapping(self):
        mapping = {}

        for row in range(self.table.rowCount()):
            source = self.table.item(row, 0).text()
            combo = self.table.cellWidget(row, 1)

            target = combo.currentText()

            if target:
                mapping[source] = target

        return mapping