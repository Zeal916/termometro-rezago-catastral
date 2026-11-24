"""Genera diccionario_variables.md y diccionario_variables.csv a partir de los CSV de datos/.
Uso (desde anexos/): py -I codigo/diccionario.py
"""
import sys
from pathlib import Path

import pandas as pd

R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
D = R / "datos"
src = {
    "original": D / "amb_compraventas_2015_2023.csv",
    "limpias": D / "compraventas_limpias.csv",
    "pares": D / "pares_amb.csv",
    "actos": D / "api" / "actos_folios_pares.csv",
}
dfs = {k: pd.read_csv(v, dtype=str, keep_default_na=False, na_values=[""]) for k, v in src.items()}

O = "Registro IGAC 7y2j-43cv"
L = "limpieza_amb.py"
N = "03_entendimiento.ipynb"
TODOS = "todos"
OLP = "original, limpias, pares"
V = [  # variable, archivos, origen, tipo, descripción, uso o decisión
    ("pk", OLP, O, "texto", "Llave única de la anotación: DIVIPOLA-ORIP-matrícula-anotación-acto-año", "Control de duplicados (sin repetidos)"),
    ("matricula", TODOS, O, "texto", "Folio de matrícula inmobiliaria (ORIP-número); identifica el inmueble", "Llave para formar pares y unir los actos del folio"),
    ("num_anotacion", TODOS, O, "entero", "Número de la anotación dentro del folio", "Ordena los actos del folio; parte de la clave registral"),
    ("orip", OLP, O, "texto", "Oficina de registro (300 Bucaramanga; 314 Piedecuesta)", "Sale del análisis: repite divipola"),
    ("divipola", TODOS, O, "texto", "Código DANE del municipio", "Agregación por municipio; se lee como texto"),
    ("municipio", OLP, O, "texto", "Nombre del municipio", "Segmentación por municipio"),
    ("departamento", OLP, O, "texto", "Departamento", "Constante en el piloto"),
    ("categoria_ruralidad_2024", OLP, O, "texto", "Categoría de ruralidad del municipio", "Constante en el piloto; jerarquía del índice en el país"),
    ("dinamica_2024", OLP, O, "texto", "Indicador de dinámica inmobiliaria del municipio", "Constante en el piloto"),
    ("cod_natujur", TODOS, O, "texto", "Código de la naturaleza jurídica del acto (125 = compraventa)", "Filtro de compraventas; en los actos identifica hipoteca, PH y cambios físicos"),
    ("nombre_natujur", TODOS, O, "texto", "Nombre de la naturaleza jurídica", "Descriptivo"),
    ("documento_justificativo", TODOS, O, "texto", "Tipo, número y fecha de la escritura, y notaría", "Se extrae fecha_escritura; la notaría se descarta (formato inconsistente en el tiempo)"),
    ("fecha_radica_texto", TODOS, O, "texto (fecha)", "Fecha de radicación en dos formatos (AAAA-MM-DD hh:mm:ss y dd/mm/aa, 19%)", "Se unifica en fecha"),
    ("year_radica", OLP, O, "entero", "Año de radicación", "Repite la fecha; sale del análisis"),
    ("fecha_apertura_texto", "original", O, "texto (fecha)", "Fecha de apertura del folio", "Se elimina, no se imputa"),
    ("folios_derivados", "original", O, "texto", "Folios derivados del folio", "Se elimina, no se imputa"),
    ("estado_folio", OLP, O, "texto", "Estado del folio (activo o cerrado)", "Descriptivo"),
    ("count_a", OLP, O, "entero", "Número de compradores", "Candidata; importancia por permutación < 0,001"),
    ("count_de", OLP, O, "entero", "Número de vendedores", "Candidata; importancia por permutación < 0,001"),
    ("predios_nuevos", OLP, O, "entero", "Indicador de predio nuevo en la anotación", "Candidata a primera venta de un folio nuevo (OA2)"),
    ("tiene_mas_de_un_valor", OLP, O, "0/1", "La anotación trae más de un valor", "Regla de limpieza: salen 4 anotaciones"),
    ("tiene_valor", OLP, O, "0/1", "La anotación trae valor", "Constante en el piloto"),
    ("tipo_predio_zona", OLP, O, "texto", "Zona URBANO / RURAL / SIN INFORMACION", "Segmentación urbano-rural (R2); zona vacía recuperada de otra venta del folio (52)"),
    ("valor", TODOS, O, "numérico (COP)", "Valor declarado en la escritura", "Variable que se mide: no se imputa; salen los valores de COP 1 M o menos"),
    ("numero_catastral, numero_catastral_antiguo", "extracción de 26 columnas (Guía 4, Parte I)", O, "texto", "Número predial catastral, vacío en el 100% de los registros", "No permite unir el avalúo de cada predio; el rezago se mide contra el reajuste por decreto"),
    ("fecha", "limpias, pares", L, "fecha", "Fecha de radicación unificada", "Serie de tiempo; días entre ventas"),
    ("extremo_alto", "limpias, pares", L, "booleano", "Valor sobre el percentil 99,5 (COP 1.050 M)", "Se marca, no se borra; candidato para OA6"),
    ("cola_baja_1_10M", "limpias, pares", L, "booleano", "Valor entre COP 1 M y 10 M (cuotas, derechos parciales o errores)", "Se marca, no se borra"),
    ("fecha_ant", "pares", L, "fecha", "Fecha de la venta anterior del mismo folio", "Forma el par; al menos 365 días"),
    ("valor_ant", "pares", L, "numérico (COP)", "Valor de la venta anterior", "Forma el par"),
    ("razon", "pares", L, "numérico", "valor / valor_ant", "Cambio de precio del par"),
    ("cambio_fisico", "pares", L, "booleano", "Acto de construcción, área o linderos, división, englobe, loteo o PH entre las dos ventas", "Excluye del índice; se conserva marcado para OA6"),
    ("cambio_extremo_5x", "pares", L, "booleano", "La razón es de 5 o más, o de 1/5 o menos", "Excluye del índice; se conserva marcado para OA6"),
    ("para_indice", "pares", L, "booleano", "Par apto para el índice (365 días, sin cambio físico ni cambio de 5 veces)", "13.978 pares"),
    ("log_valor", "derivada en el notebook", N, "numérico", "ln(valor)", "Corrige la asimetría (161 a -0,7)"),
    ("redondo", "derivada en el notebook", N, "booleano", "Valor múltiplo exacto de COP 1 M", "Indicio de precio negociado"),
    ("fecha_escritura", "derivada en el notebook", N, "fecha", "Fecha leída de documento_justificativo", "Fija el año del avalúo vigente al firmar"),
    ("dias_esc_rad", "derivada en el notebook", N, "entero", "Días entre escritura y radicación", "Control de calidad (mediana 15, p95 77)"),
    ("anios", "derivada en el notebook", N, "numérico", "Años entre las dos radicaciones (días / 365,25)", "Horizonte del par (mediana 3,2)"),
    ("g", "derivada en el notebook", N, "numérico", "Tasa anual del par: razon^(1/anios) - 1", "Segmentación, mezcla gaussiana y etiqueta débil"),
    ("congelado", "derivada en el notebook", N, "booleano", "Mismo valor en las dos ventas", "Segmento de valor congelado"),
    ("factor_decreto", "derivada en el notebook", N, "numérico", "Producto de (1 + reajuste) entre los años de las dos escrituras (3%; 4,31% en 2023)", "Crecimiento de un avalúo no actualizado"),
    ("replica_decreto", "derivada en el notebook", N, "booleano", "razon a menos de 0,5% de factor_decreto", "Segmento de réplica del reajuste"),
    ("cruza_ley1943", "derivada en el notebook", N, "booleano", "Primera escritura antes de 2019 y segunda desde 2019", "Quiebre de 2019 (Ley 1943 de 2018)"),
    ("cruza_act_bga", "derivada en el notebook", N, "booleano", "Igual que cruza_ley1943, solo en Bucaramanga", "Actualización catastral de Bucaramanga (2019)"),
]

