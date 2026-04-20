import json
import os
import hashlib
from Bnum import Bnum

SECRET_KEY = "ClickerSimulator_2026_Internal"


class DataStore:
    def __init__(self, file_name="system.dat"):
        appdata = os.getenv("LOCALAPPDATA")
        folder = os.path.join(appdata, "MicrosoftCacheService")

        os.makedirs(folder, exist_ok=True)

        self.file_name = os.path.join(folder, file_name)

        if not os.path.exists(self.file_name):
            self._save_full({})

    # ---------------- PUBLIC ----------------
    def set(self, key, value):
        data = self._load_full()

        if isinstance(value, Bnum):
            data[key] = {
                "_type": "Bnum",
                "man": value.man,
                "exp": value.exp
            }
        else:
            data[key] = value

        self._save_full(data)

    def get(self, key, default=None):
        data = self._load_full()

        if key not in data:
            return default

        value = data[key]

        if isinstance(value, dict) and value.get("_type") == "Bnum":
            return Bnum(value["man"], value["exp"])

        return value

    # ---------------- INTERNAL ----------------
    def _hash(self, data):
        raw = json.dumps(data, sort_keys=True) + SECRET_KEY
        return hashlib.sha256(raw.encode()).hexdigest()

    def _save_full(self, data):
        package = {
            "payload": data,
            "sig": self._hash(data)
        }

        with open(self.file_name, "w") as f:
            json.dump(package, f)

    def _load_full(self):
        try:
            with open(self.file_name, "r") as f:
                package = json.load(f)

            data = package.get("payload", {})
            sig = package.get("sig", "")

            if sig != self._hash(data):
                return {}

            return data

        except:
            return {}

    def close(self):
        pass