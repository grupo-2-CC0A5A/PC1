from item import ItemDB

class Store:
    def __init__(self, name, items=None):
        self.name = name
        self.item_db = ItemDB()
        if items is None:
            self.items = self.item_db.get_all_items()
        else:
            self.items = items

    def add_item(self, new_item):
        item_id = self.item_db.add_item(new_item)
        new_item.id = item_id

        self.items = self.item_db.get_all_items()

    def remove_item(self, item):
        self.items.remove(item)

    def get_total_value(self):
        return sum(item.precio * item.numPares for item in self.items)

    def close_db(self):
        self.item_db.close()