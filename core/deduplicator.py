from difflib import SequenceMatcher

class Deduplicator:

    def similarity(self, a, b):
        return SequenceMatcher(None, str(a), str(b)).ratio()

    def score(self, r1, r2):
        score = 0

        email1 = str(r1.get("email") or "").lower()
        email2 = str(r2.get("email") or "").lower()

        if email1 and email1 == email2:
            return 100

        name1 = str(r1.get("name") or "").lower()
        name2 = str(r2.get("name") or "").lower()

        phone1 = str(r1.get("phone") or "")
        phone2 = str(r2.get("phone") or "")

        address1 = str(r1.get("address") or "").lower()
        address2 = str(r2.get("address") or "").lower()

        if name1 and name2 and self.similarity(name1, name2) > 0.85:
            score += 50

        if phone1 and phone2 and self.similarity(phone1, phone2) > 0.9:
            score += 30

        if address1 and address2 and self.similarity(address1, address2) > 0.8:
            score += 20

        return score

    def create_blocks(self, records):
        blocks = {}

        for r in records:
            key = None

            # 🔹 1. email domain (najlepsze)
            email = str(r.get("email") or "").lower()

            if "@" in email:
                key = email.split("@")[1]

            # 🔹 2. fallback: pierwsza litera nazwiska
            elif r.get("name"):
                key = str(r["name"])[0].lower()

            else:
                key = "unknown"

            blocks.setdefault(key, []).append(r)

        return blocks

    def group(self, df):
        records = df.to_dict(orient="records")

        blocks = self.create_blocks(records)

        groups = []

        for block_key, block_records in blocks.items():
            used = set()

            for i, r1 in enumerate(block_records):
                if i in used:
                    continue

                group = [r1]

                for j, r2 in enumerate(block_records):
                    if j != i and j not in used:
                        if self.score(r1, r2) >= 60:
                            group.append(r2)
                            used.add(j)

                groups.append(group)

        return groups