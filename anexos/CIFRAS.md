# Hoja maestra de cifras

Cada cifra del documento final (`documento/anteproyecto.pdf`; texto fuente en `recuperacion/documento_fuente/anteproyecto.md`) con el archivo que la produce. Es la herramienta de control prevista en el plan: antes de cada entrega se contrasta el documento con esta hoja y, si un script cambia, se actualizan las dos.

Las rutas son relativas a `anexos/`. Convención: `cifras.json:clave` es una clave de `datos/guia_1/cifras.json`; `resultados_X.txt §n` es la sección n de `codigo/guia_5/resultados_X.txt`.

## 1. Contexto (fuentes documentales, no calculadas)

| Cifra | Fuente |
|---|---|
| 1.639.140 predios rurales en 527 municipios; aumento mediano de 326% por zona | Resolución IGAC 2057 de 2025; el 326% también en `cifras.json:art49_pct_p10_p50_p90` |
| 41,34% del área actualizada (julio 2026), 59,1% de la meta; meta de 70% del PND (41,34 / 0,591) | IGAC (2026d), nota del 27 de julio de 2026, verificada en la web el 25 de noviembre de 2026 |
| 836 municipios con el IGAC como gestor | `cifras.json:mun_gestor_igac` (datos.gov.co, bhcx-bx97) |
| IPVN 53 municipios, IVP 22 capitales, IPVU 9 ciudades | DANE y Banco de la República (anexo de la Guía 1, Parte III) |
| Demanda de nulidad contra la Res. 2057 admitida en septiembre de 2026 | Vanguardia (2026, 9 de octubre) |
| Rango legal del avalúo de 60% a 100% del valor comercial | Decreto 148 de 2020 (Diario Oficial 51.217), definición de avalúo catastral; texto verificado |

## 2. Nacional, Guía 1 y 2 (`codigo/guia_1/analisis_guia1.py` → `datos/guia_1/cifras.json`)

| Cifra | Clave |
|---|---|
| 5.424.769 compraventas; 3.995.772 con valor; 1.096 municipios | `compraventas`, `con_valor`, `municipios_con_valor` |
| 30,9 M de actos; 5,4 M actos del folio | `actos_total`, `actos_folio_total` |
| 15% con venta anterior (430.456 de 2.853.681 compraventas de un predio con valor y fecha); 10% con al menos un año; 9% entra al índice | `reventas_pct`, `reventas_365_pct`, `pares_pct` |
| 256.973 pares: 183.439 urbanos, 71.004 rurales, 2.530 sin zona | `pares`, `pares_urbanos`, `pares_rurales`, `pares_sin_zona` |
| 41% de las reventas crece 0-5% anual; 14% exactamente 0% o 3% | `pares_crec_0a5pct_anual`, `pares_crec_exacto_0_o_3pct` |
| 50% en 2018 → 31% en 2019 → 40% en 2021-2023 | `pares_crec_0a5pct_por_anio_2a_venta` |
| 340 municipios urbanos y 324 rurales con índice propio; 235/235 con el IGAC como gestor | `mun_indice_URBANO`, `mun_indice_RURAL`, `mun_igac_indice_*` |
| Banda urbana 2023: 153 a 250 (136 municipios); mínimos cuadrados 180; avalúo 127 | `idx2023_URBANO_*`, `mun_cotas_urbanas`, `reajuste_acumulado_2015_2023_aprox` |
| Pérdida del avalúo de 17% a 49% | `perdida_avaluo_vs_mercado_pct` |
| Umbral del piso de 60%: índice 2023 > 211 (127 / 0,6); con el reajuste por decretos reales del AMB, 128,3 / 0,6 = 214; 49 urbanos y 53 rurales sin IC | `umbral_indice_piso60`, `mun_bajo_piso60_sin_ic` |
| MdAPE: regla 18,3% (IC 18,0-18,8); sin ajuste 23,4%; mínimos cuadrados 24,6%; robusto 20,6%; caso ideal 14,8%; meta 16,5% | `MdAPE_*` |
| 56.994 reventas de prueba; 36,9% compatibles con el avalúo; 3,5% vs 7,2% y 43,6% vs 38,3% | `pares_prueba`, `prueba_pct_compatible_avaluo`, `MdAPE_por_grupo` |
| AUC 0,745 (regla) y 0,757 (índice robusto); detección máxima de 3% con cupo de 2%; 9,8% cambia 5 veces o más | `alertas_regla`, `alertas_indice_robusto`, `reventas_365_cambio_5x_o_mas_pct` |
| Cupo de 2%: unas 960 alertas al año | `alertas_al_anio_con_presupuesto` (957) |
| Res. 2057: 7.484 zonas, 527 municipios, 656 zonas de 4%, 1.521 de más de 1.000% | `art49_*` |
| 143 municipios del Art. 49 con índice rural; 68 de Santander, 15 con índice rural | `art49_mun_indice_rural`, `santander_art49`, `santander_art49_indice_rural` |
| Spearman de 0,10 sin año de actualización | `art49_spearman_municipal` |

