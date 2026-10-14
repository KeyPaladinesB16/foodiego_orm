
from models.base_model import Model
from database.connection import DatabaseConnection


class Restaurante(Model):
    """Modelo que representa la tabla restaurantes."""

    table_name = "restaurantes"
    primary_key = "id_restaurante"

    fields = [
        "nombre",
        "tipo_cocina",
        "direccion",
        "telefono",
        "calificacion_promedio"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        """Guarda el restaurante en la base de datos."""
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

        self.id_restaurante = cursor.lastrowid
        conn.close()

        print(
            f"Restaurante '{self.nombre}' guardado "
            f"con ID {self.id_restaurante}"
        )

    def get_pedidos(self):
        """Obtiene los pedidos de este restaurante."""
        from models.pedido import Pedido

        query = """
            SELECT * FROM pedidos
            WHERE id_restaurante = ?
            ORDER BY fecha_pedido DESC
        """

        conn = DatabaseConnection.get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(
                query, (self.id_restaurante,)
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
