import requests
from tiendas.tipo import inferir_tipo

def buscar(juego):
    # Endpoint de Algolia para Green Man Gaming
    url = "https://sczizsp09z-dsn.algolia.net/1/indexes/*/queries"

    headers = {
        "x-algolia-application-id": "SCZIZSP09Z",
        "x-algolia-api-key": "3bc4cebab2aa8cddab9e9a3cfad5aef3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.greenmangaming.com",
        "Referer": "https://www.greenmangaming.com/"
    }

    # Le pasamos los mismos filtros que usa la página para traer solo juegos vendibles en Argentina
    filtros = "IsSellable:true AND AvailableRegions:AR AND NOT ExcludeCountryCodes:AR"
    
    data = {
        "requests": [
            {
                "indexName": "prod_ProductSearch_AR_AM", # Índice regional
                "params": f"query={juego}&filters={filtros}&hitsPerPage=10"
            }
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        datos = r.json()
    except Exception as e:
        print(f"[DEBUG GMG] Error en la petición: {e}")
        return []

    resultados = []

    try:
        # Algolia devuelve una lista de resultados, tomamos la primera query [0]
        lista_juegos = datos["results"][0]["hits"]
    except (KeyError, IndexError):
        return []

    for item in lista_juegos:
        titulo = item.get("DisplayName")
        url_parcial = item.get("Url")
        
        # Entramos al diccionario Regions -> AR para buscar el precio
        region_data = item.get("Regions", {}).get("AR", {})
        
        if not region_data:
            continue

        # "Drp" suele ser el precio final. "CurrencyCode" nos dice la moneda (suele ser USD)
        precio = region_data.get("Drp")
        moneda = region_data.get("CurrencyCode", "USD")

        # Verificaciones de seguridad y de stock
        if not titulo or precio is None or float(precio) <= 0 or not url_parcial:
            continue

        # GMG usa URLs relativas, así que le sumamos el dominio base
        link = f"https://www.greenmangaming.com{url_parcial}"

        tipo = inferir_tipo(titulo, extra_texts=[url_parcial])

        resultados.append({
            "tienda": "Green Man Gaming",
            "titulo": titulo,
            "precio": float(precio),
            "moneda": moneda,
            "link": link,
            "tipo": tipo
        })

    return resultados
