"""Cifras y figuras de la Guía 1 (v2). Termómetro catastral.

Uso:  python analisis_guia1.py            (descarga lo que falte a ./datos)
      DATA=<carpeta> python analisis_guia1.py   (reusar una descarga existente)

Fuentes (todas abiertas, sin autenticación):
  - IGAC/SNR, Registro de transacciones inmobiliarias 2015-2023 (Socrata 7y2j-43cv), solo compraventas (cód. 125).
  - IGAC, Gestores catastrales de Colombia (Socrata bhcx-bx97).
  - IGAC, Resolución 2057 de 2025 (Diario Oficial 53.354): % de aumento por zona homogénea geoeconómica, Art. 49.
"""
import json, os, re, urllib.parse, urllib.request, zlib
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # raíz del repositorio
DATA = os.environ.get('DATA', os.path.join(ROOT, 'datos', 'guia_1', 'descarga'))
OUT = os.path.join(ROOT, 'datos', 'guia_1')
os.makedirs(DATA, exist_ok=True); os.makedirs(OUT, exist_ok=True)
SOC = 'https://www.datos.gov.co/resource/'
RES2057 = ('https://camacol.co/sites/default/files/descargables/'
           'IGAC%20RESOLUCION%200002057%20DEL%2030%20DE%20DICIEMBRE%20DE%202025.pdf')
YEARS = range(2015, 2024)


def get(url, path):
    if not os.path.exists(path):
        print('descargando', os.path.basename(path))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=600) as r, open(path, 'wb') as f:
            f.write(r.read())
    return path


def soql(dataset, ext='json', **q):
    return SOC + f'{dataset}.{ext}?' + urllib.parse.urlencode({f'${k}': v for k, v in q.items()})


# ---------------------------------------------------------------- 1. compraventas
for y in YEARS:
    get(soql('7y2j-43cv', 'csv', select='matricula,fecha_radica_texto,year_radica,divipola,tipo_predio_zona,'
             'count_a,count_de,documento_justificativo,valor',
             where=f"cod_natujur='125' AND year_radica='{y}'", limit=2000000), os.path.join(DATA, f'cv_{y}.csv'))
cv = pd.concat([pd.read_csv(os.path.join(DATA, f'cv_{y}.csv'), dtype=str) for y in YEARS])
cv['v'] = pd.to_numeric(cv.valor, errors='coerce')
cv['y'] = cv.year_radica.astype(int)
cv['div'] = cv.divipola.str.zfill(5)
# fecha_radica_texto mezcla yyyy-mm-dd, dd/mm/yyyy y dd/mm/yy -> se parsea explícitamente
s = cv.fecha_radica_texto.str[:10]
cv['f'] = (pd.to_datetime(s, format='%Y-%m-%d', errors='coerce')
           .fillna(pd.to_datetime(s, format='%d/%m/%Y', errors='coerce'))
           .fillna(pd.to_datetime(cv.fecha_radica_texto.str[:8], format='%d/%m/%y', errors='coerce')))
# una escritura con varios predios trae un precio global -> solo escrituras de un predio
k = cv.documento_justificativo.fillna('') + '|' + cv['div']
cv['ndeed'] = k.map(k.value_counts())
R = {'compraventas': len(cv), 'con_valor': int((cv.v > 0).sum()), 'escritura_1_predio': int((cv.ndeed == 1).sum()),
     'municipios_con_valor': int(cv.loc[cv.v > 0, 'div'].nunique())}
# otros actos del mismo folio para depurar cambios físicos y anticipar el tipo de escritura (piloto AMB en la Guía 3,
# país en el Capstone): se descargan filtrados por código, no los 30,9 M de actos
FOLIO = {'hipoteca': ('203', '204', '205', '219'), 'propiedad_horizontal': ('317',), 'construccion': ('910', '911'),
         'englobe_desenglobe': ('913', '915', '919')}
