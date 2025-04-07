# -*- coding: utf-8 -*-
"""
Comprehensive Hospital Data Script

This script generates a variety of datasets simulating hospital data.
Static datasets (e.g., employees, patients, etc.) are generated once.
For daily time-series data (bed occupancy, ER performance, staff workload),
the script appends new data from the day after the last recorded date up to today.
Data is saved in the local folder: C:\hospital_data.
"""

import os
import random
import pandas as pd
import faker
from datetime import datetime, timedelta

# Initialize Faker and seed for reproducibility
fake = faker.Faker()
random.seed(42)

# Define date ranges
FIVE_YEAR_START = datetime(2020, 1, 1)
# For static data, we use an initial end date. For time-series data, we update up to today's date.
initial_end = datetime(2024, 12, 31)
refresh_date = datetime.today().date()  # current refresh date

# ---------- Define Basic Entities: Branches & Departments ----------

branches = [
    {"branch_id": 1, "name": "Lagos General Hospital", "state": "Lagos"},
    {"branch_id": 2, "name": "Abuja Specialist Clinic", "state": "FCT"},
    {"branch_id": 3, "name": "Kano Medical Center", "state": "Kano"},
    {"branch_id": 4, "name": "Port Harcourt Teaching Hospital", "state": "Rivers"},
    {"branch_id": 5, "name": "Enugu State Hospital", "state": "Enugu"}
]

department_names = ["General Medicine", "Pediatrics", "Cardiology", "Orthopedics",
                    "Gynecology", "Radiology", "Emergency", "ICU", "Surgery"]
departments = []
dept_id = 1
for branch in branches:
    dept_list = random.sample(department_names, k=random.randint(3, 5))
    for name in dept_list:
        departments.append({
            "Department ID": dept_id,
            "Department Name": name,
            "Branch ID": branch["branch_id"],
            "Branch Name": branch["name"],
            "State": branch["state"]
        })
        dept_id += 1
departments_df = pd.DataFrame(departments)

# ---------- Data Generation Functions ----------

