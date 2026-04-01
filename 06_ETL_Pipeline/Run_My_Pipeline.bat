@echo off
:: الدخول للمسار باستخدام علامات تنصيص لضمان قراءة المسافات
cd /d "D:\SQL\TRAINING PROJECTS\SalesPilot_SaaS Analytics Data Warehouse\SaaS-Sales-Analytics\06_ETL_Pipeline"

echo 🚀 Starting ETL Pipeline...

:: تغيير الاسم لـ pipeline.py لأنه الاسم الموجود في مجلدك
python pipeline.py

echo ---------------------------------------------------
echo 🏁 Finished.
pause