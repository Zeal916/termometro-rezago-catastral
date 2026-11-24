"""Vigencia de la última actualización catastral rural en los 68 municipios de Santander del Art. 49.

1. Descarga (si falta) la memoria técnica de cada municipio publicada por el IGAC y busca en el texto una
   declaración del año de la última formación o actualización.
2. Comprueba que cada memoria cite la regla de exclusión de la Ley 2294 de 2023 (predios formados o actualizados en
   los cinco años previos al 19 de mayo de 2023), que da la cota: última actualización rural en 2017 o antes.
3. Calcula la relación implícita entre el avalúo vigente y el valor comercial: la memoria aplica el 60% al valor
   comercial y fija el aumento para cerrar la brecha, así que avalúo vigente / valor comercial = 0,6 / (1 + aumento).
   No aplica a las zonas con 4%, donde el avalúo vigente se consideró acorde al mercado.
4. Para los 15 municipios con índice rural propio, calcula los años de rezago que implica esa relación si el mercado
   hubiera superado al reajuste siempre al ritmo medido en 2015-2023, partiendo de un avalúo entre 60% y 100% del
   valor comercial en la última actualización. Es un ejercicio exploratorio de consistencia.
Uso: python vigencias_santander.py -> resultados_vigencias_santander.txt y vigencias_santander_municipios.csv
"""
import io
import re
import urllib.parse
import urllib.request
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import pandas as pd
import pdfplumber

BASE = Path(__file__).resolve().parent
PDFS = BASE.parents[2] / "datos" / "memorias_art49_santander"
REAJUSTE_2023 = 100 * 1.03 ** 7 * 1.0431          # misma referencia de las secciones anteriores (128,3)
COTA = 2017                                        # última actualización posible para entrar al Art. 49

enl = pd.read_csv(BASE / "memorias_art49_santander_enlaces.csv", dtype={"div": str})
mun = pd.read_csv(BASE / "res2057_santander_municipios.csv", dtype={"div": str})
z = pd.read_csv(BASE.parents[1] / "Entrega 1" / "Guia1_v2_Termometro_Catastral" / "analisis" / "salidas" / "res2057_zonas.csv",
                dtype={"div": str, "zhg": str})
z = z[z["div"].isin(mun["div"])].copy()

# ---------------------------------------------------------------- 1 y 2. memorias técnicas
PDFS.mkdir(parents=True, exist_ok=True)
# Busca años de 1950 a 2019 hasta 60 caracteres después de la expresión clave; complementado con lectura manual
AÑO_DECLARADO = re.compile(r"(?i)(?:[uú]ltima\s+(?:actualizaci[oó]n|formaci[oó]n)|vigencia\s+catastral|"
                           r"actualizad[oa]s?\s+en|formad[oa]s?\s+en)[^.]{0,60}?\b(19[5-9]\d|20[01]\d)\b")
REGLA = re.compile(r"cinco\s+a[ñn]os\s+previos\s+al\s+19\s+de\s+mayo\s+de\s+2023", re.I)
filas = []
for r in enl.itertuples():
    destino = PDFS / f"{r.div}.pdf"
    if not destino.exists():
        req = urllib.request.Request(urllib.parse.quote(r.url, safe=":/%"), headers={"User-Agent": "Mozilla/5.0"})
        destino.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    with pdfplumber.open(destino) as pdf:
        t = "\n".join((p.extract_text() or "") for p in pdf.pages)
        paginas = len(pdf.pages)
    filas.append({"div": r.div, "paginas": paginas, "texto": len(t),
                  "anios_declarados": sorted(set(AÑO_DECLARADO.findall(t))), "cita_regla_5_anios": bool(REGLA.search(t))})
memo = pd.DataFrame(filas)

# ---------------------------------------------------------------- 3. relación avalúo vigente / valor comercial
z["av_vc"] = np.where(z.pct == 4, np.nan, 0.6 / (1 + z.pct / 100))
rel = z.groupby("div").agg(zonas=("zhg", "size"), zonas_4pct=("pct", lambda s: int((s == 4).sum())),
                           av_vc_mediana=("av_vc", "median"), av_vc_min=("av_vc", "min"), av_vc_max=("av_vc", "max"))
out = mun[["div", "municipio", "pares_RURAL", "idx2023_rural", "pct_mediana"]].join(rel, on="div").merge(memo, on="div")

