# Termómetro de rezago catastral

Anteproyecto del curso **Gerencia de Proyectos de Analytics** (Maestría en Inteligencia Analítica de Datos, Universidad de los Andes), Caso Dinámica Inmobiliaria 2026. Equipo 23: Nicolás Santos (líder y negocio), Cristian Ortiz (ingeniería y calidad de datos), Daniel Aguirre (modelación) y Dayan Hincapie (visualización y documentación). Asesor: Carlos Ramírez.

**Problema.** El IGAC debe decidir en qué municipios actualizar o revisar primero el avalúo catastral y sustentar o corregir el ajuste del Art. 49 de la Ley 2294 de 2023 (Resolución 2057 de 2025). El proyecto mide, con las ventas repetidas del Registro de Transacciones Inmobiliarias del IGAC 2015-2023 (datos.gov.co, `7y2j-43cv`), la brecha entre el avalúo y el mercado por municipio, en zona urbana y rural, después de separar las escrituras declaradas por el avalúo.

**Empiece por:** [`documento/anteproyecto.pdf`](documento/anteproyecto.pdf), el documento final que consolida las cinco guías (18 páginas).

## Cómo está organizado

| Carpeta | Para qué | Quién la usa |
|---|---|---|
| [`documento/`](documento/) | El entregable: `anteproyecto.pdf` y `anteproyecto.docx` | Quien evalúa o lee el anteproyecto |
| [`anexos/`](anexos/) | Los anexos que cita el documento: entregas de las Guías 1 a 5, código y resultados, datos del piloto, figuras, diccionario de variables y hoja maestra de cifras | Quien quiere verificar o profundizar lo que dice el documento |
| [`recuperacion/`](recuperacion/) | Lo necesario para reconstruir o seguir editando el proyecto: fuente del documento, fuentes editables de cada entrega (Word, Excel, HTML), presentación, notas del equipo, descarga de datos y el procedimiento paso a paso | El equipo, si hay que modificar algo o si se pierde todo lo demás |

Este repositorio es la fuente de documentación del proyecto: si se pierde todo lo demás, se recupera desde aquí siguiendo [`recuperacion/README.md`](recuperacion/README.md).

## Cronología

| Semana | Entrega | Resultado principal | Anexo |
|---|---|---|---|
| S1-S3 (oct 2026) | Guía 1: carta del proyecto y anexo | 8 ideas, filtro y matriz valor-capacidad; problema de negocio; línea base nacional (MdAPE 18,3%, AUC 0,757). Retroalimentación aplicada el 24 oct | `anexos/guia_1/`, `anexos/codigo/guia_1/` |
| S3-S4 | Guía 2: planteamiento del problema de Analytics | Kano (R1-R10, A1-A5), objetivos OA1-OA6, fuentes, metas y estado del arte | `anexos/guia_2/` |
| S4 | Guía 3: RBS, AMEF y video de avance | 21 riesgos; 9 altos; acciones en el plan | `anexos/guia_3/` |
| S5-S6 | Guía 4: calidad, limpieza y entendimiento (AMB) | 13.978 pares; 52,4% en patrón de avalúo; quiebre de 2019 | `anexos/guia_4/`, `anexos/codigo/guia_4/` |
| S7-S8 (nov 2026) | Guía 5 y documento final | Ampliación a Santander; enfoques, métodos, evaluación, monitoreo, cierre y plan del Capstone | `anexos/guia_5/`, `anexos/codigo/guia_5/`, `documento/` |

Las Guías 2, 3 y 4 no recibieron observaciones. El Capstone (8 semanas, 192 horas) construye el producto según la sección 7 del documento.

## Uso responsable

Los resultados son señales para revisar, no conclusiones sobre un avalúo, un predio o una persona. El proyecto no modifica avalúos ni emite conclusiones jurídicas o de fraude.
