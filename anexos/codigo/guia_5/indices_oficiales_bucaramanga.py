"""Contraste del índice de ventas repetidas del piloto urbano con los índices oficiales de precios de vivienda.

- IVP (DANE): variación anual de los avalúos comerciales de predios urbanos habitacionales, municipio de Bucaramanga.
  Se lee de la tabla "Total nacional y 22 ciudades" de cada boletín anual (fila "Bucaramanga <año anterior> <año>").
- IPVN (DANE): variación anual (IV trimestre frente al IV trimestre anterior) del precio de la vivienda nueva,
  Bucaramanga AM (Bucaramanga, Floridablanca, Girón y Piedecuesta). Se lee de la sección "2.1 Resultados anuales por
  áreas urbanas y metropolitanas" de cada boletín del IV trimestre. En 2022 ese gráfico no trae texto extraíble y la
  variación se obtiene encadenando el año corrido al III trimestre con la variación del IV trimestre; el mismo cálculo
  sobre el total nacional reproduce la variación publicada (8,78%).
- IPVU (Banco de la República): no se compara; según BanRep (2015) su serie anual solo se desagrega para Bogotá, Cali,
  Medellín y un agregado de "otras ciudades" que incluye Bucaramanga.
Entradas: PDF oficiales en fuentes_indices_oficiales/ y pares_santander.csv (entendimiento_santander.py).
Uso: python indices_oficiales_bucaramanga.py -> resultados_indices_oficiales.txt, fig_indices_oficiales.png
"""
import io
import re
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdfplumber

BASE = Path(__file__).resolve().parent
FUENTES = BASE / "fuentes_indices_oficiales"
ANIOS = list(range(2016, 2024))
REAJUSTE = {a: 0.03 for a in range(2016, 2023)} | {2023: 0.0431}   # misma serie de las secciones anteriores


def texto(nombre):
    with pdfplumber.open(FUENTES / nombre) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)


def num(s):
    return float(s.replace(",", "."))


# ---------------------------------------------------------------- IVP: fila "Bucaramanga anterior actual"
ivp = {}
for a in ANIOS:
    t = texto(f"bol_IVP{a % 100}.pdf" if a < 2023 else f"bol-IVP-{a}.pdf")
    filas = re.findall(r"^Bucaramanga (-?\d+,\d+) (-?\d+,\d+) (-?\d+,\d+)\s*$", t, flags=re.M)
    if filas:
        ivp[a] = num(filas[0][1])
    else:  # 2022: la tabla trae la variación en la fila de cobertura; se usa el texto "Bucaramanga (x%)"
        ivp[a] = num(re.search(r"Bucaramanga \((-?\d+,\d+)%\)", t).group(1))
# Consistencia: la columna "año anterior" del boletín siguiente repite el valor de este año
for a in ANIOS:   # el boletín del año siguiente (hasta 2024) repite el valor en su columna "año anterior"
    t = texto(f"bol_IVP{(a + 1) % 100}.pdf" if a + 1 < 2023 else f"bol-IVP-{a + 1}.pdf")
    previo = re.findall(r"^Bucaramanga (-?\d+,\d+) (-?\d+,\d+) (-?\d+,\d+)\s*$", t, flags=re.M)
    if previo:
        assert num(previo[0][0]) == ivp[a], (a, previo, ivp[a])


# ---------------------------------------------------------------- IPVN: sección 2.1 de cada boletín del IV trimestre
def seccion(t, ini, fin):
    L = t.splitlines()
    i = next(k for k, l in enumerate(L) if re.search(ini, l, re.I))
    j = next(k for k, l in enumerate(L) if k > i and re.search(fin, l, re.I))
    return "\n".join(L[i:j])


ipvn = {}
for a in ANIOS:
    if a == 2022:
        continue
    s = seccion(texto(f"ipvn_IV_{a}.pdf"), r"2\.1\.? *RESULTADOS ANUALES POR [ÁA]REAS", r"2\.2\.? *RESULTADOS TRIMESTRALES")
    ipvn[a] = num(re.search(r"Bucaramanga AM ?(-?\d+,\d+)", s).group(1))
# 2022: año corrido al III trimestre (gráfico de año corrido del boletín III-2022) y trimestral del IV trimestre
t3, t4 = texto("ipvn_III_2022.pdf"), texto("ipvn_IV_2022.pdf")
s3 = seccion(t3, r"Variaciones a[ñn]o corrido, por [áa]reas", r"Variaciones anuales, por [áa]reas")
s4 = seccion(t4, r"Variaciones trimestrales, por [áa]reas", r"Fuente: DANE")
corr3, trim4 = num(re.search(r"Bucaramanga AM ?(-?\d+,\d+)", s3).group(1)), num(re.search(r"Bucaramanga AM ?(-?\d+,\d+)", s4).group(1))
tot3, tot4 = num(re.search(r"Total ?(-?\d+,\d+)", s3).group(1)), num(re.search(r"Total ?(-?\d+,\d+)", s4).group(1))
ipvn[2022] = 100 * ((1 + corr3 / 100) * (1 + trim4 / 100) - 1)
control_total = 100 * ((1 + tot3 / 100) * (1 + tot4 / 100) - 1)
assert abs(control_total - 8.78) < 0.02, control_total     # variación anual publicada del total nacional 2022


