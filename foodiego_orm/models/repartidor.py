
from models.base_model import Model
from database.connection import DatabaseConnection


class Repartidor(Model):
    """Modelo que representa la tabla repartidores."""

    table_name = "repartidores"
    primary_key = "id_repartidor"

    fields = [
        "nombre",
        "apellido",
        "tipo_vehiculo",
        "placa",
        "estado"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        """Guarda el repartidor en la base de datos."""
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

        conn, cursor = DatabaseConnection.execute_query(
            query, values
        )

        self.id_repartidor = cursor.lastrowid
        conn.close()

        print(
            f"Repartidor '{self.nombre} {self.apellido}' "
            f"guardado con ID {self.id_repartidor}"
        )

    def get_pedidos_asignados(self):
        """Obtiene los pedidos asignados al repartidor."""
        from models.pedido import Pedido

        query = """
            SELECT * FROM pedidos
            WHERE id_repartidor = ?
            ORDER BY fecha_pedido DESC
        """

        conn = DatabaseConnection.get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(
                query, (self.id_repartidor,)
            )

            filas = cursor.fetchall()
            columnas = [
                description[0]
                for description in cursor.description
            ]

            return [
                Pedido(**dict(zip(columnas, fila)))
                for fila in filas
            ]
        finally:
            conn.close()

    def asignar_pedido(self, id_pedido):
        """Asigna un pedido y actualiza su estado."""

        query = """
            UPDATE pedidos
            SET id_repartidor = ?, estado = 'en_camino'
            WHERE id_pedido = ?
        """

        conn, cursor = DatabaseConnection.execute_query(
            query, (self.id_repartidor, id_pedido)
        )

        actualizado = cursor.rowcount
        conn.close()

        if actualizado:
            self.update(estado="en_ruta")
            print(f"Pedido {id_pedido} asignado.")
        else:
            print("No se encontró el pedido.")
