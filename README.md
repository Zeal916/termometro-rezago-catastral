# Termómetro de rezago catastral

Anteproyecto del curso **Gerencia de Proyectos de Analytics** (Maestría en Inteligencia Analítica de Datos, Universidad de los Andes), Caso Dinámica Inmobiliaria 2026. Equipo 23: Nicolás Santos (líder y negocio), Cristian Ortiz (ingeniería y calidad de datos), Daniel Aguirre (modelación) y Dayan Hincapie (visualización y documentación). Asesor: Carlos Ramírez.

**Problema.** El IGAC debe decidir en qué municipios actualizar o revisar primero el avalúo catastral y sustentar o corregir el ajuste del Art. 49 de la Ley 2294 de 2023 (Resolución 2057 de 2025). El proyecto mide, con las ventas repetidas del Registro de Transacciones Inmobiliarias del IGAC 2015-2023 (datos.gov.co, `7y2j-43cv`), la brecha entre el avalúo y el mercado por municipio, en zona urbana y rural, después de separar las escrituras declaradas por el avalúo.

**Este repositorio es la fuente de documentación del proyecto.** Contiene el documento final, las entregas de las cinco guías con sus fuentes editables, el código, los datos del piloto, los scripts que descargan lo que no se versiona, el diccionario de variables y la hoja maestra de cifras. Si se pierde todo lo demás, el proyecto se recupera desde aquí (ver [Recuperar el proyecto](#recuperar-el-proyecto)).

**Empiece por:** [`documento/anteproyecto.pdf`](documento/anteproyecto.pdf), el documento final que consolida las cinco guías (14 páginas).

## Estructura

| Carpeta o archivo | Qué contiene |
|---|---|
| `documento/` | Documento final del anteproyecto: `anteproyecto.pdf` y `.docx` (generados), `anteproyecto.md` (fuente única del texto), `estilo.css`, `img/` y `construir.py` |
| `CIFRAS.md` | Hoja maestra de cifras: cada cifra del documento con el archivo que la produce |
| `diccionario_variables.md` / `.csv` | 45 variables (originales, de limpieza y derivadas) con origen, tipo, vacíos y uso |
| `anexos/guia_1/` | Carta del proyecto y anexo entregados. `fuente/`: HTML del anexo, carta en Excel y scripts que los generan. `version_1/`: primera versión, antes de aplicar la retroalimentación |
| `anexos/guia_2/` | Planteamiento del problema de Analytics y anexo (Kano, recursos, fuentes, objetivos, métricas, estado del arte). `fuente/`: Word y HTML |
| `anexos/guia_3/` | RBS y AMEF en PDF y Excel. `fuente/`: presentación y guion del video de avance (semana 4) |
| `anexos/guia_4/` | Informe de calidad, limpieza y entendimiento. `fuente/`: Parte II en Markdown y Word |
| `anexos/guia_5/` | Partes I y II tal como se redactaron. `fuente/`: script que genera el Word de la Parte I |
| `presentacion/` | Presentación del anteproyecto y guion del video final |
| `codigo/guia_1/` | `analisis_guia1.py`: análisis nacional (5,4 M de compraventas): línea base, índices por municipio y cruce con la Res. 2057 |
| `codigo/guia_4/` | `limpieza_amb.py`, `descarga_actos.py` y notebooks de calidad (`02_…`) y entendimiento (`03_…`) del AMB |
| `codigo/guia_5/` | Ampliación a Santander, variables del folio para OA2, contraste con IVP e IPVN, perfil de la Res. 2057 y vigencias del Art. 49. Cada script deja sus `resultados_*.txt`, CSV y figuras en la misma carpeta |
| `codigo/descarga_amb.py` | Descarga desde la API la base de compraventas del AMB y todos los actos del AMB |
| `codigo/diccionario.py` | Regenera el diccionario de variables |
| `datos/` | Compraventas del AMB 2015-2023, compraventas limpias, pares y actos de los folios (`api/`); salidas nacionales (`guia_1/`) |
| `figuras/` | Gráficas de las Guías 1, 3 y 4 |
| `notas_equipo/` | Notas de trabajo: hallazgos de la Guía 1, guion y pendientes del video, pendientes y bitácora de la limpieza de la Guía 4 |

## Cronología

| Semana | Entrega | Resultado principal | Dónde |
|---|---|---|---|
| S1-S3 (oct 2026) | Guía 1: carta del proyecto y anexo | 8 ideas, filtro y matriz valor-capacidad; problema de negocio; línea base nacional (MdAPE 18,3%, AUC 0,757). Retroalimentación aplicada el 24 oct | `anexos/guia_1/`, `codigo/guia_1/` |
| S3-S4 | Guía 2: planteamiento del problema de Analytics | Kano (R1-R10, A1-A5), objetivos OA1-OA6, fuentes, metas y estado del arte | `anexos/guia_2/` |
| S4 | Guía 3: RBS, AMEF y video de avance | 21 riesgos; 9 altos; acciones en el plan | `anexos/guia_3/` |
| S5-S6 | Guía 4: calidad, limpieza y entendimiento (AMB) | 13.978 pares; 52,4% en patrón de avalúo; quiebre de 2019 | `anexos/guia_4/`, `codigo/guia_4/` |
| S7-S8 (nov 2026) | Guía 5 y documento final | Ampliación a Santander; enfoques, métodos, evaluación, monitoreo, cierre y plan del Capstone | `anexos/guia_5/`, `codigo/guia_5/`, `documento/` |

Las Guías 2, 3 y 4 no recibieron observaciones. El Capstone (8 semanas, 192 horas) construye el producto según la sección 7 del documento.

## Recuperar el proyecto

Requisitos: Python 3.11 o superior con `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `pdfplumber`, `pymupdf` y `python-docx`; [pandoc](https://pandoc.org) y Microsoft Edge o Chrome para generar el documento. Todos los comandos se ejecutan desde la raíz del repositorio.

```bash
git clone https://github.com/Zeal916/termometro-rezago-catastral.git
cd termometro-rezago-catastral
py -m pip install pandas numpy matplotlib scikit-learn pdfplumber pymupdf python-docx
```

**1. Datos.** Lo que pesa menos de 50 MB está versionado. Lo demás se descarga de la API pública (sin credenciales):

| Archivo | Versionado | Cómo obtenerlo |
|---|---|---|
| `datos/amb_compraventas_2015_2023.csv` (165.517 filas) | Sí | `py -I codigo/descarga_amb.py compraventas` lo reconstruye idéntico (verificado el 23 nov 2026) |
| `datos/api/actos_folios_pares.csv` (76.065 actos) | Sí | `py -I codigo/guia_4/descarga_actos.py` |
| `datos/guia_5/santander_actos.csv` (737.238 actos) | No | `py -I codigo/guia_5/descarga_santander.py` |
| `datos/guia_5/amb_7y2j-43cv.csv` (1.062.263 actos) | No | `py -I codigo/descarga_amb.py actos` |
| `datos/guia_1/descarga/` (compraventas del país, ~800 MB) | No | La descarga `py -I codigo/guia_1/analisis_guia1.py` |
| `datos/guia_5/memorias_art49_santander/` (68 memorias técnicas en PDF) | No | Las descarga `py -I codigo/guia_5/vigencias_santander.py` desde `codigo/guia_5/memorias_art49_santander_enlaces.csv` |

**2. Resultados**, en este orden (cada paso usa las salidas del anterior):

```bash
py -I codigo/guia_1/analisis_guia1.py              # línea base nacional -> datos/guia_1/
py -I codigo/guia_4/limpieza_amb.py                # limpieza del AMB -> datos/compraventas_limpias.csv, datos/pares_amb.csv
py -I codigo/diccionario.py                        # diccionario de variables
py -I codigo/guia_5/entendimiento_santander.py     # ampliación a Santander (requiere santander_actos.csv)
py -I codigo/guia_5/variables_oa2_amb.py           # variables del folio para OA2 (requiere amb_7y2j-43cv.csv)
py -I codigo/guia_5/indices_oficiales_bucaramanga.py
py -I codigo/guia_5/perfil_res2057_santander.py
py -I codigo/guia_5/vigencias_santander.py
```

Los notebooks `codigo/guia_4/03_entendimiento.ipynb` y `02_entendimiento_calidad_compraventas.ipynb` se ejecutan desde su carpeta. El 02 usa la extracción original de 26 columnas, que incluye `numero_catastral` y `numero_catastral_antiguo` (vacías en el 100%); `datos/amb_compraventas_2015_2023.csv` trae las otras 24, así que con ese archivo el notebook puede requerir ajustes en las celdas que leen esas dos columnas.

Resultado esperado de la limpieza: 165.517 compraventas → 133.720 limpias (80,8%) → 14.469 pares con al menos 365 días → 13.978 pares para el índice (12.399 urbanos, 1.398 rurales, 181 sin zona). La limpieza, el perfil de la Res. 2057, el contraste con índices oficiales y las vigencias del Art. 49 se volvieron a ejecutar desde el repositorio el 23 nov 2026 y produjeron salidas idénticas; la descarga de compraventas del AMB reconstruyó el archivo versionado fila por fila. El análisis nacional, la ampliación a Santander y las variables de OA2 no se volvieron a ejecutar porque dependen de descargas grandes; sus salidas versionadas son las originales.

**3. Documento.** Se edita `documento/anteproyecto.md` y se regenera:

```bash
cd documento && py -I construir.py    # anteproyecto.html, .pdf y .docx (requiere pandoc en el PATH y Microsoft Edge)
```

Si cambia una cifra, se actualizan juntos el script, su salida, `CIFRAS.md` y el documento.

**No incluido:** las guías, el caso y las plantillas del curso son material de la Universidad de los Andes y no se publican aquí; están en la plataforma del curso (GUIA1_v5, GUIA2_v4, GUIA3_v3, GUIA4_v3, GUIA5_v2, Caso Dinámica Inmobiliaria 2026 v3, plantilla de la carta del proyecto y formatos de la Guía 3).

## Fuentes de datos

- IGAC (2026). Registro de transacciones inmobiliarias en Colombia 2015-2023 (`7y2j-43cv`) y Gestores catastrales de Colombia (`bhcx-bx97`). datos.gov.co. Datos abiertos.
- IGAC. Resoluciones 1912 de 2024, 1939 de 2025, 2057 de 2025 (`codigo/guia_5/res2057.pdf`) y 0384 de 2026; memorias técnicas del Art. 49 (enlaces en `codigo/guia_5/memorias_art49_santander_enlaces.csv`).
- DANE (IPVN, IVP; boletines en `codigo/guia_5/fuentes_indices_oficiales/`) y Banco de la República (IPVU).

## Uso responsable

Los resultados son señales para revisar, no conclusiones sobre un avalúo, un predio o una persona. El proyecto no modifica avalúos ni emite conclusiones jurídicas o de fraude.
