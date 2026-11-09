
import os
import sqlite3
from datetime import datetime
from database.db import get_connection


# Generate Bill Receipt
def generate_receipt():

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

        # Create receipt content
        receipt = f"""
================================================================
                    HOSPITAL MANAGEMENT SYSTEM
                         PAYMENT RECEIPT
================================================================

Receipt Date : {receipt_date}
Receipt Time : {receipt_time}

----------------------------------------------------------------
                         BILL INFORMATION
----------------------------------------------------------------

Bill ID          : {bill_id}
Appointment ID   : {appointment_id}

----------------------------------------------------------------
                         PATIENT DETAILS
----------------------------------------------------------------

Patient Name     : {patient_name}
Phone Number     : {patient_phone}
Address          : {patient_address}

----------------------------------------------------------------
                         DOCTOR DETAILS
----------------------------------------------------------------

Doctor Name      : {doctor_name}
Specialization   : {specialization}

----------------------------------------------------------------
                         PAYMENT DETAILS
----------------------------------------------------------------

Consultation Fee       : Rs. {consultation_fee:.2f}
Additional Charges     : Rs. {additional_charges:.2f}

----------------------------------------------------------------
TOTAL AMOUNT           : Rs. {total_amount:.2f}
PAYMENT STATUS         : {payment_status}
----------------------------------------------------------------

                  Thank you for visiting!
                 Wishing you good health.

================================================================
"""

        # Create receipts folder if it does not exist
        os.makedirs("receipts", exist_ok=True)

        # Save receipt as text file
        file_path = os.path.join(
            "receipts",
            f"Bill_{bill_id}.txt"
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(receipt)

        print("\nReceipt generated successfully!")
        print("Receipt Location:", file_path)

    except sqlite3.Error as e:
        print("Database error:", e)

    except OSError as e:
        print("File creation error:", e)

    finally:
        if conn is not None:
            conn.close()
