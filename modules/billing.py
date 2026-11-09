
import sqlite3
import math

from database.db import get_connection


# Validate Positive ID
def validate_id(value, field_name):

    try:
        record_id = int(value)

        if record_id <= 0:
            print(f"{field_name} must be greater than zero!")
            return None

        return record_id

    except ValueError:
        print(f"Invalid {field_name}!")
        return None


# Generate Bill
def generate_bill():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n===== GENERATE BILL =====")

        # Get Appointment ID
        appointment_id = validate_id(
            input("Enter Appointment ID: "),
            "Appointment ID"
        )

        if appointment_id is None:
            return

        # Fetch appointment and consultation fee
        cursor.execute(
            """
            SELECT
                a.appointment_id,
                a.patient_id,
                p.name,
                d.name,
                d.consultation_fee,
                a.status
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = ?
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found!")
            return

        if appointment[5] == "Cancelled":
            print("Cannot generate bill for a cancelled appointment!")
            return

        # Check whether bill already exists
        cursor.execute(
            "SELECT bill_id FROM bills WHERE appointment_id = ?",
            (appointment_id,)
        )

        existing_bill = cursor.fetchone()

        if existing_bill is not None:
            print(
                f"Bill already exists for this appointment. "
                f"Bill ID: {existing_bill[0]}"
            )
            return

        patient_id = appointment[1]
        patient_name = appointment[2]
        doctor_name = appointment[3]
        consultation_fee = appointment[4]

        print("\n========== BILL DETAILS ==========")
        print("Patient Name     :", patient_name)
        print("Doctor Name      :", doctor_name)
        print("Consultation Fee : ₹{:.2f}".format(consultation_fee))

        # Get additional charges
        try:
            additional_charges = float(
                input("Enter Additional Charges: ")
            )

            if not math.isfinite(additional_charges):
                print("Please enter a valid finite amount!")
                return

            if additional_charges < 0:
                print("Charges cannot be negative!")
                return

        except ValueError:
            print("Invalid charges!")
            return

        # Calculate total amount
        total_amount = consultation_fee + additional_charges

        print("----------------------------------")
        print("Consultation Fee   : ₹{:.2f}".format(consultation_fee))
        print("Additional Charges : ₹{:.2f}".format(additional_charges))
        print("Total Amount       : ₹{:.2f}".format(total_amount))
        print("Payment Status     : Pending")
        print("----------------------------------")

        # Insert bill
        cursor.execute(
            """
            INSERT INTO bills (
                patient_id,
                appointment_id,
                consultation_fee,
                additional_charges,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                appointment_id,
                consultation_fee,
                additional_charges,
                total_amount
            )
        )

        conn.commit()

        print("\nBill generated successfully!")
        print("Generated Bill ID:", cursor.lastrowid)

    except sqlite3.IntegrityError:
        print("Unable to generate bill due to a database constraint.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# View All Bills
def view_bills():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                b.bill_id,
                p.name,
                b.appointment_id,
                b.consultation_fee,
                b.additional_charges,
                b.total_amount,
                b.payment_status
            FROM bills b
            JOIN patients p
                ON b.patient_id = p.patient_id
            ORDER BY b.bill_id
            """
        )

        bills = cursor.fetchall()

        if not bills:
            print("No bills found!")
            return

        print("\n========== BILL DETAILS ==========\n")

        for bill in bills:

            bill_id = bill[0]
            patient_name = bill[1]
            appointment_id = bill[2]
            consultation_fee = bill[3]
            additional_charges = bill[4]
            total_amount = bill[5]
            payment_status = bill[6]

            print("Bill ID             :", bill_id)
            print("Patient Name        :", patient_name)
            print("Appointment ID      :", appointment_id)
            print("Consultation Fee    : ₹{:.2f}".format(consultation_fee))
            print("Additional Charges  : ₹{:.2f}".format(additional_charges))
            print("Total Amount        : ₹{:.2f}".format(total_amount))
            print("Payment Status      :", payment_status)

            print("-" * 45)

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Search Bill by ID
def search_bill():

    bill_id = validate_id(
        input("Enter Bill ID: "),
        "Bill ID"
    )

    if bill_id is None:
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                b.bill_id,
                p.name,
                b.appointment_id,
                b.consultation_fee,
                b.additional_charges,
                b.total_amount,
                b.payment_status
            FROM bills b
            JOIN patients p
                ON b.patient_id = p.patient_id
            WHERE b.bill_id = ?
            """,
            (bill_id,)
        )

        bill = cursor.fetchone()

        if bill is None:
            print("Bill not found!")
            return

        print("\n========== BILL DETAILS ==========")

        print("Bill ID             :", bill[0])
        print("Patient Name        :", bill[1])
        print("Appointment ID      :", bill[2])
        print("Consultation Fee    : ₹{:.2f}".format(bill[3]))
        print("Additional Charges  : ₹{:.2f}".format(bill[4]))
        print("Total Amount        : ₹{:.2f}".format(bill[5]))
        print("Payment Status      :", bill[6])

        print("==================================")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Update Payment Status
def update_payment_status():

    bill_id = validate_id(
        input("Enter Bill ID: "),
        "Bill ID"
    )

    if bill_id is None:
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check whether bill exists
        cursor.execute(
            """
            SELECT bill_id, payment_status
            FROM bills
            WHERE bill_id = ?
            """,
            (bill_id,)
        )

        bill = cursor.fetchone()

        if bill is None:
            print("Bill not found!")
            return

        print("\nCurrent Payment Status:", bill[1])

        # Get new payment status
        new_status = input(
            "Enter New Status (Paid/Pending): "
        ).strip().capitalize()

        if new_status not in ["Paid", "Pending"]:
            print("Invalid Payment Status!")
            return

        # Check whether status is already the same
        if bill[1] == new_status:
            print(f"Bill payment status is already {new_status}!")
            return

        # Update payment status
        cursor.execute(
            """
            UPDATE bills
            SET payment_status = ?
            WHERE bill_id = ?
            """,
            (new_status, bill_id)
        )

        conn.commit()

        print("Payment status updated successfully!")
        print("New Payment Status:", new_status)

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()
