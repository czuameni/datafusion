import os

class Exporter:

    def ensure_folder(self, path):
        folder = os.path.dirname(path)

        if folder:
            os.makedirs(folder, exist_ok=True)

    def export(self, df, path):
        self.ensure_folder(path)

        if path.endswith(".csv"):
            df.to_csv(path, index=False)

        elif path.endswith(".xlsx"):
            df.to_excel(path, index=False)

        else:
            raise ValueError("Unsupported file format")