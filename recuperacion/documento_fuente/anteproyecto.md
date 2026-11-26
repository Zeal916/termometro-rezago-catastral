---
lang: es
pagetitle: "Termómetro de rezago catastral"
---

::: portada
<div><p>TERMÓMETRO DE REZAGO CATASTRAL</p><p>DOCUMENTO FINAL DEL ANTEPROYECTO</p></div>

<div><p>NICOLÁS SANTOS</p><p>CRISTIAN ORTIZ</p><p>DANIEL AGUIRRE</p><p>DAYAN HINCAPIE</p><p>&nbsp;</p><p>ASESOR: CARLOS RAMÍREZ</p></div>

<div><p>GERENCIA DE PROYECTOS DE ANALYTICS</p><p>MAESTRÍA EN INTELIGENCIA ANALÍTICA DE DATOS</p><p>UNIVERSIDAD DE LOS ANDES</p><p>2026</p></div>

<div class="pt-pie"><p>Anexos y código: <span>https://github.com/Zeal916/termometro-rezago-catastral</span></p></div>
:::

## 1. Abstract

El avalúo catastral, base del impuesto predial, debe estar entre 60% y 100% del valor comercial, pero sin actualización solo sube cerca de 3% al año. En 2026 el IGAC aumentó de una vez los avalúos de 1,6 millones de predios rurales (Art. 49 de la Ley 2294 de 2023) sin un contraste público con el mercado: las medidas oficiales de precios cubren como máximo 53 municipios urbanos y ninguna zona rural. Se propone un termómetro de rezago catastral. Con las ventas repetidas del Registro de Transacciones Inmobiliarias del IGAC 2015-2023 se construye un índice de mercado por municipio, urbano y rural, después de clasificar las escrituras declaradas por el avalúo; con él se mide la brecha frente al reajuste, se prioriza dónde actualizar, se contrasta el Art. 49 y se señalan operaciones atípicas. Los datos muestran que la brecha se puede medir (un avalúo sin actualizar perdió entre 17% y 49% frente al mercado) y que 41% de las reventas sigue al avalúo. Las metas son bajar el error mediano de 18,3% a 16,5%, superar un AUC de 0,757 y pasar de 53 a 340 municipios urbanos y de 0 a 324 rurales con evidencia propia.

## 2. Índice de contenido, tablas y figuras

<div id="indice"></div>

## 3. Introducción

**Problema de negocio.** El Instituto Geográfico Agustín Codazzi (IGAC), a través de la Dirección de Gestión Catastral y del Observatorio Inmobiliario Catastral (OIC), debe decidir en qué municipios actualizar o revisar primero el avalúo catastral y sustentar o corregir el ajuste del Art. 49 (Resolución 2057 de 2025), hoy en revisión y demandado. **Problema de Analytics.** Se traduce en tres preguntas que se pueden responder con datos que el propio IGAC publica: cuánto se separó el avalúo del mercado en cada municipio, urbano y rural; si el aumento del Art. 49 coincide con lo que muestran las ventas; y qué operaciones del registro son atípicas y deben revisarse.

**Métrica de negocio, beneficio esperado y seguimiento.** La métrica de negocio es el número de municipios con evidencia de mercado propia para decidir (hoy 53 urbanos y 0 rurales; meta, 340 y 324), junto con los municipios del Art. 49 contrastados (de 0 a 143) y los municipios donde el avalúo quedó bajo el piso legal de 60%, identificados con IC 95%. El beneficio financiero trazable es la parte de la base del predial que dejó de corresponder al mercado. El desempeño del proyecto se sigue con métricas de proceso (90% o más de hitos a tiempo y desviación de horas de ±15% o menos) y con métricas técnicas medidas contra una línea base: bajar el error mediano de 18,3% a 16,5% o menos y superar un AUC de 0,757.

**Relación con las guías.** La Guía 1 seleccionó el proyecto entre ocho ideas y formuló la carta; la Guía 2 tradujo el problema en requerimientos (modelo Kano), seis objetivos de análisis, fuentes y metas; la Guía 3 identificó 21 riesgos con una RBS y los ponderó con un AMEF; la Guía 4 evaluó la calidad de los datos y los limpió; y la Guía 5 eligió los enfoques y métodos y ajustó el plan del Capstone.

**Estructura del documento.** La sección 4 revisa el estado del arte. La sección 5 desarrolla el proyecto por las fases de la metodología de administración de proyectos de Analytics: inicialización (5.1, Guía 1), analizar y diseñar o planificación (5.2, Guías 2 a 5), configuración y construcción o ejecución (5.3), operación y monitoreo y control (5.4) y cierre (5.5, Guía 5); la sección 5.6 verifica el anteproyecto y registra las mejoras incorporadas. Las secciones 6 y 7 presentan las referencias y los anexos, que están en el repositorio del proyecto.

## 4. Estado del arte en las investigaciones en el área

El planteamiento se apoya en siete trabajos recientes y aplicaciones vigentes (Tabla 1). La diferencia del proyecto es combinar tres elementos que esos trabajos tratan por separado: la clasificación de escrituras declaradas por el avalúo, los índices rurales por municipio y el contraste de un ajuste masivo ya aplicado.

Table: Tabla 1. Trabajos relacionados y aporte al proyecto (Guía 2).

| Trabajo | Hallazgo principal | Aporte al proyecto |
|--------------------|------------------------------|----------------------------------|
| IGAC (2024a), documento metodológico del Art. 49 | Ajustó unos 245.000 datos del OIC (95% de la SNR) por considerarlos bajo el valor comercial | Mismo cliente y fuente; el proyecto mide ese sesgo en lugar de suponerlo |
| Banco de la República (s.f.), IPVU | Índice de ventas repetidas con avalúos hipotecarios en 9 ciudades | Valida el método en Colombia; el proyecto lo lleva a 340 municipios urbanos y 324 rurales |
| Avenancio-León y Howard (2022) | El avalúo responde menos que el mercado a las características del vecindario | Respalda la relación avalúo-precio como métrica de equidad |
| Anagol et al. (2025) | 7,3% de las escrituras de Mumbai declaran un valor a menos de 1% del valor oficial | Es el fenómeno encontrado: la cercanía al valor oficial es variable para OA2 |
| Zilli et al. (2024) | Random Forest y Gradient Boosting dominan el avalúo masivo y superan a los métodos tradicionales | Candidatos de OA2 y OA4; necesidad de línea base e IC |
| Han et al. (2022), ADBench | Ningún método no supervisado gana en todos los casos | Evaluar alertas con anomalías inyectadas y contra líneas base |
| Pulgarín-Franco (2024) | En 53 municipios colombianos, actualizar no aumentó por sí solo el recaudo | El beneficio se mide como base gravable, no como recaudo |

**Relación con el proyecto.** En lo metodológico, el IPVU y los trabajos clásicos de ventas repetidas (Bailey et al., 1963; Case y Shiller, 1987) sustentan comparar cada inmueble consigo mismo cuando el registro no trae atributos, y el modelo jerárquico de Francke y van de Minne (2017) muestra cómo compartir información entre municipios con pocos pares, que es el caso rural. En lo tecnológico, Zilli et al. (2024) y Han et al. (2022) orientan la elección de modelos: árboles potenciados frente a una línea base simple y alertas evaluadas contra varias líneas base. En el enfoque de negocio, Avenancio-León y Howard (2022) y Pulgarín-Franco (2024) muestran que el rezago del avalúo es un problema de equidad y de base gravable, y Anagol et al. (2025) e IGAC (2024a) documentan que el valor declarado se acerca al oficial. Ninguno mide ese sesgo en el registro colombiano ni contrasta un ajuste masivo ya aplicado: ese es el vacío que cubre el proyecto.

## 5. Desarrollo del proyecto

El proyecto se gestiona con la metodología de administración de proyectos de Analytics (MAPA) del curso, cuyas fases equivalen a los cinco grupos de procesos del PMI: inicialización (inicio), analizar y diseñar (planificación), configuración y construcción (ejecución), operación, optimización y despliegue (monitoreo y control) y cierre. El anteproyecto completó la inicialización y la planificación con resultados sobre los datos; la ejecución, el monitoreo y el cierre quedan planteados para el Capstone.

### 5.1 Fase de inicialización (Guía 1)

**El sector y el cliente.** El avalúo catastral es la base del impuesto predial y debe estar entre 60% y 100% del valor comercial (Decreto 148 de 2020). El IGAC es la máxima autoridad catastral y gestor directo en 836 municipios (IGAC, 2026b); su Observatorio Inmobiliario Catastral (OIC) debe monitorear el mercado y alertar sobre comportamientos atípicos. En julio de 2026 el IGAC reportó 41,34% del área del país actualizada, frente a la meta de 70% del PND 2022-2026: 59,1% de la meta (IGAC, 2026d). Con la Resolución 2057 de 2025 aumentó de una vez los avalúos de 1.639.140 predios rurales en 527 municipios, con un aumento mediano de 326% por zona homogénea (IGAC, 2025), y en septiembre de 2026 el Consejo de Estado admitió una demanda de nulidad contra esa resolución (Vanguardia, 2026). Desde agosto de 2026 hay un nuevo gobierno, crítico del ajuste, y el proyecto de ley C159 de 2026 propone un techo de 50% del valor comercial (Cámara de Representantes, 2026). La medida que propone el proyecto sirve con cualquiera de las dos reglas, porque ambas exigen medir el valor comercial.

