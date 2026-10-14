from database.connection import DatabaseConnection
from models.base_model import Model

class Cliente(Model):
    table_name = "clientes"
    fields = ["nombre", "apellido", "email", "telefono", "direccion_entrega"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def save(self):
        """INSERT - Crea un nuevo registro en la BD."""
        values = [getattr(self, field) for field in self.fields]
        placeholders = ', '.join(['?' for _ in self.fields])
        columns = ', '.join(self.fields)

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        # CORRECCIÓN: execute_query ya devuelve el ID y cierra la conexión internamente
        self.id_cliente = DatabaseConnection.execute_query(query, tuple(values))

        print(f"Cliente '{self.nombre}' guardado con ID {self.id_cliente}")