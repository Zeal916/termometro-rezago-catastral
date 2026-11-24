"""Carta del proyecto (sobre la plantilla del curso) + figura de jerarquización (Parte II del anexo)."""
import datetime as dt, os, shutil
import openpyxl
from openpyxl.styles import Alignment
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(os.path.dirname(ROOT), 'Carta Proyecto - Guía 1.xlsx')
DST = os.path.join(ROOT, 'Carta_Proyecto_Guia1_v2.xlsx')

# ---------------------------------------------------------------- figura: matriz valor x capacidad de avanzar (IBM, 2020)
# solo las ideas que pasan el filtro de la Parte I; el horizonte dice cuándo se aborda cada una
ideas = [  # (id, nombre corto, capacidad de avanzar 1-5, valor 1-5, horizonte)
    ('1', 'Termómetro de rezago', 4.5, 4.8, 'foco: anteproyecto y Capstone'),
    ('5', 'Declarado al avalúo', 4.1, 3.9, 'corto plazo: limpia el dato del índice'),
    ('2', 'Revisión Art. 49', 2.6, 4.5, 'mediano plazo:\nvigencias dispersas')]
fig, ax = plt.subplots(figsize=(6.3, 2.5))
ax.axvline(3, color='#bbbbbb', lw=1)
for i, n, x, y, hz in ideas:
    ax.scatter(x, y, s=60, color='#1f5fbf', zorder=3)
    izq = x < 3  # rótulo a la izquierda para no cruzar la línea x = 3
    ax.annotate(f'{i}. {n}\n({hz})' if izq else f'{i}. {n} ({hz})', (x, y), xytext=(-6, 0) if izq else (6, -3),
                textcoords='offset points', fontsize=7.5, color='#1f5fbf', ha='right' if izq else 'left',
                va='center' if izq else 'baseline')
for (x, y, t) in ((3.05, 5.25, 'Enfocar ahora'), (1.05, 5.25, 'Valiosa, difícil hoy'),
                  (3.05, 0.8, 'Fácil, poco valor'), (1.05, 0.8, 'Descartar')):
    ax.text(x, y, t, fontsize=8, color='#777777', style='italic')
ax.set_xlim(1, 7.6); ax.set_ylim(0.6, 5.5); ax.set_xticks(range(1, 6))  # escala 1-5; el espacio extra es para rótulos
ax.set_xlabel('Capacidad del equipo de avanzar (datos, tiempo, conocimiento)')
ax.set_ylabel('Valor para el cliente')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_bounds(1, 5); ax.axhline(3, xmax=(5 - 1) / 6.6, color='#bbbbbb', lw=1)
ax.set_title('La 1 es el foco, la 5 limpia el dato y la 2 es valiosa pero hoy difícil', loc='left',
             fontsize=9.5)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'salidas', 'fig3_matriz_ibm.png'), dpi=200); plt.close(fig)

