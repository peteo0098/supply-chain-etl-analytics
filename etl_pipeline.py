import pandas as pd
from sqlalchemy import create_engine

# --- 1. DATABASE CONNECTION ---
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'  # Place your actual password here
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

print("🔄 Loading CSV file...")
# Load dataset
df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='latin1')

print("🧹 Cleaning and transforming data...")

# --- 2. TRANSFORMATION: Dim_Customer ---
dim_customer = df[[
    'Customer Id', 'Customer Fname', 'Customer Lname', 
    'Customer City', 'Customer Country', 'Customer Segment'
]].drop_duplicates(subset=['Customer Id']).copy()

dim_customer.columns = [
    'customer_id', 'customer_fname', 'customer_lname', 
    'customer_city', 'customer_country', 'customer_segment'
]

# --- 3. TRANSFORMATION: Dim_Product ---
dim_product = df[[
    'Product Card Id', 'Product Name', 'Category Name', 
    'Department Name', 'Product Price'
]].drop_duplicates(subset=['Product Card Id']).copy()

dim_product.columns = [
    'product_card_id', 'product_name', 'category_name', 
    'department_name', 'product_price'
]

# --- 4. TRANSFORMATION: Dim_Date ---
df['order_date'] = pd.to_datetime(df['order date (DateOrders)'])

dim_date = pd.DataFrame()
dim_date['full_date'] = df['order_date'].dt.date.drop_duplicates()
dim_date['date_key'] = pd.to_datetime(dim_date['full_date']).dt.strftime('%Y%m%d').astype(int)
dim_date['year'] = pd.to_datetime(dim_date['full_date']).dt.year
dim_date['quarter'] = pd.to_datetime(dim_date['full_date']).dt.quarter
dim_date['month'] = pd.to_datetime(dim_date['full_date']).dt.month
dim_date['month_name'] = pd.to_datetime(dim_date['full_date']).dt.strftime('%B')
dim_date['day_of_week'] = pd.to_datetime(dim_date['full_date']).dt.strftime('%A')
dim_date['is_weekend'] = pd.to_datetime(dim_date['full_date']).dt.dayofweek >= 5

# --- 5. TRANSFORMATION: Fact_Shipments ---
df['order_date_key'] = df['order_date'].dt.strftime('%Y%m%d').astype(int)

# Dynamic column handling for Late Risk
late_risk_col = 'Late_risk' if 'Late_risk' in df.columns else ('Late risk' if 'Late risk' in df.columns else df.columns[df.columns.str.contains('Late', case=False)][0])

fact_shipments = df[[
    'Order Id', 'Order Item Id', 'Customer Id', 'Product Card Id', 'order_date_key',
    'Days for shipping (real)', 'Days for shipment (scheduled)', 'Delivery Status', late_risk_col,
    'Sales', 'Order Item Discount', 'Order Item Profit Ratio', 'Benefit per order'
]].copy()

fact_shipments.columns = [
    'order_id', 'order_item_id', 'customer_id', 'product_card_id', 'order_date_key',
    'days_for_shipping_real', 'days_for_shipment_scheduled', 'delivery_status', 'late_risk',
    'sales', 'order_item_discount', 'order_item_profit_ratio', 'gross_profit'
]

# --- 6. LOAD DATA TO POSTGRESQL ---
print("🚀 Writing data to PostgreSQL...")

dim_customer.to_sql('dim_customer', engine, if_exists='append', index=False)
print("✅ Dim_Customer successfully loaded.")

dim_product.to_sql('dim_product', engine, if_exists='append', index=False)
print("✅ Dim_Product successfully loaded.")

dim_date.to_sql('dim_date', engine, if_exists='append', index=False)
print("✅ Dim_Date successfully loaded.")

fact_shipments.to_sql('fact_shipments', engine, if_exists='append', index=False)
print("🎉 Fact_Shipments successfully loaded!")

print("🔥 ETL PIPELINE COMPLETED SUCCESSFULLY!")
