# Termómetro de rezago catastral

Anteproyecto del curso **Gerencia de Proyectos de Analytics** (Maestría en Inteligencia Analítica de Datos, Universidad de los Andes), Caso Dinámica Inmobiliaria 2026. Equipo 23: Nicolás Santos, Cristian Ortiz, Daniel Aguirre y Dayan Hincapie. Asesor: Carlos Ramírez.

**Problema.** El IGAC debe decidir en qué municipios actualizar o revisar primero el avalúo catastral y sustentar o corregir el ajuste del Art. 49 de la Ley 2294 de 2023 (Resolución 2057 de 2025). El proyecto propone medir, con las ventas repetidas del Registro de Transacciones Inmobiliarias del IGAC 2015-2023 (datos.gov.co, `7y2j-43cv`), la brecha entre el avalúo y el mercado por municipio, en zona urbana y rural, después de separar las escrituras declaradas por el avalúo.

Este repositorio contiene los **anexos del documento final del anteproyecto**: las entregas completas de las Guías 1 a 5, el código, los datos del piloto y el diccionario de variables.

## Contenido

| Carpeta o archivo | Qué contiene |
|---|---|
| `documento/` | Documento final del anteproyecto (consolida las cinco guías) |
| `anexos/guia_1/` | Carta del proyecto y anexo: ideación, filtro de siete características, matriz valor-capacidad, 5W, accesibilidad, limitantes, beneficios, criterios de éxito y cronograma |
| `anexos/guia_2/` | Planteamiento del problema de Analytics y anexo: modelo Kano, requerimientos R1-R10 y A1-A5, recursos, presupuesto, fuentes, objetivos OA1-OA6, métricas y estado del arte |
| `anexos/guia_3/` | RBS y AMEF (21 factores de riesgo con RPN, plan de acciones y contraste con la matriz probabilidad × impacto), en PDF y Excel |
| `anexos/guia_4/` | Informe de calidad, limpieza y entendimiento de los datos (piloto del AMB) |
| `anexos/guia_5/` | Parte I (enfoques, métodos, evaluación, monitoreo e implementación) y Parte II (cronograma, riesgos y beneficios) |
| `codigo/guia_1/` | `analisis_guia1.py`: análisis nacional (5,4 M de compraventas) que produce la línea base (MdAPE, AUC), los índices por municipio y zona, y el cruce con la Resolución 2057; salidas en `datos/guia_1/` |
| `codigo/guia_4/` | `limpieza_amb.py`, `descarga_actos.py` y los notebooks `02_entendimiento_calidad_compraventas.ipynb` y `03_entendimiento.ipynb` |
| `codigo/diccionario.py` | Genera el diccionario de variables a partir de los CSV |
| `datos/` | Compraventas del AMB 2015-2023, compraventas limpias, pares de ventas repetidas y actos de los folios (`datos/api/`) |
| `figuras/` | Gráficas de las Guías 3 y 4 |
| `diccionario_variables.md` / `.csv` | Variables originales, de limpieza y derivadas, con origen, tipo, vacíos y uso |

## Reproducción

Requiere Python 3.11 o superior con `pandas`, `numpy`, `matplotlib` y `scikit-learn`. Desde la raíz del repositorio:

```bash
py -I codigo/guia_4/limpieza_amb.py     # escribe datos/compraventas_limpias.csv y datos/pares_amb.csv
py -I codigo/guia_4/descarga_actos.py   # opcional: vuelve a descargar los actos de los folios desde la API
py -I codigo/guia_4/limpieza_amb.py     # repite la limpieza con los actos descargados
py -I codigo/diccionario.py             # regenera el diccionario de variables
```

El análisis nacional se ejecuta con `py -I codigo/guia_1/analisis_guia1.py`: descarga lo que falte a `datos/guia_1/descarga/` (no versionada, varios GB) y escribe `cifras.json`, los CSV y las figuras en `datos/guia_1/`.

El notebook `03_entendimiento.ipynb` se ejecuta desde `codigo/guia_4/` y lee los archivos de `datos/`. El notebook `02_entendimiento_calidad_compraventas.ipynb` usa la extracción original de 26 columnas (`Registro_de_transacciones_base.csv`), que incluye las columnas `numero_catastral` y `numero_catastral_antiguo` (vacías en el 100%); la descarga de `datos/` trae las otras 24.

Resultado esperado de la limpieza: 165.517 compraventas → 133.720 limpias (80,8%) → 14.469 pares con al menos 365 días → 13.978 pares para el índice (12.399 urbanos, 1.398 rurales, 181 sin zona).

## Fuentes

- IGAC (2026). Registro de transacciones inmobiliarias en Colombia 2015-2023 (`7y2j-43cv`). datos.gov.co. Datos abiertos.
- IGAC. Resoluciones 1912 de 2024, 1939 de 2025, 2057 de 2025 y 0384 de 2026.
- DANE (IPVN, IVP) y Banco de la República (IPVU).

## Uso responsable

Los resultados son señales para revisar, no conclusiones sobre un avalúo, un predio o una persona. El proyecto no modifica avalúos ni emite conclusiones jurídicas o de fraude.