# ---------------------------------------------------------------- carta
shutil.copy(SRC, DST)
wb = openpyxl.load_workbook(DST); ws = wb.active
C = {
    'C2': 'Termómetro de rezago catastral: evidencia de mercado para medir la relación avalúo-mercado, priorizar la '
          'actualización y revisar el ajuste de avalúos del Art. 49 (Ley 2294 de 2023), con el Registro de '
          'Transacciones Inmobiliarias IGAC 2015-2023',
    'C3': 'Nicolás Santos', 'H3': 'Carlos Ramírez',
    'C4': '-', 'H4': dt.datetime(2026, 10, 24),
    'C6': 'El avalúo catastral es la base del impuesto predial y por norma debe estar entre el 60% y el 100% del valor '
          'comercial (Decreto 148 de 2020). Sin actualización solo sube por decreto: ~3% anual, y en predios rurales '
          'agropecuarios según los precios al productor agropecuario. El IGAC es gestor catastral de 836 municipios; en '
          'julio de 2026 reportó 41,34% del área del país actualizada, frente a la meta de 70% del PND 2022-2026. En '
          '2026 subió de una sola vez los avalúos de 1.639.140 predios rurales en 527 municipios (Art. 49; Res. 2057 de '
          '2025), con un aumento mediano de 326% por zona homogénea. Hubo un paro campesino en Santander, la Res. 0384 '
          'de 2026 permitió revisar los porcentajes (acuerdos en 33 municipios de Santander) y el Consejo de Estado '
          'admitió una demanda de nulidad (25 sep 2026). Desde agosto de 2026 hay un nuevo gobierno, crítico del ajuste, '
          'y el proyecto de ley C159 de 2026 propone un techo de 50% del valor comercial. El Registro IGAC/SNR tiene '
          '5,4 M de compraventas 2015-2023 (4,0 M con valor, 1.096 municipios).',
    'C7': 'Mejoraremos la medición de la relación entre el avalúo y el mercado con la que el IGAC decide qué municipios '
          'actualizar o revisar primero y verifica el ajuste del Art. 49, para la Dirección de Gestión Catastral y el '
          'Observatorio Inmobiliario Catastral (OIC). Hoy las medidas oficiales de precios son urbanas y parciales '
          '(IPVN: 53 municipios, vivienda nueva; IVP: 22 capitales; IPVU: 9 ciudades) y no hay ninguna rural. La Res. '
          '2057 fijó los aumentos desde el nivel central y hoy se revisan municipio por municipio, sin un contraste '
          'público e independiente con las ventas. Además, el 41% de las reventas crece entre 0% y 5% anual, compatible '
          'con escrituras declaradas por el avalúo y no por el precio real. Al resolverlo, el IGAC focaliza la '
          'actualización y las revisiones donde la brecha es mayor y sustenta o corrige el ajuste con evidencia '
          'reproducible. La medida sirve con cualquier regla: piso de 60% o techo de 50%. Una alerta es una señal para '
          'revisar, no una conclusión sobre un avalúo o una persona. Necesitan participar los analistas del OIC, las '
          'direcciones territoriales del IGAC y las secretarías de Hacienda municipales.',
    'C10': 'Cliente y champion: IGAC, Dirección de Gestión Catastral (dueña del proceso de actualización y del Art. 49), '
           'con el OIC (Dirección de Investigación y Prospectiva).\n'
           'Deben participar: analistas del OIC (validan el índice), direcciones territoriales del IGAC (revisan los '
           'aumentos con la Res. 0384), secretarías de Hacienda municipales (recaudo predial), SNR (fuente registral).\n'
           'Afectados positivamente: municipios con rezago (recaudo y planeación), propietarios de zonas sobreajustadas '
           '(corrección), ciudadanía (equidad: las tierras más baratas eran las más rezagadas).\n'
           'Afectados negativamente o en riesgo: propietarios de municipios priorizados (más predial), municipios donde se '
           'reduzca el ajuste (menos recaudo), IGAC si la evidencia contradice el ajuste (riesgo reputacional y jurídico), '
           'gremios agropecuarios que se oponen al ajuste.\n'
           'Interesados en la decisión: DNP (PND 2026-2030), Ministerio de Hacienda (finanzas territoriales), Congreso '
           '(proyecto C159 de 2026), Federación Colombiana de Municipios y gobernaciones con mesas de revisión '
           '(Santander, Valle).',
    'C11': '(1) Índice de mercado por municipio, urbano y rural, con IC 95% de ±10% o menos; si no se logra, índice '
           'departamental.\n'
           '(2) Brecha mercado vs reajuste y ranking de prioridad con su razón en el 100% de los municipios con índice.\n'
           '(3) Contraste del Art. 49 con el mercado, desde el año de la última actualización: "coherente" o '
           '"revisar", con la razón, en 143 municipios.\n'
           '(4) Reproducible: un script regenera el 100% de las cifras desde datos abiertos, con diccionario.\n'
           '(5) Alertas: 2% de las reventas (~960 al año), con los cambios físicos ya depurados y cada una con su razón, '
           'y advertencia de uso en cada vista '
           '(índice ≠ avalúo; alerta ≠ irregularidad).',
    'H11': 'Rezago catastral (un avalúo sin actualizar perdió entre 17% y 49% frente al mercado entre 2015 y 2023); '
           'cumplimiento de la regla legal (piso de 60%, o techo de 50% si se aprueba el C159); recaudo predial y '
           'equidad; legitimidad del ajuste (reclamos y demandas); productividad de la actualización; calidad del valor '
           'registrado (escrituras declaradas por el avalúo).',
    'C13': 'Este semestre (anteproyecto, 8 semanas): formular el problema, adquirir y evaluar las fuentes, y demostrar con '
           'análisis exploratorio que el rezago se puede medir con transacciones. Próximo semestre (Capstone): construir '
           'el Termómetro, un producto que (i) permita explorar el volumen, los valores y la evolución de las '
           'compraventas por territorio, (ii) estime un índice de mercado por municipio identificando las escrituras '
           'declaradas por el avalúo, (iii) estime el valor registrado de cada reventa mejor que la regla del reajuste y '
           'muestre los factores asociados a las diferencias, (iv) priorice municipios y operaciones atípicas para '
           'revisión, y (v) documente sus límites de uso.',
    'C15': 'Negocio: municipios con evidencia de mercado propia para decidir dónde actualizar o revisar, urbano / '
           'rural (el resto, con índice departamental)',
    'H15': '53 como máximo (IPVN, solo vivienda nueva) / 0', 'I15': '340 / 324',
    'C16': 'Negocio: municipios del Art. 49 con contraste entre mercado y ajuste, con índice rural propio y desde el '
           'año de la última actualización',
    'H16': '0', 'I16': '143',
    'C17': 'Negocio: municipios donde el avalúo quedó bajo el piso legal de 60% (supuesto: al 100% en 2015 y '
           'solo reajuste anual; índice 2023 mayor a 211), en lista con IC 95% y año de última actualización',
    'H17': 'Ninguno identificado (hoy, sin IC: 49 urbanos / 53 rurales; pérdida mediana urbana de 17% a 49%)',
    'I17': 'Lista con IC 95%',
    'C18': 'Técnicas: error mediano (MdAPE) al estimar una reventa, 56.994 de prueba / AUC de detección de anomalías '
           'x2 y x0,5. Las mejoras deben tener un IC 95% que excluya 0',
    'H18': '18,3% (regla) / 0,745 (regla) y 0,757 (índice robusto)', 'I18': '≤ 16,5% / > 0,757',
    'C19': 'Proceso: hitos a tiempo / desviación de horas / municipios del Art. 49 (Res. IGAC 2057 de 2025) con año '
           'de última actualización consolidado, primero los 68 de Santander (S5) / variables documentadas en el '
           'diccionario (S4)',
    'H19': 'Inicia en S3 / inicia en S3 / 0 de 527 / 0%',
    'I19': '≥ 90% / ±15% / 527 / 100%',
    'A14': 'Métricas (negocio, técnicas y proceso)',
    'C20': 'Incluye: compraventas (cód. 125) del país 2015-2023 y, para depurar cambios físicos y anticipar el tipo de '
           'escritura, los demás actos del mismo folio (hipoteca, propiedad horizontal, construcción, englobe y '
           'desenglobe; 5,4 M descargados por código); exploración descriptiva; índice por municipio en zona '
           'urbana y rural, departamental donde faltan datos; brecha frente al reajuste; contraste con los municipios '
           'del Art. 49 (aumento de la Res. 2057; los ajustes publicados se muestran al lado); piloto en Santander (68 municipios del Art. 49, 15 con índice '
           'rural propio); alertas de operaciones atípicas en reventas.\n'
           'Excluye: valor de compraventas sin venta anterior (85% de las de un predio con valor), contraste por zona homogénea, recálculo del avalúo, '
           'conclusiones jurídicas o de fraude, puesta en producción.',
    'H20': 'Anteproyecto y Capstone de 8 semanas cada uno (~192 h del equipo por curso); 4 estudiantes de tiempo '
           'parcial; solo datos abiertos y software libre; el avalúo por predio no se puede unir con las ventas (se '
           'compara el índice con el reajuste por decreto; las vigencias salen de memorias y resoluciones); las ventas no traen área, estrato ni zona '
           'homogénea (se usan ventas repetidas del mismo inmueble); datos hasta 2023; sin etiquetas de "avalúo '
           'correcto"; regla legal en discusión (proyecto C159).',
    'C22': 'Cuantitativos: índice de mercado en 340 municipios urbanos y 324 rurales, frente a 53 urbanos y 0 rurales '
           'hoy; contraste del Art. 49 en 143 municipios frente a 0; pérdida de base del predial medida por municipio '
           '(hoy entre 17% y 49% en 8 años) y municipios bajo el piso de 60% identificados; error de estimación ≤ 16,5% frente a 18,3% de la regla; alertas mejores que '
           'la mejor línea base.\nCualitativos: priorización transparente del presupuesto de actualización y revisión; '
           'evidencia pública para un ajuste en litigio y para el debate del PND 2026-2030 y del C159; reglas que marcan '
           'aumentos extremos en la propia resolución (Baraya: 32.433% corregido a 4%); método replicable por la Red de '
           'Observatorios Inmobiliarios Catastrales.',
    'C24': 'Nicolás Santos', 'G24': 'Líder de proyecto / analista de negocio',
    'C25': 'Cristian Ortiz', 'G25': 'Ingeniería y calidad de datos',
    'C26': 'Daniel Aguirre', 'G26': 'Modelación (índices y alertas)',
    'C27': 'Dayan Hincapie', 'G27': 'Visualización, documentación y comunicación',
    'C28': 'Carlos Ramírez', 'G28': 'Asesor y validador de dominio',
    'C31': '[Inicio y Planificación] Caso, ideación, jerarquización, 5W, carta y anexo (primera versión y revisión); plan, riesgos '
           'y línea base.',
    'F31': '5 - 25 oct 2026 (S1-S3)', 'H31': 'Nicolás Santos',
    'C32': '[Ejecución] Requerimientos (Kano), problema y métrica de analytics, fuentes, estado del arte e inicio de la '
           'consolidación de vigencias de Santander (S3). Calidad, piloto de depuración de cambios '
           'físicos con los actos del folio (AMB), diccionario y video de avance (S4).',
    'F32': '19 oct - 1 nov 2026 (S3-S4)', 'H32': 'Cristian Ortiz',
    'C33': '[Ejecución] Análisis exploratorio descriptivo, índices piloto, sensibilidad y contraste piloto en Santander (S5-S6) y propuesta de modelos de tipo de escritura, '
           'índices y alertas (S7).',
    'F33': '2 - 22 nov 2026 (S5-S7)', 'H33': 'Daniel Aguirre',
    'C34': '[Planificación y Ejecución - Capstone] Plan (C1), datos depurados con los actos del folio en todo el país (C2-C3), modelos (C3-C6) y tablero '
           '(C5-C7): 151 h del equipo.',
    'F34': 'Capstone, semanas C1-C7', 'H34': 'Daniel Aguirre',
    'C35': '[Monitoreo y control + Cierre] Revisión semanal de hitos, horas, riesgos, demanda y C159; cierres del '
           'anteproyecto (23-29 nov 2026) y del Capstone (C7-C8, 33 h con 8 de holgura).',
    'F35': '5 oct 2026 - fin del Capstone', 'H35': 'Nicolás Santos (monitoreo); Dayan Hincapie (cierres)',
}
for cell, val in C.items():
    ws[cell] = val
    ws[cell].alignment = Alignment(wrap_text=True, vertical='top')
