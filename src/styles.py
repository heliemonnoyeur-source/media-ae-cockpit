import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg: #081120;
                --panel: rgba(15, 23, 42, 0.78);
                --panel-border: rgba(148, 163, 184, 0.18);
                --text: #e2e8f0;
                --muted: #94a3b8;
                --accent: #38bdf8;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 28%),
                    radial-gradient(circle at top right, rgba(129, 140, 248, 0.18), transparent 22%),
                    linear-gradient(180deg, #020617 0%, #081120 100%);
                color: var(--text);
            }

            [data-testid="stSidebar"] {
                background: rgba(2, 6, 23, 0.92);
                border-right: 1px solid rgba(148, 163, 184, 0.12);
            }

            [data-testid="stMetric"],
            .hero-card {
                background: var(--panel);
                border: 1px solid var(--panel-border);
                border-radius: 20px;
                box-shadow: 0 24px 60px rgba(2, 6, 23, 0.32);
                backdrop-filter: blur(12px);
            }

            [data-testid="stMetric"] {
                padding: 0.6rem 0.8rem;
            }

            .hero-card {
                padding: 1.5rem 1.6rem;
                margin-bottom: 1rem;
                background:
                    linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(15, 23, 42, 0.82)),
                    rgba(15, 23, 42, 0.78);
            }

            .hero-kicker {
                text-transform: uppercase;
                letter-spacing: 0.14em;
                font-size: 0.75rem;
                color: #7dd3fc;
                margin-bottom: 0.45rem;
            }

            .hero-title {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }

            .hero-copy {
                color: var(--muted);
                max-width: 54rem;
                line-height: 1.55;
            }

            .section-title {
                font-size: 1.15rem;
                font-weight: 650;
                margin: 0.4rem 0 0.1rem 0;
            }

            .section-copy {
                color: var(--muted);
                margin-bottom: 0.8rem;
            }

            .metric-card {
                background: rgba(15, 23, 42, 0.72);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 18px;
                padding: 1rem 1rem 0.9rem 1rem;
                min-height: 128px;
            }

            .metric-label {
                color: var(--muted);
                font-size: 0.85rem;
                margin-bottom: 0.35rem;
            }

            .metric-value {
                font-size: 1.75rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            }

            .metric-caption {
                color: var(--muted);
                font-size: 0.85rem;
            }

            .pill {
                display: inline-block;
                border-radius: 999px;
                padding: 0.28rem 0.7rem;
                font-size: 0.78rem;
                font-weight: 650;
                margin-right: 0.35rem;
                margin-bottom: 0.3rem;
            }

            .pill-critical {
                background: rgba(248, 113, 113, 0.16);
                color: #fdba74;
            }

            .pill-high {
                background: rgba(251, 191, 36, 0.18);
                color: #fde68a;
            }

            .pill-medium {
                background: rgba(59, 130, 246, 0.14);
                color: #bfdbfe;
            }

            .pill-monitor {
                background: rgba(148, 163, 184, 0.18);
                color: #cbd5e1;
            }

            .callout {
                border-left: 4px solid var(--accent);
                padding: 0.9rem 1rem;
                background: rgba(15, 23, 42, 0.7);
                border-radius: 0 14px 14px 0;
                margin-bottom: 0.75rem;
            }

            .news-card {
                padding: 1rem 1rem 0.9rem 1rem;
                border-radius: 18px;
                border: 1px solid rgba(148, 163, 184, 0.14);
                background: rgba(15, 23, 42, 0.68);
                margin-bottom: 0.65rem;
            }

            .news-title {
                font-size: 0.98rem;
                font-weight: 650;
                margin-bottom: 0.25rem;
            }

            .news-meta {
                color: var(--muted);
                font-size: 0.78rem;
                margin-bottom: 0.35rem;
            }

            div[data-testid="stDataFrame"],
            div[data-testid="stPlotlyChart"] {
                background: rgba(15, 23, 42, 0.52);
                border-radius: 18px;
                padding: 0.45rem;
                border: 1px solid rgba(148, 163, 184, 0.1);
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 999px;
                background: rgba(15, 23, 42, 0.68);
                border: 1px solid rgba(148, 163, 184, 0.12);
                padding: 0.5rem 0.9rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(
    title: str,
    subtitle: str,
    kicker: str = "Media vertical command center",
) -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-copy">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_callout(text: str) -> None:
    st.markdown(f'<div class="callout">{text}</div>', unsafe_allow_html=True)


def render_news_item(title: str, meta: str, summary: str) -> None:
    st.markdown(
        f"""
        <div class="news-card">
            <div class="news-title">{title}</div>
            <div class="news-meta">{meta}</div>
            <div>{summary}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def priority_pill(priority_bucket: str) -> str:
    bucket_key = priority_bucket.lower().replace(" ", "-")
    return f'<span class="pill pill-{bucket_key}">{priority_bucket}</span>'
