from __future__ import annotations

from typing import Any

import pandas as pd


STAGE_ORDER = ["Prospecting", "Discovery", "Evaluation", "Proposal", "Negotiation"]
STAGE_WEIGHTS = {
    "Prospecting": 1,
    "Discovery": 2,
    "Evaluation": 3,
    "Proposal": 4,
    "Negotiation": 5,
    "Closed Won": 6,
    "Closed Lost": 0,
}
SCORE_COMPONENT_LABELS = {
    "pipeline_points": "Pipeline",
    "stage_points": "Stage urgency",
    "sql_points": "Recent SQLs",
    "mql_points": "Recent MQLs",
    "activity_gap_points": "Activity gap",
    "strategic_points": "Strategic account",
    "news_points": "Recent news",
    "partner_points": "Partner involvement",
}


def _today() -> pd.Timestamp:
    return pd.Timestamp.today().normalize()


def _normalize_text(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(dtype="object")
    return df[column].fillna("").astype(str).str.strip()


def _priority_bucket(score: float) -> str:
    if score >= 75:
        return "Critical"
    if score >= 55:
        return "High"
    if score >= 35:
        return "Medium"
    return "Monitor"


def _activity_gap_points(days_since_activity: float) -> int:
    if pd.isna(days_since_activity):
        return 12
    if days_since_activity >= 21:
        return 12
    if days_since_activity >= 14:
        return 10
    if days_since_activity >= 7:
        return 6
    return 2


def _safe_max(value: float, fallback: float = 1.0) -> float:
    return value if value and value > 0 else fallback


def _top_driver(row: pd.Series) -> str:
    drivers = [
        (label, row[column])
        for column, label in SCORE_COMPONENT_LABELS.items()
        if row.get(column, 0) > 0
    ]
    if not drivers:
        return "Whitespace opportunity"
    top_two = sorted(drivers, key=lambda item: item[1], reverse=True)[:2]
    return " + ".join(label for label, _ in top_two)


def _action_plan(row: pd.Series) -> tuple[str, str]:
    if row["pipeline_amount"] >= 1_000_000 and row["days_since_activity"] >= 14:
        return (
            "Stalled late-stage deal",
            "Re-engage the buying committee on the stalled deal, confirm the close plan, and schedule an executive checkpoint this week.",
        )
    if row["recent_news_count"] > 0 and row["pipeline_amount"] < 1_000_000:
        return (
            "News-trigger outreach",
            "Reference the latest company news in tailored outreach and connect it to the value story for digital media revenue growth.",
        )
    if row["sql_6m"] >= 2 and row["open_opps"] == 0:
        return (
            "Convert demand to pipeline",
            "Turn recent SQL momentum into fresh discovery by locking an account planning meeting with the best-fit stakeholder set.",
        )
    if row["highest_stage"] in {"Proposal", "Negotiation"} and row["partner_involved"]:
        return (
            "Partner close plan",
            "Align your partner, champion, and internal team on a joint close plan with procurement, legal, and success criteria.",
        )
    if row["highest_stage"] in {"Proposal", "Negotiation"}:
        return (
            "Close plan inspection",
            "Tighten the mutual action plan, validate commercial blockers, and secure the next decision-maker conversation.",
        )
    if row["strategic_account"] and row["days_since_activity"] >= 10:
        return (
            "Executive sponsorship",
            "Rebuild executive coverage on this strategic account and create a leadership touchpoint tied to the broader media strategy.",
        )
    if row["mql_6m"] >= 3:
        return (
            "Expand multithreading",
            "Mine recent marketing engagement for new personas, then open follow-up discovery around measurement, monetization, or audience data.",
        )
    return (
        "Whitespace development",
        "Review whitespace, refresh contacts, and queue targeted outreach for the next uncovered team or initiative.",
    )


def _prepare_open_opportunities(opportunities: pd.DataFrame) -> pd.DataFrame:
    if opportunities.empty:
        return opportunities.copy()
    open_opportunities = opportunities.copy()
    open_opportunities["status"] = _normalize_text(open_opportunities, "status")
    open_opportunities["stage"] = _normalize_text(open_opportunities, "stage")
    open_opportunities = open_opportunities[open_opportunities["status"].eq("Open")].copy()
    open_opportunities["stage_rank"] = open_opportunities["stage"].map(STAGE_WEIGHTS).fillna(0)
    return open_opportunities


def build_account_summary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    accounts = data["accounts"].copy()
    opportunities = data["opportunities"].copy()
    activities = data["activities"].copy()
    leads = data["leads"].copy()
    news = data["news"].copy()

    today = _today()
    six_month_cutoff = today - pd.DateOffset(months=6)
    news_cutoff = today - pd.Timedelta(days=45)
    activity_30_day_cutoff = today - pd.Timedelta(days=30)

    accounts["strategic_account"] = accounts["strategic_account"].fillna(False).astype(bool)
    accounts["partner_involved"] = accounts["partner_involved"].fillna(False).astype(bool)

    open_opportunities = _prepare_open_opportunities(opportunities)
    if not open_opportunities.empty:
        open_opportunities["amount"] = pd.to_numeric(open_opportunities["amount"], errors="coerce").fillna(0)

    opportunity_rollup = (
        open_opportunities.groupby("account_id", as_index=False)
        .agg(
            pipeline_amount=("amount", "sum"),
            open_opps=("opportunity_id", "count"),
            max_stage_rank=("stage_rank", "max"),
            next_close_date=("close_date", "min"),
        )
        if not open_opportunities.empty
        else pd.DataFrame(columns=["account_id", "pipeline_amount", "open_opps", "max_stage_rank", "next_close_date"])
    )

    highest_stage = (
        open_opportunities.sort_values(
            ["account_id", "stage_rank", "amount"],
            ascending=[True, False, False],
        )
        .drop_duplicates(subset="account_id")
        [["account_id", "stage"]]
        .rename(columns={"stage": "highest_stage"})
        if not open_opportunities.empty
        else pd.DataFrame(columns=["account_id", "highest_stage"])
    )

    lead_window = leads[leads["lead_date"] >= six_month_cutoff].copy()
    lead_window["lead_type"] = _normalize_text(lead_window, "lead_type").str.upper()
    if not lead_window.empty:
        lead_counts = (
            lead_window.pivot_table(
                index="account_id",
                columns="lead_type",
                values="lead_id",
                aggfunc="count",
                fill_value=0,
            )
            .rename(columns={"SQL": "sql_6m", "MQL": "mql_6m"})
            .reset_index()
        )
    else:
        lead_counts = pd.DataFrame(columns=["account_id", "sql_6m", "mql_6m"])

    activity_summary = (
        activities.groupby("account_id", as_index=False)
        .agg(
            last_activity_date=("activity_date", "max"),
            activities_30d=("activity_id", lambda series: int((activities.loc[series.index, "activity_date"] >= activity_30_day_cutoff).sum())),
        )
        if not activities.empty
        else pd.DataFrame(columns=["account_id", "last_activity_date", "activities_30d"])
    )

    news_recent = news[news["news_date"] >= news_cutoff].copy()
    news_summary = (
        news_recent.groupby("account_id", as_index=False)
        .agg(
            recent_news_count=("news_id", "count"),
            latest_news_date=("news_date", "max"),
        )
        if not news_recent.empty
        else pd.DataFrame(columns=["account_id", "recent_news_count", "latest_news_date"])
    )

    latest_news = (
        news_recent.sort_values(["account_id", "news_date"], ascending=[True, False])
        .drop_duplicates(subset="account_id")
        [["account_id", "headline"]]
        .rename(columns={"headline": "latest_headline"})
        if not news_recent.empty
        else pd.DataFrame(columns=["account_id", "latest_headline"])
    )

    summary = accounts.merge(opportunity_rollup, on="account_id", how="left")
    summary = summary.merge(highest_stage, on="account_id", how="left")
    summary = summary.merge(lead_counts, on="account_id", how="left")
    summary = summary.merge(activity_summary, on="account_id", how="left")
    summary = summary.merge(news_summary, on="account_id", how="left")
    summary = summary.merge(latest_news, on="account_id", how="left")

    fill_zero_columns = [
        "pipeline_amount",
        "open_opps",
        "max_stage_rank",
        "sql_6m",
        "mql_6m",
        "activities_30d",
        "recent_news_count",
    ]
    for column in fill_zero_columns:
        if column not in summary.columns:
            summary[column] = 0
        summary[column] = summary[column].fillna(0)

    summary["highest_stage"] = summary["highest_stage"].fillna("No open opp")
    summary["days_since_activity"] = (
        today - summary["last_activity_date"]
    ).dt.days.fillna(45)

    max_pipeline = _safe_max(float(summary["pipeline_amount"].max()))
    summary["pipeline_points"] = (summary["pipeline_amount"] / max_pipeline * 25).round(1)
    summary["stage_points"] = (summary["max_stage_rank"] / 5 * 15).round(1)
    summary["sql_points"] = summary["sql_6m"].clip(upper=3) * 4
    summary["mql_points"] = summary["mql_6m"].clip(upper=4) * 2
    summary["activity_gap_points"] = summary["days_since_activity"].apply(_activity_gap_points)
    summary["strategic_points"] = summary["strategic_account"].apply(lambda value: 10 if value else 0)
    summary["news_points"] = summary["recent_news_count"].clip(upper=2) * 5
    summary["partner_points"] = summary["partner_involved"].apply(lambda value: 8 if value else 0)

    score_columns = list(SCORE_COMPONENT_LABELS.keys())
    summary["priority_score"] = summary[score_columns].sum(axis=1).round(1)
    summary["priority_bucket"] = summary["priority_score"].apply(_priority_bucket)
    summary["top_driver"] = summary.apply(_top_driver, axis=1)

    actions = summary.apply(_action_plan, axis=1, result_type="expand")
    summary["action_category"] = actions[0]
    summary["next_best_action"] = actions[1]

    summary["priority_rank"] = summary["priority_score"].rank(method="first", ascending=False).astype(int)

    sort_columns = ["priority_score", "pipeline_amount", "sql_6m", "mql_6m"]
    summary = summary.sort_values(sort_columns, ascending=[False, False, False, False]).reset_index(drop=True)
    summary["priority_rank"] = summary.index + 1
    return summary


def stage_pipeline_summary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    opportunities = _prepare_open_opportunities(data["opportunities"])
    if opportunities.empty:
        return pd.DataFrame(columns=["stage", "open_opps", "pipeline_amount"])

    opportunities["amount"] = pd.to_numeric(opportunities["amount"], errors="coerce").fillna(0)
    summary = (
        opportunities.groupby("stage", as_index=False)
        .agg(open_opps=("opportunity_id", "count"), pipeline_amount=("amount", "sum"))
    )
    summary["stage_rank"] = summary["stage"].map(STAGE_WEIGHTS).fillna(0)
    summary = summary.sort_values("stage_rank").drop(columns=["stage_rank"])
    return summary


def monthly_lead_summary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    leads = data["leads"].copy()
    if leads.empty:
        return pd.DataFrame(columns=["month", "lead_type", "count"])

    today = _today()
    month_floor = (today - pd.DateOffset(months=5)).replace(day=1)
    leads = leads[leads["lead_date"] >= month_floor].copy()
    leads["lead_type"] = _normalize_text(leads, "lead_type").str.upper()
    leads["month"] = leads["lead_date"].dt.to_period("M").dt.to_timestamp()
    summary = (
        leads.groupby(["month", "lead_type"], as_index=False)
        .agg(count=("lead_id", "count"))
        .sort_values(["month", "lead_type"])
    )
    return summary


def recent_activity_feed(data: dict[str, pd.DataFrame], limit: int = 10) -> pd.DataFrame:
    activities = data["activities"].copy()
    accounts = data["accounts"][["account_id", "account_name"]].copy()
    if activities.empty:
        return pd.DataFrame(columns=["activity_date", "account_name", "activity_type", "summary", "owner"])

    feed = activities.merge(accounts, on="account_id", how="left")
    feed = feed.sort_values("activity_date", ascending=False).head(limit)
    return feed[["activity_date", "account_name", "activity_type", "summary", "owner"]]


def recent_news_feed(data: dict[str, pd.DataFrame], limit: int = 8) -> pd.DataFrame:
    news = data["news"].copy()
    accounts = data["accounts"][["account_id", "account_name"]].copy()
    if news.empty:
        return pd.DataFrame(columns=["news_date", "account_name", "headline", "summary", "sentiment", "importance"])

    feed = news.merge(accounts, on="account_id", how="left")
    feed = feed.sort_values("news_date", ascending=False).head(limit)
    return feed[["news_date", "account_name", "headline", "summary", "sentiment", "importance"]]


def daily_action_queue(summary: pd.DataFrame, limit: int = 12) -> pd.DataFrame:
    action_queue = summary.copy()
    action_queue["action_rank"] = (
        action_queue["priority_score"]
        + action_queue["days_since_activity"].clip(upper=30) * 0.3
        + action_queue["recent_news_count"] * 2
    )
    action_queue = action_queue.sort_values(
        ["action_rank", "priority_score", "pipeline_amount"],
        ascending=[False, False, False],
    ).head(limit)
    return action_queue[
        [
            "priority_rank",
            "account_name",
            "owner",
            "priority_bucket",
            "pipeline_amount",
            "highest_stage",
            "days_since_activity",
            "action_category",
            "next_best_action",
            "top_driver",
        ]
    ]


def score_breakdown(row: pd.Series) -> pd.DataFrame:
    breakdown = pd.DataFrame(
        [
            {"component": label, "points": float(row[column])}
            for column, label in SCORE_COMPONENT_LABELS.items()
        ]
    )
    return breakdown.sort_values("points", ascending=True)


def account_detail_bundle(data: dict[str, pd.DataFrame], account_id: str) -> dict[str, Any]:
    summary = build_account_summary(data)
    account_row = summary.loc[summary["account_id"] == account_id].iloc[0]

    opportunities = _prepare_open_opportunities(data["opportunities"])
    opportunities = opportunities.loc[opportunities["account_id"] == account_id].copy()
    opportunities["amount"] = pd.to_numeric(opportunities["amount"], errors="coerce").fillna(0)
    opportunities = opportunities.sort_values(["stage_rank", "amount"], ascending=[False, False])

    activities = data["activities"].loc[data["activities"]["account_id"] == account_id].copy()
    activities = activities.sort_values("activity_date", ascending=False)

    leads = data["leads"].loc[data["leads"]["account_id"] == account_id].copy()
    leads = leads.sort_values("lead_date", ascending=False)

    news = data["news"].loc[data["news"]["account_id"] == account_id].copy()
    news = news.sort_values("news_date", ascending=False)

    return {
        "summary": account_row,
        "score_breakdown": score_breakdown(account_row),
        "opportunities": opportunities,
        "activities": activities,
        "leads": leads,
        "news": news,
    }
