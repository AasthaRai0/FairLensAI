from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import io
import logging

logger = logging.getLogger(__name__)


class PDFService:

    def __init__(self):
        self.page_size = letter
        self.margin = 0.5 * inch

    def generate_report(self, audit_result, output_path=None):

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        story = []
        styles = getSampleStyleSheet()

        # ✅ TITLE
        story.append(self._create_title(styles))
        story.append(Spacer(1, 0.3 * inch))

        # ✅ SUMMARY
        story.append(self._create_summary_section(audit_result, styles))
        story.append(Spacer(1, 0.3 * inch))

        # ✅ SCORE
        story.append(self._create_score_section(audit_result, styles))
        story.append(Spacer(1, 0.2 * inch))

        # ✅ 🔐 ARMORIQ BADGE
        story.append(self._create_verification_section(audit_result, styles))
        story.append(Spacer(1, 0.3 * inch))

        # ✅ METRICS TABLE
        story.append(self._create_metrics_table(audit_result))
        story.append(Spacer(1, 0.3 * inch))

        # ✅ EXPLANATION (FIXED)
        story.extend(self._create_explanation_section(audit_result, styles))
        story.append(Spacer(1, 0.3 * inch))

        # ✅ RECOMMENDATIONS (FIXED)
        story.extend(self._create_recommendations_section(audit_result, styles))
        story.append(Spacer(1, 0.3 * inch))

        # ✅ FOOTER
        story.append(self._create_footer(styles))

        doc.build(story)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        if output_path:
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)

        return pdf_bytes

    # ---------------- UI COMPONENTS ----------------

    def _create_title(self, styles):
        style = ParagraphStyle(
            'title',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=22,
            textColor=colors.HexColor("#1F2937")
        )

        return Paragraph(
            "<b>FairLens AI Fairness Audit Report</b><br/><font size=10 color='#6B7280'>Ethical AI Compliance Report</font>",
            style
        )

    def _create_summary_section(self, audit_result, styles):
        text = f"""
        <b>File:</b> {audit_result.get("file_name")}<br/>
        <b>Date:</b> {audit_result.get("timestamp")}<br/>
        <b>Protected Attributes:</b> {", ".join(audit_result.get("protected_attributes", []))}<br/>
        <b>Outcome:</b> {audit_result.get("outcome_column")}
        """
        return Paragraph(text, styles['Normal'])

    def _create_score_section(self, audit_result, styles):
        score = audit_result.get("overall_score", 0)

        if score < 40:
            color = "#EF4444"
            level = "Critical"
            msg = "High bias detected. Immediate action required."
        elif score < 70:
            color = "#F59E0B"
            level = "Moderate"
            msg = "Moderate bias present."
        else:
            color = "#10B981"
            level = "Good"
            msg = "System is relatively fair."

        text = f"""
        <font size=16><b>Fairness Score: {score:.1f}/100</b></font><br/>
        <font color="{color}"><b>{level}</b></font><br/>
        <font size=10>{msg}</font>
        """

        return Paragraph(text, styles['Normal'])

    # 🔐 ARMORIQ BADGE
    def _create_verification_section(self, audit_result, styles):
        verified = audit_result.get("verified", False)

        if verified:
            text = '<font color="#10B981"><b>✔ Verified by ArmorIQ</b></font>'
        else:
            text = '<font color="#EF4444"><b>✘ Not Verified</b></font>'

        return Paragraph(text, styles['Normal'])

    def _create_metrics_table(self, audit_result):
        metrics = audit_result.get("metrics", {})
        attrs = audit_result.get("protected_attributes", [])

        data = [["Attribute", "DP", "EOD", "EO"]]

        for attr in attrs:
            dp = metrics.get("demographic_parity_difference", {}).get(attr, 0)
            eod = metrics.get("equalized_odds_difference", {}).get(attr, 0)
            eo = metrics.get("equal_opportunity_difference", {}).get(attr, 0)

            data.append([
                attr,
                f"{dp:.3f}",
                f"{eod:.3f}",
                f"{eo:.3f}"
            ])

        table = Table(data)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        return table

    def _create_explanation_section(self, audit_result, styles):
        return [
            Paragraph("<b>Explanation</b>", styles['Heading2']),
            Paragraph(audit_result.get("explanation", ""), styles['Normal'])
        ]

    def _create_recommendations_section(self, audit_result, styles):
        items = [Paragraph("<b>Recommendations</b>", styles['Heading2'])]

        for i, rec in enumerate(audit_result.get("recommendations", []), 1):
            items.append(Paragraph(f"{i}. {rec}", styles['Normal']))

        return items

    def _create_footer(self, styles):
        text = f"Generated on {datetime.utcnow()} | FairLens Platform"

        style = ParagraphStyle(
            'footer',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            fontSize=8,
            textColor=colors.grey
        )

        return Paragraph(text, style)