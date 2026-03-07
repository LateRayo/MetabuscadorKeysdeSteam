import argparse
from rich.console import Console
from rich.table import Table

# Tus tiendas
from tiendas import eneba, cdkeyoffer, fanatical, gamivo, humblebundle, instantgaming, greenmangaming, kinguin

def main():
    console = Console()

    # --- CONFIGURACIÓN DE ARGPARSE ---
    parser = argparse.ArgumentParser(description="Metabuscador de ofertas de videojuegos en múltiples tiendas.")
    
    # Argumento principal: El nombre del juego (puede tener varias palabras)
    parser.add_argument("juego", nargs="+", help="El nombre del juego que querés buscar (ej: elden ring)")
    
    # Flag opcional: --max o -m para limitar los resultados
    parser.add_argument("-m", "--max", type=int, default=None, help="Cantidad máxima de resultados a mostrar en la tabla")

    # nargs="+" permite pasarle varias palabras separadas por espacio
    parser.add_argument("-e", "--exclude", nargs="+", default=[], help="Palabras a excluir de los resultados (ej: xbox ps5 account)")
    
    # Leemos los comandos que ingresó el usuario
    args = parser.parse_args()
    
    # Unimos las palabras del juego
    juego = " ".join(args.juego)
    max_resultados = args.max
    palabras_excluidas = [p.lower() for p in args.exclude]
    # ---------------------------------

    console.print(f"\n[bold cyan]🔍 Buscando los mejores precios para:[/bold cyan] [bold white]'{juego}'[/bold white]...\n")

    resultados = []

    # animacion mientras se ejecuta el bloque de codigo
    with console.status("[bold green]Buscando en las bases de datos...[/bold green]", spinner="dots"):
        try: resultados += eneba.buscar(juego)
        except Exception: pass
        
        try: resultados += cdkeyoffer.buscar(juego)
        except Exception: pass
        
        try: resultados += fanatical.buscar(juego)
        except Exception: pass
        
        try: resultados += gamivo.buscar(juego)
        except Exception: pass
        
        try: resultados += humblebundle.buscar(juego)
        except Exception: pass
        
        try: resultados += instantgaming.buscar(juego)
        except Exception: pass
        
        try: resultados += greenmangaming.buscar(juego)
        except Exception: pass

        try: resultados += kinguin.buscar(juego)
        except Exception: pass

    # Filtramos con tu función personalizada
    resultados = filtrar_por_letras(resultados, juego)

    if palabras_excluidas:
        resultados_limpios = []
        for r in resultados:
            titulo_minuscula = r['titulo'].lower()
            
            # Usamos la función any() de Python.
            # Significa: "Si ALGUNA de las palabras excluidas está en el título, NO lo guardes"
            if not any(excluida in titulo_minuscula for excluida in palabras_excluidas):
                resultados_limpios.append(r)
                
        resultados = resultados_limpios

    if not resultados:
        console.print("[bold yellow]No se encontraron resultados que coincidan con tu búsqueda.[/bold yellow]\n")
        return

    # Ordenamos TODOS los resultados por precio
    resultados.sort(key=lambda x: x["precio"])

    # --- APLICAMOS EL FLAG --max ---
    if max_resultados is not None:
        # Recortamos la lista para quedarnos solo con los primeros X elementos
        resultados = resultados[:max_resultados]
    # -------------------------------

    # Dibujamos la tabla
    table = Table(title="🏆 Mejores Ofertas Encontradas", show_header=True, header_style="bold magenta")
    table.add_column("Tienda", style="dim", width=15)
    table.add_column("Precio", justify="right", style="green", width=12)
    table.add_column("Juego", style="cyan")
    table.add_column("Link de Compra", style="blue")

    for r in resultados:
        precio_formateado = f"{r['precio']:.2f} {r['moneda']}"
        table.add_row(
            r['tienda'],
            precio_formateado,
            r['titulo'],
            r['link']
        )

    console.print(table)
    console.print(f"\n[dim]✨ Búsqueda finalizada. Mostrando {len(resultados)} resultados.[/dim]\n")


def filtrar_por_letras(resultados, busqueda, porcentaje_minimo=90):
    # (El código de tu función se mantiene exactamente igual que antes)
    resultados_filtrados = []
    busqueda_limpia = busqueda.lower().replace(" ", "")
    
    if not busqueda_limpia:
        return resultados

    for r in resultados:
        titulo_juego = r['titulo'].lower()
        letras_coincidentes = 0
        
        for letra in busqueda_limpia:
            if letra in titulo_juego:
                letras_coincidentes += 1
                
        if len(busqueda_limpia) > 0:
            porcentaje = (letras_coincidentes / len(busqueda_limpia)) * 100
        else:
            porcentaje = 0
        
        if porcentaje >= porcentaje_minimo:
            resultados_filtrados.append(r)
            
    return resultados_filtrados

if __name__ == "__main__":
    main()