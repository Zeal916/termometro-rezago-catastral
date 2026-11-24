# Bitácora de la Parte II (para ti, no se entrega)

Aquí está todo lo que se hizo, en orden, con el porqué de cada decisión, lo que se descartó y dónde podrían cuestionarte. Fecha: 8 de noviembre de 2026.

## 1. Qué pide la guía y cómo se respondió

| La guía pide | Dónde está en `Parte_II_Limpieza_G23` |
|---|---|
| Identificar las causas de limpieza (a. rango, b. inválidos o vacíos, c. extremos, d. interrelaciones) | Tabla 1: una fila por hallazgo, cada una con su punto de la guía, el conteo y la decisión |
| Seleccionar y justificar: eliminación, imputación por regresión o imputación aleatoria | Sección "Soluciones seleccionadas": se responde para las tres |
| Entregable punto 2: causas y **resultados** del proceso | Tablas 2 y 3 (embudos) + "Lo que la limpieza no resuelve" |
| Entregable punto 4: anexos técnicos obligatorios | Anexo T2: scripts, códigos de acto, fecha de descarga y control de cuadre |
| Rúbrica (45%): la decisión debe salir de las particularidades de **nuestros** datos | Cada regla tiene un número del AMB y, cuando se pudo, una prueba (por ejemplo, la mediana de la razón 3,22 frente a 1,10) |

## 2. Archivos creados en `guia_4`

| Archivo | Qué es | ¿Va al entregable? |
|---|---|---|
| `Parte_II_Limpieza_G23.md` / `.docx` | La Parte II redactada, con su anexo T2 | Sí: se pega en el informe del equipo |
| `limpieza_amb.py` | Aplica todas las reglas y escribe los dos CSV y el embudo | Se cita en el anexo |
| `descarga_actos.py` | Descarga de la API los actos de los folios con pares | Se cita en el anexo |
| `resultados_limpieza.txt` | La salida del script: el embudo que se ve en las tablas 2 y 3 | Soporte |
| `compraventas_limpias.csv` | 133.720 compraventas limpias, con marcas de extremos | Insumo de la Parte III |
| `pares_amb.csv` | 14.469 pares con marcas; 13.978 con `para_indice = True` | Insumo de la Parte III |
| `datos_api/actos_folios_pares.csv` + `LEEME_descarga.json` | 76.065 actos descargados y el registro de la descarga | Soporte |

Si cambias una regla, vuelve a correr `py -I limpieza_amb.py > resultados_limpieza.txt` y actualiza las cifras del documento. Las cifras del documento salen todas de esa corrida, o de verificaciones que corrí aparte sobre esos mismos archivos.

## 3. Paso a paso y decisiones

### 3.1 Perfilado del CSV local
- `datos/amb_compraventas_2015_2023.csv`: 165.517 filas, solo compraventas (código 125), con los 4 municipios del AMB.
- **Hallazgo:** no hay vacíos en el valor ni en la fecha. Por eso la respuesta a "eliminación general" es que se elimina **por regla**, no por vacío. Si alguien del equipo escribe "se eliminaron las filas con datos vacíos", estaría describiendo algo que no ocurre en esta base.

