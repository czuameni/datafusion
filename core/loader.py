import pandas as pd

class DataLoader:

    def load(self, file_paths):
        dfs = []

        for path in file_paths:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            elif path.endswith(".xlsx"):
                df = pd.read_excel(path)
            else:
                continue

            df["__source__"] = path
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)