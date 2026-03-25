from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QLabel, QMessageBox,
    QTabWidget, QProgressBar, QListWidget
)

from PyQt6.QtGui import QIcon

from core.loader import DataLoader
from core.mapper import DataMapper
from services.pipeline import Pipeline
from core.exporter import Exporter

from ui.mapping_view import MappingView
from ui.preview_view import PreviewView
from ui.stats_view import StatsView
from services.mapping_service import MappingService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DataFusion")
        self.setWindowIcon(QIcon("datafusion.ico"))
        self.setGeometry(100, 100, 1000, 700)

        self.loader = DataLoader()
        self.mapper = DataMapper()
        self.pipeline = Pipeline()

        self.exporter = Exporter()
        self.result_df = None

        self.mapping_service = MappingService()

        self.report_data = None

        self.files = []
        self.mapping = {}

        self.init_ui()

    def init_ui(self):
        container = QWidget()
        layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload Files")
        self.upload_btn.clicked.connect(self.upload_files)
        layout.addWidget(self.upload_btn)

        self.status_label = QLabel("No files loaded")
        layout.addWidget(self.status_label)

        self.process_btn = QPushButton("Process")
        self.process_btn.clicked.connect(self.process_data)
        layout.addWidget(self.process_btn)

        self.process_status = QLabel("")
        layout.addWidget(self.process_status)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_data)
        layout.addWidget(self.export_btn)

        self.export_report_btn = QPushButton("Export Report")
        self.export_report_btn.clicked.connect(self.export_report)
        layout.addWidget(self.export_report_btn)

        self.save_mapping_btn = QPushButton("Save Mapping")
        self.save_mapping_btn.clicked.connect(self.save_mapping)
        layout.addWidget(self.save_mapping_btn)

        self.load_mapping_btn = QPushButton("Load Mapping")
        self.load_mapping_btn.clicked.connect(self.load_mapping)
        layout.addWidget(self.load_mapping_btn)

        self.tabs = QTabWidget()

        self.mapping_view = MappingView()
        self.tabs.addTab(self.mapping_view, "Mapping")

        self.preview_before = PreviewView()
        self.preview_before.table.setEditTriggers(self.preview_before.table.EditTrigger.NoEditTriggers)
        self.tabs.addTab(self.preview_before, "Before")

        self.preview_after = PreviewView()
        self.tabs.addTab(self.preview_after, "After")

        self.stats = StatsView()
        self.tabs.addTab(self.stats, "Stats")

        self.duplicates_list = QListWidget()
        self.tabs.addTab(self.duplicates_list, "Duplicates")

        layout.addWidget(self.tabs)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def upload_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select files",
            "",
            "Data Files (*.csv *.xlsx *.xls)"
        )

        if not files:
            return

        self.files = files
        self.status_label.setText(f"{len(files)} files loaded")

        print("📂 Files selected:", files)

        try:
            df = self.loader.load(files)

            print("📊 Columns detected:", list(df.columns))

            mapping = self.mapper.suggest(df.columns)

            print("🧠 Suggested mapping:", mapping)

            self.mapping_view.set_columns(df.columns, mapping)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load files:\n{e}")

    def process_data(self):

        if not self.files:
            QMessageBox.warning(self, "Warning", "No files selected")
            return

        mapping = self.mapping_view.get_mapping()

        if not mapping:
            QMessageBox.warning(self, "Warning", "No mapping defined")
            return

        print("🚀 Processing started...")
        print("📌 Mapping used:", mapping)

        self.process_status.setText("Processing...")
        self.progress.setValue(20)

        try:
            threshold = self.slider.value() if hasattr(self, "slider") else 60

            df_before, result_df, report, groups = self.pipeline.run(self.files, mapping)

            self.before_df = df_before
            self.result_df = result_df

            self.preview_before.set_data(df_before)
            self.preview_after.set_data(result_df)

            self.stats.set_data(report)

            self.report_data = report

            self.duplicate_groups = groups

            self.duplicates_list.clear()

            for i, group in enumerate(groups):
                if len(group) > 1:
                    self.duplicates_list.addItem(f"Group {i+1}: {len(group)} records")

            self.progress.setValue(100)
            self.process_status.setText("Done")

        except Exception as e:
            self.process_status.setText("Error")
            self.progress.setValue(0)

            QMessageBox.critical(self, "Error", f"Processing failed:\n{e}")

    def export_data(self):

        if self.result_df is None:
            QMessageBox.warning(self, "Warning", "No data to export")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )

        if not path:
            return

        try:
            self.exporter.export(self.result_df, path)
            QMessageBox.information(self, "Success", "File exported successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{e}")

    def export_report(self):

        if self.report_data is None:
            QMessageBox.warning(self, "Warning", "No report to export")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save report",
            "",
            "JSON Files (*.json)"
        )

        if not path:
            return

        try:
            import json

            with open(path, "w") as f:
                json.dump(self.report_data, f, indent=4)

            QMessageBox.information(self, "Success", "Report exported successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{e}")

    def save_mapping(self):

        mapping = self.mapping_view.get_mapping()

        if not mapping:
            QMessageBox.warning(self, "Warning", "No mapping to save")
            return

        name, ok = QFileDialog.getSaveFileName(
            self,
            "Save mapping",
            "",
            "JSON Files (*.json)"
        )

        if not name:
            return

        try:
            import json
            with open(name, "w") as f:
                json.dump(mapping, f, indent=4)

            QMessageBox.information(self, "Success", "Mapping saved")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save failed:\n{e}")

    def load_mapping(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load mapping",
            "",
            "JSON Files (*.json)"
        )

        if not path:
            return

        try:
            import json
            with open(path, "r") as f:
                mapping = json.load(f)

            columns = []
            for row in range(self.mapping_view.table.rowCount()):
                col_name = self.mapping_view.table.item(row, 0).text()
                columns.append(col_name)

            self.mapping_view.set_columns(columns, mapping)

            QMessageBox.information(self, "Success", "Mapping loaded")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Load failed:\n{e}")
