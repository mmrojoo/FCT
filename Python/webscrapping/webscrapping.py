import requests
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient("mongo", 27017)
db = client['formula4youdb']
collection = db['pilotos']

# URL de la página web
url = "https://www.formula1.com/en/drivers.html"

try:
    # Realizar la solicitud GET a la página web
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos los datos
    escuderias = [p_tag.text for p_tag in soup.find_all('p', class_='listing-item--team f1--xxs f1-color--gray5')]
    ranking = [div_tag.text for div_tag in soup.find_all('div', class_='rank')]
    puntos = [div_tag.text for div_tag in soup.find_all('div', class_='f1-wide--s')]
    nombres = [span_tag.text.strip() for span_tag in
               soup.find_all('span', class_='d-block f1--xxs f1-color--carbonBlack')]
    apellidos = [span_tag.text.strip() for span_tag in
                 soup.find_all('span', class_='d-block f1-bold--s f1-color--carbonBlack')]

    # Verificar y actualizar los datos en la base de datos
    for escuderia, rank, punto, nombre, apellido in zip(escuderias, ranking, puntos, nombres, apellidos):
        driver = {
            "nombre": nombre,
            "apellido": apellido
        }

        # Buscar si el piloto ya existe en la base de datos
        existing_driver = collection.find_one(driver)

        if existing_driver:
            print(f"Actualizando piloto {nombre} {apellido}")
            # Actualizar el registro existente si los datos han cambiado
            update_data = {
                "$set": {
                    "escuderia": escuderia,
                    "ranking": rank,
                    "puntos": punto
                }
            }
            collection.update_one(driver, update_data)
        else:
            print(f"Insertando nuevo piloto {nombre} {apellido}")
            # Insertar un nuevo registro si el piloto no existe
            new_driver = {
                "escuderia": escuderia,
                "ranking": rank,
                "puntos": punto,
                "nombre": nombre,
                "apellido": apellido
            }
            collection.insert_one(new_driver)

    # Cerrar la conexión a MongoDB
    client.close()

    print("Los datos se actualizaron correctamente en la base de datos.")

except Exception as e:
    print("Error al actualizar los datos en la base de datos:", e)
