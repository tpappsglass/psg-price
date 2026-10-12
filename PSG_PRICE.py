import streamlit as st
import pandas as pd
import google.generativeai as genai
import io

# --- SAFE IMPORT REPORTLAB ---
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing, Rect, String

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="PSG PRICE - Calumen Engine", layout="wide")
st.title("🪟 PSG PRICE - Calumen Style Configurator & Precision Nesting Engine")

# --- 2. ΒΙΒΛΙΟΘΗΚΗ ΥΑΛΟΠΙΝΑΚΩΝ ---
if 'GLASS_CATALOG' not in st.session_state:
    st.session_state.GLASS_CATALOG = {
        # CLEAR FLOAT GLASS
        "CLEAR FLOAT GLASS 3mm": {"thick": 3.0, "price": 3.47, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "CLEAR FLOAT GLASS 4mm": {"thick": 4.0, "price": 4.20, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "CLEAR FLOAT GLASS 5mm": {"thick": 5.0, "price": 5.25, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "CLEAR FLOAT GLASS 6mm": {"thick": 6.0, "price": 6.30, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "CLEAR FLOAT GLASS 8mm": {"thick": 8.0, "price": 8.82, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "CLEAR FLOAT GLASS 10mm": {"thick": 10.0, "price": 11.03, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "CLEAR FLOAT GLASS 12mm": {"thick": 12.0, "price": 15.75, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},

        # TINTED FLOAT GLASS
        "TINTED FLOAT GLASS 4mm": {"thick": 4.0, "price": 5.70, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "TINTED FLOAT GLASS 5mm": {"thick": 5.0, "price": 7.13, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "TINTED FLOAT GLASS 6mm": {"thick": 6.0, "price": 8.55, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "TINTED FLOAT GLASS 8mm": {"thick": 8.0, "price": 11.97, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "TINTED FLOAT GLASS 10mm": {"thick": 10.0, "price": 14.96, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},

        # SATINATED GLASS
        "SATINATED GLASS 4mm": {"thick": 4.0, "price": 7.80, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "SATINATED GLASS 5mm": {"thick": 5.0, "price": 8.75, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "SATINATED GLASS 6mm": {"thick": 6.0, "price": 9.70, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "SATINATED GLASS 8mm": {"thick": 8.0, "price": 11.98, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "SATINATED GLASS 10mm": {"thick": 10.0, "price": 13.98, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},

        # MIRROR
        "MIRROR 3mm": {"thick": 3.0, "price": 8.00, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": False},
        "MIRROR 4mm": {"thick": 4.0, "price": 9.00, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": False},
        "MIRROR 5mm": {"thick": 5.0, "price": 10.00, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": False},
        "MIRROR 6mm": {"thick": 6.0, "price": 11.00, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": False},

        # DIAMANT® (ULTRA CLEAR)
        "DIAMANT® 4mm": {"thick": 4.0, "price": 7.65, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "DIAMANT® 5mm": {"thick": 5.0, "price": 9.60, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "DIAMANT® 6mm": {"thick": 6.0, "price": 11.00, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "DIAMANT® 8mm": {"thick": 8.0, "price": 15.40, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},
        "DIAMANT® 10mm": {"thick": 10.0, "price": 19.00, "temp": "NORMAL", "kopi": "ΜΟΝΗ", "xil": False},

        # LOUKI / SPECIAL
        "COOL LITE® ST 108 6mm": {"thick": 6.0, "price": 23.00, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": False},
        "4mm LOUKI": {"thick": 4.0, "price": 13.00, "temp": "LOW-E", "kopi": "LAMI", "xil": False},
        "6mm LOUKI": {"thick": 6.0, "price": 19.70, "temp": "LOW-E", "kopi": "LAMI", "xil": False},
        "8mm LOUKI": {"thick": 8.0, "price": 27.00, "temp": "LOW-E", "kopi": "LAMI", "xil": False},

        # LAMINATED GLASS
        "LAMINATED GLASS 33.1 (6.38mm)": {"thick": 6.38, "price": 11.00, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 33.2 (6.76mm)": {"thick": 6.76, "price": 13.00, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 33.4 (7.52mm)": {"thick": 7.52, "price": 17.00, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 33.2 MAT": {"thick": 6.76, "price": 14.00, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 33.2 SC": {"thick": 6.76, "price": 15.00, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 44.1 (8.38mm)": {"thick": 8.38, "price": 12.98, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 44.2 (8.76mm)": {"thick": 8.76, "price": 14.98, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 44.4 (9.52mm)": {"thick": 9.52, "price": 18.98, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 44.1 MAT": {"thick": 8.38, "price": 15.98, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 44.2 SC": {"thick": 8.76, "price": 16.98, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 55.1 (10.38mm)": {"thick": 10.38, "price": 15.32, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 55.2 (10.76mm)": {"thick": 10.76, "price": 17.32, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 55.4 (11.52mm)": {"thick": 11.52, "price": 21.32, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 55.1 MAT": {"thick": 10.38, "price": 18.32, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 55.2 SC": {"thick": 10.76, "price": 19.32, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 66.1 (12.38mm)": {"thick": 12.38, "price": 17.77, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 66.2 (12.76mm)": {"thick": 12.76, "price": 19.77, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 66.4 (13.52mm)": {"thick": 13.52, "price": 23.77, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 66.1 MAT": {"thick": 12.38, "price": 19.77, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 66.2 SC": {"thick": 12.76, "price": 21.77, "temp": "NO", "kopi": "LAMI", "xil": False},
        "LAMINATED GLASS 88.1 (16.38mm)": {"thick": 16.38, "price": 24.50, "temp": "NO", "kopi": "LAMI", "xil": False},

        # ΕΞΑΙΡΕΙΣΕΙΣ LAMINATED GLASS
        "LAMINATED GLASS 66.8 (15.04mm) [Εξαίρεση]": {"thick": 15.04, "price": 31.77, "temp": "NO", "kopi": "3€/m2",
                                                      "xil": False},
        "LAMINATED GLASS 88.12 (20.56mm) [Εξαίρεση]": {"thick": 20.56, "price": 46.87, "temp": "NO", "kopi": "4€/m2",
                                                       "xil": True},

        # CLIMAX & CLIMAX SELECT
        "CLIMAX 4mm": {"thick": 4.0, "price": 5.70, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},
        "CLIMAX 6mm": {"thick": 6.0, "price": 7.80, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},
        "CLIMAX 33.1": {"thick": 6.38, "price": 13.00, "temp": "NO", "kopi": "LAMI", "xil": True},
        "CLIMAX 44.1": {"thick": 8.38, "price": 14.98, "temp": "NO", "kopi": "LAMI", "xil": True},
        "CLIMAX 33.1 SC": {"thick": 6.38, "price": 17.00, "temp": "NO", "kopi": "LAMI", "xil": True},
        "CLIMAX 44.1 SC": {"thick": 8.38, "price": 18.98, "temp": "NO", "kopi": "LAMI", "xil": True},
        "CLIMAX SELECT 4mm": {"thick": 4.0, "price": 6.70, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},
        "CLIMAX SELECT 6mm": {"thick": 6.0, "price": 8.20, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},

        # ŞİŞECAM TEMPERABLE LOW-E
        "ŞİŞECAM T 62/44 6mm": {"thick": 6.0, "price": 9.70, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
        "ŞİŞECAM T 62/44 8mm": {"thick": 8.0, "price": 12.22, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},

        # PLANITHERM®, PLANISTAR® & COOL LITE®
        "PLANITHERM® XN 4mm": {"thick": 4.0, "price": 7.35, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},
        "PLANITHERM® XN 6mm": {"thick": 6.0, "price": 10.70, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},
        "PLANISTAR® EVO 4mm": {"thick": 4.0, "price": 8.75, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},
        "PLANISTAR® EVO 6mm": {"thick": 6.0, "price": 12.10, "temp": "NO", "kopi": "ΜΟΝΗ", "xil": True},

        "COOL LITE® KN 166 II 6mm": {"thick": 6.0, "price": 16.50, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
        "COOL LITE® KN 166 II 8mm": {"thick": 8.0, "price": 20.80, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
        "COOL LITE® SKN 154 II 6mm": {"thick": 6.0, "price": 20.50, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
        "COOL LITE® SKN 154 II 8mm": {"thick": 8.0, "price": 24.80, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
        "COOL LITE® XTREME 61/29 6mm": {"thick": 6.0, "price": 26.00, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},

        # GUARDIAN
        "GUARDIAN SN 70S II 6mm": {"thick": 6.0, "price": 18.10, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
        "GUARDIAN SN 63S II 6mm": {"thick": 6.0, "price": 20.00, "temp": "LOW-E", "kopi": "ΜΟΝΗ", "xil": True},
    }

# --- 3. ΒΙΒΛΙΟΘΗΚΗ PVB & SPACERS ---
if 'PVB_EXTRAS' not in st.session_state:
    st.session_state.PVB_EXTRAS = {
        "Χωρίς Έξτρα Μεμβράνη": {"thick": 0.00, "price": 0.00},
        "PVB CLEAR 0.38mm (+€3.20)": {"thick": 0.38, "price": 3.20},
        "PVB CLEAR 0.76mm (+€6.23)": {"thick": 0.76, "price": 6.23},
        "PVB CLEAR 1.14mm (+€9.73)": {"thick": 1.14, "price": 9.73},
        "PVB CLEAR 1.52mm (+€12.51)": {"thick": 1.52, "price": 12.51},
        "PVB ACOUSTIC (SC) 0.76mm (+€8.97)": {"thick": 0.76, "price": 8.97},
        "PVB MAT 0.38mm (+€6.86)": {"thick": 0.38, "price": 6.86},
        "PVB GREY 0.38mm (+€5.50)": {"thick": 0.38, "price": 5.50},
        "PVB BRONZE (+€5.50)": {"thick": 0.38, "price": 5.50},
    }

if 'SPACERS_CATALOG' not in st.session_state:
    spacers = {}
    widths = [10, 11, 12, 14, 15, 16, 18, 20, 22, 24, 26, 27, 28, 30, 32]
    for w in widths:
        price = 8.00 if w <= 18 else 12.00
        spacers[f"ALUMINIUM {w}mm (+€{price:.2f}/m²)"] = {"thick": float(w), "price": price, "type": "ALUMINIUM"}
    for w in [10, 11, 12, 14, 15, 16, 18, 20, 22, 24, 26, 27]:
        price = 10.00 if w <= 18 else 15.00
        spacers[f"TECHNOFORM (Warm-Edge) {w}mm (+€{price:.2f}/m²)"] = {"thick": float(w), "price": price,
                                                                       "type": "TECHNOFORM"}
    st.session_state.SPACERS_CATALOG = spacers

if 'RECIPES' not in st.session_state:
    st.session_state.RECIPES = {
        "CLEAR FLOAT 10mm (Security + Rode)": {
            "type": "Μονό Γυαλί",
            "layers": ["CLEAR FLOAT GLASS 10mm (Security) (Rode)"],
            "total_thick": 10.0,
            "raw_glass_cost_m2": 11.03,
            "processing_cost_m2": 8.00,
            "has_rode": True,
            "pack_trans": False
        }
    }

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("📂 Διαχείριση Παραγγελίας")
    project_name = st.text_input("Όνομα Project / Πελάτη:", value="Παραγγελία_01")
    uploaded_file = st.file_uploader("Φόρτωση Αρχείου (.csv):", type=["csv"])

    st.header("⚙️ Ρυθμίσεις Κοστολόγησης")
    st.caption("🎯 **Στόχος Τζίρου:** 25% ΓΒΕ & 15% Καθαρό Κέρδος (Άμεσο Κόστος 60%)")
    api_key = st.text_input("Gemini API Key:", type="password")

    # --- ΕΝΗΜΕΡΩΜΕΝΑ ΠΟΣΟΣΤΑ ΠΡΟΣΑΥΞΗΣΗΣ (MARKUPS) ---
    gbe_pct = st.number_input("Γ.Β.Ε. Markup (%) [Στόχος 25% Τζίρου]", value=41.67, step=0.01) / 100
    profit_pct = st.number_input("Καθαρό Κέρδος Markup (%) [Στόχος 15% Τζίρου]", value=17.65, step=0.01) / 100
    waste_pct = st.number_input("Προεπιλεγμένη Φύρα Υλικού (%)", value=15.0, step=1.0) / 100

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(
    ["🧪 Calumen Recipe Builder", "📚 Βιβλιοθήκη Συνταγών", "📊 Κοστολόγηση Παραγγελίας & Precision Nesting"])


def render_glass_processing_options(key_prefix, glass_info):
    col_a, col_b, col_c, col_d = st.columns(4)
    thick = glass_info["thick"]
    temp_type = glass_info.get("temp", "NORMAL")
    force_xil = glass_info.get("xil", False)

    with col_a:
        sec = st.checkbox("🔥 Security / Tempered", key=f"{key_prefix}_sec", disabled=(temp_type == "NO"))

    auto_rode = True if sec else False

    with col_b:
        rode = st.checkbox("🛠️ Ροντέ / Rode", value=auto_rode or st.session_state.get(f"{key_prefix}_rode", False),
                           key=f"{key_prefix}_rode", disabled=sec)
    with col_c:
        xil = st.checkbox("🪵 Ξυλούρισμα", value=force_xil, key=f"{key_prefix}_xil", disabled=force_xil)
    with col_d:
        holes = st.number_input("🕳️ Τρύπες (τεμ)", min_value=0, max_value=20, value=0, key=f"{key_prefix}_holes")

    proc_cost = 0.0
    effective_rode = rode or sec

    if sec:
        rate = 0.8 if temp_type == "LOW-E" else 0.5
        proc_cost += rate * thick
    if effective_rode:
        proc_cost += 1.00
    if xil or force_xil:
        proc_cost += 1.00
    if holes > 0:
        proc_cost += holes * 1.00

    return proc_cost, sec, effective_rode, (xil or force_xil), holes


# GUILLOTINE 2D NESTING ALGORITHM
def run_guillotine_nesting_optimisation(pieces_list, sheet_w, sheet_h, kerf=3.0, margin=10.0):
    expanded = []
    for p in pieces_list:
        w_cut = p['cut_w']
        h_cut = p['cut_h']
        for _ in range(p['qty']):
            expanded.append((w_cut, h_cut, p))

    expanded.sort(key=lambda x: (x[0] * x[1], max(x[0], x[1])), reverse=True)

    class JumboSheet:
        def __init__(self, w, h):
            self.w = w
            self.h = h
            self.free_rects = [(margin, margin, w - 2 * margin, h - 2 * margin)]

        def place(self, pw, ph):
            best_rect_idx = -1
            best_orient = None
            best_short_side = float('inf')

            for r_idx, (rx, ry, rw, rh) in enumerate(self.free_rects):
                if pw <= rw and ph <= rh:
                    min_rem = min(rw - pw, rh - ph)
                    if min_rem < best_short_side:
                        best_short_side = min_rem
                        best_rect_idx = r_idx
                        best_orient = (pw, ph)

                if ph <= rw and pw <= rh:
                    min_rem = min(rw - ph, rh - pw)
                    if min_rem < best_short_side:
                        best_short_side = min_rem
                        best_rect_idx = r_idx
                        best_orient = (ph, pw)

            if best_rect_idx == -1:
                return False

            rx, ry, rw, rh = self.free_rects.pop(best_rect_idx)
            w_placed, h_placed = best_orient

            right_w = rw - w_placed - kerf
            right_h = h_placed
            top_w = rw
            top_h = rh - h_placed - kerf

            if right_w > 0 and right_h > 0:
                self.free_rects.append((rx + w_placed + kerf, ry, right_w, right_h))
            if top_w > 0 and top_h > 0:
                self.free_rects.append((rx, ry + h_placed + kerf, top_w, top_h))

            return True

    sheets = []
    for pw, ph, _ in expanded:
        placed = False
        for sheet in sheets:
            if sheet.place(pw, ph):
                placed = True
                break
        if not placed:
            new_sheet = JumboSheet(sheet_w, sheet_h)
            new_sheet.place(pw, ph)
            sheets.append(new_sheet)

    total_net_area = sum(pw * ph for pw, ph, _ in expanded) / 1e6
    total_jumbo_area = len(sheets) * (sheet_w * sheet_h / 1e6)
    opt_waste_pct = max(0.0,
                        ((total_jumbo_area - total_net_area) / total_jumbo_area * 100)) if total_jumbo_area > 0 else 0.0

    return len(sheets), opt_waste_pct, total_jumbo_area, total_net_area


# PDF GENERATION FUNCTION (REPORTLAB)
def generate_pdf_report(proj_name, sheet_label, sw, sh, sheets_cnt, net_m2, jumbo_m2, waste_p, grand_total, opt_rows):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []

    title_style = ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, leading=22,
                                 textColor=colors.HexColor('#003366'))
    story.append(Paragraph(f"<b>PSG PRICE - Cutting & Optimization Report</b>", title_style))
    story.append(Spacer(1, 10))

    sub_style = ParagraphStyle(name='SubStyle', fontName='Helvetica', fontSize=11, leading=14,
                               textColor=colors.HexColor('#333333'))
    story.append(Paragraph(f"Project: <b>{proj_name}</b> | Selected Stock Sheet: <b>{sheet_label}</b>", sub_style))
    story.append(Spacer(1, 15))

    summary_data = [
        ['Stock Sheet Dimension', f"{sheet_label}"],
        ['Sheets Required', f"{sheets_cnt} pcs ({jumbo_m2:.2f} m2)"],
        ['Net Glass Area', f"{net_m2:.2f} m2"],
        ['Real Nesting Waste %', f"{waste_p:.2f} %"],
        ['Total Estimated Sale Price', f"{grand_total:.2f} €"]
    ]
    t = Table(summary_data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111111')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc'))
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Vector Diagram
    draw_w = 500
    scale = draw_w / sw
    draw_h = sh * scale

    d = Drawing(draw_w, draw_h)
    d.add(Rect(0, 0, draw_w, draw_h, fillColor=colors.HexColor('#e6f2ff'), strokeColor=colors.HexColor('#003366'),
               strokeWidth=1.5))

    cur_x, cur_y, max_h = 10, 10, 0
    for idx, p in enumerate(opt_rows):
        pw, ph, qty = p['cut_w'], p['cut_h'], p['qty']
        for q in range(qty):
            if cur_x + pw > sw:
                cur_x = 10
                cur_y += max_h + 10
                max_h = 0
            if cur_y + ph <= sh:
                rx = cur_x * scale
                ry = (sh - (cur_y + ph)) * scale
                rw = pw * scale
                rh = ph * scale

                d.add(Rect(rx, ry, rw, rh, fillColor=colors.HexColor('#b8daff'), strokeColor=colors.HexColor('#004085'),
                           strokeWidth=0.8))
                d.add(String(rx + rw / 2, ry + rh / 2 - 3, f"P{idx + 1} ({pw:.0f}x{ph:.0f})", textAnchor='middle',
                             fontName='Helvetica', fontSize=6, fillColor=colors.HexColor('#002752')))

                cur_x += pw + 10
                max_h = max(max_h, ph)

    story.append(d)
    doc.build(story)
    buffer.seek(0)
    return buffer


# ==========================================
# TAB 1: CALUMEN RECIPE BUILDER
# ==========================================
with tab1:
    st.header("🔬 Δημιουργία Συνταγής Υαλοστάσιου (Calumen Style)")
    glazing_type = st.radio("Τύπος Υαλοστάσιου:", ["Μονό Γυαλί", "Διπλό Υαλοστάσιο", "Τριπλό Υαλοστάσιο"],
                            horizontal=True)

    col_b1, col_b2, col_b3 = st.columns(3)

    recipe_layers = []
    total_thick = 0.0
    raw_glass_cost_m2 = 0.0
    processing_cost_m2 = 0.0
    has_any_rode = False

    # --- ΓΥΑΛΙ 1 ---
    with col_b1:
        st.subheader("🔵 Εξωτερικός Υαλοπίνακας (Γ1)")
        is_lami_1 = st.checkbox("Είναι Laminated / Συγκολλημένο;", key="l1")

        if not is_lami_1:
            g1_mat = st.selectbox("Επιλογή Γυαλιού 1:", list(st.session_state.GLASS_CATALOG.keys()), key="g1_s")
            g1_info = st.session_state.GLASS_CATALOG[g1_mat]
            g1_proc_cost, sec1, rode1, xil1, holes1 = render_glass_processing_options("g1", g1_info)
            if rode1 or sec1:
                has_any_rode = True

            kopi_type = g1_info.get("kopi", "ΜΟΝΗ")
            kopi_cost = 3.0 if kopi_type == "3€/m2" else (4.0 if kopi_type == "4€/m2" else 1.0)

            tag = f"{g1_mat}" + (" (Security)" if sec1 else "") + (" (Rode)" if rode1 else "")
            recipe_layers.append(tag)
            total_thick += g1_info["thick"]
            raw_glass_cost_m2 += g1_info["price"]
            processing_cost_m2 += g1_proc_cost + kopi_cost
        else:
            g1_a = st.selectbox("Φύλλο A:", list(st.session_state.GLASS_CATALOG.keys()), key="g1_a")
            c_g1a, sec1a, rode1a, _, _ = render_glass_processing_options("g1a", st.session_state.GLASS_CATALOG[g1_a])
            pvb_1 = st.selectbox("Μεμβράνη PVB:", list(st.session_state.PVB_EXTRAS.keys()), key="pvb1")
            g1_b = st.selectbox("Φύλλο B:", list(st.session_state.GLASS_CATALOG.keys()), key="g1_b")
            c_g1b, sec1b, rode1b, _, _ = render_glass_processing_options("g1b", st.session_state.GLASS_CATALOG[g1_b])

            if rode1a or sec1a or rode1b or sec1b:
                has_any_rode = True

            recipe_layers.extend([g1_a, pvb_1, g1_b])
            t1 = st.session_state.GLASS_CATALOG[g1_a]["thick"] + st.session_state.PVB_EXTRAS[pvb_1]["thick"] + \
                 st.session_state.GLASS_CATALOG[g1_b]["thick"]
            total_thick += t1
            raw_glass_cost_m2 += st.session_state.GLASS_CATALOG[g1_a]["price"] + st.session_state.PVB_EXTRAS[pvb_1][
                "price"] + st.session_state.GLASS_CATALOG[g1_b]["price"]
            processing_cost_m2 += c_g1a + c_g1b + 7.0

    # --- ΔΙΑΚΕΝΟ 1 & ΓΥΑΛΙ 2 ---
    if glazing_type in ["Διπλό Υαλοστάσιο", "Τριπλό Υαλοστάσιο"]:
        with col_b2:
            st.subheader("🟡 Διάκενο 1 & Γυαλί 2")
            sp1 = st.selectbox("Επιλογή Διάκενου 1:", list(st.session_state.SPACERS_CATALOG.keys()), key="sp1")
            recipe_layers.append(sp1)
            total_thick += st.session_state.SPACERS_CATALOG[sp1]["thick"]
            processing_cost_m2 += st.session_state.SPACERS_CATALOG[sp1]["price"]

            st.divider()
            is_lami_2 = st.checkbox("Το Γυαλί 2 είναι Laminated;", key="l2")
            if not is_lami_2:
                g2_mat = st.selectbox("Επιλογή Γυαλιού 2:", list(st.session_state.GLASS_CATALOG.keys()), key="g2_s")
                g2_info = st.session_state.GLASS_CATALOG[g2_mat]
                g2_proc_cost, sec2, rode2, xil2, holes2 = render_glass_processing_options("g2", g2_info)
                if rode2 or sec2:
                    has_any_rode = True

                kopi_type2 = g2_info.get("kopi", "ΜΟΝΗ")
                kopi_cost2 = 3.0 if kopi_type2 == "3€/m2" else (4.0 if kopi_type2 == "4€/m2" else 1.0)

                tag = f"{g2_mat}" + (" (Security)" if sec2 else "") + (" (Rode)" if rode2 else "")
                recipe_layers.append(tag)
                total_thick += g2_info["thick"]
                raw_glass_cost_m2 += g2_info["price"]
                processing_cost_m2 += g2_proc_cost + kopi_cost2
            else:
                g2_a = st.selectbox("Φύλλο A (Γ2):", list(st.session_state.GLASS_CATALOG.keys()), key="g2_a")
                c_g2a, sec2a, rode2a, _, _ = render_glass_processing_options("g2a",
                                                                             st.session_state.GLASS_CATALOG[g2_a])
                pvb_2 = st.selectbox("Μεμβράνη PVB (Γ2):", list(st.session_state.PVB_EXTRAS.keys()), key="pvb2")
                g2_b = st.selectbox("Φύλλο B (Γ2):", list(st.session_state.GLASS_CATALOG.keys()), key="g2_b")
                c_g2b, sec2b, rode2b, _, _ = render_glass_processing_options("g2b",
                                                                             st.session_state.GLASS_CATALOG[g2_b])

                if rode2a or sec2a or rode2b or sec2b:
                    has_any_rode = True

                recipe_layers.extend([g2_a, pvb_2, g2_b])
                t2 = st.session_state.GLASS_CATALOG[g2_a]["thick"] + st.session_state.PVB_EXTRAS[pvb_2]["thick"] + \
                     st.session_state.GLASS_CATALOG[g2_b]["thick"]
                total_thick += t2
                raw_glass_cost_m2 += st.session_state.GLASS_CATALOG[g2_a]["price"] + st.session_state.PVB_EXTRAS[pvb_2][
                    "price"] + st.session_state.GLASS_CATALOG[g2_b]["price"]
                processing_cost_m2 += c_g2a + c_g2b + 7.0

    # --- ΔΙΑΚΕΝΟ 2 & ΓΥΑΛΙ 3 (ΤΡΙΠΛΟ) ---
    if glazing_type == "Τριπλό Υαλοστάσιο":
        with col_b3:
            st.subheader("🔴 Διάκενο 2 & Γυαλί 3")
            sp2 = st.selectbox("Επιλογή Διάκενου 2:", list(st.session_state.SPACERS_CATALOG.keys()), key="sp2")
            recipe_layers.append(sp2)
            total_thick += st.session_state.SPACERS_CATALOG[sp2]["thick"]
            processing_cost_m2 += st.session_state.SPACERS_CATALOG[sp2]["price"]

            st.divider()
            g3_mat = st.selectbox("Επιλογή Γυαλιού 3:", list(st.session_state.GLASS_CATALOG.keys()), key="g3_s")
            g3_info = st.session_state.GLASS_CATALOG[g3_mat]
            g3_proc_cost, sec3, rode3, xil3, holes3 = render_glass_processing_options("g3", g3_info)
            if rode3 or sec3:
                has_any_rode = True

            kopi_type3 = g3_info.get("kopi", "ΜΟΝΗ")
            kopi_cost3 = 3.0 if kopi_type3 == "3€/m2" else (4.0 if kopi_type3 == "4€/m2" else 1.0)

            tag = f"{g3_mat}" + (" (Security)" if sec3 else "") + (" (Rode)" if rode3 else "")
            recipe_layers.append(tag)
            total_thick += g3_info["thick"]
            raw_glass_cost_m2 += g3_info["price"]
            processing_cost_m2 += g3_proc_cost + kopi_cost3

    st.divider()
    include_pack_trans = st.checkbox("🚚 Προσθήκη Συσκευασίας & Μεταφοράς (+€3.50 / m²)", value=False, key="recipe_pt")
    pack_trans_cost = 3.50 if include_pack_trans else 0.0

    # --- ΥΠΟΛΟΓΙΣΜΟΣ ΜΕ ΤΑ ΝΕΑ MARKUPS (41.67% ΓΒΕ & 17.65% ΚΕΡΔΟΣ) ---
    glass_cost_with_waste = raw_glass_cost_m2 * (1 + waste_pct)
    direct_cost_m2_cat1 = glass_cost_with_waste + processing_cost_m2 + pack_trans_cost
    est_sale_price_m2 = direct_cost_m2_cat1 * (1 + gbe_pct) * (1 + profit_pct)

    st.subheader("🖼️ Επισκόπηση Σύνθεσης & Τιμολόγηση")
    st.info(f"**Δομή:** {' ➔ '.join(recipe_layers)}")
    if has_any_rode:
        st.warning(
            "⚠️ Η σύνθεση περιέχει Ροντέ. Στην 3η σελίδα προστίθενται αυτόματα +2mm σε κάθε πλευρά (+4mm W / +4mm H) για την κοπή.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Συνολικό Πάχος", f"{total_thick:.2f} mm")
    m2.metric("Άμεσο Κόστος / m² (Cat 1)", f"{direct_cost_m2_cat1:.2f} €/m²")
    m3.metric("🎯 Επιθυμητή Τιμή Πώλησης (Cat 1)", f"{est_sale_price_m2:.2f} €/m²")

    recipe_name = st.text_input("Όνομα Συνταγής για Αποθήκευση στη Βιβλιοθήκη:",
                                value=f"{glazing_type} ({total_thick:.1f}mm)")

    if st.button("💾 Αποθήκευση Συνταγής στη Βιβλιοθήκη"):
        st.session_state.RECIPES[recipe_name] = {
            "type": glazing_type,
            "layers": recipe_layers,
            "total_thick": round(total_thick, 2),
            "raw_glass_cost_m2": round(raw_glass_cost_m2, 2),
            "processing_cost_m2": round(processing_cost_m2, 2),
            "has_rode": has_any_rode,
            "pack_trans": include_pack_trans
        }
        st.success(f"Η συνταγή '{recipe_name}' αποθηκεύτηκε επιτυχώς στη Βιβλιοθήκη!")

# ==========================================
# TAB 2: ΒΙΒΛΙΟΘΗΚΗ
# ==========================================
with tab2:
    st.header("📚 Αποθηκευμένες Συνταγές Calumen")
    recipe_data = []
    for r_name, r_info in st.session_state.RECIPES.items():
        pt_cost = 3.50 if r_info.get("pack_trans", False) else 0.0
        r_raw = r_info.get("raw_glass_cost_m2", r_info.get("base_cost_m2", 0.0))
        r_proc = r_info.get("processing_cost_m2", 0.0)
        dir_c = (r_raw * (1 + waste_pct)) + r_proc + pt_cost
        r_sale = dir_c * (1 + gbe_pct) * (1 + profit_pct)
        recipe_data.append({
            "Όνομα Συνταγής": r_name,
            "Τύπος": r_info["type"],
            "Σύνθεση": " | ".join(r_info["layers"]),
            "Πάχος (mm)": r_info["total_thick"],
            "Προσαυξητικό Ροντέ (+2mm/πλευρά)": "Ναι (+4mm W/H)" if r_info.get("has_rode", False) else "Όχι",
            "Συσκευασία/Μεταφορά": "Ναι" if r_info.get("pack_trans", False) else "Όχι",
            "Άμεσο Κόστος / m² (€)": round(dir_c, 2),
            "Τιμή Πώλησης / m² (Cat 1) (€)": round(r_sale, 2)
        })
    st.dataframe(pd.DataFrame(recipe_data), use_container_width=True)

# ==========================================
# TAB 3: ΚΟΣΤΟΛΟΓΗΣΗ ΠΑΡΑΓΓΕΛΙΑΣ, NESTING & PDF EXTRACT
# ==========================================
with tab3:
    st.header("📊 Ακριβής Κοστολόγηση Παραγγελίας, Precision Nesting & PDF Report")

    stock_sheet_options = {
        "6.000 x 3.210 mm (Jumbo - Προεπιλογή)": (6000.0, 3210.0),
        "3.210 x 2.550 mm": (3210.0, 2550.0),
        "3.210 x 2.225 mm": (3210.0, 2225.0),
        "3.010 x 5.100 mm": (3010.0, 5100.0),
    }

    selected_sheet_label = st.selectbox(
        "📐 Επιλέξτε Διάσταση Αρχικού Φύλλου Κοπής (Stock Sheet):",
        list(stock_sheet_options.keys())
    )
    sheet_w, sheet_h = stock_sheet_options[selected_sheet_label]

    st.caption(
        "Εισάγετε διαστάσεις παραγγελίας. Το σύστημα προσθέτει +2mm/πλευρά αν υπάρχει Ροντέ, υπολογίζει τη φύρα στο επιλεγμένο φύλλο και παράγει PDF αναφορά.")

    default_order = [{
        'Συνταγή Calumen': list(st.session_state.RECIPES.keys())[0],
        'Πλάτος (mm)': 1500, 'Ύψος (mm)': 2000, 'Τεμάχια': 1,
        'Φύρα (%)': round(waste_pct * 100, 1)
    }]
    order_df = pd.DataFrame(default_order)

    column_config_order = {
        "Συνταγή Calumen": st.column_config.SelectboxColumn("Επιλογή Συνταγής",
                                                            options=list(st.session_state.RECIPES.keys())),
    }
    edited_order = st.data_editor(order_df, num_rows="dynamic", use_container_width=True,
                                  column_config=column_config_order)

    if not edited_order.empty:
        processed_pieces_for_opt = []
        res_rows = []

        for idx, row in edited_order.iterrows():
            rec_name = str(row.get('Συνταγή Calumen', ''))
            w_raw = pd.to_numeric(row.get('Πλάτος (mm)'), errors='coerce') or 0.0
            h_raw = pd.to_numeric(row.get('Ύψος (mm)'), errors='coerce') or 0.0
            qty = int(pd.to_numeric(row.get('Τεμάχια'), errors='coerce') or 0)
            user_w_pct = (pd.to_numeric(row.get('Φύρα (%)'), errors='coerce') or 0.0) / 100

            if rec_name in st.session_state.RECIPES and w_raw > 0 and h_raw > 0 and qty > 0:
                rec = st.session_state.RECIPES[rec_name]
                is_rode = rec.get("has_rode", False)

                w_cut = w_raw + 4.0 if is_rode else w_raw
                h_cut = h_raw + 4.0 if is_rode else h_raw
                area_cut_m2 = (w_cut / 1000.0) * (h_cut / 1000.0)

                if w_cut > 2800 and h_cut > 2800:
                    cat = 3
                    cat_mult = 1.35
                    pt_cost = 4.50
                elif area_cut_m2 > 3.75:
                    cat = 2
                    cat_mult = 1.15
                    pt_cost = 3.50
                else:
                    cat = 1
                    cat_mult = 1.00
                    pt_cost = 3.50

                pack_trans_cost = pt_cost if rec.get("pack_trans", False) else 0.0

                r_raw = rec.get("raw_glass_cost_m2", rec.get("base_cost_m2", 0.0))
                r_proc = rec.get("processing_cost_m2", 0.0)

                dir_cost_m2 = ((r_raw * (1 + user_w_pct)) + r_proc + pack_trans_cost) * cat_mult
                sale_price_m2_std = dir_cost_m2 * (1 + gbe_pct) * (1 + profit_pct)
                total_m2_row = area_cut_m2 * qty
                total_sale_std = sale_price_m2_std * total_m2_row

                processed_pieces_for_opt.append({
                    'rec_name': rec_name,
                    'cut_w': w_cut,
                    'cut_h': h_cut,
                    'qty': qty,
                    'area_m2': area_cut_m2,
                    'raw_glass_cost_m2': r_raw,
                    'processing_cost_m2': r_proc,
                    'cat_mult': cat_mult,
                    'pack_trans_cost': pack_trans_cost
                })

                res_rows.append({
                    'Συνταγή': rec_name,
                    'Διαστάσεις (mm)': f"{w_raw:.0f} x {h_raw:.0f}",
                    'Διαστάσεις Κοπής (+2mm/πλευρά)': f"{w_cut:.0f} x {h_cut:.0f}" if is_rode else f"{w_raw:.0f} x {h_raw:.0f}",
                    'Τεμάχια': qty,
                    'm² / Τεμ': round(area_cut_m2, 3),
                    'Κατηγορία': f"Cat {cat}",
                    'Σύνολο m²': round(total_m2_row, 2),
                    'Τιμή / m² (Αρχική €)': round(sale_price_m2_std, 2),
                    'Σύνολο (€ - Αρχικό)': round(total_sale_std, 2)
                })

        if res_rows:
            full_res_df = pd.DataFrame(res_rows)
            st.subheader("📊 Αποτελέσματα Αρχικής Κοστολόγησης (με Εκτιμώμενη Φύρα)")
            st.dataframe(full_res_df, use_container_width=True)

            # --- RUN PRECISION GUILLOTINE NESTING ENGINE ON SELECTED SHEET ---
            sheets_used, opt_waste_pct, total_jumbo_m2, net_used_m2 = run_guillotine_nesting_optimisation(
                processed_pieces_for_opt, sheet_w, sheet_h)

            st.divider()
            st.subheader(f"🧩 Αποτελέσματα Guillotine Nesting ({selected_sheet_label})")

            col_o1, col_o2, col_o3, col_o4 = st.columns(4)
            col_o1.metric("Απαιτούμενα Φύλλα", f"{sheets_used} τεμ ({total_jumbo_m2:.2f} m²)")
            col_o2.metric("Καθαρά m² Γυαλιού", f"{net_used_m2:.2f} m²")
            col_o3.metric("🔥 Πραγματική Φύρα Nesting", f"{opt_waste_pct:.2f} %")

            opt_res_rows = []
            grand_total_opt_sale = 0.0

            for p in processed_pieces_for_opt:
                dir_cost_m2_opt = ((p['raw_glass_cost_m2'] * (1 + (opt_waste_pct / 100))) + p['processing_cost_m2'] + p[
                    'pack_trans_cost']) * p['cat_mult']
                sale_price_m2_opt = dir_cost_m2_opt * (1 + gbe_pct) * (1 + profit_pct)
                row_total_opt = sale_price_m2_opt * (p['area_m2'] * p['qty'])
                grand_total_opt_sale += row_total_opt

                opt_res_rows.append({
                    'Συνταγή': p['rec_name'],
                    'Διαστάσεις Κοπής (mm)': f"{p['cut_w']:.0f} x {p['cut_h']:.0f}",
                    'Τεμάχια': p['qty'],
                    'Πραγματικό Ποσοστό Φύρας Nesting (%)': f"{opt_waste_pct:.2f}%",
                    'Βελτιστοποιημένη Τιμή / m² (€)': round(sale_price_m2_opt, 2),
                    'Τελικό Σύνολο με Nesting (€)': round(row_total_opt, 2)
                })

            col_o4.metric("🎯 Τελική Τιμή Προσφοράς", f"{grand_total_opt_sale:.2f} €")

            st.info(
                f"💡 **Ακρίβεια Nesting:** Για την κάλυψη **{net_used_m2:.2f} m²** καθαρού γυαλιού στο φύλλο **{selected_sheet_label}**, απαιτούνται **{sheets_used} φύλλα**, παράγοντας **ακριβή φύρα {opt_waste_pct:.2f}%**.")

            st.subheader("📋 Αναλυτικός Πίνακας Προσφοράς με Nesting")
            st.dataframe(pd.DataFrame(opt_res_rows), use_container_width=True)

            # --- DYNAMIC PDF REPORT DOWNLOAD BUTTON ---
            st.divider()
            if REPORTLAB_AVAILABLE:
                pdf_data = generate_pdf_report(
                    proj_name=project_name,
                    sheet_label=selected_sheet_label,
                    sw=sheet_w,
                    sh=sheet_h,
                    sheets_cnt=sheets_used,
                    net_m2=net_used_m2,
                    jumbo_m2=total_jumbo_m2,
                    waste_p=opt_waste_pct,
                    grand_total=grand_total_opt_sale,
                    opt_rows=processed_pieces_for_opt
                )

                st.download_button(
                    label="📥 Κατέβασμα PDF Αναφοράς & Διαγράμματος Κοπής",
                    data=pdf_data,
                    file_name=f"PSG_PRICE_Report_{project_name}.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning(
                    "⚠️ Για την παραγωγή του αρχείου PDF απαιτείται η βιβλιοθήκη `reportlab`. Παρακαλώ τρέξτε `pip install reportlab` στο Terminal του PyCharm.")

            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    if st.button("📝 Δημιουργία Επαγγελματικής Προσφοράς με AI"):
                        prompt = f"Συνέταξε προσφορά για: {opt_res_rows} (Project: {project_name}, Φύλλο: {selected_sheet_label}, Φύρα: {opt_waste_pct:.2f}%)"
                        res = model.generate_content(prompt)
                        st.write(res.text)
                except Exception as e:
                    st.error(f"Σφάλμα AI: {e}")