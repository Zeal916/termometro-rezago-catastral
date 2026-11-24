"""Exporta el anexo (HTML -> .docx y .pdf con Word) y la carta (.xlsx -> .pdf con Excel). Requiere pywin32 y Office."""
import os
import win32com.client as win32

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CM = 28.35  # puntos por centímetro

word = win32.DispatchEx('Word.Application'); word.Visible = False
doc = word.Documents.Open(os.path.join(HERE, 'anexo_guia1.html'))
doc.ActiveWindow.View.Type = 3  # vista de impresión
ps = doc.PageSetup
ps.PageWidth, ps.PageHeight = 21.59 * CM, 27.94 * CM  # carta
ps.TopMargin = ps.BottomMargin = 2.0 * CM
ps.LeftMargin = ps.RightMargin = 2.0 * CM
for shp in doc.InlineShapes:  # incrustar las imágenes en lugar de enlazarlas
    if shp.LinkFormat is not None:
        shp.LinkFormat.SavePictureWithDocument = True
        shp.LinkFormat.BreakLink()
doc.Content.Font.Name = 'Arial'
doc.Content.Font.Color = 0  # negro
for t in doc.Tables:  # Word agrega espacio después de cada párrafo de celda al importar HTML
    t.Range.ParagraphFormat.SpaceBefore = 0
    t.Range.ParagraphFormat.SpaceAfter = 0
    t.Range.ParagraphFormat.LineSpacingRule = 0  # sencillo
    t.Rows(1).HeadingFormat = True               # el encabezado se repite si la tabla sigue en otra página
doc.Sections(1).Footers(1).PageNumbers.Add(2)  # número de página centrado
doc.Sections(1).Footers(1).Range.Font.Name = 'Arial'
doc.Sections(1).Footers(1).Range.Font.Size = 9
DOCX = os.path.join(ROOT, 'Anexo_Guia1_Partes_I-VII.docx')
doc.SaveAs2(DOCX, FileFormat=16)
# "no partir filas" solo después de convertir a .docx: aplicado sobre el HTML, Word encoge las columnas y duplica
# las páginas
for t in doc.Tables:
    t.Rows.AllowBreakAcrossPages = False
for p in doc.Paragraphs:  # títulos h1-h3 pegados a lo que sigue: sin encabezados huérfanos al pie de página
    if p.OutlineLevel <= 3:
        p.KeepWithNext = True
doc.Save()
doc.SaveAs2(os.path.join(ROOT, 'Anexo_Guia1_Partes_I-VII.pdf'), FileFormat=17)
print('páginas del anexo:', doc.ComputeStatistics(2))
doc.Close(False); word.Quit()

excel = win32.DispatchEx('Excel.Application'); excel.Visible = False; excel.DisplayAlerts = False
wb = excel.Workbooks.Open(os.path.join(ROOT, 'Carta_Proyecto_Guia1_v2.xlsx'))
ws = wb.Worksheets(1)
ps = ws.PageSetup
ps.Orientation = 1                                # vertical
ps.BottomMargin = excel.InchesToPoints(0.8)       # la plantilla dejaba el pie de página encima de la tabla
ps.FooterMargin = excel.InchesToPoints(0.3)
# zoom fijo en vez de "ajustar a páginas": así Excel respeta el salto manual antes de las métricas (fila 14)
# y cada página (1: necesidades; 2: proyecto y planeación) cabe completa
pw, ph = (612, 792) if ps.PaperSize == 1 else (595, 842)  # carta o A4, en puntos
w = ws.Range('A1:I35').Width
h = max(ws.Range('A1:I13').Height, ws.Range('A14:I35').Height)
ps.Zoom = int(min(100 * (pw - ps.LeftMargin - ps.RightMargin) / w, 100 * (ph - ps.TopMargin - ps.BottomMargin) / h))
ws.ExportAsFixedFormat(0, os.path.join(ROOT, 'Carta_Proyecto_Guia1_v2.pdf'))
print('zoom de la carta:', ps.Zoom, '| páginas:', ws.PageSetup.Pages.Count)
wb.Close(False); excel.Quit()
del ps, ws, wb, excel  # liberar COM para que Excel no quede abierto con el archivo bloqueado
print('ok')
