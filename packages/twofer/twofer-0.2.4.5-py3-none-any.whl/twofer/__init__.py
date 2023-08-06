import json
from importlib import metadata
from typing import Any, ItemsView, Iterator, KeysView, ValuesView


try:
    VERSION = metadata.version(__name__)
except:
    VERSION = 'unknown'


class Database:

    def __init__(self, source: str) -> None:
        self.source = source
        self.db = {}

    def __len__(self) -> int:
        return self.db.__len__()

    def __getitem__(self, key: str) -> Any | None:
        return self.db.__getitem__(key)

    def __setitem__(self, key: str, value: Any | None) -> None:
        self.db.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self.db.__delitem__(key)

    def __iter__(self) -> Iterator:
        return self.db.__iter__()

    def __contains__(self, item: str):
        return self.db.__contains__(item)

    def clear(self) -> None:
        self.db.clear()

    def get(self, key: str, default: Any | None = None) -> Any | None:
        return self.db.get(key, default)

    def items(self) -> ItemsView[str, Any | None]:
        return self.db.items()

    def keys(self) -> KeysView[str]:
        return self.db.keys()

    def values(self) -> ValuesView[Any | None]:
        return self.db.values()

    def pop(self, key: str, default: Any | None) -> Any | None:
        return self.db.pop(key, default)

    def setdefault(self, key: str, default: Any | None) -> Any | None:
        return self.db.setdefault(key, default)

    def load(self) -> None:
        try:
            with open(self.source, encoding='utf-8') as f:
                self.db.clear()
                self.db.update(json.load(f))
        except FileNotFoundError:
            pass

    def save(self) -> None:
        with open(self.source, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2)