## 3. Piloto del AMB, Guía 4 (`codigo/guia_4/`)

| Cifra | Fuente |
|---|---|
| 165.517 compraventas → 133.720 limpias (80,8%) → 14.469 pares → 13.978 para el índice (12.399 urbanos, 1.398 rurales, 181 sin zona) | `codigo/guia_4/resultados_limpieza.txt` (salida de `limpieza_amb.py`) |
| 770 valores ≤ COP 1 M; 4 con más de un valor, 112 duplicados exactos y 90 con valores distintos (206); 30.821 de varios predios; razón 3,22 con cambio físico vs 1,10 | idem |
| 19.672 pares consecutivos; 5.203 con menos de un año; 156 con cambio físico y 335 con cambio de 5 veces o más (491) | idem |
| 76.065 actos de 13.129 folios | `datos/api/LEEME_descarga.json` |
| Vacíos: numero_catastral 100%, folios_derivados 99,99%, fecha_apertura 80,93%; fecha dd/mm/aa en 19% | `codigo/guia_4/02_entendimiento_calidad_compraventas.ipynb` (salidas de celdas) y `diccionario_variables.md` |
| 52,4% en patrón de avalúo; variación mediana 2,98%; grupo estable de 53,2% en 1,7% anual | `codigo/guia_4/03_entendimiento.ipynb` |
| Salto de 13,9% en 2019; índice 143,2 vs 128,3 del decreto; AUC 0,68 con variables del registro | idem |
| Base limpia de 25 columnas (26 originales, 4 vacías retiradas, 3 derivadas); 7 constantes y 4 redundantes: 14 columnas | idem; informe de la Guía 4 |

## 4. Santander y Art. 49, Guía 5 (`codigo/guia_5/`)

| Cifra | Fuente |
|---|---|
| 301.356 compraventas de Santander (165.517 AMB, 90.982 Art. 49, 44.857 otros) | `resultados_entendimiento_santander.txt` §1-2 |
| Art. 49: 32,8% sin valor; 27,6% sin número de escritura | idem §1 |
| 5.016 pares en el Art. 49; mediana de 8 pares rurales por municipio | idem §3 |
| 41,3% de pares rurales del Art. 49 con patrón de avalúo | idem §4 |
| Salto de 2019: 11,5% (AMB rural) a 22,9% (Art. 49 rural); "Otros urbano" 36,2% | idem §6 |
| Hipoteca el mismo día: 2,9% en Art. 49 rural | idem §7 |
| Hipoteca el mismo día: 31,9% de las compraventas limpias del AMB | `resultados_variables_oa2.txt` |
| AUC 0,676 → 0,734 (+0,058, IC 0,047-0,070); por folio 0,684 → 0,750; 4 variables del folio: hipoteca en la venta 1 y en la venta 2, propiedad horizontal y primera venta de un folio nuevo | idem |
| Índice urbano a menos de 3,5 puntos del IVP e IPVN en 2023; IVP 4,5% e IPVN 1,4% en 2019 | `resultados_indices_oficiales.txt` |
| 1.058 zonas en Santander; 215 zonas (61 municipios) sobre 3 veces la mediana | `resultados_res2057_santander.txt` §1, §3 |
| 14 de 15 municipios con mercado sobre el reajuste; mediana 1,45; Spearman -0,19 | idem §5 |
| 0 de 68 memorias declaran el año de actualización; cota 2017 o antes | `resultados_vigencias_santander.txt` §1-2 |
| Relación implícita avalúo/comercial: mediana 9,9% en 1.014 zonas | idem §3 |

## 5. Gestión (sin cálculo)

| Cifra | Fuente |
|---|---|
| 21 factores de riesgo en 12 categorías: 9 altos, 7 medios y 5 bajos; RPN total 3.764, máximo 360; 62% del RPN en datos y técnico-analítico | `guia_3/AMEF_Guia_3.xlsx` |
| Retroalimentación de la Guía 4: 31,5 de 35 | Calificación recibida por el equipo (no está en el repositorio) |
| Scores Kano (R1 = 90 … A5 = 45) | `guia_2/Anexo_Guia_2.pdf`, Tablas 1 y 2 |
| 384 horas (192 + 192), COP 60.000 por hora, COP 23.040.000; 8 h de contingencia en el Capstone | `guia_2/Anexo_Guia_2.pdf`, Tablas 4 y 5; `guia_5/Guia_5_Parte_II.docx` |

## 6. Presentación (`recuperacion/presentacion/Presentacion_anteproyecto_v3.pptx`)

| Cifra | Fuente |
|---|---|
| Histograma de la diapositiva 4: 52% (52,3%) de los 13.978 pares para el índice crece entre 0% y 5% anual | `datos/pares_amb.csv` (columna `para_indice`); el documento reporta 52,4% con una definición más amplia (valor congelado, réplica del reajuste o 0-5%) |
| Demás cifras de las diapositivas | Las mismas de este documento |
