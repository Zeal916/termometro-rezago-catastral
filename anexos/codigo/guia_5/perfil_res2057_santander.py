"""Perfil de la Resolución IGAC 2057 de 2025 (ajuste del Art. 49, Ley 2294 de 2023) en los municipios de Santander.

Usa las salidas ya calculadas por analisis_guia1.py (extracción de la resolución por zona homogénea geoeconómica e
índices de ventas repetidas por municipio y zona). No descarga nada.
Uso: python perfil_res2057_santander.py  -> imprime y escribe resultados_res2057_santander.txt,
     res2057_santander_municipios.csv y fig_res2057_santander.png
"""
import io
import json
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
SAL = BASE.parents[1] / "datos" / "guia_1"  # salidas de codigo/guia_1/analisis_guia1.py
# Avalúo 2015 = 100 con la misma serie de reajuste del índice exploratorio del AMB (notebook 03): 3% anual 2016-2022
# y 4,31% en 2023 = 128,3. En predios rurales agropecuarios el reajuste sigue los precios al productor (Ley 101 de 1993),
# así que es una referencia.
REAJUSTE_2023 = 100 * 1.03 ** 7 * 1.0431
NOMBRE = {"CHARALA": "Charalá", "CONCEPCION": "Concepción", "SAN JOSE DE MIRANDA": "San José de Miranda",
          "SAN ANDRES": "San Andrés"}
DESPLAZA = {"CHARALA": (-38, 4), "CONCEPCION": (-52, -10), "SAN JOSE DE MIRANDA": (4, 6), "PUENTE NACIONAL": (4, 4)}
VECES_MEDIANA = 3            # regla de consistencia propuesta en el AMEF (plan A3): zona con aumento > 3 veces la mediana

cifras = json.load(open(SAL / "cifras.json", encoding="utf-8"))
z = pd.read_csv(SAL / "res2057_zonas.csv", dtype={"div": str, "zhg": str})
m = pd.read_csv(SAL / "art49_municipios.csv", dtype={"div": str})
ix = pd.read_csv(SAL / "indices_municipio_zona.csv", dtype={"div": str})

zs = z[z["div"].str[:2] == "68"].copy()
ms = m[m["div"].str[:2] == "68"].copy()

# Dispersión dentro de cada municipio y regla de consistencia
zs["mediana_mun"] = zs.groupby("div").pct.transform("median")
zs["sobre_3x"] = zs.pct > VECES_MEDIANA * zs.mediana_mun
disp = zs.groupby("div").pct.agg(p25=lambda s: s.quantile(.25), p75=lambda s: s.quantile(.75))
ms = ms.join(disp, on="div")
ms["zonas_sobre_3x"] = ms["div"].map(zs.groupby("div").sobre_3x.sum())
ms["factor_mediano"] = 1 + ms.pct_mediana / 100                     # multiplica el avalúo por este factor
ms["mercado_sobre_reajuste"] = ms.idx2023_rural / REAJUSTE_2023      # cuánto subió el mercado frente al decreto, 2015-2023

con = ms[ms.idx2023_rural.notna()].sort_values("idx2023_rural", ascending=False)
rho = con[["idx2023_rural", "pct_mediana"]].corr("spearman").iloc[0, 1]

# Comprobación contra el PDF con un patrón distinto al de la extracción original (mismo lector de texto, pdfplumber).
# PDF: copia pública de Camacol guardada en esta carpeta
import pdfplumber
import re
paginas = pdfplumber.open(BASE / "res2057.pdf").pages
texto = "\n".join((p.extract_text() or "") for p in paginas)
pag_do = re.findall(r"(?:DIARI\s?O\s+OFICIAL\s+(\d{3}))|(?:^(\d{3})\s+DIARIO)", texto, flags=re.M)
pag_do = sorted({int(a or b) for a, b in pag_do})
v = pd.DataFrame(re.findall(r"\b(68\d{3})\b\D{0,60}?\b(\d{2,3})\s+([\d\.]+,\d+)\s*%", texto),
                 columns=["div", "zhg", "pct"]).drop_duplicates(["div", "zhg"])
