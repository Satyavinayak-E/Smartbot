import matplotlib.pyplot as plt
from fpdf import FPDF
import analytics

def create_report():
    data = analytics.get_analytics()

    # === Generate Bar Chart ===
    plt.figure(figsize=(6, 4))
    plt.bar(['Total', 'Success', 'Failure'], [data['total'], data['success'], data['failure']],
            color=['#007bff', '#28a745', '#dc3545'])
    plt.title('Search Analytics - Bar Chart')
    plt.xlabel('Query Type')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
    bar_path = 'static/reports/bar_chart.png'
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()

    # === Generate Pie Chart ===
    plt.figure(figsize=(5, 5))
    plt.pie([data['success'], data['failure']], labels=['Success', 'Failure'], autopct='%1.1f%%',
            colors=['#28a745', '#dc3545'], startangle=140)
    plt.title('Search Success vs Failure - Pie Chart')
    pie_path = 'static/reports/pie_chart.png'
    plt.tight_layout()
    plt.savefig(pie_path)
    plt.close()

    # === Generate PDF Report ===
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Search Analytics Report", ln=True, align='C')

    # Analytics Summary
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Total Queries: {data['total']}", ln=True)
    pdf.cell(0, 10, f"Successful Queries: {data['success']}", ln=True)
    pdf.cell(0, 10, f"Unsuccessful Queries: {data['failure']}", ln=True)

    # Add bar chart
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Bar Chart:", ln=True)
    pdf.image(bar_path, x=30, y=70, w=150)
    pdf.ln(90)

    # Add pie chart
    pdf.set_y(170)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Pie Chart:", ln=True)
    pdf.image(pie_path, x=50, y=180, w=100)

    # Save PDF
    pdf_path = 'static/reports/analytics_report.pdf'
    pdf.output(pdf_path)

    return pdf_path
