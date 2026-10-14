import sqlite3
import os

class DatabaseConnection:
    DB_PATH = os.path.join(os.path.dirname(__file__), 'foodiego.db')

    @classmethod
    def get_connection(cls):
        conn = sqlite3.connect(cls.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def execute_query(cls, query, params=()):
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def fetch_all(cls, query, params=()):
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()

    @classmethod
    def initialize_tables(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        sql_script = """
        CREATE TABLE IF NOT EXISTS clientes(
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL, apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, telefono TEXT,
            direccion_entrega TEXT NOT NULL,
            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS restaurantes(
            id_restaurante INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL, tipo_cocina TEXT,
            direccion TEXT NOT NULL, telefono TEXT,
            calificacion_promedio REAL DEFAULT 0.0
        );
        CREATE TABLE IF NOT EXISTS repartidores(
            id_repartidor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL, apellido TEXT NOT NULL,
            tipo_vehiculo TEXT, placa TEXT UNIQUE,
            estado TEXT DEFAULT 'disponible'
        );
        CREATE TABLE IF NOT EXISTS pedidos(
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL, id_restaurante INTEGER NOT NULL,
            id_repartidor INTEGER, fecha_pedido TEXT DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'pendiente', total REAL NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id_restaurante),
            FOREIGN KEY (id_repartidor) REFERENCES repartidores(id_repartidor)
        );
        """
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("✅ Tablas creadas correctamente.")