cods = [c for cs in FOLIO.values() for c in cs]
n = pd.read_csv(get(soql('7y2j-43cv', 'csv', select='cod_natujur,count(*) as n', group='cod_natujur',
                         where='cod_natujur in(' + ','.join(f"'{c}'" for c in cods) + ')'),
                    os.path.join(DATA, 'actos_folio.csv')), dtype={'cod_natujur': str}).set_index('cod_natujur').n
R['actos_folio'] = {k: int(n.reindex(cs).sum()) for k, cs in FOLIO.items()}
R['actos_folio_total'] = sum(R['actos_folio'].values())
R['actos_total'] = int(pd.read_csv(get(soql('7y2j-43cv', 'csv', select='count(*) as n'),
                                       os.path.join(DATA, 'actos_total.csv'))).n[0])

# ---------------------------------------------------------------- 2. reventas y pares de ventas repetidas
r = cv[(cv.v > 1e6) & (cv.ndeed == 1) & cv.f.notna()].sort_values(['matricula', 'f'])
g = r.groupby('matricula')
r = r.assign(pv=g.v.shift(), pf=g.f.shift(), py=g.y.shift())
q = r[r.pv.notna()].copy()                      # todas las reventas: la compraventa tiene una venta anterior
q['lr'] = np.log(q.v / q.pv)
q['dias'] = (q.f - q.pf).dt.days
q['py'] = q.py.astype(int)
q['zona'] = q.tipo_predio_zona.where(q.tipo_predio_zona.isin(['URBANO', 'RURAL']), 'OTRA')
q['dep'] = q['div'].str[:2]
# dominio de evaluación: reventas con al menos un año entre ventas (las rápidas van a reglas de calidad del dato)
qa = q[(q.dias >= 365) & (q.py < q.y)]
# pares para construir índices: además |cambio| < 5x (errores, lote que se construyó). Es un filtro de entrenamiento:
# usa el valor de la segunda venta, así que nunca se aplica al conjunto de prueba
p = qa[qa.lr.abs() < np.log(5)]
base = len(r)
R.update({'compraventas_1_predio_valor_fecha': base,
          'reventas_todas': len(q), 'reventas_pct': round(100 * len(q) / base, 1),
          'reventas_365': len(qa), 'reventas_365_pct': round(100 * len(qa) / base, 1),
          'pares': len(p), 'pares_pct': round(100 * len(p) / base, 1),
          'pares_urbanos': int((p.zona == 'URBANO').sum()), 'pares_rurales': int((p.zona == 'RURAL').sum()),
          'pares_sin_zona': int((p.zona == 'OTRA').sum())})

import statsmodels.api as sm


def diseno(d):
    return np.column_stack([(d.y.values == t).astype(float) - (d.py.values == t).astype(float) for t in YEARS[1:]])


def bmn(d, robust=True):
    """Índice Bailey-Muth-Nourse, base 2015=100: lr = sum_t b_t (D_t,2a venta - D_t,1a venta).
    robust=True estima por mediana (LAD): la distribución de cambios es muy asimétrica."""
    X = diseno(d)
    b = (sm.QuantReg(d.lr.values, X).fit(q=.5, max_iter=5000).params if robust
         else np.linalg.lstsq(X, d.lr.values, rcond=None)[0])
    return dict(zip(YEARS, 100 * np.exp(np.r_[0, b])))


MIN_PARES, MIN_POR_ANIO = 30, 5


def identificable(d):
    """Índice propio solo con 30 o más pares, al menos 5 pares que toquen cada año 2015-2023 y matriz de rango completo.
    Sin eso el nivel de algún año frente a 2015 no está identificado o sale inestable (muestras chicas)."""
    if len(d) < MIN_PARES:
        return False
    toques = pd.concat([d.py, d.y]).value_counts()
    if any(toques.get(t, 0) < MIN_POR_ANIO for t in YEARS):
        return False
    return np.linalg.matrix_rank(diseno(d)) == len(YEARS) - 1


