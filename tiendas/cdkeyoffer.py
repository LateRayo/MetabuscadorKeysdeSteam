import requests
from tiendas.tipo import inferir_tipo

def buscar(juego):
    # La URL exacta de la API que descubriste
    url = "https://de.cdkeyoffer.com/index/product"
    
    params = {
        "search": juego,
        "page": 1
    }

    # Le pasamos un User-Agent estándar por las dudas, siempre es buena práctica
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    r = requests.get(url, params=params, headers=headers)
    resultados = []

    try:
        datos = r.json()
    except Exception:
        # Si la página falla y no devuelve JSON, devolvemos la lista vacía para no romper el main
        return resultados

    # Verificamos que la respuesta sea exitosa (el "code" es "0000" según tu JSON)
    if datos.get("code") == "0000" and "msg" in datos:
        for item in datos["msg"]:
            titulo = item.get("product_name")
            
            
            # Extraemos el precio (ej: "EUR 38.26")
            precio_crudo = item.get("net_price", "")
            if not precio_crudo:
                continue
            
            # Separamos "EUR" y "38.26" usando split()
            partes = precio_crudo.split() 
            if len(partes) == 2:
                moneda = partes[0]
                try:
                    precio = float(partes[1])
                except ValueError:
                    continue
            else:
                continue
            
            # Armamos el link completo
            detail_url = item.get("detail_url")
            link_final = f"https://www.cdkeyoffer.com/{detail_url}"
            tipo = inferir_tipo(titulo, extra_texts=[detail_url])

            resultados.append({
                "tienda": "CDKeyOffer",
                "titulo": titulo,
                "precio": precio,
                "moneda": moneda,
                "link": link_final,
                "tipo": tipo
            })

    return resultados
