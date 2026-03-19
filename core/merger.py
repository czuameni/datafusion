class Merger:

    def merge_group(self, group):
        merged = {}

        keys = group[0].keys()

        for key in keys:
            values = []

            for r in group:
                val = r.get(key)

                if val is not None and str(val).strip().lower() not in ["", "nan"]:
                    values.append(str(val))

            if not values:
                merged[key] = None
            else:
                merged[key] = max(values, key=len)

        return merged