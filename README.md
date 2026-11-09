# Hospital Management System

A console-based Hospital Management System developed using **Python and SQLite** to manage hospital operations, including patients, doctors, appointments, billing, payment receipts, dashboards, and reports.

## Project Overview

The Hospital Management System is designed to simplify daily hospital administration by providing a centralized application for managing patient records, doctor information, appointments, and billing.

The application uses Python for application logic and SQLite for database management. It also generates text and PDF payment receipts.

## Features

### 1. Patient Management
- Register new patients.
- View all patients.
- Search patients by ID and name.
- Update patient information.
- Delete patient records.
- Validate patient details.
- Prevent duplicate phone numbers.

### 2. Doctor Management
- Register doctors.
- View doctor records.
- Search doctors.
- Update doctor information.
- Delete doctor records.
- Manage specialization, experience, consultation fees, and contact details.
- Prevent duplicate phone numbers.

### 3. Appointment Management
- Schedule appointments.
- View all appointments.
- Search appointments.
- Update appointment details.
- Cancel appointments.
- Validate appointment dates and times.
- Prevent scheduling conflicts.

### 4. Billing Management
- Generate bills using appointment details.
- Automatically retrieve consultation fees.
- Add additional charges.
- Calculate total billing amounts.
- View and search bills.
- Update payment status.
- Prevent duplicate bills for the same appointment.

### 5. Receipt Generation
- Generate payment receipts in TXT format.
- Generate professional PDF receipts.
- Include patient, doctor, appointment, and payment information.
- Automatically save receipts in the `receipts` directory.

### 6. Hospital Dashboard
- Total patients.
- Total doctors.
- Total appointments.
- Scheduled, completed, and cancelled appointments.
- Total bills.
- Revenue collected.
- Pending payment amount.
- Today's appointments and revenue.
- Most frequently visited doctor.

### 7. Reports
- Date-wise appointment report.
- Patient history report.
- Doctor-wise appointment report.
- Monthly revenue report.

### 8. Input Validation and Error Handling
- Validate user inputs.
- Handle invalid IDs and missing records.
- Prevent duplicate entries.
- Handle database errors.
- Handle file creation errors.
- Ensure database connections are properly closed.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| SQLite | Database management |
| SQL | Database queries and operations |
| ReportLab | PDF receipt generation |
| VS Code | Development environment |
| Git | Version control |
| GitHub | Source code hosting |

## Project Structure

```text
Hospital_Management_System/
│
├── main.py
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── hospital.db
│
├── modules/
│   ├── __init__.py
│   ├── patients.py
│   ├── doctors.py
│   ├── appointments.py
│   ├── billing.py
│   ├── receipts.py
│   └── pdf_receipts.py
│
├── reports/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── appointment_report.py
│   ├── patient_history.py
│   ├── doctor_report.py
│   └── revenue_report.py
│
├── receipts/
│   ├── Bill_1.txt
│   └── Bill_1.pdf
│
├── README.md
└── .gitignore
```

*Note: The receipts directory contains generated receipt files. Individual receipt files and the SQLite database should generally not be committed if they contain test or personal data.*

## Database Design

The application uses SQLite as its relational database.

Main database tables:

- **patients** – Stores patient information.
- **doctors** – Stores doctor information.
- **appointments** – Stores appointment details and status.
- **bills** – Stores consultation fees, additional charges, total amounts, and payment status.

Foreign key relationships connect patients, doctors, appointments, and bills.

## Installation and Setup

### Prerequisites

- Python 3.x
- Visual Studio Code (recommended)
- Git (for GitHub upload)

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the project folder

```bash
cd Hospital_Management_System
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install reportlab
```

SQLite is included with Python, so a separate installation is not required.

### Step 6: Run the application

```bash
python main.py
```

The application menu will appear in the terminal.

## Application Menu

| Options | Functionality |
|---|---|
| 1–6 | Patient Management |
| 7–11 | Doctor Management |
| 12–16 | Appointment Management |
| 17–22 | Billing and Receipt Generation |
| 23 | Hospital Dashboard |
| 24 | Date-wise Appointment Report |
| 25 | Patient History Report |
| 26 | Doctor-wise Appointment Report |
| 27 | Monthly Revenue Report |
| 28 | Exit |

## Testing

The application was tested through its main menu.

Testing covered:

- Patient registration, searching, updating, and deletion.
- Doctor registration