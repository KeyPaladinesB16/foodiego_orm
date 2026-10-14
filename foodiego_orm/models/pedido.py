
from models.base_model import Model


class Pedido(Model):
    """Modelo que representa la tabla pedidos."""

    table_name = "pedidos"
    primary_key = "id_pedido"

    fields = [
        "id_cliente",
        "id_restaurante",
        "id_repartidor",
        "estado",
        "total"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        """Guarda el pedido en la base de datos."""
        columns = ", ".join(self.fields)
        placeholders = ", ".join(["?"] * len(self.fields))
        values = tuple(
            getattr(self, field, None)
            for field in self.fields
        )

        query = (
            f"INSERT INTO {self.table_name} "
            f"({columns}) VALUES ({placeholders})"
        )

        from database.connection import DatabaseConnection

        conn, cursor = DatabaseConnection.execute_query(
            query, values
        )

        self.id_pedido = cursor.lastrowid
        conn.close()

        print(f"Pedido #{self.id_pedido} creado")

    def get_cliente(self):
        """Obtiene el cliente asociado al pedido."""
        from models.cliente import Cliente
        return Cliente.find_by_id(self.id_cliente)

    def get_restaurante(self):
        """Obtiene el restaurante asociado al pedido."""
        from models.restaurante import Restaurante
        return Restaurante.find_by_id(self.id_restaurante)

    def get_repartidor(self):
        """Obtiene el repartidor asignado."""
        from models.repartidor import Repartidor

        if self.id_repartidor is None:
            return None

        return Repartidor.find_by_id(self.id_repartidor)

    def detalles_pedido(self):
        """Muestra la información del pedido."""
        cliente = self.get_cliente()
        restaurante = self.get_restaurante()
        repartidor = self.get_repartidor()

        print(f"\n{'=' * 50}")
        print(f"PEDIDO #{self.id_pedido}")
        print(f"{'=' * 50}")

        if cliente:
            print(
                f"Cliente: {cliente.nombre} "
                f"{cliente.apellido}"
            )
            print(f"Dirección: {cliente.direccion_entrega}")

        if restaurante:
            print(f"Restaurante: {restaurante.nombre}")
            print(f"Tipo: {restaurante.tipo_cocina}")

        print(f"Fecha: {self.fecha_pedido}")
        print(f"Total: ${self.total}")
        print(f"Estado: {self.estado.upper()}")

        if repartidor:
            print(
                f"Repartidor: {repartidor.nombre} "
                f"{repartidor.apellido}"
            )
            print(
                f"Vehículo: {repartidor.tipo_vehiculo} "
                f"({repartidor.placa})"
            )
        else:
            print("Repartidor: Sin asignar")

        print(f"{'=' * 50}\n")
