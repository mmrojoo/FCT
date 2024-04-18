import pymongo
import bcrypt
import re
from pymongo import MongoClient

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb', 27017)
db = client['formula4youdb']
collection = db['user']


def verificar_correo_existente(correo):
    """Verifica si el correo electrónico ya existe en la base de datos."""
    usuario_existente = collection.find_one({"correo": correo})
    return usuario_existente is not None


def validar_correo(correo):
    """Valida el formato del correo electrónico."""
    # Expresión regular para validar el formato del correo electrónico
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, correo)


def registrar_usuario():
    print("Registro de Usuario")
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")

    # Validar el correo electrónico
    while True:
        correo = input("Correo electrónico: ")
        if validar_correo(correo):
            break
        else:
            print("Formato de correo electrónico inválido. Inténtelo de nuevo.")

    # Solicitar y validar la contraseña
    while True:
        password1 = input("Contraseña: ")
        password2 = input("Repetir contraseña: ")

        if password1 == password2:
            break
        else:
            print("Las contraseñas no coinciden. Inténtelo de nuevo.")

    # Verificar si el correo electrónico ya existe
    if verificar_correo_existente(correo):
        print("El correo electrónico ya está registrado.")
        return

    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())

    # Crear el documento del usuario
    usuario = {
        "nombre": nombre,
        "apellidos": apellidos,
        "correo": correo,
        "contraseña": hashed_password.decode('utf-8')  # Convertir bytes a string
    }

    # Insertar el usuario en la base de datos
    try:
        collection.insert_one(usuario)
        print("Usuario registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")


if __name__ == "__main__":
    registrar_usuario()
