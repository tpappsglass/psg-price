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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------
# REGISTER UNICODE GREEK FONT (Arial Narrow / Arial)
# ---------------------------------------------------------
try:
    pdfmetrics.registerFont(TTFont('Arial', 'ARIALN.TTF'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'ARIALNB.TTF'))
    FONT_NAME = 'Arial'
    FONT_BOLD = 'Arial-Bold'
except Exception as e:
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
        FONT_NAME = 'Arial'
        FONT_BOLD = 'Arial-Bold'
    except:
        FONT_NAME = 'Helvetica'
        FONT_BOLD = 'Helvetica-Bold'

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="PSG PRICE - Calumen & Pro Nesting Engine", layout="wide")

# ---------------------------------------------------------
# EXTENDED GLASS DATABASE (KOSTOLOGIO)
# ---------------------------------------------------------
GLASS_DB = {
    "CLEAR FLOAT GLASS 3 mm": {"cost": 3.47},
    "CLEAR FLOAT GLASS 4 mm": {"cost": 4.20},
    "CLEAR FLOAT GLASS 5 mm": {"cost": 5.25},
    "CLEAR FLOAT GLASS 6 mm": {"cost": 6.30},
    "CLEAR FLOAT GLASS 8 mm": {"cost": 8.82},
    "CLEAR FLOAT GLASS 10 mm": {"cost": 11.03},
    "CLEAR FLOAT GLASS 12 mm": {"cost": 15.75},
    "TINTED FLOAT GLASS 4 mm": {"cost": 5.70},
    "TINTED FLOAT GLASS 5 mm": {"cost": 7.13},
    "TINTED FLOAT GLASS 6 mm": {"cost": 8.55},
    "TINTED FLOAT GLASS 8 mm": {"cost": 11.97},
    "TINTED FLOAT GLASS 10 mm": {"cost": 14.96},
    "SATINATED GLASS 4 mm": {"cost": 7.80},
    "SATINATED GLASS 5 mm": {"cost": 8.75},
    "SATINATED GLASS 6 mm": {"cost": 9.70},
    "SATINATED GLASS 8 mm": {"cost": 11.98},
    "SATINATED GLASS 10 mm": {"cost": 13.98},
    "MIRROR 3 mm": {"cost": 8.00},
    "MIRROR 4 mm": {"cost": 9.00},
    "MIRROR 5 mm": {"cost": 10.00},
    "MIRROR 6 mm": {"cost": 11.00},
    "DIAMANT® 4 mm": {"cost": 7.65},
    "DIAMANT® 5 mm": {"cost": 9.60},
    "DIAMANT® 6 mm": {"cost": 11.00},
    "DIAMANT® 8 mm": {"cost": 15.40},
    "DIAMANT® 10 mm": {"cost": 19.00},
    "COOL LITE® ST 108 6mm": {"cost": 23.00},
    "4mm LOUKI 4mm": {"cost": 13.00},
    "6mm LOUKI 6mm": {"cost": 19.70},
    "8mm LOUKI 8mm": {"cost": 27.00},
    "LAMINATED GLASS 33.1": {"cost": 11.00},
    "LAMINATED GLASS 33.2": {"cost": 13.00},
    "LAMINATED GLASS 33.4": {"cost": 17.00},
    "LAMINATED GLASS 33.2 MAT": {"cost": 14.00},
    "LAMINATED GLASS 33.2 SC": {"cost": 15.00},
    "LAMINATED GLASS 44.1": {"cost": 12.98},
    "LAMINATED GLASS 44.2": {"cost": 14.98},
    "LAMINATED GLASS 44.4": {"cost": 18.98},
    "LAMINATED GLASS 44.1 MAT": {"cost": 15.98},
    "LAMINATED GLASS 44.2 SC": {"cost": 16.98},
    "LAMINATED GLASS 55.1": {"cost": 15.32},
    "LAMINATED GLASS 55.2": {"cost": 17.32},
    "LAMINATED GLASS 55.4": {"cost": 21.32},
    "LAMINATED GLASS 55.1 MAT": {"cost": 18.32},
    "LAMINATED GLASS 55.2 SC": {"cost": 19.32},
    "LAMINATED GLASS 66.1": {"cost": 17.77},
    "LAMINATED GLASS 66.2": {"cost": 19.77},
    "LAMINATED GLASS 66.4": {"cost": 23.77},
    "LAMINATED GLASS 66.1 MAT": {"cost": 19.77},
    "LAMINATED GLASS 66.2 SC": {"cost": 21.77},
    "LAMINATED GLASS 88.1": {"cost": 24.50},
    "LAMINATED GLASS 66.8": {"cost": 31.77},
    "LAMINATED GLASS 88.12": {"cost": 46.87},
    "CLIMAX 4mm": {"cost": 5.70},
    "CLIMAX 6mm": {"cost": 7.80},
    "CLIMAX 33.1": {"cost": 13.00},
    "CLIMAX 44.1": {"cost": 14.98},
    "CLIMAX 33.1 SC": {"cost": 17.00},
    "CLIMAX SC 44.1 SC": {"cost": 18.98},
    "CLIMAX SELECT 4mm": {"cost": 6.70},
    "CLIMAX SELECT 6mm": {"cost": 8.20},
    "CLIMAX SELECT 33.1": {"cost": 14.00},
    "CLIMAX SELECT 44.1": {"cost": 15.98},
    "CLIMAX SELECT SC 33.1 SC": {"cost": 18.00},
    "CLIMAX SELECT SC 44.1 SC": {"cost": 19.98},
    "ŞİŞECAM T 62/44 6mm": {"cost": 9.70},
    "ŞİŞECAM T 62/44 8mm": {"cost": 12.22},
    "ŞİŞECAM T 43/28 6mm": {"cost": 9.70},
    "ŞİŞECAM T 43/28 8mm": {"cost": 12.22},
    "ŞİŞECAM T 70/33 6mm": {"cost": 12.20},
    "ŞİŞECAM T70/33 8mm": {"cost": 14.72},
    "PLANITHERM® XN 4mm": {"cost": 7.35},
    "PLANITHERM® XN 6mm": {"cost": 10.70},
    "PLANITHERM® XN 8mm": {"cost": 14.10},
    "STADIP® PLANITHERM® XN 33.1": {"cost": 18.40},
    "STADIP® PLANITHERM® XN 33.2": {"cost": 21.60},
    "STADIP® PLANITHERM® XN 33.2 SC": {"cost": 22.30},
    "STADIP® PLANITHERM® XN 44.1": {"cost": 17.80},
    "STADIP® PLANITHERM® XN 44.2": {"cost": 21.00},
    "STADIP® PLANITHERM® XN 44.2 SC": {"cost": 21.70},
    "STADIP® PLANITHERM® XN 66.1": {"cost": 25.10},
    "STADIP® PLANITHERM® XN 66.2": {"cost": 28.30},
    "STADIP® PLANITHERM® XN 66.2 SC": {"cost": 29.00},
    "PLANISTAR® EVO 4mm": {"cost": 8.75},
    "PLANISTAR® EVO 6mm": {"cost": 12.10},
    "PLANISTAR® EVO 8mm": {"cost": 15.50},
    "STADIP® PLANISTAR® EVO 33.1": {"cost": 16.20},
    "STADIP® PLANISTAR® EVO 33.2": {"cost": 19.40},
    "STADIP® PLANISTAR® EVO 33.2 SC": {"cost": 20.10},
    "STADIP® PLANISTAR® EVO 44.1": {"cost": 18.70},
    "STADIP® PLANISTAR® EVO 44.2": {"cost": 21.90},
    "STADIP® PLANISTAR® EVO 44.2 SC": {"cost": 22.60},
    "STADIP® PLANISTAR® EVO 66.1": {"cost": 26.00},
    "STADIP® PLANISTAR® EVO 66.2": {"cost": 29.20},
    "STADIP® PLANISTAR® EVO 66.2 SC": {"cost": 29.90},
    "PLANISTAR® SUN PLUS 4mm": {"cost": 10.75},
    "PLANISTAR® SUN PLUS 6mm": {"cost": 14.10},
    "STADIP® PLANISTAR® SUN PLUS 33.1": {"cost": 18.40},
    "STADIP® PLANISTAR® SUN PLUS 33.2": {"cost": 21.60},
    "STADIP® PLANISTAR® SUN PLUS 33.2 SC": {"cost": 22.30},
    "STADIP® PLANISTAR® SUN PLUS 44.1": {"cost": 20.90},
    "STADIP® PLANISTAR® SUN PLUS 44.2": {"cost": 24.10},
    "STADIP® PLANISTAR® SUN PLUS 44.2 SC": {"cost": 24.80},
    "COOL LITE® KN 166 II 6mm": {"cost": 16.50},
    "COOL LITE® KN 166 II 8mm": {"cost": 20.80},
    "COOL LITE® KN 166 II 10mm": {"cost": 24.60},
    "COOL LITE® KN 148 II 6mm": {"cost": 16.50},
    "COOL LITE® KN 148 II 8mm": {"cost": 20.80},
    "COOL LITE® KN 148 II 10mm": {"cost": 24.60},
    "COOL LITE® SKN 154 II 6mm": {"cost": 20.50},
    "COOL LITE® SKN 154 II 8mm": {"cost": 24.80},
    "COOL LITE® SKN 154 II 10mm": {"cost": 28.60},
    "COOL LITE® SKN 176 II 6mm": {"cost": 20.50},
    "COOL LITE® SKN 176 II 8mm": {"cost": 24.80},
    "COOL LITE® SKN 176 II 10mm": {"cost": 28.60},
    "COOL LITE® SKN 144 II 6mm": {"cost": 24.00},
    "COOL LITE® SKN 144 II 8mm": {"cost": 29.30},
    "COOL LITE® SKN 144 II 10mm": {"cost": 34.50},
    "COOL LITE® SKN 183 II 6mm": {"cost": 24.00},
    "COOL LITE® SKN 183 II 8mm": {"cost": 29.30},
    "COOL LITE® SKN 183 II 10mm": {"cost": 34.50},
    "COOL LITE® XTREME 61/29 6mm": {"cost": 26.00},
    "COOL LITE® XTREME 61/29 8mm": {"cost": 31.50},
    "COOL LITE® XTREME 61/29 10mm": {"cost": 36.50},
    "COOL LITE® XTREME 70/33 6mm": {"cost": 26.00},
    "COOL LITE® XTREME 70/33 8mm": {"cost": 31.50},
    "COOL LITE® XTREME 70/33 10mm": {"cost": 36.50},
    "GUARDIAN SN 70S II 6mm": {"cost": 18.10},
    "GUARDIAN SN 63S II 6mm": {"cost": 20.00},
    "GUARDIAN SNX 60S II 6mm": {"cost": 24.10},
    "GUARDIAN SN 70/37 II 6mm": {"cost": 21.30},
    "GUARDIAN SN 75 II 6mm": {"cost": 19.39},
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

# ---------------------------------------------------------
# PROCESSING COSTS (Base vs Flat Extras)
# ---------------------------------------------------------
COST_TEMP = 6.50
COST_LAMI_PROC = 7.00
COST_RODE = 1.20
COST_PACK = 3.50
COST_HOLES = 2.50 

FLAT_HST = 15.00
FLAT_SILKSCREEN = 15.00
FLAT_STEP = 15.00
FLAT_BONDING = 35.00 

STOCK_SHEETS = {
    "6.000 x 3.210 mm (Jumbo - Προεπιλογή)": (6000, 3210),
    "3.210 x 2.250 mm (Standard)": (3210, 2250),
    "2.550 x 1.605 mm (Half Sheet)": (2550, 1605)
}

# ---------------------------------------------------------
# SIDEBAR: FISCAL INPUTS
# ---------------------------------------------------------
st.sidebar.header("📋 Διαχείριση Παραγγελίας")
customer_name = st.sidebar.text_input("Όνομα Project / Πελάτη", "")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Δυναμικές Ρυθμίσεις Κοστολόγησης")

# Αλλαγμένες οι προεπιλεγμένες τιμές σύμφωνα με το αίτημα (28.0 και 16.0)
gbe_pct = st.sidebar.number_input("Γ.Β.Ε. / Έξοδα (%)", min_value=0.0, max_value=80.0, value=28.0, step=0.5)
profit_pct = st.sidebar.number_input("Καθαρό Κέρδος (%)", min_value=0.0, max_value=80.0, value=16.0, step=0.5)

gbe_markup = gbe_pct / (100.0 - gbe_pct) if gbe_pct < 100 else 0
profit_markup = profit_pct / (100.0 - profit_pct) if profit_pct < 100 else 0

st.sidebar.info(f"💡 **Markups:**\n- ΓΒE: +{gbe_markup*100:.2f}%\n- Κέρδος: +{profit_markup*100:.2f}%")

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def clean_recipe_name(full_name):
    if not full_name: return ""
    return full_name.split(" (")[0].strip()

def calculate_component_cost(glasses_list, pvbs_list, temp_list, hst_list, silk_list, holes_list, manual_rode):
    base_cost = 0.0
    extra_cost = 0.0
    num_glasses = len(glasses_list)
    
    any_tempered = any(temp_list)
    is_rode = manual_rode or any_tempered 

    for g in glasses_list:
        if g in GLASS_DB:
            base_cost += GLASS_DB[g]["cost"]

    for pvb in pvbs_list:
        if pvb in PVB_DB:
            base_cost += PVB_DB[pvb]

    for temp in temp_list:
        if temp: base_cost += COST_TEMP
        
    for hole in holes_list:
        if hole: base_cost += COST_HOLES

    for hst in hst_list:
        if hst: extra_cost += FLAT_HST
    for silk in silk_list:
        if silk: extra_cost += FLAT_SILKSCREEN

    if num_glasses > 1:
        base_cost += (num_glasses - 1) * COST_LAMI_PROC

    if is_rode:
        base_cost += COST_RODE

    return base_cost, extra_cost, any_tempered

# ---------------------------------------------------------
# INDUSTRIAL NESTING: Global Bottom-Left Fill (BLF) + MAXAS
# ---------------------------------------------------------
def run_guillotine_nesting(items, stock_w, stock_h):
    stock_area = (stock_w / 1000.0) * (stock_h / 1000.0)
    
    individual_pieces = []
    p_id = 1
    for item in items:
        for _ in range(item['qty']):
            individual_pieces.append({'id': p_id, 'w': item['w'], 'h': item['h']})
            p_id += 1

    # Ταξινόμηση βάσει μεγαλύτερης πλευράς (στήνει στήλες) και μετά εμβαδού
    individual_pieces.sort(key=lambda p: (max(p['w'], p['h']), p['w']*p['h']), reverse=True)

    sheets = []
    
    for p in individual_pieces:
        w_p, h_p = p['w'], p['h']
        orientations = [(w_p, h_p)]
        if w_p != h_p: orientations.append((h_p, w_p))
        
        best_sheet_idx = -1
        best_rect_idx = -1
        best_orientation = None
        
        best_x = float('inf')
        best_y = float('inf')
        best_area_fit = float('inf')
        
        for s_idx, sheet in enumerate(sheets):
            for r_idx, fr in enumerate(sheet['free_rects']):
                for ow, oh in orientations:
                    if ow <= fr['w'] and oh <= fr['h']:
                        area_fit = (fr['w'] * fr['h']) - (ow * oh)
                        
                        # Προτεραιότητες Αναζήτησης (Ο πυρήνας του στριμώγματος):
                        # 1. Πάντα προσπαθεί να γεμίσει το πιο ΠΑΛΙΟ φύλλο πρώτα (s_idx).
                        # 2. Αν είναι στο ίδιο φύλλο, σπρώχνει τέρμα ΑΡΙΣΤΕΡΑ (fr['x']).
                        # 3. Μετά σπρώχνει τέρμα ΚΑΤΩ (fr['y']).
                        is_better = False
                        if best_sheet_idx == -1:
                            is_better = True
                        elif s_idx < best_sheet_idx:
                            is_better = True
                        elif s_idx == best_sheet_idx:
                            if fr['x'] < best_x:
                                is_better = True
                            elif fr['x'] == best_x:
                                if fr['y'] < best_y:
                                    is_better = True
                                elif fr['y'] == best_y:
                                    if area_fit < best_area_fit:
                                        is_better = True
                        
                        if is_better:
                            best_sheet_idx = s_idx
                            best_x = fr['x']
                            best_y = fr['y']
                            best_area_fit = area_fit
                            best_rect_idx = r_idx
                            best_orientation = (ow, oh)
                            
        if best_sheet_idx != -1:
            # Βρέθηκε κενό!
            sheet = sheets[best_sheet_idx]
            fr = sheet['free_rects'].pop(best_rect_idx)
            ow, oh = best_orientation
            sheet['items'].append({'id': p['id'], 'x': fr['x'], 'y': fr['y'], 'w': ow, 'h': oh})
            
            w_left = fr['w'] - ow
            h_left = fr['h'] - oh
            
            # Δοκιμή MAXAS (Maximal Area Split)
            area_h_right = w_left * oh
            area_h_top = fr['w'] * h_left
            max_area_h = max(area_h_right, area_h_top)
            
            area_v_right = w_left * fr['h']
            area_v_top = ow * h_left
            max_area_v = max(area_v_right, area_v_top)
            
            if max_area_h > max_area_v:
                r_right = {'x': fr['x'] + ow, 'y': fr['y'], 'w': w_left, 'h': oh}
                r_top = {'x': fr['x'], 'y': fr['y'] + oh, 'w': fr['w'], 'h': h_left}
            else:
                r_right = {'x': fr['x'] + ow, 'y': fr['y'], 'w': w_left, 'h': fr['h']}
                r_top = {'x': fr['x'], 'y': fr['y'] + oh, 'w': ow, 'h': h_left}
                
            if r_right['w'] > 0 and r_right['h'] > 0: sheet['free_rects'].append(r_right)
            if r_top['w'] > 0 and r_top['h'] > 0: sheet['free_rects'].append(r_top)
            
        else:
            # Αναγκαστικό άνοιγμα νέου φύλλου
            best_new_ow, best_new_oh = orientations[0]
            best_new_maxas = -1
            for o_w, o_h in orientations:
                if o_w <= stock_w and o_h <= stock_h:
                    area_h = max((stock_w - o_w) * o_h, stock_w * (stock_h - o_h))
                    area_v = max((stock_w - o_w) * stock_h, o_w * (stock_h - o_h))
                    maxas = max(area_h, area_v)
                    if maxas > best_new_maxas:
                        best_new_maxas = maxas
                        best_new_ow, best_new_oh = o_w, o_h
            
            ow, oh = best_new_ow, best_new_oh
            
            new_sheet = {'items': [{'id': p['id'], 'x': 0, 'y': 0, 'w': ow, 'h': oh}], 'free_rects': []}
            
            w_left = stock_w - ow
            h_left = stock_h - oh
            
            area_h_right = w_left * oh
            area_h_top = stock_w * h_left
            max_area_h = max(area_h_right, area_h_top)
            
            area_v_right = w_left * stock_h
            area_v_top = ow * h_left
            max_area_v = max(area_v_right, area_v_top)
            
            if max_area_h > max_area_v:
                r_right = {'x': ow, 'y': 0, 'w': w_left, 'h': oh}
                r_top = {'x': 0, 'y': oh, 'w': stock_w, 'h': h_left}
            else:
                r_right = {'x': ow, 'y': 0, 'w': w_left, 'h': stock_h}
                r_top = {'x': 0, 'y': oh, 'w': ow, 'h': h_left}
                
            if r_right['w'] > 0 and r_right['h'] > 0: new_sheet['free_rects'].append(r_right)
            if r_top['w'] > 0 and r_top['h'] > 0: new_sheet['free_rects'].append(r_top)
            
            sheets.append(new_sheet)
            
    placed_sheets = [s['items'] for s in sheets]
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
        self.setFont(FONT_NAME, 8)
        self.setFillColor(colors.HexColor("#555555"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 36, 20, page_text)
        self.drawString(36, 20, "PAP SAFETY GLASS S.A. - PSG OFFER")
        self.restoreState()

def generate_pdf_offer(customer_name, df_items, df_summary, totals, est_delivery_str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=14, leading=16, textColor=colors.HexColor("#1A365D"))
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9, leading=11, textColor=colors.HexColor("#4A5568"))
    normal_style = ParagraphStyle('NormText', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, leading=10, textColor=colors.HexColor("#2D3748"))
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8, leading=10, textColor=colors.HexColor("#1A365D"))
    header_cell = ParagraphStyle('HeaderCell', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8, leading=10, textColor=colors.white, alignment=1)
    
    story = []
    cust_display = customer_name.upper() if customer_name.strip() else "-"
    date_str = est_delivery_str if est_delivery_str else pd.Timestamp.now().strftime('%d/%m/%Y')

    header_data = [
        [
            Paragraph("<b>PSG INDUSTRIES</b><br/><font size=11 color='#2B6CB0'>PSG OFFER - ΠΡΟΣΦΟΡΑ</font>", title_style),
            Paragraph(f"<b>PAP SAFETY GLASS S.A.</b><br/>INDUSTRIAL AREA OF THESSALONIKI<br/>tel: +30 2310 796 180<br/>psg@psglass.gr | www.psglass.gr", normal_style)
        ],
        [
            Paragraph(f"<b>CUSTOMER:</b> {cust_display}", subtitle_style),
            Paragraph(f"<b>DATE:</b> {pd.Timestamp.now().strftime('%d/%m/%Y')}<br/><b>EST. DELIVERY DATE:</b> {date_str}", normal_style)
        ]
    ]
    t_header = Table(header_data, colWidths=[300, 220])
    t_header.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_header)
    story.append(Spacer(1, 10))

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

    t_items = Table(items_table_data, colWidths=[230, 45, 45, 35, 55, 40, 70])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 10))

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

    t_summary = Table(summary_table_data, colWidths=[250, 40, 60, 70, 100])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#EDF2F7")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 10))

    financial_data = [
        [Paragraph("<b>WITHOUT VAT:</b>", bold_style), Paragraph(f"<b>{totals['net']:.2f}€</b>", bold_style)],
        [Paragraph("<b>VAT (24%):</b>", bold_style), Paragraph(f"<b>{totals['vat']:.2f}€</b>", bold_style)],
        [Paragraph("<b>TOTAL:</b>", title_style), Paragraph(f"<b>{totals['total']:.2f}€</b>", title_style)],
        [Paragraph("<b>Προκαταβολή 40%:</b>", bold_style), Paragraph(f"<b>{totals['advance']:.2f}€</b>", bold_style)],
    ]
    t_financial = Table(financial_data, colWidths=[120, 100])
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
    - <b>PEIRAEUS BANK:</b> GR67 0172 2610 00526101 3442 742 (ΛΟΓ: 5261-013442-742)<br/>
    - <b>EUROBANK:</b> GR66 0260 3500 0004 2020 0696 947 (SWIFT: ERBKGRAA)<br/>
    - <b>ALPHA BANK:</b> GR35 0140 7180 7180 0233 0001 437 (ΛΟΓ: 7180 0233 0001 437)
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
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=14, leading=16, textColor=colors.HexColor("#C53030"))
    normal_style = ParagraphStyle('NormText', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, leading=10, textColor=colors.HexColor("#2D3748"))
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9, leading=11, textColor=colors.HexColor("#1A365D"))
    header_cell = ParagraphStyle('HeaderCell', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8, leading=10, textColor=colors.white, alignment=1)

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
    holes_list = []

    st.markdown("---")
    st.markdown("##### 📄 1ο Φύλλο Γυαλιού")
    g1 = st.selectbox("Επιλογή 1ου Γυαλιού", list(GLASS_DB.keys()), key=f"{pane_key_prefix}_g1")
    t1 = st.checkbox("Security (Tempered) 1ο Γυαλί", key=f"{pane_key_prefix}_t1")
    h1 = st.checkbox("Heat Soak Test (HST) 1ο Γυαλί", key=f"{pane_key_prefix}_h1")
    s1 = st.checkbox("Μεταξοτυπία 1ο Γυαλί", key=f"{pane_key_prefix}_s1")
    hole1 = st.checkbox("Τρύπες 1ο Γυαλί", key=f"{pane_key_prefix}_hole1")
    
    glasses_list.append(g1)
    temp_list.append(t1)
    hst_list.append(h1)
    silk_list.append(s1)
    holes_list.append(hole1)

    for i in range(2, num_panes + 1):
        st.markdown(f"**🔗 Μεμβράνη PVB #{i-1}**")
        pvb = st.selectbox(f"Επιλογή PVB #{i-1}", list(PVB_DB.keys()), key=f"{pane_key_prefix}_pvb_{i-1}")
        pvbs_list.append(pvb)

        st.markdown(f"##### 📄 {i}ο Φύλλο Γυαλιού")
        g = st.selectbox(f"Επιλογή {i}ου Γυαλιού", list(GLASS_DB.keys()), key=f"{pane_key_prefix}_g{i}")
        t = st.checkbox(f"Security (Tempered) {i}ο Γυαλί", key=f"{pane_key_prefix}_t{i}")
        h = st.checkbox(f"Heat Soak Test (HST) {i}ο Γυαλί", key=f"{pane_key_prefix}_h{i}")
        s = st.checkbox(f"Μεταξοτυπία {i}ο Γυαλί", key=f"{pane_key_prefix}_s{i}")
        hole = st.checkbox(f"Τρύπες {i}ο Γυαλί", key=f"{pane_key_prefix}_hole{i}")
        
        glasses_list.append(g)
        temp_list.append(t)
        hst_list.append(h)
        silk_list.append(s)
        holes_list.append(hole)

    any_temp = any(temp_list)
    rode_label = "Ροντέ / Τρόχισμα (Μπαίνει αυτόματα λόγω Tempered)" if any_temp else "Ροντέ / Τρόχισμα (Laminated)"
    p_rode = st.checkbox(rode_label, value=any_temp, disabled=any_temp, key=f"{pane_key_prefix}_rode")

    name = "+".join(glasses_list)
    return glasses_list, pvbs_list, temp_list, hst_list, silk_list, holes_list, p_rode, name, any_temp

