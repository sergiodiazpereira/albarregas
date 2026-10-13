# El informe de caza: de las tablas a las conclusiones

El creador de NevWorld ya tiene tu parte de caza, pero necesita un resumen: **qué presas aparecen más, cómo se reparten las cacerías registradas por día y cómo cambió la comida disponible**. Además, quiere comprobar esta afirmación: «Si aumentó la comida, fue gracias a la caza».

Tu misión es calcular métricas y explicar qué permiten afirmar. Utiliza los datos de tu propia partida y las operaciones del tema 06. No necesitas gráficas, unir tablas ni modificar el RAW o los CSV procesados.

## Teoría de apoyo

Python es el lenguaje; pandas es la biblioteca que permite trabajar con tablas. `pd.read_csv()` devuelve un DataFrame. Al seleccionar una columna, como `hunts['prey_type']`, obtienes una Series. Los siguientes métodos pertenecen a pandas:

| Para… | Operación que puedes reutilizar |
| --- | --- |
| Contar las apariciones de cada valor | `tabla['columna'].value_counts()` |
| Obtener porcentajes | `value_counts(normalize=True) * 100` |
| Redondear a un decimal | `.round(1)` |
| Seleccionar filas que cumplen una condición | `tabla[tabla['columna'] == valor]` |
| Agrupar y sumar una cantidad | `tabla.groupby('grupo')['cantidad'].sum()` |
| Ordenar una Series por sus etiquetas | `.sort_index()` |
| Obtener cantidades sin signo negativo | `.abs()` |
| Saber si una tabla no tiene filas | `.empty` |
| Exportar una tabla sin su índice interno | `.to_csv(ruta, index=False)` |

**Una operación nueva:** `.sort_index()` ordena por las etiquetas de la Series. Si las etiquetas son días, permite mostrarlos cronológicamente. `.sort_values()` ordenaría por los valores de la métrica. Por ejemplo, con día 2 → 5 cacerías y día 1 → 2 cacerías, ordenar por índice muestra primero el día 1.

`len()`, `print()`, `if`, `for`, las listas y los diccionarios pertenecen a Python. Una máscara de comparación selecciona filas; una agrupación organiza filas para calcular un resumen. No son la misma operación.

## 1. Prepara las preguntas y los datos

Crea `scripts/actividades/03_informe_caza.py` dentro de `bigdata-game`. Carga `data/processed/hunts.csv`, creado en la actividad 02, y `data/processed/resources.csv`, generado en la teoría. Ambos deben corresponder a la misma partida. Si falta `hunts.csv`, termina la actividad anterior; no lo sustituyas por datos inventados.

Antes de calcular, completa esta ficha:

| Pregunta | Tabla y columnas necesarias | Operación y motivo |
| --- | --- | --- |
| ¿Cuántas cacerías completadas se registraron? | 42| len(hunts): cuenta cada fila de hunts.csv (cacerías completadas)|
| ¿Cuántas corresponden a cada tipo de presa? | sheep    38
deer      4| hunts['prey_type'].value_counts(): cuenta las cacerías de cada tipo de presa y las ordena de mayor a menor frecuencia|
| ¿Qué porcentaje representa cada presa? | sheep    90.5
deer      9.5| hunts['prey_type'].value_counts(normalize=True) * 100, y .round(1) para redondear a un decimal. El porcentaje se calcula sobre el total de cacerías registradas|
| ¿Cuántas cacerías se registraron en cada día observado? | 0     5
1     6
2     6
3     2
4     4
5     2
12    1
16    1
18    2
19    2
21    1
25    1
29    1
30    1
31    1
32    3
37    2
38    1| hunts['simulation_day'].value_counts().sort_index(): cuenta las filas de cada día y ordena los resultados por día|
| ¿Cuánto aumentó, disminuyó y cambió en términos netos la comida? | Aumentos registrados: 1581.0
Disminuciones registradas: 1243.0
Balance neto: 338.0| Filtrar resources por resource_type == 'food'. Sumar los amount_delta positivos para los incrementos, sumar el valor absoluto de los negativos para las reducciones y sumar todos para el balance neto.|

Comprueba que existen las columnas necesarias, que no se repite `run_id` y `event_index` dentro de cada tabla y que los campos usados en los cálculos no tienen valores ausentes. Si detectas un problema, explica el error sin borrar filas para ocultarlo. No mezcles partidas.

## 2. Resume el parte de caza

Muestra en la consola:

1. El total de cacerías completadas registradas.
2. El recuento por `prey_type`, de mayor a menor frecuencia.
3. El porcentaje de cada tipo de presa, redondeado a un decimal.
4. El recuento por `simulation_day`, ordenado por día, no por frecuencia.

Explica qué representa una fila de `hunts.csv` y cuál es el denominador de los porcentajes.
- Representa una cacería completada junto a todos sus datos relevantes