**Generación y jerarquización de ideas.** El equipo exploró el dataset completo del IGAC (30,9 M de actos registrales) y fuentes complementarias, y generó ocho ideas con las cuatro estrategias de la guía (plan estratégico, métricas de desempeño, análisis financiero y lluvia de ideas). Las filtró con las siete características de un proyecto de Analytics (enfoque en el cliente, métricas medibles, *champion*, evento recurrente, ligado al negocio, beneficio financiero trazable y solución desconocida). Pasaron tres, que se integran en un solo proyecto: la idea 5 (detector de escrituras declaradas por el avalúo) limpia el dato, la 1 (termómetro de rezago) mide la brecha y la 2 (revisión del Art. 49) la contrasta con el ajuste. Se descartaron cinco: acumulación de precios en el tope VIS (se guarda como respaldo), radar de lavado de activos (sin casos confirmados), valor absoluto de cada compraventa (sin área ni estrato), tablero descriptivo (solución conocida) e índice del AMB (ya existe el IPVU). La matriz de valor y capacidad (IBM, 2020) ubica la idea 1 como foco y la 2 como valiosa pero difícil, porque depende de vigencias dispersas en PDF (Figura 1).

Table: Tabla 2. Filtro de las ocho ideas con las siete características de un proyecto de Analytics (Guía 1).

| Característica | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------------------|------|------|------|------|------|------|------|------|
| 1. Enfoque en el cliente | Sí | Sí | Sí | Sí | Sí | Sí | Parcial | Sí |
| 2. Métricas medibles rápido | Sí | Sí | Sí | No (sin casos confirmados) | Sí | No (sin área ni estrato) | Sí | Sí |
| 3. *Champion* dueño del proceso | Sí (IGAC) | Sí (IGAC) | Parcial (MinVivienda) | Parcial | Sí (OIC) | Sí | Sí | Sí |
| 4. Evento recurrente | Sí | Sí (fase rural 2026, revisiones abiertas) | Sí | Sí | Sí | Sí | Sí | Sí |
| 5. Ligado a objetivos del negocio | Sí | Sí | Parcial | Sí | Sí | Sí | Sí | Sí |
| 6. Beneficio financiero trazable | Sí (predial) | Sí (predial) | Parcial | No | Sí (avalúos sin sesgo) | Parcial | No | Parcial |
| 7. Solución desconocida | Sí (no hay índice rural) | Sí | Sí | Sí | Sí | Sí | No (tableros del OIC) | No (IPVU) |
| **Decisión** | **Pasa** | **Pasa** | Descartada | Descartada | **Pasa** | Descartada | Descartada | Descartada |

Ideas: 1 termómetro de rezago; 2 revisión del Art. 49; 3 acumulación de precios en el tope VIS; 4 radar de lavado de activos; 5 detector de escrituras declaradas por el avalúo; 6 valor absoluto de cada compraventa; 7 tablero descriptivo; 8 índice de ventas repetidas del AMB.

![Figura 1. Matriz de valor para el cliente y capacidad de avanzar de las ideas que pasaron el filtro (Guía 1).](img/matriz_valor_capacidad.png){width=66%}

**Preguntas de la oportunidad.** (1) *Oportunidad*: el IGAC necesita saber dónde el avalúo está más lejos del mercado para decidir dónde actualizar o revisar primero y sustentar o corregir el Art. 49. (2) *Retos*: el valor registrado no siempre es el precio real; las ventas no traen área, estrato ni zona homogénea; los municipios pequeños tienen pocas reventas; el tema es sensible (paro y demandas) y la regla puede cambiar (C159). (3) *Prioridad*: decidir con evidencia de mercado, empezando por los municipios del Art. 49 con reclamos abiertos. (4) *Recursos*: sí; datos abiertos y un equipo que cubre datos, modelación, negocio y comunicación. (5) *Tiempo*: 16 semanas en dos cursos. (6) *Autoridad final*: la Dirección General del IGAC, con la Dirección de Gestión Catastral como dueña del proceso.

**5W.** *Quién*: el IGAC (Dirección de Gestión Catastral, dueña del proceso, con el OIC) es cliente y *champion*; deben participar los analistas del OIC, las direcciones territoriales y las secretarías de Hacienda; ganan los municipios rezagados y los propietarios de zonas sobreajustadas, y pueden perder los propietarios de municipios priorizados y el IGAC si la evidencia contradice su ajuste. *Qué*: medir la brecha entre mercado y avalúo por municipio y señalar dónde el Art. 49 no coincide con las ventas. *Dónde*: el país donde el índice se pueda identificar (340 municipios urbanos y 324 rurales), con piloto en Santander, epicentro del paro (68 municipios del Art. 49, 15 con índice rural propio). *Cuándo*: el problema es permanente y la urgencia es ahora (demanda admitida en septiembre de 2026, PND 2026-2030 en febrero de 2027). *Por qué*: el reajuste es menor que la valorización y, cuando una escritura se declara por el avalúo, el registro reproduce el rezago en lugar de medirlo.

**Planteamiento del problema de negocio.** *Mejoraremos* la medición de la relación entre el avalúo y el mercado con la que el IGAC decide qué municipios actualizar o revisar primero y verifica el ajuste del Art. 49, *para* la Dirección de Gestión Catastral y el OIC. *Necesitan participar* los analistas del OIC, las direcciones territoriales y las secretarías de Hacienda. *El usuario lidia hoy* con medidas oficiales urbanas y parciales (IPVN: 53 municipios, vivienda nueva; IVP: 22 capitales; IPVU: 9 ciudades), sin ninguna rural, y con aumentos fijados desde el nivel central que hoy se revisan sin contraste independiente. *Al resolverlo*, la actualización y las revisiones se dirigen a donde la brecha es mayor y el ajuste se sustenta o corrige con evidencia reproducible. Una alerta es una señal para revisar, no una conclusión sobre un avalúo o una persona.

**Métricas de negocio derivadas.** El problema define tres métricas de negocio, medibles y con línea base: municipios con evidencia de mercado propia (hoy 53 urbanos y 0 rurales; meta 340 y 324), municipios del Art. 49 con contraste entre mercado y ajuste (hoy 0; meta 143) y municipios donde el avalúo quedó bajo el piso legal de 60% (hoy 49 urbanos y 53 rurales sin intervalo de confianza; meta: todos con IC 95%). El último es el beneficio financiero trazable: la parte de la base del predial que dejó de corresponder al mercado.

**Recursos y presupuesto.** Cuatro integrantes, cerca de 6 horas por semana cada uno: 384 horas en 16 semanas (192 en el anteproyecto y 192 en el Capstone). Python y bibliotecas libres, Git y computadores personales: las compraventas y los actos (unos 11 M de filas) caben en memoria. Desembolso en efectivo de COP 0; costo de oportunidad de COP 23.040.000 (384 horas a COP 60.000, supuesto del equipo), de los cuales COP 11.520.000 corresponden al Capstone.

**Criterios de éxito del proyecto.** *Alcance*: en el anteproyecto, carta y anexo, requerimientos y fuentes, informe de calidad con diccionario, análisis exploratorio y propuesta de modelos; en el Capstone, exploración descriptiva, índice, brecha, contraste del Art. 49, alertas, factores asociados a las diferencias y tablero. Quedan fuera recalcular avalúos, medir el mercado por zona homogénea, emitir conclusiones jurídicas o de fraude y poner el producto en producción. *Tiempo*: al menos 90% de los hitos en la fecha del cronograma. *Costo*: COP 0 en licencias y datos y desviación de horas de ±15% o menos por semana. *Calidad*: cumplir las metas de negocio y técnicas (Tabla 7) con todo el análisis reproducible con un script.

**Planificación inicial de actividades.** La carta organizó las 16 semanas por grupos de procesos, con un responsable por proceso encargado de gestionar que se cumpla lo planeado (Tabla 3). La capacidad es de 24 horas del equipo por semana (cuatro personas, cerca de 6 horas cada una): 192 en el anteproyecto y 192 en el Capstone. La semana pico es S3 (49 horas), compensada con S1 (9) y S2 (21), y el plan reserva 12 horas de holgura. Las limitantes que condicionan el orden son el tiempo parcial del equipo, la consolidación de vigencias catastrales en PDF y la falta de contacto directo con el IGAC; por eso los datos van antes de la calidad, la calidad antes del análisis exploratorio y este antes de la propuesta de modelos.

Table: Tabla 3. Cronograma inicial de la carta por grupos de procesos del trabajo del equipo (Guía 1).

| Grupo de procesos | Actividades | Semanas | Responsable |
|----------------|------------------------------------------|---------------|---------------|
| Inicio y planificación | Caso, ideación, jerarquización, 5W, carta y anexo; plan, riesgos y línea base | S1-S3 (5-25 oct 2026) | Nicolás Santos |
| Ejecución | Requerimientos (Kano), problema y métrica de Analytics, fuentes y estado del arte (S3); calidad, piloto de depuración en el AMB, diccionario y video (S4) | S3-S4 (19 oct-1 nov) | Cristian Ortiz |
| Ejecución | Análisis exploratorio, índices piloto, sensibilidad y contraste piloto en Santander (S5-S6); propuesta de modelos (S7) | S5-S7 (2-22 nov) | Daniel Aguirre |
| Planificación y ejecución (Capstone) | Plan (C1), datos depurados del país (C2-C3), modelos (C3-C6) y tablero (C5-C7): 151 horas | C1-C7 | Daniel Aguirre |
| Monitoreo y control; cierre | Revisión semanal de hitos, horas, riesgos, demanda y proyecto C159; cierre del anteproyecto (23-29 nov); en el Capstone, monitoreo (C1-C8, 8 horas) y cierre (C7-C8, 33 horas con 8 de holgura) | Todo el proyecto | Nicolás Santos (monitoreo); Dayan Hincapie (cierres) |

En la carta, los grupos de procesos se aplican al trabajo del equipo: en el anteproyecto, "ejecución" es producir los entregables de las guías. En la metodología del curso esas semanas son la fase de planificación (analizar y diseñar); la ejecución de los modelos queda para el Capstone (sección 5.3). Las horas del Capstone suman 192: 151 de planificación, datos, modelación y tablero, 8 de monitoreo y 33 de cierre.

### 5.2 Fase analizar y diseñar: planificación (Guías 2 a 5)

#### 5.2.1 Del problema de negocio al problema de Analytics (Guía 2)

