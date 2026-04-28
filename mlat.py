from fpdf import FPDF


def generate_mlat(case):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "MLAT REPORT", ln=True, align="C")
    pdf.ln(10)

    for k, v in case.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    file = f"MLAT_{case['complaint_id']}.pdf"
    pdf.output(file)

    return file
