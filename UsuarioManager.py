import pyodbc

class UsuarioManager:
    def __init__(self):
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDIregistroDigital;'
            'UID=sa;'
            'PWD=13652938'
        )

    def get_user(self, username):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Usuario WHERE username = ?"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
