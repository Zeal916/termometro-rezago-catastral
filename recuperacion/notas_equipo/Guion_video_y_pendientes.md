# Video semana 4 – Guion y pendientes del equipo

Proyecto: **Termómetro de rezago catastral** (G23). El nombre del proyecto debe aparecer en el video y en el Padlet "Video Semana 4", igual que en la Carta Proyecto.

## 1. Qué evalúa la rúbrica del video (y cómo lo cubre el guion)

| Dimensión | Peso | Para llegar a "Sobresaliente" | Dónde se cubre |
|---|---|---|---|
| Estructura | 10 | Las 7 secciones: equipo, problema de negocio, problema de Analytics, relevancia, impacto de negocio, **entendimiento de los datos**, consideraciones de impacto inicial | Bloques 1 a 5 |
| Calidad de la información | 35 | Claridad y coherencia entre las partes | Hilo: negocio → relevancia → Analytics → datos → impacto |
| Apoyos visuales | 20 | Figuras y tablas pertinentes **y fáciles de leer** | Una diapositiva por idea (sección 4) |
| Calidad del video | 10 | Audio e imagen limpios en todo el video | Requisitos de grabación (sección 2) |
| Duración | 5 | **5:00 ± 5 s**. De 4:31 a 4:55 ya es "Alto" | Guion de ~740 palabras; cronometrar |

Ojo: el video se basa solo en las guías 1 y 2. Los riesgos (RBS y AMEF de la Guía 3) no van en el video.

## 2. Lo que necesito de cada compañero

**Para el video (todos):**
1. Leer su bloque y confirmar o ajustar el texto antes del **[fecha]**. Si cambian algo, que conserve la duración.
2. Grabar su bloque en un lugar silencioso, con audífonos con micrófono o micrófono externo (no el del portátil), en horizontal, a 1080p y con la cámara a la altura de los ojos. Formato: **[Zoom/Teams compartiendo diapositivas, o archivo individual]**.
3. Enviarme el archivo antes del **[fecha]** y cronometrarse: el tiempo de cada bloque está en el guion.
4. Revisar el corte final y aprobarlo antes de publicar (enlace de YouTube no listado + Padlet).

**Insumos específicos:**
- **Dayan / Daniel:** 2 o 3 gráficas limpias de los datos (ver sección 4): el histograma del crecimiento anual de las reventas (muestra el 41% entre 0% y 5%), la cobertura de los índices actuales frente a la meta y, si se puede, un mapa de los 527 municipios del Art. 49.
- **Nicolás:** confirmar que las cifras del contexto siguen vigentes (41,34% de área actualizada, 1.639.140 predios, aumento mediano de 326%, demanda ante el Consejo de Estado y C159).

**Para el documento de la Guía 3 (para que quede "Sobresaliente"):**
- **RBS:** el nivel 3 tiene que ser propio del proyecto, no el ejemplo genérico de la guía. Cada nivel 3 debe colgar con lógica de su nivel 2 (es la mitad de la nota de "Despliegue").
- **AMEF:** una fila por cada riesgo de nivel 3, con Sev, Oc y Det de 1 a 10 y RPN = Sev × Oc × Det. Para los RPN más altos: acciones realizables con los recursos que declaramos (COP 0 en efectivo, 4 personas, 16 semanas), responsable y plazo.
- **Segunda metodología:** para llegar a "Sobresaliente" los resultados deben ser coherentes con otra metodología. Sugiero una matriz de probabilidad × impacto con los mismos riesgos y mostrar que los de mayor RPN quedan en la zona roja.
- **Inconsistencia de la plantilla:** el Excel dice "Sev. (0-1)", pero la guía dice de 1 a 10. Usemos **1 a 10**, que es lo que dice la guía, y aclarémoslo en el documento (o preguntemos al profesor).
- Riesgos semilla propios de nuestro proyecto, para no partir de cero:
  - **Datos:** las vigencias (año de última actualización) están en PDF escaneados y su extracción con OCR puede retrasarse; el valor registrado sigue al avalúo (41% de las reventas); hay pocos pares en municipios rurales; no hay número catastral para cruzar con catastro.
  - **Tiempo:** la extracción con OCR es el cuello de botella (de S3 a S5).
  - **Contrato/alcance:** no hay contacto formal con el IGAC ni con el OIC para validar; la regla puede cambiar con el C159 o con un fallo del Consejo de Estado.
  - **Calidad:** las etiquetas débiles del clasificador pueden sesgarlo; el modelo podría no superar la regla del reajuste (18,3%).
  - **Entregables:** que una alerta se use como prueba de irregularidad (riesgo reputacional y jurídico).
  - **Gente:** somos 4 personas de tiempo parcial y la carga se concentra en ingeniería de datos.

