from pathlib import Path

import pandas as pd
import streamlit as st
from pandas.errors import ParserError


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

DATASET_CONFIG = {
    "accounts": {
        "file": "accounts.csv",
        "date_columns": ["renewal_date"],
        "required_columns": [
            "account_id",
            "account_name",
            "owner",
            "region",
            "segment",
            "vertical",
            "strategic_account",
            "partner_involved",
            "account_tier",
            "renewal_date",
        ],
    },
    "opportunities": {
        "file": "opportunities.csv",
        "date_columns": ["close_date", "created_date"],
        "required_columns": [
            "opportunity_id",
            "account_id",
            "opportunity_name",
            "stage",
            "amount",
            "close_date",
            "created_date",
            "status",
        ],
    },
    "activities": {
        "file": "activities.csv",
        "date_columns": ["activity_date"],
        "required_columns": [
            "activity_id",
            "account_id",
            "activity_date",
            "activity_type",
            "summary",
            "owner",
        ],
    },
    "leads": {
        "file": "leads.csv",
        "date_columns": ["lead_date"],
        "required_columns": [
            "lead_id",
            "account_id",
            "lead_date",
            "lead_type",
            "source",
            "campaign",
            "contact_title",
        ],
    },
    "news": {
        "file": "news.csv",
        "date_columns": ["news_date"],
        "required_columns": [
            "news_id",
            "account_id",
            "news_date",
            "headline",
            "summary",
            "sentiment",
            "importance",
        ],
    },
}


def _coerce_booleans(df: pd.DataFrame) -> pd.DataFrame:
    bool_columns = ["strategic_account", "partner_involved"]
    for column in bool_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin({"true", "1", "yes", "y"})
            )
    return df


def _prepare_dataframe(name: str, df: pd.DataFrame) -> pd.DataFrame:
    prepared = df.copy()
    prepared.columns = [column.strip() for column in prepared.columns]
    for column in DATASET_CONFIG[name]["date_columns"]:
        if column in prepared.columns:
            prepared[column] = pd.to_datetime(prepared[column], errors="coerce")

    id_columns = [column for column in prepared.columns if column.endswith("_id")]
    for column in id_columns:
        prepared[column] = prepared[column].astype(str).str.strip()

    return _coerce_booleans(prepared)


def _read_csv(source, source_label: str) -> pd.DataFrame:
    try:
        return pd.read_csv(source)
    except ParserError as exc:
        raise ValueError(
            f"Unable to parse CSV data from {source_label}. "
            "Check for unescaped commas or mismatched quotes in the file."
        ) from exc


@st.cache_data(show_spinner=False)
def load_default_dataset(name: str) -> pd.DataFrame:
    config = DATASET_CONFIG[name]
    source_path = DATA_DIR / config["file"]
    dataframe = _read_csv(source_path, source_path.name)
    return _prepare_dataframe(name, dataframe)


def load_dataset(name: str) -> pd.DataFrame:
    uploaded_datasets = st.session_state.get("uploaded_datasets", {})
    if name in uploaded_datasets:
        return _prepare_dataframe(name, uploaded_datasets[name])
    return load_default_dataset(name)


def load_all_data() -> dict[str, pd.DataFrame]:
    return {name: load_dataset(name) for name in DATASET_CONFIG}


def get_expected_columns(name: str) -> list[str]:
    return DATASET_CONFIG[name]["required_columns"]


def get_dataset_filename(name: str) -> str:
    return DATASET_CONFIG[name]["file"]


def get_dataset_source(name: str) -> str:
    uploaded_datasets = st.session_state.get("uploaded_datasets", {})
    return "Uploaded CSV" if name in uploaded_datasets else "Sample data"


def save_uploaded_dataset(name: str, uploaded_file) -> tuple[pd.DataFrame | None, list[str]]:
    uploaded_file.seek(0)
    dataframe = _read_csv(uploaded_file, uploaded_file.name)
    dataframe = _prepare_dataframe(name, dataframe)
    missing_columns = [
        column
        for column in DATASET_CONFIG[name]["required_columns"]
        if column not in dataframe.columns
    ]
    if missing_columns:
        return None, missing_columns

    uploaded_datasets = st.session_state.setdefault("uploaded_datasets", {})
    uploaded_datasets[name] = dataframe
    return dataframe, []


def reset_uploaded_dataset(name: str) -> None:
    uploaded_datasets = st.session_state.setdefault("uploaded_datasets", {})
    uploaded_datasets.pop(name, None)
