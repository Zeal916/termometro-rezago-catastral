# Guía 4 – Lo que la Parte II deja para las Partes I y III

La Parte II (limpieza) ya está hecha sobre el **piloto del Área Metropolitana de Bucaramanga (AMB) 2015-2023**. Este documento explica qué cifras y archivos les sirven a las Partes I y III. Así las tres partes usan la misma base y no damos dos números distintos para la misma cosa.

**Regla general:** la Guía 4 trabaja sobre el AMB (165.517 compraventas), no sobre la base nacional de la Guía 2 (5,4 M). Si el informe cita cifras nacionales, debe decir que son de la Guía 2.

---

## Parte I – Características de calidad de los datos

La guía pide describir **totalidad, consistencia, claridad y formato** y concluir si concuerdan con el problema de negocio. La Parte II ya midió todo eso. Usen estas cifras, que son las mismas del informe de limpieza.

### Totalidad (¿están completos los campos?)
- La base tiene 24 columnas. **22 están completas al 100%**, incluidos los campos del modelo: valor, fecha, folio (matrícula) y municipio.
- Vacías:
  - `folios_derivados`: 100% vacía.
  - `fecha_apertura_texto`: 81% vacía.
  - Ninguna de las dos se usa; se eliminan, no se imputan.
- `tipo_predio_zona` = `SIN INFORMACION` en 2.175 filas (1,3%).
- El **número catastral no viene** en el registro (Guía 1). Por eso no se puede cruzar el avalúo de cada predio con las ventas.
- **Ojo:** que el valor esté "completo" no significa que sea válido. 770 compraventas tienen un valor que no es un precio: 164 en 0, 161 por debajo de COP 1 M y 445 de exactamente COP 1 M.

### Consistencia (¿el dato significa lo que dice el campo?)
- El campo `valor` debería ser el precio del inmueble, pero:
  - **30.821 compraventas** pertenecen a escrituras de varios predios: el valor es un global (mediana de COP 30,6 M frente a 97 M en las de un solo predio).
  - **161 casos** repiten el mismo folio y la misma fecha (en el 66,5% con el mismo valor) y 4 anotaciones traen más de un valor.
  - **52,3% de los pares limpios** crece entre 0% y 5% al año (mediana de 2,98%, igual al reajuste por decreto). El valor escrito muchas veces sigue al avalúo y no al precio. Es el hallazgo más fuerte para concluir sobre la concordancia con el problema de negocio.
- **Granularidad:** la unidad es la **anotación en un folio**, no el inmueble ni la escritura. Una escritura puede tener varios folios y un folio varias ventas.

### Claridad (¿los análisis estadísticos dan resultados entendibles?)
- El valor es muy asimétrico: la mediana es COP 98 M, pero el máximo es COP 143.246 M (asimetría de 161). Un promedio no se entiende.
- En **logaritmo** la asimetría es -0,7: casi simétrica. Por eso trabajamos con log y medianas.

### Formato (¿el formato sirve para la técnica?)
- La fecha viene en **dos formatos**: `AAAA-MM-DD hh:mm:ss` y `dd/mm/aa` (31.569 filas, 19%). Se unificó a tipo fecha y ninguna quedó inválida. Esto importa porque el índice es una serie de tiempo.
- El valor es numérico. El código DIVIPOLA y la matrícula se leen como texto, para no perder ceros ni guiones.

### Conclusión sugerida para la Parte I
Los datos están completos en los campos que necesitamos y tienen un formato corregible. El problema de calidad está en la **consistencia del valor**: no siempre es el precio de un inmueble (escrituras de varios predios, duplicados, valores simbólicos), y en más de la mitad de las reventas sigue al avalúo. Esto concuerda con el problema de negocio: justifica la limpieza (Parte II) y el clasificador de escrituras de la Guía 2 (OA2).

