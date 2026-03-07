import urllib.parse
from curl_cffi import requests

def buscar(juego):
    url = "https://www.humblebundle.com/store/api/search"

    params = {
        "sort": "bestselling",
        "filter": "all",
        "search": juego,
        "request": 1,
        "page": 0
    }

    # Formateamos el nombre del juego para que los espacios sean "%20" en el Referer
    juego_encoded = urllib.parse.quote(juego)

    # Quitamos el Origin para no levantar sospechas.
    # Tampoco pasamos User-Agent porque curl_cffi lo asigna automáticamente.
    headers = {
        "Accept": "application/json",
        "Referer": f"https://www.humblebundle.com/store/search?sort=bestselling&filter=all&search={juego_encoded}"
    }

    try:
        # MAGIA: impersonate="chrome120" hace que nuestra huella TLS sea la de un navegador real
        r = requests.get(url, params=params, headers=headers, impersonate="chrome120", timeout=10)
        r.raise_for_status()
        datos = r.json()
    except Exception as e:
        print(f"[DEBUG HUMBLE BUNDLE] Error en la petición: {e}")
        return []

    resultados = []
    lista_resultados = datos.get("results", [])

    for item in lista_resultados:
        titulo = item.get("human_name")
        slug = item.get("human_url")
        precio_data = item.get("current_price", {})

        if not precio_data:
            continue

        precio = precio_data.get("amount")
        moneda = precio_data.get("currency", "USD")

        if not titulo or precio is None or float(precio) <= 0 or not slug:
            continue

        link = f"https://www.humblebundle.com/store/{slug}"

        resultados.append({
            "tienda": "Humble Bundle",
            "titulo": titulo,
            "precio": float(precio),
            "moneda": moneda,
            "link": link
        })

    return resultados