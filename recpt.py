import os
import requests
from io import BytesIO
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.barcode import code128
from datetime import datetime

def download_logo(url="https://www.pngall.com/wp-content/uploads/5/Finance-Logo-PNG-Image.png", filename="logo.png"):
    """Download a finance-themed logo and save locally."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            img = PILImage.open(BytesIO(response.content))
            img.save(filename, "PNG")
            print(f"Logo downloaded and saved as {filename}")
            return filename
        else:
            print("Failed to download logo. Using placeholder.")
            return None
    except Exception as e:
        print(f"Error downloading logo: {e}")
        return None

def generate_receipt(output_filename="receipt.pdf"):
    # Download logo if not already present
    logo_path = "logo.png"
    if not os.path.exists(logo_path):
        logo_path = download_logo() or logo_path

    # Initialize PDF document
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.5 * inch
    )

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title',
        fontSize=18,
        leading=22,
        alignment=1,  # Center
        spaceAfter=12,
        fontName='Times-Bold',
        textColor=colors.darkblue
    )
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        fontSize=11,
        leading=14,
        alignment=1,
        spaceAfter=6,
        fontName='Times-Roman'
    )
    normal_style = ParagraphStyle(
        name='Normal',
        fontSize=10,
        leading=12,
        spaceAfter=8,
        fontName='Times-Roman'
    )
    bold_style = ParagraphStyle(
        name='Bold',
        fontSize=10,
        leading=12,
        spaceAfter=8,
        fontName='Times-Bold'
    )
    footer_style = ParagraphStyle(
        name='Footer',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.gray,
        fontName='Times-Roman'
    )

    # Content elements
    elements = []

    # Logo (scaled to fit, mimicking Florida OFR style)
    if os.path.exists(logo_path):
        img = PILImage.open(logo_path)
        width, height = img.size
        aspect = height / width
        target_width = 1.8 * inch
        target_height = target_width * aspect
        if target_height > 1.2 * inch:
            target_height = 1.2 * inch
            target_width = target_height / aspect
        logo = Image(logo_path, width=target_width, height=target_height)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.15 * inch))
    else:
        elements.append(Paragraph("US International Wire Compliance Services", subtitle_style))
        elements.append(Spacer(1, 0.15 * inch))

    # Company Details (Miami-based, OFR-aligned)
    elements.append(Paragraph("US International Wire Compliance Services", title_style))
    elements.append(Paragraph("1500 Brickell Avenue, Suite 300, Miami, FL 33131", subtitle_style))
    elements.append(Paragraph("Phone: (305) 777-1234 | Email: compliance@uswirecompliance.org", subtitle_style))
    elements.append(Paragraph("Website: www.uswirecompliance.org | Regulated by Florida OFR", subtitle_style))
    elements.append(Spacer(1, 0.25 * inch))

    # Receipt Header
    elements.append(Paragraph("International Wire Transfer Receipt", title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Transaction Details (updated with user input)
    transaction_details = [
        ["Receipt Number:", "WCS-2025-001"],
        ["Issue Date:", datetime.now().strftime("%B %d, %Y %H:%M:%S")],
        ["Transaction ID:", "TXN-987654321"],
        ["Amount:", "$967,000.00"],
        ["Compliance Fee:", "$4,000.00"],
        ["Total Amount:", "$971,000.00"],
        ["Sender:", "Jason Lucas"],
        ["Sender TIN/SSN:", "XXX-XX-1234"],
        ["Sender Account:", "**** **** **** 1234"],
        ["Sender Address:", "799 Crandon Blvd, Key Biscayne, FL 33149"],
        ["Recipient:", "Jane Smith"],
        ["Recipient Bank:", "Global Bank Ltd."],
        ["Recipient Account:", "**** **** **** 5678"],
        ["SWIFT Code:", "GBKLUS33XXX"],
        ["Purpose:", "International Business Payment"],
        ["Processed By:", "Miami Compliance Office"]
    ]

    # Create table for transaction details
    table = Table(transaction_details, colWidths=[2.5 * inch, 4.5 * inch])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times-Roman', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 0), (1, -1), 'LEFT')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.25 * inch))

    # Barcode (mimicking FinCEN tracking)
    barcode = code128.Code128("WCS-2025-001-TXN-987654321", barHeight=0.5 * inch, barWidth=0.01 * inch)
    barcode.hAlign = 'CENTER'
    elements.append(barcode)
    elements.append(Spacer(1, 0.15 * inch))

    # Compliance and Legal Notes (aligned with BSA/AML, OFAC, FATCA)
    compliance_text = """
    <b>Regulatory Compliance Notice:</b><br/>
    This transaction complies with the Bank Secrecy Act (BSA) and Anti-Money Laundering (AML) regulations under 31 CFR 1010.410 (Travel Rule), requiring originator and beneficiary information for transfers of $3,000 or more. 
    It has been screened against the Office of Foreign Assets Control (OFAC) SDN list to ensure compliance with US sanctions. 
    Transfers exceeding $10,000 are reported to the IRS per IRS regulations. 
    Consumer protections under the Electronic Fund Transfer Act (EFTA) apply, including the right to cancel within 30 minutes of submission (CFPB Remittance Rule). 
    Retain this receipt for your records. For inquiries, contact our Miami office at (305) 777-1234 or email compliance@uswirecompliance.org. 
    Regulated by the Florida Office of Financial Regulation (OFR).
    """
    elements.append(Paragraph(compliance_text, normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Authorized Signature Placeholder
    elements.append(Paragraph("<b>Authorized By:</b> ___________________________", bold_style))
    elements.append(Paragraph("Senior Compliance Officer, US International Wire Compliance Services", normal_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Footer (OFR and federal alignment)
    footer_text = """
    US International Wire Compliance Services<br/>
    Regulated by the Florida Office of Financial Regulation, Tallahassee, FL<br/>
    In Cooperation with FinCEN and OFAC | Miami, FL | © 2025 All Rights Reserved
    """
    elements.append(Paragraph(footer_text, footer_style))

    # Build PDF
    doc.build(elements)
    print(f"PDF receipt generated: {output_filename}")

if __name__ == "__main__":
    generate_receipt()
