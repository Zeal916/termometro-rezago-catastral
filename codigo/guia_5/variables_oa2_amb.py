"""Variables del folio para el clasificador de escrituras (OA2) en el piloto del AMB.

Repite el análisis de importancia del entendimiento de datos (notebook 03_entendimiento.ipynb, técnica 8: bosque
aleatorio, 30% de prueba, semilla 0) y le agrega tres variables del folio: hipoteca registrada el mismo día de la
venta, propiedad horizontal y primera venta de un folio nuevo. Compara el AUC con y sin ellas.

Entradas: compraventas_limpias.csv y pares_amb.csv (salidas de limpieza_amb.py) y la base cruda del AMB con todos
los actos (datos/amb_7y2j-43cv.csv).
Uso: python variables_oa2_amb.py  -> imprime resultados, escribe resultados_variables_oa2.txt y fig_importancia_oa2.png
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
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split

BASE = Path(__file__).resolve().parent
PROYECTO = BASE.parents[1]  # raíz del repositorio
G4 = PROYECTO / "datos"  # salidas de codigo/guia_4/limpieza_amb.py
CRUDA = PROYECTO / "datos" / "guia_5" / "amb_7y2j-43cv.csv"  # todos los actos del AMB; no versionado
SEMILLA = 0

HIPOTECA = ["203", "204", "205", "219"]   # hipoteca, abierta, cuantía indeterminada, abierta sin límite de cuantía
PH = ["317", "331", "347"]                # constitución, reforma y adición del reglamento de propiedad horizontal


def fecha(texto):
    """Fecha de radicación: 'AAAA-MM-DD hh:mm:ss' o 'dd/mm/aa' (igual que limpieza_amb.py)."""
    return pd.to_datetime(texto, format="%Y-%m-%d %H:%M:%S", errors="coerce").fillna(
        pd.to_datetime(texto, format="%d/%m/%y", errors="coerce"))


def fecha_escritura(texto):
    """Fecha de la escritura dentro de documento_justificativo (igual que el notebook 03)."""
    d = texto.str.extract(r"(\d{1,2}/\d{1,2}/\d{2,4})")[0]
    return pd.to_datetime(d, format="%d/%m/%Y", errors="coerce").fillna(
        pd.to_datetime(d, format="%d/%m/%y", errors="coerce"))


# ---------------------------------------------------------------- 1. pares (mismo subconjunto del notebook 03)
ventas = pd.read_csv(G4 / "compraventas_limpias.csv", dtype={"matricula": str, "pk": str})
pares = pd.read_csv(G4 / "pares_amb.csv", dtype={"matricula": str, "pk": str})
for df, cols in ((ventas, ["fecha"]), (pares, ["fecha", "fecha_ant"])):
    for c in cols:
        df[c] = pd.to_datetime(df[c])

ventas["fesc"] = fecha_escritura(ventas.documento_justificativo)
pares = pares.merge(ventas[["matricula", "fecha", "fesc"]].rename(columns={"fecha": "fecha_ant", "fesc": "fesc1"}),
                    on=["matricula", "fecha_ant"], how="left")
pares["fesc2"] = fecha_escritura(pares.documento_justificativo)
pares["fesc1"] = pares.fesc1.fillna(pares.fecha_ant)
pares["fesc2"] = pares.fesc2.fillna(pares.fecha)
pares["anios"] = (pares.fecha - pares.fecha_ant).dt.days / 365.25
pares["g"] = pares.razon ** (1 / pares.anios) - 1
pares["red1"] = pares.valor_ant % 1_000_000 == 0
pares["red2"] = pares.valor % 1_000_000 == 0
pares["cruza_ley1943"] = (pares.fesc1 < "2019-01-01") & (pares.fesc2 >= "2019-01-01")
pares["cruza_act_bga"] = pares.cruza_ley1943 & (pares.municipio == "BUCARAMANGA")

d = pares[pares.para_indice & (pares.g >= 0)].copy()
y = (d.g > 0.05).astype(int)

# ---------------------------------------------------------------- 2. variables del folio desde la base cruda
a = pd.read_csv(CRUDA, dtype=str, usecols=["matricula", "num_anotacion", "fecha_radica_texto", "fecha_apertura_texto",
                                           "cod_natujur", "nombre_natujur"])
a["f"] = fecha(a.fecha_radica_texto).dt.normalize()

# Comprobaciones sobre todo el AMB
nombres = a[a.cod_natujur.isin(HIPOTECA + PH)].groupby("cod_natujur").nombre_natujur.first()
h_todo = set(zip(a.loc[a.cod_natujur.isin(HIPOTECA), "matricula"], a.loc[a.cod_natujur.isin(HIPOTECA), "f"]))
chk_hip = np.mean([(m, f) in h_todo for m, f in zip(ventas.matricula, ventas.fecha.dt.normalize())])
n1 = a[a.num_anotacion == "1"].drop_duplicates("matricula")
ap = pd.to_datetime(n1.fecha_apertura_texto, errors="coerce").dropna()

a = a[a.matricula.isin(d.matricula)]
hip = set(zip(a.loc[a.cod_natujur.isin(HIPOTECA), "matricula"], a.loc[a.cod_natujur.isin(HIPOTECA), "f"]))
ph_primero = a[a.cod_natujur.isin(PH)].groupby("matricula").f.min()   # primer acto de PH del folio en 2015-2023
folio_nuevo = set(n1.matricula)                                        # su primera anotación está en 2015-2023
primera_cv = a[a.cod_natujur == "125"].groupby("matricula").f.min()   # primera compraventa del folio (sin limpiar)

d["hipoteca_venta_1"] = [(m, f) in hip for m, f in zip(d.matricula, d.fecha_ant.dt.normalize())]
d["hipoteca_venta_2"] = [(m, f) in hip for m, f in zip(d.matricula, d.fecha.dt.normalize())]
# Solo actos de PH registrados hasta el día de la segunda venta: nada posterior a la escritura que se clasifica
d["propiedad_horizontal"] = d.matricula.map(ph_primero) <= d.fecha.dt.normalize()
ph_despues = d.matricula.map(ph_primero) > d.fecha.dt.normalize()
d["primera_venta_folio_nuevo"] = d.matricula.isin(folio_nuevo) & (
    d.fecha_ant.dt.normalize() == d.matricula.map(primera_cv))

NUEVAS = ["hipoteca_venta_1", "hipoteca_venta_2", "propiedad_horizontal", "primera_venta_folio_nuevo"]

# ---------------------------------------------------------------- 3. bosque aleatorio con y sin las variables
X = pd.DataFrame({
    "anio_venta_1": d.fesc1.dt.year, "anio_venta_2": d.fesc2.dt.year, "anios_entre_ventas": d.anios,
    "log_valor_1": np.log(d.valor_ant), "redondo_1": d.red1.astype(int), "redondo_2": d.red2.astype(int),
    "cruza_ley1943": d.cruza_ley1943.astype(int), "cruza_act_bga": d.cruza_act_bga.astype(int),
    "rural": (d.tipo_predio_zona == "RURAL").astype(int), "num_vendedores": d.count_de,
    "num_compradores": d.count_a})
for mun in ["BUCARAMANGA", "FLORIDABLANCA", "GIRÓN", "PIEDECUESTA"]:
    X["mun_" + mun[:5]] = (d.municipio == mun).astype(int)
X_nuevo = X.assign(**{c: d[c].astype(int) for c in NUEVAS})


def comparar(idx_tr, idx_te):
    """AUC en prueba del bosque sin y con las variables del folio, con la misma partición."""
    salida = []
    for M in (X, X_nuevo):
        rf = RandomForestClassifier(n_estimators=400, min_samples_leaf=20, random_state=SEMILLA, n_jobs=-1)
        rf.fit(M.loc[idx_tr], y.loc[idx_tr])
        salida += [rf, rf.predict_proba(M.loc[idx_te])[:, 1]]
    return salida


def ic_bootstrap(idx_te, p0, p1, reps=1000):
    """IC 95% de la diferencia de AUC: bootstrap pareado sobre la prueba, remuestreando folios."""
    rng = np.random.default_rng(SEMILLA)
    y_te = y.loc[idx_te].to_numpy()
    _, inv = np.unique(d.loc[idx_te, "matricula"].to_numpy(), return_inverse=True)
    grupos = [np.flatnonzero(inv == k) for k in range(inv.max() + 1)]
    dif = []
    for _ in range(reps):
        s = np.concatenate([grupos[k] for k in rng.integers(0, len(grupos), len(grupos))])
        dif.append(roc_auc_score(y_te[s], p1[s]) - roc_auc_score(y_te[s], p0[s]))
    return np.percentile(dif, [2.5, 97.5]), len(grupos)


# (a) Réplica exacta: partición por par, estratificada, como en el notebook 03
idx_tr, idx_te = train_test_split(X.index, test_size=0.3, random_state=SEMILLA, stratify=y)
rf0, p0, rf1, p1 = comparar(idx_tr, idx_te)
y_te = y.loc[idx_te].to_numpy()
auc0, auc1 = roc_auc_score(y_te, p0), roc_auc_score(y_te, p1)
ic, n_folios_te = ic_bootstrap(idx_te, p0, p1)
perm = permutation_importance(rf1, X_nuevo.loc[idx_te], y_te, scoring="roc_auc", n_repeats=10,
                              random_state=SEMILLA, n_jobs=-1)
importancia = pd.Series(perm.importances_mean, index=X_nuevo.columns).sort_values(ascending=False)

# (b) Sensibilidad: partición por folio (ningún folio en entrenamiento y prueba a la vez)
g_tr, g_te = next(GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=SEMILLA).split(X, y, d.matricula))
gidx_tr, gidx_te = X.index[g_tr], X.index[g_te]
_, q0, _, q1 = comparar(gidx_tr, gidx_te)
gy = y.loc[gidx_te].to_numpy()
gauc0, gauc1 = roc_auc_score(gy, q0), roc_auc_score(gy, q1)
gic, _ = ic_bootstrap(gidx_te, q0, q1)
folios_compartidos = len(set(d.loc[idx_tr, "matricula"]) & set(d.loc[idx_te, "matricula"]))

# ---------------------------------------------------------------- 4. reporte y figura
salida = io.StringIO()
with redirect_stdout(salida):
    print("VARIABLES DEL FOLIO PARA OA2. PILOTO AMB")
    print(f"Pares analizados (para_indice y sin caída): {len(d):,} | % mercado (>5% anual): {y.mean():.1%}")
    print(f"Prueba: {len(idx_te):,} pares de {n_folios_te:,} folios\n")
    print("CÓDIGOS USADOS (nombre tal como viene en la base)")
    for c, n in nombres.items():
        print(f"  {c}  {n}")
    print("\nCOMPROBACIÓN DE LAS DEFINICIONES")
    print(f"  Compraventas limpias del AMB con hipoteca el mismo día: {chk_hip:.1%} de {len(ventas):,}")
    print(f"  Folios con anotación 1 en 2015-2023: {len(n1):,}; con fecha de apertura llena: {len(ap):,} "
          f"(desde {ap.min():%Y-%m-%d}); abiertos antes de 2015: {(ap.dt.year < 2015).sum():,}")
    print(f"  Pares cuyo primer acto de PH es posterior a la segunda venta (no se marcan como PH): {ph_despues.sum():,}\n")
    print("PREVALENCIA Y % DE PARES DE MERCADO SEGÚN CADA VARIABLE")
    for c in NUEVAS:
        si, no = y[d[c]], y[~d[c]]
        print(f"  {c:<28} presente en {d[c].mean():6.1%} de los pares | mercado: con {si.mean():6.1%} "
              f"(n={len(si):,}) / sin {no.mean():6.1%} (n={len(no):,})")
    print("\nAUC EN PRUEBA (bosque aleatorio, 400 árboles, hoja mínima 20, semilla 0)")
    print("  (a) Partición por par, estratificada (réplica exacta del notebook 03)")
    print(f"      Variables del registro:            {auc0:.3f}")
    print(f"      Más las 4 variables del folio:     {auc1:.3f}")
    print(f"      Diferencia: {auc1 - auc0:+.3f} (IC 95%: {ic[0]:+.3f} a {ic[1]:+.3f})")
    print(f"      Folios con pares en entrenamiento y en prueba a la vez: {folios_compartidos:,}")
    print(f"  (b) Partición por folio (sensibilidad): {len(gidx_te):,} pares de prueba")
    print(f"      Variables del registro:            {gauc0:.3f}")
    print(f"      Más las 4 variables del folio:     {gauc1:.3f}")
    print(f"      Diferencia: {gauc1 - gauc0:+.3f} (IC 95%: {gic[0]:+.3f} a {gic[1]:+.3f})")
    print("  IC 95%: bootstrap pareado sobre la prueba, 1.000 réplicas remuestreando folios, con los modelos fijos")
    print("\nIMPORTANCIA POR PERMUTACIÓN CON LAS VARIABLES DEL FOLIO, PARTICIÓN (a) (caída del AUC, 10 repeticiones)")
    for k, v in importancia.items():
        print(f"  {k:<28}{v:9.5f}")
print(salida.getvalue())
(BASE / "resultados_variables_oa2.txt").write_text(salida.getvalue(), encoding="utf-8")

ETIQUETAS = {
    "log_valor_1": "Logaritmo del valor de la primera venta", "hipoteca_venta_2": "Hipoteca el día de la segunda venta",
    "redondo_2": "Segunda venta con valor redondo", "anios_entre_ventas": "Años entre ventas",
    "hipoteca_venta_1": "Hipoteca el día de la primera venta", "anio_venta_2": "Año de la segunda escritura",
    "propiedad_horizontal": "Propiedad horizontal", "redondo_1": "Primera venta con valor redondo",
    "cruza_ley1943": "Cruza la Ley 1943", "primera_venta_folio_nuevo": "Primera venta de un folio nuevo",
    "mun_BUCAR": "Bucaramanga", "cruza_act_bga": "Cruza la actualización de Bucaramanga",
    "anio_venta_1": "Año de la primera escritura", "mun_GIRÓN": "Girón", "mun_FLORI": "Floridablanca",
    "mun_PIEDE": "Piedecuesta", "rural": "Zona rural", "num_vendedores": "Número de vendedores",
    "num_compradores": "Número de compradores"}
coma = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.2f}".replace(".", ","))
fig, ax = plt.subplots(figsize=(10, 5.5))
serie = importancia.iloc[::-1]
colores = ["#b03a2e" if c in NUEVAS else "#5d6d7e" for c in serie.index]
serie.rename(ETIQUETAS).plot.barh(ax=ax, color=colores)
ax.xaxis.set_major_formatter(coma)
ax.set_title(f"Importancia de variables con las variables del folio (AUC = {auc1:.2f})".replace(".", ","),
             fontweight="bold")
ax.set_xlabel("Caída del AUC al permutar la variable (en rojo, variables del folio)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "fig_importancia_oa2.png", dpi=300, bbox_inches="tight")

# Control: si falla, el subconjunto o el modelo base ya no son los del análisis original
assert len(d) == 12_467 and round(y.mean(), 3) == 0.413 and round(auc0, 3) == 0.676, "no reproduce el análisis original"
