import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_analysis_report(csv_path, output_pdf):
    # --- Step 1: Read and Analyze Data ---
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return
    
    total_sales = df['Sales'].sum()
    avg_sales = df['Sales'].mean()
    top_performer = df.loc[df['Sales'].idxmax(), 'Category']

    # --- Step 2: Generate PDF Report ---
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2.0, height-70, "Monthly Sales Analysis Report")

    # Executive Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-120, "Executive Summary")

    c.setFont("Helvetica", 12)
    c.drawString(50, height-145, f"Total Revenue: ${total_sales:,.2f}")
    c.drawString(50, height-165, f"Average Sale: ${avg_sales:,.2f}")
    c.drawString(50, height-185, f"Highest Performing Category: {top_performer}")

    # Table Header
    y_position = height-230
    c.setFont("Helvetica-Bold", 12)
    c.line(50, y_position+15, 550, y_position+15)
    c.drawString(50, y_position, "Category")
    c.drawString(250, y_position, "Sales Volume")
    c.line(50, y_position-5, 550, y_position-5)

    # Table Rows
    c.setFont("Helvetica", 11)
    y_position -= 30
    for _, row in df.iterrows():
        c.drawString(50, y_position, str(row['Category']))
        c.drawString(250, y_position, f"${row['Sales']:,.2f}")
        y_position -= 20

        # Page overflow check
        if y_position < 50:
            c.showPage()
            y_position = height-50

    # Finalize PDF
    c.save()
    print(f"Success! Report saved as {output_pdf}")

if __name__ == "__main__":
    pd.DataFrame({
        'Category': ['Electronics', 'Home Decor', 'Apparel', 'Books', 'Software'],
        'Sales': [45000, 12000, 28000, 5500, 31000]
    }).to_csv('data.csv', index=False)

    generate_analysis_report('data.csv', 'Sales_Report.pdf')