**Resultados esperados y cambios en la organización (Guía 2, Fase a).** Se espera una solución que identifique el rezago entre avalúos y mercado y apoye la priorización de municipios, con índices por ventas repetidas urbanos y rurales, alertas de transacciones atípicas y un tablero. Participan capacidades de gestión catastral, ingeniería de datos, modelación y visualización: el IGAC y el OIC como referentes de negocio y el equipo como desarrollador. En la organización, la priorización pasaría a apoyarse en indicadores cuantitativos y trazables, y el contraste entre reajustes y precios se haría de forma sistemática, sujeto a validación técnica y adopción institucional.

Cada métrica de la carta se descompuso en submétricas y en un umbral a partir del cual se considera fracaso (Tabla 4).

Table: Tabla 4. Descomposición de las métricas de éxito y umbrales de fracaso (Guía 2).

| Métrica de la carta | Submétricas | Se considera fracaso si |
|--------------------|-------------------------------|-------------------------------|
| MdAPE de 16,5% o menos | MdAPE por zona y periodo; observaciones válidas; AUC del clasificador frente a la etiqueta débil | El IC 95% de la mejora frente a 18,3% incluye 0 |
| AUC mayor que 0,757 | AUC con anomalías ×2 y ×0,5; desempeño urbano y rural; proporción capturada con el cupo de 2% | El IC 95% de la mejora frente a 0,757 incluye 0 |
| 340 urbanos y 324 rurales | Municipios con índice propio; proporción de elegibles; ancho del IC (±10%) | Menos de 340 / 324 con índice identificado |
| 143 municipios del Art. 49 | Municipios con relación implícita entre avalúo y valor comercial (Res. 2057) y año de actualización acotado (2017 o antes); marca "coherente" o "revisar" | Menos de 143 contrastados al cierre del Capstone |
| Municipios bajo el piso de 60% | Municipios con índice 2023 mayor a 211 cuyo IC 95% excluye 211 | Algún municipio marcado sin IC |
| Tablero | Vistas publicadas; trazabilidad de los criterios de cada alerta | Alguna vista o alerta sin su razón o sin advertencia de uso |

El umbral de 211 sale de 127 / 0,6. Supone que en 2015 el avalúo estaba al 100% del valor comercial y que después solo subió por el reajuste (127 en 2023 con 3% anual): queda bajo el piso de 60% donde el índice de mercado supera 211. Con los decretos reales el reajuste del AMB llega a 128,3 (sección 5.2.4) y el umbral sería 214; el Capstone lo fija con los decretos de cada año.

**Requerimientos (modelo Kano).** Los requerimientos se clasificaron con el modelo Kano y se priorizaron con una matriz de viabilidad por impacto (score de 1 a 100). La clase Kano define qué es obligatorio y el score ordena dentro de cada clase. La Tabla 5 muestra los requerimientos a **potenciar** (básicos, unidimensionales y atractivos) y a **disminuir**; se **mantiene** como restricción no automatizar cambios de avalúo (inverso) y se **ignora** la personalización visual (indiferente). Cada uno tiene el indicador con el que se verificará al cierre del Capstone.

Table: Tabla 5. Requerimientos priorizados, objetivo de análisis e indicador de cierre (detalle en el anexo de la Guía 2).

| ID | Requerimiento | Kano | Score | OA | Indicador de cierre |
|----|-----------------|--------|------|-----|----------------------------------------|
| R1 | Calidad y trazabilidad | Básico | 90 | OA1 | 100% de variables y fuentes en el diccionario; 100% de exclusiones con regla |
| R2 | Segmentación urbano-rural | Básico | 81 | OA1 | 100% de los pares con zona; los que no la tienen, aparte |
| R3 | Índices por ventas repetidas | Básico | 80 | OA3 | Índice 2015-2023 con IC 95% en cada municipio con 30 pares y 5 por año |
| R10 | Contraste del Art. 49 | Básico | 60 | OA5 | 143 municipios contrastados ("coherente" o "revisar", con su razón) |
| R4 | Precisión | Unidim. | 70 | OA4 | MdAPE de 16,5% o menos en reventas de prueba (hoy 18,3%) |
| R5 | Cobertura | Unidim. | 63 | OA3 | 340 municipios urbanos y 324 rurales con índice propio |
| R6 | Detección de anomalías | Unidim. | 63 | OA6 | AUC mayor que 0,757; cupo de 2% de las reventas |
| R7 | Alertas de rezago (piso de 60%) | Unidim. | 72 | OA5 | Municipios con índice 2023 mayor a 211 identificados con IC 95% |
| R9 | Clasificar escrituras | Unidim. | 70 | OA2 | Mejora del MdAPE con IC 95% que excluya 0 |
| R8 | Tablero | Atractivo | 64 | No aplica | Cinco vistas, todas con advertencias de uso |
| A1 | Registros inválidos en el índice | Disminuir | 90 | OA1 | 0 pares con fecha inválida, varios predios o valor ≤ COP 1 M |
| A4 | Automatización sin validación | Disminuir | 81 | No aplica | 0 modificaciones automáticas; cada salida rotulada como señal |
| A2 | Distorsión por escrituras por avalúo | Disminuir | 70 | OA2 | Banda del índice urbano 2023 más angosta que 153-250 |
| A3 | Dependencia de análisis manuales | Disminuir | 56 | OA1 | 100% del análisis reproducible con un script |
| A5 | Funcionalidades no esenciales | Disminuir | 45 | No aplica | Tablero dentro de las 24 horas planeadas (±15%) |

R9 y R10 se agregaron en una segunda iteración, al contrastar la primera clasificación con documentos oficiales: el documento metodológico del Art. 49 (IGAC, 2024a) ajusta las transacciones de la SNR porque las considera por debajo del valor comercial, y la Resolución 2057 debe contrastarse con el mercado. R10 es básico aunque tenga el score más bajo, porque sin él no se responde la pregunta del Art. 49; su baja viabilidad lo convierte en el principal riesgo del plan. Los *key drivers* son R1, R2, R3 y R9, que habilita a R3, R4 y R6. Sin contacto directo con el IGAC, la clasificación se sustenta en documentos públicos y se validará con un panel (sección 5.4).

**Enunciado.** Construir, con las compraventas repetidas del Registro de Transacciones Inmobiliarias del IGAC 2015-2023 (IGAC, 2026a), un índice de precios de mercado por municipio, en zona urbana y rural, clasificando antes con aprendizaje supervisado las escrituras declaradas por el avalúo. Con el índice se mide la brecha entre avalúo y mercado, se prioriza dónde actualizar o revisar, se contrasta el ajuste del Art. 49 y se señalan operaciones atípicas. Responde tres preguntas: ¿cuánto se separó el avalúo del mercado en cada municipio?, ¿coincide el aumento del Art. 49 con las ventas? y ¿qué operaciones son atípicas y deben revisarse?

**Por qué ventas repetidas y por qué clasificar escrituras.** El registro no trae área, estrato, zona homogénea ni número catastral, así que un modelo hedónico no es defendible; comparar cada inmueble consigo mismo sí lo es (Bailey et al., 1963; Case y Shiller, 1987), y es el método del IPVU del Banco de la República. A nivel nacional hay 256.973 pares utilizables (183.439 urbanos y 71.004 rurales), pero solo 15% de las compraventas de un predio con valor tiene una venta anterior: por eso el producto decide por municipio y no estima el valor de cada predio. Además, 41% de las reventas crece entre 0% y 5% anual, igual que el reajuste, y esa proporción cayó de 50% en 2018 a 31% en 2019, cuando la Ley 1943 de 2018 exigió declarar el precio real. Una parte del registro reproduce el rezago: si se indexa sin separarla, el índice mide el avalúo y no el mercado. Por eso el índice urbano queda hoy entre dos cotas: en 2023 un inmueble que valía 100 en 2015 se vendía entre 153 y 250, frente a 127 del avalúo reajustado (Figura 2).

![Figura 2. Índice de mercado urbano (mediana de 136 municipios) entre sus dos cotas, frente al avalúo sin actualizar (Guía 1).](img/banda_nacional.png){width=82%}

**Objetivos de análisis.** El objetivo general se descompone en seis objetivos en cascada, cada uno ligado a requerimientos y métricas (Tabla 6).

Table: Tabla 6. Objetivos de análisis, técnica candidata y acción que habilitan.

| OA | Objetivo | Técnica candidata | Acción que habilita |
|-----|------------------------------|--------------------------------|----------------------------|
| OA1 | Preparar la base: depurar compraventas y actos del folio, formar pares, diccionario | Reglas de calidad con umbrales; análisis exploratorio | Informe de calidad; análisis reproducible |
| OA2 | Clasificar cada escritura: refleja el mercado o sigue el avalúo | Regresión logística y árboles potenciados con etiquetas débiles | Excluir o ponderar escrituras por avalúo |
| OA3 | Índice de mercado por municipio, urbano y rural | Ventas repetidas robustas y por mínimos cuadrados; jerárquico por departamento | Medida común también donde no existe ninguna oficial |
| OA4 | Estimar el valor de una reventa mejor que el reajuste | Venta anterior por el índice, ajustada con OA2 | Demostrar que el índice mide el mercado |
| OA5 | Brecha, ranking y contraste del Art. 49 | Reglas de decisión auditables | Priorizar; sustentar o corregir el ajuste |
| OA6 | Detectar operaciones atípicas | Desviación frente al índice; anomalías inyectadas | Revisión por analistas del OIC |

**Línea base y metas.** Todas las metas parten de una línea base medida sobre 56.994 reventas de prueba, sin filtrar por el valor que se predice (Tabla 7). La regla del reajuste gana a los índices porque 36,9% de las reventas crece como el avalúo: ahí falla 3,5%, frente a 7,2% del índice; en el resto falla 43,6% y el índice 38,3%. Si se conociera de antemano el tipo de escritura el error bajaría a 14,8%; la meta pide capturar la mitad de esa mejora con variables conocidas antes de la venta. Una mejora cuenta solo si el IC 95% de la diferencia excluye el cero.

