# 🧊 AWS ETL Pipeline: S3 ➜ Lambda ➜ Cleaned CSV ➜ S3

This project demonstrates an end-to-end **AWS serverless ETL pipeline** using **S3** and **Lambda**. It reads raw employee data, processes it to handle bad records, groups the data by department, and writes the result back to S3 in clean CSV format.

---

## 📌 Problem Statement

The input data (`employee_raw.csv`) contains inconsistent or bad entries such as:
- Missing or incorrect `PhoneNumber`
- Invalid `Salary` or `Age` values
- Inconsistent `Dept` or `Designation` fields

The goal is to:
- Clean and validate the data
- Group by department (`Dept`)
- Summarize department-wise employee counts and average salary
- Output a structured, clean CSV to another S3 location

---

## 🧩 Sample Raw Data (employee_raw.csv)

| EmpID | Dept | EmpName | Salary | Age | PhoneNumber | Address | JobRole | Designation |
|-------|------|---------|--------|-----|-------------|---------|---------|-------------|
| 101 | Sales | John D | 50000 | 29 | 9876543210 | NYC | Executive | Sales Rep |
| 102 | HR | Jane | -2000 | abc | 1234 | Boston | HR Analyst | HR |
| 103 | Dev | Max | 65000 | 26 | 9000011122 | SF | Developer | SDE I |

---

## ⚙️ AWS Services Used

- **Amazon S3** – Source and destination storage for CSV files
- **AWS Lambda** – ETL logic implemented in Python
- **IAM** – Role-based access to S3 from Lambda
- *(Optional)* CloudWatch for logging and monitoring

---

## 🚀 Pipeline Workflow

┌────────────┐ ┌──────────────┐ ┌────────────────────┐
│ Raw CSV in │ ─────▶ │ Lambda (ETL) │ ────▶ │ Cleaned CSV Output │
│ S3 Bucket │ │ Python │ │ in S3 Output │
└────────────┘ └──────────────┘ └────────────────────┘