## 3. Lo que cada bloque tiene que decir

No hay que aprenderse el guion. Cada quien puede decir su parte con sus propias palabras o leer el guion de referencia de la sección 4; lo único obligatorio es cubrir estos puntos y respetar el tiempo de su bloque. Las cifras están en las diapositivas, así que se pueden leer de ahí.

### Bloque 1 – Equipo · Cristian · 0:00–0:25 · diapositiva 1
- [ ] Equipo 23: los cuatro integrantes y el asesor, Carlos Ramírez.
- [ ] El nombre del proyecto: **Termómetro de rezago catastral** (lo exige la actividad).
- [ ] En una frase, qué hace: medir qué tan lejos están los avalúos catastrales del mercado inmobiliario.

### Bloque 2 – Problema de negocio y relevancia · Nicolás · 0:25–1:35 · diapositivas 2 a 4
- [ ] El avalúo es la base del predial y por norma debe estar entre el 60% y el 100% del valor comercial.
- [ ] Sin actualización, el avalúo solo sube cerca de 3% al año por decreto y se queda atrás del mercado.
- [ ] El IGAC tiene el 41% del área del país actualizada, frente a una meta de 70%.
- [ ] El Art. 49 subió de una vez los avalúos de 1,6 millones de predios rurales en 527 municipios (aumento mediano de 326%).
- [ ] Lo que generó: paro campesino en Santander, revisión municipio por municipio (Res. 0384) y una demanda ante el Consejo de Estado.
- [ ] Por qué es relevante: los índices oficiales de precios son urbanos y parciales (el IPVN cubre 53 municipios) y no hay ninguno rural, así que el IGAC decide sin contrastar con las ventas reales.

### Bloque 3 – Problema de Analytics · Daniel · 1:35–2:45 · diapositivas 5 y 6
- [ ] El problema de negocio: mejorar la medición de la relación avalúo–mercado con la que la Dirección de Gestión Catastral y el OIC deciden qué municipios actualizar o revisar primero.
- [ ] El problema de Analytics: medir con transacciones registradas la brecha entre mercado y avalúo por municipio, en zona urbana y rural.
- [ ] Las tres técnicas y para qué sirve cada una: índice de ventas repetidas (no necesita área ni estrato), clasificador de escrituras y detector de anomalías (cupo de 2%).
- [ ] Las metas frente a la línea base: MdAPE de 18,3% a 16,5% o menos; AUC mayor a 0,757; de 53 y 0 municipios con índice a 340 urbanos y 324 rurales.

### Bloque 4 – Entendimiento de los datos · Dayan · 2:45–3:50 · diapositivas 7 y 8
- [ ] La fuente principal es abierta: el Registro de Transacciones Inmobiliarias del IGAC 2015–2023, con 5,4 M de compraventas, 4,0 M con valor y 1.096 municipios.
- [ ] Se complementa con la Resolución 2057 (7.484 zonas con su aumento) y se valida con los índices del DANE y del Banco de la República.
- [ ] Hallazgo 1: solo el 15% de las compraventas tiene una venta anterior, por eso medimos por municipio y no por predio.
- [ ] Hallazgo 2: el 41% de las reventas crece entre 0% y 5% al año, es decir, el valor sigue al avalúo; por eso clasificamos las escrituras.
- [ ] Hallazgo 3: el año de la última actualización está en PDF escaneados; se extrae con OCR, empezando por los 68 municipios de Santander.