# ¿cuántos pares crecen como el avalúo? (0-5% anual, compatible con escriturar por el avalúo catastral)
ann = np.exp(p.lr / (p.y - p.py)) - 1
R['pares_crec_0a5pct_anual'] = round(float(ann.between(0, .05).mean()), 3)
R['pares_crec_exacto_0_o_3pct'] = round(float(ann.round(3).isin([0, .03]).mean()), 3)
R['pares_crec_0a5pct_por_anio_2a_venta'] = ann.between(0, .05).groupby(p.y).mean().round(2).to_dict()

cnt = p.groupby(['div', 'zona']).size().unstack(fill_value=0)
ok = [(key, d) for key, d in p.groupby(['div', 'zona']) if key[1] != 'OTRA' and identificable(d)]
idx = {key: bmn(d) for key, d in ok}
idx_ols = {key: bmn(d, robust=False) for key, d in ok}
for z in ('URBANO', 'RURAL'):
    R[f'mun_{z}_30'] = int((cnt[z] >= 30).sum())
    R[f'mun_indice_{z}'] = sum(1 for (_, zz) in idx if zz == z)
R['idx2023_RURAL_robusto_p50'] = round(float(np.median([d[2023] for (_, z), d in idx.items() if z == 'RURAL'])))
# cotas del mercado urbano en municipios grandes: el índice robusto con todas las reventas se pega al reajuste cuando
# muchas escrituras siguen el avalúo (cota inferior); quitar las reventas que crecen 0-5% anual también quita mercado
# lento (cota superior). El mercado está entre ambas.
grandes = [key for key in idx if key[1] == 'URBANO' and cnt.loc[key] >= 200]
sin_lento = dict(list(p[~ann.between(0, .05)].groupby(['div', 'zona'])))
idx_sin = {key: bmn(sin_lento[key]) for key in grandes if key in sin_lento and identificable(sin_lento[key])}
keys_b = [k for k in grandes if k in idx_sin]
med = lambda ix, t: float(np.median([ix[k][t] for k in keys_b]))
REAJ = {t: 100 * 1.03 ** (t - 2015) for t in YEARS}  # reajuste ~3%/año (meta de inflación); serie exacta: Guía 2
R.update({'mun_cotas_urbanas': len(keys_b),
          'idx2023_URBANO_cota_inferior': round(med(idx, 2023)),
          'idx2023_URBANO_cota_superior': round(med(idx_sin, 2023)),
          'idx2023_URBANO_ols': round(med(idx_ols, 2023)),
          'idx_URBANO_cotas_por_anio': {t: [round(med(idx, t)), round(med(idx_sin, t))] for t in YEARS},
          'reajuste_acumulado_2015_2023_aprox': round(REAJ[2023])})
# avalúo sin actualizar desde 2015 por debajo del piso legal de 60% aunque en 2015 estuviera al 100% del valor
# comercial: reajuste / índice < 0,6. Con la cota inferior y sin IC son candidatos, no conclusiones
piso = REAJ[2023] / .6
R['umbral_indice_piso60'] = round(piso)
R['mun_bajo_piso60_sin_ic'] = {z: sum(1 for (_, zz), d in idx.items() if zz == z and d[2023] > piso)
                               for z in ('URBANO', 'RURAL')}
R['perdida_avaluo_vs_mercado_pct'] = [round(100 * (1 - REAJ[2023] / R['idx2023_URBANO_cota_inferior'])),
                                      round(100 * (1 - REAJ[2023] / R['idx2023_URBANO_cota_superior']))]