Table: Tabla 7. Línea base y metas técnicas y de negocio.

| Métrica | Línea base | Meta |
|------------------------------|----------------------------------------|------------------------------|
| MdAPE al estimar una reventa | 18,3% regla del reajuste (IC 95%: 18,0-18,8); sin ajuste 23,4%; índice robusto 20,6% | 16,5% o menos, mejora con IC 95% que excluya 0 |
| AUC de anomalías inyectadas (×2 y ×0,5) | 0,745 regla; 0,757 índice robusto | Mayor que 0,757, con IC de la mejora que excluya 0 |
| Municipios con índice propio (urbano / rural) | 53 / 0 | 340 / 324; IC del índice de ±10% o menos |
| Municipios del Art. 49 con contraste | 0 | 143 |
| Municipios bajo el piso de 60% | 49 urbanos y 53 rurales, sin IC | Todos identificados con IC 95% |
| Proceso: hitos / horas | Seguimiento semanal desde S3 | 90% o más a tiempo / desviación ±15% |
| Subjetiva: utilidad de la priorización (panel, 1 a 5) | Sin medir | 4 o más |

**Técnicas candidatas para clasificar escrituras.** La regla del reajuste es el benchmark (MdAPE de 18,3%; gana al coincidir con 36,9% de las reventas, pero no distingue el tipo de escritura). La regresión logística es la línea base interpretable y barata; los árboles potenciados capturan no linealidades e interacciones, pero son menos interpretables y más sensibles a etiquetas débiles. Criterios de selección: mejora del MdAPE con IC 95% que excluya 0, capacidad de explicar los factores asociados a las diferencias, viabilidad en computadores personales y estabilidad frente a etiquetas débiles; si el complejo no supera con claridad al simple, se elige el simple.

#### 5.2.2 Riesgos del proyecto (Guía 3)

Los riesgos se identificaron con una estructura de desglose de riesgos (RBS; Hillson, 2002) de tres niveles: cinco ramas (datos, técnico-analítico, gestión del proyecto, cliente y *stakeholders*, externo), 12 categorías y 21 factores propios del proyecto. Cada factor se evaluó con un AMEF en escala de 1 a 10 (RPN = severidad × ocurrencia × detección): 9 riesgos son altos (RPN de 200 o más), 7 medios y 5 bajos. El orden coincide con el de una matriz de probabilidad por impacto: los cinco mayores RPN son también los cinco primeros de la matriz. Datos y técnico-analítico suman 62% del RPN total, por lo que ahí se concentran las acciones (Tabla 9; AMEF completo en el anexo de la Guía 3).

Table: Tabla 8. Estructura de desglose de riesgos (RBS) y concentración del RPN por rama (Guía 3).

| Rama (nivel 1) | Categorías (nivel 2) | Factores | RPN total | RPN promedio | % del RPN |
|---------------|----------------------------------------------|------|------|------|------|
| 1. Datos | Valor registrado; cobertura y calidad del registro; fuentes y acceso | 6 | 1.272 | 212 | 34% |
| 2. Técnico-analítico | Clasificación de escrituras; evaluación de los modelos; validación | 5 | 1.063 | 213 | 28% |
| 3. Gestión del proyecto | Cronograma y horas; equipo y coordinación | 4 | 439 | 110 | 12% |
| 4. Cliente y *stakeholders* | Validación con el cliente; uso y adopción | 3 | 672 | 224 | 18% |
| 5. Externo | Normativo y judicial; político e institucional | 3 | 318 | 106 | 8% |
| **Total** | 12 categorías | **21** | **3.764** | **179** | **100%** |

Escalas del AMEF (1 a 10): la severidad va de "sin efecto en los requerimientos" (1-2) a "deja sin cumplir un requerimiento básico o la pregunta de negocio" (9-10); la ocurrencia, de "remota" a "casi segura"; la detección, de "un control automático lo detecta de inmediato" a "no existe control". Un riesgo es alto con RPN de 200 o más y medio con 100 o más, y la atención es obligatoria si la severidad es 9 o más. Cliente y *stakeholders* tiene el mayor RPN promedio porque depende de un cliente sin contacto directo.

Table: Tabla 9. Riesgos altos (RPN de 200 o más), acción y momento en el plan del Capstone.

| Factor de riesgo (RBS) | RPN | Acción incorporada al plan | Etapa |
|----------------------------------|------|------------------------------------------------|----------|
| 1.1.1 Escrituras declaradas por el avalúo; quiebre de 2019 | 360 | Ponderar pares por la probabilidad de OA2; variable de periodo; validar con IVP e IPVN | C3-C6 |
| 4.1.1 Requerimientos y resultados sin validar con el IGAC | 336 | Panel de 3 a 5 evaluadores (asesor, profesores de la MIAD y profesionales de catastro) y documentos públicos; ajustes registrados en C1 | C1, C8 |
| 1.2.3 Índice municipal frente a aumentos fijados por zona | 294 | Dispersión entre zonas (p25-p75) y regla de 3 veces la mediana; marcar "revisar" | C3-C6 |
| 2.1.1 Ruido en etiquetas débiles (pares mixtos) | 288 | Etiqueta por escritura con folios de 3 ventas; etiquetas ponderadas por confianza | C3-C6 |
| 1.3.1 Año de la última actualización sin consolidar | 252 | Relación implícita de la Res. 2057 como insumo principal, con el año acotado (2017 o antes); la falta del año exacto se reporta como limitación | C2-C6 |
| 2.2.1 Fuga de información en la evaluación | 240 | Partición por folio; auditoría de variables; validación temporal | C3-C6 |
| 2.2.2 Anomalías inyectadas poco realistas | 216 | Tipos realistas (valor al avalúo, simbólicos, ×1,5 y ×0,7); revisar 50 alertas | C4-C6 |
| 4.2.2 El IGAC no puede operar el producto | 216 | Herramienta sin licencias (decisión en C1); manual y script de actualización anual | C1, C8 |
| 1.2.2 Errores de digitación y cambios físicos leídos como cambios de precio | 210 | Depurar con los actos del folio (156 pares con cambio físico); excluir del índice los cambios de 5 veces o más (335 pares) y conservarlos para OA6 | C2-C3 |

#### 5.2.3 Cronograma y recursos ajustados (Guía 5, Parte II)

**Ejecución del anteproyecto frente al plan.** El cronograma de la carta (Guía 1) asignó 79 horas a S1-S3 y 113 a S4-S8. Todas las entregas del curso se hicieron en su semana; dentro de ellas se reubicaron tres tareas técnicas (calidad del AMB, diccionario y contraste en Santander) y cambió el método del contraste del Art. 49 (Tabla 10).

Table: Tabla 10. Plan y ejecución del anteproyecto (S1-S8).

| Semanas | Plan de la carta | Ejecución | Ajuste |
|----------|------------------------------|------------------------------|------------------------|
| S1-S3 | Caso, ideación, jerarquización, carta y anexo; requerimientos, fuentes y estado del arte; inicio de vigencias de Santander | Guía 1 entregada y revisada con la retroalimentación (24 oct); Guía 2 entregada | Se agregaron R9 y R10 |
| S4 | Calidad, piloto de depuración en el AMB, diccionario y video | Guía 3 (RBS, AMEF) y video de avance | Diccionario completado en S8 |
| S5-S6 | Análisis exploratorio, índices piloto, sensibilidad y contraste en Santander | Guía 4: calidad, limpieza y entendimiento del AMB | El contraste en Santander pasó a S7 |
| S7 | Propuesta de modelos | Ampliación a Santander y Guía 5 (Parte I) | Año de última actualización reemplazado por la relación implícita de la Res. 2057 |
| S8 | Cierre: documento final | Documento final y repositorio | Sin ajuste |

**Cronograma ajustado.** Se mantienen las 16 semanas y las 192 horas del Capstone (incluidas 8 de contingencia), pero el cronograma de la carta se ajustó para reflejar las dependencias técnicas entre objetivos: datos antes de modelación, índice sobre escrituras ya clasificadas y alertas medidas contra el índice depurado (Tabla 11 y Figura 3).

Table: Tabla 11. Cronograma del Capstone por fase.

| Fase | Semanas | Horas | Actividades principales | Responsable | Hito |
|--------------|--------|------|----------------------------------------|---------------|-----------------|
| Planificación | C1 | 23 | Ajustar metas, dependencias, alcance y criterios de aceptación con el panel; elegir herramienta de tablero | Nicolás Santos | Plan del Capstone |
| Datos (OA1) | C2-C3 | 40 | Actos del folio en el país, calidad y variables previas a la venta | Cristian Ortiz | Base depurada |
| Modelación (OA2-OA6) | C3-C6 | 64 | Clasificar escrituras, índices y reventas, priorizar y detectar anomalías | Daniel Aguirre | Modelos validados |
| Tablero | C5-C7 | 24 | Cinco vistas con indicadores y advertencias de uso | Dayan Hincapie | Tablero de prueba |
| Monitoreo y control | C1-C8 | 8 | Seguimiento semanal de hitos, horas, métricas y riesgos | Nicolás Santos | Informe de validación |
| Cierre | C7-C8 | 33 | Documentación, validación con el panel, capacitación y entrega | Dayan Hincapie | Producto y documento final |
| **Total** | **8 semanas** | **192** | | | |

![Figura 3. Diagrama de Gantt del Capstone; las barras indican semanas de ejecución, no horas por semana.](img/gantt_capstone.png){width=95%}

**Riesgos y recursos.** Se mantienen los recursos previstos: cuatro integrantes con un responsable por proceso, cerca de 6 horas semanales por persona, datos públicos, Python y Git, COP 0 de desembolso y COP 11.520.000 de costo de oportunidad en el Capstone. Las acciones de los riesgos de mayor RPN quedaron dentro del cronograma (Tabla 9): no requieren recursos adicionales, sino validaciones por folio, evaluación temporal, intervalos de confianza y revisión del panel antes de presentar resultados.

