"""
Professional Invoice Generator
Creates branded PDF invoices for customers
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

class InvoiceGenerator:
    """Generate professional PDF invoices"""
    
    def __init__(self):
        self.output_folder = 'invoices'
        os.makedirs(self.output_folder, exist_ok=True)
    
    def generate_invoice(self, sale_data, items_data, customer_data=None):
        """
        Generate invoice PDF
        
        sale_data: (id, invoice_number, sale_date, customer_name, total_amount, 
                    payment_percentage, sale_status, source)
        items_data: [(product_name, quantity, unit_price, discount, subtotal), ...]
        """
        
        invoice_number = sale_data[1]
        filename = f"Invoice_{invoice_number}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=10
        )
        
        # Add logo if exists
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
            elements.append(logo)
            elements.append(Spacer(1, 0.3*inch))
        
        # Company header
        company_name = Paragraph("<b>☀️ KHSOLAR</b>", title_style)
        elements.append(company_name)
        
        company_info = Paragraph(
            "<b>Professional Solar Solutions</b><br/>"
            "📞 Phone: +855 888 836 588<br/>"
            "💬 Telegram: @chhanycls<br/>"
            "🌐 Website: khsolarcom.streamlit.app",
            header_style
        )
        elements.append(company_info)
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice title and number
        invoice_title = Paragraph(
            f"<b>INVOICE</b><br/>"
            f"<font size=10>Invoice No: {invoice_number}</font>",
            title_style
        )
        elements.append(invoice_title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Date and customer info table
        info_data = [
            ['Invoice Date:', sale_data[2], 'Customer:', sale_data[3]],
            ['Payment Status:', 
             'Paid' if sale_data[5] >= 100 else f'{sale_data[5]:.0f}% Paid',
             'Phone:', customer_data[3] if customer_data and len(customer_data) > 3 else 'N/A'],
            ['Order Status:', sale_data[6], 'Email:', 
             customer_data[4] if customer_data and len(customer_data) > 4 else 'N/A']
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Items table header
        items_header = Paragraph("<b>Items</b>", styles['Heading2'])
        elements.append(items_header)
        elements.append(Spacer(1, 0.1*inch))
        
        # Items data
        items_table_data = [
            ['#', 'Product', 'Qty', 'Unit Price', 'Discount', 'Subtotal']
        ]
        
        for idx, item in enumerate(items_data, 1):
            items_table_data.append([
                str(idx),
                item[0],  # product_name
                str(item[1]),  # quantity
                f"${item[2]:,.2f}",  # unit_price
                f"${item[3]:,.2f}",  # discount
                f"${item[4]:,.2f}"   # subtotal
            ])
        
        items_table = Table(items_table_data, 
                           colWidths=[0.4*inch, 3.2*inch, 0.6*inch, 1.2*inch, 1*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Totals
        subtotal = sum(item[4] for item in items_data)
        discount_total = sum(item[3] for item in items_data)
        total = sale_data[4]
        paid_amount = total * (sale_data[5] / 100)
        remaining = total - paid_amount
        
        totals_data = [
            ['Subtotal:', f'${subtotal:,.2f}'],
            ['Total Discount:', f'${discount_total:,.2f}'],
            ['<b>TOTAL:</b>', f'<b>${total:,.2f}</b>'],
            ['Paid:', f'${paid_amount:,.2f}'],
            ['<b>Balance Due:</b>', f'<b>${remaining:,.2f}</b>']
        ]
        
        totals_table = Table(totals_data, colWidths=[5.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('FONTSIZE', (0, 4), (-1, 4), 12),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.HexColor('#ef4444')),
            ('LINEABOVE', (0, 2), (-1, 2), 1, colors.grey),
            ('LINEABOVE', (0, 4), (-1, 4), 1, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Payment info
        payment_info = Paragraph(
            "<b>Payment Information:</b><br/>"
            "Bank Transfer: [Your Bank Details]<br/>"
            "ABA: [Account Number]<br/>"
            "Wing/TrueMoney: +855 888 836 588",
            styles['Normal']
        )
        elements.append(payment_info)
        elements.append(Spacer(1, 0.3*inch))
        
        # Terms and conditions
        terms = Paragraph(
            "<b>Terms & Conditions:</b><br/>"
            "• Payment due within 30 days<br/>"
            "• 5-25 year warranty on solar panels<br/>"
            "• 5-10 year warranty on inverters<br/>"
            "• Installation included in price<br/>"
            "• Technical support: +855 888 836 588",
            styles['Normal']
        )
        elements.append(terms)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer = Paragraph(
            "<i>Thank you for your business!<br/>"
            "For questions about this invoice, contact us at +855 888 836 588 or @chhanycls</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, 
                          textColor=colors.grey, alignment=TA_CENTER)
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        return filepath
    
    def generate_quotation(self, customer_name, items, notes=''):
        """Generate a quotation (similar to invoice but as a quote)"""
        # Similar structure to invoice but marked as quotation
        pass
