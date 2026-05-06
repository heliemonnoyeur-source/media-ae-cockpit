import pandas as pd


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_integer(value: float | int) -> str:
    return f"{int(value):,}"


def format_date(value) -> str:
    if pd.isna(value):
        return "N/A"
    return pd.to_datetime(value).strftime("%b %d, %Y")
