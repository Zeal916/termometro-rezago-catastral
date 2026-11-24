"""Entendimiento de las compraventas de Santander (piloto rural del Art. 49).

Aplica a todo Santander las mismas reglas de limpieza y de formación de pares del piloto del AMB (limpieza_amb.py) y
las técnicas del notebook 03_entendimiento.ipynb (segmentos de los pares, índice Bailey-Muth-Nourse y quiebre de 2019),
y compara el AMB (4 municipios) con los 68 municipios del Art. 49 y los otros 15, en zona urbana y rural.
Entrada: ../../../datos/santander_actos.csv (descarga_santander.py).
Uso: python entendimiento_santander.py -> resultados_entendimiento_santander.txt, pares_santander.csv,
     fig_entendimiento_santander.png
"""
import io
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
ENTRADA = BASE.parents[1] / "datos" / "guia_5" / "santander_actos.csv"  # lo genera descarga_santander.py
AMB = {"68001", "68276", "68307", "68547"}       # Bucaramanga, Floridablanca, Girón, Piedecuesta
CAMBIO_FISICO = {"317", "902", "903", "909", "910", "911", "912", "913", "915", "917", "918", "919", "920",
                 "924", "964"}                   # mismos códigos que limpieza_amb.py
HIPOTECA = {"203", "204", "205", "219"}
REAJUSTE = {a: 0.03 for a in range(2010, 2023)} | {2023: 0.0431}   # misma serie del notebook 03
ANIOS = list(range(2016, 2024))


def fecha(texto):
    return pd.to_datetime(texto, format="%Y-%m-%d %H:%M:%S", errors="coerce").fillna(
        pd.to_datetime(texto, format="%d/%m/%y", errors="coerce"))


def fecha_escritura(texto):
    d = texto.str.extract(r"(\d{1,2}/\d{1,2}/\d{2,4})")[0]
    return pd.to_datetime(d, format="%d/%m/%Y", errors="coerce").fillna(
        pd.to_datetime(d, format="%d/%m/%y", errors="coerce"))


a = pd.read_csv(ENTRADA, dtype=str)
a["f"] = fecha(a.fecha_radica_texto)
cv = a[a.cod_natujur == "125"].copy()
# Los 68 municipios de Santander del Art. 49 (Resolución 2057 de 2025); ninguno es del AMB
ART49 = set(pd.read_csv(BASE / "res2057_santander_municipios.csv", dtype={"div": str})["div"])
assert not ART49 & AMB and len(ART49) == 68
cv["ambito"] = np.select([cv.divipola.isin(AMB), cv.divipola.isin(ART49)], ["AMB", "Art49"], default="Otros")

# ---------------------------------------------------------------- 1. calidad (antes de limpiar)
cv["valor"] = pd.to_numeric(cv.valor, errors="coerce")
# El texto del documento puede repetirse entre ámbitos (63 compraventas fuera del AMB comparten documento con una del
# AMB); como en el piloto del AMB, la regla de "escritura de un solo predio" se evalúa dentro de cada ámbito
n_predios_doc = cv.groupby(["ambito", "documento_justificativo"]).matricula.transform("nunique")
# Documento truncado sin número ni fecha de escritura ("01-ESCRIT", "01-ESCRITURA"): no identifica la escritura
cv["doc_sin_numero"] = ~cv.documento_justificativo.fillna("").str.contains(r"\d{2,}.*\d", regex=True)
doc_ok = cv[~cv.doc_sin_numero]
g_doc = doc_ok.groupby(["ambito", "documento_justificativo"]).agg(pred=("matricula", "nunique"),
                                                                   mun=("divipola", "nunique"))
calidad = cv.groupby("ambito").apply(lambda g: pd.Series({
    "compraventas": len(g), "municipios": g.divipola.nunique(),
    "fecha formato dd/mm/aa (%)": 100 * g.fecha_radica_texto.str.contains("/").mean(),
    "valor vacío (%)": 100 * g.valor.isna().mean(),
    "valor de 0 a COP 1 M (%)": 100 * (g.valor <= 1e6).mean(),
    "zona SIN INFORMACION (%)": 100 * (g.tipo_predio_zona == "SIN INFORMACION").mean(),
    "rural (%)": 100 * (g.tipo_predio_zona == "RURAL").mean(),
    "documento sin número de escritura (%)": 100 * g.doc_sin_numero.mean(),
    "escritura con varios predios, de los documentos con número (%)":
        100 * (n_predios_doc[g.index[~g.doc_sin_numero]] > 1).mean(),
    "valor redondo, de los > 1 M (%)": 100 * (g.valor[g.valor > 1e6] % 1e6 == 0).mean()}), include_groups=False)

