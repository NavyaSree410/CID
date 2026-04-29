from fpdf import FPDF


def generate(case):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 12)

    pdf.cell(200, 10, "MLAT REPORT", ln=True)

    for k, v in case.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    file = f"{case['case_id']}.pdf"
    pdf.output(file)

    return file
