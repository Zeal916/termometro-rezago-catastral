# Recuperación del proyecto

Todo lo necesario para reconstruir el anteproyecto desde cero o seguir editándolo. Los anexos que se leen están en [`../anexos/`](../anexos/); aquí están las fuentes y el procedimiento.

| Carpeta o archivo | Contenido |
|---|---|
| `documento_fuente/` | Fuente única del documento final: `anteproyecto.md`, `estilo.css`, `img/` y `construir.py`, que genera `../documento/anteproyecto.pdf` y `.docx` |
| `fuentes_editables/guia_1/` | HTML del anexo, carta en Excel y scripts que los generan (`construir_carta.py`, `exportar_office.py`); `version_1/`, la primera versión antes de la retroalimentación |
| `fuentes_editables/guia_2/` | Word final del anexo y del planteamiento; HTML y estilos |
| `fuentes_editables/guia_3/` | Presentación y guion del video de avance (semana 4) |
| `fuentes_editables/guia_4/` | Parte II (limpieza) en Markdown y Word |
| `fuentes_editables/guia_5/` | Script que genera el Word de la Parte I |
| `presentacion/` | Presentación del anteproyecto y guion del video final |
| `notas_equipo/` | Notas de trabajo: hallazgos de la Guía 1, guion y pendientes del video, pendientes y bitácora de la limpieza de la Guía 4 |
| `descarga_amb.py` | Descarga desde la API la base de compraventas del AMB y todos los actos del AMB |

## Requisitos

Python 3.11 o superior con `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `pdfplumber`, `pymupdf` y `python-docx`; [pandoc](https://pandoc.org) en el PATH y Microsoft Edge para generar el documento.

```bash
git clone https://github.com/Zeal916/termometro-rezago-catastral.git
cd termometro-rezago-catastral
py -m pip install pandas numpy matplotlib scikit-learn pdfplumber pymupdf python-docx
```

## 1. Datos

Lo que pesa menos de 50 MB está versionado en `anexos/datos/`. Lo demás se descarga de la API pública, sin credenciales:

| Archivo (en `anexos/datos/`) | Versionado | Cómo obtenerlo (desde la raíz del repositorio) |
|---|---|---|
| `amb_compraventas_2015_2023.csv` (165.517 filas) | Sí | `py -I recuperacion/descarga_amb.py compraventas` lo reconstruye idéntico (verificado el 23 nov 2026) |
| `api/actos_folios_pares.csv` (76.065 actos) | Sí | `cd anexos && py -I codigo/guia_4/descarga_actos.py` |
| `guia_5/santander_actos.csv` (737.238 actos) | No | `cd anexos && py -I codigo/guia_5/descarga_santander.py` |
| `guia_5/amb_7y2j-43cv.csv` (1.062.263 actos) | No | `py -I recuperacion/descarga_amb.py actos` |
| `guia_5/memorias_art49_santander/` (68 PDF) | No | Las descarga `codigo/guia_5/vigencias_santander.py` |
| `guia_1/descarga/` (compraventas del país, ~800 MB) | No | Las descarga `codigo/guia_1/analisis_guia1.py` |

## 2. Resultados

Desde `anexos/`, en este orden (cada paso usa las salidas del anterior):

```bash
cd anexos
py -I codigo/guia_1/analisis_guia1.py              # línea base nacional -> datos/guia_1/
py -I codigo/guia_4/limpieza_amb.py                # limpieza del AMB -> datos/compraventas_limpias.csv, datos/pares_amb.csv
py -I codigo/diccionario.py                        # diccionario de variables
py -I codigo/guia_5/entendimiento_santander.py     # ampliación a Santander (requiere santander_actos.csv)
py -I codigo/guia_5/variables_oa2_amb.py           # variables del folio para OA2 (requiere amb_7y2j-43cv.csv)
py -I codigo/guia_5/indices_oficiales_bucaramanga.py
py -I codigo/guia_5/perfil_res2057_santander.py
py -I codigo/guia_5/vigencias_santander.py
```

Los notebooks de `codigo/guia_4/` se ejecutan desde su carpeta. El `02_…` usa la extracción original de 26 columnas, que incluye `numero_catastral` y `numero_catastral_antiguo` (vacías en el 100%); `datos/amb_compraventas_2015_2023.csv` trae las otras 24, así que con ese archivo el notebook puede requerir ajustes en las celdas que leen esas dos columnas.

Resultado esperado de la limpieza: 165.517 compraventas → 133.720 limpias (80,8%) → 14.469 pares con al menos 365 días → 13.978 pares para el índice (12.399 urbanos, 1.398 rurales, 181 sin zona).

**Verificado el 23 nov 2026:** la limpieza, el diccionario, el perfil de la Res. 2057, el contraste con índices oficiales y las vigencias del Art. 49 se ejecutaron desde el repositorio y produjeron salidas idénticas; la descarga de compraventas del AMB reconstruyó el archivo versionado fila por fila. El análisis nacional, la ampliación a Santander y las variables de OA2 no se volvieron a ejecutar porque dependen de descargas grandes; sus salidas versionadas son las originales.

## 3. Documento

Se edita `documento_fuente/anteproyecto.md` y se regenera:

```bash
cd recuperacion/documento_fuente && py -I construir.py    # escribe ../../documento/anteproyecto.pdf y .docx
```

El documento sigue la estructura de la guía del anteproyecto (portada, abstract, índice, introducción, estado del arte, desarrollo por fases 5.1 a 5.5, referencias y anexos). `construir.py` genera el PDF dos veces: la primera ubica la página de cada sección, tabla y figura y la segunda escribe el índice con esos números. Imprime primero en `documento_fuente/_borrador.pdf` y luego reemplaza `documento/anteproyecto.pdf`; si ese PDF está abierto en un visor, el script lo avisa y hay que cerrarlo y volver a ejecutarlo.

Si cambia una cifra, se actualizan juntos el script, su salida, `anexos/CIFRAS.md` y el documento.

## No incluido

Las guías, el caso y las plantillas del curso son material de la Universidad de los Andes y no se publican aquí; están en la plataforma del curso: GUIA1_v5, GUIA2_v4, GUIA3_v3, GUIA4_v3, GUIA5_v2, Caso Dinámica Inmobiliaria 2026 v3, plantilla de la carta del proyecto y formatos de la Guía 3.
