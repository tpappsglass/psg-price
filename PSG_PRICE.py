import streamlit as st
import pandas as pd
import numpy as np
import math
import io

# ReportLab Imports for PDF Generation
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
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
    "argon": 1.50,
    "packing_transport": 3.50
}

STOCK_SHEETS = {
    "6.000 x 3.210 mm (Jumbo - Προεπιλογή)": (6000, 3210),
    "3.210 x 2.250 mm (Standard)": (3210, 2250),
    "2.550 x 1.605 mm (Half Sheet)": (2550, 1605)
}

# ---------------------------------------------------------
# SIDEBAR: DYNAMIC FISCAL INPUTS
# ---------------------------------------------------------
st.sidebar.header("📋 Διαχείριση Παραγγελίας")
customer_name = st.sidebar.text_input("Όνομα Project / Πελάτη", "")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Δυναμικές Ρυθμίσεις Κοστολόγησης")

gbe_pct = st.sidebar.number_input("Γ.Β.Ε. / Έξοδα (%)", min_value=0.0, max_value=80.0, value=45.0, step=0.5)
profit_pct = st.sidebar.number_input("Καθαρό Κέρδος (%)", min_value=0.0, max_value=80.0, value=20.0, step=0.5)

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

def calculate_single_glass_cost(g_main, g_extra, is_lami, pvb_type, is_temp, is_rode):
    cost = 0.0
    if g_main in GLASS_DB:
        cost += GLASS_DB[g_main]["cost"]
    if is_lami:
        cost += PROCESSING_COSTS["lami_processing"]
        if g_extra in GLASS_DB:
            cost += GLASS_DB[g_extra]["cost"]
        if pvb_type in PVB_DB:
            cost += PVB_DB[pvb_type]
    if is_temp:
        cost += PROCESSING_COSTS["tempering"]
    return cost

def run_nesting_optimization(items, stock_w, stock_h):
    stock_area = (stock_w / 1000.0) * (stock_h / 1000.0)
    total_used_area = 0.0
    for item in items:
        w, h, qty = item['w'], item['h'], item['qty']
        piece_area = (w / 1000.0) * (h / 1000.0)
        total_used_area += piece_area * qty

    sheets_needed = max(1, math.ceil(total_used_area / (stock_area * 0.85)))
    total_stock_area = sheets_needed * stock_area
    waste_percentage = max(0.0, ((total_stock_area - total_used_area) / total_stock_area) * 100.0)

    return sheets_needed, round(waste_percentage, 1), round(total_used_area, 2)

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

