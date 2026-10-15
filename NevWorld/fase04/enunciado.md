# El parte de caza, de un vistazo

Ya has transformado los eventos de caza y calculado sus métricas. Ahora el creador de NevWorld quiere **ver qué tipos de presa aparecen más en las cacerías completadas**, sin tener que leer toda la tabla.

Convierte uno de los recuentos de la actividad 3 en un gráfico de barras. Trabaja con tu propia partida.

## Teoría de apoyo

Pandas prepara los datos; Matplotlib configura y guarda la figura. Para este gráfico puedes reutilizar:

| Para… | Utiliza… |
| --- | --- |
| Contar las cacerías por presa | `hunts['prey_type'].value_counts()` |
| Crear la figura | `plt.figure(figsize=(8, 4))` |
| Dibujar las barras de una Series | `counts.plot.bar(color='steelblue')` |
| Escribir el título y los nombres de los ejes | `plt.title()`, `plt.xlabel()`, `plt.ylabel()` |
| Inclinar y alinear las etiquetas | `plt.xticks(rotation=30, ha='right')` |
| Ajustar los márgenes | `plt.tight_layout()` |
| Guardar el PNG y cerrar la figura | `plt.savefig(ruta)` y `plt.close()` |

`value_counts()` ordena por frecuencia de mayor a menor. Cada etiqueta de la Series será una categoría del eje horizontal y su valor será la altura de una barra.

## 1. Decide qué vas a representar

Utiliza `data/processed/hunts.csv`, creado en la actividad 2. Si no existe, genera primero esa tabla. Antes de programar, responde:

- ¿Qué representa cada barra? El número de cacerías completadas registradas para un tipo de presa
- ¿Qué cantidad y unidad aparecerán en el eje vertical? El eje vertical muestra el número de cacerías, no la cantidad de comida.
- ¿Por qué usar barras y no una línea que conecte las presas? Se usan barras porque los tipos de presa son categorías; unirlas con una línea sugeriría una continuidad que no existe.

Elige un título que deje claro que se representan **cacerías completadas registradas**, no cantidades de comida obtenida.

## 2. Crea el gráfico

Crea `scripts/actividades/04_grafico_caza.py` dentro de `bigdata-game`. El script debe:

1. Importar `Path`, pandas como `pd` y `matplotlib.pyplot` como `plt`.
2. Leer `hunts.csv` y obtener el recuento por `prey_type`.
3. Si no hay filas, mostrar un aviso y omitir el gráfico. No inventes presas ni cantidades.
4. Si hay datos, crear un gráfico de barras con título, ejes identificados, etiquetas legibles y un color a tu elección.
5. Guardar la imagen como `reports/charts/05_hunts_by_prey.png`, creando la carpeta si hace falta, y cerrar la figura.

Reutiliza las validaciones de la actividad anterior: cada cacería debe tener una presa informada. Un valor ausente en una fila existente no equivale a una tabla vacía.

Ejecuta desde la raíz de `bigdata-game`, con el entorno que tenga pandas y Matplotlib:

```powershell
python scripts/actividades/04_grafico_caza.py
```

El script guarda una imagen; no necesita abrir una ventana. Abre el PNG desde el explorador de VS Code o de tu sistema. Si no hay datos y existía una imagen de una ejecución anterior, no la presentes como resultado de esta partida.

## 3. Comprueba e interpreta

Compara las alturas de las barras con los recuentos de tu actividad 03. La suma de las cantidades representadas debe coincidir con el total de cacerías de esa misma partida. Comprueba que no se corten los títulos o etiquetas.

Escribe tres frases:

1. **Observación:** indica qué presa o presas tienen más registros y cuántos, incluyendo los empates.
 La presa con más registros es sheep, con 38 cacerías completadas.
2. **Límite:** explica por qué el gráfico no muestra cuánto tiempo se dedicó a cazar ni cuánta comida produjo cada presa.
El gráfico cuenta cacerías completadas, pero no muestra cuánto tiempo se dedicó a cazar ni cuánta comida produjo cada presa.
3. **Pregunta pendiente:** plantea algo que no puedas responder con este gráfico e indica qué dato adicional necesitarías. ¿Qué presa produjo más comida por hora de caza? Para responder harían falta los datos de comida obtenida y tiempo dedicado a cada cacería.

Si no hay cacerías, entrega el aviso del script y explica por qué no hay gráfico ni se puede elegir una presa predominante.

## Entrega

Sube al portfolio en una nueva carpeta el script, el PNG y una ficha breve con las tres decisiones iniciales, la comparación con tus recuentos y las tres frases finales. No modifiques el RAW ni los CSV procesados.