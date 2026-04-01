import pandas as pd
import logging
from typing import Dict
from pathlib import Path

from config import BASE_PATH
from config import TABLE_MAPPING
from config import SCHEMAS

# =========================================
# 🔹 Logging
# =========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.data = data

    # =========================================
    # 🔹 Generic Cleaning
    # =========================================
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.strip()
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()

    # =========================================
    # 🔹 Fact Cleaning
    # =========================================
    def _clean_facsubscriptions(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Cleaning FactSubscriptions")

        df = self._standardize_columns(df)

        required_cols = ["SubscriptionID", "CompanyID", "PlanID", "SnapshotDateKey"]

        existing_cols = [col for col in required_cols if col in df.columns]
        if existing_cols:
            df = df.dropna(subset=existing_cols)

        if "SnapshotDateKey" in df.columns:
            df["SnapshotDateKey"] = pd.to_numeric(df["SnapshotDateKey"], errors="coerce")

        numeric_cols = ["ActiveUsers", "MRR_Amount"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        flag_cols = ["IsActive", "IsChurned", "IsUpgrade", "IsDowngrade"]
        for col in flag_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(int)

        if "SubscriptionID" in df.columns and "SnapshotDateKey" in df.columns:
            df = df.drop_duplicates(subset=["SubscriptionID", "SnapshotDateKey"])

        if "CompanyID" in df.columns and "SnapshotDateKey" in df.columns:
            df = df.sort_values(by=["CompanyID", "SnapshotDateKey"])

        logger.info(f"FactSubscriptions cleaned | Rows: {len(df)}")

        return df

    # =========================================
    # 🔹 DimDate Cleaning
    # =========================================
    def _clean_dimdate(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Cleaning DimDate")

        df = self._standardize_columns(df)
        df = self._remove_duplicates(df)

        if "DateKey" in df.columns:
            df["DateKey"] = pd.to_numeric(df["DateKey"], errors="coerce")

        if "FullDate" in df.columns:
            df["FullDate"] = pd.to_datetime(df["FullDate"], errors="coerce")

        return df

    # =========================================
    # 🔹 DimPlan Cleaning
    # =========================================
    def _clean_dimplan(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Cleaning DimPlan")

        df = self._standardize_columns(df)
        df = self._remove_duplicates(df)

        numeric_cols = ["BasePrice", "UserFee", "TierLevel"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    # =========================================
    # 🔹 DimCompany Cleaning
    # =========================================
    def _clean_dimcompany(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Cleaning DimCompany")

        df = self._standardize_columns(df)
        df = self._remove_duplicates(df)

        if "SignupDateKey" in df.columns:
            df["SignupDateKey"] = pd.to_numeric(df["SignupDateKey"], errors="coerce")

        return df

    # =========================================
    # 🔹 Main Transform
    # =========================================
    def transform(self) -> Dict[str, pd.DataFrame]:
        logger.info("🚀 Starting Transformation Layer")

        transformed_data = {}

        for name, df in self.data.items():

            if df is None or df.empty:
                logger.warning(f"Skipping empty dataset: {name}")
                continue

            if name == "fact_subscriptions":
                cleaned_df = self._clean_facsubscriptions(df)

            elif name == "dim_date":
                cleaned_df = self._clean_dimdate(df)

            elif name == "dim_plan":
                cleaned_df = self._clean_dimplan(df)

            elif name == "dim_company":  # ✅ FIXED
                cleaned_df = self._clean_dimcompany(df)

            else:
                logger.warning(f"Unknown dataset skipped: {name}")
                continue

            transformed_data[name] = cleaned_df

        logger.info("✅ Transformation completed successfully")

        return transformed_data


# =========================================
# 🚀 Run Pipeline
# =========================================
if __name__ == "__main__":
    from extract import DataExtractor

    extractor = DataExtractor(base_path=BASE_PATH)
    data = extractor.extract_all()

    transformer = DataTransformer(data)
    transformed_data = transformer.transform()

    # =========================================
    # 💾 Save Processed Layer
    # =========================================
    processed_path = Path(BASE_PATH).parent / "Processed"
    processed_path.mkdir(parents=True, exist_ok=True)

    for name, df in transformed_data.items():
        file_path = processed_path / f"{name}.csv"
        df.to_csv(file_path, index=False)
        logger.info(f"✅ Saved: {file_path}")

    # Debug
    for name, df in transformed_data.items():
        print(f"\n{name} | Rows: {len(df)}")
        print(df.head())