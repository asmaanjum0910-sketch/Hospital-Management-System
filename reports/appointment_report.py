from database.db import get_connection
from datetime import datetime


# Date-wise Appointment Report
def date_wise_appointment_report():

    conn = get_connection()
    cursor = conn.cursor()

    # Get appointment date
    appointment_date = input(
        "Enter appointment date (YYYY-MM-DD): "
    ).strip()

    # Validate date
    try:
        datetime.strptime(appointment_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date! Please use YYYY-MM-DD format.")
        conn.close()
        return

    # Fetch appointments
    cursor.execute("""
        SELECT
            a.appointment_id,
            p.name,
            d.name,
            a.appointment_time,
            a.reason,
            a.status
        FROM appointments a
        JOIN patients p
            ON a.patient_id = p.patient_id
        JOIN doctors d
            ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date = ?
        ORDER BY a.appointment_time
    """, (appointment_date,))

    appointments = cursor.fetchall()

    conn.close()

    # Display report
    print("\n" + "=" * 100)
    print("                 DATE-WISE APPOINTMENT REPORT")
    print("=" * 100)

    print("Appointment Date:", appointment_date)

    if not appointments:
        print("\nNo appointments found for this date.")
        return

    print("-" * 100)

    print(
        f"{'ID':<8}"
        f"{'Patient Name':<20}"
        f"{'Doctor Name':<20}"
        f"{'Time':<12}"
        f"{'Reason':<22}"
        f"{'Status':<15}"
    )

    print("-" * 100)

    for appointment in appointments:

        appointment_id, patient_name, doctor_name, appointment_time, reason, status = appointment

        print(
            f"{appointment_id:<8}"
            f"{patient_name:<20}"
            f"{doctor_name:<20}"
            f"{appointment_time:<12}"
            f"{(reason or 'N/A')[:20]:<22}"
            f"{status:<15}"
        )

    print("-" * 100)
    print("Total Appointments:", len(appointments))
    print("=" * 100)