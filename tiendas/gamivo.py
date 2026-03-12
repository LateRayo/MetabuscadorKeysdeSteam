import cloudscraper
from tiendas.tipo import inferir_tipo

def buscar(juego):
    url = "https://search.gamivo.com/_search/"

    # Agregamos Origin y Referer. Son vitales para evitar el error 403.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://www.gamivo.com",
        "Referer": "https://www.gamivo.com/",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Consulta para Elasticsearch
    data = {
        "query": {
            "match": {
                "name": juego
            }
        },
        "size": 10
    }

    # Usamos cloudscraper en lugar de requests normal
    scraper = cloudscraper.create_scraper()

    try:
        # Hacemos el POST usando el scraper
        r = scraper.post(url, headers=headers, json=data)
        r.raise_for_status() # Si da error 403, saltará al except
        datos = r.json()
    except Exception as e:
        print(f"[DEBUG GAMIVO] Error en la petición: {e} - Código: {r.status_code if 'r' in locals() else 'Desconocido'}")
        return []

    resultados = []

    lista_hits = datos.get("hits", {}).get("hits", [])

    for item in lista_hits:
        source = item.get("_source", {})

        titulo = source.get("name")
        precio = source.get("lowestPrice")
        slug = source.get("slug")

        # --- EL ARREGLO ---
        # Agregamos la condición de que el precio tiene que ser mayor a 0
        if not titulo or not precio or float(precio) <= 0 or not slug:
            continue
        # ------------------

        link = f"https://www.gamivo.com/product/{slug}"

        tipo = inferir_tipo(titulo, extra_texts=[slug])

        resultados.append({
            "tienda": "Gamivo",
            "titulo": titulo,
            "precio": float(precio),
            "moneda": "EUR",
            "link": link,
            "tipo": tipo
        })

    return resultados