### Bloque 5 – Impacto inicial y cierre · Cristian · 3:50–5:00 · diapositivas 9 y 10
- [ ] Los tres impactos: focalizar con un ranking de municipios, sustentar o corregir el Art. 49 en 143 municipios, y alertas para el OIC.
- [ ] A quién afecta: ganan los municipios con rezago (recaudo y planeación) y los propietarios de zonas sobreajustadas (corrección); otros pagarían más predial, por eso la evidencia debe ser transparente.
- [ ] El límite: una alerta es una señal para revisar, no una conclusión sobre un avalúo o una persona; el producto no modifica avalúos.
- [ ] La medida sirve con cualquier regla: el piso actual de 60% o el techo de 50% del proyecto de ley C159.
- [ ] Los recursos: 16 semanas, herramientas abiertas y COP 0 en efectivo.
- [ ] Cerrar con el nombre del proyecto y agradecer.

## 4. Guion de referencia (opcional, para quien prefiera leer) · ~750 palabras ≈ 5:00

> Cronometrar en un primer ensayo. Si se pasa de 5:05, recortar las frases marcadas con **[recortable]**. Si queda corto, hablar un poco más despacio en vez de agregar texto.

### Bloque 1 – Equipo · Cristian · 0:00–0:25
*[Diapositiva: título del proyecto, logos, nombres y asesor]*

> Hola, somos el equipo 23 de Gerencia de Proyectos de Analytics: Nicolás Santos, encargado del proyecto; Daniel Aguirre; Dayan Hincapié, y yo, Cristian Ortiz, con la asesoría de Carlos Ramírez. Les presentamos el avance de nuestro anteproyecto: el **Termómetro de rezago catastral**, una herramienta para medir qué tan lejos están los avalúos catastrales del mercado inmobiliario en Colombia.

### Bloque 2 – Problema de negocio y relevancia · Nicolás · 0:25–1:35
*[Diapositiva: "avalúo entre 60% y 100% del valor comercial" + línea de tiempo 2026 del Art. 49]*

> El avalúo catastral es la base del impuesto predial y, por norma, debe estar entre el 60% y el 100% del valor comercial. Pero cuando un municipio no se actualiza, el avalúo solo sube por decreto, cerca de 3% al año, mientras el mercado puede subir mucho más. Hoy el IGAC reporta apenas 41% del área del país actualizada, frente a una meta de 70%.
>
> En 2026 el IGAC aplicó el artículo 49 de la Ley 2294 y subió de una sola vez los avalúos de más de 1,6 millones de predios rurales en 527 municipios, con un aumento mediano de 326%. **[recortable]** Eso generó un paro campesino en Santander, revisiones municipio por municipio y una demanda ante el Consejo de Estado.
>
> ¿Por qué es relevante? Porque las medidas oficiales de precios son urbanas y parciales —el índice de vivienda nueva del DANE cubre 53 municipios— y en lo rural no existe ninguna. Hoy el IGAC decide dónde actualizar, y defiende el ajuste, sin un contraste independiente con las ventas reales.

### Bloque 3 – Problema de Analytics · Daniel · 1:35–2:45
*[Diapositiva: enunciado "Mejoraremos… / Para…" + esquema de 3 técnicas + tabla línea base → meta]*

> Nuestro problema de negocio es mejorar la medición de la relación entre el avalúo y el mercado con la que la Dirección de Gestión Catastral y el Observatorio Inmobiliario Catastral deciden qué municipios actualizar o revisar primero.
>
> Lo traducimos a un problema de Analytics: medir, con transacciones registradas, la brecha entre el mercado y el avalúo por municipio, en zona urbana y rural. Para eso usamos tres técnicas: un índice de ventas repetidas, que compara cada inmueble consigo mismo y por eso no necesita área ni estrato; un clasificador que separa las escrituras con el precio real de las declaradas por el avalúo, y un detector de anomalías con un cupo de 2% de alertas.
>
> Nuestras metas: bajar el error mediano de 18,3% a 16,5% o menos, superar un AUC de 0,757 en anomalías y pasar de 53 municipios con índice urbano, y cero rurales, a 340 y 324.

### Bloque 4 – Entendimiento de los datos · Dayan · 2:45–3:50
*[Diapositiva: fuentes con cifras + histograma del crecimiento anual de las reventas con el pico entre 0% y 5% resaltado]*

