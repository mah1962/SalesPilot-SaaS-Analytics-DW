import logging
import time
import os
import requests
import sys
from datetime import datetime
from pathlib import Path

# استيراد المكونات
from config import BASE_PATH
from extract import DataExtractor
from transform import DataTransformer
from validation import DataValidator
from load import DataLoader
from etl_report import ETLReporter

# --- 1. تحديد المسارات المطلقة ---
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "Logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

current_date = datetime.now().strftime('%Y-%m-%d')
log_file = os.path.join(log_dir, f"pipeline_execution_{current_date}.log")

# --- 2. إعدادات الـ Logging (نسخة الإجبار الفوري) ---
# تنظيف أي إعدادات سابقة قد تسبب تعارض
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# إعداد الـ Logger الرئيسي
logger = logging.getLogger("ETL_ORCHESTRATOR")
logger.setLevel(logging.INFO)

# 1. الملحق الخاص بالملف (File Handler) - مع إجبار التحديث اللحظي
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | 🚀 %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# 2. الملحق الخاص بالشاشة (Console Handler)
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter("%(asctime)s | %(levelname)s | 🚀 %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# --- 3. بيانات تليجرام ---
TELEGRAM_TOKEN = "8730409837:AAEFLIiQRr_1651mQo_FTQM5Qi3LAKNAweg"
CHAT_ID = "7656351623"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception:
        pass

def run_full_pipeline():
    start_time = time.time()
    logger.info("Starting Full SaaS Analytics ETL Pipeline")
    
    try:
        # Step 1: Extract
        logger.info("Step 1: Extracting Raw CSV Files...")
        extractor = DataExtractor(base_path=BASE_PATH)
        raw_data = extractor.extract_all()
        
        # Step 2: Transform
        logger.info("Step 2: Transforming Data...")
        transformer = DataTransformer(raw_data)
        transformed_data = transformer.transform()
        
        # Step 3: Validate
        logger.info("Step 3: Validating Transformed Data...")
        validator = DataValidator(transformed_data)
        validator.validate()
        
        # Step 4: Save Processed
        processed_path = BASE_PATH.parent / "Processed"
        processed_path.mkdir(parents=True, exist_ok=True)
        for name, df in transformed_data.items():
            df.to_csv(processed_path / f"{name}.csv", index=False)
        logger.info(f"✅ Transformed data saved to: {processed_path}")

        # Step 5: Load
        logger.info("Step 4: Clearing SQL Tables & Loading New Data...")
        loader = DataLoader()
        loader.load_all()
        
        # Step 6: Report
        logger.info("Step 5: Generating Final ETL Audit Report...")
        reporter = ETLReporter()
        reporter.generate_report()

        duration = round(time.time() - start_time, 2)
        logger.info(f"🏁 PIPELINE FINISHED SUCCESSFULLY in {duration} seconds!")

    except Exception as e:
        error_msg = f"❌ PIPELINE FAILED! Error Details: {str(e)}"
        logger.error(error_msg)
        send_telegram_alert(error_msg)
        raise

if __name__ == "__main__":
    run_full_pipeline()