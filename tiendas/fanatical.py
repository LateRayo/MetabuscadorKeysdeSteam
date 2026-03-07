import requests

def buscar(juego):
    # La URL base de la API de Algolia para esta tienda
    url = "https://w2m9492ddv-dsn.algolia.net/1/indexes/fan/query"

    # Los headers requieren el ID de la app y esa API Key gigante que capturaste
    headers = {
        "x-algolia-application-id": "W2M9492DDV",
        "x-algolia-api-key": "YmZhMmJiZWNmYzRjNTcwOTYxMjViNWY0Y2QyNjA2MDgyMjczN2U0ZmFmNTFmYjQ0ODRhYTI2ZGQ5ZTE0ZDAxZWZpbHRlcnM9ZGlzYWJsZWQlMjAlM0QlMjAwJTIwQU5EJTIwYXZhaWxhYmxlX3ZhbGlkX2Zyb20lMjAlM0MlM0QlMjAxNzcyODM5NDQyJTIwQU5EKGF2YWlsYWJsZV92YWxpZF91bnRpbCUyMCUzRCUyMDAlMjBPUiUyMGF2YWlsYWJsZV92YWxpZF91bnRpbCUyMCUzRSUyMDE3NzI4Mzk0NDIpJmZhY2V0RmlsdGVycz0lNUIlMjJpbmNsdWRlZF9yZWdpb25zJTNBQVIlMjIlNUQmcmVzdHJpY3RJbmRpY2VzPWZhbiUyQ2Zhbl9hbHRfcmFuayUyQ2Zhbl9uYW1lJTJDZmFuX2xhdGVzdF9kZWFscyUyQ2Zhbl9kaXNjb3VudCUyQ2Zhbl9yZWxlYXNlX2RhdGVfYXNjJTJDZmFuX3JlbGVhc2VfZGF0ZV9kZXNjJTJDZmFuX3ByaWNlX2FzYyUyQ2Zhbl9wcmljZV9kZXNjJTJDZmFuX2VuZGluZ19zb29uJTJDZmFuX21vc3Rfd2FudGVkJTJDZmFuX21hbnVhbF9wcmljZV9yYW5rJTJDZmFuX2Jlc3RfcHJpY2VfcmFuayUyQ2Zhbl91bmxpbWl0ZWQlMkNmYW5fbWV0YWNyaXRpYyUyQ2Zhbl90b3BfcmF0ZWQlMkNmYW5fcHJpY2VfYXNjX3VubGltaXRlZCUyQ2Zhbl9sYXRlc3RfZGVhbHNfdW5saW1pdGVkJnZhbGlkVW50aWw9MTc3Mjg0MDY0Mg=="
    }

    # Algolia espera los parámetros de búsqueda dentro de un JSON con la key "params"
    data = {
        "params": f"query={juego}&hitsPerPage=10"
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status() # Verifica que no haya error 400/500
        datos = r.json()
    except Exception:
        # Si la API cambia o se cae, devolvemos lista vacía para no romper el main
        return []

    resultados = []

    # Iteramos sobre la lista "hits" que trae los juegos
    for item in datos.get("hits", []):
        titulo = item.get("name")
        slug = item.get("slug")
        precios = item.get("price")

        # Filtro de seguridad por si algún juego viene roto o sin precio
        if not precios or not titulo or not slug:
            continue

        # Elegimos la moneda (priorizando USD como venimos haciendo)
        if "USD" in precios:
            moneda = "USD"
        elif "EUR" in precios:
            moneda = "EUR"
        else:
            moneda = list(precios.keys())[0]

        precio = precios[moneda]

        # Armamos el link (Fanatical usa la estructura /game/ o /dlc/ seguido del slug)
        # Usamos /game/ de forma genérica porque suele redirigir bien
        link = f"https://www.fanatical.com/es/game/{slug}"

        resultados.append({
            "tienda": "Fanatical",
            "titulo": titulo,
            "precio": precio,
            "moneda": moneda,
            "link": link
        })

    return resultados