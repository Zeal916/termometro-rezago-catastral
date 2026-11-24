"""Genera documento/anteproyecto.pdf (Edge sin interfaz) y documento/anteproyecto.docx (pandoc) desde anteproyecto.md;
el HTML intermedio queda en esta carpeta y no se versiona.
Uso: py -I construir.py
"""
import subprocess
from pathlib import Path

import fitz  # PyMuPDF, solo para contar páginas
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, Cm

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI.parents[1] / "documento"  # el entregable vive en documento/
MD, HTML = AQUI / "anteproyecto.md", AQUI / "anteproyecto.html"
PDF, DOCX = SALIDA / "anteproyecto.pdf", SALIDA / "anteproyecto.docx"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

subprocess.run(["pandoc", MD.name, "-s", "--embed-resources", "--css", "estilo.css",
                "--metadata", "lang=es", "-o", HTML.name], cwd=AQUI, check=True)
subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF}", HTML.as_uri()], check=True, capture_output=True)
print("PDF:", len(fitz.open(PDF)), "páginas")

subprocess.run(["pandoc", MD.name, "-o", str(DOCX)], cwd=AQUI, check=True)
doc = Document(DOCX)
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin = s.bottom_margin = Cm(2.0)
for nombre in ("Normal", "Body Text", "First Paragraph", "Compact"):
    if nombre in [st.name for st in doc.styles]:
        doc.styles[nombre].font.name = "Calibri"
        doc.styles[nombre].font.size = Pt(10.5)
for t in doc.tables:
    t.style = doc.styles["Table Grid"] if "Table Grid" in [st.name for st in doc.styles] else t.style
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for fila in t.rows:
        for celda in fila.cells:
            for p in celda.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8.5)
doc.save(DOCX)
print("DOCX listo")
