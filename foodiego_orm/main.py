from database.connection import DatabaseConnection
from models.cliente import Cliente


def main():
    DatabaseConnection.initialize_tables()

    print("\n--- 1. CREANDO CLIENTE (CREATE) ---")
    cliente_nuevo = Cliente(
        nombre="Noemi",
        apellido="Perez",
        email="noemi@foodiego.com",
        telefono="5551234567",
        direccion_entrega="Av. Tecnológica 100"
    )
    cliente_nuevo.save()

    print("\n--- 2. LEYENDO TODOS (READ ALL) ---")
    clientes = Cliente.all()
    for c in clientes:
        print(f"ID: {c.id_cliente} | Nombre: {c.nombre} {c.apellido}")

    if clientes:
        primer_cliente = clientes[0]

        print("\n--- 3. ACTUALIZANDO (UPDATE) ---")
        primer_cliente.direccion_entrega = "Calle Nueva 456"
        primer_cliente.update()

        print("\n--- 4. ELIMINANDO (DELETE) ---")
        primer_cliente.delete()


if __name__ == "__main__":
    main()