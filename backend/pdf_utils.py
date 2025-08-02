from fpdf import FPDF
import os

def save_case_pdf(case_data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Delhi High Court Case Details", ln=True, align="C")
    pdf.ln(10)  # Add vertical space

    for key, value in case_data.items():
        if isinstance(value, list):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt=f"{key}:", ln=True)
            pdf.set_font("Arial", size=12)
            for item in value:
                pdf.multi_cell(0, 10, txt=f"• {item}")
        else:
            pdf.multi_cell(0, 10, txt=f"{key}: {value}")

        pdf.ln(5)

    # Ensure pdf folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)