def random_date(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def generate_employees(num=200):
    employees = []
    for _ in range(num):
        dept = random.choice(departments)
        employees.append({
            "Employee ID": fake.uuid4(),
            "Name": fake.name(),
            "Age": random.randint(22, 65),
            "Gender": random.choice(["Male", "Female"]),
            "Phone": fake.phone_number(),
            "Email": fake.email(),
            "Department ID": dept["Department ID"],
            "Department Name": dept["Department Name"],
            "Branch Name": dept["Branch Name"],
            "State": dept["State"],
            "Role": random.choice(["Doctor", "Nurse", "Technician", "Administrator", "Janitorial", "Pharmacist"])
        })
    return pd.DataFrame(employees)

def generate_patients(num=1000):
    patients = []
    for _ in range(num):
        branch = random.choice(branches)
        patients.append({
            "Patient ID": fake.uuid4(),
            "Name": fake.name(),
            "Age": random.randint(1, 90),
            "Gender": random.choice(["Male", "Female"]),
            "Phone": fake.phone_number(),
            "Address": fake.address().replace("\n", ", "),
            "Branch Name": branch["name"],
            "State": branch["state"],
            "Insurance Provider": random.choice(["AXA Mansard", "Leadway Health", "Avon HMO", "Hygeia HMO", "Reliance HMO"]),
            "Insurance Status": random.choice(["Approved", "Pending", "Rejected"])
        })
    return pd.DataFrame(patients)

def generate_patient_admissions(patients_df, num=1500):
    admissions = []
    for _ in range(num):
        patient = patients_df.sample(1).iloc[0]
        admission_date = random_date(FIVE_YEAR_START, initial_end)
        discharge_date = admission_date + timedelta(days=random.randint(1, 14))
        admissions.append({
            "Admission ID": fake.uuid4(),
            "Patient ID": patient["Patient ID"],
            "Admission Date": admission_date.date(),
            "Discharge Date": discharge_date.date(),
            "Is Readmission": random.choice(["Yes", "No"]),
            "Branch Name": patient["Branch Name"],
            "State": patient["State"],
            "Bed Number": random.randint(1, 200)
        })
    return pd.DataFrame(admissions)

def generate_billing(patients_df, num=1200):
    billing = []
    for _ in range(num):
        patient = patients_df.sample(1).iloc[0]
        billing_date = random_date(FIVE_YEAR_START, initial_end)
        total_amount = round(random.uniform(5000, 2000000), 2)
        insurance_covered = total_amount if random.choice([True, False]) else round(random.uniform(0, total_amount), 2)
        billing.append({
            "Billing ID": fake.uuid4(),
            "Patient ID": patient["Patient ID"],
            "Date": billing_date.date(),
            "Total Amount": total_amount,
            "Insurance Covered": insurance_covered,
            "Out-of-Pocket": round(total_amount - insurance_covered, 2),
            "Payment Method": random.choice(["Cash", "POS", "Bank Transfer", "Insurance"]),
            "Branch Name": patient["Branch Name"],
            "State": patient["State"]
        })
    return pd.DataFrame(billing)

def generate_overall_finance(num=300):
    finance = []
    for _ in range(num):
        branch = random.choice(branches)
        finance_date = random_date(FIVE_YEAR_START, initial_end)
        revenue = round(random.uniform(500000, 5000000), 2)
        expenses = round(random.uniform(200000, 4000000), 2)
        finance.append({
            "Finance ID": fake.uuid4(),
            "Branch Name": branch["name"],
            "State": branch["state"],
            "Date": finance_date.date(),
            "Total Revenue": revenue,
            "Total Expenses": expenses,
            "Profit/Loss": round(revenue - expenses, 2)
        })
    return pd.DataFrame(finance)

def generate_department_financials(departments, start_date, end_date):
    dept_finance = []
    current = start_date.replace(day=1)
    while current <= end_date:
        for dept in departments:
            revenue = round(random.uniform(100000, 1000000), 2)
            expenses = round(random.uniform(50000, 800000), 2)
            total_claims = random.randint(50, 200)
            approved_claims = random.randint(int(total_claims * 0.5), total_claims)
            num_patients = random.randint(20, 100)
            cost_per_patient = round(expenses / num_patients, 2) if num_patients > 0 else 0
            dept_finance.append({
                "Department Financial ID": fake.uuid4(),
                "Department ID": dept["Department ID"],
                "Department Name": dept["Department Name"],
                "Branch Name": dept["Branch Name"],
                "State": dept["State"],
                "Month": current.strftime("%Y-%m"),
                "Revenue": revenue,
                "Expenses": expenses,
                "Total Claims Submitted": total_claims,
                "Insurance Claims Approved": approved_claims,
                "Cost Per Patient": cost_per_patient
            })
        # Increment to next month
        next_month = current.month % 12 + 1
        next_year = current.year + (current.month // 12)
        current = current.replace(year=next_year, month=next_month)
    return pd.DataFrame(dept_finance)

def generate_drug_inventory(num=300):
    drugs = ["Paracetamol", "Ibuprofen", "Amoxicillin", "Metformin", "Atorvastatin", "Omeprazole", "Ciprofloxacin"]
    inventory = []
    for _ in range(num):
        branch = random.choice(branches)
        snapshot_date = random_date(FIVE_YEAR_START, initial_end)
        inventory.append({
            "Drug Inventory ID": fake.uuid4(),
            "Drug Name": random.choice(drugs),
            "Quantity": random.randint(10, 500),
            "Unit Cost": round(random.uniform(50, 1000), 2),
            "Expiry Date": fake.date_between(start_date="today", end_date="+2y"),
            "Snapshot Date": snapshot_date.date(),
            "Branch Name": branch["name"],
            "State": branch["state"]
        })
    return pd.DataFrame(inventory)

def generate_salary_payments(employees_df, num_payments=500):
    salary_payments = []
    for _ in range(num_payments):
        employee = employees_df.sample(1).iloc[0]
        payment_date = random_date(FIVE_YEAR_START, initial_end)
        base_salary = random.randint(50000, 300000)
        salary_payments.append({
            "Salary Payment ID": fake.uuid4(),
            "Employee ID": employee["Employee ID"],
            "Name": employee["Name"],
            "Department Name": employee["Department Name"],
            "Branch Name": employee["Branch Name"],
            "Payment Date": payment_date.date(),
            "Amount Paid": base_salary,
            "Payment Method": random.choice(["Cash", "Bank Transfer", "Cheque"])
        })
    return pd.DataFrame(salary_payments)

def generate_hospital_expenses(num=400):
    expense_categories = ["Diesel", "Vendor Payments", "Maintenance", "Utilities", "Medical Supplies"]
    expenses = []
    for _ in range(num):
        branch = random.choice(branches)
        expense_date = random_date(FIVE_YEAR_START, initial_end)
        amount = round(random.uniform(1000, 100000), 2)
        expenses.append({
            "Expense ID": fake.uuid4(),
            "Branch Name": branch["name"],
            "State": branch["state"],
            "Date": expense_date.date(),
            "Category": random.choice(expense_categories),
            "Amount": amount,
            "Vendor": fake.company() if random.choice([True, False]) else "Internal"
        })
    return pd.DataFrame(expenses)

def generate_equipment_availability(num=300):
    equipment_names = ["X-Ray Machine", "MRI Scanner", "Ultrasound", "CT Scanner", "Ventilator", "ECG Machine"]
    equipment_data = []
    for _ in range(num):
        branch = random.choice(branches)
        dept = random.choice(departments)
        snapshot_date = random_date(FIVE_YEAR_START, initial_end)
        equipment_data.append({
            "Equipment ID": fake.uuid4(),
            "Equipment Name": random.choice(equipment_names),
            "Status": random.choice(["Operational", "Under Maintenance", "Out of Service"]),
            "Branch Name": branch["name"],
            "Department Name": dept["Department Name"],
            "Last Maintenance Date": snapshot_date.date()
        })
    return pd.DataFrame(equipment_data)

# ---------- Time-Series Data Functions (with Update Logic) ----------

def generate_bed_occupancy(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    occupancy = []
    for branch in branches:
        total_beds = random.randint(100, 300)
        for day in dates:
            occupied = random.randint(int(total_beds * 0.5), total_beds)
            occupancy.append({
                "Date": day.date(),
                "Branch Name": branch["name"],
                "State": branch["state"],
                "Total Beds": total_beds,
                "Occupied Beds": occupied,
                "Occupancy Rate (%)": round(occupied / total_beds * 100, 2)
            })
    return pd.DataFrame(occupancy)

def generate_er_performance(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    er_data = []
    for branch in branches:
        for day in dates:
            wait_time = random.randint(5, 240)
            inflow = random.randint(10, 100)
            outflow = inflow - random.randint(0, 5)
            success_rate = round(random.uniform(70, 100), 2)
            er_data.append({
                "ER Performance ID": fake.uuid4(),
                "Date": day.date(),
                "ER Wait Time (minutes)": wait_time,
                "Patient Inflow": inflow,
                "Patient Outflow": outflow,
                "Treatment Success Rate (%)": success_rate,
                "Branch Name": branch["name"],
                "State": branch["state"]
            })
    return pd.DataFrame(er_data)

def generate_staff_workload(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    workload = []
    for dept in departments:
        for day in dates:
            num_staff = random.randint(5, 20)
            patients_served = random.randint(num_staff * 2, num_staff * 10)
            workload.append({
                "Date": day.date(),
                "Department ID": dept["Department ID"],
                "Department Name": dept["Department Name"],
                "Branch Name": dept["Branch Name"],
                "State": dept["State"],
                "Number of Staff": num_staff,
                "Patients Served": patients_served
            })
    return pd.DataFrame(workload)

def update_timeseries_data(file_path, gen_func, date_col, start_date, end_date, **kwargs):
    """
    If file exists, load existing data and generate new rows from the day after the last date
    to end_date. Otherwise, generate data from start_date to end_date.
    """
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path, parse_dates=[date_col])
        last_date = existing_df[date_col].max().date()
        new_start = last_date + timedelta(days=1)
        if new_start <= end_date:
            new_data = gen_func(new_start, end_date, **kwargs)
            updated_df = pd.concat([existing_df, new_data], ignore_index=True)
        else:
            updated_df = existing_df
    else:
        updated_df = gen_func(start_date, end_date, **kwargs)
    return updated_df

# ---------- Local Directory Setup ----------
base_dir = r"C:\hospital_data"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# ---------- Generate and Save Static Data (only once) ----------

employees_file = os.path.join(base_dir, "employees.csv")
if not os.path.exists(employees_file):
    employees_df = generate_employees(200)
    employees_df.to_csv(employees_file, index=False)

patients_file = os.path.join(base_dir, "patients.csv")
if not os.path.exists(patients_file):
    patients_df = generate_patients(1000)
    patients_df.to_csv(patients_file, index=False)

departments_file = os.path.join(base_dir, "departments.csv")
if not os.path.exists(departments_file):
    departments_df.to_csv(departments_file, index=False)

admissions_file = os.path.join(base_dir, "patient_admissions.csv")
if not os.path.exists(admissions_file):
    patients_df = pd.read_csv(patients_file) if os.path.exists(patients_file) else generate_patients(1000)
    admissions_df = generate_patient_admissions(patients_df, 1500)
    admissions_df.to_csv(admissions_file, index=False)

billing_file = os.path.join(base_dir, "billing.csv")
if not os.path.exists(billing_file):
    patients_df = pd.read_csv(patients_file) if os.path.exists(patients_file) else generate_patients(1000)
    billing_df = generate_billing(patients_df, 1200)
    billing_df.to_csv(billing_file, index=False)

overall_finance_file = os.path.join(base_dir, "overall_finance.csv")
if not os.path.exists(overall_finance_file):
    overall_finance_df = generate_overall_finance(300)
    overall_finance_df.to_csv(overall_finance_file, index=False)

dept_finance_file = os.path.join(base_dir, "department_finance.csv")
if not os.path.exists(dept_finance_file):
    dept_finance_df = generate_department_financials(departments, FIVE_YEAR_START, initial_end)
    dept_finance_df.to_csv(dept_finance_file, index=False)

drug_inventory_file = os.path.join(base_dir, "drug_inventory.csv")
if not os.path.exists(drug_inventory_file):
    drug_inventory_df = generate_drug_inventory(300)
    drug_inventory_df.to_csv(drug_inventory_file, index=False)

salary_payments_file = os.path.join(base_dir, "salary_payments.csv")
if not os.path.exists(salary_payments_file):
    employees_df = pd.read_csv(employees_file) if os.path.exists(employees_file) else generate_employees(200)
    salary_payments_df = generate_salary_payments(employees_df, 500)
    salary_payments_df.to_csv(salary_payments_file, index=False)

hospital_expenses_file = os.path.join(base_dir, "hospital_expenses.csv")
if not os.path.exists(hospital_expenses_file):
    hospital_expenses_df = generate_hospital_expenses(400)
    hospital_expenses_df.to_csv(hospital_expenses_file, index=False)

equipment_file = os.path.join(base_dir, "equipment_availability.csv")
if not os.path.exists(equipment_file):
    equipment_df = generate_equipment_availability(300)
    equipment_df.to_csv(equipment_file, index=False)

# ---------- Update Time-Series Data (append new days) ----------

bed_occupancy_file = os.path.join(base_dir, "bed_occupancy.csv")
bed_occupancy_df = update_timeseries_data(
    bed_occupancy_file,
    generate_bed_occupancy,
    date_col="Date",
    start_date=FIVE_YEAR_START.date(),
    end_date=refresh_date
)
bed_occupancy_df.to_csv(bed_occupancy_file, index=False)

er_performance_file = os.path.join(base_dir, "er_performance.csv")
er_performance_df = update_timeseries_data(
    er_performance_file,
    generate_er_performance,
    date_col="Date",
    start_date=FIVE_YEAR_START.date(),
    end_date=refresh_date
)
er_performance_df.to_csv(er_performance_file, index=False)

staff_workload_file = os.path.join(base_dir, "staff_workload.csv")
staff_workload_df = update_timeseries_data(
    staff_workload_file,
    generate_staff_workload,
    date_col="Date",
    start_date=FIVE_YEAR_START.date(),
    end_date=refresh_date
)
staff_workload_df.to_csv(staff_workload_file, index=False)

print(f"Hospital data generated/updated and saved to: {base_dir}")
