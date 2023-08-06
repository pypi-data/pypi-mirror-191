from pathlib import Path

import pandas as pd

from finance_autofill.main import finance_autofill


def _create_test_files(dir_name: str) -> str:
    df = pd.DataFrame(
        {
            "InsuranceCompanyName": ["Aetna", "Delta Dental", "Aetna", "Aetna"],
            "BillingCompanyName": ["Pornhub", "Bilibili", "Bilibili", "Pornhub"],
            "BillingProvince": ["Jilin", "Jilin", "Hainan", "Hainan"],
            "Fee": [9.02, 14.04, 9.02, 9.02],
        }
    )
    file_name = Path(dir_name).joinpath("insurance-records.xlsx")
    df.to_excel(str(file_name), engine="openpyxl", index=False)
    return file_name


def test_finance_autofill(tmp_path: Path):
    input_file = _create_test_files(str(tmp_path))
    return finance_autofill(input_file)