Si la tabla está vacía, muestra un mensaje indicando que no hay cacerías completadas registradas. El total será cero; no intentes acceder al primer elemento de un recuento vacío ni inventes una presa predominante. Un día que no aparece en el recuento no es automáticamente un día observado con cero cacerías: este archivo no determina por sí solo todo el periodo de observación.

## 3. Examina los cambios de comida

Filtra las filas de `resources` cuyo `resource_type` sea `food`. Después calcula:

- **Incrementos registrados:** suma de los `amount_delta` positivos.
- **Reducciones registradas:** suma de las magnitudes de los `amount_delta` negativos; muéstrala como número positivo.
- **Balance neto:** suma de todos los `amount_delta` de comida.

Ejemplo inventado: +12, −5 y +3 producen incrementos de 15, reducciones de 5 y balance de +10. No es el resultado que debes entregar: usa tus datos.

Si no hay eventos de comida, las tres sumas serán cero, pero muestra también un aviso. Ese cero significa que no hay variaciones registradas que sumar; no demuestra que el mundo no tuviera comida.

## 4. Comprueba y guarda el informe

Comprueba con `assert` que:

- La suma de los recuentos por presa coincide con el total de cacerías.
- La suma de los recuentos por día también coincide con ese total.
- Los incrementos menos las reducciones coinciden con el balance de comida.

Si hay cacerías, revisa que los porcentajes sin redondear sumen aproximadamente 100. Los porcentajes redondeados pueden no sumar exactamente 100. Para comparar números decimales puedes usar `abs(a - b) < 0.000001`: aquí `abs()` es una función de Python que mide la magnitud de la diferencia.

Crea un DataFrame de resumen con dos columnas, `metric` y `value`, y estas cinco filas:

| metric | Qué guardar en value |
| --- | --- |
| `hunt_events` | Total de cacerías completadas registradas |
| `food_change_events` | Número de eventos de cambio de comida |
| `food_gains` | Incrementos de comida registrados |
| `food_reductions` | Reducciones de comida, como cantidad positiva |
| `food_net_change` | Balance neto de comida |

Guárdalo en `reports/hunting_summary.csv`, sin índice. Reutiliza `pd.DataFrame` con una lista de diccionarios como en la teoría. Los recuentos por presa y día y los porcentajes se incorporarán a la ficha, junto con la salida de las comprobaciones.

Ejecuta desde la raíz de `bigdata-game`, con el entorno que tenga pandas:

```powershell
python scripts/actividades/03_informe_caza.py
```

## 5. Defiende tus conclusiones

Responde utilizando tus resultados reales:

1. ¿Qué presa o presas tienen el mayor recuento? Si hay empate, indícalo; si no hay datos, explica por qué no puedes responder. La oveja tiene mayor recuento
2. ¿El porcentaje de una presa representa porcentaje de cacerías, de aldeanos o de tiempo? Justifica el denominador. Representa cuánto se ha cazado esa presa con respecto a otras presas
3. ¿El día con más cacerías fue necesariamente el día en que se dedicó más tiempo a cazar? No tiene porque, ya que solo tenemos datos de cacerías completadas, no conocemos el tiempo que se ha dedicado cada día a cacerías incompletas.
4. ¿El balance neto indica las existencias finales de comida? ¿Qué información faltaría? No, indica cuánto cambiaron los eventos de comida registrados
5. ¿Puedes demostrar que todos los incrementos de comida se deben a la caza? ¿Qué vínculo entre eventos necesitarías para justificarlo? No, los eventos indican aumentos de comida, pero no tienen vínculo necesariamente con los eventos de caza.

## Ampliación para l@s más rápid@s: contrastar con las fotografías

Carga `snapshots.csv` de la misma partida, ordénalo por `tick` y `event_index` y calcula la diferencia de `food_stock` entre la primera y la última fotografía disponibles. Muestra también sus ticks.

Antes de usar `.iloc`, comprueba si hay filas. Con una sola fotografía, explica por qué la diferencia de cero no demuestra estabilidad durante toda la partida.

Compara esa diferencia con tu balance de comida. ¿Tienen necesariamente el mismo intervalo de observación? Explica por qué una discrepancia no prueba por sí sola un error. No fuerces la igualdad con un `assert`.

## Entrega y valoración

Entrega el script, `hunting_summary.csv` y una ficha con las decisiones de diseño, los recuentos y porcentajes, las comprobaciones y las cinco respuestas. Identifica el archivo RAW de origen y la partida utilizada. Si realizas la ampliación, incluye sus resultados y explicación.

Se valorará la elección razonada de operaciones, los cálculos correctos, el tratamiento de tablas vacías y la prudencia al interpretar resultados. Las cifras pueden variar entre partidas.