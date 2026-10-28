"""
EXTRA · El DTE protegiendo una base de datos SQLite

Esto es lo que van a necesitar en el prototipo de E6: que la base de datos
nunca guarde un estado imposible. Hay dos defensas y este script muestra las dos:

  1. En la tabla, un CHECK que solo admite los estados del DTE.
  2. En el programa, cambiar_estado(), que solo acepta eventos con flecha.

Uso:
    python extra_sqlite.py                          # con el ejemplo
    python extra_sqlite.py mi_sistema/estados.py    # con su sistema

Crea el archivo demo.db (no lo suban al repositorio; ya está en .gitignore).
"""

import sqlite3
import sys

import maquina as m


def crear_tablas(con, dte):
    valores = ", ".join("'" + e.replace("'", "''") + "'" for e in sorted(m.leer(dte, "ESTADOS")))
    con.executescript(f"""
        DROP TABLE IF EXISTS historial;
        DROP TABLE IF EXISTS entidad;
        CREATE TABLE entidad (
            folio  INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL CHECK (estado IN ({valores}))
        );
        CREATE TABLE historial (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            folio   INTEGER NOT NULL REFERENCES entidad(folio),
            origen  TEXT NOT NULL,
            evento  TEXT NOT NULL,
            destino TEXT NOT NULL,
            momento TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );
    """)


def crear_entidad(con, dte):
    cur = con.execute("INSERT INTO entidad (estado) VALUES (?)", (m.leer(dte, "ESTADO_INICIAL"),))
    con.commit()
    return cur.lastrowid


def cambiar_estado(con, dte, folio, evento):
    """Aplica un evento a una entidad guardada. Si no hay flecha, no toca la base."""
    fila = con.execute("SELECT estado FROM entidad WHERE folio = ?", (folio,)).fetchone()
    if fila is None:
        raise LookupError(f"No existe el folio {folio}")
    actual = fila[0]
    nuevo = m.aplicar(dte, actual, evento)  # lanza TransicionInvalida si no hay flecha
    con.execute("UPDATE entidad SET estado = ? WHERE folio = ?", (nuevo, folio))
    con.execute("INSERT INTO historial (folio, origen, evento, destino) VALUES (?, ?, ?, ?)",
                (folio, actual, evento, nuevo))
    con.commit()
    return nuevo


def main():
    m.preparar_consola()
    ruta = sys.argv[1] if len(sys.argv) > 1 else "ejemplo/estados_prestamo.py"
    dte = m.cargar(ruta)
    entidad = m.leer(dte, "NOMBRE_ENTIDAD", "Entidad")

    con = sqlite3.connect("demo.db")
    crear_tablas(con, dte)
    folio = crear_entidad(con, dte)
    print(m.negritas(f"{entidad} · folio {folio} creado en estado «{m.leer(dte, 'ESTADO_INICIAL')}»\n"))

    print(m.negritas("1. Camino feliz a través de cambiar_estado()"))
    for evento in m.leer(dte, "CAMINO_FELIZ", []):
        print(m.verde(f"  ✔ {evento:<16} → {cambiar_estado(con, dte, folio, evento)}"))

    print(m.negritas("\n2. Un evento sin flecha: lo detiene el programa"))
    casos = m.leer(dte, "CASOS_INVALIDOS", [])
    if casos:
        otro = crear_entidad(con, dte)
        estado_caso, evento_caso = casos[0]
        con.execute("UPDATE entidad SET estado = ? WHERE folio = ?", (estado_caso, otro))
        try:
            cambiar_estado(con, dte, otro, evento_caso)
        except m.TransicionInvalida as error:
            print(m.rojo(f"  ✘ {error}"))

    print(m.negritas("\n3. Alguien se salta el programa y escribe directo en la base"))
    try:
        con.execute("UPDATE entidad SET estado = 'estado_inventado' WHERE folio = ?", (folio,))
    except sqlite3.IntegrityError as error:
        print(m.rojo(f"  ✘ SQLite lo rechaza: {error}"))
        con.rollback()

    print(m.negritas("\n4. Historial guardado"))
    for origen, evento, destino, momento in con.execute(
            "SELECT origen, evento, destino, momento FROM historial WHERE folio = ? ORDER BY id", (folio,)):
        print(f"  {momento}  {origen} --{evento}--> {destino}")

    con.close()


if __name__ == "__main__":
    main()
