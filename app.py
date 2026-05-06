import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import DATASET_CONFIG, get_dataset_source, load_all_data
from src.formatters import format_currency, format_date, format_integer
from src.scoring import (
    build_account_summary,
    daily_action_queue,
    monthly_lead_summary,
    recent_activity_feed,
    recent_news_feed,
    stage_pipeline_summary,
)
from src.styles import apply_theme, render_callout, render_hero, render_metric_card, render_news_item, render_section_header


st.set_page_config(page_title="Media AE Sales Cockpit", layout="wide")
apply_theme()


def build_sidebar() -> None:
    st.sidebar.title("Media AE cockpit")
    st.sidebar.caption("Sample data is loaded by default. Upload your own CSVs from the CSV Upload page.")
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


def styled_priority_table(summary: pd.DataFrame) -> pd.DataFrame:
    table = summary.copy()
    table["Priority score"] = table["priority_score"].round(1)
    table["Pipeline"] = table["pipeline_amount"].map(format_currency)
    table["Last activity"] = table["last_activity_date"].map(format_date)
    table["Account"] = table["account_name"]
    table["Action"] = table["action_category"]
    return table[
        [
            "priority_rank",
            "Account",
            "Priority score",
            "priority_bucket",
            "Pipeline",
            "highest_stage",
            "sql_6m",
            "mql_6m",
            "Last activity",
            "Action",
        ]
    ].rename(
        columns={
            "priority_rank": "Rank",
            "priority_bucket": "Bucket",
            "highest_stage": "Top stage",
            "sql_6m": "SQLs (6m)",
            "mql_6m": "MQLs (6m)",
        }
    )


build_sidebar()
data = load_all_data()
summary = build_account_summary(data)
stage_summary = stage_pipeline_summary(data)
lead_summary = monthly_lead_summary(data)
activity_feed = recent_activity_feed(data, limit=8)
news_feed = recent_news_feed(data, limit=6)
action_queue = daily_action_queue(summary, limit=6)

top_account = summary.iloc[0]
critical_count = int((summary["priority_bucket"] == "Critical").sum())

render_hero(
    "Enterprise Media Sales Cockpit",
    "Prioritize the right media accounts, spot dormant pipeline, and focus each day on the next best actions most likely to move revenue.",
)
render_callout(
    f"Today's top account is {top_account['account_name']} with a score of {top_account['priority_score']:.1f}. "
    f"Primary driver: {top_account['top_driver']}. Recommended move: {top_account['action_category']}."
)

metric_cols = st.columns(4)
with metric_cols[0]:
    render_metric_card(
        "Open pipeline",
        format_currency(summary["pipeline_amount"].sum()),
        f"{format_integer(summary['open_opps'].sum())} open opportunities across the vertical",
    )
with metric_cols[1]:
    render_metric_card(
        "SQLs in last 6 months",
        format_integer(summary["sql_6m"].sum()),
        "Sales qualified activity across demand sources",
    )
with metric_cols[2]:
    render_metric_card(
        "MQLs in last 6 months",
        format_integer(summary["mql_6m"].sum()),
        "Recent marketing engagement ready for multithreading",
    )
with metric_cols[3]:
    render_metric_card(
        "Accounts needing focus",
        format_integer(critical_count),
        "Accounts currently ranked as critical",
    )

chart_cols = st.columns(2)
with chart_cols[0]:
    render_section_header("Pipeline overview", "Open opportunities and pipeline amount by stage.")
    stage_chart = px.bar(
        stage_summary,
        x="stage",
        y="pipeline_amount",
        color="open_opps",
        text_auto=".2s",
        color_continuous_scale="Blues",
        labels={"stage": "Stage", "pipeline_amount": "Pipeline", "open_opps": "Open opps"},
    )
    stage_chart.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
    )
    stage_chart.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(stage_chart, use_container_width=True)

with chart_cols[1]:
    render_section_header("Demand trend", "SQLs and MQLs generated over the last 6 months.")
    lead_chart = px.line(
        lead_summary,
        x="month",
        y="count",
        color="lead_type",
        markers=True,
        color_discrete_map={"SQL": "#38bdf8", "MQL": "#818cf8"},
        labels={"month": "Month", "count": "Volume", "lead_type": "Lead type"},
    )
    lead_chart.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
    )
    st.plotly_chart(lead_chart, use_container_width=True)

feed_cols = st.columns([1.15, 1])
with feed_cols[0]:
    render_section_header("Recent account activity", "Latest meetings, calls, and follow-up notes across the book.")
    activity_table = activity_feed.copy()
    activity_table["activity_date"] = activity_table["activity_date"].map(format_date)
    activity_table = activity_table.rename(
        columns={
            "activity_date": "Date",
            "account_name": "Account",
            "activity_type": "Type",
            "summary": "Summary",
            "owner": "Owner",
        }
    )
    st.dataframe(activity_table, hide_index=True, use_container_width=True)

with feed_cols[1]:
    render_section_header("Recent company news", "News triggers worth using in outreach and account planning.")
    if news_feed.empty:
        st.info("No recent news records are available in the current dataset.")
    else:
        for row in news_feed.itertuples():
            render_news_item(
                row.headline,
                f"{row.account_name} | {format_date(row.news_date)} | {row.importance} importance",
                row.summary,
            )

bottom_cols = st.columns([1.2, 1])
with bottom_cols[0]:
    render_section_header("Top priority accounts for today", "Ranked by the scoring engine across pipeline, demand, activity, news, and strategic context.")
    st.dataframe(styled_priority_table(summary.head(10)), hide_index=True, use_container_width=True)

with bottom_cols[1]:
    render_section_header("Next best action recommendations", "Daily plays generated from the current score signals.")
    for row in action_queue.itertuples():
        render_news_item(
            f"{row.account_name} | {row.action_category}",
            f"Rank {row.priority_rank} | {row.priority_bucket} | {format_currency(row.pipeline_amount)} pipeline",
            row.next_best_action,
        )

