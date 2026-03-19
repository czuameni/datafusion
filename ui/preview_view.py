from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView


class PreviewView(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.table = QTableWidget()

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        
        self.table.setMaximumHeight(300)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def set_data(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))

        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                value = str(df.iloc[i, j])
                self.table.setItem(i, j, QTableWidgetItem(value))
                self.table.resizeColumnsToContents()