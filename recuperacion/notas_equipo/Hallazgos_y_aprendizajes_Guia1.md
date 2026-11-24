# Guía 1 – Hallazgos, tips y lo que debes aprender del proceso

> Documento de estudio personal (no se entrega). Resume qué se hizo, por qué, qué descubrimos en los datos reales y qué debes poder explicar si te preguntan.

## 1. Qué se entregó y dónde está

| Archivo | Para qué |
|---|---|
| `Carta_Proyecto_Guia1.pdf` | **Entregable 1** – Carta Proyecto con el formato de la guía (3 págs.) |
| `Anexo_Guia1_Respuestas.pdf` | **Entregable 2** – Anexo con respuestas a las Partes I–VII (5 págs.; el máximo es 10) |
| `fuente/*.html` + `estilos.css` | Fuente editable de los PDF (ver sección 8) |
| Este `.md` | Solo para ti |

**Antes de entregar debes completar los `[corchetes]`:** nombres del equipo, encargado, asesor y fechas de aprobación. No los inventé.

## 2. La lógica de la guía (el "hilo" que debes entender)

La guía es un embudo: **muchas ideas → una oportunidad → un problema bien redactado → ¿es factible? → replantear → medir éxito**.

1. **Parte I – Idealización:** generar ideas con 4 estrategias (plan estratégico, análisis financiero, métricas de desempeño, orgánicas) y filtrarlas con 7 criterios. *Una idea que falla un criterio se descarta.*
2. **Parte II – Jerarquizar y describir:** matriz valor vs. potencial (IBM), 5 W, y el enunciado «Mejoraremos… / Para… / El usuario lidia hoy porque… / Al resolverlo…».
3. **Parte III – Accesibilidad:** ¿hay datos?, ¿se puede modelar?, ¿la organización lo va a usar?
4. **Parte IV – Replanteamiento:** si III revela problemas, se vuelve a II y se reformula. Aquí se declaran las **limitantes**.
5. **Parte V – Beneficios:** con una métrica y un nivel *actual*.
6. **Parte VI – Criterios de éxito:** de cierre (triple restricción) **y** de avance (monitoreo).
7. **Parte VII – Contexto:** la organización y el sector.

> **Tip clave:** el problema se define **en términos de negocio, no de técnica**. «Entrenar un XGBoost» no es un problema de negocio; «el OIC no sabe qué operaciones revisar primero» sí.

## 3. Decisiones que tomé (y por qué) – defiéndelas

| Decisión | Razón |
|---|---|
| **Territorio: Área Metropolitana de Bucaramanga** (Bucaramanga, Floridablanca, Girón, Piedecuesta) | Cobertura de valor ≈100 %, volumen suficiente (165 517 compraventas), mercado urbano comparable. Es la justificación que el caso pide explícitamente (criterios de cobertura, volumen, comparabilidad, pertinencia). |
| **Acto: solo compraventas (cód. 125)** | Es el que mejor representa un precio de mercado; cancelaciones, aclaraciones o reglamentos de PH no tienen un valor comparable. |
| **Unir valoración + atípicos en una oportunidad** | El caso los presenta como dos dimensiones complementarias sobre la misma población; los residuos del modelo de valor alimentan la priorización de atípicos. |
| **Cliente: OIC–IGAC** | Es el actor cuyo mandato (monitorear y alertar) encaja con el problema y cumple el criterio de «champion». |
| **Metas como «reducir ≥20 % vs. línea base ingenua»** | Aún no existe una línea base medida. En vez de inventar un número absoluto de error, la meta se ata a una referencia simple que se medirá en la fase *Medir*. |
| **Sin VPN** | No hay costos observables en un piloto académico; inventarlo sería fabricar datos. Se explica cómo calcularlo si el OIC aporta horas y costos. |

## 4. Hallazgos reales en los datos (consultados por API el 18/10/2026)

Fuente: datos.gov.co, id `7y2j-43cv`. Esto es lo más valioso para tu sustentación.

1. **El campo `valor` no está en todas las ciudades por igual.** Entre compraventas: Bogotá 39,5 %, Medellín 42,1 %, Cali 40,9 %, Barranquilla 40,1 %. En cambio Bucaramanga, Ibagué, Pereira, Cúcuta, Cartagena, Armenia, Manizales, Villavicencio y Pasto tienen ≈100 %. Escoger Bogotá por ser la más grande habría sido un error: casi el 60 % de sus compraventas no se podría modelar. **Lección: la selección de territorio debe guiarse por la pregunta y por la calidad del dato, no por el tamaño.**
2. **Hay valores extremos muy marcados.** En Bucaramanga: máximo de COP 143 246 millones en una sola compraventa; 653 compraventas > COP 1 000 M (0,9 %); 15 > COP 10 000 M; 77 con valor 0. Se necesitan métricas robustas y tratamiento documentado (marcar, no borrar).
3. **Cola baja sospechosa:** 5,9 % de las compraventas de Bucaramanga están entre COP 1 y 10 M. Puede ser cuota parcial, derecho de cuota o error de digitación.
4. **`numero_catastral` y `numero_catastral_antiguo` vienen vacíos** (0 de 1 062 263 filas en el AMB, y 0 en todo 2023). Esto significa que **no se puede cruzar con catastro** por esa vía. Es una limitante grande para el Capstone.
5. **La unidad de observación es la anotación, no el inmueble.** Una compraventa parcial puede generar folios derivados (7 258 en el AMB).
6. **Descripción vs. realidad:** la ficha dice 30 905 678 registros; la API devuelve 30 903 248. Diferencia pequeña, pero documéntala: demuestra que no se confía ciegamente en la ficha.
7. **Efecto pandemia:** compraventas del AMB caen de ~19–20 mil/año a 12 724 en 2020 y se recuperan a 21 502 en 2022. Cuidado con la validación temporal.
8. **El precio promedio de Bucaramanga sube de ≈COP 136 M (2015) a ≈COP 180 M (2023)**, con un salto en 2020 (≈191 M), probablemente por cambio de composición de lo que se vendió. Esto es una hipótesis, no una conclusión.
9. **Panorama nacional:** 59 % de las anotaciones tiene valor; la compraventa (5,4 M) es el acto «con dinámica» más numeroso.