**Pendiente de la Parte I:** redactar con estas cifras y no decir que "se eliminaron filas con datos vacíos". En esta base no hay vacíos en los campos del modelo; lo que se elimina, se elimina por reglas.

---

## Parte III – Entendimiento de los datos

### Con qué archivos trabajar (se comparten en el .zip)
| Archivo | Qué tiene | Cómo usarlo |
|---|---|---|
| `compraventas_limpias.csv` | 133.720 compraventas ya depuradas, con dos marcas: `extremo_alto` (> COP 1.050 M) y `cola_baja_1_10M` | Estadísticas descriptivas por año, municipio y zona |
| `pares_amb.csv` | 14.469 pares de ventas del mismo inmueble con al menos un año entre ellas. Columnas clave: `valor_ant`, `valor`, `fecha_ant`, `fecha`, `razon` (valor / valor_ant), `cambio_fisico`, `cambio_extremo_5x`, `para_indice` | **Filtrar `para_indice == True` (13.978 pares)** para todo lo del índice; los otros 491 sirven para hablar de anomalías |
| `datos_api/actos_folios_pares.csv` | 76.065 actos (hipotecas, propiedad horizontal, construcción, etc.) de los inmuebles con pares | Para la técnica 6 (adición de información) |

### Cómo se conectan con las 9 técnicas de la guía
1. **Filtración** y 2. **Imputación:** ya están hechas en la Parte II. Remitan a ella y no las repitan. Lo que se decidió: se filtra por reglas y no se imputa el valor.
3. **Reducción de dimensiones:** casi no aplica. Las variables útiles son pocas: valor, fecha, municipio, zona y actos.
4. **Extracción de features:** la tasa de crecimiento anual del par, el tiempo entre ventas, si hubo hipoteca el mismo día de la venta y si el inmueble es de propiedad horizontal (desde los actos). Son las variables previas a la venta que propuso la Guía 2 para OA2.
5. **Estadísticas básicas:** distribución del valor (en log), compraventas por año (se nota la caída de 2020) y por municipio.
6. **Adición de información:** cruzar los pares con los actos y, si alcanza el tiempo, con el reajuste anual por decreto.
7. **Segmentación:** urbano frente a rural (12.399 frente a 1.398 pares), por municipio y por período (antes y después de 2019, cuando la Ley 1943 exigió declarar el precio real).
8. **Variables más importantes:** qué separa a las escrituras que crecen como el avalúo de las demás.
9. **Clasificación o agrupación:** agrupar los pares por tasa de crecimiento; deberían salir un grupo cercano a 3% y otro de mercado.

### El resultado que la Parte III tiene que explicar
**El 52,3% de los pares limpios crece entre 0% y 5% al año y la mediana es 2,98%.** En el AMB, más de la mitad del registro reproduce el reajuste del avalúo. Esa es la "conclusión acerca de la coherencia con la problemática de negocio" que pide el entregable: confirma que el registro sin clasificar mediría el rezago y no el mercado.

Ojo: no es comparable directamente con el 41% de la Guía 2, que se midió sobre todas las reventas nacionales.

### Pendientes de la Parte III
- Decidir si se usan los pares rurales: son 1.398 en el AMB, pocos para un índice rural, pero sirven como ejemplo.
- Justificar qué técnicas de las 9 se usan y cuáles no (la rúbrica pide la justificación, no solo la descripción).
- Incluir en los anexos las tablas y gráficas que salgan.

---

## Cómo reproducir los archivos (opcional)
Los scripts están en el .zip. Hacen falta Python, pandas y el archivo original `amb_compraventas_2015_2023.csv` (39 MB, lo tiene Cristian). Se corren desde la carpeta `guia_4`, con el original en `datos/`, una carpeta al lado de `guia_4`:

```
py -I limpieza_amb.py      # compraventas_limpias.csv y pares_amb.csv
py -I descarga_actos.py    # actos desde la API de datos.gov.co (~3 min)
py -I limpieza_amb.py      # aplica la regla de cambio físico
```
