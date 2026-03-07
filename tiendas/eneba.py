import requests # Importamos la librería requests.
# Esta librería permite hacer peticiones HTTP desde Python

def buscar(juego):
# Definimos una función llamada "buscar".
# Recibe como parámetro "juego", que será el texto que queremos buscar.

    url = "https://ihjzq5lw2r-dsn.algolia.net/1/indexes/*/queries"
    # Esta es la URL del servidor al que vamos a hacer la petición.
    # Eneba usa un sistema de búsqueda llamado Algolia.
    # Muchas webs usan Algolia porque es muy rápido para buscar productos.
    #
    # /1/indexes/*/queries
    # significa: hacer consultas (queries) en los índices de búsqueda.

    headers = {
        "x-algolia-api-key": "53864095e814940ffed0f69a897331f1",
        "x-algolia-application-id": "IHJZQ5LW2R",
        "content-type": "application/json"
    }
    # Los "headers" son información extra que se envía junto con la petición.
    # Funcionan como metadatos que el servidor necesita para aceptar la consulta.
    #
    # En este caso Algolia requiere:
    # - api key
    # - application id
    # - content-type

    data = {
    # Aquí construimos el cuerpo de la petición (body).
    #
    # En HTTP POST los datos se envían en el cuerpo.
    # En este caso usamos JSON porque la API lo espera así.

        "requests": [
            {
                "indexName": "products_ar",  # indexName es la "base de datos de búsqueda"
                # En este caso productos de Argentina
                "query": juego, # El texto que el usuario quiere buscar
                "page": 0, # página de resultados (para paginación)
                "hitsPerPage": 10 # cuantos resultados queremos
            }
        ]
    }

    r = requests.post(url, json=data, headers=headers) # Aquí hacemos la petición HTTP POST.
    # requests.post envía:
    # - la URL
    # - el JSON
    # - los headers
    #
    # El servidor responde con datos en formato JSON.

    resultados = [] # Creamos una lista vacía donde vamos a guardar
    # los resultados que encontremos.

    for item in r.json()["results"][0]["hits"]: # r.json() convierte la respuesta del servidor (JSON)
    # en estructuras de Python (diccionarios y listas).
    # La estructura de Algolia es:
    #
    # results
    #   └ hits
    #       └ cada producto
    #
    # Por eso accedemos así:
    #
    # r.json()["results"][0]["hits"]
    #
    # results → lista de queries
    # [0] → nuestra única query
    # hits → productos encontrados

        titulo = item["translations"]["en_US"]["name"]
        # Cada item es un producto.
        #
        # Dentro tiene muchos datos:
        # - nombre
        # - precios
        # - slug
        # - plataforma
        #
        # Aquí obtenemos el nombre en inglés.

        precios = item["lowestPrice"]
        # lowestPrice es un diccionario con precios
        # en distintas monedas.
        #
        # Ejemplo:
        # {
        #   "USD": 1299,
        #   "EUR": 1199
        # }
        #
        # Los precios vienen en centavos.

        # --- LA SOLUCIÓN ---
        # Si precios es None (no hay stock/precio), saltamos a la siguiente iteración
        if not precios:
            continue

        # elegir moneda
        if "USD" in precios: # Preferimos USD si existe.
            moneda = "USD"
        elif "EUR" in precios: # Si no, EUR.
            moneda = "EUR"
        else:
            moneda = list(precios.keys())[0] # Si no, usamos la primera disponible.

        precio = precios[moneda] / 100  # Convertimos centavos a unidades. 1299 → 12.99

        slug = item["slug"]  # slug es la parte de la URL del producto.
        # Ejemplo: steam-elden-ring-pc-steam-key-global

        link = f"https://www.eneba.com/es/{slug}"  #Construimos el link completo usando f-string.
        # Es la forma moderna de insertar variables en strings.

        resultados.append({
        # Guardamos el resultado en la lista.
        # Usamos un diccionario para representar un resultado.
            "tienda": "Eneba",
            "titulo": titulo,
            "precio": precio,
            "moneda": moneda,
            "link": link
        })

    return resultados
# Finalmente devolvemos la lista de resultados.
# Esta función retorna todos los juegos encontrados.