## 5. Tips de gerencia de proyectos que se aplicaron

- **Triple restricción** (alcance, tiempo, costo) **+ calidad + satisfacción de SH**: cada criterio de éxito de la Parte VI se asoció a una dimensión.
- **Métricas de negocio ≠ métricas de proceso.** La rúbrica pide **ambas** (10 %). Negocio: precisión@100, reducción de error. Proceso: horas vs. plan, % de datos validados, MAE por iteración.
- **CTQ (voz del cliente, medibles)** vs. **Key Business Drivers (variables del negocio)**: los CTQ son lo que el cliente exige del producto; los drivers son lo que mueve el éxito de la compañía. No son lo mismo; revisa la carta para ver el contraste.
- **DMAIC como esqueleto del cronograma:** Definir, Medir, Analizar, Mejorar, Controlar, con responsable por fase. La rúbrica pide que se refleje la relación con los grupos de procesos y que se vean los recursos y limitantes.
- **Stakeholders afectados negativamente:** la rúbrica de «Alto/Sobresaliente» lo pide. Aquí: personas señaladas por falsos positivos y notarías/ORIP por carga adicional.
- **Escribe la limitación junto a la solución:** «alerta ≠ fraude», «estimación ≠ avalúo». El caso lo repite varias veces; es una señal de qué espera el docente.

## 6. Cómo se alinea con la rúbrica (revisa que no se pierda nada)

| Dimensión (peso) | Dónde se cubre |
|---|---|
| Completitud del formato (10 %) | Carta: todos los campos diligenciados y coherentes entre sí |
| Necesidades: contexto y problema (40 %) | Carta + Partes II, IV, VII del anexo: *qué*, *para quién*, *quién participa*, *por qué*; beneficios; SH positivos y negativos |
| Criterios de éxito (15 %) | Parte VI.1 con justificación y medibles |
| Métricas de desempeño (10 %) | Carta y Parte V/VI.2: negocio y desarrollo/monitoreo |
| Recursos y limitantes (15 %) | Parte III y IV: humanos, datos, tecnológicos; de dónde salen los datos; limitantes de adquisición |
| Planificación inicial (10 %) | Carta: DMAIC con fechas y responsables |

**Punto débil que debes reforzar tú:** la rúbrica pide justificar el problema con «clara investigación y sustento de conceptos de negocio del sector inmobiliario». Se dejó una base sólida (DANE, IGAC, ISO 19152, IVS, UIAF), pero si quieres subir de nivel, añade 1–2 fuentes propias (p. ej., datos del mercado de vivienda de Santander, informes de Camacol o del Banco de la República) y una frase sobre el mercado de Bucaramanga.

## 7. Pendientes y puntos a validar antes de entregar

1. **Completar nombres, asesor y fechas** (todos los `[corchetes]`).
2. **Discutirlo con tu equipo:** el territorio y el enfoque fueron decisión mía con base en datos. Si prefieren otra ciudad (p. ej. Ibagué o Pereira), la estructura se mantiene; solo cambian cifras.
3. **Las metas (≥20 %, precisión@100 ≥50 %) son propuestas.** Justifícalas como hipótesis a calibrar en *Medir*; no son resultados.
4. **Confirmar la categoría DNP** de Floridablanca, Girón y Piedecuesta (solo verifiqué Bucaramanga).
5. **Aceptación de los stakeholders:** la guía pide su aceptación si hay acceso. Si no hablaste con nadie del OIC, déjalo como supuesto (así está redactado).
6. **Ajustar el cronograma a fechas reales** y confirmar si el curso quiere el plan por semanas o por fechas.
7. **Revisar los PDF** (portada, ortografía, nombres) antes de subirlos.

## 8. Cómo reproducir o editar

- Edita `fuente/carta_proyecto.html` o `fuente/anexo_guia1.html` y regenera con Edge sin interfaz:
  `msedge --headless --no-pdf-header-footer --print-to-pdf=salida.pdf file:///ruta/archivo.html`
- Consultas a la API (ejemplo, SoQL):
  `https://www.datos.gov.co/resource/7y2j-43cv.json?$select=count(*) as n&$where=divipola='68001' AND cod_natujur='125'`
  Los alias necesitan la palabra `as`; los campos numéricos como `valor` admiten `avg`, `sum`, `max`.
- La plantilla Excel de la carta no se llenó: el entregable pedido es PDF.

## 9. Mirando hacia las siguientes guías

- **Guía 2 (adquisición):** descarga paginada de ~1,06 M filas del AMB (o solo 165 517 compraventas); registra fecha de descarga y versión.
- **Guía 3/4:** perfilado de calidad (completitud, unicidad, validez, consistencia), análisis de extremos, comparabilidad por municipio·año·zona. Define reglas **antes** de modelar.
- **Capstone:** valida temporalmente (no mezcles años al azar), reporta MAE/MdAPE en escala de valor y en log, y explica que una alerta es una señal, no una acusación.
