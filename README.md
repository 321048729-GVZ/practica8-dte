# Práctica 8 · Del diagrama de transición de estados al código

**Ingeniería de Software · Grupo 1359 / 1359A · Ciclo 2027-1**
FES Cuautitlán · Campo 4 · Unidad 5, tema 5.7

**Sesión:** miércoles 28 de octubre, 18:00 a 19:30, laboratorio
**Modalidad:** en equipo
**Entrega:** enlace a su último commit, en Classroom, antes de las 19:30

---

## De qué se trata

Un diagrama de transición de estados (DTE) parece un dibujo, pero en el fondo es una tabla: cada flecha dice «si la entidad está en *este* estado y ocurre *este* evento, pasa a *este otro* estado». Si esa tabla está bien hecha, el sistema no puede llegar nunca a una situación imposible: devolver algo que no se prestó, cobrar un pedido cancelado o cerrar un reporte que nadie atendió.

Hoy van a escribir el DTE de una entidad de su proyecto como datos en Python, y tres programas lo van a poner a prueba:

| Archivo | Qué hace |
|---|---|
| `simulador.py` | Ustedes son el mundo exterior: escriben eventos y ven si el sistema los acepta. La misión es recorrer todas las flechas. |
| `verificar.py` | Revisa su DTE en tres niveles y les dice exactamente qué está mal y por qué. |
| `extra_sqlite.py` | Muestra su DTE protegiendo una base de datos real. Es la pieza que van a reutilizar en E6. |

No necesitan instalar nada: todo usa Python estándar.

---

## Paso 0 · Abran su copia (5 min)

1. Den clic en **Use this template → Create a new repository**. Créenlo en su cuenta con el nombre `practica8-equipo#`. Lo crea **una sola persona** por equipo y agrega a los demás como colaboradores (*Settings → Collaborators*).
2. Ábranlo en **Code → Codespaces → Create codespace on main**. Tarda un par de minutos la primera vez.

¿Prefieren trabajar en la computadora del laboratorio? Clonen el repositorio y abran una terminal dentro de la carpeta:

```bash
git clone https://github.com/SU-USUARIO/practica8-equipo#.git
cd practica8-equipo#
python --version   # necesitan 3.8 o más reciente
```

En Windows, si `python` no responde, prueben con `py`.

> Todos los comandos se corren desde la carpeta principal del repositorio, no desde dentro de `mi_sistema/` ni de `reto/`.

---

## Paso 1 · Jueguen con el ejemplo (10 min)

```bash
python simulador.py
```

Se abre el DTE del **préstamo de equipo de laboratorio**, el mismo sistema del ejemplo de los minispecs. Escriban eventos o el número de la opción.

**Misión:** llegar a `6 de 6 flechas`. Una sola vida no alcanza: van a tener que usar `reiniciar`. Mientras juegan, intenten también algo imposible, como `devolver` un préstamo recién solicitado, y lean qué responde el sistema.

Comandos útiles: `pendientes`, `historial`, `diagrama`, `ayuda`, `salir`.

Cuando terminen, abran `ejemplo/estados_prestamo.py` y vean cómo cada flecha que recorrieron es una línea de `TRANSICIONES`.

---

## Paso 2 · Reto: arreglen el DTE de la cafetería (15 min)

Un equipo del semestre pasado entregó el DTE del pedido de la cafetería y tiene **4 errores**. Lean la entrevista con el dueño que viene al inicio del archivo y después verifiquen:

```bash
python verificar.py reto/estados_con_errores.py
```

Corrijan `reto/estados_con_errores.py` hasta que pasen los tres niveles. Por cada corrección dejen un comentario `# CORREGIDO: ...` que explique qué estaba mal **en el diagrama**.

Ojo: arreglar un nivel puede destapar errores del siguiente. Y en uno de los errores no está mal la flecha, sino la prueba. Decidir cuál de los dos está mal es parte del reto: la respuesta está en lo que dijo el dueño.

---

## Paso 3 · Su sistema (50 min)

### 3a. Dibujen el DTE (10 min)

Elijan **una** entidad de su modelo E-R (E4) que pase por varias situaciones a lo largo del tiempo: un reporte, una solicitud, una cita, un pedido. Si su diccionario de datos ya tiene un campo `estado`, esa es la entidad.