v["pct"] = v.pct.str.replace(".", "", regex=False).str.replace(",", ".").astype(float)
cruce = zs.merge(v, on=["div", "zhg"], how="outer", suffixes=("", "_pdf"), indicator=True)
ver = (int((cruce._merge == "both").sum()), int((cruce._merge != "both").sum()),
       int((cruce.pct != cruce.pct_pdf)[cruce._merge == "both"].sum()))

nac = z.pct
salida = io.StringIO()
with redirect_stdout(salida):
    print("PERFIL DE LA RESOLUCIÓN 2057 DE 2025 EN SANTANDER")
    print("\n1. COMPLETITUD DE LA EXTRACCIÓN (todo el país)")
    print(f"  PDF: {len(paginas)} páginas, del Diario Oficial páginas {pag_do[0]} a {pag_do[-1]}")
    print(f"  Porcentajes en el texto del PDF: {cifras['res2057_porcentajes_en_texto']:,}; filas extraídas: "
          f"{cifras['res2057_filas_extraidas']:,}; zonas válidas sin duplicar: {len(z):,} de {z['div'].nunique()} municipios")
    print(f"  Santander: {len(zs):,} zonas ({len(zs) / len(z):.1%} del país) en {zs['div'].nunique()} municipios")
    print(f"  Zonas por municipio en Santander: mínimo {ms.zonas.min()}, mediana {ms.zonas.median():.0f}, máximo {ms.zonas.max()}")
    print(f"  Aumentos faltantes o negativos: {int(zs.pct.isna().sum())} / {int((zs.pct < 0).sum())}")
    print(f"  Verificación contra el PDF (otro patrón): {ver[0]:,} zonas en ambas, {ver[1]} en una sola, "
          f"{ver[2]} con valor distinto")

    print("\n2. DISTRIBUCIÓN DEL AUMENTO POR ZONA (%)")
    q = [.10, .25, .50, .75, .90]
    print("  Percentiles 10/25/50/75/90  Santander: " + " / ".join(f"{zs.pct.quantile(p):,.0f}" for p in q)
          + f" | máximo {zs.pct.max():,.0f}")
    print("                              País:      " + " / ".join(f"{nac.quantile(p):,.0f}" for p in q))
    print(f"  Zonas con 4% exacto: Santander {(zs.pct == 4).sum():,} ({(zs.pct == 4).mean():.1%}); "
          f"país {(nac == 4).sum():,} ({(nac == 4).mean():.1%})")
    print(f"  Zonas con más de 1.000%: Santander {(zs.pct > 1000).sum():,} ({(zs.pct > 1000).mean():.1%}); "
          f"país {(nac > 1000).sum():,} ({(nac > 1000).mean():.1%})")
    print(f"  Mediana municipal del aumento en Santander: p25 {ms.pct_mediana.quantile(.25):,.0f}, "
          f"p50 {ms.pct_mediana.median():,.0f}, p75 {ms.pct_mediana.quantile(.75):,.0f}")

    print(f"\n3. CONSISTENCIA DENTRO DE CADA MUNICIPIO (zona con aumento mayor a {VECES_MEDIANA} veces la mediana del municipio)")
    print(f"  Zonas marcadas: {zs.sobre_3x.sum():,} ({zs.sobre_3x.mean():.1%}) en {(ms.zonas_sobre_3x > 0).sum()} de "
          f"{len(ms)} municipios")
    print(f"  Razón p75/p25 del aumento dentro del municipio: mediana {(ms.p75 / ms.p25).median():.1f}, "
          f"máximo {(ms.p75 / ms.p25).max():.1f}")
    top = zs.sort_values("pct", ascending=False).head(5)
    print("  Cinco zonas con mayor aumento: " + "; ".join(
        f"{r.municipio} zona {r.zhg}: {r.pct:,.0f}% (mediana del municipio {r.mediana_mun:,.1f}%)" for r in top.itertuples()))

    print("\n4. COBERTURA CON EVIDENCIA DE MERCADO (pares de ventas repetidas 2015-2023)")
    print(f"  Municipios con 30 o más pares rurales: {(ms.pares_RURAL >= 30).sum()} | con índice rural propio "
          f"(30 pares y 5 por año): {len(con)} | con índice urbano propio: {int(ms.indice_urbano.sum())}")
    print(f"  Pares rurales por municipio: mediana {ms.pares_RURAL.median():.0f}; municipios con 0 pares rurales: "
          f"{(ms.pares_RURAL == 0).sum()}")
    print(f"  Zonas cubiertas por los {len(con)} municipios con índice rural: "
          f"{zs['div'].isin(con['div']).sum():,} de {len(zs):,}")

    print(f"\n5. CONTRASTE EXPLORATORIO EN LOS {len(con)} MUNICIPIOS CON ÍNDICE RURAL (sin año de última actualización)")
    print(f"  Índice rural 2023 (2015 = 100): mediana {con.idx2023_rural.median():.0f}, rango "
          f"{con.idx2023_rural.min():.0f} a {con.idx2023_rural.max():.0f}; reajuste acumulado {REAJUSTE_2023:.1f}")
    print(f"  Mercado/reajuste: mediana {con.mercado_sobre_reajuste.median():.2f}")
    print(f"  Municipios con índice rural mayor al reajuste: {(con.idx2023_rural > REAJUSTE_2023).sum()} de {len(con)}")
    print(f"  Spearman entre índice rural 2023 y aumento mediano: {rho:.2f} (n = {len(con)})")
    print("  Municipio | pares rurales | índice 2023 | mercado/reajuste | aumento mediano % | p25-p75 | zonas >3x")
    for r in con.itertuples():
        print(f"  {r.municipio:<22}{r.pares_RURAL:>6.0f}{r.idx2023_rural:>9.0f}{r.mercado_sobre_reajuste:>9.2f}"
              f"{r.pct_mediana:>11,.1f}   {r.p25:,.1f}-{r.p75:,.1f}{r.zonas_sobre_3x:>6.0f}")