ws.oddFooter.center.text = 'Gerencia de Proyectos de Analytics · Caso Dinámica Inmobiliaria 2026'
for cell in ('C4', 'H4'):
    ws[cell].number_format = 'dd/mm/yyyy'

# Excel no autoajusta celdas combinadas: altura de fila estimada por largo del texto y ancho del rango
# ponytail: estimación por caracteres (~1,1 por unidad de ancho, conservadora), revisar el PDF si cambia la fuente
from math import ceil
from openpyxl.utils import get_column_letter
width = lambda c: ws.column_dimensions[get_column_letter(c)].width or 8.43
spans = {r.min_row * 100 + r.min_col: r for r in ws.merged_cells.ranges}
need = {}
for row in ws.iter_rows():
    for c in row:
        if not isinstance(c.value, str):
            continue
        rg = spans.get(c.row * 100 + c.column)
        c0, c1, r0, r1 = (rg.min_col, rg.max_col, rg.min_row, rg.max_row) if rg else (c.column, c.column, c.row, c.row)
        size = c.font.sz or 10
        cpl = sum(width(j) for j in range(c0, c1 + 1)) * 1.1 * 10 / size
        lines = sum(max(1, ceil(len(par) / cpl)) for par in c.value.split('\n'))
        h = (lines * size * 1.3 + 4) / (r1 - r0 + 1)
        for r_ in range(r0, r1 + 1):
            need[r_] = max(need.get(r_, 15), h)
for r_, h in need.items():
    ws.row_dimensions[r_].height = h
from openpyxl.worksheet.pagebreak import Break
ws.row_breaks.append(Break(id=13))  # la tabla de métricas empieza en la página 2 y no se parte
wb.save(DST)
print('ok', DST)