# ---------------------------------------------------------------- 4. años de rezago implícitos (15 con índice)
con = out.idx2023_rural.notna()
exceso = (out.idx2023_rural / REAJUSTE_2023) ** (1 / 8) - 1          # cuánto supera el mercado al reajuste por año
for r0, nombre in ((0.6, "anios_desde_60"), (1.0, "anios_desde_100")):
    out[nombre] = np.where(con & (exceso > 0), np.log(r0 / out.av_vc_mediana) / np.log1p(exceso), np.nan)
out["exceso_anual_pct"] = 100 * exceso

salida = io.StringIO()
with redirect_stdout(salida):
    print("VIGENCIA DE LA ÚLTIMA ACTUALIZACIÓN RURAL, 68 MUNICIPIOS DE SANTANDER DEL ART. 49")
    print(f"\n1. Memorias técnicas leídas: {len(memo)} de {len(enl)}; páginas por memoria {memo.paginas.min()} a "
          f"{memo.paginas.max()}; todas con texto extraíble: {bool((memo.texto > 2000).all())}")
    print(f"   Memorias que declaran el año de la última formación o actualización: "
          f"{int(memo.anios_declarados.map(len).gt(0).sum())}")
    print(f"2. Memorias que citan la exclusión de predios formados o actualizados en los cinco años previos al 19 de "
          f"mayo de 2023: {int(memo.cita_regla_5_anios.sum())} de {len(memo)} -> cota: última actualización en {COTA} o antes")
    v = z.av_vc.dropna()
    print(f"\n3. Avalúo vigente / valor comercial implícito (zonas sin 4%: {len(v):,} de {len(z):,})")
    print(f"   Por zona: p10 {v.quantile(.1):.1%}, mediana {v.median():.1%}, p90 {v.quantile(.9):.1%}; "
          f"zonas bajo 10%: {(v < .1).mean():.1%}")
    Q = (.1, .25, .5, .75, .9)
    print("   Percentiles 10/25/50/75/90 por zona: " + " / ".join(f"{v.quantile(q):.1%}" for q in Q))
    print("   Percentiles 10/25/50/75/90 de la mediana municipal: " + " / ".join(f"{out.av_vc_mediana.quantile(q):.1%}" for q in Q))
    # Sensibilidad: algunas memorias (Los Santos) llaman "4%" a zonas que la resolución publica con 5%
    v10 = (0.6 / (1 + z.pct / 100)).where(z.pct > 10)
    print(f"   Sensibilidad, excluyendo también las {int(z.pct.between(4.01, 10).sum())} zonas con aumento de más de 4% "
          f"y hasta 10%: mediana por zona {v10.median():.1%}; mediana municipal {v10.groupby(z['div']).median().median():.1%}")
    print(f"\n4. Años de rezago implícitos (exploratorio), {int(con.sum())} municipios con índice rural")
    print("   Municipio | índice 2023 | exceso anual del mercado sobre el reajuste % | avalúo/comercial mediano | "
          "años si partía de 60% | años si partía de 100% | año implícito (60% / 100%)")
    for r in out[con].sort_values("anios_desde_60").itertuples():
        print(f"   {r.municipio:<22}{r.idx2023_rural:>6.0f}{r.exceso_anual_pct:>8.1f}{r.av_vc_mediana:>9.1%}"
              f"{r.anios_desde_60:>9.0f}{r.anios_desde_100:>9.0f}   {2026 - r.anios_desde_60:.0f} / {2026 - r.anios_desde_100:.0f}")
    q = out[con]
    print(f"   Años desde 60%: mediana {q.anios_desde_60.median():.0f} (rango {q.anios_desde_60.min():.0f} a "
          f"{q.anios_desde_60.max():.0f}); municipios con años implícitos menores a {2026 - COTA} (incompatibles con la "
          f"cota): {int((q.anios_desde_100 < 2026 - COTA).sum())}")
print(salida.getvalue())
(BASE / "resultados_vigencias_santander.txt").write_text(salida.getvalue(), encoding="utf-8")
out.drop(columns=["texto"]).to_csv(BASE / "vigencias_santander_municipios.csv", index=False, encoding="utf-8")
assert len(memo) == 68 and memo.cita_regla_5_anios.all()
