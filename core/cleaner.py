class DataCleaner:

    def clean(self, df):
        df = df.copy()

        df.columns = [c.strip().lower() for c in df.columns]

        df = df.drop_duplicates()
        df = df.dropna(how="all")

        return df