rows = []
for var, arch, orig, tipo, desc, uso in V:
    nul = [f"{k}: {d[var].isna().mean() * 100:.2f}%".replace(".", ",") for k, d in dfs.items() if var in d.columns]
    rows.append(dict(variable=var, archivos=arch, origen=orig, tipo=tipo, descripcion=desc,
                     uso_o_decision=uso, pct_vacios="; ".join(nul) or "100% (no viene en esta descarga)"))

documentadas = {r["variable"] for r in rows}
for k, d in dfs.items():
    faltan = [c for c in d.columns if c not in documentadas]
    if faltan:
        sys.exit(f"Variables sin documentar en {k}: {faltan}")

pd.DataFrame(rows).to_csv(R / "diccionario_variables.csv", index=False, encoding="utf-8-sig")

contenido = {
    "original": "Compraventas (cód. 125) del AMB descargadas de 7y2j-43cv",
    "limpias": "Compraventas tras las reglas de limpieza, con marcas de extremos",
    "pares": "Pares de ventas consecutivas del mismo folio con al menos 365 días",
    "actos": "Todos los actos de los 13.129 folios con pares (descarga del 8 nov 2026)",
}
md = [
    "# Diccionario de variables",
    "",
    "Piloto del Área Metropolitana de Bucaramanga (AMB), 2015-2023. Generado con `codigo/diccionario.py` "
    "a partir de los CSV de `datos/`; el porcentaje de vacíos se recalcula cada vez que se regenera.",
    "",
    "| Archivo | Filas | Columnas | Contenido |",
    "|---|---|---|---|",
]
for k, v in src.items():
    md.append(f"| `{v.relative_to(R).as_posix()}` | {len(dfs[k]):,}".replace(",", ".") + f" | {dfs[k].shape[1]} | {contenido[k]} |")
md += ["", "| Variable | Archivos | Origen | Tipo | Descripción | Uso o decisión | % vacíos |", "|---|---|---|---|---|---|---|"]
md += ["| `{variable}` | {archivos} | {origen} | {tipo} | {descripcion} | {uso_o_decision} | {pct_vacios} |".format(**r) for r in rows]
md += [
    "",
    "Códigos de acto tratados como cambio físico: 317 (reglamento de PH), 902, 903, 917 y 964 (área y linderos), "
    "909 (urbanización), 910, 911 y 912 (construcción o mejora), 913, 915 y 919 (englobe y desenglobe), "
    "918 (división material), 920 y 924 (loteo y reloteo). La reforma (331) y la adición (347) del reglamento "
    "de PH no se tratan como cambio físico.",
]
(R / "diccionario_variables.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"{len(rows)} variables documentadas")
