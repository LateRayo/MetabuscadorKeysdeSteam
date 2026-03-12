import base64          # Se usa para traducir texto cifrado en formato Base64 a texto normal.
import re              # "Regular Expressions" (Expresiones Regulares). Permite buscar patrones de texto complejos.
import urllib.parse    # Se usa para convertir caracteres normales a formato seguro para URLs (ej: un espacio se vuelve "%20").
from curl_cffi import requests #Eengaña a los servidores simulando ser un navegador web real.
from tiendas.tipo import inferir_tipo

# =====================================================================
# FUNCIÓN 1: EL ROBO DE LA LLAVE (Bypassing)
# =====================================================================
def obtener_llave_fresca():
    """
    Kinguin usa llaves de API (Tokens) que vencen a las pocas horas. 
    Esta función entra a la página principal de Kinguin como si fuera un humano, 
    lee el código fuente y "roba" la llave válida del día.
    """
    url = "https://www.kinguin.net/"
    
    # Fingimos que aceptamos el mismo tipo de contenido que pediría un navegador normal
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }
    
    try:
        # MAGIA ANTI-BOT: Le decimos a curl_cffi que encripte la conexión exactamente 
        # igual que lo haría Google Chrome versión 120 (impersonate="chrome120").
        # Esto engaña al firewall de Cloudflare para que no nos tire Error 403.
        r = requests.get(url, headers=headers, impersonate="chrome120", timeout=15)
        html = r.text # obtengo la respuesta de la request
        
        # LA LUPA MEJORADA (Regex): 
        # Le pedimos a Python que busque en TODO el código de la página web cualquier 
        # palabra extrañamente larga (de 100 caracteres o más) que solo tenga letras, números y el signo "=".
        # Esto se debe a que las llaves en formato Base64(un cifrado sencillo) se ven exactamente así.
        candidatos = re.findall(r'[A-Za-z0-9=]{100,}', html)
        
        # Revisamos cada texto largo que encontró para ver cuál es la llave real
        for cand in candidatos:
            try:
                # Intentamos decodificar el texto de Base64 a texto legible
                decodificado = base64.b64decode(cand).decode('utf-8')
                
                # Las llaves de Algolia de Kinguin siempre tienen adentro la frase "validUntil=" (válido hasta).
                # Si encontramos esa frase, ¡bingo! Esa es nuestra llave.
                if "validUntil=" in decodificado:
                    return cand # Devolvemos la llave cifrada lista para usarse
            except Exception:
                # Si el texto largo no era código Base64 válido, Python dará un error.
                # Con 'continue' le decimos que ignore el error y pruebe con el siguiente texto largo.
                continue
                
        # SISTEMA DE DEPURACIÓN (Debug):
        # Si revisó todos los textos y no encontró la llave, guarda el código de la página web 
        # en un archivo de texto en tu computadora. Así podés abrirlo y buscar a mano qué cambió Kinguin.
        with open("kinguin_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    except Exception as e:
        print(f"[DEBUG KINGUIN] Error de red al conseguir llave: {e}")
    
    return None # Retorna vacío si todo falló

# =====================================================================
# FUNCIÓN 2: LA BÚSQUEDA DEL JUEGO
# =====================================================================
def buscar(juego):
    """
    Usa la llave robada en la primera función para conectarse directamente 
    a la base de datos de Algolia (el buscador de Kinguin) y extraer los precios.
    """
    
    # Paso 1: Llamamos a nuestra función ladrona para conseguir el acceso
    api_key_dinamica = obtener_llave_fresca()
    
    # Si la función falló y no trajo la llave, cortamos acá para que el programa no colapse.
    if not api_key_dinamica:
        print("[DEBUG KINGUIN] No se encontró la API Key. Se guardó 'kinguin_debug.html' para investigar.")
        return []

    # Paso 2: Configuramos la conexión a la base de datos de Algolia
    url = "https://cl3qvy8wc3-dsn.algolia.net/1/indexes/*/queries"

    # Parámetros que Algolia requiere en la URL (ID de la tienda y la llave que acabamos de robar)
    params_url = {
        "x-algolia-application-id": "CL3QVY8WC3",
        "x-algolia-api-key": api_key_dinamica
    }

    # Encabezados obligatorios para que Algolia sepa que le enviaremos un archivo JSON y fingir que venimos de Kinguin
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.kinguin.net",
        "Referer": "https://www.kinguin.net/"
    }

    # El nombre exacto de la "tabla" (Index) de la base de datos donde Kinguin guarda los juegos más vendidos
    indice_kinguin = "production_products_bestsellers_desc" 
    
    # Armamos la "pregunta" (Query) para la base de datos.
    # urllib.parse.quote convierte "elden ring" en "elden%20ring" para no romper el formato de la URL.
    data = {
        "requests": [
            {
                "indexName": indice_kinguin,
                "params": f"query={urllib.parse.quote(juego)}&hitsPerPage=10"
            }
        ]
    }

    try:
        # Enviamos la petición POST disfrazados de Chrome
        r = requests.post(url, params=params_url, headers=headers, json=data, impersonate="chrome120", timeout=10)
        datos = r.json() # Transformamos la respuesta en un diccionario de Python
        
        # Si Algolia devuelve un error (ej: la llave venció o el formato está mal), avisamos en consola
        if r.status_code != 200:
            print(f"[DEBUG KINGUIN] Error de Algolia: {r.text}")
            return []
            
    except Exception as e:
        print(f"[DEBUG KINGUIN] Error en la petición final: {e}")
        return []

    resultados = []

    # Intentamos acceder a la lista de juegos dentro del enjambre de datos que devolvió Algolia
    try:
        lista_juegos = datos["results"][0]["hits"]
    except (KeyError, IndexError):
        return []

    # =====================================================================
    # PASO 3: LIMPIEZA Y FORMATEO DE LOS RESULTADOS
    # =====================================================================
    for item in lista_juegos:
        # Extraemos solo los datos que nos importan
        titulo = item.get("name")
        precio = item.get("price")
        external_id = item.get("externalId")
        url_key = item.get("urlKey")

        # Filtro de seguridad: si falta algún dato crucial o el juego es gratis/error (precio <= 0), lo saltamos.
        if not titulo or precio is None or float(precio) <= 0 or not url_key:
            continue

        # Kinguin genera los links de compra uniendo el ID numérico y el nombre con guiones (urlKey)
        link = f"https://www.kinguin.net/category/{external_id}/{url_key}"

        # Guardamos el resultado en el formato estandarizado que espera nuestro main.py
        tipo = inferir_tipo(titulo, extra_texts=[url_key])

        resultados.append({
            "tienda": "Kinguin",
            "titulo": titulo,
            "precio": float(precio),
            "moneda": "EUR", 
            "link": link,
            "tipo": tipo
        })

    return resultados # Devolvemos la lista final lista para unirse a las demás tiendas
