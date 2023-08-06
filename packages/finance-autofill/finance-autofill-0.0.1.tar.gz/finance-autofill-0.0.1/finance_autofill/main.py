from typing import List

import fire
import pandas as pd


def main():
    return fire.Fire(finance_autofill)


def finance_autofill(excel_file: str) -> None:
    """Summarize the transaction records and write them in two new spreadsheets in the same file.
    
    It separates the rows by the `Fee` of 9.02 and 14.04 in two tables. Then, for each table, it groups the rows by the `BillingCompanyName`, counts the number of transactions and sums up the fee. It writes the count and the sum in two rows after the rows of the one `BillingCompanyName`.

    Parameters
    ----------
    excel_file : str
        Path to the excel file to summarize and write to.
    """
    _check_file(excel_file)
    df = _read_spreadsheet(excel_file)
    summarized_dfs = _get_summarized_dfs(df)
    _write_spreadsheet(excel_file, summarized_dfs[0], "ON")
    _write_spreadsheet(excel_file, summarized_dfs[1], "ATL")
    return


def _check_file(excel_file: str) -> None:
    ef = pd.ExcelFile(excel_file)
    ess = ef.sheet_names
    if len(ess) == 0:
        raise ValueError("Emtpy excel file!")
    if "ON" in ess:
        raise ValueError("'ON' already written. Please check if you need to delete it.")
    if "ATL" in ess:
        raise ValueError(
            "'ATL' already written. Please check if you need to delete it."
        )
    return


def _read_spreadsheet(excel_file: str) -> None:
    return pd.read_excel(excel_file, sheet_name=0)


def _write_spreadsheet(excel_file: str, df: pd.DataFrame, sheet_name: str) -> None:
    with pd.ExcelWriter(excel_file, mode="a") as writer:
        df.to_excel(writer, sheet_name, index=False)
    return


def _get_summarized_dfs(df: pd.DataFrame) -> List[pd.DataFrame]:
    summarized_dfs = []
    df1 = df.loc[df["Fee"] == 9.02]
    df2 = df.loc[df["Fee"] == 14.04]
    df1 = _get_summarized_df(df1)
    df2 = _get_summarized_df(df2)
    return [df1, df2]


def _get_summarized_df(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["BillingCompanyName"])
    sub_dfs2 = []
    for name, sub_df in grouped:
        sum_fee = sub_df["Fee"].sum()
        count = sub_df["BillingCompanyName"].count()
        sub_df2 = _compose_new_df(sub_df, sum_fee, count, name)
        sub_dfs2.append(sub_df2)
    return _compose_summarized_df(sub_dfs2)


def _compose_new_df(
    sub_df: pd.DataFrame, sum_fee: float, count: int, name: str
) -> pd.DataFrame:
    columns = sub_df.columns
    rows = pd.DataFrame(dict(zip(columns, [["", ""]] * len(columns))))
    rows.iloc[0][0] = "{} Count".format(name)
    rows.iloc[0][1] = count
    rows.iloc[1][0] = "{} Total".format(name)
    rows.iloc[1][1] = sum_fee
    return pd.concat([sub_df, rows])


def _compose_summarized_df(sub_dfs: List[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(sub_dfs)