#### 5.2.4 Datos: fuentes, calidad, limpieza y entendimiento (Guías 2 y 4)

**Fuentes y transformaciones.** Casi todo existe y es público; se generan dos insumos (Tabla 12). No se requiere encuesta para el modelo; el cuestionario Kano es solo para validar requerimientos. El avalúo de cada predio no se puede unir con las ventas (los catastros abiertos no traen matrícula), por lo que el índice se compara con el reajuste por decreto.

Table: Tabla 12. Fuentes, tipo de dato, estado y uso (Guías 1 y 2).

| Fuente | Tipo | Estado | Uso |
|-----------------------|--------------|------------|------------------------------|
| Registro de Transacciones IGAC 2015-2023 (IGAC, 2026a) y actos del folio | Estructurado transaccional, API Socrata | Existe | Base del índice, línea base y alertas; actos para depurar cambios físicos y crear variables de OA2 |
| Resolución 2057 de 2025 (IGAC, 2025) | PDF por zona homogénea | Existe; 7.484 zonas extraídas | Aumento por contrastar (Art. 49) |
| Memorias técnicas del Art. 49 (Santander) y actos de revisión de la Res. 0384 (IGAC, 2026c; Norte de Santander, opcionales) | PDF por municipio | Existe; disperso | Avalúo vigente y valor comercial propuesto; año de actualización acotado (2017 o antes), porque ninguna memoria lo declara |
| IVP (DANE, 2016-2024), IPVN (DANE, 2017-2024) e IPVU (Banco de la República, s.f.) | Series de tiempo | Existe | Validación externa del índice urbano |
| Gestores catastrales (IGAC, 2026b), DIVIPOLA, decretos de reajuste | Catálogos y normas | Existe | Municipios con el IGAC como gestor; reajuste de cerca de 3% |
| Etiqueta de tipo de escritura | Derivado | Se genera | Etiqueta débil de OA2 |

Los umbrales de las transformaciones se fijaron con una razón explícita y una prueba de sensibilidad (Tabla 13).

Table: Tabla 13. Umbrales de los datos y su justificación (Guía 1).

| Umbral | Razón | Verificación |
|--------------------|--------------------------------------|---------------------|
| Solo escrituras de un predio | Una escritura con varios predios trae un precio global | 30.821 casos en el AMB (Guía 4) |
| Valor mayor que COP 1 M | Valores menores son errores o actos simbólicos | 770 casos en el AMB (Guía 4) |
| Al menos 365 días entre ventas | Las reventas rápidas mezclan errores y operaciones atípicas | Sensibilidad con 180 días |
| Cambio menor a 5 veces, solo para el índice | Cambios mayores suelen ser errores o cambios físicos; la evaluación usa todas las reventas | Sensibilidad con 3 y 10 veces |
| Índice propio: 30 pares y 5 por año | Sin pares en un año, su nivel no está identificado | Ancho del IC (meta ±10%); si no, índice departamental |
| Cupo de alertas de 2% (unas 960 al año) | Carga que un equipo pequeño puede revisar (cerca de 4 por día hábil) | Sensibilidad con 1% y 5% |

**¿La organización apoyará la solución?** Sí, por mandato: el OIC debe monitorear el mercado y alertar sobre comportamientos atípicos, y la metodología del Art. 49 (IGAC, 2024b) ya usa transacciones de la SNR y modelos estadísticos. El limitante es que no hay contacto directo con el IGAC, que tiene nueva dirección y un gobierno crítico del ajuste; por eso el producto se presenta como una medición neutral frente a la regla y no como un dictamen.

**Calidad.** Se evaluaron las 165.517 compraventas del AMB 2015-2023 (Bucaramanga, Floridablanca, Girón y Piedecuesta), el territorio piloto de la limpieza. Los campos del modelo (folio, fecha, municipio y valor) están completos al 100%, sin filas ni claves registrales repetidas. Los problemas son de **granularidad, estandarización y codificación**, como anticipa la lista de chequeo: la unidad es la anotación en un folio y no el inmueble ni la escritura (una escritura con varios folios trae un precio global); la fecha viene en dos formatos (19% en dd/mm/aa); los identificadores catastrales están vacíos en el 100% (el avalúo de cada predio no se puede unir, así que el rezago se mide contra el reajuste por decreto); y la notaría cambia de formato a mitad de la serie, por lo que se descarta.

Table: Tabla 14. Síntesis de la calidad de los datos y concordancia con el problema de negocio (Guía 4).

| Criterio | Hallazgo en la base original | Concordancia con el problema |
|------------|----------------------------------------|----------------------------------|
| Totalidad | Folio, fecha, municipio y valor completos al 100%; vacíos en numero_catastral (100%), folios_derivados (99,99%) y fecha_apertura (80,93%) | Se pueden formar pares (R3); el avalúo por predio no se une: el rezago se mide contra el reajuste |
| Consistencia | Sin filas, pk ni claves registrales repetidas; 164 valores en cero y extremos de hasta COP 143.246 M | Base trazable (R1); ceros, extremos y ventas anotadas dos veces se tratan en la limpieza |
| Claridad (granularidad) | 139.909 inmuebles; 19.086 con ventas en distintos años (13,6%); el valor es el declarado | Hay candidatos a ventas repetidas, pero hay que depurar (OA1) y clasificar escrituras (OA2) |
| Formato | CSV de 26 variables; fecha en dos formatos (19% dd/mm/aa) | Las fechas se unifican para calcular días entre ventas |
| Edad y accesibilidad | 2015-2023; datos abiertos con origen en la SNR | Nueve años de valorización; reproducible sin costo |

**Limpieza.** Se elimina por regla, no por vacío; el valor no se imputa porque es la variable que se mide, y los extremos se marcan para el detector de anomalías en lugar de borrarse (Tabla 16). Los cambios físicos entre dos ventas se depuraron con los 76.065 actos de los 13.129 folios con pares, descargados de la API: en esos pares el precio se multiplica por 3,22 (mediana), frente a 1,10 en el resto.

Table: Tabla 15. Causas de limpieza identificadas (puntos a-d de la Guía 4) y decisión.

| Punto | Hallazgo en el AMB | Registros | Decisión |
|-------------|----------------------------------------|----------|--------------------|
| a. Rango válido | Valor 0, menor a COP 1 M o exactamente 1 M | 770 | Eliminar |
| a. Rango del par | Ventas del mismo folio con menos de un año | 5.203 pares | Excluir del índice |
| b. Formato | Fecha en dos formatos | 31.569 | Unificar; ninguna inválida |
| b. Categoría vacía | Zona SIN INFORMACION | 1.855 | Recuperar de otra venta del folio (52); el resto, categoría propia |
| c. Extremos | Sobre el percentil 99,5 (COP 1.050 M); cola de COP 1 a 10 M | 663; 5.806 | Marcar, no eliminar (insumo de OA6) |
| c. Cambio extremo en el par | Precio por 5 o más, o dividido por 5, sin cambio físico | 335 pares | Excluir del índice; conservar para OA6 |
| d. Interrelaciones | Escrituras de varios predios (precio global; mediana COP 30,6 M frente a 97 M) | 30.821 | Eliminar |
| d. Duplicados | Más de un valor en la anotación; mismo folio y fecha con igual valor (queda una) o distinto (salen ambas) | 4 + 112 + 90 | Eliminar / dejar una / eliminar ambas |
| d. Cambio físico | Construcción, área, división, englobe, loteo o PH entre ventas (precio por 3,22) | 156 pares | Excluir del índice |

La imputación por regresión no se aplica al valor, porque es la variable que se mide e imputarla fabricaría el precio; tampoco hace falta, porque lo eliminado no se concentra en un año (de 14,9% en 2019 a 21,0% en 2015). La imputación aleatoria se descarta porque introduce variación que no viene del mercado.

Table: Tabla 16. Embudo de limpieza y formación de pares, AMB 2015-2023.

| Paso | Quedan | Salen |
|----------------------------------------------------------------|------------------|------------------|
| Compraventas registradas (código 125), fecha unificada | 165.517 | 0 |
| Valor mayor que COP 1 M | 164.747 | 770 |
| Un solo valor en la anotación; sin duplicados de folio y fecha | 164.541 | 206 |
| Escritura de un solo predio: **compraventas limpias** | 133.720 (80,8%) | 30.821 |
| Pares consecutivos del mismo folio con al menos 365 días | 14.469 | No aplica |
| Sin cambio físico ni cambio de precio de 5 veces o más: **pares para el índice** | 13.978 | 491 (marcados para OA6) |

**Entendimiento.** Se aplicaron siete de las nueve técnicas de la guía y la agrupación de la novena (INFORMS, 2014), cada una justificada frente al problema (Tabla 17). Cuatro hallazgos orientan el modelo.

Table: Tabla 17. Selección de técnicas de entendimiento de los datos (Guía 4).

| Técnica | ¿Se usa? | Por qué, frente al problema | Resultado |
|----------------|------------|----------------------------------|---------------------|
| 1. Filtración | Sí | El índice solo admite pares comparables; cada análisis declara su subconjunto sin borrar | 13.978 pares; tres periodos frente a 2019 |
| 2. Imputación | No | Los campos del modelo están completos; imputar el valor fabricaría el precio | No aplica |
| 3. Reducción de dimensiones | Sí, por selección | La base limpia tiene 25 columnas (26 originales, menos 4 vacías y más 3 derivadas); 7 son constantes y 4 repiten información; con una sola variable numérica un ACP no aporta | De 25 a 14 columnas |
| 4. Extracción de variables | Sí | El registro no dice si el valor es precio o avalúo; hay que construir indicios | 11 variables (tasa anual, valor redondo, réplica del decreto) |
| 5. Estadísticas básicas | Sí | Nivel, dispersión y forma del valor por municipio, zona y año | Mediana COP 98 M; asimetría 161 (-0,7 en logaritmo) |
| 6. Adición de información | Sí | El rezago se define frente a reglas externas | Decretos de reajuste, Ley 1943 y actualización de Bucaramanga |
| 7. Segmentación | Sí | Separar pares de mercado de pares de avalúo con reglas explicables | 5 segmentos; 52,4% en patrón de avalúo |
| 8. Variables más importantes | Sí | Saber qué anticipa un precio de mercado (insumo de OA2) | Valor inicial y redondez dominan; AUC 0,68 |
| 9. Clasificación o agrupación | Agrupación sí; clasificación no | No hay etiqueta verdadera; una mezcla gaussiana muestra los grupos sin suponerlos | Grupo estable de 53% en 1,7% anual |

