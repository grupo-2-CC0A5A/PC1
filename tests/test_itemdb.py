import unittest
from unittest.mock import Mock
from src.item import (
    Item,
    ItemDB,
    MissingMarcaException,
    MissingPrecioException,
    MissingTallaException,
    MissingNumParesException,
)

class TestItem(unittest.TestCase):
    def test_valid_item(self):
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=10)
        self.assertEqual(item.marca, "Nike")
        self.assertEqual(item.talla, 42)
        self.assertEqual(item.precio, 100.0)
        self.assertEqual(item.numPares, 10)

    def test_invalid_item_negative_price(self):
        with self.assertRaises(AssertionError):
            Item(marca="Adidas", talla=40, precio=-50.0, numPares=5)


class TestItemDB(unittest.TestCase):
    def setUp(self):
        # Instanciar normalmente y reemplazar DB real por un mock
        self.itemdb = ItemDB()
        self.mock_db = Mock()
        self.itemdb._db = self.mock_db

    def test_add_item_creates_new(self):
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=5)
        self.mock_db.find_by_marca_talla.return_value = None
        self.mock_db.create.return_value = 1

        result = self.itemdb.add_item(item)

        self.mock_db.create.assert_called_with(item.to_dict())
        self.assertEqual(result, 1)

    def test_add_item_updates_existing(self):
        existing_item = Item(id=1, marca="Nike", talla=42, precio=100.0, numPares=3)
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=2)

        # 🔹 Devolver dict en lugar de objeto
        self.mock_db.find_by_marca_talla.return_value = existing_item.to_dict()
        self.mock_db.update.return_value = None

        result = self.itemdb.add_item(item)

        self.mock_db.update.assert_called_with(1, {"numPares": 5})
        self.assertEqual(result, 1)

    def test_add_item_missing_marca(self):
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=2)
        item.marca = None  # invalidamos después de creado
        with self.assertRaises(MissingMarcaException):
            self.itemdb.add_item(item)

    def test_add_item_missing_precio(self):
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=2)
        item.precio = None
        with self.assertRaises(MissingPrecioException):
            self.itemdb.add_item(item)

    def test_add_item_missing_talla(self):
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=2)
        item.talla = None
        with self.assertRaises(MissingTallaException):
            self.itemdb.add_item(item)

    def test_add_item_missing_numPares(self):
        item = Item(marca="Nike", talla=42, precio=100.0, numPares=2)
        item.numPares = None
        with self.assertRaises(MissingNumParesException):
            self.itemdb.add_item(item)


if __name__ == "__main__":
    unittest.main()