def generate_pdf_nesting_report(customer_name, df_items, stock_w, stock_h, sheets_needed, waste_pct, total_m2):
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

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer

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
    with col1:
        st.subheader("🔵 Εξωτερικός Υαλοπίνακας (Γ1)")
        g1_main = st.selectbox("Επιλογή Βασικού Γυαλιού 1", list(GLASS_DB.keys()), key="g1_main")
        p1_lami = st.checkbox("Είναι Laminated / Συγκολλημένος", key="p1_lami")
        
        g1_extra = None
        pvb1_type = None
        if p1_lami:
            st.markdown("**Σύνθεση Triplex / Laminated (Γ1):**")
            g1_extra = st.selectbox("Επιλογή 2ου Γυαλιού (Γ1)", list(GLASS_DB.keys()), key="g1_extra")
            pvb1_type = st.selectbox("Επιλογή Μεμβράνης PVB (Γ1)", list(PVB_DB.keys()), key="pvb1_type")
            
        p1_temp = st.checkbox("Security / Tempered", key="p1_temp")
        p1_rode = st.checkbox("Ροντέ / Τρόχισμα", key="p1_rode")

    # GLASS 2 CONFIG
    g2_main, g2_extra, pvb2_type, p2_temp, p2_rode = None, None, None, False, False
    if is_double:
        with col2:
            st.subheader("🟢 Μεσαίος / Εσωτερικός (Γ2)")
            g2_main = st.selectbox("Επιλογή Βασικού Γυαλιού 2", list(GLASS_DB.keys()), key="g2_main")
            p2_lami = st.checkbox("Είναι Laminated / Συγκολλημένος ", key="p2_lami")
            if p2_lami:
                st.markdown("**Σύνθεση Triplex / Laminated (Γ2):**")
                g2_extra = st.selectbox("Επιλογή 2ου Γυαλιού (Γ2)", list(GLASS_DB.keys()), key="g2_extra")
                pvb2_type = st.selectbox("Επιλογή Μεμβράνης PVB (Γ2)", list(PVB_DB.keys()), key="pvb2_type")
            p2_temp = st.checkbox("Security / Tempered ", key="p2_temp")
            p2_rode = st.checkbox("Ροντέ / Τρόχισμα ", key="p2_rode")

    # GLASS 3 CONFIG
    g3_main, g3_extra, pvb3_type, p3_temp, p3_rode = None, None, None, False, False
    if is_triple:
        with col3:
            st.subheader("🔴 Εσωτερικός (Γ3)")
            g3_main = st.selectbox("Επιλογή Βασικού Γυαλιού 3", list(GLASS_DB.keys()), key="g3_main")
            p3_lami = st.checkbox("Είναι Laminated / Συγκολλημένος  ", key="p3_lami")
            if p3_lami:
                st.markdown("**Σύνθεση Triplex / Laminated (Γ3):**")
                g3_extra = st.selectbox("Επιλογή 2ου Γυαλιού (Γ3)", list(GLASS_DB.keys()), key="g3_extra")
                pvb3_type = st.selectbox("Επιλογή Μεμβράνης PVB (Γ3)", list(PVB_DB.keys()), key="pvb3_type")
            p3_temp = st.checkbox("Security / Tempered  ", key="p3_temp")
            p3_rode = st.checkbox("Ροντέ / Τρόχισμα  ", key="p3_rode")

    # SPACER & AIR GAP CONFIG (FOR DOUBLE/TRIPLE)
    spacer_cost = 0.0
    spacer_desc = ""
    if is_double:
        st.markdown("---")
        st.subheader("🔲 Ρυθμίσεις Διάκενου / Αποστάτη (Spacer)")
        col_sp1, col_sp2, col_sp3 = st.columns(3)
        with col_sp1:
            spacer_mat = st.selectbox("Υλικό Διάκενου", ["Technoform Warm Edge", "Aluminium"], key="sp_mat")
        with col_sp2:
            spacer_size = st.selectbox("Πάχος Διάκενου (mm)", [10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32], index=4, key="sp_size")
        with col_sp3:
            add_argon = st.checkbox("Πλήρωση Αερίου Argon (+€1.50/m²)", value=True, key="add_argon")

        sp_key = f"{'Technoform' if 'Technoform' in spacer_mat else 'Aluminium'} {'< 18mm' if spacer_size < 18 else '> 18mm'}"
        spacer_cost = SPACER_PRICES.get(sp_key, 10.00)
        if is_triple: spacer_cost *= 2
        if add_argon: spacer_cost += (PROCESSING_COSTS["argon"] * (2 if is_triple else 1))

        spacer_desc = f" / {spacer_size}mm {spacer_mat}" + (" + Argon" if add_argon else "")

    st.markdown("---")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        add_pack = st.checkbox("Προσθήκη Συσκευασίας & Μεταφοράς (+€3.50 / m²)", value=True)
    with col_opt2:
        waste_pct_est = st.number_input("⚠️ Εκτιμώμενη Φθορά Υλικού (%) [Προαιρετικά]", min_value=0.0, max_value=50.0, value=0.0, step=1.0)

    # CALCULATE TOTAL DIRECT COST
    c1 = calculate_single_glass_cost(g1_main, g1_extra, p1_lami, pvb1_type, p1_temp, p1_rode)
    c2 = calculate_single_glass_cost(g2_main, g2_extra, 'p2_lami' in locals() and p2_lami, pvb2_type, p2_temp, p2_rode) if is_double else 0.0
    c3 = calculate_single_glass_cost(g3_main, g3_extra, 'p3_lami' in locals() and p3_lami, pvb3_type, p3_temp, p3_rode) if is_triple else 0.0

    direct_cost = c1 + c2 + c3 + spacer_cost
    if add_pack: direct_cost += PROCESSING_COSTS["packing_transport"]
    if waste_pct_est > 0: direct_cost *= (1.0 + (waste_pct_est / 100.0))

    cost_with_gbe = direct_cost + (direct_cost * gbe_markup)
    final_price_m2 = cost_with_gbe + (cost_with_gbe * profit_markup)

    # FORMULATE RECIPE NAME
    name1 = f"{g1_main}{'+' + g1_extra if p1_lami else ''}"
    full_recipe_name = name1
    if is_double:
        name2 = f"{g2_main}{'+' + g2_extra if 'p2_lami' in locals() and p2_lami else ''}"
        full_recipe_name += f"{spacer_desc} / {name2}"
    if is_triple:
        name3 = f"{g3_main}{'+' + g3_extra if 'p3_lami' in locals() and p3_lami else ''}"
        full_recipe_name += f" / {name3}"
    if p1_temp or p2_temp or p3_temp:
        full_recipe_name += " Tempered [HST]"

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
# TAB 3: OFFER GENERATION, NESTING & AUTOMATIC CLEAN DESCRIPTIONS
# ---------------------------------------------------------
with tab3:
    st.header("📊 Ακριβής Κοστολόγηση Παραγωγής, Nesting & PDF Προσφορά")
    
    selected_sheet_label = st.selectbox("📐 Επιλέξτε Διάσταση Αρχικού Φύλλου Κοπής (Stock Sheet):", list(STOCK_SHEETS.keys()))
    stock_w, stock_h = STOCK_SHEETS[selected_sheet_label]

    available_recipes = list(st.session_state.recipes.keys()) if st.session_state.recipes else ["CLIMAX SELECT 33.1 / 16mm Technoform Warm Edge + Argon / CLEAR FLOAT GLASS 4 mm Tempered [HST]"]
    
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
        sheets_needed, waste_pct, total_m2 = run_nesting_optimization(nesting_items, stock_w, stock_h)

        st.subheader("📋 Επισκόπηση Υπολογισμών Παραγγελίας & Nesting Report")
        col_n1, col_n2, col_n3 = st.columns(3)
        col_n1.metric("Συνολικά Πραγματικά Καθαρά m²", f"{total_m2:.2f} m²")
        col_n2.metric("Φύλλα Κοπής (Stock Sheets)", f"{sheets_needed} τεμ")
        col_n3.metric("Πραγματική Φύρα Κοπής (Waste)", f"{waste_pct}%")

        st.dataframe(df_processed, use_container_width=True)

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
        pdf_nesting = generate_pdf_nesting_report(customer_name, df_processed, stock_w, stock_h, sheets_needed, waste_pct, total_m2)

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
                label="✂️ Λήψη Αναφοράς Κοπών & Nesting σε PDF",
                data=pdf_nesting,
                file_name=f"PSG_Nesting_Report_{file_cust_name}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