1. **El registro mezcla dos poblaciones.** El 52,4% de los pares limpios queda con el valor congelado, replica el reajuste o crece entre 0% y 5% al año; la variación mediana es 2,98%, casi igual al reajuste. Una mezcla gaussiana encuentra un grupo estable de 53% centrado en 1,7% anual. No es un error de dato: lo separa el clasificador (OA2), no una regla de limpieza.
2. **2019 es un quiebre.** El índice de ventas repetidas crece 2,8% anual hasta 2018 (como el decreto) y salta 13,9% en 2019 en los cuatro municipios a la vez, cuando la Ley 1943 obligó a declarar el precio real; la proporción de valores redondos sube de cerca de 48% a 66,5%. El índice debe modelar ese quiebre.
3. **Hay una primera señal de rezago, que es un piso.** Entre 2015 y 2023 el índice sube 43,2%, frente a 28,3% del avalúo reajustado (Figura 4). Como la mitad de los pares aún declara valores de avalúo, la brecha real probablemente es mayor.
4. **Las variables del registro no bastan para OA2.** Con valor inicial, redondez y años entre ventas un bosque aleatorio llega a un AUC de 0,68; hacen falta las variables del folio.

![Figura 4. Índice exploratorio de ventas repetidas del AMB frente al reajuste del avalúo (2015 = 100).](img/indice_amb.png){width=78%}

**Ampliación a Santander y al Art. 49 (Guía 5).** Para elegir los enfoques, el análisis se extendió a las 301.356 compraventas de Santander y a la Resolución 2057, con las mismas reglas de limpieza. *Datos*: en los 68 municipios del Art. 49 un tercio de las compraventas no trae valor (32,8%) y 27,6% trae el documento sin número de escritura; quedan 5.016 pares para el índice, la mitad de los municipios tiene 8 pares rurales o menos y solo 15 tienen índice rural propio. *Patrón de avalúo*: lo sigue el 41,3% de los pares rurales del Art. 49 (52,4% en el AMB). La hipoteca del mismo día, la variable del folio más útil, está en 31,9% de las compraventas del AMB pero solo en 2,9% de las rurales del Art. 49. *Clasificador*: en el AMB, agregar las variables del folio sube el AUC de 0,676 a 0,734 (mejora de 0,058, IC 95%: 0,047 a 0,070; 0,750 con partición por folio). *Quiebre de 2019*: el índice salta entre 11,5% y 22,9% en los grupos del AMB y del Art. 49. *Validación externa*: el índice urbano de Bucaramanga y del AMB acumula en 2015-2023 lo mismo que el IVP y el IPVN de Bucaramanga (a menos de 3,5 puntos), pero esos índices no muestran el salto de 2019 (4,5% y 1,4%): el salto es del registro, no del mercado. *Art. 49*: ninguna de las 68 memorias técnicas declara el año de la última actualización; todas permiten acotarlo a 2017 o antes. Por eso se usó la Resolución 2057 para calcular la relación implícita entre avalúo vigente y valor comercial: mediana de 9,9% en las 1.014 zonas de Santander con aumento distinto de 4%. 215 zonas (en 61 de 68 municipios) superan 3 veces la mediana de aumento de su municipio. En 14 de los 15 municipios con índice rural el mercado creció más que el reajuste (mediana 1,45 veces), pero el aumento aprobado no se relaciona con esa brecha (Spearman de -0,19): el contraste debe hacerse municipio por municipio y con reglas, no con una correlación.

![Figura 5. Aumento de la Resolución 2057 por zona en Santander (izquierda) e índice rural 2023 frente al aumento mediano en los 15 municipios con índice propio; la línea punteada es el reajuste por decreto (derecha).](img/res2057_santander.png){width=95%}

**Coherencia con el problema.** Los datos sirven para medir el rezago con dos condiciones: separar antes las escrituras declaradas por el avalúo y tratar 2019 como un quiebre. Son las dos decisiones que llevan a la elección de enfoques de la sección 5.3. El diccionario de variables (45 variables, con origen, tipo, vacíos y uso) y los scripts que reproducen todas las cifras están en el repositorio.

### 5.3 Fase de configuración y construcción: ejecución (Guía 5)

**Elección de enfoques.** El problema exige los cuatro enfoques, y los datos confirmaron cada uno y cambiaron cómo se aplica (Tabla 18).

Table: Tabla 18. Enfoques, pregunta que responden y evidencia de los datos que los justifica.

| Enfoque | Pregunta | OA | Evidencia de los datos |
|-----------|--------------------------|--------|-------------------------------------------------------|
| Descriptivo | ¿Cuánto se separó el avalúo del mercado en cada municipio, urbano y rural? | OA1, OA3 | Sin área ni estrato, pero con ventas repetidas: 13.978 pares en el AMB y 5.016 en los 68 municipios del Art. 49 de Santander. Con pocos pares rurales, el índice debe ser jerárquico |
| Diagnóstico | ¿Por qué el valor registrado no siempre refleja el precio? | OA4 | 52,4% de los pares del AMB y 41,3% de los rurales del Art. 49 siguen un patrón de avalúo; el salto de 2019 no aparece en el IVP ni el IPVN: apunta a la Ley 1943, no al mercado |
| Predictivo | ¿Qué escrituras siguen al avalúo? ¿Cuánto valdría una reventa? ¿Qué operaciones son atípicas? | OA2, OA4, OA6 | AUC de 0,73 a 0,75 con variables del folio; 480 pares en los grupos extremos de la mezcla gaussiana |
| Prescriptivo | ¿Dónde actualizar o revisar primero? ¿El Art. 49 es coherente con el mercado? | OA5 | Relación implícita de 9,9%; 215 zonas sobre 3 veces la mediana de su municipio |

El componente prescriptivo usa **reglas de decisión y no optimización**: el costo de actualizar cada municipio, que exigiría una asignación con presupuesto, no es público. Las reglas (brecha frente al reajuste, piso legal de 60%, consistencia entre zonas y entre aumento y mercado) usan solo datos públicos y se pueden explicar a quien decide.

**Selección de métodos.** Los métodos se eligen por seis factores: precisión de los datos frente a la del modelo, relevancia frente a la pregunta, disponibilidad y nivel de agregación de los datos, tiempo y personal (INFORMS, 2014, pp. 55-56). Tres pesan en todos: la decisión es por municipio y zona, no por predio; el registro no permite estimar cada predio; y el tiempo del Capstone favorece métodos libres, reproducibles con un script y explicables (Tabla 19).

Table: Tabla 19. Métodos por objetivo, justificación y alternativa descartada.

| OA | Método | Por qué | Alternativa descartada |
|-----|--------------------------------------|--------------------------------|-------------------------|
| OA1 | Reglas de calidad con umbrales; segmentación por reglas y mezcla gaussiana | Disponibilidad: un tercio de las compraventas del Art. 49 no trae valor; las reglas se explican | Imputar el valor: fabricaría el dato que se mide |
| OA2 | Regresión logística (línea base) y árboles potenciados con etiquetas débiles; versión para OA4 sin variables derivadas del valor | La clase es de cada escritura y no hay etiqueta confirmada; el complejo se adopta solo si mejora con claridad (Zilli et al., 2024) | Filtrar por crecimiento de 0% a 5%: deja pares mixtos |
| OA3 | Ventas repetidas robustas y por mínimos cuadrados, con quiebre en 2019, ponderación por OA2, versión jerárquica por departamento y ruralidad (Francke y van de Minne, 2017) e IC | Sin atributos, comparar cada predio consigo mismo es lo único defendible; con pocos pares hay que compartir información | Hedónico: exige atributos que no hay |
| OA4 | Venta anterior llevada por el índice y ajustada con OA2; factores asociados al error | Mide si el índice depurado describe el mercado mejor que el reajuste | Estimar ventas sin antecedente |
| OA5 | Reglas: cociente índice/reajuste, piso de 60%, relación implícita, dispersión entre zonas, regla de 3 veces la mediana | La pregunta es de priorización; reglas auditables | Optimización: falta el costo por municipio |
| OA6 | Desviación de cada reventa frente al índice, cupo de 2%, comparada con líneas base (Han et al., 2022) | Sin etiquetas de fraude, no supervisado y evaluado con anomalías inyectadas | Clasificación supervisada de fraude |

**Construcción y evaluación del modelo.** La ejecución es en cascada: OA1, OA2, luego OA3 y OA4, y al final OA5 y OA6.

1. *División de los datos.* Partición por inmueble: 20% de los folios va a prueba según una función fija de la matrícula, para que ningún predio esté en entrenamiento y prueba. En desarrollo (80%) se aplican el filtro de 5 veces y las etiquetas débiles; la validación cruzada de 5 grupos por folio compara candidatos y ajusta hiperparámetros; la prueba (todas las reventas con al menos un año, sin filtrar por el valor) se usa una sola vez. OA2 y OA6 se validan además en el tiempo (entrenar con 2015-2020 y probar con 2021-2023).
2. *Técnicas de evaluación.* IC 95% por *bootstrap* de folios con contraste de hipótesis sobre cada mejora; anomalías inyectadas (×2 y ×0,5, más tipos realistas) con AUC por tipo; validación externa del índice urbano contra IVP e IPVN y del contraste rural contra la Resolución 2057; revisión por el panel de 50 alertas y de las marcas "revisar".
3. *Selección del mejor modelo.* Se descarta el candidato que no pase la auditoría de fuga; en OA2 se elige por su efecto en el MdAPE de OA4 y no solo por el AUC; el modelo complejo gana solo si el IC 95% de su mejora frente al simple excluye el cero; el resultado debe confirmarse en la validación temporal; si ningún clasificador mejora la línea base, se reporta la banda entre las dos cotas.

