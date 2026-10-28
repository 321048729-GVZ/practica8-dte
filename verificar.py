"""
Verificador del DTE por niveles.

Uso:
    python verificar.py                              # revisa mi_sistema/estados.py
    python verificar.py ejemplo/estados_prestamo.py
    python verificar.py reto/estados_con_errores.py

Nivel 1 · Estructura   ¿Está todo declarado y con el tipo correcto?
Nivel 2 · Diagrama     ¿El DTE tiene sentido como ciclo de vida?
Nivel 3 · Escenarios   ¿Los casos de prueba se comportan como dicen?

Un nivel solo se revisa si el anterior pasó. Si los tres pasan, se genera
docs/dte_generado.md con el diagrama, que GitHub dibuja automáticamente.
"""

import os
import sys

import maquina as m

RUTA_POR_DEFECTO = "mi_sistema/estados.py"


class Reporte:
    def __init__(self):
        self.errores = 0
        self.avisos = 0

    def ok(self, texto):
        print(m.verde("  ✔ ") + texto)

    def error(self, texto, pista=""):
        self.errores += 1
        print(m.rojo("  ✘ ") + texto)
        if pista:
            print(m.tenue("      Pista: " + pista))

    def aviso(self, texto, pista=""):
        self.avisos += 1
        print(m.amarillo("  ! ") + texto)
        if pista:
            print(m.tenue("      " + pista))


def titulo(texto):
    print("\n" + m.negritas(texto))


# ----------------------------------------------------------------------
# Nivel 1 · Estructura
# ----------------------------------------------------------------------

def nivel_1(dte, r):
    titulo("Nivel 1 · Estructura")

    entidad = m.leer(dte, "NOMBRE_ENTIDAD")
    if isinstance(entidad, str) and entidad.strip():
        r.ok(f"Entidad: {entidad}")
    else:
        r.error("NOMBRE_ENTIDAD está vacío.", "Escriban el nombre de la entidad de su E-R cuyo ciclo de vida van a modelar.")

    estados = m.leer(dte, "ESTADOS")
    if not estados:  # incluye {} vacío, que Python lee como diccionario
        r.error("ESTADOS está vacío.", "Escriban sus estados entre llaves: {\"pendiente\", \"en_revision\", ...}.")
        estados = set()
    elif not isinstance(estados, (set, list, tuple)) or not all(isinstance(e, str) and e for e in estados):
        r.error("ESTADOS debe ser un conjunto de textos, por ejemplo {\"abierto\", \"cerrado\"}.")
        estados = set()
    else:
        estados = set(estados)
        if len(estados) < 3:
            r.error(f"ESTADOS tiene {len(estados)} estado(s).", "Un ciclo de vida útil tiene al menos 3; para esta práctica busquen de 4 a 7.")
        else:
            r.ok(f"{len(estados)} estados declarados")
            if len(estados) > 7:
                r.aviso("Tienen más de 7 estados.", "¿Seguro que todos son estados de la misma entidad? Quizá alguno pertenece a otra.")

    inicial = m.leer(dte, "ESTADO_INICIAL")
    if not inicial:
        r.error("ESTADO_INICIAL está vacío.", "Es el estado en el que nace la entidad, la flecha que sale del punto negro.")
    elif inicial not in estados:
        r.error(f"ESTADO_INICIAL «{inicial}» no está en ESTADOS.", "Revisen que esté escrito igual en los dos lugares.")
    else:
        r.ok(f"Estado inicial: {inicial}")

    finales = m.leer(dte, "ESTADOS_FINALES")
    if not isinstance(finales, (set, list, tuple)) or not finales:
        r.error("ESTADOS_FINALES está vacío.", "¿En qué estado termina la vida de la entidad? Puede haber más de uno.")
    else:
        fuera = set(finales) - estados
        if fuera:
            r.error(f"Estos finales no están en ESTADOS: {', '.join(sorted(fuera))}")
        elif inicial in finales:
            r.error("El estado inicial también está marcado como final.", "Entonces la entidad nace muerta. Separen dónde empieza y dónde termina.")
        else:
            r.ok(f"Estados finales: {', '.join(sorted(finales))}")

    transiciones = m.leer(dte, "TRANSICIONES")
    if not isinstance(transiciones, dict) or not transiciones:
        r.error("TRANSICIONES está vacío.", "Cada flecha del DTE es una línea: (\"origen\", \"evento\"): \"destino\".")
    else:
        mal_formadas = [
            k for k, v in transiciones.items()
            if not (isinstance(k, tuple) and len(k) == 2 and all(isinstance(x, str) for x in k) and isinstance(v, str))
        ]
        if mal_formadas:
            r.error(f"{len(mal_formadas)} transición(es) no tienen la forma (\"origen\", \"evento\"): \"destino\".", f"Revisen: {mal_formadas[0]!r}")
        else:
            r.ok(f"{len(transiciones)} transiciones (flechas) declaradas")


