from database.db import get_connection


# Monthly Revenue Report
def monthly_revenue_report():

    conn = get_connection()
    cursor = conn.cursor()

    # Get Month and Year
    month = input("Enter month (MM): ").strip()
    year = input("Enter year (YYYY): ").strip()

    # Validate month and year
    if not month.isdigit() or not year.isdigit():
        print("Invalid month or year!")
        conn.close()
        return

    month = int(month)
    year = int(year)

    if not 1 <= month <= 12 or year < 1:
        print("Invalid month or year!")
        conn.close()
        return

    month = f"{month:02d}"
    year = str(year)

    # Fetch Monthly Billing Summary
    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN payment_status = 'Paid' THEN 1 ELSE 0 END),
            SUM(CASE WHEN payment_status = 'Pending' THEN 1 ELSE 0 END),
            COALESCE(
                SUM(CASE
                    WHEN payment_status = 'Paid'
                    THEN total_amount
                    ELSE 0
                END), 0
            ),
            COALESCE(
                SUM(CASE
                    WHEN payment_status = 'Pending'
                    THEN total_amount
                    ELSE 0
                END), 0
            )
        FROM bills b
        JOIN appointments a
        ON b.appointment_id = a.appointment_id
        WHERE strftime('%m', a.appointment_date) = ?
        AND strftime('%Y', a.appointment_date) = ?
    """, (month, year))

    summary = cursor.fetchone()

    conn.close()

    total_bills = summary[0]
    paid_bills = summary[1] or 0
    pending_bills = summary[2] or 0
    total_revenue = summary[3]
    pending_amount = summary[4]

    # Display Report
    print("\n" + "=" * 65)
    print("                 MONTHLY REVENUE REPORT")
    print("=" * 65)

    print(f"\nReport Month: {month}/{year}")

    print("\n----- BILLING SUMMARY -----")
    print("Total Bills Generated :", total_bills)
    print("Paid Bills            :", paid_bills)
    print("Pending Bills         :", pending_bills)

    print("\n----- FINANCIAL SUMMARY -----")
    print("Revenue Collected     : Rs. {:.2f}".format(total_revenue))
    print("Pending Amount        : Rs. {:.2f}".format(pending_amount))

    print("=" * 65)