# ---------------------------------------------------------------- 2. limpieza (reglas de limpieza_amb.py)
d = cv.rename(columns={"f": "fecha"})
embudo = [("Compraventas 2015-2023 (cód. 125)", d.groupby("ambito").size())]
def paso(nombre, conservar):
    global d
    d = d[conservar]
    embudo.append((nombre, d.groupby("ambito").size()))
paso("Fecha válida", d.fecha.notna())
paso("Valor > COP 1 M", d.valor > 1e6)
paso("Un solo valor en la anotación", d.tiene_mas_de_un_valor == "0")
paso("Duplicado exacto (folio, fecha, valor): queda uno", ~d.duplicated(["matricula", "fecha", "valor"]))
paso("Mismo folio y fecha con valores distintos: salen todos", ~d.duplicated(["matricula", "fecha"], keep=False))
paso("Documento con número de escritura", ~d.doc_sin_numero)
n_pred = d.groupby(["ambito", "documento_justificativo"]).matricula.transform("nunique")
paso("Escritura de un solo predio", n_pred == 1)
zona_folio = d[d.tipo_predio_zona != "SIN INFORMACION"].groupby("matricula").tipo_predio_zona.first()
sin = d.tipo_predio_zona == "SIN INFORMACION"
d.loc[sin, "tipo_predio_zona"] = d.loc[sin, "matricula"].map(zona_folio).fillna("SIN INFORMACION")

# ---------------------------------------------------------------- 3. pares
d = d.sort_values(["matricula", "fecha"])
prev = d.groupby("matricula")[["fecha", "valor", "documento_justificativo"]].shift()
p = d.assign(fecha_ant=prev.fecha, valor_ant=prev.valor, doc_ant=prev.documento_justificativo
             ).dropna(subset=["fecha_ant"])
pares = [("Pares consecutivos del mismo folio", p.groupby("ambito").size())]
p = p[(p.fecha - p.fecha_ant).dt.days >= 365].copy()
pares.append(("Pares con >= 365 días", p.groupby("ambito").size()))
p["razon"] = p.valor / p.valor_ant
fis = a[a.cod_natujur.isin(CAMBIO_FISICO)][["matricula", "f"]]
x = p[["matricula", "fecha", "fecha_ant"]].reset_index().merge(fis, on="matricula")
x = x[(x.f > x.fecha_ant) & (x.f <= x.fecha)]
p["cambio_fisico"] = p.index.isin(x["index"])
pares.append(("Pares sin cambio físico", p[~p.cambio_fisico].groupby("ambito").size()))
p["para_indice"] = ~p.cambio_fisico & ~((p.razon >= 5) | (p.razon <= 0.2))
pares.append(("Pares para el índice (sin cambios de 5 veces o más)", p[p.para_indice].groupby("ambito").size()))

# ---------------------------------------------------------------- 4. variables y segmentos (notebook 03)
p["fesc1"] = fecha_escritura(p.doc_ant).fillna(p.fecha_ant)
p["fesc2"] = fecha_escritura(p.documento_justificativo).fillna(p.fecha)
p["anios"] = (p.fecha - p.fecha_ant).dt.days / 365.25
p["g"] = p.razon ** (1 / p.anios) - 1
p["congelado"] = p.razon == 1
fac = lambda a1, a2: np.prod([1 + REAJUSTE.get(t, 0.03) for t in range(int(a1) + 1, int(a2) + 1)])
p["factor_decreto"] = [fac(i, j) for i, j in zip(p.fesc1.dt.year, p.fesc2.dt.year)]
p["replica_decreto"] = ((p.razon / p.factor_decreto - 1).abs() < 0.005) & ~p.congelado
p["segmento"] = np.select(
    [p.congelado, p.replica_decreto, p.g < 0, p.g <= 0.05],
    ["1 Valor congelado", "2 Réplica del reajuste", "5 Caída", "3 Crecimiento bajo (0-5%)"],
    default="4 Crecimiento de mercado (>5%)")
p["zona"] = p.tipo_predio_zona.where(p.tipo_predio_zona.isin(["URBANO", "RURAL"]), "SIN INFORMACION")
p["grupo"] = p.ambito + " " + p.zona.str.lower()
p["periodo"] = np.select([p.fesc1 >= "2019-01-01", p.fesc2 >= "2019-01-01"], ["C ambas 2019+", "B cruza 2019"],
                         default="A ambas <2019")