# ---------------------------------------------------------------- 3. línea base de la estimación, sin fuga
# partición estable por inmueble: 20% prueba. Entrenamiento con los pares filtrados; prueba con TODAS las reventas
# de al menos un año, sin filtrar por el valor de la segunda venta (que es lo que se quiere predecir)
enprueba = lambda d: d.matricula.map(lambda m: zlib.crc32(m.encode())) % 5 == 0
tr, te = p[~enprueba(p)], qa[enprueba(qa)].copy()
yrs = (te.y - te.py).values
err = lambda ratio: np.abs(np.asarray(ratio, dtype=float) * np.exp(-te.lr.values) - 1)
E = {'regla': err(1.03 ** yrs), 'sin_ajuste': err(np.ones(len(te)))}
for robust in (False, True):
    # municipio-zona si es identificable; si no, departamento-zona; si no, nacional por zona
    lvl = [{k_: bmn(d, robust) for k_, d in tr.groupby(keys) if identificable(d)}
           for keys in (['div', 'zona'], ['dep', 'zona'], ['zona'])]
    ratios = []
    for dv, dp, z, y, py in zip(te['div'], te.dep, te.zona, te.y, te.py):
        d = lvl[0].get((dv, z)) or lvl[1].get((dp, z)) or lvl[2].get((z,))
        ratios.append(d[y] / d[py] if d else 1.0)
    E['indice_robusto' if robust else 'indice_ols'] = err(ratios)
    if robust:
        ratios_rob = np.array(ratios)
for k_, e in E.items():
    R[f'MdAPE_{k_}'] = round(100 * float(np.median(e)), 1)
R['pares_prueba'] = len(te)

# IC 95% bootstrap remuestreando inmuebles (un inmueble puede aportar varios pares)
codes = pd.factorize(te.matricula)[0]; n_m = codes.max() + 1
rng = np.random.default_rng(2026)
W = [np.bincount(rng.integers(0, n_m, n_m), minlength=n_m)[codes] for _ in range(300)]
wmed = lambda e, w: float(np.median(np.repeat(e, w)))
bs = 100 * np.array([(wmed(E['regla'], w), wmed(E['indice_robusto'], w)) for w in W])
R['MdAPE_regla_IC95'] = [round(x, 1) for x in np.percentile(bs[:, 0], [2.5, 97.5])]
R['MdAPE_dif_robusto_menos_regla_IC95'] = [round(x, 1) for x in np.percentile(bs[:, 1] - bs[:, 0], [2.5, 97.5])]
# diagnóstico (usa el valor observado para agrupar, no es un modelo): reventas que crecen como el avalúo vs el resto
ann_te = np.exp(te.lr.values / yrs) - 1
av = (ann_te >= 0) & (ann_te <= .05)
R['prueba_pct_compatible_avaluo'] = round(100 * av.mean(), 1)
R['MdAPE_por_grupo'] = {gname: {'regla': round(100 * float(np.median(E['regla'][m])), 1),
                                'indice_robusto': round(100 * float(np.median(E['indice_robusto'][m])), 1)}
                        for gname, m in (('compatible_avaluo', av), ('resto', ~av))}
# cota de mejora: si se supiera de antemano el tipo de escritura (regla en un grupo, índice en el otro)
R['MdAPE_oraculo'] = round(100 * float(np.median(np.where(av, E['regla'], E['indice_robusto']))), 1)
# meta: capturar la mitad de esa mejora máxima, redondeada hacia abajo a 0,5 puntos
R['MdAPE_meta'] = float(np.floor(2 * (R['MdAPE_regla'] + R['MdAPE_oraculo']) / 2) / 2)

# ---------------------------------------------------------------- 3b. línea base de alertas (sin etiquetas)
# presupuesto fijo: se alerta el 2% de las reventas con mayor desviación frente a lo esperado. Cada reventa de prueba
# se altera por separado x2 y x0,5 (sub o sobredeclaración) y x10 y x0,1 (digitación), y se mide qué parte de esas
# alteraciones cae dentro del presupuesto. Con presupuesto fijo, un modelo más preciso detecta más (Han et al., 2022)
B = .02
lr_te = te.lr.values


def deteccion(expct, f):
    thr = np.quantile(np.abs(lr_te - expct), 1 - B)
    return ((np.abs(lr_te + np.log(f) - expct) > thr).astype(float) + (np.abs(lr_te - np.log(f) - expct) > thr)) / 2


from scipy.stats import rankdata


