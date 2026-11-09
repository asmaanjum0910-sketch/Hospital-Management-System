
import sqlite3
from pathlib import Path

# Get the database folder location
DB_PATH = Path(__file__).resolve().parent / "hospital.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Create Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    # Create Doctors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT NOT NULL,
            experience INTEGER NOT NULL,
            consultation_fee REAL NOT NULL
        )
    """)


    # Create Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled',

            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id),

            FOREIGN KEY (doctor_id)
                REFERENCES doctors(doctor_id)
        )
    """)
    # Create Bills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            appointment_id INTEGER NOT NULL UNIQUE,
            consultation_fee REAL NOT NULL,
            additional_charges REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            payment_status TEXT DEFAULT 'Pending',

            FOREIGN KEY (patient_id)
                REFERENCES patients(patient_id),

            FOREIGN KEY (appointment_id)
                REFERENCES appointments(appointment_id)
        )
    """)

    conn.commit()
    conn.close()

    print("All database tables created successfully!")
