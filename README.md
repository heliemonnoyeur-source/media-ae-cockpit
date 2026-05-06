# Media AE Sales Cockpit

A modern Streamlit sales cockpit for an Enterprise Account Executive managing a Media vertical. The app helps prioritize accounts, understand pipeline health, review recent demand and activity, and focus on the most important actions to take each day.

## Features

- Home dashboard with:
  - pipeline overview
  - open opportunities by stage
  - SQLs from the last 6 months
  - MQLs from the last 6 months
  - recent account activity
  - recent company news
  - top priority accounts for today
  - next best action recommendations
- Account prioritization page with filters and ranked account scoring
- Daily actions page with a focused action queue
- Account detail page with score breakdown, pipeline, activity, leads, and news
- CSV upload page to replace sample data during a Streamlit session
- Sample CSV files with fake media-account data

## Tech stack

- Python
- Streamlit
- pandas
- plotly

## Project structure

```text
.
├── app.py
├── data
│   ├── accounts.csv
│   ├── activities.csv
│   ├── leads.csv
│   ├── news.csv
│   └── opportunities.csv
├── pages
│   ├── 1_Account_Prioritization.py
│   ├── 2_Daily_Actions.py
│   ├── 3_Account_Detail.py
│   └── 4_CSV_Upload.py
├── requirements.txt
└── src
    ├── __init__.py
    ├── data_loader.py
    ├── formatters.py
    ├── scoring.py
    └── styles.py
```

## Scoring engine

Accounts are prioritized using a point-based scoring model that blends:

- pipeline amount
- opportunity stage urgency
- recent SQL volume
- recent MQL volume
- activity gaps
- strategic account flag
- recent news
- partner involvement

The resulting score is translated into priority buckets:

- Critical
- High
- Medium
- Monitor

The app also generates a `next best action` recommendation for each account based on the account's strongest signals.

## Local setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app locally:

   ```bash
   streamlit run app.py
   ```

4. Open the local Streamlit URL shown in your terminal.

## CSV data model

Use the sample files in `data/` as templates for your own uploads.

### accounts.csv

```text
account_id, account_name, owner, region, segment, vertical, strategic_account, partner_involved, account_tier, renewal_date
```

### opportunities.csv

```text
opportunity_id, account_id, opportunity_name, stage, amount, close_date, created_date, status
```

### activities.csv

```text
activity_id, account_id, activity_date, activity_type, summary, owner
```

### leads.csv

```text
lead_id, account_id, lead_date, lead_type, source, campaign, contact_title
```

### news.csv

```text
news_id, account_id, news_date, headline, summary, sentiment, importance
```

## Notes

- Sample data is loaded by default.
- Uploaded CSVs override the sample datasets for the current Streamlit session only.
- The sample dataset is tailored to a Media enterprise-sales workflow and uses fake records.
