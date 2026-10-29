"""
RETO · Pedido de la cafetería de la FES

Un equipo del semestre pasado entregó este DTE y está mal. Tiene
4 errores. Su trabajo es encontrarlos y corregirlos con ayuda del
verificador y del simulador:

    python verificar.py reto/estados_con_errores.py
    python simulador.py reto/estados_con_errores.py

Reglas:
  - Corrijan el archivo; no lo reescriban desde cero.
  - Por cada error que corrijan, dejen un comentario  # CORREGIDO: ...
    explicando qué estaba mal en el diagrama, no en el código.
  - Un error de un nivel puede esconder otros del siguiente nivel.
    Sigan verificando hasta que pasen los 3.

Lo que el dueño de la cafetería les contó en la entrevista:
  «El cliente registra su pedido y lo paga. Ya pagado, cocina lo prepara.
   A veces, a media preparación, se acaba un insumo y el pedido se queda
   en espera hasta que llega; luego se sigue preparando. Cuando está listo,
   se le entrega al cliente. Un pedido se puede cancelar mientras no se haya
   pagado. Un pedido cancelado ya no se recupera: el cliente hace uno nuevo.»
"""

NOMBRE_ENTIDAD = "Pedido de cafetería"

ESTADOS = {
    "registrado",
    "pagado",
    "en_preparacion",
    # CORREGIDO: Se eliminó el estado 'en_espera' y su transición inalcanzable.
    "listo",
    "entregado",
    "cancelado",
}

ESTADO_INICIAL = "registrado"

ESTADOS_FINALES = {"entregado", "cancelado"}

TRANSICIONES = {
    ("registrado", "pagar"): "pagado",
    ("registrado", "cancelar"): "cancelado",
    ("pagado", "preparar"): "en_preparacion",
    ("en_preparacion", "terminar"): "listo",
    # CORREGIDO: Se eliminó el estado 'en_espera' y su transición inalcanzable.
    # CORREGIDO: Se corrigió el nombre del estado 'entregdo' a 'entregado'.
    ("listo", "entregar"): "entregado",
    # CORREGIDO: Se eliminó la transición 'reactivar' porque 'cancelado' es un estado final y no debe tener salidas.
}

CAMINO_FELIZ = ["pagar", "preparar", "terminar", "entregar"]

CASOS_INVALIDOS = [
    ("pagado", "cancelar"),      # ya pagado no se cancela
    # CORREGIDO: Se eliminó ("registrado", "cancelar") de CASOS_INVALIDOS porque el dueño indicó que un pedido sí se puede cancelar antes de pagar.
    ("listo", "preparar"),       # un pedido listo no vuelve a cocina
]
