USE DATABASE HOSPITAL_RAW;
USE SCHEMA RAW_DATA;



PUT file://C:/hospital_data/bed_occupancy.csv @raw_hospital_stage;
PUT file://C:/hospital_data/billing.csv @raw_hospital_stage;
PUT file://C:/hospital_data/department_finance.csv @raw_hospital_stage;
PUT file://C:/hospital_data/departments.csv @raw_hospital_stage;
PUT file://C:/hospital_data/drug_inventory.csv @raw_hospital_stage;
PUT file://C:/hospital_data/employees.csv @raw_hospital_stage;
PUT file://C:/hospital_data/equipment_availability.csv @raw_hospital_stage;
PUT file://C:/hospital_data/er_performance.csv @raw_hospital_stage;
PUT file://C:/hospital_data/hospital_expenses.csv @raw_hospital_stage;
PUT file://C:/hospital_data/overall_finance.csv @raw_hospital_stage;
PUT file://C:/hospital_data/patient_admissions.csv @raw_hospital_stage;
PUT file://C:/hospital_data/patients.csv @raw_hospital_stage;
PUT file://C:/hospital_data/salary_payments.csv @raw_hospital_stage;
PUT file://C:/hospital_data/staff_workload.csv @raw_hospital_stage;

list @raw_hospital_stage;

