class DataMapper:

    STANDARD = ["name", "email", "phone", "address", "website", "notes"]

    def suggest(self, columns):
        mapping = {}

        for col in columns:

            # 🔥 TO DODAJESZ
            if col.startswith("__"):
                mapping[col] = None
                continue

            c = col.lower()

            if "mail" in c:
                mapping[col] = "email"
            elif "phone" in c or "tel" in c:
                mapping[col] = "phone"
            elif "name" in c:
                mapping[col] = "name"
            elif "addr" in c:
                mapping[col] = "address"
            else:
                mapping[col] = None

        return mapping

    def apply(self, df, mapping):
        df = df.rename(columns=mapping)

        for col in self.STANDARD:
            if col not in df:
                df[col] = None

        return df[self.STANDARD]