from database.connection import DatabaseConnection


class Model:
    fields = []
    table_name = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_pk_column(self):
        return f"id_{self.table_name}"

    def _row_to_dict(self, row):
        return dict(zip(row.keys(), row))

    def save(self):
        values = [getattr(self, field) for field in self.fields]
        placeholders = ', '.join(['?' for _ in self.fields])
        columns = ', '.join(self.fields)
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        last_id = DatabaseConnection.execute_query(query, tuple(values))
        setattr(self, self._get_pk_column(), last_id)
        print(f"✅ Guardado en '{self.table_name}' con ID: {last_id}")
        return last_id

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.table_name}"
        rows = DatabaseConnection.fetch_all(query)
        objects = []
        for row in rows:
            obj_dict = dict(zip(row.keys(), row))
            objects.append(cls(**obj_dict))
        return objects

    @classmethod
    def find_by_id(cls, id_value):
        id_column = f"id_{cls.table_name}"
        query = f"SELECT * FROM {cls.table_name} WHERE {id_column} = ?"
        rows = DatabaseConnection.fetch_all(query, (id_value,))
        if rows:
            obj_dict = dict(zip(rows[0].keys(), rows[0]))
            return cls(**obj_dict)
        return None

    def update(self):
        id_column = self._get_pk_column()
        id_value = getattr(self, id_column, None)
        if not id_value:
            print("❌ Error: El objeto no tiene ID para actualizar.");
            return

        values = [getattr(self, field) for field in self.fields]
        values.append(id_value)
        set_clause = ', '.join([f"{field} = ?" for field in self.fields])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {id_column} = ?"

        DatabaseConnection.execute_query(query, tuple(values))
        print(f"✅ Registro en '{self.table_name}' actualizado.")

    def delete(self):
        id_column = self._get_pk_column()
        id_value = getattr(self, id_column, None)
        if not id_value:
            print("❌ Error: El objeto no tiene ID para eliminar.");
            return

        query = f"DELETE FROM {self.table_name} WHERE {id_column} = ?"
        DatabaseConnection.execute_query(query, (id_value,))
        print(f"✅ Registro en '{self.table_name}' eliminado.")