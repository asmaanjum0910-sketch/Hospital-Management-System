
import sqlite3
from datetime import datetime

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


# Validate Appointment Date
def validate_date(date_value):

    try:
        parsed_date = datetime.strptime(date_value, "%Y-%m-%d")

        if parsed_date.strftime("%Y-%m-%d") != date_value:
            return False

        return True

    except ValueError:
        return False


# Validate Appointment Time
def validate_time(time_value):

    try:
        parsed_time = datetime.strptime(time_value, "%H:%M")

        if parsed_time.strftime("%H:%M") != time_value:
            return False

        return True

    except ValueError:
        return False


# Check Appointment Time Conflict
def check_appointment_conflict(
    cursor, patient_id, doctor_id,
    appointment_date, appointment_time,
    exclude_appointment_id=None
):

    query = """
        SELECT appointment_id
        FROM appointments
        WHERE appointment_date = ?
        AND appointment_time = ?
        AND status != 'Cancelled'
        AND (doctor_id = ? OR patient_id = ?)
    """

    parameters = [
        appointment_date,
        appointment_time,
        doctor_id,
        patient_id
    ]

    if exclude_appointment_id is not None:
        query += " AND appointment_id != ?"
        parameters.append(exclude_appointment_id)

    cursor.execute(query, tuple(parameters))

    return cursor.fetchone() is not None


