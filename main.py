
from database.db import create_tables
from modules.pdf_receipts import generate_pdf_receipt
from modules.receipts import generate_receipt
from reports.dashboard import hospital_dashboard
from reports.appointment_report import date_wise_appointment_report
from reports.patient_history import patient_history_report
from reports.doctor_report import doctor_appointment_report
from reports.revenue_report import monthly_revenue_report

from modules.patients import (
    add_patient,
    view_patients,
    search_patient,
    search_patient_by_name,
    update_patient,
    delete_patient
)

from modules.doctors import (
    add_doctor,
    view_doctors,
    search_doctor,
    update_doctor,
    delete_doctor
)

from modules.appointments import (
    add_appointment,
    view_appointments,
    search_appointment,
    update_appointment,
    cancel_appointment
)

from modules.billing import (
    generate_bill,
    view_bills,
    search_bill,
    update_payment_status
)


def main():

    create_tables()

    while True:

        print("\n========== HOSPITAL MANAGEMENT SYSTEM ==========")

        print("\n----- PATIENT MANAGEMENT -----")
        print("1. Register Patient")
        print("2. View Patients")
        print("3. Search Patient by ID")
        print("4. Search Patient by Name")
        print("5. Update Patient")
        print("6. Delete Patient")

        print("\n----- DOCTOR MANAGEMENT -----")
        print("7. Register Doctor")
        print("8. View Doctors")
        print("9. Search Doctor by ID")
        print("10. Update Doctor")
        print("11. Delete Doctor")

        print("\n----- APPOINTMENT MANAGEMENT -----")
        print("12. Book Appointment")
        print("13. View Appointments")
        print("14. Search Appointment")
        print("15. Update Appointment")
        print("16. Cancel Appointment")

        print("\n----- BILLING MANAGEMENT -----")
        print("17. Generate Bill")
        print("18. View All Bills")
        print("19. Search Bill")
        print("20. Update Payment Status")
        print("21. Generate Bill Receipt")
        print("21. Generate Bill Receipt (TXT)")
        print("22. Generate PDF Bill Receipt")
        print("23. Hospital Dashboard")
        print("24. Date-wise Appointment Report")
        print("25. Patient History Report")
        print("26. Doctor-wise Appointment Report")
        print("27. Monthly Revenue Report")
        print("\n28. Exit")

        choice = input("\nEnter your choice: ")

        # Patient Management
        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            search_patient()

        elif choice == "4":
            search_patient_by_name()

        elif choice == "5":
            update_patient()

        elif choice == "6":
            delete_patient()

        # Doctor Management
        elif choice == "7":
            add_doctor()

        elif choice == "8":
            view_doctors()

        elif choice == "9":
            search_doctor()

        elif choice == "10":
            update_doctor()

        elif choice == "11":
            delete_doctor()

        # Appointment Management
        elif choice == "12":
            add_appointment()

        elif choice == "13":
            view_appointments()

        elif choice == "14":
            search_appointment()

        elif choice == "15":
            update_appointment()

        elif choice == "16":
            cancel_appointment()

        # Billing Management
        elif choice == "17":
            generate_bill()

        elif choice == "18":
            view_bills()

        elif choice == "19":
            search_bill()

        elif choice == "20":
            update_payment_status()

        elif choice == "21":
            generate_receipt()

        elif choice == "21":
            generate_receipt()

        elif choice == "22":
            generate_pdf_receipt()

        elif choice == "23":
            hospital_dashboard()
        
        elif choice == "24":
            date_wise_appointment_report()

        elif choice == "25":
            patient_history_report()
            
        elif choice == "26":
            doctor_appointment_report()    
        
        elif choice == "27":
            monthly_revenue_report()
                
        elif choice == "28":
            print("Thank you for using Hospital Management System!")
            break

if __name__ == "__main__":
    main()
