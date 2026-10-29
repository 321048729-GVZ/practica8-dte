# DTE generado desde el código · Producto

Este archivo lo genera `verificar.py`. No lo editen a mano: si algo está mal, corrijan el archivo de estados y vuelvan a verificar.

Compárenlo con el DTE que dibujaron en diagrams.net. Deben ser el mismo diagrama.

```mermaid
stateDiagram-v2
    state "agotado" as agotado
    state "baja" as baja
    state "descontinuado" as descontinuado
    state "disponible" as disponible
    state "registrado" as registrado
    [*] --> registrado
    registrado --> disponible : ingresar_stock / activar producto
    registrado --> baja : dar_de_baja / remover registro
    disponible --> agotado : vender_todo / marcar sin stock
    disponible --> descontinuado : descontinuar / retirar de catálogo
    agotado --> disponible : reabastecer / actualizar existencias
    agotado --> descontinuado : descontinuar / retirar de catálogo
    baja --> [*]
    descontinuado --> [*]
```
