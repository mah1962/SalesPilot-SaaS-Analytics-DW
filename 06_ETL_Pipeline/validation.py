import pandas as pd
import logging
import pyodbc
from typing import Dict
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


class DataValidator:

    def __init__(self, data: Dict[str, pd.DataFrame]):
        self.data = data

    # =========================================
    # 🔹 Generic Checks
    # =========================================
    def _check_empty(self, df: pd.DataFrame, name: str):
        if df.empty:
            raise ValueError(f"{name} is empty ❌")

    def _check_nulls(self, df: pd.DataFrame, cols: list, name: str):
        for col in cols:
            if col in df.columns and df[col].isnull().any():
                raise ValueError(f"{name}: Column {col} contains NULL ❌")

    def _check_duplicates(self, df: pd.DataFrame, subset: list, name: str):
        if all(col in df.columns for col in subset):
            if df.duplicated(subset=subset).any():
                raise ValueError(f"{name}: Duplicate records found ❌")

    def _check_negative(self, df: pd.DataFrame, cols: list, name: str):
        for col in cols:
            if col in df.columns and (df[col] < 0).any():
                raise ValueError(f"{name}: Negative value in {col} ❌")

    # =========================================
    # 🔹 Fact Validation
    # =========================================
    def _validate_facsubscriptions(self, df: pd.DataFrame):
        name = "FacSubscriptions"
        logger.info(f"Validating {name}")

        self._check_empty(df, name)
        self._check_nulls(df, ["SubscriptionID", "CompanyID", "PlanID"], name)
        self._check_duplicates(df, ["SubscriptionID", "SnapshotDateKey"], name)
        self._check_negative(df, ["MRR_Amount", "ActiveUsers"], name)

    # =========================================
    # 🔹 Dim Validation
    # =========================================
    def _validate_dimdate(self, df: pd.DataFrame):
        name = "DimDate"
        logger.info(f"Validating {name}")

        self._check_empty(df, name)
        self._check_duplicates(df, ["DateKey"], name)

    def _validate_dimplan(self, df: pd.DataFrame):
        name = "DimPlan"
        logger.info(f"Validating {name}")

        self._check_empty(df, name)
        self._check_duplicates(df, ["PlanID"], name)

    def _validate_dimcompany(self, df: pd.DataFrame):
        name = "DimCompany"
        logger.info(f"Validating {name}")

        self._check_empty(df, name)
        self._check_duplicates(df, ["CompanyID"], name)

    # =========================================
    # 🔹 Main Validation
    # =========================================
    def validate(self):
        logger.info("🚀 Starting Validation Layer")

        for name, df in self.data.items():

            if name == "fact_subscriptions":
                self._validate_facsubscriptions(df)

            elif name == "dim_date":
                self._validate_dimdate(df)

            elif name == "dim_plan":
                self._validate_dimplan(df)

            elif name == "dim_company":
                self._validate_dimcompany(df)

            else:
                logger.warning(f"No validation rules for {name}")

        logger.info("✅ Validation passed successfully")

if __name__ == "__main__":
    from extract import DataExtractor
    from transform import DataTransformer
    from config import BASE_PATH

    # Extract
    extractor = DataExtractor(base_path=BASE_PATH)
    raw_data = extractor.extract_all()

    # Transform
    transformer = DataTransformer(raw_data)
    transformed_data = transformer.transform()

    # Validate
    validator = DataValidator(transformed_data)
    validator.validate()

    print("✅ Validation Finished Successfully")