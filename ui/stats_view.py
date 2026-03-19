from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class StatsView(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel("Stats will appear here")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def set_data(self, report):
        text = (
            f"Input: {report['input']}\n"
            f"Output: {report['output']}\n"
            f"Duplicates removed: {report['duplicates_removed']}\n"
        )

        self.label.setText(text)