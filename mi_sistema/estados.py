"""
SU SISTEMA · Diagrama de transición de estados

Llenen este archivo con el ciclo de vida de UNA entidad de su proyecto.
Sigan el mismo orden que el ejemplo (ejemplo/estados_prestamo.py).

Cómo elegir la entidad: abran su modelo E-R (E4) y busquen la entidad
que pasa por más situaciones a lo largo del tiempo: un reporte, una
solicitud, una cita, un pedido, una orden de trabajo. Si su diccionario
de datos tiene un campo `estado`, esa es la entidad.

Cuando terminen cada bloque, verifiquen:
    python verificar.py
y jueguen con su diagrama:
    python simulador.py mi_sistema/estados.py
"""

# 1. ¿Qué entidad de su E-R van a modelar?
NOMBRE_ENTIDAD = ""

# 2. Sus estados (de 4 a 7). Sustantivos o participios, en minúsculas,
#    con guion bajo en lugar de espacios. Deben coincidir con los valores
#    del campo `estado` en docs/datos.md.
ESTADOS = {
    # "pendiente",
    # "en_revision",
}

# 3. ¿En qué estado nace la entidad?
ESTADO_INICIAL = ""

# 4. ¿En qué estado o estados termina su ciclo de vida?
ESTADOS_FINALES = {
    # "cerrado",
}

# 5. Las flechas de su DTE, una por línea:
#        ("estado_origen", "evento"): "estado_destino",
TRANSICIONES = {
    # ("pendiente", "asignar"): "en_revision",
}

# 6. Opcional: la acción que ejecuta el sistema en cada flecha
#    (la parte derecha de «evento / acción» en su DTE).
ACCIONES = {
    # ("pendiente", "asignar"): "notificar al técnico",
}

# 7. Escenarios de prueba.
#    El caso normal que les describió su usuario, como lista de eventos:
CAMINO_FELIZ = [
    # "asignar", "resolver", "cerrar",
]

#    Al menos 2 cosas que alguien va a intentar y que su sistema debe rechazar.
#    Escriban junto a cada una, en un comentario, por qué es inválida.
CASOS_INVALIDOS = [
    # ("pendiente", "cerrar"),  # no se cierra un reporte que nadie atendió
]
