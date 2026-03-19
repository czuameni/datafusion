import json
import os

class MappingService:

    BASE_PATH = "storage/mappings"

    def save(self, mapping, name="default"):
        os.makedirs(self.BASE_PATH, exist_ok=True)

        path = os.path.join(self.BASE_PATH, f"{name}.json")

        with open(path, "w") as f:
            json.dump(mapping, f, indent=4)

    def load(self, name="default"):
        path = os.path.join(self.BASE_PATH, f"{name}.json")

        if not os.path.exists(path):
            return None

        with open(path, "r") as f:
            return json.load(f)