
from database.db import get_connection
from datetime import date

# Hospital Dashboard
def hospital_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    # Total Doctors
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]

    # Most Frequently Visited Doctor
    cursor.execute("""
    SELECT
        d.name,
        COUNT(a.appointment_id) AS total_appointments
    FROM doctors d
    JOIN appointments a
        ON d.doctor_id = a.doctor_id
    GROUP BY d.doctor_id, d.name
    ORDER BY total_appointments DESC
    LIMIT 1
    """)

    top_doctor = cursor.fetchone()
    
    # Total Appointments
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]

    # Today's Appointments

    today = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT COUNT(*)
    FROM appointments
    WHERE appointment_date = ?
    """, (today,))

    todays_appointments = cursor.fetchone()[0]
    
    # Scheduled Appointments
    cursor.execute("""
        SELECT COUNT(*)
        FROM appointments
        WHERE status = 'Scheduled'
    """)
    scheduled_appointments = cursor.fetchone()[0]

    # Completed Appointments
    cursor.execute("""
        SELECT COUNT(*)
        FROM appointments
        WHERE status = 'Completed'
    """)
    completed_appointments = cursor.fetchone()[0]

    # Cancelled Appointments
    cursor.execute("""
        SELECT COUNT(*)
        FROM appointments
        WHERE status = 'Cancelled'
    """)
    cancelled_appointments = cursor.fetchone()[0]

    # Total Bills
    cursor.execute("SELECT COUNT(*) FROM bills")
    total_bills = cursor.fetchone()[0]

    # Total Revenue Collected
    cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM bills
        WHERE payment_status = 'Paid'
    """)
    total_revenue = cursor.fetchone()[0]

    # Today's Revenue
    cursor.execute("""
    SELECT COALESCE(SUM(b.total_amount), 0)
    FROM bills b
    JOIN appointments a
        ON b.appointment_id = a.appointment_id
    WHERE b.payment_status = 'Paid'
      AND a.appointment_date = ?
""", (today,))

    todays_revenue = cursor.fetchone()[0]   
    # Pending Payment Amount
    cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM bills
        WHERE payment_status = 'Pending'
    """)
    pending_amount = cursor.fetchone()[0]

    conn.close()

    # Display Dashboard
    print("\n" + "=" * 50)
    print("             HOSPITAL DASHBOARD")
    print("=" * 50)

    print("\n----- GENERAL STATISTICS -----")

    print("Total Patients          :", total_patients)
    print("Total Doctors           :", total_doctors)
    if top_doctor:
        print("Most Visited Doctor     :", top_doctor[0])
        print("Doctor Appointments     :", top_doctor[1])
    else:
        print("Most Visited Doctor     : No appointments yet")
    print("Total Appointments      :", total_appointments)
    print("Today's Appointments    :", todays_appointments)
    print("\n----- APPOINTMENT SUMMARY -----")

    print("Scheduled Appointments :", scheduled_appointments)
    print("Completed Appointments :", completed_appointments)
    print("Cancelled Appointments :", cancelled_appointments)

    print("\n----- BILLING SUMMARY -----")

    print("Total Bills Generated  :", total_bills)
    print("Revenue Collected      : Rs. {:.2f}".format(total_revenue))
    print("Today's Revenue        : Rs. {:.2f}".format(todays_revenue))
    print("Pending Payments       : Rs. {:.2f}".format(pending_amount))

    print("\n" + "=" * 50)
