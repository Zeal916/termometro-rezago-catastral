---
title: "Parte II. Técnicas de limpieza de datos"
subtitle: "Termómetro de rezago catastral · Equipo 23 · Piloto: Área Metropolitana de Bucaramanga (AMB)"
lang: es
---

## Por qué hay que limpiar estos datos

El Registro de Transacciones Inmobiliarias del IGAC (7y2j-43cv) se genera para dar fe pública de la propiedad, no para medir precios. Cada fila es una anotación en un folio de matrícula: el valor que se registra es el de la escritura, aunque esa escritura cubra varios inmuebles, una cuota parcial o un predio que cambió entre una venta y la siguiente. Como el índice de ventas repetidas compara cada inmueble consigo mismo, cualquier diferencia que no sea de precio (un error de digitación, una construcción nueva o un englobe) se lee como valorización. Por eso la limpieza es una condición del requerimiento R1 (calidad y trazabilidad) y del objetivo OA1 de la Guía 2.

La limpieza se aplicó como piloto a las 165.517 compraventas del AMB 2015-2023 (Bucaramanga, Floridablanca, Girón y Piedecuesta), el mismo territorio de la Guía 1. Para depurar los cambios físicos se descargaron además los 76.065 actos registrados en los 13.129 folios que forman pares (Anexo T2). Las reglas no dependen del municipio, así que se aplican sin cambios a la base nacional.

## Qué se encontró en los datos

**Tabla 1. Causas de limpieza identificadas (puntos a-d de la guía)**

| Punto de la guía | Qué se encontró en el AMB | Registros | Decisión |
|---|---|---|---|
| a. Respuestas válidas solo dentro de un rango | Valor igual a 0 (164), entre COP 1 y 999.999 (161) o exactamente COP 1 M (445): no son precios de un inmueble urbano | 770 | Eliminar |
| a. Rango del par | Ventas del mismo folio con menos de un año de diferencia: el cambio de precio no es comparable con una tendencia anual | 5.203 pares | Excluir del índice |
| b. Respuestas inválidas o vacías | `folios_derivados` vacío en el 100% y `fecha_apertura_texto` en el 81% | 2 columnas | Eliminar la columna (no se usa en el modelo) |
| b. Formato no correspondiente | La fecha de radicación viene en dos formatos (`AAAA-MM-DD hh:mm:ss` y `dd/mm/aa`, 19% de las filas) | 31.569 | Unificar; ninguna fecha quedó inválida |
| b. Categoría vacía | Zona `SIN INFORMACION` | 1.855 | Recuperar de otra venta del mismo folio (52); el resto queda como categoría propia |
| c. Valores extremos | Compraventas por encima del percentil 99,5 (COP 1.050 M); el máximo es COP 143.246 M. El 35,7% de las ventas de más de COP 1.000 M son escrituras de varios predios | 663 | Marcar, no eliminar |
| c. Cola baja | Ventas entre COP 1 M y 10 M (cuotas, derechos parciales o errores) | 5.806 | Marcar, no eliminar |
| c. Cambio extremo en el par | El precio se multiplica o se divide por 5 o más entre las dos ventas, sin cambio físico registrado (294 suben, 41 bajan; en 141 la primera venta es menor a COP 10 M) | 335 pares | Excluir del índice y conservar para OA6 |
| d. Interrelaciones que no deberían existir | Una escritura con varios folios trae el precio global de todos: la mediana es COP 30,6 M, frente a COP 97 M en las de un solo predio | 30.821 | Eliminar |
| d. Duplicados | Mismo folio y fecha: si el valor es igual, es la misma venta anotada dos veces; si es distinto, no se sabe cuál es el correcto | 112 + 90 | Dejar una copia / eliminar ambas |
| d. Varios valores en una anotación | Marca `tiene_mas_de_un_valor` | 4 | Eliminar |
| d. Cambio físico entre las dos ventas | Construcción, corrección de área o linderos, división, englobe, loteo o constitución de propiedad horizontal registrada entre las dos ventas. En esos pares el precio se multiplica por 3,22 (mediana), frente a 1,10 en el resto | 156 pares | Excluir del índice |

Dos actos se revisaron y **no** se tratan como cambio físico: la reforma (331) y la adición (347) del reglamento de propiedad horizontal. Se registran en todas las unidades de un edificio cuando cambia el conjunto, no la unidad, y en los pares que los tienen la razón de precios (1,03 a 1,10) es igual a la del total.

## Soluciones seleccionadas

**Eliminación general: sí, pero por regla y no por vacío.** En la base no hay celdas vacías en los campos del modelo: el valor, la fecha, el folio y el municipio están completos en el 100% de las filas. El problema no son los vacíos, sino valores que existen pero no representan el precio de un inmueble. Cada eliminación responde a una regla de la Tabla 1, con su conteo, y no a la ausencia de un dato.

