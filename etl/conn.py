import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host ="localhost",
            user= "root",
            password = "",
            database="pccomponentes"
            
        )

        if conexion.is_connected():
            print("Conexion en verde, todo bien")   
            return conexion   
    except Error as e:
          print(f"Error al conectar a DB: {e}")
          return None
