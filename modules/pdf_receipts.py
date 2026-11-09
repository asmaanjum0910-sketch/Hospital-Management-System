
import os
import sqlite3
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from database.db import get_connection


# Generate PDF Bill Receipt
def generate_pdf_receipt():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get Bill ID
        try:
            bill_id = int(input("Enter Bill ID: "))

            if bill_id <= 0:
                print("Bill ID must be a positive number!")
                return

        except ValueError:
            print("Invalid Bill ID!")
            return

        # Fetch bill details
        cursor.execute("""
            SELECT
                b.bill_id,
                b.appointment_id,
                p.name,
                p.phone,
                p.address,
                d.name,
                d.specialization,
                b.consultation_fee,
                b.additional_charges,
                b.total_amount,
                b.payment_status
            FROM bills b
            JOIN patients p
                ON b.patient_id = p.patient_id
            JOIN appointments a
                ON b.appointment_id = a.appointment_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE b.bill_id = ?
        """, (bill_id,))

        bill = cursor.fetchone()

        if bill is None:
            print("Bill not found!")
            return

        # Store bill details
        bill_id = bill[0]
        appointment_id = bill[1]
        patient_name = bill[2]
        patient_phone = bill[3]
        patient_address = bill[4]
        doctor_name = bill[5]
        specialization = bill[6]
        consultation_fee = bill[7]
        additional_charges = bill[8]
        total_amount = bill[9]
        payment_status = bill[10]

        # Get current date and time
        now = datetime.now()
        receipt_date = now.strftime("%d-%m-%Y")
        receipt_time = now.strftime("%I:%M %p")

        # Create receipts folder
        os.makedirs("receipts", exist_ok=True)

        # PDF file path
        file_path = os.path.join(
            "receipts",
            f"Bill_{bill_id}.pdf"
        )

        # Create PDF document
        document = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "HospitalTitle",
            parent=styles["Title"],
            fontSize=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            spaceAfter=5
        )

        subtitle_style = ParagraphStyle(
            "ReceiptTitle",
            parent=styles["Heading2"],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=15
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading3"],
            textColor=colors.darkblue,
            spaceBefore=10,
            spaceAfter=8
        )

        normal_style = styles["Normal"]

        # PDF content
        elements = []

        elements.append(
            Paragraph("HOSPITAL MANAGEMENT SYSTEM", title_style)
        )

        elements.append(
            Paragraph("PAYMENT RECEIPT", subtitle_style)
        )

        elements.append(
            Paragraph(
                f"<b>Receipt Date:</b> {receipt_date} "
                f"&nbsp;&nbsp;&nbsp; <b>Receipt Time:</b> {receipt_time}",
                normal_style
            )
        )

        elements.append(Spacer(1, 15))

        # Bill information
        elements.append(
            Paragraph("BILL INFORMATION", heading_style)
        )

        bill_data = [
            ["Bill ID", str(bill_id)],
            ["Appointment ID", str(appointment_id)]
        ]

        bill_table = Table(
            bill_data,
            colWidths=[65 * mm, 95 * mm]
        )

        bill_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 8)
        ]))

        elements.append(bill_table)

        # Patient information
        elements.append(
            Paragraph("PATIENT DETAILS", heading_style)
        )

        patient_data = [
            ["Patient Name", Paragraph(str(patient_name), normal_style)],
            ["Phone Number", str(patient_phone)],
            ["Address", Paragraph(str(patient_address or "N/A"), normal_style)]
        ]

        patient_table = Table(
            patient_data,
            colWidths=[65 * mm, 95 * mm]
        )

        patient_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        elements.append(patient_table)

        # Doctor information
        elements.append(
            Paragraph("DOCTOR DETAILS", heading_style)
        )

        doctor_data = [
            ["Doctor Name", Paragraph(str(doctor_name), normal_style)],
            ["Specialization", Paragraph(str(specialization), normal_style)]
        ]

        doctor_table = Table(
            doctor_data,
            colWidths=[65 * mm, 95 * mm]
        )

        doctor_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 8)
        ]))

        elements.append(doctor_table)

        # Payment information
        elements.append(
            Paragraph("PAYMENT DETAILS", heading_style)
        )

        payment_data = [
            ["Description", "Amount (Rs.)"],
            ["Consultation Fee", f"{consultation_fee:.2f}"],
            ["Additional Charges", f"{additional_charges:.2f}"],
            ["Total Amount", f"{total_amount:.2f}"],
            ["Payment Status", str(payment_status)]
        ]

        payment_table = Table(
            payment_data,
            colWidths=[95 * mm, 65 * mm]
        )

        payment_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("BACKGROUND", (0, 3), (-1, 3), colors.lightgrey),
            ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "RIGHT"),
            ("PADDING", (0, 0), (-1, -1), 9)
        ]))

        elements.append(payment_table)

        elements.append(Spacer(1, 30))

        elements.append(
            Paragraph(
                "Thank you for visiting! Wishing you good health.",
                ParagraphStyle(
                    "Footer",
                    parent=normal_style,
                    alignment=TA_CENTER,
                    textColor=colors.darkblue
                )
            )
        )

        # Generate PDF
        document.build(elements)

        print("\nPDF receipt generated successfully!")
        print("PDF Location:", file_path)

    except sqlite3.Error as e:
        print("Database error:", e)

    except OSError as e:
        print("File creation error:", e)

    except Exception as e:
        print("PDF generation error:", e)

    finally:
        if conn is not None:
            conn.close()