> ¿Qué tan bien entendemos los datos? Trabajamos con el Registro de Transacciones Inmobiliarias del IGAC 2015–2023, que es abierto: 5,4 millones de compraventas, 4 millones con valor, en 1.096 municipios. Lo complementamos con la Resolución 2057, que trae el aumento de 7.484 zonas, y con los índices del DANE y del Banco de la República para validar.
>
> Tres hallazgos cambiaron el planteamiento. Primero, solo el 15% de las compraventas tiene una venta anterior del mismo inmueble; por eso medimos la brecha por municipio y no el valor de cada predio. Segundo, el 41% de las reventas crece entre 0% y 5% al año: el valor escrito muchas veces sigue al avalúo y no al precio real, y por eso clasificamos las escrituras. Tercero, el año de la última actualización está en PDF escaneados; lo extraemos con OCR, empezando por los 68 municipios de Santander.

### Bloque 5 – Impacto inicial y cierre · Cristian · 3:50–5:00
*[Diapositiva 9: 3 impactos + "alerta ≠ irregularidad" · Diapositiva 10: recursos y gracias]*

> ¿Cuál es el impacto inicial para el negocio? Primero, focalizar: un ranking de municipios, con la razón de su prioridad, para que el IGAC actualice donde la brecha es mayor. Segundo, sustentar o corregir el ajuste del artículo 49 en 143 municipios con evidencia reproducible. Y tercero, entregar alertas al Observatorio para su revisión.
>
> Ganan los municipios con rezago, que mejoran su recaudo y su planeación, y los propietarios de zonas sobreajustadas, que pueden pedir una corrección. Pero en los municipios priorizados algunos pagarían más predial, y por eso la evidencia tiene que ser transparente.
>
> También somos claros con los límites: una alerta es una señal para revisar, no una conclusión sobre un avalúo o una persona, y el producto no modifica avalúos. **[recortable]** Además, la medida sirve con cualquier regla: el piso actual de 60% o el techo de 50% que propone el proyecto de ley C159.
>
> Lo haremos en 16 semanas, con herramientas abiertas y un desembolso en efectivo de cero pesos. Esto es el Termómetro de rezago catastral. ¡Gracias!

## 5. Apoyos visuales (20% de la nota)

| # | Diapositiva | Contenido | Responsable |
|---|---|---|---|
| 1 | Portada | Nombre del proyecto, equipo, asesor, curso | Cristian |
| 2 | La regla y el rezago | Barra del 60%–100% del valor comercial; reajuste de 3% vs. mercado | Nicolás |
| 3 | 2026: Art. 49 | Línea de tiempo: Res. 2057 → paro → Res. 0384 → demanda → C159 | Nicolás |
| 4 | El vacío | Cobertura actual: IPVN 53 · IVP 22 · IPVU 9 · rural 0 | Nicolás |
| 5 | Problema de Analytics | Enunciado + 3 técnicas en cascada | Daniel |
| 6 | Metas | Tabla línea base → meta (MdAPE, AUC, cobertura, 143) | Daniel |
| 7 | Fuentes | 5,4 M / 4,0 M / 1.096 municipios / Res. 2057 | Dayan |
| 8 | Hallazgo clave | Histograma del crecimiento anual de las reventas (pico 0%–5%) | Dayan |
| 9 | Impacto y límites | 3 impactos + "alerta ≠ irregularidad" | Cristian |
| 10 | Cierre | Recursos (16 semanas, COP 0) + gracias | Cristian |

Reglas: letra mínima de 24 pt, una idea por diapositiva y cifras grandes. La rúbrica baja a "Alto" si algún visual es difícil de leer.

## 6. Checklist antes de publicar
- [ ] Duración entre 4:55 y 5:05 (verificar en el reproductor).
- [ ] Aparecen los 4 integrantes.
- [ ] El nombre "Termómetro de rezago catastral" aparece en el video y en el título del Padlet.
- [ ] El audio está nivelado entre bloques (sin eco ni ruido de fondo).
- [ ] Enlace de YouTube **no listado** en el Padlet "Video Semana 4".
- [ ] Comentar los videos de otros equipos (lo pide la actividad).