# ---------------------------------------------------------------- índices de ventas repetidas del proyecto
p = pd.read_csv(BASE / "pares_santander.csv", dtype={"divipola": str}, parse_dates=["fecha", "fecha_ant"])
p = p[p.para_indice & (p.zona == "URBANO")]


def indice_bmn(df):
    A = np.zeros((len(df), len(ANIOS)))
    a1, a2 = df.fecha_ant.dt.year.to_numpy(), df.fecha.dt.year.to_numpy()
    for j, t in enumerate(ANIOS):
        A[:, j] = (a2 == t).astype(float) - (a1 == t).astype(float)
    b = np.linalg.lstsq(A, np.log(df.razon.to_numpy()), rcond=None)[0]
    return pd.Series(np.r_[100, 100 * np.exp(b)], index=[2015] + ANIOS)


def nivel(var):  # variaciones anuales (%) a índice 2015 = 100
    return pd.Series(100 * np.cumprod([1] + [1 + var[a] / 100 for a in ANIOS]), index=[2015] + ANIOS)


tabla = pd.DataFrame({
    "Ventas repetidas, Bucaramanga urbano": indice_bmn(p[p.divipola == "68001"]),
    "IVP Bucaramanga (avalúos comerciales)": nivel(ivp),
    "Ventas repetidas, AMB urbano": indice_bmn(p[p.ambito == "AMB"]),
    "IPVN Bucaramanga AM (vivienda nueva)": nivel(ipvn),
    "Reajuste por decreto": nivel({a: 100 * REAJUSTE[a] for a in ANIOS}),
})
var = (tabla.pct_change() * 100).loc[ANIOS]
tasa = lambda s, i, j: 100 * ((s[j] / s[i]) ** (1 / (j - i)) - 1)

salida = io.StringIO()
with redirect_stdout(salida):
    print("CONTRASTE CON ÍNDICES OFICIALES (2015 = 100)")
    print(f"Pares urbanos para el índice: Bucaramanga {int((p.divipola == '68001').sum()):,}; "
          f"AMB {int((p.ambito == 'AMB').sum()):,}")
    print(f"IPVN 2022 encadenado: año corrido III trim {corr3:.2f}% y IV trim {trim4:.2f}% -> {ipvn[2022]:.2f}% "
          f"(control total nacional: {tot3:.2f}% y {tot4:.2f}% -> {control_total:.2f}%; publicado 8,78%)")
    print("\nVARIACIÓN ANUAL (%)")
    print(var.round(2).to_string())
    print("\nNIVEL (2015 = 100)")
    print(tabla.round(1).to_string())
    print("\nCRECIMIENTO ANUAL PROMEDIO POR TRAMO (%)")
    for i, j in [(2015, 2018), (2018, 2019), (2019, 2023), (2015, 2023)]:
        print(f"  {i}-{j}: " + " | ".join(f"{c} {tasa(tabla[c], i, j):.1f}" for c in tabla.columns))
    print("\nCORRELACIÓN DE LAS VARIACIONES ANUALES 2016-2023 (Pearson, n = 8)")
    print(var.corr().round(2).to_string())
print(salida.getvalue())
(BASE / "resultados_indices_oficiales.txt").write_text(salida.getvalue(), encoding="utf-8")

fig, ax = plt.subplots(figsize=(10, 4.8))
estilos = {"Ventas repetidas, Bucaramanga urbano": ("#1f4e79", "-", "o"), "IVP Bucaramanga (avalúos comerciales)": ("#1f4e79", "--", "s"),
           "Ventas repetidas, AMB urbano": ("#b03a2e", "-", "o"), "IPVN Bucaramanga AM (vivienda nueva)": ("#b03a2e", "--", "s"),
           "Reajuste por decreto": ("grey", ":", None)}
for c, (col, ls, mk) in estilos.items():
    ax.plot(tabla.index, tabla[c], color=col, ls=ls, marker=mk, label=c)
ax.axvline(2018.5, ls=":", c="grey")
ax.text(2018.6, ax.get_ylim()[1] * 0.98, "Ley 1943", fontsize=8, va="top", color="grey")
ax.set_title("Índice del proyecto frente a índices oficiales, Bucaramanga (2015 = 100)", fontweight="bold")
ax.set_ylabel("Índice")
ax.legend(frameon=False, fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "fig_indices_oficiales.png", dpi=300, bbox_inches="tight")
