import pytest
from unittest.mock import Mock, patch, MagicMock

from src.store import Store
from src.item import Item


class TestStore:
    
    @patch('src.store.ItemDB')
    def test_store_init_sin_items(self, mock_itemdb_class):
        """Prueba la inicialización de Store sin items iniciales."""
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        mock_itemdb.get_all_items.return_value = []
        
        store = Store("Mi Tienda")
        
        assert store.name == "Mi Tienda"
        assert store.items == []
        mock_itemdb.get_all_items.assert_called_once()
    
    @patch('src.store.ItemDB')
    def test_store_init_con_items(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        items_iniciales = [Mock(), Mock()]
        store = Store("Mi Tienda", items_iniciales)
        
        assert store.name == "Mi Tienda"
        assert store.items == items_iniciales
        # No debe llamar get_all_items cuando se pasan items
        mock_itemdb.get_all_items.assert_not_called()
    
    @patch('src.store.ItemDB')
    def test_add_item(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        mock_itemdb.get_all_items.return_value = []
        mock_itemdb.add_item.return_value = 1
        
        # Items después de agregar
        new_item = Mock()
        new_item.id = None
        updated_items = [new_item]
        mock_itemdb.get_all_items.side_effect = [[], updated_items]
        
        store = Store("Mi Tienda")
        store.add_item(new_item)
        
        mock_itemdb.add_item.assert_called_once_with(new_item)
        assert new_item.id == 1
        assert store.items == updated_items
    
    @patch('src.store.ItemDB')
    def test_remove_item(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        item1 = Mock()
        item2 = Mock()
        items_iniciales = [item1, item2]
        
        store = Store("Mi Tienda", items_iniciales)
        store.remove_item(item1)
        
        assert len(store.items) == 1
        assert item1 not in store.items
        assert item2 in store.items
    
    @patch('src.store.ItemDB')
    def test_get_total_value_tienda_vacia(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        store = Store("Mi Tienda", [])
        total = store.get_total_value()
        
        assert total == 0
    
    @patch('src.store.ItemDB')
    def test_get_total_value_con_items(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        # Crear items mock
        item1 = Mock()
        item1.precio = 100.0
        item1.numPares = 2
        
        item2 = Mock()
        item2.precio = 50.0
        item2.numPares = 3
        
        items = [item1, item2]
        store = Store("Mi Tienda", items)
        total = store.get_total_value()
        
        # (100.0 * 2) + (50.0 * 3) = 200 + 150 = 350
        assert total == 350.0
    
    @patch('src.store.ItemDB')
    def test_get_total_value_items_sin_stock(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        # Items con numPares = 0
        item1 = Mock()
        item1.precio = 100.0
        item1.numPares = 0
        
        item2 = Mock()
        item2.precio = 200.0
        item2.numPares = 0
        
        items = [item1, item2]
        store = Store("Mi Tienda", items)
        total = store.get_total_value()
        
        assert total == 0
    
    @patch('src.store.ItemDB')
    def test_close_db(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        store = Store("Mi Tienda")
        store.close_db()
        
        mock_itemdb.close.assert_called_once()
    
    @patch('src.store.ItemDB')
    def test_add_item_actualiza_lista(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        mock_itemdb.get_all_items.return_value = []
        mock_itemdb.add_item.return_value = 5
        
        # Simular que después de agregar, la DB retorna más items
        item_existente = Mock()
        item_nuevo = Mock()
        item_nuevo.id = None
        items_actualizados = [item_existente, item_nuevo]
        
        mock_itemdb.get_all_items.side_effect = [[], items_actualizados]
        
        store = Store("Mi Tienda")
        assert len(store.items) == 0  # Inicialmente vacía
        
        store.add_item(item_nuevo)
        
        assert item_nuevo.id == 5
        assert len(store.items) == 2
        assert store.items == items_actualizados
    
    @patch('src.store.ItemDB')
    def test_remove_item_no_existente(self, mock_itemdb_class):
        mock_itemdb = Mock()
        mock_itemdb_class.return_value = mock_itemdb
        
        item1 = Mock()
        items_iniciales = [item1]
        store = Store("Mi Tienda", items_iniciales)
        
        item_inexistente = Mock()
        
        with pytest.raises(ValueError):
            store.remove_item(item_inexistente)
