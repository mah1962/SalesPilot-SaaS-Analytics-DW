import pandas as pd
from pathlib import Path
import logging
import pyodbc
from typing import Dict
from config import BASE_PATH
from config import SCHEMAS
SCHEMAS = {
    "staging": "Staging",
    "dw": "SaaS_DW"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class DataExtractor:

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

        if not self.base_path.exists():
            raise FileNotFoundError(f"Base_path does not exist: {self.base_path}")

    def _read_csv(self, file_path: Path) -> pd.DataFrame:
        """ Read a single csv file with error handling """
        try:
            df = pd.read_csv(file_path)

            logging.info(
                f"Loaded {file_path.name} | Rows: {len(df)} | Columns: {len(df.columns)}"
            )

            return df

        except pd.errors.EmptyDataError:
            logging.warning(f"{file_path.name} is Empty")
            return pd.DataFrame()

        except Exception as e:
            logging.error(f"Error reading {file_path.name}: {str(e)}")
            raise

    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """ Extract all csv files dynamically """
        data = {}

        csv_files = list(self.base_path.glob("*.csv"))

        if not csv_files:
            logging.warning("No csv files found in directory")

        for file in csv_files:
            key = file.stem
            data[key] = self._read_csv(file)

        logging.info(f"Extraction completed | Total datasets: {len(data)}")

        return data

    def extract_specific(self, files: list) -> Dict[str, pd.DataFrame]:
        """ Extract only specific files """
        data = {}

        for file_name in files:
            file_path = self.base_path / file_name

            if not file_path.exists():
                logging.warning(f"File not found: {file_name}")
                continue

            key = Path(file_name).stem.lower()
            data[key] = self._read_csv(file_path)

        logging.info(f"Extraction completed | Total datasets: {len(data)}")

        return data


# 🚀 Run
if __name__ == "__main__":

    extractor = DataExtractor(base_path=BASE_PATH)

    data = extractor.extract_all()

    for name, df in data.items():
        print(f"\n{name}")
        print(df.head())