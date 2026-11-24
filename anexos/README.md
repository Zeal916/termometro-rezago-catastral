# Anexos del anteproyecto

Material que cita el documento final ([`../documento/anteproyecto.pdf`](../documento/anteproyecto.pdf), sección "Anexos"). Las letras corresponden a la tabla de anexos del documento.

| Anexo | Contenido | Ruta |
|---|---|---|
| A. Guía 1 | Carta del proyecto y anexo (ideación, filtro de siete características, matriz valor-capacidad, 5W, accesibilidad, umbrales, limitantes, beneficios, criterios de éxito, cronograma) | [`guia_1/`](guia_1/) |
| B. Guía 2 | Planteamiento del problema de Analytics y anexo (Kano, requerimientos R1-R10 y A1-A5, recursos, presupuesto, fuentes, objetivos OA1-OA6, métricas, estado del arte) | [`guia_2/`](guia_2/) |
| C. Guía 3 | RBS y AMEF completos (21 factores con RPN, plan de acciones A1-A13, escalas y contraste con la matriz probabilidad × impacto), en PDF y Excel | [`guia_3/`](guia_3/) |
| D. Guía 4 | Informe de calidad, limpieza y entendimiento (piloto del AMB), con sus notebooks y scripts | [`guia_4/`](guia_4/), [`codigo/guia_4/`](codigo/guia_4/) |
| E. Guía 5 | Partes I y II tal como se redactaron | [`guia_5/`](guia_5/) |
| F. Datos y código | Análisis nacional (línea base), piloto del AMB, ampliación a Santander, variables de OA2, contraste con índices oficiales, perfil de la Res. 2057 y vigencias del Art. 49 | [`codigo/`](codigo/), [`datos/`](datos/), [`figuras/`](figuras/) |
| G. Diccionario | 45 variables con origen, tipo, porcentaje de vacíos y uso | [`diccionario_variables.md`](diccionario_variables.md) |
| H. Cifras | Cada cifra del documento con el archivo que la produce | [`CIFRAS.md`](CIFRAS.md) |

## Código y resultados

| Carpeta | Qué produce | Salidas |
|---|---|---|
| `codigo/guia_1/analisis_guia1.py` | Análisis nacional (5,4 M de compraventas): línea base (MdAPE, AUC), índices por municipio y zona, cruce con la Res. 2057 | `datos/guia_1/` (`cifras.json`, CSV y figuras) |
| `codigo/guia_4/limpieza_amb.py` | Limpieza del AMB y formación de pares | `datos/compraventas_limpias.csv`, `datos/pares_amb.csv`, `codigo/guia_4/resultados_limpieza.txt` |
| `codigo/guia_4/descarga_actos.py` | Actos de los folios con pares, desde la API | `datos/api/actos_folios_pares.csv` |
| `codigo/guia_4/02_…` y `03_….ipynb` | Calidad y entendimiento del AMB (Guía 4, Partes I y III) | Salidas de celdas y `figuras/guia_4/` |
| `codigo/guia_5/` | Ampliación a Santander, variables del folio para OA2, índices oficiales, Res. 2057 y vigencias | `resultados_*.txt`, CSV y figuras en la misma carpeta |
| `codigo/diccionario.py` | Diccionario de variables | `diccionario_variables.md` y `.csv` |

Los scripts se ejecutan desde esta carpeta (`anexos/`), por ejemplo `py -I codigo/guia_4/limpieza_amb.py`. El orden de ejecución, los requisitos y los datos que no se versionan están en [`../recuperacion/README.md`](../recuperacion/README.md).

## Fuentes de datos

- IGAC (2026). Registro de transacciones inmobiliarias en Colombia 2015-2023 (`7y2j-43cv`) y Gestores catastrales de Colombia (`bhcx-bx97`). datos.gov.co. Datos abiertos.
- IGAC. Resoluciones 1912 de 2024, 1939 de 2025, 2057 de 2025 (`codigo/guia_5/res2057.pdf`) y 0384 de 2026; memorias técnicas del Art. 49 (enlaces en `codigo/guia_5/memorias_art49_santander_enlaces.csv`).
- DANE (IPVN, IVP; boletines en `codigo/guia_5/fuentes_indices_oficiales/`) y Banco de la República (IPVU).
