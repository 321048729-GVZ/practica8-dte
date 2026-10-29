# Entrega · Práctica 8

Llenen este archivo antes de hacer su último commit. Respondan con sus palabras, en 2 o 3 líneas por pregunta.

## Equipo

| | |
|---|---|
| Número y nombre del equipo | [Escribe aquí el número/nombre de tu equipo] |
| Sistema del proyecto | Sistema de Gestión de Inventario y Ventas |
| Integrantes presentes | González Vargas ALfredo Zenif |

## Preguntas

**1. ¿Qué entidad eligieron y por qué es la que tiene el ciclo de vida más interesante de su sistema?**

Elegimos **Producto**, ya que atraviesa un ciclo completo en el inventario: nace al registrase, pasa a estar disponible con stock, se agota por ventas, se reabastece cíclicamente y termina descontinuado o dado de baja por merma o error.

**2. Del reto de la cafetería, ¿qué error les costó más encontrar? Explíquenlo como error del diagrama, no del código.**

El error visual de conectar flechas saliendo de un estado final y la falta de distinción entre eventos (verbos) y estados (sustantivos/participios). En el diagrama es fácil pasar por alto que un estado final no debe tener transiciones de salida.

**3. Al jugar con su sistema en el simulador, ¿descubrieron algún evento o caso que no habían dibujado? ¿Qué cambiaron?**

Identificamos la necesidad de dar de baja un producto directamente desde el estado `registrado` por mermas o errores de captura antes de salir a la venta. Agregamos el estado final `baja` y la transición `dar_de_baja` tanto en el diagrama como en el código.

**4. ¿Los valores de sus estados coinciden con el campo `estado` de su diccionario de datos (E4)? Si no, ¿qué van a corregir allá?**

Sí, coinciden totalmente. Inicialmente `datos.md` solo contenía `disponible`, `agotado` y `descontinuado`, por lo que actualizamos la lista en `datos.md` agregando el estado `baja` para asegurar congruencia directa.

## Uso de IA

| Herramienta | Para qué la usaron | Qué verificaron |
|---|---|---|
| GEMINI | Apoyo en la depuración del reto de la cafetería, estructuración del XML para Draw.io y definición del DTE en Python. | Que `verificar.py` aprobara los 3 niveles, cobertura completa en el simulador y coincidencia exacta de minúsculas entre XML, Python y `datos.md`. |