En su Codespace creen el archivo `docs/dte.drawio`: se abre diagrams.net dentro del editor. En la computadora del laboratorio usen [app.diagrams.net](https://app.diagrams.net) y guarden el archivo en `docs/`.

| Elemento del DTE | Cómo se dibuja |
|---|---|
| Estado | Rectángulo redondeado. Nombre que describe cómo está la entidad: `pendiente`, `pagado`, `en_revision`. |
| Estado inicial | Flecha que sale de un punto negro. Solo hay uno. |
| Estado final | Doble círculo o borde grueso. De ahí no sale ninguna flecha. |
| Transición | Flecha con la etiqueta `evento / acción`. El evento es un verbo: `pagar`, `asignar`, `cancelar`. |

Busquen de 4 a 7 estados. Si les salen más, probablemente están mezclando dos entidades.

### 3b. Escríbanlo como datos (25 min)

Llenen `mi_sistema/estados.py` siguiendo el mismo orden que el ejemplo. Verifiquen después de cada bloque, no al final:

```bash
python verificar.py
```

| Nivel | Qué revisa |
|---|---|
| 1 · Estructura | Que todo esté declarado y con la forma correcta. |
| 2 · Diagrama | Que no haya estados inalcanzables, estados de los que nunca se sale, ni flechas que salgan de un estado final. También avisa si un estado parece verbo o un evento parece estado. |
| 3 · Escenarios | Que su camino feliz llegue a un estado final y que sus casos inválidos de verdad se rechacen. |

Los avisos amarillos no bloquean, pero léanlos: casi siempre señalan una confusión entre estado y evento.

### 3c. Pónganlo a prueba (15 min)

```bash
python simulador.py mi_sistema/estados.py
```

Lleguen a cobertura completa. Mientras lo recorren, piensen como su usuario real: ¿hay algo que pasa en la vida real y que su diagrama no permite? ¿Algo que su diagrama permite y que en la vida real no debería pasar? Si encuentran algo, corrijan **el dibujo y el código**: tienen que seguir siendo el mismo diagrama.

Cuando pasen los tres niveles, `verificar.py` genera `docs/dte_generado.md`. Después del push, ábranlo en GitHub: el diagrama aparece dibujado a partir de su código. Compárenlo con el que dibujaron en diagrams.net.

---

## Paso 4 · Entreguen (10 min)

1. Llenen `ENTREGA.md`.
2. Hagan commit y push:

   ```bash
   git add .
   git commit -m "Práctica 8: DTE y máquina de estados"
   git push
   ```

3. En la pestaña **Actions** de su repositorio, el verificador corre solo con cada push. Una palomita verde significa que `mi_sistema/estados.py` pasa los tres niveles. Si aparece el aviso de que los *workflows* están deshabilitados, den clic en *Enable*.
4. Peguen en Classroom el enlace a su commit y den clic en Entregar.

**Lo que reviso:**
- que el DTE dibujado y `docs/dte_generado.md` sean el mismo diagrama;
- que `mi_sistema/estados.py` pase los tres niveles;
- que el reto esté corregido y cada corrección tenga su comentario;
- que `ENTREGA.md` esté completo.

---

## Extra · Su DTE protegiendo una base de datos

Si terminan antes:

```bash
python extra_sqlite.py mi_sistema/estados.py
```

Lean `extra_sqlite.py`. Van a ver dos defensas: el `CHECK` de la tabla, que impide guardar un estado que no existe, y `cambiar_estado()`, que impide saltarse una flecha. Las dos salen del mismo DTE que acaban de escribir. Para E6, copien `maquina.py` y `mi_sistema/estados.py` a su proyecto: es la lógica de estados de su prototipo, ya probada.

---

## Errores comunes

- **Confundir estado con evento.** `revisando` o `en_revision` es un estado; `revisar` es un evento.
- **Escribir un estado de dos formas.** `en_proceso` en un lado y `en proceso` en otro son, para Python, dos estados distintos.
- **Olvidar las salidas raras.** Casi todo se puede cancelar, rechazar o vencer en algún momento. Pregúntense en cada estado: ¿qué más puede pasar aquí?
- **Ponerle salidas a un estado final.** Si algo «se reabre», o el estado no era final o lo que se crea es una entidad nueva.

Si usan IA, declárenlo en `ENTREGA.md`. Ustedes responden por cada línea en la defensa individual.