### 3.2 Reglas sobre las compraventas (en el orden en que se aplican)
1. **Fecha:** hay dos formatos. 31.569 filas vienen como `dd/mm/aa`. Se unificaron y ninguna quedó inválida. En la guía 2 se habló de tres formatos a nivel nacional; en el AMB solo aparecen dos.
2. **Valor > COP 1 M:** salen 770. Esto aclara la duda de la conversación anterior: son 164 con valor 0, 161 entre 1 y 999.999 y **445 con exactamente COP 1.000.000**. La regla de la guía 2 dice "mayor que", así que esos 445 salen. Un valor redondo de un millón casi nunca es un precio real. Podrían preguntarte por qué "mayor que" y no "mayor o igual": esa es la respuesta.
3. **Un solo valor en la anotación:** salen 4.
4. **Duplicados de folio y fecha (161 grupos):** en el 66,5% de los grupos el valor es igual, así que es la misma venta anotada dos veces y se deja una copia (salen 112). Si el valor es distinto, no se sabe cuál es el correcto y salen todas las copias (90). *Primero lo hice eliminando todas las copias y luego lo corregí: borrar las dos copias de una venta repetida pierde un dato bueno.*
5. **Escritura de varios predios: es la regla que más quita (30.821).** Se identifica porque el mismo `documento_justificativo` aparece en más de un folio. Su mediana es COP 30,6 M frente a 97 M, lo que confirma que el valor es un global o una parte, no el precio del predio.
   - *Debilidad posible:* algunos textos del documento no traen la notaría (por ejemplo "ESCRITURA 2633 DEL 21/10/22; PIEDECUESTA"), así que dos escrituras distintas con el mismo número y fecha podrían confundirse. Es un caso raro y no lo cuantifiqué.
6. **Zona vacía:** solo 52 de 1.855 se recuperan de otra venta del mismo folio. Es poco, y lo honesto es reportarlo así. El resto queda como categoría `SIN INFORMACION`.

### 3.3 Extremos: se marcan y no se borran
- **El argumento:** el proyecto tiene un detector de anomalías (OA6). Si borras los extremos en la limpieza, te quedas sin lo que el detector debe encontrar.
- Las tres marcas son:
  - `extremo_alto`: por encima del percentil 99,5 (COP 1.050 M). El umbral lo escogí yo; la guía no lo fija.
  - `cola_baja_1_10M`: ventas entre COP 1 M y 10 M (5.806).
  - `cambio_extremo_5x`: pares cuyo precio se multiplica o se divide por 5 o más.
- **Asimetría de 161, y de -0,7 en logaritmo:** esto justifica trabajar en logaritmo y con medianas en lugar de recortar más datos.

### 3.4 Descarga de los actos del folio (la regla 5 de la guía 2)
- Se consultaron por API **solo los 13.129 folios que forman pares**. Son los únicos donde un cambio físico afecta el índice. Bajar todo el AMB (~1 M de actos) no habría cambiado el resultado.
- Lotes de 150 folios, reintentos ante errores de red y un registro en `LEEME_descarga.json`.
- **Control de calidad de la descarga:** las 29.409 compraventas de esos folios en la API coinciden exactamente con las del CSV local. Así se demuestra que la API y el archivo son la misma fuente.
- **Error que cometí y corregí:** al primer intento leí las fechas de la API con un formato equivocado y solo cuadraba una parte. Al corregirlo, todas las fechas se leyeron bien (0 inválidas).
- **Límite que debes conocer:** el dataset solo trae actos de 2015 a 2023. Como los pares también están en ese periodo, el intervalo entre las dos ventas siempre está cubierto. Un cambio anterior a 2015 no afecta el par.

### 3.5 Qué se considera cambio físico (la decisión más defendible con datos)
- **Sí cuentan:** construcción, corrección de área o linderos, división, englobe, desenglobe, loteo, urbanización y constitución de propiedad horizontal. En los 156 pares con alguno de esos actos el precio se multiplica por 3,22 (mediana), frente a 1,10 en los demás. Por tipo: construcción ×2,44 y corrección de área ×3,26.
- **No cuentan:** la reforma (331) y la adición (347) del reglamento de propiedad horizontal. Son los actos más frecuentes entre ventas (527 y 451 pares), pero su razón de precios es 1,03-1,10, igual a la del total. Se registran en todos los apartamentos cuando cambia el edificio. Si los hubiera incluido, habría quitado casi 1.000 pares buenos.
- La constitución de propiedad horizontal (317) aparece solo 7 veces y su razón es 1,03. La dejé por concepto: el folio deja de ser un lote y pasa a ser una unidad. Afecta muy pocos pares, pero sería legítimo discutirla.
- **Ventana:** el acto cuenta si se radicó después de la primera venta y hasta el mismo día de la segunda. Así se incluye una construcción declarada en la misma escritura de la venta.