# ---------------------------------------------------------
# STREAMLIT UI & APPS
# ---------------------------------------------------------
st.title("🧮 PSG PRICE - Calumen Style Configurator & Pro Nesting Engine")

if 'recipes' not in st.session_state:
    st.session_state.recipes = {}

if 'last_recipe_name' not in st.session_state:
    st.session_state.last_recipe_name = None

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
    
    c1_base, c1_extra, has_temp1 = 0.0, 0.0, False
    name1 = ""

    with col1:
        st.subheader("🔵 Εξωτερικός Υαλοπίνακας (Γ1)")
        p1_lami = st.checkbox("Είναι Laminated / Συγκολλημένος", key="p1_lami")
        
        if p1_lami:
            st.markdown("**Σύνθεση Triplex / Laminated:**")
            g_list, pvb_list, t_list, h_list, s_list, hole_list, rode, name1, has_temp1 = build_laminated_ui("g1", "CLEAR FLOAT GLASS 4 mm")
            c1_base, c1_extra, _ = calculate_component_cost(g_list, pvb_list, t_list, h_list, s_list, hole_list, rode)
        else:
            g1_main = st.selectbox("Επιλογή Βασικού Γυαλιού 1", list(GLASS_DB.keys()), key="g1_main")
            p1_temp_main = st.checkbox("Security / Tempered", key="p1_temp_m")
            p1_hst_main = st.checkbox("Heat Soak Test (HST)", key="p1_hst_m")
            p1_silk_main = st.checkbox("Μεταξοτυπία", key="p1_silk_m")
            p1_holes_main = st.checkbox("Τρύπες", key="p1_holes_m")
            
            p1_rode_lbl = "Ροντέ / Τρόχισμα (Αυτόματα)" if p1_temp_main else "Ροντέ / Τρόχισμα"
            p1_rode = st.checkbox(p1_rode_lbl, value=p1_temp_main, disabled=p1_temp_main, key="p1_rode")

            name1 = g1_main
            has_temp1 = p1_temp_main
            c1_base, c1_extra, _ = calculate_component_cost([g1_main], [], [p1_temp_main], [p1_hst_main], [p1_silk_main], [p1_holes_main], p1_rode)

    c2_base, c2_extra, has_temp2 = 0.0, 0.0, False
    name2 = ""

    if is_double:
        with col2:
            st.subheader("🟢 Μεσαίος / Εσωτερικός (Γ2)")
            p2_lami = st.checkbox("Είναι Laminated / Συγκολλημένος ", key="p2_lami")
            if p2_lami:
                st.markdown("**Σύνθεση Triplex / Laminated:**")
                g_list, pvb_list, t_list, h_list, s_list, hole_list, rode, name2, has_temp2 = build_laminated_ui("g2", "CLEAR FLOAT GLASS 4 mm")
                c2_base, c2_extra, _ = calculate_component_cost(g_list, pvb_list, t_list, h_list, s_list, hole_list, rode)
            else:
                g2_main = st.selectbox("Επιλογή Βασικού Γυαλιού 2", list(GLASS_DB.keys()), key="g2_main")
                p2_temp_main = st.checkbox("Security / Tempered ", key="p2_temp_m")
                p2_hst_main = st.checkbox("Heat Soak Test (HST) ", key="p2_hst_m")
                p2_silk_main = st.checkbox("Μεταξοτυπία ", key="p2_silk_m")
                p2_holes_main = st.checkbox("Τρύπες ", key="p2_holes_m")
                
                p2_rode_lbl = "Ροντέ / Τρόχισμα (Αυτόματα)" if p2_temp_main else "Ροντέ / Τρόχισμα "
                p2_rode = st.checkbox(p2_rode_lbl, value=p2_temp_main, disabled=p2_temp_main, key="p2_rode")

                name2 = g2_main
                has_temp2 = p2_temp_main
                c2_base, c2_extra, _ = calculate_component_cost([g2_main], [], [p2_temp_main], [p2_hst_main], [p2_silk_main], [p2_holes_main], p2_rode)

    c3_base, c3_extra, has_temp3 = 0.0, 0.0, False
    name3 = ""

    if is_triple:
        with col3:
            st.subheader("🔴 Εσωτερικός (Γ3)")
            p3_lami = st.checkbox("Είναι Laminated / Συγκολλημένος  ", key="p3_lami")
            if p3_lami:
                st.markdown("**Σύνθεση Triplex / Laminated:**")
                g_list, pvb_list, t_list, h_list, s_list, hole_list, rode, name3, has_temp3 = build_laminated_ui("g3", "CLEAR FLOAT GLASS 4 mm")
                c3_base, c3_extra, _ = calculate_component_cost(g_list, pvb_list, t_list, h_list, s_list, hole_list, rode)
            else:
                g3_main = st.selectbox("Επιλογή Βασικού Γυαλιού 3", list(GLASS_DB.keys()), key="g3_main")
                p3_temp_main = st.checkbox("Security / Tempered  ", key="p3_temp_m")
                p3_hst_main = st.checkbox("Heat Soak Test (HST)  ", key="p3_hst_m")
                p3_silk_main = st.checkbox("Μεταξοτυπία  ", key="p3_silk_m")
                p3_holes_main = st.checkbox("Τρύπες  ", key="p3_holes_m")
                
                p3_rode_lbl = "Ροντέ / Τρόχισμα (Αυτόματα)" if p3_temp_main else "Ροντέ / Τρόχισμα  "
                p3_rode = st.checkbox(p3_rode_lbl, value=p3_temp_main, disabled=p3_temp_main, key="p3_rode")

                name3 = g3_main
                has_temp3 = p3_temp_main
                c3_base, c3_extra, _ = calculate_component_cost([g3_main], [], [p3_temp_main], [p3_hst_main], [p3_silk_main], [p3_holes_main], p3_rode)

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
            add_step = st.checkbox("Επεξεργασία STEP", key="add_step")

        key1 = f"{'Technoform' if 'Technoform' in sp1_mat else 'Aluminium'} {'< 18mm' if sp1_size < 18 else '> 18mm'}"
        total_spacer_cost = SPACER_PRICES.get(key1, 10.00)
        spacer_desc = f" / {sp1_size}mm {sp1_mat} + Argon"

    elif is_triple:
        st.markdown("---")
        st.subheader("🔲 Ρυθμίσεις Δύο Διάκενων / Αποστατών (Spacers) & Step")
        col_sp1, col_sp2, col_sp3 = st.columns(3)
        with col_sp1:
            sp1_mat = st.selectbox("Υλικό 1ου Διάκενου", ["Technoform Warm Edge", "Aluminium"], key="sp1_mat_trip")
            sp1_size = st.selectbox("Πάχος 1ου Διάκενου (mm)", [10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32], index=4, key="sp1_size_trip")
        with col_sp2:
            sp2_mat = st.selectbox("Υλικό 2ου Διάκενου", ["Technoform Warm Edge", "Aluminium"], key="sp2_mat_trip")
            sp2_size = st.selectbox("Πάχος 2ου Διάκενου (mm)", [10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32], index=4, key="sp2_size_trip")
        with col_sp3:
            add_step = st.checkbox("Επεξεργασία STEP", key="add_step_trip")

        key1 = f"{'Technoform' if 'Technoform' in sp1_mat else 'Aluminium'} {'< 18mm' if sp1_size < 18 else '> 18mm'}"
        key2 = f"{'Technoform' if 'Technoform' in sp2_mat else 'Aluminium'} {'< 18mm' if sp2_size < 18 else '> 18mm'}"
        total_spacer_cost = SPACER_PRICES.get(key1, 10.00) + SPACER_PRICES.get(key2, 10.00)
        spacer_desc = f" / {sp1_size}mm {sp1_mat} + Argon"

    st.markdown("---")
    col_opt1, col_opt2, col_opt3 = st.columns(3)
    with col_opt1:
        add_pack = st.checkbox("Προσθήκη Συσκευασίας & Μεταφοράς", value=True)
    with col_opt2:
        add_bonding = st.checkbox("Επεξεργασία Bonding (+35€/m² ΜΟΝΟ αν τεμάχιο > 4m²)", key="add_bonding")
    with col_opt3:
        waste_pct_est = st.number_input("⚠️ Εκτιμώμενη Φθορά Υλικού (%) [Προαιρετικά]", min_value=0.0, max_value=50.0, value=0.0, step=1.0)

    base_direct_cost = c1_base + c2_base + c3_base + total_spacer_cost
    if add_pack: base_direct_cost += COST_PACK
    if waste_pct_est > 0: base_direct_cost *= (1.0 + (waste_pct_est / 100.0))

    base_with_gbe = base_direct_cost * (1 + gbe_markup)
    final_base_m2 = base_with_gbe * (1 + profit_markup)

    total_flat_extras = c1_extra + c2_extra + c3_extra
    if add_step:
        total_flat_extras += FLAT_STEP

    display_price_m2 = final_base_m2 + total_flat_extras

    full_recipe_name = name1
    if is_double and not is_triple:
        full_recipe_name += f"{spacer_desc} / {name2}"
    elif is_triple:
        full_recipe_name += f" / {sp1_size}mm {sp1_mat} + Argon / {name2} / {sp2_size}mm {sp2_mat} + Argon / {name3}"

    if has_temp1 or has_temp2 or has_temp3:
        full_recipe_name += " Tempered"
    if add_step:
        full_recipe_name += " [STEP]"
    if add_bonding:
        full_recipe_name += " [BONDING]"

    st.markdown("---")
    st.markdown(f"### **Σύνθεση:** {full_recipe_name}")
    st.metric("Τελική Βασική Τιμή Πώλησης / m²", f"{display_price_m2:.2f} €")
    if add_bonding:
        st.info("ℹ️ **Σημείωση:** Το κόστος Bonding (+35€/m²) θα προστεθεί αυτόματα στην 3η καρτέλα, μόνο για τα τεμάχια που υπερβαίνουν τα 4m².")

    col_btn_save, col_btn_transfer = st.columns(2)
    
    with col_btn_save:
        if st.button("💾 Αποθήκευση Συνταγής στη Βιβλιοθήκη", use_container_width=True):
            st.session_state.recipes[full_recipe_name] = {
                "base_m2": final_base_m2,
                "extras_m2": total_flat_extras,
                "has_bonding": add_bonding,
                "display": display_price_m2
            }
            st.session_state.last_recipe_name = full_recipe_name
            st.success(f"Η συνταγή αποθηκεύτηκε!")

    with col_btn_transfer:
        if st.button("📥 Μεταφορά & Ενημέρωση 3ης Καρτέλας", use_container_width=True):
            st.session_state.recipes[full_recipe_name] = {
                "base_m2": final_base_m2,
                "extras_m2": total_flat_extras,
                "has_bonding": add_bonding,
                "display": display_price_m2
            }
            st.session_state.last_recipe_name = full_recipe_name
            st.info("Η σύνθεση μεταφέρθηκε επιτυχώς στη Φόρμα Κοστολόγησης!")

