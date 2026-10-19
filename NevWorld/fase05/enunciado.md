# El parte de caza también habla SQL

Ya has contado las cacerías con pandas y representado las presas en un gráfico. Ahora el creador de NevWorld quiere obtener **el mismo recuento consultando un archivo Parquet con SQL**. ¿Cambian los resultados al cambiar de herramienta?

Trabaja con la misma partida de las actividades anteriores y el tema 08. **Duración orientativa: 15–20 minutos.**

## Teoría de apoyo

| Pieza | Para qué sirve |
| --- | --- |
| pandas | Leer el CSV y trabajar con su DataFrame. |
| PyArrow | Biblioteca que pandas utiliza para escribir Parquet; no necesitas importarla directamente. |
| Parquet | Formato de archivo; no es una biblioteca ni una consulta. |
| DuckDB | Motor que ejecuta SQL desde tu script Python. |
| `COUNT(*)` | Contar las filas de cada grupo. |
| `GROUP BY` | Reunir filas que comparten un valor. |
| `AS` | Dar un nombre a una columna del resultado; no modifica el archivo original. |
| `ORDER BY ... DESC` | Ordenar de mayor a menor. |
| `.fetchdf()` | Recuperar el resultado SQL como DataFrame. |

## 1. Conserva la información en otro formato

Crea **un único archivo**: `scripts/actividades/05_caza_sql.py`, dentro de `bigdata-game`. Todos los pasos siguientes van en ese archivo, uno debajo de otro. No añadas código al script de la teoría.

1. Importa `Path`, pandas como `pd` y `duckdb`.
2. Lee `data/processed/hunts.csv`, creado en la actividad 02. Si falta, termina esa actividad primero.
3. Comprueba que existe `prey_type` y que ninguna cacería tiene esa columna sin informar. No borres registros para ocultar errores.
4. Crea `data/processed/parquet` si hace falta y guarda `hunts.parquet` utilizando `to_parquet(..., engine='pyarrow', index=False)`.
5. Muestra los tamaños del CSV y del Parquet en bytes mediante `ruta.stat().st_size`.

## 2. Pregunta por las presas con SQL

Debajo de la conversión, abre una conexión con `duckdb.connect()`. Guarda una consulta SQL en una variable Python llamada `hunt_query`, entre comillas triples.

La consulta debe:

- Leer `data/processed/parquet/hunts.parquet` mediante `read_parquet`.
- Agrupar por `prey_type`.
- Mostrar la presa y el número de cacerías completadas registradas de cada tipo.
- Llamar **`hunt_count`** a la columna calculada.
- Ordenar por ese recuento de mayor a menor.

Ejecuta la consulta con `connection.execute(hunt_query).fetchdf()` y muestra el resultado. No pegues el SQL directamente en la terminal: es texto que Python entrega a DuckDB.

## 3. Comprueba y guarda

1. Comprueba que la suma de `hunt_count` coincide con el número de filas del CSV.
2. Compara cada recuento con el que obtuviste en la actividad 03 y con las barras de la 04. Las presas empatadas pueden aparecer en distinto orden.
3. Guarda el resultado como `reports/hunts_by_prey_sql.csv`, sin índice. Crea la carpeta si hace falta y cierra la conexión al final.

Si `hunts.csv` tiene cabecera pero ninguna fila, muestra un aviso y guarda el resumen vacío con las columnas `prey_type` y `hunt_count`. No inventes presas. La suma de recuentos será cero.

Ejecuta **en la terminal, desde la raíz de `bigdata-game`**, con el entorno del tema 08 activo:

```powershell
python scripts/actividades/05_caza_sql.py
```

## 4. Explica el resultado

Responde brevemente:

1. ¿Qué representa una fila del resultado? ¿Cuenta cacerías o unidades de comida? El recuento de cacerias completadas de un tipo de presa
2. ¿Qué hace `AS hunt_count`? Si lo cambias por `AS total_cacerias`, ¿qué referencias posteriores debes actualizar? Da nombre a la columna. Si se cambia, hay que actualizar las referencias posteriores a hunt_count.
3. ¿Qué archivo ocupa menos en tu partida? ¿Demuestra eso que ese formato será siempre mejor? Ocupa menos el CSV pero no demuestra que sea mejor ya que el tamaño depende de los datos y el formato

## Entrega

Entrega el script, `reports/hunts_by_prey_sql.csv` y una ficha breve con los tamaños, la comparación con la actividad 03 y las tres respuestas. Identifica la partida utilizada. No modifiques el RAW ni `hunts.csv`.