**Métricas de la ejecución que alimentan el monitoreo.** Cada paso de la cascada produce una métrica que es insumo del monitoreo y control (sección 5.4): el AUC y el puntaje de Brier del clasificador (OA2); el ancho del IC y la diferencia con el IVP y el IPVN del índice (OA3); el MdAPE en las reventas de prueba (OA4); los municipios contrastados y marcados "revisar" (OA5); y el AUC por tipo de anomalía y la proporción de alertas que el panel considera útiles (OA6).

### 5.4 Fase de operación, optimización y despliegue: monitoreo y control (Guía 5)

**Monitoreo y control.** Las métricas de la ejecución son el insumo del monitoreo: cada una tiene línea base, meta, disparador con su acción y responsable (Tabla 20). Los umbrales son propuestas del equipo y se revisan con el panel en la primera semana del Capstone.

Table: Tabla 20. Métricas de la ejecución y su uso en monitoreo y control.

| OA | Métrica | Línea base → meta | Disparador y acción | Responsable |
|-------|----------------------|--------------------|------------------------------------|---------------|
| OA2 | AUC frente a la etiqueta débil con IC; puntaje de Brier | 0,676 sin y 0,734 con variables del folio → se acepta por su efecto en el MdAPE | AUC del año nuevo 0,05 bajo la prueba: reentrenar | Modelación |
| OA3 | Ancho del IC; diferencia con IVP e IPVN | < 3,5 puntos del IVP e IPVN (urbano) → IC ±10%; salto de 2019 corregido | IC > ±10%: índice jerárquico; > 10 puntos de diferencia: revisar la depuración | Modelación |
| OA4 | MdAPE en reventas, con IC 95% | 18,3% → 16,5% o menos | MdAPE del año nuevo sobre el IC de prueba: revisar antes de publicar | Modelación |
| OA5 | Municipios contrastados; bajo el piso con IC; marcas "revisar" | 0 → 143 contrastados | > 20% cambia de quintil: documentar; el panel confirma < 50% de marcas: ajustar reglas | Coordinación |
| OA6 | AUC con anomalías inyectadas por tipo | 0,757 → mayor, con IC que excluya 0 | El panel considera útiles < 50% de 50 alertas: ajustar cupo o regla | Modelación |
| Proceso | Hitos a tiempo; desviación de horas | Semanal → 90%; ±15% | Fuera de meta: replanificar en la reunión semanal | Coordinación |

Las herramientas de control son una **hoja maestra de cifras** generada por los scripts, de la que salen todos los documentos, con revisión cruzada antes de cada entrega; una **bitácora** de hitos y horas revisada en la reunión semanal; y el **registro de versiones** del repositorio con las métricas de cada versión. Con cada año nuevo del registro se revisan los disparadores y se ejecuta de nuevo la cascada completa. La validación con los interesados se hace con un panel de 3 a 5 evaluadores (asesor, profesores de la MIAD y profesionales de catastro u observatorios) y con documentos públicos; el panel califica de 1 a 5 la utilidad de la priorización y la claridad de las advertencias (meta: 4 o más).

**Validación de las técnicas y de los beneficios.** Las técnicas se validan con datos reservados (partición por folio y validación temporal), contra los índices oficiales y con el panel de evaluadores. Los beneficios establecidos en la carta (cobertura, contraste del Art. 49 y municipios bajo el piso de 60%) se verifican con los indicadores de cierre de la Tabla 5. Cuando un disparador se activa, la acción está definida en la Tabla 20 y la nueva versión queda registrada en el repositorio.

### 5.5 Fase de cierre (Guía 5)

**Implementación.** El producto es un tablero de cinco vistas (exploración, índice, brecha y ranking, contraste del Art. 49 y alertas) y los scripts que lo regeneran. Cada vista y cada alerta lleva la advertencia estándar: es una señal para revisar, no una irregularidad ni un dictamen sobre un avalúo o una persona. En el equipo usuario, un analista de datos ejecuta la actualización anual, un analista catastral interpreta el ranking y las alertas y decide qué revisar, y quien dirige el proceso de actualización usa el ranking para priorizar. El **entrenamiento** consiste en un manual de operación (actualizar los datos y regenerar el tablero), una guía de interpretación (qué significa cada medida y sus límites) y una demostración ante el panel. La **explotación sostenible** se garantiza con un script anual que descarga los datos nuevos, ejecuta la cascada y registra la versión, sin depender de quien lo construyó. Los **beneficios en el tiempo** se evalúan en cada actualización con las métricas de negocio (cobertura, rezago bajo el piso de 60%, contraste del Art. 49) y la calificación del panel.

**Cierre.** Al final del Capstone cada requerimiento de la Tabla 5 se marca como cumplido, cumplido en parte o no cumplido, con su razón, usando el indicador de cierre de esa tabla; la satisfacción de los interesados se mide con la calificación del panel y la proporción de alertas que considera dignas de revisión.

**Presentación de los resultados.** El documento final del Capstone presentará los resultados en estos rubros, cada uno ligado a su acción de implementación: (1) base depurada y diccionario de variables; (2) clasificador de escrituras y su efecto en el MdAPE; (3) índices municipales con IC y validación externa; (4) brecha, ranking y contraste del Art. 49, cada municipio con su razón; (5) alertas y su revisión por el panel; (6) verificación de cada requerimiento y limitaciones de uso; y (7) manual de operación y plan de actualización anual.

**Beneficios esperados.** Se mantienen los beneficios de las Guías 1 y 2: índice de mercado en 340 municipios urbanos y 324 rurales (hoy 53 y 0), contraste del Art. 49 en 143 municipios (hoy 0), municipios bajo el piso de 60% identificados con IC 95%, error de estimación de 16,5% o menos (hoy 18,3%) y alertas mejores que la mejor línea base. Los cualitativos son una priorización transparente y reproducible, evidencia pública para un ajuste en litigio y para el debate del PND 2026-2030 y del C159, reglas que habrían marcado aumentos extremos en la propia resolución (1.521 zonas con aumentos de más de 1.000%; en Santander, 215 zonas sobre 3 veces la mediana de su municipio) y un método replicable por la Red de Observatorios Inmobiliarios Catastrales. Se hacen dos precisiones a partir del anteproyecto: los beneficios se verificarán con datos reservados, intervalos de confianza y validación temporal, y donde la información no alcance (por ejemplo, municipios sin pares suficientes) se reportará la limitación y se usará la alternativa definida (índice departamental, marca "revisar" o banda entre cotas).

### 5.6 Verificación del anteproyecto y mejoras incorporadas

La Tabla 21 responde la lista de chequeo propuesta para la entrega final y registra la acción tomada en cada caso.

Table: Tabla 21. Lista de chequeo del anteproyecto.

| Dimensión | Pregunta (resumida) | Sí/No | Evidencia y acción |
|-------------|----------------------------|-----|------------------------------------------------------|
| Ideas y jerarquización | ¿La selección jerarquizó proyectos potenciales con características de Analytics? | Sí | 8 ideas, filtro de 7 características y matriz valor-capacidad; se integraron 1, 2 y 5 (sección 5.1) |
| Problema de negocio | ¿Responde a una necesidad estratégica de la que se derivan métricas? | Sí | Meta de 70% de área actualizada del PND y Art. 49; tres métricas de negocio con línea base (sección 5.1) |
| Requerimientos | ¿Están clasificados en potenciar, disminuir, mantener o ignorar? | Sí | Kano con score; 10 a potenciar, 5 a disminuir, inverso como restricción e indiferente ignorado (Tabla 5) |
| Problema de Analytics | ¿Es coherente con los requerimientos, el negocio y el enfoque? | Sí | Cada OA ligado a requerimientos y métricas (Tablas 5 y 6) y a un enfoque (Tabla 18) |
| Recolección de datos | ¿Hubo problemas de granularidad, estandarización o codificación? | Sí | Anotación por folio y escrituras de varios predios; fechas en dos formatos; identificadores catastrales vacíos y notaría inconsistente. Se resolvieron por regla (Tabla 16) |
| Preprocesamiento | ¿Reveló información que amerita iterar pasos previos? | Sí | Cuatro iteraciones: R9 y R10 agregados; clasificar escrituras y no pares; quiebre de 2019 en el índice; relación implícita de la Res. 2057, porque ninguna de las 68 memorias declara el año de última actualización |
| Proceso | ¿Se siguió el proceso y las actividades de cada guía? | Sí | Las cinco guías se desarrollaron completas; las versiones de entrega están en el repositorio |
| Proceso | ¿Se identificó qué rehacer o mejorar? | Sí | Cronograma con dependencias, metas revisables en C1, riesgos con acción en el plan |
| Productos | ¿Se realizaron todos los productos? | Sí | Carta y anexo, planteamiento, RBS y AMEF, informe de calidad, diccionario de variables (completado para esta entrega), propuesta de modelos y plan |
| Productos | ¿Se tuvieron en cuenta las dimensiones de la rúbrica? | Sí | Enfoque, método, ejecución, monitoreo y control, y cierre cubiertos en las secciones 5.3 a 5.5 |
| Retroalimentación | ¿Se revisaron los puntajes y la retroalimentación? | Sí | Guía 1: aplicada en la carta y el anexo revisados (24 oct 2026). Guía 4 (31,5 de 35): piloto en Santander y variables de OA2, atendidas en la sección 5.2.4 (mejora 6). Guías 2 y 3: sin observaciones |
| Retroalimentación | ¿Se pidió aclaración cuando hizo falta? | Sí | En clase, sobre el alcance de la entrega final (consolidar las cinco guías) |
| Retroalimentación | ¿Se planeó cómo incorporarla? | Sí | Incorporada en este documento; los umbrales se revisan con el panel en C1 |

