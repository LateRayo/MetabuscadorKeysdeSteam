# 🎮 MetaBuscador de Ofertas de Videojuegos

Un potente buscador de consola (CLI) desarrollado en Python que rastrea, compara y ordena en tiempo real los precios de videojuegos en las 8 tiendas de keys más populares del mercado. 

Diseñado con técnicas avanzadas de web scraping y evasión de firewalls (Cloudflare) mediante la falsificación de huellas TLS.

## 🚀 Características Principales

- **Búsqueda Simultánea:** Rastrea ofertas en *Eneba, Fanatical, Gamivo, Humble Bundle, Instant Gaming, Green Man Gaming, CDKeyOffer y Kinguin*.
- **Evasión Antibot:** Utiliza `curl_cffi` para simular un navegador Chrome 120 legítimo y saltar protecciones de Cloudflare.
- **Filtro Inteligente:** Algoritmo propio que descarta resultados "basura" exigiendo un 90% de coincidencia letra por letra con tu búsqueda.
- **Exclusión Personalizada:** Permite ocultar resultados indeseados (ej: cuentas compartidas o keys de consolas) usando la bandera `--exclude`.

## 🛠️ Comandos y Banderas Disponibles

Podés afinar tus búsquedas utilizando las siguientes banderas (flags):

### Banderas soportadas:
* **`-m`** o **`--max <número>`**: Limita la cantidad de resultados que se muestran en la tabla. Ideal para ver solo el "Top 3" o "Top 5" de las mejores ofertas.
* **`-e`** o **`--exclude <palabra1> <palabra2> ...`**: Elimina de la lista final cualquier resultado que contenga las palabras especificadas (no distingue entre mayúsculas y minúsculas). Excelente para filtrar DLCs, versiones de consola o cuentas compartidas.

### Ejemplos de uso:

**Búsqueda básica:**
```bash
python3 main.py "elden ring"

python3 main.py "elden ring" -m 5
# o también: python3 main.py "elden ring" --max 5

python3 main.py "elden ring" -m 10 -e xbox ps4 ps5 account
```

## 📦 Instalación y Uso (Versión Ejecutable)

Si usás Linux, podés descargar el programa compilado desde la pestaña de **[Releases]** y usarlo directamente sin instalar Python:

```bash
# Dale permisos de ejecución
chmod +x metabuscador-linux

# Ejecutalo
./metabuscador-linux "elden ring"
