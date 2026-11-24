// Convierte el borrador validado de la Parte I (versión 2: auditorias/07_parte1_coherencia_compresion/borrador_v2.md) (Markdown sencillo) a Word con el formato del proyecto.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, Footer, PageNumber, LevelFormat, TableLayoutType,
} = require("docx");

const [, , ENTRADA, SALIDA] = process.argv;
const md = fs.readFileSync(ENTRADA, "utf8").replace(/\r/g, "");
const cuerpo = md.split(/\n---\n/)[1];                       // lo que va antes de --- son notas internas
const lineas = cuerpo.split("\n");

const FUENTE = "Arial", NEGRO = "000000";
const ANCHO = 12240 - 2 * 1134;                              // carta menos márgenes de 2 cm = 9972 DXA

// Comillas tipográficas y negrillas **...**
const comillas = (s) => { let abre = true; return s.replace(/"/g, () => ((abre = !abre) ? "”" : "“")); };
function runs(texto, tam = 22, extra = {}) {
  return comillas(texto).split(/(\*\*[^*]+\*\*)/).filter(Boolean).map((p) =>
    new TextRun({ text: p.replace(/\*\*/g, ""), bold: p.startsWith("**") || extra.bold, font: FUENTE, size: tam, color: NEGRO, italics: extra.italics }));
}
const parrafo = (texto, op = {}) => new Paragraph({
  children: runs(texto, op.tam || 22, op), alignment: op.align || AlignmentType.JUSTIFIED,
  spacing: { after: op.after ?? 120, before: op.before ?? 0 }, keepNext: op.keepNext, numbering: op.numbering,
  indent: op.indent,
});

// Tablas: Arial 9, encabezado gris, bordes negros; anchos según la longitud del texto
const borde = { style: BorderStyle.SINGLE, size: 4, color: NEGRO };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };
function tabla(filas) {
  const celdas = filas.map((f) => f.replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
  const n = celdas[0].length;
  // mínimo: la palabra más larga de la columna (Arial 9, ~105 DXA por carácter, más márgenes de celda);
  // el resto del ancho se reparte según la cantidad media de texto de cada columna
  const minimos = Array.from({ length: n }, (_, j) =>
    Math.max(...celdas.map((f) => Math.max(...(f[j] || "").replace(/\*\*/g, "").split(/\s+/).map((w) => w.length)))) * 105 + 200);
  const pesos = Array.from({ length: n }, (_, j) => {
    const largo = celdas.map((f) => (f[j] || "").length);
    return largo.reduce((a, b) => a + b, 0) / largo.length;
  });
  const libre = ANCHO - minimos.reduce((a, b) => a + b, 0);
  const total = pesos.reduce((a, b) => a + b, 0);
  const anchos = minimos.map((m, j) => Math.round(m + (libre * pesos[j]) / total));
  anchos[n - 1] += ANCHO - anchos.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: ANCHO, type: WidthType.DXA }, columnWidths: anchos, layout: TableLayoutType.FIXED,
    rows: celdas.map((f, i) => new TableRow({
      tableHeader: i === 0, cantSplit: false,
      children: f.map((c, j) => new TableCell({
        width: { size: anchos[j], type: WidthType.DXA }, borders: bordes,
        shading: i === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: "E6E6E6" } : undefined,
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
        children: [new Paragraph({ children: runs(c, 18, { bold: i === 0 }), alignment: AlignmentType.LEFT })],
      })),
    })),
  });
}

// Recorrido del Markdown
const hijos = [];
let lista = 0, enLista = false, ultimaTabla = -1;
for (let i = 0; i < lineas.length; i++) {
  const l = lineas[i];
  if (!l.trim()) continue;
  if (l.startsWith("## ")) {
    const t = l.slice(3).trim();
    if (t.startsWith("Referencias")) break;                  // las referencias se escriben aparte, con cursivas APA
    hijos.push(parrafo(`**${t}**`, { align: AlignmentType.LEFT, before: 200, keepNext: true }));
    enLista = false; continue;
  }
  if (/^Tabla \d+\./.test(l)) { hijos.push(parrafo(`**${l.trim()}**`, { align: AlignmentType.LEFT, before: 120, after: 60, keepNext: true })); continue; }
  if (l.startsWith("|")) {
    const filas = [];
    while (i < lineas.length && lineas[i].startsWith("|")) { if (!/^\|\s*-/.test(lineas[i])) filas.push(lineas[i]); i++; }
    i--; hijos.push(tabla(filas)); hijos.push(new Paragraph({ children: [], spacing: { after: 60 } })); ultimaTabla = hijos.length;
    continue;
  }
  const m = l.match(/^( *)(\d+)\. (.*)$/);
  if (m) {
    const nivel = m[1].length >= 4 ? 1 : 0;
    if (nivel === 0 && m[2] === "1") lista++;                // una lista nueva empieza en 1; si no, continúa la anterior
    enLista = true;
    hijos.push(parrafo(m[3], { numbering: { reference: "num", level: nivel, instance: lista }, after: 80,
      keepNext: m[3].trim().endsWith(":") || /^\*\*[^*]+\*\*$/.test(m[3].trim()) }));
    continue;
  }
  if (/^ {4}\S/.test(l) && enLista) {                        // párrafo que continúa un punto de la lista
    hijos.push(parrafo(l.trim(), { indent: { left: 360 }, after: 80 }));
    continue;
  }
  enLista = false;
  hijos.push(parrafo(l.trim()));
}

// si lo último es una tabla, Word exige un párrafo después: se deja de 1 pt para que no abra otra página
if (ultimaTabla === hijos.length) hijos[hijos.length - 1] = new Paragraph({ children: [], spacing: { before: 0, after: 0, line: 20, lineRule: "exact" } });

// Referencias en APA, con cursivas
const ref = (partes) => new Paragraph({
  children: partes.map(([t, it]) => new TextRun({ text: t, italics: !!it, font: FUENTE, size: 22, color: NEGRO })),
  alignment: AlignmentType.LEFT, indent: { left: 567, hanging: 567 }, spacing: { after: 100 },
});
// las referencias van en la sección 6 del documento final

const encabezado = [
  parrafo("**Parte I. Elección de enfoques, construcción del modelo e implementación**", { tam: 28, align: AlignmentType.CENTER, after: 60 }),
  parrafo("Termómetro de rezago catastral. Gerencia de Proyectos de Analytics. Asesor: Carlos Ramírez.", { align: AlignmentType.LEFT, after: 0 }),
  parrafo("Equipo: Nicolás Santos, Cristian Ortiz, Daniel Aguirre, Dayan Hincapie.", { align: AlignmentType.LEFT, after: 120 }),
];

const nivel = (lvl, texto, izq) => ({
  level: lvl, format: LevelFormat.DECIMAL, text: texto, alignment: AlignmentType.LEFT,
  style: { paragraph: { indent: { left: izq, hanging: 360 } }, run: { font: FUENTE, size: 22, color: NEGRO } },
});
const doc = new Document({
  creator: "Grupo G23", lastModifiedBy: "Grupo G23", title: "Elección de enfoques, construcción del modelo e implementación", description: "",
  styles: { default: { document: { run: { font: FUENTE, size: 22, color: NEGRO } } } },
  numbering: { config: [{ reference: "num", levels: [nivel(0, "%1.", 360), nivel(1, "%2.", 720)] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: FUENTE, size: 18, color: NEGRO })] })] }) },
    children: [...encabezado, ...hijos],
  }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(SALIDA, b); console.log("escrito", SALIDA, b.length); });
