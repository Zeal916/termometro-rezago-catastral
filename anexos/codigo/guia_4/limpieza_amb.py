"""Guía 4, Parte II: limpieza de compraventas del AMB (reglas de la Guía 2).
Uso: py -I limpieza_amb.py  -> imprime el embudo y escribe compraventas_limpias.csv y pares_amb.csv
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "datos"  # carpeta datos del repositorio
d = pd.read_csv(BASE / "amb_compraventas_2015_2023.csv", dtype=str)
embudo = [("Compraventas del AMB 2015-2023 (cód. 125)", len(d))]

def paso(nombre, mascara_conservar):
    global d
    d = d[mascara_conservar]
    embudo.append((nombre, len(d)))

# Columnas sin información: se descartan, no se imputan
d = d.drop(columns=["folios_derivados", "fecha_apertura_texto"])

# (b) Formato: la fecha viene como 'AAAA-MM-DD hh:mm:ss' o 'dd/mm/aa'
f = d.fecha_radica_texto
d["fecha"] = pd.to_datetime(f, format="%Y-%m-%d %H:%M:%S", errors="coerce").fillna(
    pd.to_datetime(f, format="%d/%m/%y", errors="coerce"))
paso("Fecha válida", d.fecha.notna())

# (a) Rango: el valor debe ser un precio plausible (> COP 1 M)
d["valor"] = pd.to_numeric(d.valor, errors="coerce")
paso("Valor > COP 1 M (sale valor 0 y < 1 M)", d.valor > 1e6)

# (d) Interrelaciones: una sola cifra por anotación, sin duplicados de folio y fecha
paso("Un solo valor en la anotación", d.tiene_mas_de_un_valor == "0")
paso("Duplicado exacto (folio, fecha, valor): queda uno", ~d.duplicated(["matricula", "fecha", "valor"]))
paso("Mismo folio y fecha con valores distintos: salen todos", ~d.duplicated(["matricula", "fecha"], keep=False))

# (c)/(d) Escritura con varios predios = precio global, no del predio
n_predios = d.groupby("documento_justificativo").matricula.transform("nunique")
paso("Escritura de un solo predio", n_predios == 1)

# (b) Zona 'SIN INFORMACION': se recupera de otra venta del mismo folio; si no, queda como categoría
zona_folio = d[d.tipo_predio_zona != "SIN INFORMACION"].groupby("matricula").tipo_predio_zona.first()
sin = d.tipo_predio_zona == "SIN INFORMACION"
d.loc[sin, "tipo_predio_zona"] = d.loc[sin, "matricula"].map(zona_folio).fillna("SIN INFORMACION")

# (c) Extremos: se MARCAN, no se borran (OA6 los necesita como candidatos a anomalía)
d["extremo_alto"] = d.valor > d.valor.quantile(.995)
d["cola_baja_1_10M"] = d.valor < 1e7

d.to_csv(BASE / "compraventas_limpias.csv", index=False)

# Pares de ventas repetidas: ventas consecutivas del mismo folio con >= 365 días
d = d.sort_values(["matricula", "fecha"])
prev = d.groupby("matricula")[["fecha", "valor"]].shift()
p = d.assign(fecha_ant=prev.fecha, valor_ant=prev.valor).dropna(subset=["fecha_ant"])
pares = [("Pares consecutivos del mismo folio", len(p))]
p = p[(p.fecha - p.fecha_ant).dt.days >= 365]
pares.append(("Pares con >= 365 días", len(p)))
p["razon"] = p.valor / p.valor_ant

# (d) Cambio físico entre las dos ventas (actos del folio descargados con descarga_actos.py).
# Reforma/adición del reglamento de PH (331, 347) NO cuenta: se registra en todas las unidades del edificio
# y la mediana de la razón de precios en esos pares (1,03-1,10) es igual a la del total (1,10).
CAMBIO_FISICO = {"317", "902", "903", "909", "910", "911", "912", "913", "915", "917", "918", "919", "920",
                 "924", "964"}
actos = BASE / "api" / "actos_folios_pares.csv"
p["cambio_fisico"] = False
if actos.exists():
    a = pd.read_csv(actos, dtype=str)
    a = a[a.cod_natujur.isin(CAMBIO_FISICO)]
    a["fecha_acto"] = pd.to_datetime(a.fecha_radica_texto, format="%Y-%m-%d %H:%M:%S", errors="coerce").fillna(
        pd.to_datetime(a.fecha_radica_texto, format="%d/%m/%y", errors="coerce"))
    x = p[["matricula", "fecha", "fecha_ant"]].reset_index().merge(a[["matricula", "fecha_acto"]], on="matricula")
    x = x[(x.fecha_acto > x.fecha_ant) & (x.fecha_acto <= x.fecha)]
    p.loc[p.index.isin(x["index"]), "cambio_fisico"] = True
    pares.append(("Pares sin cambio físico entre las dos ventas", int((~p.cambio_fisico).sum())))
else:
    print("AVISO: falta datos_api/actos_folios_pares.csv; corre descarga_actos.py")

p["cambio_extremo_5x"] = (p.razon >= 5) | (p.razon <= 1 / 5)
p["para_indice"] = ~p.cambio_fisico & ~p.cambio_extremo_5x
pares.append(("Pares para el índice (además, sin cambios de 5 veces o más)", int(p.para_indice.sum())))
p.to_csv(BASE / "pares_amb.csv", index=False)

print("EMBUDO DE COMPRAVENTAS")
for i, (n, v) in enumerate(embudo):
    quita = "" if i == 0 else f"  (-{embudo[i-1][1] - v:,})"
    print(f"{n:<50}{v:>9,}{quita}")
print(f"Zona recuperada por folio: {sin.sum() - (d.tipo_predio_zona == 'SIN INFORMACION').sum():,} de {sin.sum():,}")
print(f"Marcados extremo alto (p99,5 > COP {d.valor.quantile(.995)/1e6:,.0f} M): {d.extremo_alto.sum():,}")
print(f"Marcados cola baja (COP 1-10 M): {d.cola_baja_1_10M.sum():,}")
print("\nPARES")
for n, v in pares:
    print(f"{n:<50}{v:>9,}")
print("Por zona:", p[p.para_indice].tipo_predio_zona.value_counts().to_dict())
print(f"Mediana razón de precios: con cambio físico {p[p.cambio_fisico].razon.median():.2f}; "
      f"sin cambio físico {p[~p.cambio_fisico].razon.median():.2f}")