# ----------------------------------------------------------------------
# Nivel 2 · Diagrama
# ----------------------------------------------------------------------

def nivel_2(dte, r):
    titulo("Nivel 2 · Diagrama")
    estados = set(m.leer(dte, "ESTADOS"))
    inicial = m.leer(dte, "ESTADO_INICIAL")
    finales = set(m.leer(dte, "ESTADOS_FINALES"))
    transiciones = m.leer(dte, "TRANSICIONES")

    # Todo estado usado en una flecha está declarado
    no_declarados = set()
    for (orig, ev), dest in transiciones.items():
        for e in (orig, dest):
            if e not in estados:
                no_declarados.add(e)
    if no_declarados:
        for e in sorted(no_declarados):
            r.error(f"La flecha usa el estado «{e}», que no está en ESTADOS.",
                    "¿Es un error de dedo o un estado que olvidaron declarar? Debe escribirse igual en todos lados.")
        print(m.tenue("  · Corrijan primero los nombres: las demás revisiones del diagrama dependen de que estén bien."))
        return
    r.ok("Todas las flechas usan estados declarados")

    # De un estado final no sale nada
    salen_de_final = [(o, ev) for (o, ev) in transiciones if o in finales]
    if salen_de_final:
        for o, ev in salen_de_final:
            r.error(f"Del estado final «{o}» sale la flecha «{ev}».",
                    "Un estado final no tiene salidas. O quiten la flecha, o ese estado no es final.")
    else:
        r.ok("Ningún estado final tiene flechas de salida")

    # Todo estado es alcanzable desde el inicial
    alcanzables = m.alcanzables(dte, inicial)
    huerfanos = estados - alcanzables
    if huerfanos:
        for e in sorted(huerfanos):
            r.error(f"El estado «{e}» es inalcanzable: ninguna secuencia de eventos llega a él desde «{inicial}».",
                    "Falta una flecha que entre a ese estado, o ese estado sobra.")
    else:
        r.ok(f"Todos los estados son alcanzables desde «{inicial}»")

    # Desde todo estado no final se puede terminar (no hay trampas)
    atrapados = [e for e in estados - finales - huerfanos if not (m.alcanzables(dte, e) & finales)]
    if atrapados:
        for e in sorted(atrapados):
            r.error(f"Desde «{e}» no hay ningún camino a un estado final.",
                    "La entidad entra ahí y nunca termina. ¿Qué evento real la saca de ese estado?")
    else:
        r.ok("Desde cualquier estado se puede llegar a un final")

    # Avisos de nombres: estados que parecen verbos y eventos que parecen estados
    for e in sorted(estados):
        if e.lower().endswith(("ar", "er", "ir")):
            r.aviso(f"El estado «{e}» parece un verbo.",
                    "Los estados dicen cómo está la entidad (pendiente, pagado); los verbos van en los eventos.")
    eventos = sorted({ev for (_, ev) in transiciones})
    for ev in eventos:
        if ev.lower().endswith(("ado", "ido", "ada", "ida")):
            r.aviso(f"El evento «{ev}» parece un estado.",
                    "Los eventos son lo que ocurre (pagar, cancelar); el resultado es el estado destino.")


# ----------------------------------------------------------------------
# Nivel 3 · Escenarios
# ----------------------------------------------------------------------

