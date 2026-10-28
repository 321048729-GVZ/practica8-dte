"""
Motor de la máquina de estados.

Este archivo NO se modifica. Lo usan simulador.py, verificar.py y
extra_sqlite.py para leer el DTE que ustedes declaran en un archivo
de estados (por ejemplo, mi_sistema/estados.py).

La idea central de la práctica está aquí: un diagrama de transición
de estados es, en el fondo, una tabla. Cada flecha del diagrama es una
fila de la forma (estado_origen, evento) -> estado_destino. Si la tabla
está bien hecha, el programa no puede llegar a un estado imposible.
"""

import importlib.util
import os
import sys
import unicodedata
from collections import deque


# ----------------------------------------------------------------------
# Consola: colores y acentos que funcionen en Codespaces, Linux, macOS
# y en las terminales de Windows del laboratorio.
# ----------------------------------------------------------------------

def preparar_consola():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if os.name == "nt":
        os.system("")  # activa los colores ANSI en Windows 10 y posteriores


_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _c(codigo, texto):
    return f"\033[{codigo}m{texto}\033[0m" if _COLOR else texto


def verde(t):
    return _c("32", t)


def rojo(t):
    return _c("31", t)


def amarillo(t):
    return _c("33", t)


def azul(t):
    return _c("36", t)


def negritas(t):
    return _c("1", t)


def tenue(t):
    return _c("2", t)


# ----------------------------------------------------------------------
# Carga del archivo de estados
# ----------------------------------------------------------------------

def cargar(ruta):
    """Importa un archivo de estados a partir de su ruta."""
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No encuentro el archivo {ruta}")
    nombre = "dte_" + os.path.splitext(os.path.basename(ruta))[0]
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def leer(modulo, nombre, por_defecto=None):
    return getattr(modulo, nombre, por_defecto)


# ----------------------------------------------------------------------
# Reglas de la máquina
# ----------------------------------------------------------------------

class TransicionInvalida(ValueError):
    """Se lanza cuando un evento no tiene flecha desde el estado actual."""


def aplicar(modulo, estado, evento):
    """Devuelve el estado siguiente o lanza TransicionInvalida."""
    finales = set(leer(modulo, "ESTADOS_FINALES", set()))
    transiciones = leer(modulo, "TRANSICIONES", {})
    if estado in finales:
        raise TransicionInvalida(
            f"'{estado}' es un estado final: el ciclo de vida ya terminó y no admite eventos."
        )
    siguiente = transiciones.get((estado, evento))
    if siguiente is None:
        raise TransicionInvalida(
            f"El evento '{evento}' no está permitido en el estado '{estado}': "
            f"en el DTE no hay ninguna flecha '{evento}' que salga de '{estado}'."
        )
    return siguiente


def eventos_desde(modulo, estado):
    """Lista de (evento, destino) que salen de un estado."""
    transiciones = leer(modulo, "TRANSICIONES", {})
    return [(ev, dest) for (orig, ev), dest in transiciones.items() if orig == estado]


def accion(modulo, origen, evento):
    acciones = leer(modulo, "ACCIONES", {}) or {}
    return acciones.get((origen, evento), "")


def alcanzables(modulo, desde):
    """Estados a los que se puede llegar partiendo de 'desde'."""
    transiciones = leer(modulo, "TRANSICIONES", {})
    vistos = {desde}
    cola = deque([desde])
    while cola:
        actual = cola.popleft()
        for (orig, _), dest in transiciones.items():
            if orig == actual and dest not in vistos:
                vistos.add(dest)
                cola.append(dest)
    return vistos


# ----------------------------------------------------------------------
# Diagrama en Mermaid (GitHub lo dibuja solo al abrir el archivo .md)
# ----------------------------------------------------------------------

def _id(nombre):
    sin_acentos = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode()
    limpio = "".join(ch if ch.isalnum() else "_" for ch in sin_acentos)
    return limpio or "estado"


def mermaid(modulo):
    estados = list(leer(modulo, "ESTADOS", []))
    inicial = leer(modulo, "ESTADO_INICIAL")
    finales = set(leer(modulo, "ESTADOS_FINALES", set()))
    transiciones = leer(modulo, "TRANSICIONES", {})

    lineas = ["stateDiagram-v2"]
    for e in sorted(estados):
        lineas.append(f'    state "{e}" as {_id(e)}')
    if inicial:
        lineas.append(f"    [*] --> {_id(inicial)}")
    for (orig, ev), dest in transiciones.items():
        etiqueta = ev
        texto_accion = accion(modulo, orig, ev)
        if texto_accion:
            etiqueta = f"{ev} / {texto_accion}"
        etiqueta = etiqueta.replace(":", " ")
        lineas.append(f"    {_id(orig)} --> {_id(dest)} : {etiqueta}")
    for f in sorted(finales):
        lineas.append(f"    {_id(f)} --> [*]")
    return "\n".join(lineas)


def escribir_diagrama(modulo, ruta_salida):
    entidad = leer(modulo, "NOMBRE_ENTIDAD", "Entidad")
    contenido = (
        f"# DTE generado desde el código · {entidad}\n\n"
        "Este archivo lo genera `verificar.py`. No lo editen a mano: si algo está mal, "
        "corrijan el archivo de estados y vuelvan a verificar.\n\n"
        "Compárenlo con el DTE que dibujaron en diagrams.net. Deben ser el mismo diagrama.\n\n"
        "```mermaid\n" + mermaid(modulo) + "\n```\n"
    )
    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido)
