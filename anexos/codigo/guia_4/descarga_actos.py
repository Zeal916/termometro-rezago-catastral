"""Descarga de la API (datos.gov.co, 7y2j-43cv) todos los actos registrados de los folios que forman pares.
Requiere haber corrido limpieza_amb.py una vez (lee pares_amb.csv). Uso: py -I descarga_actos.py
"""
import csv
import io
import json
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[2] / "datos"  # carpeta datos del repositorio
URL = "https://www.datos.gov.co/resource/7y2j-43cv.csv"
COLS = "matricula,num_anotacion,fecha_radica_texto,cod_natujur,nombre_natujur,divipola,documento_justificativo,valor"
LOTE, LIMITE = 150, 50000
SALIDA = BASE / "api" / "actos_folios_pares.csv"


def pedir(params, intentos=4):
    url = URL + "?" + urllib.parse.urlencode(params)
    for i in range(intentos):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return list(csv.DictReader(io.StringIO(r.read().decode("utf-8"))))
        except Exception as e:  # red inestable: reintenta con espera creciente
            if i == intentos - 1:
                raise
            print("  reintento", i + 1, e)
            time.sleep(5 * (i + 1))


folios = sorted(pd.read_csv(BASE / "pares_amb.csv", usecols=["matricula"], dtype=str).matricula.unique())
print(f"Folios a consultar: {len(folios):,}")
filas = []
for i in range(0, len(folios), LOTE):
    lista = ",".join(f"'{m}'" for m in folios[i:i + LOTE])
    offset = 0
    while True:
        r = pedir({"$select": COLS, "$where": f"matricula in({lista})", "$order": "matricula,num_anotacion",
                   "$limit": LIMITE, "$offset": offset})
        filas += r
        if len(r) < LIMITE:
            break
        offset += LIMITE
    if (i // LOTE) % 10 == 0:
        print(f"  {i + LOTE:,} folios, {len(filas):,} actos")

SALIDA.parent.mkdir(exist_ok=True)
d = pd.DataFrame(filas)
d.to_csv(SALIDA, index=False)
faltan = set(folios) - set(d.matricula)
(SALIDA.parent / "LEEME_descarga.json").write_text(json.dumps({
    "fuente": "https://www.datos.gov.co/resource/7y2j-43cv", "fecha_descarga": str(date.today()),
    "folios_consultados": len(folios), "actos_descargados": len(d), "folios_sin_respuesta": len(faltan)},
    ensure_ascii=False, indent=2))
print(f"Listo: {len(d):,} actos de {d.matricula.nunique():,} folios; sin respuesta: {len(faltan)}")
