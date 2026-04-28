from fpdf import FPDF


def generate(case):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "MLAT REQUEST DOCUMENT", ln=True, align="C")
    pdf.ln(10)

    for k, v in case.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    file = f"MLAT_{case['case_id']}.pdf"
    pdf.output(file)

    return file
