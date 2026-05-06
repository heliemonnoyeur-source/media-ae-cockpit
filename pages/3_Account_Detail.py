import plotly.express as px
import streamlit as st

from src.data_loader import DATASET_CONFIG, get_dataset_source, load_all_data
from src.formatters import format_currency, format_date
from src.scoring import account_detail_bundle, build_account_summary
from src.styles import apply_theme, render_callout, render_hero, render_news_item, render_section_header


st.set_page_config(page_title="Account Detail", layout="wide")
apply_theme()


def build_sidebar() -> None:
    st.sidebar.title("Media AE cockpit")
    st.sidebar.caption("Drill into one account to understand score composition, pipeline, activity, and news context.")
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

account_names = summary["account_name"].tolist()
default_account = st.query_params.get("account", account_names[0] if account_names else "")
default_index = account_names.index(default_account) if default_account in account_names else 0

selected_account = st.selectbox("Select an account", account_names, index=default_index)
st.query_params["account"] = selected_account
selected_account_id = summary.loc[summary["account_name"] == selected_account, "account_id"].iloc[0]
details = account_detail_bundle(data, selected_account_id)
account_row = details["summary"]

render_hero(
    f"Account detail | {account_row['account_name']}",
    "Review the full account context, including score composition, open opportunities, demand signals, recent activity, and company news.",
)
render_callout(
    f"{account_row['account_name']} is ranked #{account_row['priority_rank']} with a score of {account_row['priority_score']:.1f}. "
    f"Recommended move: {account_row['next_best_action']}"
)

metric_cols = st.columns(5)
metric_cols[0].metric("Priority score", f"{account_row['priority_score']:.1f}")
metric_cols[1].metric("Pipeline", format_currency(account_row["pipeline_amount"]))
metric_cols[2].metric("Top stage", account_row["highest_stage"])
metric_cols[3].metric("Last activity", format_date(account_row["last_activity_date"]))
metric_cols[4].metric("SQLs / MQLs", f"{int(account_row['sql_6m'])} / {int(account_row['mql_6m'])}")

detail_cols = st.columns([1.1, 1.2])
with detail_cols[0]:
    render_section_header(
        "Score breakdown",
        "Each component shows how the prioritization engine ranked this account today.",
    )
    breakdown_chart = px.bar(
        details["score_breakdown"],
        x="points",
        y="component",
        orientation="h",
        text_auto=True,
        color="points",
        color_continuous_scale="Blues",
        labels={"points": "Points", "component": "Score component"},
    )
    breakdown_chart.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        coloraxis_showscale=False,
    )
    st.plotly_chart(breakdown_chart, use_container_width=True)

with detail_cols[1]:
    render_section_header(
        "Account context",
        "Useful context fields to support planning, multithreading, and internal reviews.",
    )
    st.markdown(
        f"""
        - **Owner:** {account_row['owner']}
        - **Region:** {account_row['region']}
        - **Segment:** {account_row['segment']}
        - **Vertical:** {account_row['vertical']}
        - **Strategic account:** {"Yes" if account_row['strategic_account'] else "No"}
        - **Partner involved:** {"Yes" if account_row['partner_involved'] else "No"}
        - **Renewal date:** {format_date(account_row['renewal_date'])}
        - **Top driver:** {account_row['top_driver']}

        **Next best action**

        {account_row['next_best_action']}
        """
    )

tabs = st.tabs(["Open opportunities", "Recent activity", "Demand signals", "Company news"])

with tabs[0]:
    render_section_header("Open opportunities by stage", "Pipeline currently attached to this account.")
    open_opps = details["opportunities"].copy()
    if open_opps.empty:
        st.info("No open opportunities are associated with this account.")
    else:
        opp_table = open_opps[
            ["opportunity_name", "stage", "amount", "close_date", "created_date"]
        ].copy()
        opp_table["amount"] = opp_table["amount"].map(format_currency)
        opp_table["close_date"] = opp_table["close_date"].map(format_date)
        opp_table["created_date"] = opp_table["created_date"].map(format_date)
        opp_table = opp_table.rename(
            columns={
                "opportunity_name": "Opportunity",
                "stage": "Stage",
                "amount": "Amount",
                "close_date": "Close date",
                "created_date": "Created",
            }
        )
        st.dataframe(opp_table, hide_index=True, use_container_width=True)

with tabs[1]:
    render_section_header("Recent account activity", "Recent calls, meetings, and follow-up logged against this account.")
    activities = details["activities"].copy()
    if activities.empty:
        st.info("No activity records are available for this account.")
    else:
        activities["activity_date"] = activities["activity_date"].map(format_date)
        activities = activities.rename(
            columns={
                "activity_date": "Date",
                "activity_type": "Type",
                "summary": "Summary",
                "owner": "Owner",
            }
        )
        st.dataframe(
            activities[["Date", "Type", "Summary", "Owner"]],
            hide_index=True,
            use_container_width=True,
        )

with tabs[2]:
    render_section_header("Demand signals", "MQL and SQL activity captured over the last six months.")
    leads = details["leads"].copy()
    if leads.empty:
        st.info("No lead records are available for this account.")
    else:
        lead_mix = leads["lead_type"].value_counts().rename_axis("Lead type").reset_index(name="Count")
        lead_chart = px.pie(
            lead_mix,
            names="Lead type",
            values="Count",
            color="Lead type",
            color_discrete_map={"SQL": "#38bdf8", "MQL": "#818cf8"},
        )
        lead_chart.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
        )
        chart_col, table_col = st.columns([0.8, 1.2])
        with chart_col:
            st.plotly_chart(lead_chart, use_container_width=True)
        with table_col:
            lead_table = leads[["lead_date", "lead_type", "source", "campaign", "contact_title"]].copy()
            lead_table["lead_date"] = lead_table["lead_date"].map(format_date)
            lead_table = lead_table.rename(
                columns={
                    "lead_date": "Date",
                    "lead_type": "Type",
                    "source": "Source",
                    "campaign": "Campaign",
                    "contact_title": "Contact title",
                }
            )
            st.dataframe(lead_table, hide_index=True, use_container_width=True)

with tabs[3]:
    render_section_header("Company news", "Recent news triggers available for personalization and account planning.")
    news = details["news"].copy()
    if news.empty:
        st.info("No news records are available for this account.")
    else:
        for row in news.itertuples():
            render_news_item(
                row.headline,
                f"{format_date(row.news_date)} | {row.sentiment} sentiment | {row.importance} importance",
                row.summary,
            )
