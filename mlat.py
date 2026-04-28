from fpdf import FPDF

def generate_mlat(case):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "MLAT REQUEST REPORT", ln=True, align="C")
    pdf.ln(10)

    for k, v in case.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    filename = f"MLAT_{case.get('complaint_id', 'UNKNOWN')}.pdf"
    pdf.output(filename)

    return filename
