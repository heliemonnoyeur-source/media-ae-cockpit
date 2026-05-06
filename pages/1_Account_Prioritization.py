import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import DATASET_CONFIG, get_dataset_source, load_all_data
from src.formatters import format_currency, format_date
from src.scoring import build_account_summary
from src.styles import apply_theme, render_callout, render_hero, render_section_header


st.set_page_config(page_title="Account Prioritization", layout="wide")
apply_theme()


def build_sidebar() -> None:
    st.sidebar.title("Media AE cockpit")
    st.sidebar.caption("Use the filters on this page to reshape the ranked account list.")
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
data = load_all_data()
summary = build_account_summary(data)

render_hero(
    "Account prioritization",
    "Sort the book by urgency, pipeline quality, demand momentum, activity gaps, and strategic context so the highest-leverage accounts stay in focus.",
)

left_filters, right_filters = st.columns([1.2, 2.4])
with left_filters:
    owner_options = ["All"] + sorted(summary["owner"].dropna().unique().tolist())
    bucket_options = ["All"] + ["Critical", "High", "Medium", "Monitor"]
    strategic_only = st.checkbox("Strategic accounts only")
    selected_owner = st.selectbox("Owner", owner_options)
    selected_bucket = st.selectbox("Priority bucket", bucket_options)

with right_filters:
    pipeline_bounds = (
        float(summary["pipeline_amount"].min()),
        float(summary["pipeline_amount"].max()),
    )
    pipeline_filter = st.slider(
        "Pipeline amount",
        min_value=float(pipeline_bounds[0]),
        max_value=float(pipeline_bounds[1]),
        value=(float(pipeline_bounds[0]), float(pipeline_bounds[1])),
        step=100_000.0,
    )
    days_filter = st.slider(
        "Days since last activity",
        min_value=0,
        max_value=int(summary["days_since_activity"].max()),
        value=(0, int(summary["days_since_activity"].max())),
    )

filtered = summary.copy()
filtered = filtered[
    filtered["pipeline_amount"].between(pipeline_filter[0], pipeline_filter[1])
    & filtered["days_since_activity"].between(days_filter[0], days_filter[1])
]
if strategic_only:
    filtered = filtered[filtered["strategic_account"]]
if selected_owner != "All":
    filtered = filtered[filtered["owner"] == selected_owner]
if selected_bucket != "All":
    filtered = filtered[filtered["priority_bucket"] == selected_bucket]

if filtered.empty:
    st.warning("No accounts match the selected filters.")
    st.stop()

top_row = filtered.iloc[0]
render_callout(
    f"Current top account in this filtered view: {top_row['account_name']} ({top_row['priority_score']:.1f}). "
    f"Next best action: {top_row['next_best_action']}"
)

rank_cols = st.columns([1.15, 1])
with rank_cols[0]:
    render_section_header(
        "Ranked account list",
        "Use this table to identify which accounts deserve attention first and why they surfaced.",
    )
    table = filtered[
        [
            "priority_rank",
            "account_name",
            "owner",
            "priority_bucket",
            "priority_score",
            "pipeline_amount",
            "highest_stage",
            "sql_6m",
            "mql_6m",
            "days_since_activity",
            "top_driver",
            "action_category",
        ]
    ].copy()
    table["priority_score"] = table["priority_score"].round(1)
    table["pipeline_amount"] = table["pipeline_amount"].map(format_currency)
    table = table.rename(
        columns={
            "priority_rank": "Rank",
            "account_name": "Account",
            "owner": "Owner",
            "priority_bucket": "Bucket",
            "priority_score": "Score",
            "pipeline_amount": "Pipeline",
            "highest_stage": "Top stage",
            "sql_6m": "SQLs (6m)",
            "mql_6m": "MQLs (6m)",
            "days_since_activity": "Days since activity",
            "top_driver": "Top driver",
            "action_category": "Action theme",
        }
    )
    st.dataframe(table, hide_index=True, use_container_width=True)

with rank_cols[1]:
    render_section_header(
        "Score mix by account",
        "Compare the filtered accounts on total score to see where concentration is highest.",
    )
    score_chart = px.bar(
        filtered.sort_values("priority_score", ascending=True).tail(12),
        x="priority_score",
        y="account_name",
        color="priority_bucket",
        orientation="h",
        color_discrete_map={
            "Critical": "#f97316",
            "High": "#f59e0b",
            "Medium": "#38bdf8",
            "Monitor": "#22c55e",
        },
        labels={"priority_score": "Priority score", "account_name": "Account"},
    )
    score_chart.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        legend_title_text="Bucket",
    )
    st.plotly_chart(score_chart, use_container_width=True)

render_section_header(
    "Selected account spotlight",
    "Use the selector to review why a specific account is ranked where it is.",
)
account_choice = st.selectbox(
    "Choose an account",
    filtered["account_name"].tolist(),
    index=0,
)
spotlight = filtered.loc[filtered["account_name"] == account_choice].iloc[0]

spotlight_cols = st.columns(4)
spotlight_cols[0].metric("Priority score", f"{spotlight['priority_score']:.1f}")
spotlight_cols[1].metric("Pipeline", format_currency(spotlight["pipeline_amount"]))
spotlight_cols[2].metric("SQLs / MQLs", f"{int(spotlight['sql_6m'])} / {int(spotlight['mql_6m'])}")
spotlight_cols[3].metric("Last activity", format_date(spotlight["last_activity_date"]))

st.markdown(
    f"""
    **Recommended move:** {spotlight['next_best_action']}

    **Why it surfaced:** {spotlight['top_driver']} | Top stage: {spotlight['highest_stage']} | Action theme: {spotlight['action_category']}
    """
)