# ---------------------------------------------------------
# TAB 2: RECIPE LIBRARY
# ---------------------------------------------------------
with tab2:
    st.header("📚 Αποθηκευμένες Συνταγές & Τιμοκατάλογος")
    if st.session_state.recipes:
        display_data = []
        for k, v in st.session_state.recipes.items():
            if isinstance(v, dict):
                price = v["display"]
            else:
                price = v 
            display_data.append([k, f"{price:.2f} €"])
        
        df_rec = pd.DataFrame(display_data, columns=["Σύνθεση Υαλοστασίου", "Βασική Τιμή (€/m²)"])
        st.dataframe(df_rec, use_container_width=True)
    else:
        st.info("Δεν υπάρχουν ακόμα αποθηκευμένες συνταγές. Δημιουργήστε μία στην 1η καρτέλα.")

# ---------------------------------------------------------
# TAB 3: OFFER GENERATION, NESTING & PDF
# ---------------------------------------------------------
with tab3:
    st.header("📊 Ακριβής Κοστολόγηση Παραγωγής, Pro Nesting & PDF Προσφορά")
    
    selected_sheet_label = st.selectbox("📐 Επιλέξτε Διάσταση Αρχικού Φύλλου Κοπής (Stock Sheet):", list(STOCK_SHEETS.keys()))
    stock_w, stock_h = STOCK_SHEETS[selected_sheet_label]

    available_recipes = list(st.session_state.recipes.keys()) if st.session_state.recipes else ["Παρακαλώ φτιάξτε συνταγή στην 1η Καρτέλα"]
    active_recipe = st.session_state.get('last_recipe_name', available_recipes[0])
    if active_recipe not in available_recipes:
        active_recipe = available_recipes[0]

    default_data = pd.DataFrame([
        {"Επιλογή Συνταγής": active_recipe, "Πλάτος (mm)": 1086, "Ύψος (mm)": 473, "Τεμάχια": 1, "Σημειώσεις": ""},
        {"Επιλογή Συνταγής": active_recipe, "Πλάτος (mm)": 1106, "Ύψος (mm)": 473, "Τεμάχια": 1, "Σημειώσεις": ""},
    ])

    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config={
            "Επιλογή Συνταγής": st.column_config.SelectboxColumn("Σύνθεση", options=available_recipes, default=active_recipe, required=True),
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
        recipe_full = str(row.get("Επιλογή Συνταγής", active_recipe))
        clean_desc = clean_recipe_name(recipe_full)
        
        w_val = pd.to_numeric(row.get("Πλάτος (mm)"), errors="coerce")
        h_val = pd.to_numeric(row.get("Ύψος (mm)"), errors="coerce")
        q_val = pd.to_numeric(row.get("Τεμάχια"), errors="coerce")

        w = float(w_val) if pd.notna(w_val) else 0.0
        h = float(h_val) if pd.notna(h_val) else 0.0
        qty = int(q_val) if pd.notna(q_val) else 0

        if w > 0 and h > 0 and qty > 0:
            area_m2 = (w / 1000.0) * (h / 1000.0)
            total_area_m2 = area_m2 * qty
            
            rec_val = st.session_state.recipes.get(recipe_full, {"base_m2": 165.0, "extras_m2": 0.0, "has_bonding": False})
            if isinstance(rec_val, (float, int)):
                unit_price = rec_val
            else:
                unit_price = rec_val["base_m2"] + rec_val["extras_m2"]
                if rec_val["has_bonding"] and area_m2 > 4.0:
                    unit_price += FLAT_BONDING

            total_price = total_area_m2 * unit_price

            processed_items.append({
                "Περιγραφή": clean_desc,
                "Πλάτος (mm)": w,
                "Ύψος (mm)": h,
                "Τεμάχια": qty,
                "Τιμή/m² (€)": unit_price,
                "Σύνολο m²": round(total_area_m2, 2),
                "Σύνολο (€)": round(total_price, 2),
                "Σημειώσεις": str(row.get("Σημειώσεις", ""))
            })
            nesting_items.append({'w': w, 'h': h, 'qty': qty})

    df_processed = pd.DataFrame(processed_items)

    if not df_processed.empty:
        sheets_needed, waste_pct, total_m2, placed_sheets = run_guillotine_nesting(nesting_items, stock_w, stock_h)

        st.subheader("📋 Επισκόπηση Υπολογισμών Παραγγελίας & Nesting Report")
        col_n1, col_n2, col_n3 = st.columns(3)
        col_n1.metric("Συνολικά Πραγματικά Καθαρά m²", f"{total_m2:.2f} m²")
        col_n2.metric("Φύλλα Κοπής (Stock Sheets)", f"{sheets_needed} τεμ")
        col_n3.metric("Πραγματική Φύρα Κοπής (Waste)", f"{waste_pct}%")

        st.dataframe(df_processed, use_container_width=True)

        st.subheader("🎨 Οπτική Διάταξη Κοπών (Pro Guillotine 2D Packing)")
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
        st.subheader("📅 Ημερομηνία Παράδοσης")
        est_delivery_date = st.date_input("Επιλέξτε Εκτιμώμενη Ημερομηνία Παράδοσης (EST. DELIVERY DATE):")
        est_delivery_str = est_delivery_date.strftime('%d/%m/%Y')
        
        file_cust_name = customer_name.strip() if customer_name.strip() else "Customer"
        
        pdf_offer = generate_pdf_offer(customer_name, df_processed, df_summary, totals_dict, est_delivery_str)
        pdf_nesting = generate_pdf_nesting_report(customer_name, df_processed, stock_w, stock_h, sheets_needed, waste_pct, total_m2, placed_sheets)

        st.markdown("<br>", unsafe_allow_html=True)
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