# Add Appointment
def add_appointment():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n===== BOOK APPOINTMENT =====")

        # Get Patient ID
        patient_id = validate_id(
            input("Enter Patient ID: "),
            "Patient ID"
        )

        if patient_id is None:
            return

        # Check whether patient exists
        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        if cursor.fetchone() is None:
            print("Patient not found!")
            return

        # Get Doctor ID
        doctor_id = validate_id(
            input("Enter Doctor ID: "),
            "Doctor ID"
        )

        if doctor_id is None:
            return

        # Check whether doctor exists
        cursor.execute(
            "SELECT doctor_id FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )

        if cursor.fetchone() is None:
            print("Doctor not found!")
            return

        # Get appointment date
        appointment_date = input(
            "Enter Appointment Date (YYYY-MM-DD): "
        ).strip()

        if not validate_date(appointment_date):
            print("Invalid date! Please use YYYY-MM-DD format.")
            return

        # Get appointment time
        appointment_time = input(
            "Enter Appointment Time (HH:MM): "
        ).strip()

        if not validate_time(appointment_time):
            print("Invalid time! Please use HH:MM format.")
            return

        # Get reason
        reason = input(
            "Enter Reason for Appointment: "
        ).strip()

        if not reason:
            print("Appointment reason cannot be empty!")
            return

        # Check doctor and patient availability
        if check_appointment_conflict(
            cursor,
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time
        ):
            print(
                "Appointment conflict! The doctor or patient "
                "already has an appointment at this date and time."
            )
            return

        # Insert appointment
        cursor.execute(
            """
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason
            )
        )

        conn.commit()

        print("\nAppointment booked successfully!")

    except sqlite3.IntegrityError:
        print("Unable to book appointment due to a database constraint.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# View Appointments
def view_appointments():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                a.appointment_id,
                p.name,
                d.name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
                a.status
            FROM appointments a
            JOIN patients p
                ON a.patient_id = p.patient_id
            JOIN doctors d
                ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date, a.appointment_time
            """
        )

        appointments = cursor.fetchall()

        if not appointments:
            print("No appointments found!")
            return

        print("\n================ APPOINTMENT DETAILS ================\n")

        print(
            f"{'ID':<5}"
            f"{'Patient Name':<20}"
            f"{'Doctor Name':<20}"
            f"{'Specialization':<20}"
            f"{'Date':<15}"
            f"{'Time':<10}"
            f"{'Status':<12}"
        )

        print("-" * 102)

        for appointment in appointments:

            appointment_id = appointment[0]
            patient_name = appointment[1]
            doctor_name = appointment[2]
            specialization = appointment[3]
            date = appointment[4]
            time = appointment[5]
            reason = appointment[6]
            status = appointment[7]

            print(
                f"{appointment_id:<5}"
                f"{patient_name:<20}"
                f"{doctor_name:<20}"
                f"{specialization:<20}"
                f"{date:<15}"
                f"{time:<10}"
                f"{status:<12}"
            )

            print(f"Reason: {reason}")
            print("-" * 102)

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Search Appointment by ID
def search_appointment():

    appointment_id = validate_id(
        input("Enter Appointment ID: "),
        "Appointment ID"
    )

    if appointment_id is None:
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                a.appointment_id,
                p.name,
                d.name,
                d.specialization,
                a.appointment_date,
                a.appointment_time,
                a.reason,
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

        print("\n========== APPOINTMENT DETAILS ==========")

        print("Appointment ID :", appointment[0])
        print("Patient Name   :", appointment[1])
        print("Doctor Name    :", appointment[2])
        print("Specialization :", appointment[3])
        print("Date           :", appointment[4])
        print("Time           :", appointment[5])
        print("Reason         :", appointment[6])
        print("Status         :", appointment[7])

        print("=========================================")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Update Appointment
def update_appointment():

    appointment_id = validate_id(
        input("Enter Appointment ID to update: "),
        "Appointment ID"
    )

    if appointment_id is None:
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM appointments
            WHERE appointment_id = ?
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found!")
            return

        print("\nCurrent Appointment Details:")
        print("Date   :", appointment[3])
        print("Time   :", appointment[4])
        print("Reason :", appointment[5])
        print("Status :", appointment[6])

        # Get new date
        new_date = input(
            "Enter New Date (YYYY-MM-DD): "
        ).strip()

        if not validate_date(new_date):
            print("Invalid date! Please use YYYY-MM-DD format.")
            return

        # Get new time
        new_time = input(
            "Enter New Time (HH:MM): "
        ).strip()

        if not validate_time(new_time):
            print("Invalid time! Please use HH:MM format.")
            return

        # Get new reason
        new_reason = input("Enter New Reason: ").strip()

        if not new_reason:
            print("Appointment reason cannot be empty!")
            return

        # Get new status
        new_status = input(
            "Enter Status (Scheduled/Completed/Cancelled): "
        ).strip().capitalize()

        if new_status not in [
            "Scheduled",
            "Completed",
            "Cancelled"
        ]:
            print("Invalid status!")
            return

        # Check time conflict
        if new_status != "Cancelled":

            conflict = check_appointment_conflict(
                cursor,
                appointment[1],
                appointment[2],
                new_date,
                new_time,
                appointment_id
            )

            if conflict:
                print(
                    "Appointment conflict! The doctor or patient "
                    "already has another appointment at this date and time."
                )
                return

        # Update appointment
        cursor.execute(
            """
            UPDATE appointments
            SET appointment_date = ?,
                appointment_time = ?,
                reason = ?,
                status = ?
            WHERE appointment_id = ?
            """,
            (
                new_date,
                new_time,
                new_reason,
                new_status,
                appointment_id
            )
        )

        conn.commit()

        print("Appointment updated successfully!")

    except sqlite3.IntegrityError:
        print("Unable to update appointment due to a database constraint.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Cancel Appointment
def cancel_appointment():

    appointment_id = validate_id(
        input("Enter Appointment ID to cancel: "),
        "Appointment ID"
    )

    if appointment_id is None:
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT status
            FROM appointments
            WHERE appointment_id = ?
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found!")
            return

        if appointment[0] == "Cancelled":
            print("Appointment is already cancelled!")
            return

        confirm = input(
            "Are you sure you want to cancel this appointment? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            cursor.execute(
                """
                UPDATE appointments
                SET status = 'Cancelled'
                WHERE appointment_id = ?
                """,
                (appointment_id,)
            )

            conn.commit()

            print("Appointment cancelled successfully!")

        else:
            print("Appointment cancellation aborted!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()
