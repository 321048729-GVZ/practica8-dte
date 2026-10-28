"""
Simulador interactivo de un diagrama de transición de estados.

Uso:
    python simulador.py                              # abre el ejemplo del préstamo
    python simulador.py mi_sistema/estados.py        # abre su sistema
    python simulador.py reto/estados_con_errores.py  # abre el reto

Ustedes son el mundo exterior: escriben eventos y el simulador decide si
la entidad cambia de estado o si el evento se rechaza. La meta es recorrer
TODAS las flechas del diagrama (cobertura completa).
"""

import sys

import maquina as m

RUTA_POR_DEFECTO = "ejemplo/estados_prestamo.py"

AYUDA = """
Comandos:
  <evento> o <número>   intenta ese evento desde el estado actual
  historial             muestra los eventos que han ocurrido en esta vida
  pendientes            muestra las flechas que todavía no recorren
  diagrama              imprime el DTE en Mermaid (péguenlo en mermaid.live)
  reiniciar             empieza una vida nueva desde el estado inicial
  ayuda                 muestra esta ayuda
  salir                 termina el simulador
"""


def barra(hechas, total, ancho=20):
    llenas = int(ancho * hechas / total) if total else 0
    return "█" * llenas + "░" * (ancho - llenas)


def mostrar_estado(dte, estado, recorridas, total):
    finales = set(m.leer(dte, "ESTADOS_FINALES", set()))
    print()
    print(m.negritas("Estado actual: ") + m.azul(f"[{estado}]"))
    cobertura = f"{len(recorridas)} de {total} flechas"
    print(m.tenue(f"Cobertura: {barra(len(recorridas), total)} {cobertura}"))

    if estado in finales:
        print(m.verde("● Estado final. El ciclo de vida de esta entidad terminó."))
        if len(recorridas) < total:
            print("  Escriban «reiniciar» para recorrer las flechas que faltan.")
        return []

    opciones = m.eventos_desde(dte, estado)
    if not opciones:
        print(m.rojo("✘ Este estado no es final y no tiene ninguna flecha de salida."))
        print("  La entidad se quedó atrapada aquí para siempre. Eso es un error del DTE.")
        return []

    print("Eventos posibles desde aquí:")
    for i, (evento, destino) in enumerate(opciones, start=1):
        marca = m.verde("✔") if (estado, evento) in recorridas else " "
        texto_accion = m.accion(dte, estado, evento)
        detalle = m.tenue(f"  / {texto_accion}") if texto_accion else ""
        print(f"  {marca} {i}) {evento:<18} → {destino}{detalle}")
    return opciones


def main():
    m.preparar_consola()
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    try:
        dte = m.cargar(ruta)
    except Exception as error:  # el archivo puede tener errores de sintaxis
        print(m.rojo(f"No pude abrir {ruta}: {error}"))
        print("Revisen que el archivo exista y que Python lo pueda leer sin errores.")
        sys.exit(1)

    inicial = m.leer(dte, "ESTADO_INICIAL")
    transiciones = m.leer(dte, "TRANSICIONES", {})
    if not inicial or not transiciones:
        print(m.rojo("Este archivo todavía no tiene ESTADO_INICIAL o TRANSICIONES."))
        print("Llénenlos y vuelvan a intentar. Primero corran verificar.py para ver qué falta.")
        sys.exit(1)

    entidad = m.leer(dte, "NOMBRE_ENTIDAD", "Entidad")
    total = len(transiciones)
    recorridas = set()
    estado = inicial
    historial = []
    vida = 1

    print(m.negritas(f"\n=== Simulador de estados · {entidad} ==="))
    print("Ustedes son el mundo exterior: escriban un evento y vean si el sistema lo acepta.")
    print("Misión: recorrer todas las flechas del diagrama. Escriban «ayuda» para ver los comandos.")

    opciones = mostrar_estado(dte, estado, recorridas, total)

    while True:
        try:
            entrada = input(m.negritas("\n> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not entrada:
            continue
        comando = entrada.lower()

        if comando == "salir":
            break
        if comando == "ayuda":
            print(AYUDA)
            continue
        if comando == "historial":
            if historial:
                print(f"Vida {vida}: {inicial} → " + " → ".join(f"{ev} → {dest}" for ev, dest in historial))
            else:
                print("Todavía no ocurre ningún evento en esta vida.")
            continue
        if comando == "pendientes":
            faltan = [k for k in transiciones if k not in recorridas]
            if not faltan:
                print(m.verde("No falta ninguna: ya recorrieron todo el diagrama."))
            for orig, ev in faltan:
                print(f"  {orig} --{ev}--> {transiciones[(orig, ev)]}")
            continue
        if comando == "diagrama":
            print(m.mermaid(dte))
            continue
        if comando == "reiniciar":
            vida += 1
            estado, historial = inicial, []
            print(m.tenue(f"--- Vida {vida}: una entidad nueva empieza en [{inicial}] ---"))
            opciones = mostrar_estado(dte, estado, recorridas, total)
            continue

        evento = entrada
        if entrada.isdigit() and 1 <= int(entrada) <= len(opciones):
            evento = opciones[int(entrada) - 1][0]

        try:
            nuevo = m.aplicar(dte, estado, evento)
        except m.TransicionInvalida as error:
            print(m.rojo(f"✘ Rechazado. {error}"))
            print(m.tenue("  El estado no cambió. Esto es justo lo que el sistema debe hacer con un evento imposible."))
            continue

        texto_accion = m.accion(dte, estado, evento)
        recorridas.add((estado, evento))
        historial.append((evento, nuevo))
        mensaje = f"✔ {estado} --{evento}--> {nuevo}"
        if texto_accion:
            mensaje += f"   (el sistema: {texto_accion})"
        print(m.verde(mensaje))
        estado = nuevo

        if len(recorridas) == total:
            print(m.verde(m.negritas("★ Cobertura completa: recorrieron todas las flechas del DTE.")))

        opciones = mostrar_estado(dte, estado, recorridas, total)

    print(f"\nRecorrieron {len(recorridas)} de {total} flechas en {vida} vida(s). Hasta luego.")


if __name__ == "__main__":
    main()
