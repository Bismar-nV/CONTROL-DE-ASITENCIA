import pyodbc
import base64

class DocenteManager:
    def __init__(self):
        self.connection = pyodbc.connect(
             'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=NOGALES\\NOGALES;'  
            'DATABASE=PDIregistroDigital;'
            'UID=sa;'
            'PWD=13652938'
        )

    def add_docente(self, nombre, apellido, email, foto, estado):
        query = '''INSERT INTO Docente (nombre, apellido, email, foto, estado) 
                   VALUES (?, ?, ?, ?, ?)'''
        cursor = self.connection.cursor()
        try:
            foto_binario = base64.b64decode(foto.split(',')[1]) if foto else None
            cursor.execute(query, (nombre, apellido, email, foto_binario, estado))
            self.connection.commit()
        except Exception as e:
            print(f"Error al agregar docente: {e}")
        finally:
            cursor.close()

    def get_docentes(self):
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Docente"
            cursor.execute(query)
            docentes = cursor.fetchall()
            return docentes
        except Exception as e:
            print(f"Error al obtener docentes: {e}")
            return []
        finally:
            cursor.close()

    def update_docente(self, docente_id, nombre, apellido, email, foto, estado):
        cursor = self.connection.cursor()
        try:
            if foto:
                query = '''UPDATE Docente SET nombre = ?, apellido = ?, email = ?, foto = CONVERT(varbinary(max), ?), estado = ? WHERE id = ?'''
                foto_binario = base64.b64decode(foto.split(',')[1])  # Decodifica la imagen base64
                cursor.execute(query, (nombre, apellido, email, foto_binario, estado, docente_id))
            else:
                query = '''UPDATE Docente SET nombre = ?, apellido = ?, email = ?, estado = ? WHERE id = ?'''
                cursor.execute(query, (nombre, apellido, email, estado, docente_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al actualizar docente: {e}")
        finally:
            cursor.close()

    def delete_docente(self, docente_id):
        query = '''UPDATE Docente SET estado = ? WHERE id = ?'''
        cursor = self.connection.cursor()
        try:
            estado_inactivo = 0  # Suponiendo que el estado 0 indica "inactivo"
            cursor.execute(query, (estado_inactivo, docente_id))
            self.connection.commit()
        except Exception as e:
            print(f"Error al cambiar el estado del docente: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        try:
            self.connection.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
