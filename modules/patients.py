
import sqlite3
from database.db import get_connection


# ==================================================
# 1. INPUT VALIDATION FUNCTIONS
# ==================================================

def validate_name(name):

    while not name.strip():
        print("Name cannot be empty!")
        name = input("Enter patient name: ")

    return name.strip()


def validate_age():

    while True:
        try:
            age = int(input("Enter patient age: "))

            if 1 <= age <= 120:
                return age
            else:
                print("Age must be between 1 and 120.")

        except ValueError:
            print("Please enter a valid number.")


def validate_gender():

    while True:
        gender = input(
            "Enter gender (Male/Female/Other): "
        ).strip().capitalize()

        if gender in ["Male", "Female", "Other"]:
            return gender

        print("Invalid gender. Try again.")


def validate_phone():

    while True:
        phone = input(
            "Enter 10-digit phone number: "
        ).strip()

        if phone.isdigit() and len(phone) == 10:
            return phone

        print("Phone number must contain exactly 10 digits.")


def validate_address():

    while True:
        address = input("Enter address: ").strip()

        if address:
            return address

        print("Address cannot be empty!")


# ==================================================
# 2. ADD PATIENT
# ==================================================

def add_patient():

    print("\n===== REGISTER PATIENT =====")

    name = validate_name(input("Enter patient name: "))
    age = validate_age()
    gender = validate_gender()
    phone = validate_phone()
    address = validate_address()

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check duplicate phone number
        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE TRIM(phone) = ?
            """,
            (phone,)
        )

        existing_patient = cursor.fetchone()

        if existing_patient:
            print("This phone number is already registered!")
            return

        # Insert patient details
        cursor.execute("""
            INSERT INTO patients
            (name, age, gender, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, phone, address))

        conn.commit()

        print("Patient registered successfully!")

    except sqlite3.IntegrityError as e:
        print("Database integrity error:", e)

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# ==================================================
# 3. VIEW ALL PATIENTS
# ==================================================

def view_patients():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM patients")

        patients = cursor.fetchall()

        if patients:

            print("\n================ PATIENT RECORDS ================")

            print(
                "{:<12} {:<20} {:<8} {:<10} {:<15} {:<20}".format(
                    "Patient ID", "Name", "Age",
                    "Gender", "Phone", "Address"
                )
            )

            print("-" * 90)

            for patient in patients:

                print(
                    "{:<12} {:<20} {:<8} {:<10} {:<15} {:<20}".format(
                        patient[0],
                        patient[1],
                        patient[2],
                        patient[3],
                        patient[4],
                        patient[5]
                    )
                )

        else:
            print("No patient records found!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# ==================================================
# 4. SEARCH PATIENT BY ID
# ==================================================

def search_patient():

    try:
        patient_id = int(input("Enter Patient ID to search: "))

        if patient_id <= 0:
            print("Patient ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid Patient ID!")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient:
            print("\n===== PATIENT DETAILS =====")
            print("Patient ID:", patient[0])
            print("Name:", patient[1])
            print("Age:", patient[2])
            print("Gender:", patient[3])
            print("Phone:", patient[4])
            print("Address:", patient[5])

        else:
            print("Patient not found!")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# ==================================================
# 5. SEARCH PATIENT BY NAME
# ==================================================

def search_patient_by_name():

    name = input("Enter patient name to search: ").strip()

    if not name:
        print("Patient name cannot be empty!")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM patients
            WHERE name LIKE ?
            """,
            ('%' + name + '%',)
        )

        patients = cursor.fetchall()

        if patients:

            print("\n===== SEARCH RESULTS =====")

            print(
                f"{'ID':<12}"
                f"{'Name':<20}"
                f"{'Age':<9}"
                f"{'Gender':<11}"
                f"{'Phone':<15}"
                f"{'Address'}"
            )

            print("-" * 85)

            for patient in patients:

                print(
                    f"{patient[0]:<12}"
                    f"{patient[1]:<20}"
                    f"{patient[2]:<9}"
                    f"{patient[3]:<11}"
                    f"{patient[4]:<15}"
                    f"{patient[5]}"
                )

        else:
            print("No patient found with that name.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# ==================================================
# 6. UPDATE PATIENT
# ==================================================

def update_patient():

    try:
        patient_id = int(input("Enter Patient ID to update: "))

        if patient_id <= 0:
            print("Patient ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid Patient ID.")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if not patient:
            print("Patient not found!")
            return

        print("\nCurrent Patient Details:", patient)

        name = validate_name(input("Enter new name: "))
        age = validate_age()
        gender = validate_gender()
        phone = validate_phone()
        address = validate_address()

        # Check duplicate phone number excluding current patient
        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE TRIM(phone) = ? AND patient_id != ?
            """,
            (phone, patient_id)
        )

        existing_patient = cursor.fetchone()

        if existing_patient:
            print(
                "This phone number is already registered "
                "with another patient!"
            )
            return

        # Update patient details
        cursor.execute("""
            UPDATE patients
            SET name = ?,
                age = ?,
                gender = ?,
                phone = ?,
                address = ?
            WHERE patient_id = ?
        """, (name, age, gender, phone, address, patient_id))

        conn.commit()

        print("Patient details updated successfully!")

    except sqlite3.IntegrityError as e:
        print("Database integrity error:", e)

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()


# ==================================================
# 7. DELETE PATIENT
# ==================================================

def delete_patient():

    try:
        patient_id = int(input("Enter Patient ID to delete: "))

        if patient_id <= 0:
            print("Patient ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid Patient ID.")
        return

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if not patient:
            print("Patient not found!")
            return

        print("\nPatient Details:", patient)

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            cursor.execute(
                "DELETE FROM patients WHERE patient_id = ?",
                (patient_id,)
            )

            conn.commit()

            print("Patient deleted successfully!")

        else:
            print("Deletion cancelled.")

    except sqlite3.IntegrityError:
        print(
            "Cannot delete this patient because related "
            "appointments or billing records exist."
        )

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()
