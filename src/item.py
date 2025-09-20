from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict

from db import DB

@dataclass
class Item:
    marca: str
    talla: int
    precio: float
    numPares: int = 0
    id: int = field(default=None, compare=False)

    def __post_init__(self):
        assert self.precio >= 0, f"precio {self.precio} should be positive"
        assert self.numPares >= 0, f"numPares {self.numPares} should be positive"
        assert self.talla > 0, f"talla {self.talla} should be positive"

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, tuple):
            return Item(id=data[0], marca=data[1], talla=data[2], precio=data[3], numPares=data[4])
        return Item(**data)
    def to_dict(self):
        return asdict(self)


class ItemDB:
    def __init__(self):
        self._db = DB(".", "store")

    def find_by_marca_talla(self, marca, talla) -> Item:
        data = self._db.find_by_marca_talla(marca, talla)
        if data is None:
            return None
        return Item.from_dict(data)

    def add_item(self, item: Item):
        if item.marca is None:
            raise MissingMarcaException
        if item.precio is None:
            raise MissingPrecioException
        if item.numPares is None:
            raise MissingNumParesException
        if item.talla is None:
            raise MissingTallaException

        existing_item = self.find_by_marca_talla(item.marca, item.talla)
        if existing_item:
            # update item if marca and talla match
            new_quantity = existing_item.numPares + item.numPares
            self._db.update(existing_item.id, {"numPares": new_quantity})
            return existing_item.id
        else:
            return self._db.create(item.to_dict())

    def get_item(self, id) -> Item:
        data = self._db.read(id)
        if data is None:
            return None
        return Item.from_dict(data)

    def get_all_items(self) -> list[Item]:
        data = self._db.read_all()
        return [Item.from_dict(item) for item in data]

    def update_item(self, id, mods) -> None:
        self._db.update(id, mods)

    def delete_item(self, id) -> None:
        self._db.delete(id)

    def delete_all_items(self) -> None:
        self._db.delete_all()

    def count_items(self):
        return self._db.count()

    def close(self):
        self._db.close()


class ItemException(Exception):
    pass

class MissingMarcaException(ItemException):
    pass

class MissingTallaException(ItemException):
    pass

class MissingPrecioException(ItemException):
    pass

class MissingNumParesException(ItemException):
    pass