hip = set(zip(a.loc[a.cod_natujur.isin(HIPOTECA), "matricula"], a.loc[a.cod_natujur.isin(HIPOTECA), "f"].dt.normalize()))
d["hipoteca_mismo_dia"] = [(m, f) in hip for m, f in zip(d.matricula, d.fecha.dt.normalize())]
d["zona"] = d.tipo_predio_zona.where(d.tipo_predio_zona.isin(["URBANO", "RURAL"]), "SIN INFORMACION")

pi = p[p.para_indice & (p.zona != "SIN INFORMACION")].copy()
p["grupo"] = p.grupo.str.replace("Art49", "Art. 49")
pi["grupo"] = pi.grupo.str.replace("Art49", "Art. 49")
GRUPOS = ["AMB urbano", "AMB rural", "Art. 49 urbano", "Art. 49 rural", "Otros urbano", "Otros rural"]


def indice_bmn(df):
    A = np.zeros((len(df), len(ANIOS)))
    a1, a2 = df.fecha_ant.dt.year.to_numpy(), df.fecha.dt.year.to_numpy()
    for j, t in enumerate(ANIOS):
        A[:, j] = (a2 == t).astype(float) - (a1 == t).astype(float)
    b = np.linalg.lstsq(A, np.log(df.razon.to_numpy()), rcond=None)[0]
    return pd.Series(np.r_[100, 100 * np.exp(b)], index=[2015] + ANIOS)


indices = pd.DataFrame({g: indice_bmn(pi[pi.grupo == g]) for g in GRUPOS})
indices["Reajuste por decreto"] = [100 * np.prod([1 + REAJUSTE[t] for t in range(2016, y + 1)]) for y in indices.index]
tasa = lambda s, i, j: 100 * ((s[j] / s[i]) ** (1 / (j - i)) - 1)

# ---------------------------------------------------------------- 5. reporte
pd.set_option("display.width", 200)
def tabla(serie_por_ambito):
    return " | ".join(f"{k} {v:,}" for k, v in serie_por_ambito.items())

