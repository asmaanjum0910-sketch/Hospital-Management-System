from database.db import get_connection


# Doctor-wise Appointment Report
def doctor_appointment_report():

    conn = get_connection()
    cursor = conn.cursor()

    # Get Doctor ID
    try:
        doctor_id = int(input("Enter Doctor ID: "))
    except ValueError:
        print("Invalid Doctor ID!")
        conn.close()
        return

    # Fetch Doctor Details
    cursor.execute("""
        SELECT doctor_id, name, specialization
        FROM doctors
        WHERE doctor_id = ?
    """, (doctor_id,))

    doctor = cursor.fetchone()

    if doctor is None:
        print("Doctor not found!")
        conn.close()
        return

    # Fetch Appointment Summary
    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'Scheduled' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)
        FROM appointments
        WHERE doctor_id = ?
    """, (doctor_id,))

    summary = cursor.fetchone()

    # Fetch Appointment Details
    cursor.execute("""
        SELECT
            a.appointment_id,
            p.name,
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        WHERE a.doctor_id = ?
        ORDER BY a.appointment_date DESC,
                 a.appointment_time DESC
    """, (doctor_id,))

    appointments = cursor.fetchall()

    conn.close()

    # Display Report
    print("\n" + "=" * 75)
    print("                 DOCTOR-WISE APPOINTMENT REPORT")
    print("=" * 75)

    print("\n----- DOCTOR DETAILS -----")
    print("Doctor ID      :", doctor[0])
    print("Doctor Name    :", doctor[1])
    print("Specialization :", doctor[2])

    print("\n----- APPOINTMENT SUMMARY -----")
    print("Total Appointments      :", summary[0])
    print("Scheduled Appointments :", summary[1] or 0)
    print("Completed Appointments :", summary[2] or 0)
    print("Cancelled Appointments :", summary[3] or 0)

    print("\n----- APPOINTMENT DETAILS -----")

    if not appointments:
        print("No appointments found for this doctor.")

    else:
        for appointment in appointments:

            print("-" * 75)
            print("Appointment ID :", appointment[0])
            print("Patient Name   :", appointment[1])
            print("Date           :", appointment[2])
            print("Time           :", appointment[3])
            print("Reason         :", appointment[4] or "N/A")
            print("Status         :", appointment[5])

    print("=" * 75)