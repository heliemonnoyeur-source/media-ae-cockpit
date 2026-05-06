import pandas as pd
import streamlit as st

from src.data_loader import DATASET_CONFIG, get_dataset_source, load_all_data
from src.formatters import format_currency, format_date
from src.scoring import build_account_summary, daily_action_queue
from src.styles import apply_theme, render_callout, render_hero, render_news_item, render_section_header


st.set_page_config(page_title="Daily Actions", layout="wide")
apply_theme()


def build_sidebar() -> None:
    st.sidebar.title("Media AE cockpit")
    st.sidebar.caption("This page compresses the highest-leverage actions into a daily operating plan.")
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
actions = daily_action_queue(summary, limit=12)

render_hero(
    "Daily actions",
    "Start the day with the accounts that need movement now: stalled late-stage deals, recent news triggers, strategic gaps, and fresh demand to convert.",
)
render_callout(
    "Prioritize the first five accounts below before lower-ranked work. The queue blends overall score, recent news, and inactivity signals to surface what deserves attention today."
)

focus_cols = st.columns(4)
focus_cols[0].metric("Actions in queue", len(actions))
focus_cols[1].metric(
    "Late-stage stalls",
    int(
        (
            summary["highest_stage"].isin(["Proposal", "Negotiation"])
            & (summary["days_since_activity"] >= 14)
        ).sum()
    ),
)
focus_cols[2].metric("News-trigger accounts", int((summary["recent_news_count"] > 0).sum()))
focus_cols[3].metric("Strategic gaps", int((summary["strategic_account"] & (summary["days_since_activity"] >= 10)).sum()))

top_actions, action_breakout = st.columns([1.35, 1])
with top_actions:
    render_section_header(
        "Action queue",
        "Use this ranked list as the working set for calls, emails, internal follow-up, and leadership prep.",
    )
    action_table = actions.copy()
    action_table["pipeline_amount"] = action_table["pipeline_amount"].map(format_currency)
    action_table = action_table.rename(
        columns={
            "priority_rank": "Rank",
            "account_name": "Account",
            "owner": "Owner",
            "priority_bucket": "Bucket",
            "pipeline_amount": "Pipeline",
            "highest_stage": "Top stage",
            "days_since_activity": "Days since activity",
            "action_category": "Action theme",
            "next_best_action": "Recommended action",
            "top_driver": "Top driver",
        }
    )
    st.dataframe(action_table, hide_index=True, use_container_width=True)

with action_breakout:
    render_section_header(
        "Playbook by action type",
        "See which themes dominate the day so you can batch your work.",
    )
    counts = actions["action_category"].value_counts().rename_axis("Action theme").reset_index(name="Accounts")
    st.dataframe(counts, hide_index=True, use_container_width=True)

    render_section_header(
        "First call recommendations",
        "Conversation starters generated from the current dataset.",
    )
    for row in actions.head(5).itertuples():
        render_news_item(
            f"{row.account_name} | {row.action_category}",
            f"{row.priority_bucket} priority | {format_currency(row.pipeline_amount)} | {row.days_since_activity} days since activity",
            row.next_best_action,
        )

tabs = st.tabs(["Stalled pipeline", "News triggers", "Fresh demand"])
with tabs[0]:
    stalled = summary[
        summary["highest_stage"].isin(["Proposal", "Negotiation"])
        & (summary["days_since_activity"] >= 14)
    ][
        ["account_name", "pipeline_amount", "highest_stage", "days_since_activity", "next_best_action"]
    ].copy()
    stalled["pipeline_amount"] = stalled["pipeline_amount"].map(format_currency)
    stalled = stalled.rename(
        columns={
            "account_name": "Account",
            "pipeline_amount": "Pipeline",
            "highest_stage": "Top stage",
            "days_since_activity": "Days since activity",
            "next_best_action": "Recommended action",
        }
    )
    st.dataframe(stalled, hide_index=True, use_container_width=True)

with tabs[1]:
    news_accounts = summary[summary["recent_news_count"] > 0][
        ["account_name", "latest_headline", "recent_news_count", "next_best_action"]
    ].copy()
    news_accounts = news_accounts.rename(
        columns={
            "account_name": "Account",
            "latest_headline": "Latest headline",
            "recent_news_count": "News items",
            "next_best_action": "Recommended action",
        }
    )
    st.dataframe(news_accounts, hide_index=True, use_container_width=True)

with tabs[2]:
    fresh_demand = summary[(summary["sql_6m"] > 0) | (summary["mql_6m"] > 0)][
        ["account_name", "sql_6m", "mql_6m", "open_opps", "next_best_action"]
    ].copy()
    fresh_demand = fresh_demand.rename(
        columns={
            "account_name": "Account",
            "sql_6m": "SQLs (6m)",
            "mql_6m": "MQLs (6m)",
            "open_opps": "Open opps",
            "next_best_action": "Recommended action",
        }
    )
    st.dataframe(fresh_demand, hide_index=True, use_container_width=True)
