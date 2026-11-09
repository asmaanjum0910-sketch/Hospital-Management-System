
import sqlite3
import math
from database.db import get_connection


# Validate Doctor Name
def validate_name(name):
    while not name.strip():
        print("Doctor name cannot be empty!")
        name = input("Enter doctor name: ").strip()

    return name


# Validate Specialization
def validate_specialization(specialization):
    while not specialization.strip():
        print("Specialization cannot be empty!")
        specialization = input("Enter specialization: ").strip()

    return specialization


# Validate Phone Number
def validate_phone(phone):
    while not phone.isdigit() or len(phone) != 10:
        print("Phone number must contain exactly 10 digits!")
        phone = input("Enter phone number: ").strip()

    return phone


# Validate Experience
def validate_experience():
    while True:
        try:
            experience = int(input("Enter years of experience: "))

            if experience < 0:
                print("Experience cannot be negative!")
                continue

            return experience

        except ValueError:
            print("Please enter a valid whole number!")


# Validate Consultation Fee
def validate_consultation_fee():
    while True:
        try:
            fee = float(input("Enter consultation fee: "))

            if not math.isfinite(fee) or fee <= 0:
                print("Consultation fee must be a valid number greater than zero!")
                continue

            return fee

        except ValueError:
            print("Please enter a valid consultation fee!")


# Add Doctor
def add_doctor():

    print("\n===== DOCTOR REGISTRATION =====")

    name = validate_name(input("Enter doctor name: ").strip())
    specialization = validate_specialization(
        input("Enter specialization: ").strip()
    )
    phone = validate_phone(input("Enter phone number: ").strip())
    experience = validate_experience()
    consultation_fee = validate_consultation_fee()

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check duplicate phone number
        cursor.execute(
            "SELECT doctor_id FROM doctors WHERE TRIM(phone) = ?",
            (phone,)
        )

        existing_doctor = cursor.fetchone()

        if existing_doctor:
            print("This phone number is already registered!")
            return

        # Insert doctor details
        cursor.execute(
            """
            INSERT INTO doctors
            (name, specialization, phone, experience, consultation_fee)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, specialization, phone, experience, consultation_fee)
        )

        conn.commit()

        print("\nDoctor registered successfully!")

    except sqlite3.IntegrityError:
        print("Unable to register doctor due to a database constraint.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# View Doctors
def view_doctors():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()

        if doctors:
            print("\n====================== DOCTOR RECORDS ======================")

            print(
                f"{'Doctor ID':<12}"
                f"{'Name':<20}"
                f"{'Specialization':<20}"
                f"{'Phone':<15}"
                f"{'Experience':<12}"
                f"{'Fee':<10}"
            )

            print("-" * 90)

            for doctor in doctors:
                print(
                    f"{doctor[0]:<12}"
                    f"{doctor[1]:<20}"
                    f"{doctor[2]:<20}"
                    f"{doctor[3]:<15}"
                    f"{doctor[4]:<12}"
                    f"{doctor[5]:<10.2f}"
                )

        else:
            print("No doctor records found!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Search Doctor
def search_doctor():

    try:
        doctor_id = int(input("Enter Doctor ID to search: "))

        if doctor_id <= 0:
            print("Doctor ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid Doctor ID!")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if doctor:
            print("\n===== DOCTOR DETAILS =====")
            print("Doctor ID:", doctor[0])
            print("Name:", doctor[1])
            print("Specialization:", doctor[2])
            print("Phone:", doctor[3])
            print("Experience:", doctor[4], "years")
            print("Consultation Fee: ₹", doctor[5])

        else:
            print("Doctor not found!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Update Doctor
def update_doctor():

    try:
        doctor_id = int(input("Enter Doctor ID to update: "))

        if doctor_id <= 0:
            print("Doctor ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid Doctor ID!")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if not doctor:
            print("Doctor not found!")
            return

        print("\nCurrent Doctor Details:", doctor)

        name = validate_name(
            input("Enter new doctor name: ").strip()
        )

        specialization = validate_specialization(
            input("Enter new specialization: ").strip()
        )

        phone = validate_phone(
            input("Enter new phone number: ").strip()
        )

        experience = validate_experience()
        consultation_fee = validate_consultation_fee()

        # Check duplicate phone number excluding current doctor
        cursor.execute(
            """
            SELECT doctor_id FROM doctors
            WHERE TRIM(phone) = ? AND doctor_id != ?
            """,
            (phone, doctor_id)
        )

        existing_doctor = cursor.fetchone()

        if existing_doctor:
            print("This phone number is already registered with another doctor!")
            return

        # Update doctor details
        cursor.execute(
            """
            UPDATE doctors
            SET name = ?,
                specialization = ?,
                phone = ?,
                experience = ?,
                consultation_fee = ?
            WHERE doctor_id = ?
            """,
            (
                name,
                specialization,
                phone,
                experience,
                consultation_fee,
                doctor_id
            )
        )

        conn.commit()

        print("Doctor details updated successfully!")

    except sqlite3.IntegrityError:
        print("Unable to update doctor due to a database constraint.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# Delete Doctor
def delete_doctor():

    try:
        doctor_id = int(input("Enter Doctor ID to delete: "))

        if doctor_id <= 0:
            print("Doctor ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid Doctor ID!")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if not doctor:
            print("Doctor not found!")
            return

        print("\n===== DOCTOR DETAILS =====")
        print("Doctor ID:", doctor[0])
        print("Name:", doctor[1])
        print("Specialization:", doctor[2])

        confirm = input(
            "Are you sure you want to delete this doctor? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            cursor.execute(
                "DELETE FROM doctors WHERE doctor_id = ?",
                (doctor_id,)
            )

            conn.commit()

            print("Doctor deleted successfully!")

        else:
            print("Doctor deletion cancelled!")

    except sqlite3.IntegrityError:
        print(
            "Cannot delete this doctor because existing appointments "
            "are linked to this doctor."
        )

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()
