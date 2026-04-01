import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

# ===============================
# CONFIG
# ===============================
START_YEAR = 2022
END_YEAR = 2026
NUM_COMPANIES = 250

# تأكد أن هذا المسار صحيح في جهازك
OUTPUT_PATH = r"D:\SQL\TRAINING PROJECTS\SalesPilot_SaaS Analytics Data Warehouse\SaaS-Sales-Analytics\01_Data\Raw"

COUNTRIES = ["USA", "UK", "Germany", "UAE", "Egypt"]
INDUSTRIES = ["FinTech", "HealthTech", "EdTech", "E-commerce", "Logistics"]
ACQ_CHANNELS = ["Paid Ads", "Organic", "Referral", "Partner", "Outbound Sales"]

def save_data(dim_plan, dim_date, dim_company, fact_subscriptions):
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        print(f"📁 Created directory: {OUTPUT_PATH}")

    files = ["dim_plan.csv", "dim_date.csv", "dim_company.csv", "fact_subscriptions.csv"]

    # حذف الملفات القديمة لتجنب تداخل البيانات
    for f in files:
        full_path = os.path.join(OUTPUT_PATH, f)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                print(f"⚠️ Could not delete {f}: {e}")

    print("🗑️ Old files cleaned up")

    # حفظ الملفات الجديدة
    dim_plan.to_csv(os.path.join(OUTPUT_PATH, "dim_plan.csv"), index=False)
    dim_date.to_csv(os.path.join(OUTPUT_PATH, "dim_date.csv"), index=False)
    dim_company.to_csv(os.path.join(OUTPUT_PATH, "dim_company.csv"), index=False)
    fact_subscriptions.to_csv(os.path.join(OUTPUT_PATH, "fact_subscriptions.csv"), index=False)
    
    print(f"💾 Data saved successfully to: {OUTPUT_PATH}")

# ===============================
# GENERATION FUNCTIONS
# ===============================

def generate_dim_plan():
    plans = [
        (1, "Starter", 49, 5, "Monthly", 1),
        (2, "Growth", 99, 10, "Monthly", 2),
        (3, "Pro", 199, 20, "Monthly", 3),
        (4, "Enterprise", 499, 35, "Annual", 4),
    ]
    return pd.DataFrame(plans, columns=["PlanID", "PlanName", "BasePrice", "UserFee", "BillingCycle", "TierLevel"])

def generate_dim_date():
    dates = pd.date_range(start=f"{START_YEAR}-01-01", end=f"{END_YEAR}-12-31", freq="MS")
    df = pd.DataFrame()
    df["FullDate"] = dates
    df["DateKey"] = df["FullDate"].dt.strftime("%Y%m%d").astype(int)
    df["Day"] = df["FullDate"].dt.day
    df["Month"] = df["FullDate"].dt.month
    df["MonthName"] = df["FullDate"].dt.month_name()
    df["Quarter"] = df["FullDate"].dt.quarter
    df["Year"] = df["FullDate"].dt.year
    df["WeekNumber"] = df["FullDate"].dt.isocalendar().week
    return df

def generate_dim_company():
    companies = []
    size_distribution = ["SMB"]*150 + ["Mid-Market"]*75 + ["Enterprise"]*25
    for i in range(1, NUM_COMPANIES + 1):
        size = random.choice(size_distribution)
        signup_year = random.randint(START_YEAR, 2025)
        signup_month = random.randint(1, 12)
        signup_date = datetime(signup_year, signup_month, 1)
        signup_key = int(signup_date.strftime("%Y%m%d"))
        
        companies.append([i, f"Company_{i}", random.choice(INDUSTRIES), random.choice(COUNTRIES), 
                          size, random.choice(ACQ_CHANNELS), signup_key])
    
    return pd.DataFrame(companies, columns=["CompanyID","CompanyName","Industry","Country",
                                            "CompanySize","AcquisitionChannel","SignupDateKey"])

def generate_fact_subscriptions(dim_company, dim_plan, dim_date):
    records = []
    sub_id = 1
    for _, comp in dim_company.iterrows():
        start_key = comp["SignupDateKey"]
        churn_prob = 0.04 if comp["CompanySize"] == "SMB" else 0.02 if comp["CompanySize"] == "Mid-Market" else 0.01
        active_plan = random.randint(1, 3)
        is_churned_flag = False

        # القفل المنطقي: النشاط يبدأ فقط من تاريخ الاشتراك
        active_periods = dim_date[dim_date["DateKey"] >= start_key]
        
        for _, d_row in active_periods.iterrows():
            if is_churned_flag: break
            
            status_active = 1
            status_churn = 0
            if random.random() < churn_prob:
                status_active = 0
                status_churn = 1
                is_churned_flag = True

            plan_info = dim_plan[dim_plan["PlanID"] == active_plan].iloc[0]
            users = random.randint(5, 500) # تبسيط لعدد المستخدمين
            mrr = plan_info["BasePrice"] + (users * plan_info["UserFee"])

            records.append([sub_id, comp["CompanyID"], active_plan, d_row["DateKey"], 
                            users, round(mrr, 2), status_active, status_churn, 0, 0])
            sub_id += 1
            
    return pd.DataFrame(records, columns=["SubscriptionID","CompanyID","PlanID","SnapshotDateKey",
                                          "ActiveUsers","MRR_Amount","IsActive","IsChurned",
                                          "IsUpgrade","IsDowngrade"])

# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    try:
        print("🚀 Starting Data Generation Process...")
        
        d_plan = generate_dim_plan()
        d_date = generate_dim_date()
        d_comp = generate_dim_company()
        print(f"✅ Dimensions Created ({len(d_comp)} companies)")

        f_subs = generate_fact_subscriptions(d_comp, d_plan, d_date)
        print(f"✅ Fact Table Created ({len(f_subs)} records)")

        save_data(d_plan, d_date, d_comp, f_subs)
        
        print("🏁 All steps completed successfully!")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")