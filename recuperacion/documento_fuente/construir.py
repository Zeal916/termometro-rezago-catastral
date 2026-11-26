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
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

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


def limpio(texto):
    return re.sub(r"[*_`]", "", texto).strip().rstrip(".")


def indice_html(items, paginas, anclas):
    """Índice en una columna. Cada entrada es un enlace a su sección, tabla o figura; los títulos largos
    pasan al renglón siguiente con sangría y la línea de puntos y la página quedan en el último renglón."""
    vistos = {"sec": 0, "tab": 0, "fig": 0}

    def fila(i, k, lvl, texto):
        destino = anclas[k][vistos[k]]
        vistos[k] += 1
        m = re.match(r"^((?:Tabla|Figura) \d+\.)\s*(.*)$", texto)
        etiqueta = f'<span class="ix-l">{html.escape(m.group(1))}</span>' if m else ""
        titulo = html.escape(m.group(2) if m else texto)
        return (f'<a class="ix n{lvl}" href="#{destino}">{etiqueta}<span class="ix-t">{titulo}</span>'
                f'<span class="ix-p">{paginas.get(i, "00")}</span></a>')

    partes = {"sec": [], "tab": [], "fig": []}
    for i, (k, lvl, t) in enumerate(items):
        partes[k].append(fila(i, k, lvl if k == "sec" else 0, limpio(t)))
    return ('<div id="indice"><p class="ix-h">Contenido</p>' + "".join(partes["sec"])
            + '<p class="ix-h">Tablas</p>' + "".join(partes["tab"])
            + '<p class="ix-h">Figuras</p>' + "".join(partes["fig"]) + "</div>")


def anclar(doc_html):
    """Identificadores de destino para el índice: los de pandoc en los títulos y uno por tabla y figura."""
    sec = [m.group(2) for m in re.finditer(r'<h([2-4])[^>]*\bid="([^"]+)"[^>]*>(.*?)</h\1>', doc_html, re.S)
           if "Índice de contenido" not in m.group(3)]
    cont = {"tabla": 0, "figura": 0}

    def marcar(tipo):
        def f(m):
            cont[tipo] += 1
            return f'{m.group(0)} id="{tipo}-{cont[tipo]}"'
        return f
    doc_html = re.sub(r"<caption\b", marcar("tabla"), doc_html)
    doc_html = re.sub(r"<figure\b", marcar("figura"), doc_html)
    return doc_html, {"sec": sec, "tab": [f"tabla-{n}" for n in range(1, cont["tabla"] + 1)],
                      "fig": [f"figura-{n}" for n in range(1, cont["figura"] + 1)]}


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
base, anclas = anclar(base)
assert [len(anclas[k]) for k in ("sec", "tab", "fig")] == [sum(1 for x in items if x[0] == k) for k in ("sec", "tab", "fig")],     "el número de destinos no coincide con el de entradas del índice"
imprimir(base.replace(MARCA, indice_html(items, {}, anclas)))      # pasada 1: números provisionales
paginas, _ = ubicar(items)
imprimir(base.replace(MARCA, indice_html(items, paginas, anclas)))  # pasada 2: números reales
paginas2, total = ubicar(items)
assert paginas2 == paginas, "la paginación cambió entre pasadas"
try:
    TMP.replace(PDF)
except PermissionError:
    raise SystemExit(f"No se pudo reemplazar {PDF}: ciérrelo en el visor de PDF y vuelva a ejecutar. El borrador quedó en {TMP}")
# Anexo A: la carta del proyecto ajustada va al final del PDF, cada página en una hoja oficio con título y número
CARTA = AQUI.parents[1] / "anexos" / "guia_1" / "Carta_Proyecto_ajustada.pdf"
pdf, carta = fitz.open(PDF), fitz.open(CARTA)
cm = 72 / 2.54
for n, pag in enumerate(carta, 1):
    hoja = pdf.new_page(width=8.5 * 72, height=14 * 72)
    hoja.insert_text((2 * cm, 2 * cm + 10), f"Anexo A. Carta del proyecto ajustada ({n} de {len(carta)})", fontname="hebo", fontsize=12)
    marco = fitz.Rect(2 * cm, 2.8 * cm, hoja.rect.width - 2 * cm, hoja.rect.height - 2.4 * cm)
    caja = fitz.Rect()  # contenido de la página de Excel, sin sus márgenes blancos
    for x in [d["rect"] for d in pag.get_drawings()] + [fitz.Rect(b[:4]) for b in pag.get_text("blocks") if b[1] < pag.rect.height * 0.9]:  # sin el pie de la plantilla
        caja |= x
    hoja.show_pdf_page(marco, carta, pag.number, keep_proportion=True, clip=caja + (-4, -4, 4, 4))
    hoja.insert_text((hoja.rect.width - 2 * cm - 10, hoja.rect.height - 1.2 * cm), str(len(pdf)), fontname="helv", fontsize=9)
pdf.save(TMP)
pdf.close(); carta.close()
TMP.replace(PDF)
total = len(fitz.open(PDF))
print("PDF:", total, "páginas (con la carta ajustada como Anexo A)")

# Word editable: el índice es un campo de tabla de contenido que Word actualiza al abrir
subprocess.run(["pandoc", MD.name, "--toc", "--toc-depth=3", "-o", str(DOCX)], cwd=AQUI, check=True)
doc = Document(DOCX)
for s in doc.sections:
    s.page_width, s.page_height = Cm(21.59), Cm(35.56)  # oficio
    s.left_margin = s.right_margin = Cm(2.0)
    s.top_margin = s.bottom_margin = Cm(2.0)
estilos = [st.name for st in doc.styles]
for nombre in ("Normal", "Body Text", "First Paragraph", "Compact", "Title", "Heading 1", "Heading 2", "Heading 3",
               "Heading 4", "Table Caption", "Image Caption", "TOC Heading", "Hyperlink"):
    if nombre in estilos:  # regla del equipo: Arial y texto negro
        f = doc.styles[nombre].font
        f.name = "Arial"
        f.color.rgb = RGBColor(0, 0, 0)
        if nombre in ("Normal", "Body Text", "First Paragraph", "Compact"):
            f.size = Pt(11)
for t in doc.tables:
    if "Table Grid" in estilos:
        t.style = doc.styles["Table Grid"]
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for fila in t.rows:
        for celda in fila.cells:
            for p in celda.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
                    r.font.name = "Arial"
    for celda in t.rows[0].cells:  # encabezado gris E6E6E6
        sombra = OxmlElement("w:shd")
        sombra.set(qn("w:val"), "clear")
        sombra.set(qn("w:fill"), "E6E6E6")
        celda._tc.get_or_add_tcPr().append(sombra)
# Portada: centrada y en negrilla, como en el PDF; salto de página antes del Abstract
for p in doc.paragraphs:
    if p.text.startswith("1. Abstract"):
        p.paragraph_format.page_break_before = True
        break
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.bold = "github" not in r.text
        r.font.size = Pt(10)
doc.save(DOCX)
print("DOCX listo")
