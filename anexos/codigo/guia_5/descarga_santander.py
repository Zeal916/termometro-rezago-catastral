"""Descarga de la API de datos.gov.co (Registro de Transacciones Inmobiliarias IGAC, 7y2j-43cv) de los actos de
Santander (divipola 68xxx) necesarios para el piloto: compraventas (125), actos de cambio físico usados en la
limpieza, hipotecas y propiedad horizontal. No requiere credenciales.
Uso: python descarga_santander.py  -> ../../../datos/santander_actos.csv y LEEME_santander.json
"""
import csv
import io
import json
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
SALIDA = BASE.parents[1] / "datos" / "guia_5" / "santander_actos.csv"  # no versionado: lo descarga este script
URL = "https://www.datos.gov.co/resource/7y2j-43cv.csv"
CAMBIO_FISICO = ["317", "902", "903", "909", "910", "911", "912", "913", "915", "917", "918", "919", "920", "924", "964"]
CODIGOS = ["125", "203", "204", "205", "219", "331", "347"] + CAMBIO_FISICO
COLS = ("pk,matricula,num_anotacion,fecha_radica_texto,year_radica,divipola,municipio,tipo_predio_zona,"
        "categoria_ruralidad_2024,cod_natujur,documento_justificativo,count_a,count_de,tiene_mas_de_un_valor,valor")
WHERE = "starts_with(divipola,'68') AND cod_natujur in(" + ",".join(f"'{c}'" for c in CODIGOS) + ")"
LIMITE = 50_000


def pedir(params, intentos=5):
    url = URL + "?" + urllib.parse.urlencode(params)
    for i in range(intentos):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return list(csv.DictReader(io.StringIO(r.read().decode("utf-8"))))
        except Exception as e:  # red inestable: reintenta con espera creciente
            if i == intentos - 1:
                raise
            print("  reintento", i + 1, e)
            time.sleep(5 * (i + 1))


esperado = int(pedir({"$select": "count(*) as n", "$where": WHERE})[0]["n"])
filas, offset = [], 0
while True:
    r = pedir({"$select": COLS, "$where": WHERE, "$order": "pk", "$limit": LIMITE, "$offset": offset})
    filas += r
    print(f"  {len(filas):,} de {esperado:,}")
    if len(r) < LIMITE:
        break
    offset += LIMITE

SALIDA.parent.mkdir(exist_ok=True)
with open(SALIDA, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS.split(","))
    w.writeheader()
    w.writerows(filas)
(BASE / "LEEME_santander.json").write_text(json.dumps({
    "fuente": "https://www.datos.gov.co/resource/7y2j-43cv", "fecha_descarga": str(date.today()), "filtro": WHERE,
    "filas_esperadas": esperado, "filas_descargadas": len(filas), "archivo": str(SALIDA.name)},
    ensure_ascii=False, indent=2), encoding="utf-8")
assert len(filas) == esperado, "descarga incompleta"
print(f"Listo: {len(filas):,} filas en {SALIDA}")