salida = io.StringIO()
with redirect_stdout(salida):
    print("ENTENDIMIENTO DE LAS COMPRAVENTAS DE SANTANDER (AMB frente a los otros municipios)")
    print("\n1. CALIDAD ANTES DE LIMPIAR")
    print(calidad.T.round(1).to_string())
    print(f"  Compraventas sin valor en toda Santander: {int(cv.valor.isna().sum()):,} (en la API, tiene_valor = 0 "
          f"cuenta {51_689:,}; ver LEEME_santander.json)")
    sv = cv[cv.ambito == "Art49"]
    print("  Art. 49, sin valor por zona (%): " + " | ".join(
        f"{k} {v:.1f}" for k, v in (100 * sv.valor.isna().groupby(sv.tipo_predio_zona).mean()).items()))
    print("  Documentos sin número de escritura: " + " | ".join(
        f"{k} {v:,}" for k, v in cv[cv.doc_sin_numero].groupby("ambito").size().items())
        + f"; textos: {cv[cv.doc_sin_numero].documento_justificativo.value_counts().to_dict()}"
        + f"; con valor > COP 1 M: {int((cv.doc_sin_numero & (cv.valor > 1e6)).sum()):,}")
    multi = g_doc[g_doc.pred > 1]
    print("  Escrituras con número y varios predios (de ellas, con predios en más de un municipio): " + " | ".join(
        f"{k} {len(g):,} ({int((g.mun > 1).sum())})" for k, g in multi.groupby(level="ambito")))
    print("\n2. EMBUDO DE LIMPIEZA (mismas reglas del AMB)")
    for n, s in embudo:
        print(f"  {n:<55}{tabla(s)}")
    print(f"  Compraventas limpias por zona: {d.groupby(['ambito', 'zona']).size().to_dict()}")
    print(f"  Municipios con compraventas limpias: {d.groupby('ambito').divipola.nunique().to_dict()}")
    print("\n3. PARES DE VENTAS REPETIDAS")
    for n, s in pares:
        print(f"  {n:<55}{tabla(s)}")
    print(f"  Pares para el índice por grupo: {pi.grupo.value_counts().reindex(GRUPOS).to_dict()}")
    print(f"  Pares para el índice sin zona (fuera de los grupos): {int((p.para_indice & (p.zona == 'SIN INFORMACION')).sum())}")
    pr = p[p.para_indice & (p.ambito == "Art49")].groupby("divipola").size()      # incluye pares sin zona
    pr_rural = pi[pi.grupo == "Art. 49 rural"].groupby("divipola").size()
    print(f"  Art. 49: municipios con al menos un par para el índice (con o sin zona) {pr.size} de 68; "
          f"con 30 o más {int((pr >= 30).sum())}; "
          f"con 30 o más pares rurales {int((pr_rural >= 30).sum())}; mediana de pares rurales por municipio "
          f"{pr_rural.reindex(sorted(ART49), fill_value=0).median():.0f}")
    print(f"  Mediana de la razón de precios: con cambio físico {p[p.cambio_fisico].razon.median():.2f}; "
          f"sin cambio físico {p[~p.cambio_fisico].razon.median():.2f}")
    print("\n4. SEGMENTOS DE LOS PARES PARA EL ÍNDICE (% por grupo)")
    seg = pd.crosstab(pi.segmento, pi.grupo, normalize="columns").reindex(columns=GRUPOS) * 100
    print(seg.round(1).to_string())
    print("  Patrón de avalúo (segmentos 1 a 3): " + " | ".join(
        f"{g} {seg.loc[seg.index.str[0].isin(list('123')), g].sum():.1f}%" for g in GRUPOS))
    print("  Variación anual mediana: " + " | ".join(f"{g} {100 * pi[pi.grupo == g].g.median():.1f}%" for g in GRUPOS))
    print("\n5. QUIEBRE DE 2019: % de réplica del reajuste y de crecimiento de mercado por periodo de las escrituras")
    for g in GRUPOS:
        q = pi[pi.grupo == g]
        t = pd.crosstab(q.segmento, q.periodo, normalize="columns") * 100
        rep = t.loc["2 Réplica del reajuste"] if "2 Réplica del reajuste" in t.index else pd.Series(0, t.columns)
        mer = t.loc["4 Crecimiento de mercado (>5%)"]
        print(f"  {g:<13} réplica: " + ", ".join(f"{c[2:]} {rep.get(c, 0):.1f}%" for c in sorted(t.columns))
              + " | mercado: " + ", ".join(f"{c[2:]} {mer.get(c, 0):.1f}%" for c in sorted(t.columns))
              + f" | pares {q.periodo.value_counts().sort_index().to_dict()}")
    print("\n6. ÍNDICE BAILEY-MUTH-NOURSE (2015 = 100, mínimos cuadrados, como el notebook 03)")
    print(indices.round(1).to_string())
    print("  Crecimiento anual (%): tramo | " + " | ".join(indices.columns))
    for i, j in [(2015, 2018), (2018, 2019), (2019, 2023), (2015, 2023)]:
        print(f"  {i}-{j} | " + " | ".join(f"{tasa(indices[c], i, j):.1f}" for c in indices.columns))
    print("\n7. HIPOTECA REGISTRADA EL MISMO DÍA (% de las compraventas limpias)")
    print("  " + " | ".join(f"{k[0]} {k[1].lower()} {100 * v:.1f}%" for k, v in
                           d[d.zona != "SIN INFORMACION"].groupby(["ambito", "zona"]).hipoteca_mismo_dia.mean().items()))
print(salida.getvalue())
(BASE / "resultados_entendimiento_santander.txt").write_text(salida.getvalue(), encoding="utf-8")
p.drop(columns=["f"], errors="ignore").to_csv(BASE / "pares_santander.csv", index=False, encoding="utf-8")

# Control: el AMB debe reproducir el piloto ya entregado (limpieza_amb.py)
assert int(cv.valor.isna().sum()) == 51_689, "cambió el número de compraventas sin valor"
n_amb = dict(embudo)["Escritura de un solo predio"]["AMB"]
assert n_amb == 133_720 and dict(pares)["Pares para el índice (sin cambios de 5 veces o más)"]["AMB"] == 13_978, n_amb

# Figura: índice por grupo frente al reajuste
fig, ax = plt.subplots(figsize=(10, 4.8))
SERIES_FIG = ["AMB urbano", "AMB rural", "Art. 49 urbano", "Art. 49 rural", "Reajuste por decreto"]   # las de la tabla
for c, col in zip(SERIES_FIG, ["#1f4e79", "#7fa7d6", "#b03a2e", "#e6a19b", "grey"]):
    ax.plot(indices.index, indices[c], marker=None if "decreto" in c else "o", ls="--" if "decreto" in c else "-",
            color=col, label=c)
ax.axvline(2018.5, ls=":", c="grey")
ax.text(2018.6, ax.get_ylim()[1] * 0.98, "Ley 1943", fontsize=8, va="top", color="grey")
ax.set_title("Índice de ventas repetidas en Santander por grupo (2015 = 100)", fontweight="bold")
ax.set_ylabel("Índice")
ax.legend(frameon=False, fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "fig_entendimiento_santander.png", dpi=300, bbox_inches="tight")
