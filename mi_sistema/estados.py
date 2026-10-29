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

"""
SU SISTEMA · Diagrama de transición de estados
Entidad: Producto
"""

# 1. Nombre de la entidad de su E-R
NOMBRE_ENTIDAD = "Producto"

# 2. Sus estados (de 4 a 7), coinciden con docs/datos.md
ESTADOS = {
    "registrado",
    "disponible",
    "agotado",
    "descontinuado",
    "baja",
}

# 3. Estado en el que nace la entidad
ESTADO_INICIAL = "registrado"

# 4. Estados donde termina su ciclo de vida
ESTADOS_FINALES = {"descontinuado", "baja"}

# 5. Las flechas de su DTE: ("estado_origen", "evento"): "estado_destino"
TRANSICIONES = {
    ("registrado", "ingresar_stock"): "disponible",
    ("registrado", "dar_de_baja"): "baja",
    ("disponible", "vender_todo"): "agotado",
    ("disponible", "descontinuar"): "descontinuado",
    ("agotado", "reabastecer"): "disponible",
    ("agotado", "descontinuar"): "descontinuado",
}

# 6. Acción que ejecuta el sistema en cada flecha
ACCIONES = {
    ("registrado", "ingresar_stock"): "activar producto",
    ("registrado", "dar_de_baja"): "remover registro",
    ("disponible", "vender_todo"): "marcar sin stock",
    ("disponible", "descontinuar"): "retirar de catálogo",
    ("agotado", "reabastecer"): "actualizar existencias",
    ("agotado", "descontinuar"): "retirar de catálogo",
}

# 7. Escenarios de prueba
CAMINO_FELIZ = ["ingresar_stock", "vender_todo", "descontinuar"]

CASOS_INVALIDOS = [
    ("registrado", "vender_todo"),      # Sin stock inicial no se puede vender
    ("descontinuado", "reabastecer"),   # Un producto descontinuado ya no se reabastece
    ("agotado", "vender_todo"),         # Agotado no tiene existencias para vender
]