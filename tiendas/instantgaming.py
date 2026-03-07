import requests

def buscar(juego):
    url = "https://qknhp8tc3y-dsn.algolia.net/1/indexes/produits_es_spotlighted_desc/query"

    # Agregamos Origin y Referer para pasar la validación de seguridad de Algolia
    headers = {
        "x-algolia-application-id": "QKNHP8TC3Y",
        "x-algolia-api-key": "4813969db52fc22897f8b84bac1299ad",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.instant-gaming.com",
        "Referer": "https://www.instant-gaming.com/"
    }

    filtros_region = '(country_whitelist:"AR" OR country_whitelist:"worldwide" OR country_whitelist:"WW") AND (NOT country_blacklist:"AR")'
    
    data = {
        "params": f"query={juego}&hitsPerPage=10&filters={filtros_region}"
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        datos = r.json()
    except Exception as e:
        print(f"[DEBUG INSTANT GAMING] Error en la petición: {e}")
        return []

    resultados = []

    for item in datos.get("hits", []):
        titulo = item.get("name")
        precio_texto = item.get("price_eur")
        prod_id = item.get("prod_id")
        seo_name = item.get("seo_name")

        if not titulo or not precio_texto or not prod_id or not seo_name:
            continue

        try:
            precio = float(precio_texto)
        except ValueError:
            continue

        if precio <= 0:
            continue

        link = f"https://www.instant-gaming.com/es/{prod_id}-{seo_name}/"

        resultados.append({
            "tienda": "Instant Gaming",
            "titulo": titulo,
            "precio": precio,
            "moneda": "EUR",
            "link": link
        })

    return resultados