import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from config import SQL_CONFIG, TABLE_MAPPING, SCHEMAS
import os

class ETLReporter:
    def __init__(self):
        self.config = SQL_CONFIG
        conn_url = (
            f"mssql+pyodbc://@{self.config['server']}/"
            f"{self.config['database']}?"
            f"driver={self.config['driver']}&trusted_connection=yes"
        )
        self.engine = create_engine(conn_url)

    def generate_report(self):
        report_data = []
        schema = SCHEMAS["staging"]

        print("📊 Fetching live row counts from SQL Server...")

        for file_key, table_name in TABLE_MAPPING.items():
            try:
                # سؤال السيكوال مباشرة عن عدد الصفوف
                query = text(f"SELECT COUNT(*) FROM [{schema}].[{table_name}]")
                with self.engine.connect() as conn:
                    count = conn.execute(query).scalar()
                
                report_data.append({
                    "Execution_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Target_Table": table_name,
                    "Status": "Success",
                    "Rows_Loaded": count, # هذا هو العدد الحقيقي
                    "Remarks": "Verified from Database"
                })
            except Exception as e:
                report_data.append({
                    "Execution_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Target_Table": table_name,
                    "Status": "Failed",
                    "Rows_Loaded": 0,
                    "Remarks": str(e)[:50]
                })

        # حفظ التقرير في مجلد reports
        df_report = pd.DataFrame(report_data)
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/etl_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_report.to_csv(filename, index=False)
        print(f"✅ Report generated: {filename}")

if __name__ == "__main__":
    reporter = ETLReporter()
    reporter.generate_report()