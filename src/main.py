from store import Store
from item import Item

def main():
    my_store = Store("Tienda 1")

    nike_shoes = Item(marca="Nike", talla=30, precio=160, numPares=1)
    fila_shoes = Item(marca="Fila", talla=40, precio=85, numPares=10)
    adidas_shoes = Item(marca="Adidas", talla=32, precio=150, numPares=22)
    fila_shoes2 = Item(marca="Fila", talla=42, precio=85, numPares=5)

    my_store.add_item(nike_shoes)
    my_store.add_item(fila_shoes)
    my_store.add_item(adidas_shoes)
    my_store.add_item(fila_shoes2)

    print(f"Tienda: {my_store.name}")

    print()
    print("Item")
    for item in my_store.items:
        print(f"- {item.marca} (Talla {item.talla}): ${item.precio} (Pares: {item.numPares})")

    total_value = my_store.get_total_value()
    print(f"Valor total del inventario: ${total_value:.2f}")

    my_store.close_db()

if __name__ == "__main__":
    main()