**Imputación por regresión: no se aplica al valor.** El valor registrado es la variable que el proyecto mide. Imputarlo con un modelo sería fabricar el precio de mercado que se quiere observar, y el índice terminaría reproduciendo el modelo de imputación. Tampoco hace falta: los registros que se eliminan son el 19% de las compraventas y no se concentran en un año (la proporción eliminada va de 14,9% en 2019 a 21,0% en 2015), de modo que la serie no pierde ningún periodo. La única imputación es determinística: la zona vacía se toma de otra venta del mismo folio, porque la zona de un predio no cambia entre ventas.

**Imputación aleatoria: no se aplica.** Introduce variación que no viene del mercado, y un índice de ventas repetidas necesita los dos precios observados del mismo inmueble.

**Los extremos se marcan y no se borran.** La guía pide justificar si deben existir. Un valor extremo puede ser un error, una venta de lujo o una operación atípica, y esa diferencia es justo lo que busca el detector de anomalías (OA6). Por eso las compraventas extremas siguen en la base con una marca (`extremo_alto`, `cola_baja_1_10M`, `cambio_extremo_5x`), se excluyen solo del cálculo del índice y se usan después para evaluar el detector. El valor es muy asimétrico (asimetría de 161), pero en logaritmo es casi simétrico (-0,7), por lo que el modelo trabaja en logaritmo y con medianas en lugar de recortar más datos.

## Resultados del proceso

**Tabla 2. Embudo de limpieza de compraventas, AMB 2015-2023**

| Paso | Quedan | Salen |
|---|---:|---:|
| Compraventas registradas (código 125) | 165.517 | |
| Fecha válida, con formato unificado | 165.517 | 0 |
| Valor mayor que COP 1 M | 164.747 | 770 |
| Un solo valor en la anotación | 164.743 | 4 |
| Duplicado exacto de folio, fecha y valor (queda uno) | 164.631 | 112 |
| Mismo folio y fecha con valores distintos | 164.541 | 90 |
| Escritura de un solo predio | **133.720** | 30.821 |

Quedan 133.720 compraventas limpias (80,8%): 118.070 urbanas, 13.847 rurales y 1.803 sin zona. Su mediana es COP 98 M y el 98% está entre COP 3,8 M y 760 M.

**Tabla 3. Formación de pares de ventas repetidas**

| Paso | Pares |
|---|---:|
| Ventas consecutivas del mismo folio | 19.672 |
| Con al menos 365 días entre las dos ventas | 14.469 |
| Sin cambio físico registrado entre las dos ventas | 14.313 |
| Sin cambios de precio de 5 veces o más: **pares para el índice** | **13.978** |

Los 13.978 pares son 12.399 urbanos, 1.398 rurales y 181 sin zona. Los 491 pares excluidos por cambio físico o por cambio extremo no se borran: quedan marcados en el archivo de pares para evaluar el detector de anomalías.

**Lo que la limpieza no resuelve.** En los pares limpios, el 52,3% del valor crece entre 0% y 5% al año y la mediana es 2,98%, casi igual al reajuste por decreto. Esas escrituras no tienen un error de dato, sino un valor declarado por el avalúo. Por eso no se eliminan con una regla de limpieza: las separa el clasificador de escrituras (OA2), como se planteó en la Guía 2.

## Anexo técnico T2. Soporte de la limpieza

**Archivos (carpeta `guia_4`):**

- `limpieza_amb.py`: aplica en orden todas las reglas de la Tabla 1 y genera `compraventas_limpias.csv` (133.720 filas, con las marcas de extremos) y `pares_amb.csv` (14.469 pares con las columnas `cambio_fisico`, `cambio_extremo_5x` y `para_indice`). La salida completa está en `resultados_limpieza.txt`.
- `descarga_actos.py`: consulta la API de datos.gov.co (7y2j-43cv) por lotes de 150 folios y descarga todos los actos de los folios que forman pares. Se descargaron 76.065 actos de 13.129 folios el 8 de noviembre de 2026; ningún folio quedó sin respuesta. Control: las 29.409 compraventas de esos folios coinciden con las del archivo local.

**Códigos de acto tratados como cambio físico:** 317 (constitución de reglamento de propiedad horizontal), 902, 903, 917 y 964 (corrección o determinación de área y linderos), 909 (constitución de urbanización), 910, 911 y 912 (declaración de construcción o de mejora), 913, 915 y 919 (englobe y desenglobe), 918 (división material), 920 y 924 (loteo y reloteo). Un acto cuenta si se radicó después de la primera venta y hasta el día de la segunda.

**Reproducción:** `py -I limpieza_amb.py`, luego `py -I descarga_actos.py` y de nuevo `py -I limpieza_amb.py`. La descarga necesita la lista de pares, y la limpieza usa los actos si ya están descargados.
