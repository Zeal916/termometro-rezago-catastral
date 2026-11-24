"""Descarga del Registro de Transacciones Inmobiliarias del IGAC (datos.gov.co, 7y2j-43cv) para el piloto del
Área Metropolitana de Bucaramanga (Bucaramanga, Floridablanca, Girón y Piedecuesta), 2015-2023. No requiere credenciales.

Uso, desde la raíz del repositorio:
  py -I codigo/descarga_amb.py compraventas  -> datos/amb_compraventas_2015_2023.csv (base de la Guía 4, 165.517 filas)
  py -I codigo/descarga_amb.py actos         -> datos/guia_5/amb_7y2j-43cv.csv (todos los actos; insumo de variables_oa2_amb.py)
  py -I codigo/descarga_amb.py conteo        -> solo consulta cuántas filas tiene cada descarga

El archivo de compraventas ya viene versionado en datos/; este script permite reconstruirlo si se pierde.
"""
import csv
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
URL = "https://www.datos.gov.co/resource/7y2j-43cv.csv"
AMB = "divipola in('68001','68276','68307','68547')"
PERIODO = "year_radica between '2015' and '2023'"
COLS = ("categoria_ruralidad_2024,cod_natujur,count_a,count_de,departamento,dinamica_2024,divipola,"
        "documento_justificativo,estado_folio,fecha_apertura_texto,fecha_radica_texto,folios_derivados,matricula,"
        "municipio,nombre_natujur,num_anotacion,orip,pk,predios_nuevos,tiene_mas_de_un_valor,tiene_valor,"
        "tipo_predio_zona,valor,year_radica")
DESCARGAS = {
    "compraventas": (f"{AMB} AND {PERIODO} AND cod_natujur='125'", RAIZ / "datos" / "amb_compraventas_2015_2023.csv"),
    "actos": (f"{AMB} AND {PERIODO}", RAIZ / "datos" / "guia_5" / "amb_7y2j-43cv.csv"),
}
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


def contar(where):
    return int(pedir({"$select": "count(*) as n", "$where": where})[0]["n"])


def descargar(nombre):
    where, salida = DESCARGAS[nombre]
    esperado = contar(where)
    filas, offset = [], 0
    while True:
        r = pedir({"$select": COLS, "$where": where, "$order": "pk", "$limit": LIMITE, "$offset": offset})
        filas += r
        print(f"  {len(filas):,} de {esperado:,}")
        if len(r) < LIMITE:
            break
        offset += LIMITE
    salida.parent.mkdir(parents=True, exist_ok=True)
    with open(salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS.split(","))
        w.writeheader()
        w.writerows(filas)
    salida.with_name(f"LEEME_{salida.stem}.json").write_text(json.dumps({
        "fuente": URL, "fecha_descarga": str(date.today()), "filtro": where,
        "filas_esperadas": esperado, "filas_descargadas": len(filas)}, ensure_ascii=False, indent=2), encoding="utf-8")
    assert len(filas) == esperado, "descarga incompleta"
    print(f"Listo: {len(filas):,} filas en {salida}")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "conteo"
    if modo == "conteo":
        for nombre, (where, salida) in DESCARGAS.items():
            print(f"{nombre}: {contar(where):,} filas -> {salida.relative_to(RAIZ)}")
    elif modo in DESCARGAS:
        descargar(modo)
    else:
        sys.exit(f"Modo desconocido: {modo}. Use compraventas, actos o conteo.")
