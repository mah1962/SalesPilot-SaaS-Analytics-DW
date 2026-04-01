from pathlib import Path

BASE_PATH = Path(r"D:\SQL\TRAINING PROJECTS\SalesPilot_SaaS Analytics Data Warehouse\SaaS-Sales-Analytics\01_Data\Raw")

SQL_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "localhost",
    "database": "SalesPilotDW",
    # حذفنا اليوزر والباسورد لأننا سنستخدم Trusted_Connection في load.py
}

TABLE_MAPPING = {
    "dim_company": "DimCompany",       # مطابق لـ dim_company.csv
    "dim_date": "DimDate",             # مطابق لـ dim_date.csv
    "dim_plan": "DimPlan",             # مطابق لـ dim_plan.csv
    "fact_subscriptions": "FactSubscriptions" # مطابق لـ fact_subscriptions.csv
}

SCHEMAS = {
    "staging": "dbo",
    "dw": "dbo"
}