def nivel_3(dte, r):
    titulo("Nivel 3 · Escenarios")
    inicial = m.leer(dte, "ESTADO_INICIAL")
    finales = set(m.leer(dte, "ESTADOS_FINALES"))
    transiciones = m.leer(dte, "TRANSICIONES")

    camino = m.leer(dte, "CAMINO_FELIZ") or []
    if not camino:
        r.error("CAMINO_FELIZ está vacío.", "Escriban la secuencia de eventos del caso normal, del estado inicial a un final.")
    else:
        estado = inicial
        recorrido = [estado]
        fallo = False
        for ev in camino:
            try:
                estado = m.aplicar(dte, estado, ev)
                recorrido.append(estado)
            except m.TransicionInvalida as error:
                r.error(f"El camino feliz se rompe en el evento «{ev}». {error}")
                fallo = True
                break
        if not fallo:
            if estado in finales:
                r.ok("Camino feliz: " + " → ".join(recorrido))
            else:
                r.error(f"El camino feliz termina en «{estado}», que no es final.",
                        "Agreguen los eventos que faltan para cerrar el ciclo de vida.")

    casos = m.leer(dte, "CASOS_INVALIDOS") or []
    if len(casos) < 2:
        r.error(f"CASOS_INVALIDOS tiene {len(casos)} caso(s); se piden al menos 2.",
                "Piensen qué intentaría hacer un usuario distraído o tramposo con su sistema.")
    for caso in casos:
        if not (isinstance(caso, tuple) and len(caso) == 2):
            r.error(f"El caso {caso!r} no tiene la forma (\"estado\", \"evento\").")
            continue
        estado, ev = caso
        try:
            destino = m.aplicar(dte, estado, ev)
        except m.TransicionInvalida:
            r.ok(f"Se rechaza «{ev}» en «{estado}»")
        else:
            r.error(f"Dicen que «{ev}» en «{estado}» debe fallar, pero su DTE lo permite y lleva a «{destino}».",
                    "Una de las dos cosas está mal: la flecha sobra o el caso no es inválido. Decidan cuál.")

    # Cobertura del camino feliz
    if camino:
        usadas = set()
        estado = inicial
        for ev in camino:
            if (estado, ev) not in transiciones:
                break
            usadas.add((estado, ev))
            estado = transiciones[(estado, ev)]
        sin_usar = len(transiciones) - len(usadas)
        if sin_usar:
            print(m.tenue(f"  · El camino feliz recorre {len(usadas)} de {len(transiciones)} flechas. "
                          f"Faltan {sin_usar}: recórranlas en el simulador."))


# ----------------------------------------------------------------------

def main():
    m.preparar_consola()
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    print(m.negritas(f"Verificando {ruta}"))

    try:
        dte = m.cargar(ruta)
    except SyntaxError as error:
        print(m.rojo(f"  ✘ Python no puede leer el archivo: error de sintaxis en la línea {error.lineno}."))
        print(m.tenue("      Revisen comas, comillas y llaves cerca de esa línea."))
        sys.exit(1)
    except Exception as error:
        print(m.rojo(f"  ✘ No pude abrir el archivo: {error}"))
        sys.exit(1)

    r = Reporte()
    niveles = [nivel_1, nivel_2, nivel_3]
    aprobados = 0
    for numero, nivel in enumerate(niveles, start=1):
        antes = r.errores
        nivel(dte, r)
        if r.errores > antes:
            print(m.rojo(f"\nNivel {numero} con {r.errores - antes} error(es). Corríjanlos y vuelvan a verificar."))
            break
        aprobados = numero

    print()
    if aprobados == len(niveles):
        salida = os.path.join("docs", "dte_generado.md")
        if os.path.abspath(ruta).startswith(os.path.abspath("mi_sistema")):
            m.escribir_diagrama(dte, salida)
            print(m.tenue(f"Diagrama actualizado en {salida}. Ábranlo en GitHub para verlo dibujado."))
        mensaje = "★ Los 3 niveles pasaron."
        if r.avisos:
            mensaje += f" Hay {r.avisos} aviso(s): no bloquean, pero revísenlos."
        print(m.verde(m.negritas(mensaje)))
        sys.exit(0)
    else:
        print(f"Niveles aprobados: {aprobados} de {len(niveles)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
