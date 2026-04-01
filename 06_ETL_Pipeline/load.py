import pandas as pd
import logging
import warnings
from sqlalchemy import create_engine, text
from config import SQL_CONFIG, TABLE_MAPPING, SCHEMAS, BASE_PATH
from pathlib import Path

# تعطيل تحذيرات إصدار السيرفر
warnings.filterwarnings('ignore', category=UserWarning)

# إعداد الـ Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("LOAD_LAYER")

class DataLoader:
    def __init__(self):
        self.config = SQL_CONFIG
        self.base_path = Path(BASE_PATH).parent / "Processed"
        
        conn_url = (
            f"mssql+pyodbc://@{self.config['server']}/"
            f"{self.config['database']}?"
            f"driver={self.config['driver']}&trusted_connection=yes"
        )
        self.engine = create_engine(conn_url)

    def clear_database_tables(self):
        """مسح الجداول المتغيرة فقط لتجنب أخطاء العلاقات مع الجداول الثابتة"""
        try:
            with self.engine.begin() as conn:
                logger.info("🧹 STARTING GLOBAL CLEANUP...")
                # مسح الجداول بالترتيب الصحيح (الفاكت أولاً)
                conn.execute(text("DELETE FROM dbo.FactSubscriptions"))
                conn.execute(text("DELETE FROM dbo.DimCompany"))
                conn.execute(text("DELETE FROM dbo.DimPlan"))
                # ملاحظة: لم نمسح DimDate لأنه جدول مرجعي ثابت ويسبب مشاكل في الـ Foreign Keys
                logger.info("✅ Variable tables cleaned successfully.")
        except Exception as e:
            logger.error(f"💥 FAILED to clean database: {str(e)[:100]}")
            raise e

    def load_all(self):
        print("\n" + "="*60)
        logger.info("🚀 STARTING DATABASE LOAD PROCESS")
        print("="*60)

        # 1. تنظيف الجداول الأساسية قبل الرفع
        self.clear_database_tables()

        # 2. تحميل البيانات من المجلد المعالج (Processed)
        for file_key, table_name in TABLE_MAPPING.items():
            
            # --- إضافة استثناء لجدول التاريخ ---
            if table_name == "DimDate":
                logger.info(f"⏭️ Skipping {table_name}: Static table already exists.")
                continue

            csv_path = self.base_path / f"{file_key}.csv"
            
            if not csv_path.exists():
                logger.error(f"❌ File missing: {file_key}.csv")
                continue

            try:
                df = pd.read_csv(csv_path)
                with self.engine.begin() as conn:
                    logger.info(f"📤 Uploading {len(df)} rows to {table_name}...")
                    df.to_sql(
                        name=table_name, 
                        con=conn, 
                        schema="dbo", 
                        if_exists="append", # نستخدم append لأننا مسحنا البيانات بـ DELETE
                        index=False
                    )
                logger.info(f"✅ SUCCESS: {table_name} updated.")
            except Exception as e:
                logger.error(f"💥 FAILED to load {table_name}: {str(e)[:100]}")

        print("="*60)
        logger.info("🏁 ALL DYNAMIC TABLES LOADED SUCCESSFULLY")
        print("="*60 + "\n")

if __name__ == "__main__":
    loader = DataLoader()
    loader.load_all()