print(salida.getvalue())
(BASE / "resultados_res2057_santander.txt").write_text(salida.getvalue(), encoding="utf-8")
ms.drop(columns=["indice_urbano"]).assign(indice_urbano=ms.indice_urbano).to_csv(
    BASE / "res2057_santander_municipios.csv", index=False, encoding="utf-8")

coma = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", "."))
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
bins = np.logspace(np.log10(4), np.log10(zs.pct.max()), 40)
ax[0].hist(zs.pct, bins=bins, color="#5d6d7e")
ax[0].set_xscale("log")
ax[0].xaxis.set_major_formatter(coma)
ax[0].set_title(f"Aumento por zona en Santander ({len(zs):,} zonas)".replace(",", "."), fontweight="bold")
ax[0].set_xlabel("Aumento del avalúo (%; escala logarítmica)")
ax[0].set_ylabel("Zonas")
ax[1].scatter(con.idx2023_rural, con.pct_mediana, color="#b03a2e")
for r in con.itertuples():
    ax[1].annotate(NOMBRE.get(r.municipio, r.municipio.title()), (r.idx2023_rural, r.pct_mediana), fontsize=7,
                   xytext=DESPLAZA.get(r.municipio, (3, 3)), textcoords="offset points")
ax[1].axvline(REAJUSTE_2023, ls="--", c="grey")
ax[1].text(REAJUSTE_2023 + 2, ax[1].get_ylim()[1] * 0.95, "reajuste por decreto 2015-2023", fontsize=8, color="grey",
           va="top")
ax[1].yaxis.set_major_formatter(coma)
ax[1].set_title(f"Índice rural 2023 y aumento mediano ({len(con)} municipios)", fontweight="bold")
ax[1].set_xlabel("Índice rural de ventas repetidas 2023 (2015 = 100)")
ax[1].set_ylabel("Aumento mediano del municipio (%)")
for a in ax:
    a.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "fig_res2057_santander.png", dpi=300, bbox_inches="tight")

# Control: deben coincidir con las cifras ya publicadas
assert len(ms) == cifras["santander_art49"] == 68 and len(con) == cifras["santander_art49_indice_rural"] == 15
assert ver == (len(zs), 0, 0), "la extracción no coincide con el PDF"
