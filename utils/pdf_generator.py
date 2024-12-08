from fpdf import FPDF

def create_pdf(data, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SMB Analysis Report", ln=True, align='C')

    # Target Website Analysis
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Target Website Analysis", ln=True)
    for key, value in data["Target Website Analysis"].items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Competitor Comparison
    pdf.cell(200, 10, txt="Competitor Comparison", ln=True)
    # Add competitor comparison table or chart here...

    # Social Media Analysis
    pdf.cell(200, 10, txt="Social Media Analysis", ln=True)
    for platform, metrics in data["Social Media Analysis"].items():
        pdf.cell(200, 10, txt=f"{platform}:", ln=True)
        for key, value in metrics.items():
            pdf.cell(200, 10, txt=f"    {key}: {value}", ln=True)

    pdf.output(filename)
    print(f"Report saved as {filename}")