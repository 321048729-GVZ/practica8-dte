"""
EJEMPLO RESUELTO · Préstamo de equipo de laboratorio

Es el mismo sistema que usamos en el ejemplo de los minispecs (Práctica 7).
Aquí está su diagrama de transición de estados escrito como datos.
Léanlo completo antes de escribir el suyo: cada bloque tiene su
equivalente en mi_sistema/estados.py.

Pruébenlo con:
    python simulador.py ejemplo/estados_prestamo.py
    python verificar.py ejemplo/estados_prestamo.py
"""

# 1. La entidad cuyo ciclo de vida modelamos.
#    Debe ser una entidad de su modelo E-R (E4).
NOMBRE_ENTIDAD = "Préstamo de equipo"

# 2. Los estados. Son sustantivos o participios: describen CÓMO ESTÁ
#    la entidad, no qué se le hace. Deben ser exactamente los valores
#    que admite el campo `estado` en su diccionario de datos.
ESTADOS = {
    "solicitado",
    "aprobado",
    "rechazado",
    "entregado",
    "vencido",
    "devuelto",
}

# 3. Dónde empieza la vida de la entidad (la flecha que sale del punto negro).
ESTADO_INICIAL = "solicitado"

# 4. Dónde termina (los estados con doble círculo). Desde aquí no sale ninguna flecha.
ESTADOS_FINALES = {"rechazado", "devuelto"}

# 5. LAS FLECHAS. Cada flecha del DTE es exactamente una línea:
#        (estado_origen, evento): estado_destino
#    Los eventos son verbos: lo que pasa en el mundo y provoca el cambio.
TRANSICIONES = {
    ("solicitado", "aprobar"): "aprobado",
    ("solicitado", "rechazar"): "rechazado",
    ("aprobado", "entregar"): "entregado",
    ("entregado", "devolver"): "devuelto",
    ("entregado", "vence_plazo"): "vencido",
    ("vencido", "devolver"): "devuelto",
}

# 6. Opcional: la acción que el sistema ejecuta al recorrer la flecha.
#    Es la parte derecha de la etiqueta «evento / acción» del DTE.
ACCIONES = {
    ("solicitado", "aprobar"): "reservar equipo",
    ("solicitado", "rechazar"): "notificar al alumno",
    ("aprobado", "entregar"): "registrar fecha-límite",
    ("entregado", "devolver"): "emitir comprobante-devolución",
    ("entregado", "vence_plazo"): "avisar al alumno",
    ("vencido", "devolver"): "registrar adeudo y emitir comprobante",
}

# 7. Escenarios de prueba.
#    CAMINO_FELIZ: una secuencia de eventos que lleva del estado inicial
#    a un estado final. Es el caso normal que el usuario les describió.
CAMINO_FELIZ = ["aprobar", "entregar", "devolver"]

#    CASOS_INVALIDOS: cosas que en la vida real alguien va a intentar
#    y que el sistema DEBE rechazar. Cada uno es (estado, evento).
CASOS_INVALIDOS = [
    ("solicitado", "devolver"),   # no se puede devolver algo que nunca se entregó
    ("aprobado", "vence_plazo"),  # el plazo corre desde la entrega, no desde la aprobación
    ("devuelto", "entregar"),     # un préstamo cerrado no se reabre: se hace uno nuevo
]
