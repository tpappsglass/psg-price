import streamlit as st
import pandas as pd
import numpy as np
import math
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ReportLab Imports for PDF Generation
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="PSG PRICE - Calumen & Nesting Offer Engine", layout="wide")

# ---------------------------------------------------------
# EXTENDED GLASS DATABASE (132 GLASS TYPES FROM KOSTOLOGIO.XLSX)
# ---------------------------------------------------------
GLASS_DB = {
    "CLEAR FLOAT GLASS 3 mm": {"cost": 3.47, "type": "CLEAR FLOAT GLASS"},
    "CLEAR FLOAT GLASS 4 mm": {"cost": 4.2, "type": "CLEAR FLOAT GLASS"},
    "CLEAR FLOAT GLASS 5 mm": {"cost": 5.25, "type": "CLEAR FLOAT GLASS"},
    "CLEAR FLOAT GLASS 6 mm": {"cost": 6.3, "type": "CLEAR FLOAT GLASS"},
    "CLEAR FLOAT GLASS 8 mm": {"cost": 8.82, "type": "CLEAR FLOAT GLASS"},
    "CLEAR FLOAT GLASS 10 mm": {"cost": 11.03, "type": "CLEAR FLOAT GLASS"},
    "CLEAR FLOAT GLASS 12 mm": {"cost": 15.75, "type": "CLEAR FLOAT GLASS"},
    "TINTED FLOAT GLASS 4 mm": {"cost": 5.7, "type": "TINTED FLOAT GLASS"},
    "TINTED FLOAT GLASS 5 mm": {"cost": 7.13, "type": "TINTED FLOAT GLASS"},
    "TINTED FLOAT GLASS 6 mm": {"cost": 8.55, "type": "TINTED FLOAT GLASS"},
    "TINTED FLOAT GLASS 8 mm": {"cost": 11.97, "type": "TINTED FLOAT GLASS"},
    "TINTED FLOAT GLASS 10 mm": {"cost": 14.96, "type": "TINTED FLOAT GLASS"},
    "SATINATED GLASS 4 mm": {"cost": 7.8, "type": "SATINATED GLASS"},
    "SATINATED GLASS 5 mm": {"cost": 8.75, "type": "SATINATED GLASS"},
    "SATINATED GLASS 6 mm": {"cost": 9.7, "type": "SATINATED GLASS"},
    "SATINATED GLASS 8 mm": {"cost": 11.98, "type": "SATINATED GLASS"},
    "SATINATED GLASS 10 mm": {"cost": 13.98, "type": "SATINATED GLASS"},
    "MIRROR 3 mm": {"cost": 8.0, "type": "MIRROR"},
    "MIRROR 4 mm": {"cost": 9.0, "type": "MIRROR"},
    "MIRROR 5 mm": {"cost": 10.0, "type": "MIRROR"},
    "MIRROR 6 mm": {"cost": 11.0, "type": "MIRROR"},
    "DIAMANT® 4 mm": {"cost": 7.65, "type": "DIAMANT®"},
    "DIAMANT® 5 mm": {"cost": 9.6, "type": "DIAMANT®"},
    "DIAMANT® 6 mm": {"cost": 11.0, "type": "DIAMANT®"},
    "DIAMANT® 8 mm": {"cost": 15.4, "type": "DIAMANT®"},
    "DIAMANT® 10 mm": {"cost": 19.0, "type": "DIAMANT®"},
    "COOL LITE® ST 108 6mm": {"cost": 23.0, "type": "COOL LITE® ST 108"},
    "4mm LOUKI 4mm": {"cost": 13.0, "type": "4mm LOUKI"},
    "6mm LOUKI 6mm": {"cost": 19.7, "type": "6mm LOUKI"},
    "8mm LOUKI 8mm": {"cost": 27.0, "type": "8mm LOUKI"},
    "LAMINATED GLASS 33.1": {"cost": 11.0, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 33.2": {"cost": 13.0, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 33.4": {"cost": 17.0, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 33.2 MAT": {"cost": 14.0, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 33.2 SC": {"cost": 15.0, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 44.1": {"cost": 12.98, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 44.2": {"cost": 14.98, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 44.4": {"cost": 18.98, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 44.1 MAT": {"cost": 15.98, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 44.2 SC": {"cost": 16.98, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 55.1": {"cost": 15.32, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 55.2": {"cost": 17.32, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 55.4": {"cost": 21.32, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 55.1 MAT": {"cost": 18.32, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 55.2 SC": {"cost": 19.32, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 66.1": {"cost": 17.77, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 66.2": {"cost": 19.77, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 66.4": {"cost": 23.77, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 66.1 MAT": {"cost": 19.77, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 66.2 SC": {"cost": 21.77, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 88.1": {"cost": 24.5, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 66.8": {"cost": 31.77, "type": "LAMINATED GLASS"},
    "LAMINATED GLASS 88.12": {"cost": 46.87, "type": "LAMINATED GLASS"},
    "CLIMAX 4mm": {"cost": 5.7, "type": "CLIMAX"},
    "CLIMAX 6mm": {"cost": 7.8, "type": "CLIMAX"},
    "CLIMAX 33.1": {"cost": 13.0, "type": "CLIMAX"},
    "CLIMAX 44.1": {"cost": 14.98, "type": "CLIMAX"},
    "CLIMAX 33.1 SC": {"cost": 17.0, "type": "CLIMAX"},
    "CLIMAX SC 44.1 SC": {"cost": 18.98, "type": "CLIMAX SC"},
    "CLIMAX SELECT 4mm": {"cost": 6.7, "type": "CLIMAX SELECT"},
    "CLIMAX SELECT 6mm": {"cost": 8.2, "type": "CLIMAX SELECT"},
    "CLIMAX SELECT 33.1": {"cost": 14.0, "type": "CLIMAX SELECT"},
    "CLIMAX SELECT 44.1": {"cost": 15.98, "type": "CLIMAX SELECT"},
    "CLIMAX SELECT SC 33.1 SC": {"cost": 18.0, "type": "CLIMAX SELECT SC"},
    "CLIMAX SELECT SC 44.1 SC": {"cost": 19.98, "type": "CLIMAX SELECT SC"},
    "ŞİŞECAM T 62/44 6mm": {"cost": 9.7, "type": "ŞİŞECAM T 62/44"},
    "ŞİŞECAM T 62/44 8mm": {"cost": 12.22, "type": "ŞİŞECAM T 62/44"},
    "ŞİŞECAM T 43/28 6mm": {"cost": 9.7, "type": "ŞİŞECAM T 43/28"},
    "ŞİŞECAM T 43/28 8mm": {"cost": 12.22, "type": "ŞİŞECAM T 43/28"},
    "ŞİŞECAM T 70/33 6mm": {"cost": 12.2, "type": "ŞİŞECAM T 70/33"},
    "ŞİŞECAM T70/33 8mm": {"cost": 14.72, "type": "ŞİŞECAM T70/33"},
    "PLANITHERM® XN 4mm": {"cost": 7.35, "type": "PLANITHERM® XN"},
    "PLANITHERM® XN 6mm": {"cost": 10.7, "type": "PLANITHERM® XN"},
    "PLANITHERM® XN 8mm": {"cost": 14.1, "type": "PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 33.1": {"cost": 18.4, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 33.2": {"cost": 21.6, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 33.2 SC": {"cost": 22.3, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 44.1": {"cost": 17.8, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 44.2": {"cost": 21.0, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 44.2 SC": {"cost": 21.7, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 66.1": {"cost": 25.1, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 66.2": {"cost": 28.3, "type": "STADIP® PLANITHERM® XN"},
    "STADIP® PLANITHERM® XN 66.2 SC": {"cost": 29.0, "type": "STADIP® PLANITHERM® XN"},
    "PLANISTAR® EVO 4mm": {"cost": 8.75, "type": "PLANISTAR® EVO"},
    "PLANISTAR® EVO 6mm": {"cost": 12.1, "type": "PLANISTAR® EVO"},
    "PLANISTAR® EVO 8mm": {"cost": 15.5, "type": "PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 33.1": {"cost": 16.2, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 33.2": {"cost": 19.4, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 33.2 SC": {"cost": 20.1, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 44.1": {"cost": 18.7, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 44.2": {"cost": 21.9, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 44.2 SC": {"cost": 22.6, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 66.1": {"cost": 26.0, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 66.2": {"cost": 29.2, "type": "STADIP® PLANISTAR® EVO"},
    "STADIP® PLANISTAR® EVO 66.2 SC": {"cost": 29.9, "type": "STADIP® PLANISTAR® EVO"},
    "PLANISTAR® SUN PLUS 4mm": {"cost": 10.75, "type": "PLANISTAR® SUN PLUS"},
    "PLANISTAR® SUN PLUS 6mm": {"cost": 14.1, "type": "PLANISTAR® SUN PLUS"},
    "STADIP® PLANISTAR® SUN PLUS 33.1": {"cost": 18.4, "type": "STADIP® PLANISTAR® SUN PLUS"},
    "STADIP® PLANISTAR® SUN PLUS 33.2": {"cost": 21.6, "type": "STADIP® PLANISTAR® SUN PLUS"},
    "STADIP® PLANISTAR® SUN PLUS 33.2 SC": {"cost": 22.3, "type": "STADIP® PLANISTAR® SUN PLUS"},
    "STADIP® PLANISTAR® SUN PLUS 44.1": {"cost": 20.9, "type": "STADIP® PLANISTAR® SUN PLUS"},
    "STADIP® PLANISTAR® SUN PLUS 44.2": {"cost": 24.1, "type": "STADIP® PLANISTAR® SUN PLUS"},
    "STADIP® PLANISTAR® SUN PLUS 44.2 SC": {"cost": 24.8, "type": "STADIP® PLANISTAR® SUN PLUS"},
    "COOL LITE® KN 166 II 6mm": {"cost": 16.5, "type": "COOL LITE® KN 166 II"},
    "COOL LITE® KN 166 II 8mm": {"cost": 20.8, "type": "COOL LITE® KN 166 II"},
    "COOL LITE® KN 166 II 10mm": {"cost": 24.6, "type": "COOL LITE® KN 166 II"},
    "COOL LITE® KN 148 II 6mm": {"cost": 16.5, "type": "COOL LITE® KN 148 II"},
    "COOL LITE® KN 148 II 8mm": {"cost": 20.8, "type": "COOL LITE® KN 148 II"},
    "COOL LITE® KN 148 II 10mm": {"cost": 24.6, "type": "COOL LITE® KN 148 II"},
    "COOL LITE® SKN 154 II 6mm": {"cost": 20.5, "type": "COOL LITE® SKN 154 II"},
    "COOL LITE® SKN 154 II 8mm": {"cost": 24.8, "type": "COOL LITE® SKN 154 II"},
    "COOL LITE® SKN 154 II 10mm": {"cost": 28.6, "type": "COOL LITE® SKN 154 II"},
    "COOL LITE® SKN 176 II 6mm": {"cost": 20.5, "type": "COOL LITE® SKN 176 II"},
    "COOL LITE® SKN 176 II 8mm": {"cost": 24.8, "type": "COOL LITE® SKN 176 II"},
    "COOL LITE® SKN 176 II 10mm": {"cost": 28.6, "type": "COOL LITE® SKN 176 II"},
    "COOL LITE® SKN 144 II 6mm": {"cost": 24.0, "type": "COOL LITE® SKN 144 II"},
    "COOL LITE® SKN 144 II 8mm": {"cost": 29.3, "type": "COOL LITE® SKN 144 II"},
    "COOL LITE® SKN 144 II 10mm": {"cost": 34.5, "type": "COOL LITE® SKN 144 II"},
    "COOL LITE® SKN 183 II 6mm": {"cost": 24.0, "type": "COOL LITE® SKN 183 II"},
    "COOL LITE® SKN 183 II 8mm": {"cost": 29.3, "type": "COOL LITE® SKN 183 II"},
    "COOL LITE® SKN 183 II 10mm": {"cost": 34.5, "type": "COOL LITE® SKN 183 II"},
    "COOL LITE® XTREME 61/29 6mm": {"cost": 26.0, "type": "COOL LITE® XTREME 61/29"},
    "COOL LITE® XTREME 61/29 8mm": {"cost": 31.5, "type": "COOL LITE® XTREME 61/29"},
    "COOL LITE® XTREME 61/29 10mm": {"cost": 36.5, "type": "COOL LITE® XTREME 61/29"},
    "COOL LITE® XTREME 70/33 6mm": {"cost": 26.0, "type": "COOL LITE® XTREME 70/33"},
    "COOL LITE® XTREME 70/33 8mm": {"cost": 31.5, "type": "COOL LITE® XTREME 70/33"},
    "COOL LITE® XTREME 70/33 10mm": {"cost": 36.5, "type": "COOL LITE® XTREME 70/33"},
    "GUARDIAN SN 70S II 6mm": {"cost": 18.1, "type": "GUARDIAN SN 70S II"},
    "GUARDIAN SN 63S II 6mm": {"cost": 20.0, "type": "GUARDIAN SN 63S II"},
    "GUARDIAN SNX 60S II 6mm": {"cost": 24.1, "type": "GUARDIAN SNX 60S II"},
    "GUARDIAN SN 70/37 II 6mm": {"cost": 21.3, "type": "GUARDIAN SN 70/37 II"},
    "GUARDIAN SN 75 II 6mm": {"cost": 19.39, "type": "GUARDIAN SN 75 II"},
}

PVB_DB = {
    "CLEAR 0.38mm": 3.20,
    "CLEAR 0.76mm": 6.23,
    "CLEAR 1.14mm": 9.73,
    "CLEAR 1.52mm": 12.51,
    "SOUND CONTROL (SC) 0.76mm": 8.97,
    "MAT 0.38mm": 6.86,
    "GREY 0.38mm": 5.50,
    "BRONZE 0.38mm": 5.50
}

SPACER_PRICES = {
    "Aluminium < 18mm": 8.00,
    "Technoform < 18mm": 10.00,
    "Aluminium > 18mm": 12.00,
    "Technoform > 18mm": 15.00
}

PROCESSING_COSTS = {
    "tempering": 6.50,
    "lami_processing": 7.00,
    "rode": 1.20,
    "packing_transport": 3.50,
    "hst": 15.00,         # €/m² ανά γυαλί
    "silkscreen": 15.00,  # €/m² ανά γυαλί
    "step": 15.00         # €/m² ανά σύνθεση
}

STOCK_SHEETS = {
    "6.000 x 3.210 mm (Jumbo - Προεπιλογή)": (6000, 3210),
    "3.210 x 2.250 mm (Standard)": (3210, 2250),
    "2.550 x 1.605 mm (Half Sheet)": (2550, 1605)
}

# ---------------------------------------------------------
# SIDEBAR: DYNAMIC FISCAL INPUTS (UPDATED DEFAULTS: 25% GBE / 15% PROFIT)
# ---------------------------------------------------------
st.sidebar.header("📋 Διαχείριση Παραγγελίας")
customer_name = st.sidebar.text_input("Όνομα Project / Πελάτη", "")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Δυναμικές Ρυθμίσεις Κοστολόγησης")

gbe_pct = st.sidebar.number_input("Γ.Β.Ε. / Έξοδα (%)", min_value=0.0, max_value=80.0, value=25.0, step=0.5)
profit_pct = st.sidebar.number_input("Καθαρό Κέρδος (%)", min_value=0.0, max_value=80.0, value=15.0, step=0.5)

gbe_markup = gbe_pct / (100.0 - gbe_pct) if gbe_pct < 100 else 0
profit_markup = profit_pct / (100.0 - profit_pct) if profit_pct < 100 else 0

st.sidebar.info(f"💡 **Markups:**\n- ΓΒE: +{gbe_markup*100:.2f}%\n- Κέρδος: +{profit_markup*100:.2f}%")

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def clean_recipe_name(full_name):
    if not full_name:
        return ""
    clean = full_name.split(" (")[0]
    return clean.strip()

def calculate_lami_component_cost(glasses_list, pvbs_list, temp_list, hst_list, silk_list, is_rode):
    cost = 0.0
    num_glasses = len(glasses_list)
    
    for g in glasses_list:
        if g in GLASS_DB:
            cost += GLASS_DB[g]["cost"]

    for pvb in pvbs_list:
        if pvb in PVB_DB:
            cost += PVB_DB[pvb]

    for temp in temp_list:
        if temp: cost += PROCESSING_COSTS["tempering"]
    for hst in hst_list:
        if hst: cost += PROCESSING_COSTS["hst"]
    for silk in silk_list:
        if silk: cost += PROCESSING_COSTS["silkscreen"]

    if num_glasses > 1:
        cost += (num_glasses - 1) * PROCESSING_COSTS["lami_processing"]

    if is_rode:
        cost += PROCESSING_COSTS["rode"]

    return cost

def run_nesting_optimization(items, stock_w, stock_h):
    stock_area = (stock_w / 1000.0) * (stock_h / 1000.0)
    
    individual_pieces = []
    p_id = 1
    for item in items:
        for _ in range(item['qty']):
            individual_pieces.append({'id': p_id, 'w': item['w'], 'h': item['h']})
            p_id += 1

    individual_pieces.sort(key=lambda p: (p['h'], p['w']), reverse=True)

    placed_sheets = []
    current_sheet_items = []
    
    curr_x, curr_y = 0, 0
    max_row_h = 0
    
    for p in individual_pieces:
        pw, ph = p['w'], p['h']
        
        if curr_x + pw <= stock_w and curr_y + ph <= stock_h:
            current_sheet_items.append({'id': p['id'], 'x': curr_x, 'y': curr_y, 'w': pw, 'h': ph})
            curr_x += pw
            max_row_h = max(max_row_h, ph)
        elif curr_y + max_row_h + ph <= stock_h and pw <= stock_w:
            curr_y += max_row_h
            curr_x = 0
            max_row_h = ph
            current_sheet_items.append({'id': p['id'], 'x': curr_x, 'y': curr_y, 'w': pw, 'h': ph})
            curr_x += pw
        else:
            placed_sheets.append(current_sheet_items)
            current_sheet_items = [{'id': p['id'], 'x': 0, 'y': 0, 'w': pw, 'h': ph}]
            curr_x = pw
            curr_y = 0
            max_row_h = ph

    if current_sheet_items:
        placed_sheets.append(current_sheet_items)

    sheets_needed = max(1, len(placed_sheets))
    total_used_area = sum([(p['w']/1000.0)*(p['h']/1000.0) for p in individual_pieces])
    total_stock_area = sheets_needed * stock_area
    waste_percentage = max(0.0, ((total_stock_area - total_used_area) / total_stock_area) * 100.0)

    return sheets_needed, round(waste_percentage, 1), round(total_used_area, 2), placed_sheets

def create_nesting_diagram(placed_sheet_items, sheet_idx, stock_w, stock_h):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, stock_w)
    ax.set_ylim(0, stock_h)
    ax.set_aspect('equal')
    
    rect_stock = patches.Rectangle((0, 0), stock_w, stock_h, linewidth=2, edgecolor='#1A365D', facecolor='#E2E8F0')
    ax.add_patch(rect_stock)

    colors_list = ['#2B6CB0', '#319795', '#D69E2E', '#DD6B20', '#805AD5', '#3182CE']

    for item in placed_sheet_items:
        c = colors_list[item['id'] % len(colors_list)]
        rect = patches.Rectangle((item['x'], item['y']), item['w'], item['h'], linewidth=1.5, edgecolor='#1A365D', facecolor=c, alpha=0.85)
        ax.add_patch(rect)
        
        cx = item['x'] + item['w'] / 2
        cy = item['y'] + item['h'] / 2
        label_text = f"#{item['id']}\n{int(item['w'])}x{int(item['h'])}"
        ax.text(cx, cy, label_text, color='white', weight='bold', fontsize=7, ha='center', va='center')

    ax.set_title(f"Φύλλο Κοπής (Stock Sheet #{sheet_idx + 1}) - {stock_w} x {stock_h} mm", fontsize=10, fontweight='bold', color='#1A365D')
    plt.xlabel("Πλάτος (mm)", fontsize=8)
    plt.ylabel("Ύψος (mm)", fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=180, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

# ---------------------------------------------------------
# PDF ENGINES (PSG OFFER & NESTING REPORT)
# ---------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 36, 20, page_text)
        self.drawString(36, 20, "PAP SAFETY GLASS S.A. - PSG OFFER")
        self.restoreState()

def generate_pdf_offer(customer_name, df_items, df_summary, totals):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=17, textColor=colors.HexColor("#1A365D"))
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor("#4A5568"))
    normal_style = ParagraphStyle('NormText', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor("#2D3748"))
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#1A365D"))
    header_cell = ParagraphStyle('HeaderCell', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)
    
    story = []
    cust_display = customer_name.upper() if customer_name.strip() else "-"

    header_data = [
        [
            Paragraph("<b>OSG INDUSTRIES</b><br/><font size=11 color='#2B6CB0'>PSG OFFER - ΠΡΟΣΦΟΡΑ</font>", title_style),
            Paragraph(f"<b>PAP SAFETY GLASS S.A.</b><br/>INDUSTRIAL AREA OF THESSALONIKI<br/>tel: +30 2310 796 180<br/>psg@papgroup.gr | www.papgroup.gr", normal_style)
        ],
        [
            Paragraph(f"<b>CUSTOMER:</b> {cust_display}", subtitle_style),
            Paragraph(f"<b>DATE:</b> {pd.Timestamp.now().strftime('%d/%m/%Y')}<br/><b>EST. DELIVERY DATE:</b> {pd.Timestamp.now().strftime('%d/%m/%Y')}", normal_style)
        ]
    ]
    t_header = Table(header_data, colWidths=[300, 220])
    t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_header)
    story.append(Spacer(1, 12))

    items_table_data = [[
        Paragraph("PRODUCT DESCRIPTION", header_cell),
        Paragraph("WIDTH", header_cell),
        Paragraph("HEIGHT", header_cell),
        Paragraph("QTY", header_cell),
        Paragraph("PRICE/m²", header_cell),
        Paragraph("m²", header_cell),
        Paragraph("NOTES", header_cell)
    ]]

    for idx, row in df_items.iterrows():
        items_table_data.append([
            Paragraph(str(row['Περιγραφή']), normal_style),
            Paragraph(str(int(row['Πλάτος (mm)'])), normal_style),
            Paragraph(str(int(row['Ύψος (mm)'])), normal_style),
            Paragraph(str(int(row['Τεμάχια'])), normal_style),
            Paragraph(f"{row['Τιμή/m² (€)']:.2f}€", normal_style),
            Paragraph(f"{row['Σύνολο m²']:.2f}", normal_style),
            Paragraph(str(row.get('Σημειώσεις', '')), normal_style)
        ])

    t_items = Table(items_table_data, colWidths=[210, 45, 45, 35, 60, 45, 80])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 12))

    summary_table_data = [[
        Paragraph("PRODUCT DESCRIPTION", header_cell),
        Paragraph("QTY", header_cell),
        Paragraph("m²", header_cell),
        Paragraph("PRICE/m²", header_cell),
        Paragraph("PRICE", header_cell)
    ]]

    for idx, row in df_summary.iterrows():
        summary_table_data.append([
            Paragraph(str(row['Περιγραφή']), normal_style),
            Paragraph(str(int(row['Τεμάχια'])), normal_style),
            Paragraph(f"{row['Σύνολο m²']:.2f}", normal_style),
            Paragraph(f"{row['Τιμή/m² (€)']:.2f}€", normal_style),
            Paragraph(f"{row['Σύνολο (€)']:.2f}€", bold_style)
        ])

    t_summary = Table(summary_table_data, colWidths=[240, 45, 65, 75, 95])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#EDF2F7")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 12))

    financial_data = [
        [Paragraph("<b>WITHOUT VAT:</b>", bold_style), Paragraph(f"<b>{totals['net']:.2f}€</b>", bold_style)],
        [Paragraph("<b>VAT (24%):</b>", bold_style), Paragraph(f"<b>{totals['vat']:.2f}€</b>", bold_style)],
        [Paragraph("<b>TOTAL:</b>", title_style), Paragraph(f"<b>{totals['total']:.2f}€</b>", title_style)],
        [Paragraph("<b>Προκαταβολή 40%:</b>", bold_style), Paragraph(f"<b>{totals['advance']:.2f}€</b>", bold_style)],
    ]
    t_financial = Table(financial_data, colWidths=[380, 140])
    t_financial.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('LINEBELOW', (0,2), (1,2), 1, colors.HexColor("#1A365D")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))

    bank_info = """
    <b>Προκαταβολή 40%:</b> Παρακαλούμε για την κατάθεση προκαταβολής 40% επί του συνολικού ποσού.<br/>
    Μετά την κατάθεση, αποστείλετε το αποδεικτικό με email για την άμεση δρομολόγηση της παραγωγής.<br/><br/>
    <b>Τραπεζικοί Λογαριασμοί PAP SAFETY GLASS S.A.</b><br/>
    • <b>PEIRAEUS BANK:</b> GR67 0172 2610 00526101 3442 742 (ΛΟΓ: 5261-013442-742)<br/>
    • <b>EUROBANK:</b> GR66 0260 3500 0004 2020 0696 947 (SWIFT: ERBKGRAA)<br/>
    • <b>ALPHA BANK:</b> GR35 0140 7180 7180 0233 0001 437 (ΛΟΓ: 7180 0233 0001 437)
    """
    p_bank = Paragraph(bank_info, normal_style)

    totals_and_bank = Table([[p_bank, t_financial]], colWidths=[300, 220])
    totals_and_bank.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(KeepTogether([totals_and_bank]))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer

def generate_pdf_nesting_report(customer_name, df_items, stock_w, stock_h, sheets_needed, waste_pct, total_m2, placed_sheets):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=17, textColor=colors.HexColor("#C53030"))
    normal_style = ParagraphStyle('NormText', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor("#2D3748"))
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor("#1A365D"))
    header_cell = ParagraphStyle('HeaderCell', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)

    story = []
    cust_display = customer_name.upper() if customer_name.strip() else "-"

    story.append(Paragraph("<b>PAP SAFETY GLASS S.A. - CUTTING & NESTING REPORT</b>", title_style))
    story.append(Paragraph(f"<b>PROJECT / CUSTOMER:</b> {cust_display} | <b>DATE:</b> {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Spacer(1, 10))

    summary_box_data = [
        [Paragraph("<b>Stock Sheet Size:</b>", normal_style), Paragraph(f"{stock_w} x {stock_h} mm", bold_style)],
        [Paragraph("<b>Total Stock Sheets Needed:</b>", normal_style), Paragraph(f"<b>{sheets_needed} τεμάχια</b>", bold_style)],
        [Paragraph("<b>Total Net Surface Area:</b>", normal_style), Paragraph(f"<b>{total_m2:.2f} m²</b>", bold_style)],
        [Paragraph("<b>Estimated Waste (Φύρα):</b>", normal_style), Paragraph(f"<b>{waste_pct}%</b>", bold_style)]
    ]
    t_box = Table(summary_box_data, colWidths=[180, 340])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#FEB2B2")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 15))

    nest_table_data = [[
        Paragraph("#", header_cell),
        Paragraph("DESCRIPTION / SYNTHESIS", header_cell),
        Paragraph("WIDTH (mm)", header_cell),
        Paragraph("HEIGHT (mm)", header_cell),
        Paragraph("QTY", header_cell),
        Paragraph("TOTAL m²", header_cell),
        Paragraph("NOTES", header_cell)
    ]]

    for idx, row in df_items.iterrows():
        nest_table_data.append([
            Paragraph(str(idx + 1), normal_style),
            Paragraph(str(row['Περιγραφή']), normal_style),
            Paragraph(str(int(row['Πλάτος (mm)'])), normal_style),
            Paragraph(str(int(row['Ύψος (mm)'])), normal_style),
            Paragraph(str(int(row['Τεμάχια'])), normal_style),
            Paragraph(f"{row['Σύνολο m²']:.2f}", normal_style),
            Paragraph(str(row.get('Σημειώσεις', '')), normal_style)
        ])

    t_nest = Table(nest_table_data, colWidths=[20, 200, 60, 60, 40, 60, 80])
    t_nest.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#9B2C2C")),
        ('ALIGN', (0,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_nest)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>🎨 Οπτικά Σχεδιαγράμματα Κοπής (Cutting Layouts)</b>", bold_style))
    story.append(Spacer(1, 10))

    for idx, sheet_items in enumerate(placed_sheets):
        img_buf = create_nesting_diagram(sheet_items, idx, stock_w, stock_h)
        rl_img = RLImage(img_buf, width=500, height=250)
        story.append(KeepTogether([
            Paragraph(f"<b>Διάταξη Φύλλου Κοπής #{idx + 1}</b>", normal_style),
            Spacer(1, 4),
            rl_img,
            Spacer(1, 12)
        ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer

# ---------------------------------------------------------
# HELPER UI BUILDER FOR UP TO 4 LAMINATED GLASSES
# ---------------------------------------------------------
def build_laminated_ui(pane_key_prefix, default_glass_key):
    num_panes = st.selectbox("Αριθμός Φύλλων Laminated (Γυαλιών)", [2, 3, 4], index=0, key=f"{pane_key_prefix}_num_panes")
    
    glasses_list = []
    pvbs_list = []
    temp_list = []
    hst_list = []
    silk_list = []

    st.markdown("---")
    st.markdown("##### 📄 1ο Φύλλο Γυαλιού")
    g1 = st.selectbox("Επιλογή 1ου Γυαλιού", list(GLASS_DB.keys()), key=f"{pane_key_prefix}_g1")
    t1 = st.checkbox("Security (Tempered) 1ο Γυαλί", key=f"{pane_key_prefix}_t1")
    h1 = st.checkbox("Heat Soak Test (HST) 1ο Γυαλί (+€15/m²)", key=f"{pane_key_prefix}_h1")
    s1 = st.checkbox("Μεταξοτυπία 1ο Γυαλί (+€15/m²)", key=f"{pane_key_prefix}_s1")
    glasses_list.append(g1)
    temp_list.append(t1)
    hst_list.append(h1)
    silk_list.append(s1)

    for i in range(2, num_panes + 1):
        st.markdown(f"**🔗 Μεμβράνη PVB #{i-1}**")
        pvb = st.selectbox(f"Επιλογή PVB #{i-1}", list(PVB_DB.keys()), key=f"{pane_key_prefix}_pvb_{i-1}")
        pvbs_list.append(pvb)

        st.markdown(f"##### 📄 {i}ο Φύλλο Γυαλιού")
        g = st.selectbox(f"Επιλογή {i}ου Γυαλιού", list(GLASS_DB.keys()), key=f"{pane_key_prefix}_g{i}")
        t = st.checkbox(f"Security (Tempered) {i}ο Γυαλί", key=f"{pane_key_prefix}_t{i}")
        h = st.checkbox(f"Heat Soak Test (HST) {i}ο Γυαλί (+€15/m²)", key=f"{pane_key_prefix}_h{i}")
        s = st.checkbox(f"Μεταξοτυπία {i}ο Γυαλί (+€15/m²)", key=f"{pane_key_prefix}_s{i}")
        
        glasses_list.append(g)
        temp_list.append(t)
        hst_list.append(h)
        silk_list.append(s)

    p_rode = st.checkbox("Ροντέ / Τρόχισμα (Laminated)", key=f"{pane_key_prefix}_rode")

    name = "+".join(glasses_list)
    has_temp = any(temp_list)

    return glasses_list, pvbs_list, temp_list, hst_list, silk_list, p_rode, name, has_temp

# ---------------------------------------------------------
# STREAMLIT UI & APPS
# ---------------------------------------------------------
st.title("🧮 PSG PRICE - Calumen Style Configurator & Precision Nesting Engine")

if 'recipes' not in st.session_state:
    st.session_state.recipes = {}

tab1, tab2, tab3 = st.tabs(["🧪 Calumen Recipe Builder", "📚 Βιβλιοθήκη Συνταγών", "📊 Κοστολόγηση Παραγωγής & Προσφορά PDF"])

# ---------------------------------------------------------
# TAB 1: CALUMEN RECIPE BUILDER
# ---------------------------------------------------------
with tab1:
    st.header("🏗️ Δημιουργία Συνταγής Υαλοστασίου (Calumen Style)")
    glass_type = st.radio("Τύπος Υαλοστασίου", ["Μονό Γυαλί", "Διπλό Υαλοστάσιο", "Τριπλό Υαλοστάσιο"], horizontal=True)
    
    is_double = glass_type in ["Διπλό Υαλοστάσιο", "Τριπλό Υαλοστάσιο"]
    is_triple = glass_type == "Τριπλό Υαλοστάσιο"

    col1, col2, col3 = st.columns(3)
    
    # GLASS 1 CONFIG
    c1 = 0.0
    name1 = ""
    has_temp1 = False

    with col1:
        st.subheader("🔵 Εξωτερικός Υαλοπίνακας (Γ1)")
        p1_lami = st.checkbox("Είναι Laminated / Συγκολλημένος", key="p1_lami")
        
        if p1_lami:
            st.markdown("**Σύνθεση Triplex / Laminated (έως 4 γυαλιά - Γ1):**")
            g_list, pvb_list, t_list, h_list, s_list, rode, name1, has_temp1 = build_laminated_ui("g1", "CLEAR FLOAT GLASS 4 mm")
            c1 = calculate_lami_component_cost(g_list, pvb_list, t_list, h_list, s_list, rode)
        else:
            g1_main = st.selectbox("Επιλογή Βασικού Γυαλιού 1", list(GLASS_DB.keys()), key="g1_main")
            p1_temp_main = st.checkbox("Security / Tempered", key="p1_temp_m")
            p1_hst_main = st.checkbox("Heat Soak Test (HST) (+€15/m²)", key="p1_hst_m")
            p1_silk_main = st.checkbox("Μεταξοτυπία (+€15/m²)", key="p1_silk_m")
            p1_rode = st.checkbox("Ροντέ / Τρόχισμα", key="p1_rode")

            name1 = g1_main
            has_temp1 = p1_temp_main
            c1 = calculate_lami_component_cost([g1_main], [], [p1_temp_main], [p1_hst_main], [p1_silk_main], p1_rode)

    # GLASS 2 CONFIG
    c2 = 0.0
    name2 = ""
    has_temp2 = False

    if is_double:
        with col2:
            st.subheader("🟢 Μεσαίος / Εσωτερικός (Γ2)")
            p2_lami = st.checkbox("Είναι Laminated / Συγκολλημένος ", key="p2_lami")
            if p2_lami:
                st.markdown("**Σύνθεση Triplex / Laminated (έως 4 γυαλιά - Γ2):**")
                g_list, pvb_list, t_list, h_list, s_list, rode, name2, has_temp2 = build_laminated_ui("g2", "CLEAR FLOAT GLASS 4 mm")
                c2 = calculate_lami_component_cost(g_list, pvb_list, t_list, h_list, s_list, rode)
            else:
                g2_main = st.selectbox("Επιλογή Βασικού Γυαλιού 2", list(GLASS_DB.keys()), key="g2_main")
                p2_temp_main = st.checkbox("Security / Tempered ", key="p2_temp_m")
                p2_hst_main = st.checkbox("Heat Soak Test (HST) (+€15/m²) ", key="p2_hst_m")
                p2_silk_main = st.checkbox("Μεταξοτυπία (+€15/m²) ", key="p2_silk_m")
                p2_rode = st.checkbox("Ροντέ / Τρόχισμα ", key="p2_rode")

                name2 = g2_main
                has_temp2 = p2_temp_main
                c2 = calculate_lami_component_cost([g2_main], [], [p2_temp_main], [p2_hst_main], [p2_silk_main], p2_rode)

    # GLASS 3 CONFIG
    c3 = 0.0
    name3 = ""
    has_temp3 = False

    if is_triple:
        with col3:
            st.subheader("🔴 Εσωτερικός (Γ3)")
            p3_lami = st.checkbox("Είναι Laminated / Συγκολλημένος  ", key="p3_lami")
            if p3_lami:
                st.markdown("**Σύνθεση Triplex / Laminated (έως 4 γυαλιά - Γ3):**")
                g_list, pvb_list, t_list, h_list, s_list, rode, name3, has_temp3 = build_laminated_ui("g3", "CLEAR FLOAT GLASS 4 mm")
                c3 = calculate_lami_component_cost(g_list, pvb_list, t_list, h_list, s_list, rode)
            else:
                g3_main = st.selectbox("Επιλογή Βασικού Γυαλιού 3", list(GLASS_DB.keys()), key="g3_main")
                p3_temp_main = st.checkbox("Security / Tempered  ", key="p3_temp_m")
                p3_hst_main = st.checkbox("Heat Soak Test (HST) (+€15/m²)  ", key="p3_hst_m")
                p3_silk_main = st.checkbox("Μεταξοτυπία (+€15/m²)  ", key="p3_silk_m")
                p3_rode = st.checkbox("Ροντέ / Τρόχισμα  ", key="p3_rode")

                name3 = g3_main
                has_temp3 = p3_temp_main
                c3 = calculate_lami_component_cost([g3_main], [], [p3_temp_main], [p3_hst_main], [p3_silk_main], p3_rode)

    # SPACERS, STEP & AIR GAPS CONFIG
    total_spacer_cost = 0.0
    spacer_desc = ""
    add_step = False

    if is_double and not is_triple:
        st.markdown("---")
        st.subheader("🔲 Ρυθμίσεις Διάκενου / Αποστάτη (Spacer) & Step")
        col_sp1, col_sp2, col_sp3 = st.columns(3)
        with col_sp1:
            sp1_mat = st.selectbox("Υλικό Διάκενου", ["Technoform Warm Edge", "Aluminium"], key="sp1_mat")
        with col_sp2:
            sp1_size = st.selectbox("Πάχος Διάκενου (mm)", [10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32], index=4, key="sp1_size")
        with col_sp3:
            add_step = st.checkbox("Επεξεργασία STEP (+€15.00/m²)", key="add_step")

        key1 = f"{'Technoform' if 'Technoform' in sp1_mat else 'Aluminium'} {'< 18mm' if sp1_size < 18 else '> 18mm'}"
        total_spacer_cost = SPACER_PRICES.get(key1, 10.00)
        if add_step:
            total_spacer_cost += PROCESSING_COSTS["step"]
        spacer_desc = f" / {sp1_size}mm {sp1_mat} + Argon"

    elif is_triple:
        st.markdown("---")
        st.subheader("🔲 Ρυθμίσεις Δύο Διάκενων / Αποστατών (Spacers) & Step")
        col_sp1, col_sp2, col_sp3 = st.columns(3)
        with col_sp1:
            st.markdown("**1o Διάκενο (Γ1 - Γ2):**")
            sp1_mat = st.selectbox("Υλικό 1ου Διάκενου", ["Technoform Warm Edge", "Aluminium"], key="sp1_mat_trip")
            sp1_size = st.selectbox("Πάχος 1ου Διάκενου (mm)", [10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32], index=4, key="sp1_size_trip")

        with col_sp2:
            st.markdown("**2o Διάκενο (Γ2 - Γ3):**")
            sp2_mat = st.selectbox("Υλικό 2ου Διάκενου", ["Technoform Warm Edge", "Aluminium"], key="sp2_mat_trip")
            sp2_size = st.selectbox("Πάχος 2ου Διάκενου (mm)", [10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32], index=4, key="sp2_size_trip")

        with col_sp3:
            st.markdown("**Ειδικές Επεξεργασίες Σύνθεσης:**")
            add_step = st.checkbox("Επεξεργασία STEP (+€15.00/m²)", key="add_step_trip")

        key1 = f"{'Technoform' if 'Technoform' in sp1_mat else 'Aluminium'} {'< 18mm' if sp1_size < 18 else '> 18mm'}"
        key2 = f"{'Technoform' if 'Technoform' in sp2_mat else 'Aluminium'} {'< 18mm' if sp2_size < 18 else '> 18mm'}"
        total_spacer_cost = SPACER_PRICES.get(key1, 10.00) + SPACER_PRICES.get(key2, 10.00)
        if add_step:
            total_spacer_cost += PROCESSING_COSTS["step"]
        spacer_desc = f" / {sp1_size}mm {sp1_mat} + Argon"

    st.markdown("---")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        add_pack = st.checkbox("Προσθήκη Συσκευασίας & Μεταφοράς (+€3.50 / m²)", value=True)
    with col_opt2:
        waste_pct_est = st.number_input("⚠️ Εκτιμώμενη Φθορά Υλικού (%) [Προαιρετικά]", min_value=0.0, max_value=50.0, value=0.0, step=1.0)

    # CALCULATE TOTAL DIRECT COST
    direct_cost = c1 + c2 + c3 + total_spacer_cost
    if add_pack: direct_cost += PROCESSING_COSTS["packing_transport"]
    if waste_pct_est > 0: direct_cost *= (1.0 + (waste_pct_est / 100.0))

    cost_with_gbe = direct_cost + (direct_cost * gbe_markup)
    final_price_m2 = cost_with_gbe + (cost_with_gbe * profit_markup)

    # FORMULATE RECIPE NAME
    full_recipe_name = name1
    if is_double and not is_triple:
        full_recipe_name += f"{spacer_desc} / {name2}"
    elif is_triple:
        full_recipe_name += f" / {sp1_size}mm {sp1_mat} + Argon / {name2} / {sp2_size}mm {sp2_mat} + Argon / {name3}"

    if has_temp1 or has_temp2 or has_temp3:
        full_recipe_name += " Tempered"

    if add_step:
        full_recipe_name += " [STEP]"

    st.markdown("---")
    st.markdown(f"### **Σύνθεση:** {full_recipe_name}")
    st.metric("Τελική Τιμή Πώλησης / m²", f"{final_price_m2:.2f} €")

    if st.button("💾 Αποθήκευση Συνταγής στη Βιβλιοθήκη"):
        st.session_state.recipes[full_recipe_name] = round(final_price_m2, 2)
        st.success(f"Η συνταγή '{full_recipe_name}' αποθηκεύτηκε με τιμή {final_price_m2:.2f} €/m²!")

# ---------------------------------------------------------
# TAB 2: RECIPE LIBRARY
# ---------------------------------------------------------
with tab2:
    st.header("📚 Αποθηκευμένες Συνταγές & Τιμοκατάλογος")
    if st.session_state.recipes:
        df_rec = pd.DataFrame(list(st.session_state.recipes.items()), columns=["Σύνθεση Υαλοστασίου", "Τιμή Πώλησης (€/m²)"])
        st.dataframe(df_rec, use_container_width=True)
    else:
        st.info("Δεν υπάρχουν ακόμα αποθηκευμένες συνταγές. Δημιουργήστε μία στην 1η καρτέλα.")

# ---------------------------------------------------------
# TAB 3: OFFER GENERATION, NESTING & VISUAL CUTTING DIAGRAMS
# ---------------------------------------------------------
with tab3:
    st.header("📊 Ακριβής Κοστολόγηση Παραγωγής, Nesting & PDF Προσφορά")
    
    selected_sheet_label = st.selectbox("📐 Επιλέξτε Διάσταση Αρχικού Φύλλου Κοπής (Stock Sheet):", list(STOCK_SHEETS.keys()))
    stock_w, stock_h = STOCK_SHEETS[selected_sheet_label]

    available_recipes = list(st.session_state.recipes.keys()) if st.session_state.recipes else ["CLIMAX SELECT 33.1 / 16mm Technoform Warm Edge + Argon / CLEAR FLOAT GLASS 4 mm Tempered"]
    
    default_data = pd.DataFrame([
        {"Επιλογή Συνταγής": available_recipes[0], "Πλάτος (mm)": 1086, "Ύψος (mm)": 473, "Τεμάχια": 1, "Σημειώσεις": ""},
        {"Επιλογή Συνταγής": available_recipes[0], "Πλάτος (mm)": 1106, "Ύψος (mm)": 473, "Τεμάχια": 1, "Σημειώσεις": ""},
    ])

    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config={
            "Επιλογή Συνταγής": st.column_config.SelectboxColumn("Σύνθεση", options=available_recipes, required=True),
            "Πλάτος (mm)": st.column_config.NumberColumn("Πλάτος (mm)", min_value=100, max_value=6000, step=1),
            "Ύψος (mm)": st.column_config.NumberColumn("Ύψος (mm)", min_value=100, max_value=6000, step=1),
            "Τεμάχια": st.column_config.NumberColumn("Τεμάχια", min_value=1, step=1),
            "Σημειώσεις": st.column_config.TextColumn("Σημειώσεις")
        },
        use_container_width=True
    )

    processed_items = []
    nesting_items = []

    for idx, row in edited_df.iterrows():
        recipe_full = str(row.get("Επιλογή Συνταγής", ""))
        clean_desc = clean_recipe_name(recipe_full)
        
        w_val = pd.to_numeric(row.get("Πλάτος (mm)"), errors="coerce")
        h_val = pd.to_numeric(row.get("Ύψος (mm)"), errors="coerce")
        q_val = pd.to_numeric(row.get("Τεμάχια"), errors="coerce")

        w = float(w_val) if pd.notna(w_val) else 0.0
        h = float(h_val) if pd.notna(h_val) else 0.0
        qty = int(q_val) if pd.notna(q_val) else 0

        if w > 0 and h > 0 and qty > 0:
            area_m2 = (w / 1000.0) * (h / 1000.0) * qty
            unit_price = st.session_state.recipes.get(recipe_full, 165.00)
            total_price = area_m2 * unit_price

            processed_items.append({
                "Περιγραφή": clean_desc,
                "Πλάτος (mm)": w,
                "Ύψος (mm)": h,
                "Τεμάχια": qty,
                "Τιμή/m² (€)": unit_price,
                "Σύνολο m²": round(area_m2, 2),
                "Σύνολο (€)": round(total_price, 2),
                "Σημειώσεις": str(row.get("Σημειώσεις", ""))
            })
            nesting_items.append({'w': w, 'h': h, 'qty': qty})

    df_processed = pd.DataFrame(processed_items)

    if not df_processed.empty:
        sheets_needed, waste_pct, total_m2, placed_sheets = run_nesting_optimization(nesting_items, stock_w, stock_h)

        st.subheader("📋 Επισκόπηση Υπολογισμών Παραγγελίας & Nesting Report")
        col_n1, col_n2, col_n3 = st.columns(3)
        col_n1.metric("Συνολικά Πραγματικά Καθαρά m²", f"{total_m2:.2f} m²")
        col_n2.metric("Φύλλα Κοπής (Stock Sheets)", f"{sheets_needed} τεμ")
        col_n3.metric("Πραγματική Φύρα Κοπής (Waste)", f"{waste_pct}%")

        st.dataframe(df_processed, use_container_width=True)

        st.subheader("🎨 Οπτική Διάταξη Κοπών (Cutting Layouts)")
        for idx, sheet_items in enumerate(placed_sheets):
            img_buf = create_nesting_diagram(sheet_items, idx, stock_w, stock_h)
            st.image(img_buf, caption=f"Διάταξη Φύλλου Κοπής #{idx + 1} ({stock_w} x {stock_h} mm)", use_container_width=True)

        df_summary = df_processed.groupby("Περιγραφή").agg({
            "Τεμάχια": "sum",
            "Σύνολο m²": "sum",
            "Τιμή/m² (€)": "mean",
            "Σύνολο (€)": "sum"
        }).reset_index()

        net_total = df_processed["Σύνολο (€)"].sum()
        vat_amount = net_total * 0.24
        grand_total = net_total + vat_amount
        advance_payment = grand_total * 0.40

        totals_dict = {
            "net": net_total,
            "vat": vat_amount,
            "total": grand_total,
            "advance": advance_payment
        }

        st.markdown("---")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        col_f1.metric("Καθαρή Αξία", f"{net_total:.2f} €")
        col_f2.metric("ΦΠΑ (24%)", f"{vat_amount:.2f} €")
        col_f3.metric("Σύνολο με ΦΠΑ", f"{grand_total:.2f} €")
        col_f4.metric("Προκαταβολή (40%)", f"{advance_payment:.2f} €")

        st.markdown("---")
        
        file_cust_name = customer_name.strip() if customer_name.strip() else "Customer"
        
        pdf_offer = generate_pdf_offer(customer_name, df_processed, df_summary, totals_dict)
        pdf_nesting = generate_pdf_nesting_report(customer_name, df_processed, stock_w, stock_h, sheets_needed, waste_pct, total_m2, placed_sheets)

        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            st.download_button(
                label="📄 Λήψη Προσφοράς σε PDF (PSG OFFER)",
                data=pdf_offer,
                file_name=f"PSG_Offer_{file_cust_name}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col_btn2:
            st.download_button(
                label="✂️ Λήψη Αναφοράς Κοπών & Nesting σε PDF (με Σχεδιαγράμματα)",
                data=pdf_nesting,
                file_name=f"PSG_Nesting_Report_{file_cust_name}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