### 3.6 Por qué no se imputa
- **Regresión:** el valor es lo que se mide; imputarlo es circular. Además, lo eliminado (14,9% a 21,0% por año) no deja ningún año vacío.
- **Aleatoria:** mete variación que no viene del mercado.
- La guía *permite* concluir que una técnica no aplica. La rúbrica premia que la elección de **no** aplicar se justifique con los datos, y eso es lo que se hace.

## 4. El hallazgo que tienes que contarle al equipo
**En el AMB, el 52,3% de los pares limpios crece entre 0% y 5% al año, y la mediana es 2,98%**, prácticamente el reajuste por decreto. En la guía 2, la cifra nacional era 41%.

Qué significa:
- La limpieza **no** arregla esto: no es un error de dato, es un valor declarado por el avalúo. Le toca al clasificador (OA2).
- Para la **Parte III** es un resultado central: en el AMB, más de la mitad del registro reproduce el avalúo. Es coherente con el problema de negocio (refuerza la necesidad del clasificador), pero puede incomodar: un índice sin clasificar mostraría un mercado casi plano.
- Ojo: es la proporción sobre los pares *limpios*. No es directamente comparable con el 41% nacional, que se midió sobre todas las reventas.

## 5. Qué decirle a cada compañero
- **Parte I (calidad):**
  - Que use las cifras de la Tabla 1 para completitud, consistencia y formato, para que no haya dos números distintos para la misma cosa.
  - Completitud: 100% en los campos del modelo; las únicas columnas vacías son `folios_derivados` y `fecha_apertura_texto`.
  - Formato: 2 formatos de fecha.
  - Consistencia: escrituras de varios predios y duplicados.
- **Parte III (entendimiento):**
  - Debe trabajar con `compraventas_limpias.csv` y con `pares_amb.csv` filtrado por `para_indice == True`.
  - En "Filtración" e "Imputación" (técnicas 1 y 2 de su lista) debe remitir a la Parte II, no repetirla.
  - Las marcas de extremos sirven para su técnica de segmentación o agrupación.
- **Coordinación:** las cifras del contexto nacional de la guía 2 (5,4 M de compraventas, 256.973 pares) no son las de este piloto. El informe debe dejar claro que la Guía 4 trabaja sobre el AMB.

## 6. Dónde podrían cuestionarte y qué responder
| Pregunta posible | Respuesta |
|---|---|
| ¿Por qué el 19% de los datos sale? | El 97% de lo que sale son escrituras de varios predios: su valor no es el precio del predio. Lo demás son 1.000 filas. |
| ¿Por qué no imputan? | El valor es la variable de interés; imputarlo inventaría el mercado. Ver la sección 3.6. |
| ¿Por qué el percentil 99,5 y el umbral de 5 veces? | El de 5 veces viene de la guía 2. El 99,5 es una marca, no un filtro: no cambia el índice, solo identifica candidatos para OA6. |
| ¿Cómo saben que la reforma del RPH no es cambio físico? | Su razón de precios es igual a la del total (1,03-1,10 frente a 1,10). |
| ¿Es representativo del país? | Es un piloto. Las reglas no dependen del municipio, pero las proporciones sí cambian; por ejemplo, el valor declarado es 52% aquí y 41% a nivel nacional. |

## 7. Pendientes y supuestos
- [ ] Revisar que el `.docx` se vea bien al pegarlo en el informe del equipo (pandoc genera tablas simples; ajusta el estilo de tabla al del documento).
- [ ] Confirmar con el equipo si la Parte III usará los pares rurales (1.398 en el AMB): son pocos para un índice rural del AMB.
- [ ] No verifiqué cuántas escrituras de varios predios son falsos positivos por textos de documento sin notaría (sección 3.2, punto 5).
- La consola de Windows muestra mal las tildes en `resultados_limpieza.txt` si se corre sin `PYTHONIOENCODING=utf-8`; solo es la visualización, los datos están bien.
