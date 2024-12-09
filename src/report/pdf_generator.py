from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch
from config.settings import PDF_SETTINGS, OUTPUT_DIR
from datetime import datetime

class PDFReport:
    def __init__(self, website_url):
        self.website_url = website_url
        self.filename = OUTPUT_DIR / f"{website_url.replace('/', '_')}_analysis.pdf"
        self.doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=PDF_SETTINGS['margin'],
            leftMargin=PDF_SETTINGS['margin'],
            topMargin=PDF_SETTINGS['margin'],
            bottomMargin=PDF_SETTINGS['margin']
        )
        self.styles = self._create_styles()
        self.elements = []

    def _create_styles(self):
        """Create custom styles for the PDF."""
        styles = getSampleStyleSheet()
        
        # Create custom heading style
        styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=styles['Heading1'],
            fontSize=PDF_SETTINGS['heading_font_size'],
            spaceAfter=30
        ))
        
        # Create style for missing data
        styles.add(ParagraphStyle(
            name='MissingData',
            parent=styles['Normal'],
            textColor=colors.red,
            fontSize=PDF_SETTINGS['body_font_size']
        ))

        # Create style for AI summary
        styles.add(ParagraphStyle(
            name='AISummary',
            parent=styles['Normal'],
            fontSize=PDF_SETTINGS['body_font_size'],
            backColor=colors.lightgrey,
            borderPadding=8
        ))
        
        return styles

    def add_title_page(self):
        """Add a title page to the report."""
        title = f"Website Analysis Report\n{self.website_url}"
        self.elements.append(Paragraph(title, self.styles['CustomHeading']))
        self.elements.append(Spacer(1, inch))
        date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d')}"
        self.elements.append(Paragraph(date_text, self.styles['Normal']))
        self.elements.append(Spacer(1, inch))

    def add_heading(self, text, level=1):
        """Add a heading to the report."""
        style_name = f'Heading{level}'
        self.elements.append(Paragraph(text, self.styles[style_name]))
        self.elements.append(Spacer(1, 12))

    def add_missing_data_notice(self, section_name):
        """Add a notice for missing data in red text."""
        text = f"Data not available for {section_name}"
        self.elements.append(
            Paragraph(text, self.styles['MissingData'])
        )
        self.elements.append(Spacer(1, 12))

    def add_chart(self, chart_path, width=400, caption=None):
        """Add a chart image to the report with optional caption."""
        self.elements.append(Image(chart_path, width=width))
        if caption:
            self.elements.append(Paragraph(caption, self.styles['Normal']))
        self.elements.append(Spacer(1, 12))

    def add_text(self, text):
        """Add regular text to the report."""
        self.elements.append(Paragraph(text, self.styles['Normal']))
        self.elements.append(Spacer(1, 12))

    def add_ai_summary(self, summary_text):
        """Add an AI-generated summary with distinct styling."""
        self.elements.append(Paragraph("AI Summary:", self.styles['Heading3']))
        self.elements.append(Paragraph(summary_text, self.styles['AISummary']))
        self.elements.append(Spacer(1, 12))

    def add_table(self, data, col_widths=None):
        """Add a table to the report."""
        if not col_widths:
            col_widths = [inch * 2] * len(data[0])
        
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def generate(self):
        """Generate the final PDF report."""
        self.doc.build(self.elements) 