"""Genera documento/anteproyecto.pdf (Edge sin interfaz) y documento/anteproyecto.docx (pandoc) desde anteproyecto.md;
el HTML intermedio queda en esta carpeta y no se versiona.

El índice de contenido, tablas y figuras se arma en dos pasadas: la primera genera el PDF con números provisionales
y ubica la página de cada sección, tabla y figura; la segunda lo regenera con los números reales.
Uso: py -I construir.py   (requiere pandoc en el PATH y Microsoft Edge)
"""
import html
import re
import subprocess
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, Cm

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI.parents[1] / "documento"  # el entregable vive en documento/
MD, HTML = AQUI / "anteproyecto.md", AQUI / "anteproyecto.html"
PDF, DOCX = SALIDA / "anteproyecto.pdf", SALIDA / "anteproyecto.docx"
TMP = AQUI / "_borrador.pdf"  # se imprime aquí y al final reemplaza a documento/anteproyecto.pdf
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
MARCA = '<div id="indice"></div>'
INICIO_CUERPO = "El Instituto Geográfico Agustín Codazzi (IGAC), a través"  # primera frase de la introducción


def entradas(md):
    """Secciones, tablas y figuras en orden, como (tipo, nivel, texto)."""
    out = []
    for linea in md.splitlines():
        m = re.match(r"^(#{2,4}) (.+)$", linea)
        if m and "Índice de contenido" not in m.group(2):
            out.append(("sec", len(m.group(1)) - 2, m.group(2).strip()))
        m = re.match(r"^Table: (Tabla \d+\..+)$", linea)
        if m:
            out.append(("tab", 0, m.group(1).strip()))
        m = re.match(r"^!\[(Figura \d+\..+?)\]\(", linea)
        if m:
            out.append(("fig", 0, m.group(1).strip()))
    return out


def corto(texto, n=95):
    texto = re.sub(r"[*_`]", "", texto)
    return texto if len(texto) <= n else texto[: n - 1].rsplit(" ", 1)[0] + "…"


def indice_html(items, paginas):
    def fila(clase, texto, pag):
        return (f'<div class="ix {clase}"><span class="ix-t">{html.escape(texto)}</span>'
                f'<span class="ix-p">{pag}</span></div>')
    sec = [fila(f"n{lvl}", re.sub(r"[*_`]", "", t), paginas.get(i, "00")) for i, (k, lvl, t) in enumerate(items) if k == "sec"]
    tab = [fila("n0", corto(t, 58), paginas.get(i, "00")) for i, (k, _, t) in enumerate(items) if k == "tab"]
    fig = [fila("n0", corto(t, 58), paginas.get(i, "00")) for i, (k, _, t) in enumerate(items) if k == "fig"]
    return ('<div id="indice"><p class="ix-h">Contenido</p>' + "".join(sec)
            + '<p class="ix-h">Tablas</p><div class="ix-cols">' + "".join(tab) + "</div>"
            + '<p class="ix-h">Figuras</p><div class="ix-cols">' + "".join(fig) + "</div></div>")


def imprimir(html_texto):
    HTML.write_text(html_texto, encoding="utf-8")
    TMP.unlink(missing_ok=True)
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={TMP}", HTML.as_uri()], check=True, capture_output=True)
    if not TMP.exists():
        raise SystemExit("Edge no generó el PDF")


def ubicar(items):
    doc = fitz.open(TMP)
    textos = [" ".join(p.get_text().split()) for p in doc]
    inicio = next(i for i, t in enumerate(textos) if INICIO_CUERPO in t)  # páginas anteriores: portada, abstract, índice
    paginas = {}
    primera_intro = next(i for i, (_, _, t) in enumerate(items) if t.startswith("3. Introducción"))
    for i, (_, _, t) in enumerate(items):
        clave = " ".join(re.sub(r"[*_`]", "", t).split())[:40]
        desde = inicio if i >= primera_intro else 1  # lo anterior a la introducción (abstract) va tras la portada
        for n in range(desde, len(doc)):
            if clave in textos[n]:
                paginas[i] = str(n + 1)
                break
        else:
            raise SystemExit(f"No se encontró en el PDF: {clave!r}")
    n = len(doc)
    doc.close()
    return paginas, n


md = MD.read_text(encoding="utf-8")
items = entradas(md)
subprocess.run(["pandoc", MD.name, "-s", "--embed-resources", "--css", "estilo.css", "-o", HTML.name],
               cwd=AQUI, check=True)
base = re.sub(r'<div id="indice">\s*</div>', MARCA, HTML.read_text(encoding="utf-8"))
assert MARCA in base, "falta la marca del índice"


def no_partir(m):
    """Las tablas cortas no se parten entre páginas; las largas sí, por filas completas."""
    t = m.group(0)
    return t.replace("<table>", '<table style="break-inside: avoid">', 1) if t.count("<tr") <= 10 else t


base = re.sub(r"<table>.*?</table>", no_partir, base, flags=re.S)
imprimir(base.replace(MARCA, indice_html(items, {})))      # pasada 1: números provisionales
paginas, _ = ubicar(items)
imprimir(base.replace(MARCA, indice_html(items, paginas)))  # pasada 2: números reales
paginas2, total = ubicar(items)
assert paginas2 == paginas, "la paginación cambió entre pasadas"
try:
    TMP.replace(PDF)
except PermissionError:
    raise SystemExit(f"No se pudo reemplazar {PDF}: ciérrelo en el visor de PDF y vuelva a ejecutar. El borrador quedó en {TMP}")
print("PDF:", total, "páginas")

# Word editable: el índice es un campo de tabla de contenido que Word actualiza al abrir
subprocess.run(["pandoc", MD.name, "--toc", "--toc-depth=3", "-o", str(DOCX)], cwd=AQUI, check=True)
doc = Document(DOCX)
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin = s.bottom_margin = Cm(2.0)
estilos = [st.name for st in doc.styles]
for nombre in ("Normal", "Body Text", "First Paragraph", "Compact"):
    if nombre in estilos:
        doc.styles[nombre].font.name = "Calibri"
        doc.styles[nombre].font.size = Pt(10.5)
for t in doc.tables:
    if "Table Grid" in estilos:
        t.style = doc.styles["Table Grid"]
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for fila in t.rows:
        for celda in fila.cells:
            for p in celda.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8.5)
doc.save(DOCX)
print("DOCX listo")
