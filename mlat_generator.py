from fpdf import FPDF

def generate_mlat_pdf(case):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="MLAT REQUEST REPORT", ln=True, align='C')

    pdf.ln(10)

    for key, value in case.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    filename = f"MLAT_{case['complaint_id']}.pdf"
    pdf.output(filename)

    return filename
