# 🚚 End-to-End Supply Chain Data Pipeline & Analytics

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql)
![PowerBI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?style=for-the-badge&logo=powerbi)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=for-the-badge&logo=pandas)

## 📌 Executive Summary
This project delivers a complete **ETL (Extract, Transform, Load)** data pipeline and interactive analytics solution for supply chain operations. The pipeline processes transactional order data, transforms it into a **Star Schema** in a PostgreSQL data warehouse, and prepares key insights for executive reporting in Power BI.

---

## 🏗️ Architecture & Data Flow

+------------------+      +--------------------------+      +-----------------------+      +-------------------+
|  DataCo Dataset  | ---> |  Python ETL (Pandas)     | ---> | PostgreSQL DWH        | ---> | Power BI          |
|  (Raw CSV)       |      |  Cleanse & Transform     |      | (Star Schema + Views) |      | Executive Report  |
+------------------+      +--------------------------+      +-----------------------+      +-------------------+

1. **Extract**: Ingestion of 180,000+ transactional records from raw CSV data.
2. **Transform**: 
   * Data cleansing and handling of missing attributes.
   * Extraction of unique entities for dimensional tables.
   * Generating smart date keys (`strftime('%Y%m%d')`) for time dimension indexing.
3. **Load**: Automated loading into PostgreSQL database using `SQLAlchemy` and `psycopg2`.
4. **Analytics**: Optimized SQL Views creation and business KPI tracking in Power BI.

---

## 📐 Database Schema (Star Schema)

Designed according to Kimball dimensional modeling principles to minimize redundancy and optimize query performance:

* **Fact Table**: `fact_shipments` (Sales, Discounts, Gross Profit, Shipping Days, Delay Risks)
* **Dimension Tables**:
  * `dim_customer` (Customer details, location, segment)
  * `dim_product` (Product name, category, department, price)
  * `dim_date` (Full date, year, quarter, month, day of week)

---

## 💡 Key Business Insights Discovered

Advanced SQL queries revealed critical operational anomalies:

1. **Unprofitable VIP Customers**:
   * Identified top-tier customers by gross sales (e.g., **Mary Smith** with $10,524.17 sales) generating a **net loss of -$866.38** due to aggressive discount structures and shipping inefficiencies.
2. **On-Time In-Full (OTIF) Shipping Risks**:
   * Utilized SQL CTEs to isolate product categories with higher delay rates against scheduled shipping dates.

---

## 🛠️ Tech Stack & Skills Demonstrated

* **Languages**: Python, SQL (PostgreSQL), DAX
* **Libraries**: `pandas`, `sqlalchemy`, `psycopg2`
* **Data Modeling**: Star Schema, Relational Database Design, Data Warehousing
* **SQL Techniques**: CTEs (Common Table Expressions), Window Functions, Aggregations, Views Creation
* **BI Tools**: Power BI (Data modeling, DAX measures, Interactive visuals)

---

## 🚀 How to Run the ETL Pipeline

### Prerequisites
* Python 3.10+
* PostgreSQL server running locally or remotely
* Power BI Desktop

### Installation & Execution
1. Clone the repository:
   git clone https://github.com/peteo0098/supply-chain-etl-analytics.git
   cd supply-chain-etl-analytics

2. Install dependencies:
   pip install pandas sqlalchemy psycopg2

3. Configure database credentials in `etl_pipeline.py`:
   DB_USER = 'postgres'
   DB_PASSWORD = 'your_password'
   DB_HOST = 'localhost'
   DB_PORT = '5432'
   DB_NAME = 'postgres'

4. Run the ETL process:
   python etl_pipeline.py
