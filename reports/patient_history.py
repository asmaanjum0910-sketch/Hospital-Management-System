from database.db import get_connection


# Patient History Report
def patient_history_report():

    conn = get_connection()
    cursor = conn.cursor()

    # Get Patient ID
    try:
        patient_id = int(input("Enter Patient ID: "))
    except ValueError:
        print("Invalid Patient ID!")
        conn.close()
        return

    # Fetch Patient Details
    cursor.execute("""
        SELECT patient_id, name, age, gender, phone, address
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    if patient is None:
        print("Patient not found!")
        conn.close()
        return

    # Display Patient Details
    print("\n" + "=" * 70)
    print("                    PATIENT HISTORY REPORT")
    print("=" * 70)

    print("\n----- PATIENT DETAILS -----")
    print("Patient ID :", patient[0])
    print("Name       :", patient[1])
    print("Age        :", patient[2])
    print("Gender     :", patient[3])
    print("Phone      :", patient[4])
    print("Address    :", patient[5])

    # Fetch Appointment History
    cursor.execute("""
        SELECT
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            d.name,
            d.specialization,
            a.reason,
            a.status
        FROM appointments a
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        WHERE a.patient_id = ?
        ORDER BY a.appointment_date DESC,
                 a.appointment_time DESC
    """, (patient_id,))

    appointments = cursor.fetchall()

    print("\n----- APPOINTMENT HISTORY -----")

    if not appointments:
        print("No appointments found.")
    else:
        for appointment in appointments:

            print("-" * 70)
            print("Appointment ID :", appointment[0])
            print("Date            :", appointment[1])
            print("Time            :", appointment[2])
            print("Doctor          :", appointment[3])
            print("Specialization  :", appointment[4])
            print("Reason          :", appointment[5])
            print("Status          :", appointment[6])

    # Fetch Billing History
    cursor.execute("""
        SELECT
            bill_id,
            appointment_id,
            consultation_fee,
            additional_charges,
            total_amount,
            payment_status
        FROM bills
        WHERE patient_id = ?
        ORDER BY bill_id DESC
    """, (patient_id,))

    bills = cursor.fetchall()

    print("\n----- BILLING HISTORY -----")

    if not bills:
        print("No billing records found.")
    else:
        for bill in bills:

            print("-" * 70)
            print("Bill ID             :", bill[0])
            print("Appointment ID      :", bill[1])
            print("Consultation Fee    : Rs. {:.2f}".format(bill[2]))
            print("Additional Charges  : Rs. {:.2f}".format(bill[3]))
            print("Total Amount        : Rs. {:.2f}".format(bill[4]))
            print("Payment Status      :", bill[5])

    conn.close()

    print("\n" + "=" * 70)
    print("             END OF PATIENT HISTORY REPORT")
    print("=" * 70)