import streamlit as st

from src.data_loader import (
    DATASET_CONFIG,
    get_dataset_filename,
    get_dataset_source,
    get_expected_columns,
    reset_uploaded_dataset,
    save_uploaded_dataset,
)
from src.styles import apply_theme, render_callout, render_hero, render_section_header


st.set_page_config(page_title="CSV Upload", layout="wide")
apply_theme()


def build_sidebar() -> None:
    st.sidebar.title("Media AE cockpit")
    st.sidebar.caption("Upload CSVs that match the sample schemas to replace the default demo data.")
    source_lines = [
        f"- {dataset_name.title()}: {get_dataset_source(dataset_name)}"
        for dataset_name in DATASET_CONFIG
    ]
    st.sidebar.markdown("\n".join(source_lines))
    st.sidebar.divider()
    st.sidebar.page_link("app.py", label="Home dashboard")
    st.sidebar.page_link("pages/1_Account_Prioritization.py", label="Account prioritization")
    st.sidebar.page_link("pages/2_Daily_Actions.py", label="Daily actions")
    st.sidebar.page_link("pages/3_Account_Detail.py", label="Account detail")
    st.sidebar.page_link("pages/4_CSV_Upload.py", label="CSV upload")


build_sidebar()

render_hero(
    "CSV upload",
    "Replace any sample dataset with your own CSVs. Uploaded data is stored in the current Streamlit session and immediately powers the cockpit across all pages.",
)
render_callout(
    "Use the sample files in the data directory as templates. Each uploaded CSV must preserve the expected column names shown below."
)

dataset_names = list(DATASET_CONFIG.keys())
for dataset_name in dataset_names:
    render_section_header(
        dataset_name.title(),
        f"Current source: {get_dataset_source(dataset_name)} | Default file: {get_dataset_filename(dataset_name)}",
    )
    with st.expander(f"{dataset_name.title()} schema and upload controls", expanded=True):
        st.markdown("**Expected columns**")
        st.code(", ".join(get_expected_columns(dataset_name)))

        upload_col, reset_col = st.columns([2.5, 1])
        with upload_col:
            uploaded_file = st.file_uploader(
                f"Upload {dataset_name}.csv",
                type=["csv"],
                key=f"upload_{dataset_name}",
            )
            if uploaded_file is not None:
                dataframe, missing_columns = save_uploaded_dataset(dataset_name, uploaded_file)
                if missing_columns:
                    st.error(
                        "Upload failed. Missing columns: "
                        + ", ".join(missing_columns)
                    )
                else:
                    st.success(f"{dataset_name.title()} uploaded successfully.")
                    st.dataframe(dataframe.head(8), hide_index=True, use_container_width=True)

        with reset_col:
            st.markdown(" ")
            if st.button(f"Reset {dataset_name}", key=f"reset_{dataset_name}"):
                reset_uploaded_dataset(dataset_name)
                st.success(f"{dataset_name.title()} reset to sample data.")