**Mejoras incorporadas.** (0) *Retroalimentación de la Guía 1*: la carta pasó de un piloto de valoración y operaciones atípicas en el AMB para el OIC (versión del 18 de octubre) a un problema de priorización con el Art. 49 para la Dirección de Gestión Catastral, con métricas de negocio y técnicas medidas contra una línea base (MdAPE de 18,3%, AUC de 0,757), responsables por proceso y fechas reales (versión revisada del 24 de octubre); ambas versiones están en el repositorio. (1) Se unificaron las cifras de las cinco guías en un solo documento y se aclaró su base territorial: las cifras nacionales vienen de la Guía 1 y 2, las del AMB de la Guía 4 y las de Santander de la Guía 5 (el 52,4% del AMB no es comparable con el 41% nacional, que se mide sobre todas las reventas). (2) Se completó el diccionario de variables, comprometido como producto del anteproyecto. (3) Se publicó el repositorio con el código, los datos y los scripts de descarga desde la API, que reproducen las cifras de la limpieza y de la ampliación a Santander; es la fuente de documentación del proyecto. (4) Se registró como ajuste del plan el reemplazo del año de la última actualización por la relación implícita de la Resolución 2057: se leyeron las 68 memorias técnicas de Santander y ninguna declara ese año. La marca "coherente" o "revisar" se asigna con la relación implícita y el año acotado; la falta del año exacto se reporta como limitación. (5) Se conectó la tabla de riesgos del plan con los RPN del AMEF. (6) *Retroalimentación de la Guía 4* (31,5 de 35): la profesora señaló que el piloto se limitó al AMB y que faltaban las variables de OA2 de los actos del folio. El análisis se amplió a las 301.356 compraventas de Santander y a los 68 municipios del Art. 49; se perfilaron la Resolución 2057, las memorias técnicas y los índices IVP e IPVN; y se extrajeron de los 76.065 actos la hipoteca del mismo día, la propiedad horizontal y la primera venta de un folio nuevo, que suben el AUC de 0,676 a 0,734 (sección 5.2.4).

**Limitaciones.** La regla de 5% anual para separar mercado de avalúo es provisional, y el 3% de algunos decretos se asumió. El piso de 60% supone que en 2015 el avalúo estaba al 100% del valor comercial y que después solo subió por el reajuste; si estaba por debajo, el rezago es mayor y la lista es un mínimo. La etiqueta de OA2 es débil. El índice mide 2015-2023, pero el Art. 49 corrige el rezago desde la última actualización (15 a 30 años). Sin contacto directo con el IGAC, la validación descansa en el panel y en documentos públicos.

## 6. Referencias

Anagol, S., Balasubramaniam, V., Lockwood, B. B., Ramadorai, T. y Uettwiller, A. (2025). *Optimal tax policy with misreporting: Theory, and evidence from real estate* [Documento de trabajo].

Avenancio-León, C. F. y Howard, T. (2022). The assessment gap: Racial inequalities in property taxation. *The Quarterly Journal of Economics, 137*(3), 1383-1434. https://doi.org/10.1093/qje/qjac009

Bailey, M. J., Muth, R. F. y Nourse, H. O. (1963). A regression method for real estate price index construction. *Journal of the American Statistical Association, 58*(304), 933-942. https://doi.org/10.1080/01621459.1963.10480679

Banco de la República. (s.f.). *Índice de precios de la vivienda usada (IPVU): nota metodológica*. https://www.banrep.gov.co

Cámara de Representantes. (2026). *Proyecto de Ley 159 de 2026 Cámara*.

Case, K. E. y Shiller, R. J. (1987). Prices of single-family homes since 1970: New indexes for four cities. *New England Economic Review*, (septiembre-octubre), 45-56.

Decreto 148 de 2020. Por el cual se reglamentan parcialmente los artículos 79, 80, 81 y 82 de la Ley 1955 de 2019 y se modifica parcialmente el Título 2 de la Parte 2 del Libro 2 del Decreto 1170 de 2015. 4 de febrero de 2020. Diario Oficial 51.217.

Departamento Administrativo Nacional de Estadística [DANE]. (2016-2024). *Índice de Valoración Predial (IVP): boletines técnicos anuales 2016 a 2024*. https://www.dane.gov.co/files/operaciones/IVP/

Departamento Administrativo Nacional de Estadística [DANE]. (2017-2024). *Índice de Precios de la Vivienda Nueva (IPVN): boletines técnicos del IV trimestre de 2016 a 2023*. https://www.dane.gov.co/files/operaciones/IPVN/

Francke, M. K. y van de Minne, A. M. (2017). The hierarchical repeat sales model for granular commercial real estate and residential price indices. *The Journal of Real Estate Finance and Economics, 55*(4), 511-532. https://doi.org/10.1007/s11146-017-9632-4

Han, S., Hu, X., Huang, H., Jiang, M. y Zhao, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems, 35*, 32142-32159.

Hillson, D. (2002). *Use a risk breakdown structure (RBS) to understand your risks* [Ponencia]. Project Management Institute Annual Seminars & Symposium, San Antonio, TX, Estados Unidos.

IBM. (2020). *The business opportunity statement*. IBM Garage Methodology. https://www.ibm.com/garage/method

INFORMS. (2014). *Certified Analytics Professional (CAP®): Examination study guide*. Institute for Operations Research and the Management Sciences.

Instituto Geográfico Agustín Codazzi [IGAC]. (2024a). *Reducción de rezago de avalúos catastrales, artículo 49 PND 2022-2026: documento conceptual y metodológico*. Subdirección General.

Instituto Geográfico Agustín Codazzi [IGAC]. (2024b). *Resolución 1912 de 2024*.

Instituto Geográfico Agustín Codazzi [IGAC]. (2025). *Resolución 2057 de 2025* (Diario Oficial 53.354).

Instituto Geográfico Agustín Codazzi [IGAC]. (2026a). *Registro de transacciones inmobiliarias en Colombia 2015-2023* [Conjunto de datos 7y2j-43cv]. datos.gov.co. https://www.datos.gov.co/d/7y2j-43cv

Instituto Geográfico Agustín Codazzi [IGAC]. (2026b). *Gestores catastrales de Colombia* [Conjunto de datos bhcx-bx97]. datos.gov.co. https://www.datos.gov.co/d/bhcx-bx97

Instituto Geográfico Agustín Codazzi [IGAC]. (2026c). *Resolución 0384 de 2026* (Diario Oficial 53.453).

Instituto Geográfico Agustín Codazzi [IGAC]. (2026d). *IGAC da a conocer los principales resultados de su gestión 2022-2026 durante el proceso de 'empalme ante el pueblo'* [Noticia, 27 de julio de 2026]. https://www.igac.gov.co/noticias/igac-da-conocer-los-principales-resultados-de-su-gestion-2022-2026-durante-el-proceso-de-empalme-ante-el-pueblo

Ley 1943 de 2018. Por la cual se expiden normas de financiamiento para el restablecimiento del equilibrio del presupuesto general y se dictan otras disposiciones. 28 de diciembre de 2018. Diario Oficial 50.820.

Ley 2294 de 2023. Por el cual se expide el Plan Nacional de Desarrollo 2022-2026 "Colombia potencia mundial de la vida". 19 de mayo de 2023. Diario Oficial 52.400.

Pulgarín-Franco, J. A. (2024). La actualización catastral y las capacidades institucionales locales: impuesto predial y servicios públicos domiciliarios. *Bitácora Urbano Territorial, 34*(1), 97-114. https://doi.org/10.15446/bitacora.v34n1.111741

Vanguardia. (2026, 9 de octubre). *Avalúo catastral: Consejo de Estado admite demanda contra resolución del IGAC*. https://www.vanguardia.com/area-metropolitana/bucaramanga/2026/10/09/avaluo-catastral-consejo-de-estado-admite-demanda-contra-resolucion-del-igac/

Zilli, C. A., Bastos, L. C. y da Silva, L. R. (2024). Machine learning models in mass appraisal for property tax purposes: A systematic mapping study. *Aestimum, 84*, 31-52. https://doi.org/10.36253/aestim-15792

## 7. Anexos

<p style="text-align: left">Los anexos y soportes técnicos están en el repositorio público del proyecto (<a href="https://github.com/Zeal916/termometro-rezago-catastral">github.com/Zeal916/termometro-rezago-catastral</a>), en las rutas que indica la tabla; las fuentes editables y el procedimiento para reconstruir el proyecto están en <code>recuperacion/</code>. La carta del proyecto ajustada (Anexo A) se incluye además al final de este documento.</p>

| Anexo | Contenido | Ruta |
|------------|----------------------------------------------------------|------------------------------|
| A. Guía 1 | Carta del proyecto ajustada (al final de este documento; versiones de entrega en la ruta) y anexo (ideación, filtro, 5W, accesibilidad, limitantes, beneficios, criterios de éxito, cronograma) | `anexos/guia_1/` |
| B. Guía 2 | Planteamiento del problema de Analytics y anexo (Kano, recursos, fuentes, objetivos, métricas, estado del arte) | `anexos/guia_2/` |
| C. Guía 3 | RBS y AMEF completos, con plan de acciones y contraste probabilidad × impacto | `anexos/guia_3/` |
| D. Guía 4 | Informe de calidad, limpieza y entendimiento; notebooks y scripts | `anexos/guia_4/`, `anexos/codigo/guia_4/` |
| E. Guía 5 | Partes I y II en su versión de entrega | `anexos/guia_5/` |
| F. Datos y código | Análisis nacional (línea base), piloto del AMB, ampliación a Santander, variables de OA2, índices oficiales y perfil de la Res. 2057 | `anexos/codigo/`, `anexos/datos/` |
| G. Diccionario | 45 variables con origen, tipo, vacíos y uso | `anexos/diccionario_variables.md` |
| H. Cifras | Cada cifra de este documento con el archivo y la línea de resultados que la respalda | `anexos/CIFRAS.md` |