def auc(expct, f, sel=slice(None)):
    """AUC: probabilidad de que una reventa alterada x f o x 1/f tenga mayor desviación que una reventa sin alterar.
    No depende del presupuesto de alertas; un modelo más preciso la sube (ADBench reporta esta métrica)."""
    lr_, e_ = lr_te[sel], expct[sel]
    neg = np.abs(lr_ - e_)
    pos = np.r_[np.abs(lr_ + np.log(f) - e_), np.abs(lr_ - np.log(f) - e_)]
    rk = rankdata(np.r_[pos, neg])[:len(pos)]
    return (rk.sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


EXP = {'regla': yrs * np.log(1.03), 'indice_robusto': np.log(ratios_rob)}
for name, e in EXP.items():
    R[f'alertas_{name}'] = {'AUC_x2_x05': round(auc(e, 2.), 3), 'AUC_x10_x01': round(auc(e, 10.), 3),
                            'deteccion_x2_x05_con_2pct_pct': round(100 * deteccion(e, 2.).mean(), 1),
                            'deteccion_x10_x01_con_2pct_pct': round(100 * deteccion(e, 10.).mean(), 1)}
# IC 95% de la diferencia de AUC remuestreando inmuebles (100 réplicas: cada AUC ordena ~170 mil valores)
bd = []
for w in W[:100]:
    sel = np.repeat(np.arange(len(te)), w)
    bd.append(auc(EXP['indice_robusto'], 2., sel) - auc(EXP['regla'], 2., sel))
R['alertas_AUC_dif_robusto_menos_regla_IC95'] = [round(x, 3) for x in np.percentile(bd, [2.5, 97.5])]
R['alertas_presupuesto_pct'] = 100 * B
R['alertas_al_anio_con_presupuesto'] = round(B * len(q) / len(YEARS))
R['reventas_365_cambio_5x_o_mas_pct'] = round(100 * float((qa.lr.abs() >= np.log(5)).mean()), 1)

# ---------------------------------------------------------------- 4. Art. 49: Resolución 2057 de 2025
gest = pd.DataFrame(json.load(open(get(soql('bhcx-bx97', select='divipola,municipio,gestor_cat', limit=2000),
                                       os.path.join(DATA, 'gestores.json')), encoding='utf8')))
gest['div'] = gest.divipola.astype(str).str.zfill(5)
nombre = dict(zip(gest['div'], gest.municipio.str.upper()))
import pdfplumber
# el PDF va a dos columnas y el nombre del municipio a veces queda en otra línea: el nombre es opcional
rec = re.compile(r'(\d{5})[ \t]+(?:[^\d%\n]+?[ \t]+)?(\d{2,3})[ \t]+(\d+(?:\.\d{3})*,\d+)[ \t]*%')
pct_any = re.compile(r'\d+(?:\.\d{3})*,\d+[ \t]*%')
rows, n_pct = [], 0
with pdfplumber.open(get(RES2057, os.path.join(DATA, 'res2057.pdf'))) as pdf:
    for pg in pdf.pages:
        t = pg.extract_text() or ''
        n_pct += len(pct_any.findall(t))
        rows += [(m.group(1), m.group(2), float(m.group(3).replace('.', '').replace(',', '.'))) for m in rec.finditer(t)]
zh = pd.DataFrame(rows, columns=['div', 'zhg', 'pct'])
R['res2057_porcentajes_en_texto'] = n_pct; R['res2057_filas_extraidas'] = len(zh)
zh = zh[zh['div'].isin(nombre)].drop_duplicates(['div', 'zhg'])
zh.insert(1, 'municipio', zh['div'].map(nombre))
zh.to_csv(os.path.join(OUT, 'res2057_zonas.csv'), index=False)
mu = zh.groupby('div').agg(municipio=('municipio', 'first'), zonas=('zhg', 'size'),
                           pct_mediana=('pct', 'median'), pct_max=('pct', 'max')).reset_index()
R.update({'art49_zonas': len(zh), 'art49_municipios': len(mu),
          'art49_pct_p10_p50_p90': [round(x) for x in np.percentile(zh.pct, [10, 50, 90])],
          'art49_zonas_4pct': int((zh.pct == 4).sum()), 'art49_zonas_mas_1000pct': int((zh.pct > 1000).sum())})
mu = mu.join(cnt[['URBANO', 'RURAL']].add_prefix('pares_'), on='div').fillna(0)
mu['idx2023_rural'] = mu['div'].map(lambda dv: idx[(dv, 'RURAL')][2023] if (dv, 'RURAL') in idx else np.nan)
mu['indice_urbano'] = mu['div'].map(lambda dv: (dv, 'URBANO') in idx)
R['art49_mun_indice_rural'] = int(mu.idx2023_rural.notna().sum())
R['art49_mun_indice_urbano'] = int(mu.indice_urbano.sum())
st = mu[mu['div'].str[:2] == '68']
R['santander_art49'] = len(st); R['santander_art49_indice_rural'] = int(st.idx2023_rural.notna().sum())
cmp_ = mu[mu.idx2023_rural.notna()]
R['art49_spearman_municipal'] = round(float(cmp_[['idx2023_rural', 'pct_mediana']].corr('spearman').iloc[0, 1]), 2)
R['art49_municipios_comparables'] = len(cmp_)
mu.to_csv(os.path.join(OUT, 'art49_municipios.csv'), index=False)

# ---------------------------------------------------------------- 5. municipios con IGAC como gestor catastral
igac = set(gest.loc[gest.gestor_cat == 'IGAC', 'div'])
R['mun_gestor_igac'] = len(igac)
R['mun_igac_indice_urbano'] = sum(1 for (dv, z) in idx if z == 'URBANO' and dv in igac)
R['mun_igac_indice_rural'] = sum(1 for (dv, z) in idx if z == 'RURAL' and dv in igac)

pd.DataFrame([{'div': dv, 'zona': z, 'pares': int(cnt.loc[dv, z]), **{str(t): round(v, 1) for t, v in d.items()}}
              for (dv, z), d in idx.items()]).to_csv(os.path.join(OUT, 'indices_municipio_zona.csv'), index=False)
json.dump(R, open(os.path.join(OUT, 'cifras.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for k_, v in R.items():
    print(f'{k_}: {v}')

# ---------------------------------------------------------------- 6. figuras para el anexo
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False})

fig, ax = plt.subplots(figsize=(6.3, 2.4))
lo, hi = [med(idx, t) for t in YEARS], [med(idx_sin, t) for t in YEARS]
ax.fill_between(list(YEARS), lo, hi, color='#1f5fbf', alpha=.25, lw=0,
                label=f'Mercado urbano: entre ambas cotas (mediana de {len(keys_b)} municipios)')
ax.plot(list(YEARS), lo, color='#1f5fbf', lw=2, label='Cota inferior: índice robusto con todas las reventas')
ax.plot(list(YEARS), hi, color='#1f5fbf', lw=1, ls=':', label='Cota superior: sin reventas que crecen 0-5% anual')
ax.plot(list(YEARS), [REAJ[t] for t in YEARS], color='black', ls='--', lw=1.2, label='Avalúo sin actualizar (~3%/año)')
ax.set_ylabel('Índice (2015 = 100)'); ax.legend(frameon=False, fontsize=7)
ax.set_title(f'2023: mercado urbano entre {lo[-1]:.0f} y {hi[-1]:.0f}; avalúo sin actualizar, {REAJ[2023]:.0f}',
             loc='left', fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig1_indice_vs_reajuste.png'), dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.3, 2.4))
ax.scatter(cmp_.idx2023_rural, cmp_.pct_mediana, s=14, color='#1f5fbf', alpha=.7)
ax.set_xlabel(f'Índice rural de mercado 2023 (2015 = 100); {len(cmp_)} municipios con índice propio')
ax.set_ylabel('Aumento mediano por zona (%)')
rho = f'{R["art49_spearman_municipal"]:.2f}'.replace('.', ',')
ax.set_title(f'Aumento Art. 49 (Res. 2057 original) vs mercado 2015-2023 (Spearman {rho})', loc='left', fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig2_art49_vs_mercado.png'), dpi=200); plt.close(fig)
