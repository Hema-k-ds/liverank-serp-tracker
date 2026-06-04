# 📈 LiveRank — SERP Keyword Tracker with AI Reporting

> **Fetch live Google SERP data → detect rank changes → auto-generate SEO insight reports using Claude AI**

Built by [Hema Karoonyaa T M](https://github.com/Hema-k-ds) · B.Sc Computer Science, VIT Vellore

---

## What It Does

| Step | What happens |
|------|-------------|
| 1️⃣ Fetch | Pulls live Google SERP results for your tracked keywords via SerpAPI |
| 2️⃣ Parse | Extracts position, title, URL, domain into a structured pandas DataFrame |
| 3️⃣ Detect | Compares today's snapshot to previous — flags rank changes automatically |
| 4️⃣ Report | Sends cleaned data to Claude API → outputs a plain-English SEO insight report |
| 5️⃣ Save | Exports CSV snapshot + markdown report — full history accumulates over time |

The entire pipeline runs in **under 2 minutes** with a single command.

---

## Sample Output

### CSV Snapshot (`data/serp_snapshot_2025-06-01.csv`)
```
date,keyword,position,title,url,domain
2025-06-01,best SEO tools 2025,1,SEMrush Review 2025,https://semrush.com/...,semrush.com
2025-06-01,best SEO tools 2025,2,10 Best SEO Tools,https://ahrefs.com/...,ahrefs.com
2025-06-01,free keyword research tool,1,Google Keyword Planner,https://ads.google.com/...,ads.google.com
...
```

### AI Report (`reports/seo_report_2025-06-01.md`)
```markdown
## Executive Summary
Tracked keywords show moderate SERP volatility with two notable position
shifts in the past 24 hours. Most informational queries remain stable.

## Key Observations
- semrush.com displaced ahrefs.com at position #1 for "best SEO tools 2025"
- searchengineland.com entered top 3 for "how to rank on Google" — new competitor
- 5 of 7 keywords show zero movement — strong stability for informational intent

## Rank Changes & Implications
"best SEO tools 2025": semrush.com moved to #1 — likely due to a freshness
update. Monitor over next 48 hours before concluding trend.

## Top Recommendation
Publish a freshness update on any content targeting "best SEO tools" to
compete with semrush.com's newly promoted page.
```

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas)
![SerpAPI](https://img.shields.io/badge/SerpAPI-Free_Tier-green)
![Claude](https://img.shields.io/badge/Claude_AI-Anthropic-orange)

- **Python** — core pipeline
- **SerpAPI** — live Google SERP data (free tier: 100 searches/month)
- **pandas** — data parsing, cleaning, change detection
- **Anthropic Claude API** — AI report generation
- **python-dotenv** — secure key management

---

## Setup & Run

### 1. Clone & install
```bash
git clone https://github.com/Hema-k-ds/liverank-serp-tracker
cd liverank-serp-tracker
pip install -r requirements.txt
```

### 2. Add your API keys
```bash
cp .env.example .env
# Edit .env and add your SERPAPI_KEY and CLAUDE_KEY
```

> 🔑 **Free keys:**
> - SerpAPI: [serpapi.com](https://serpapi.com) — 100 searches/month, no credit card
> - Claude: [console.anthropic.com](https://console.anthropic.com) — free credits on signup

### 3. (Optional) Generate sample data for demo
```bash
python generate_sample_data.py
```

### 4. Run the tracker
```bash
python liverank.py
```

### Output files
```
data/
  rank_history.csv              ← cumulative history across all runs
  serp_snapshot_YYYY-MM-DD.csv  ← daily snapshot
reports/
  seo_report_YYYY-MM-DD.md      ← AI-generated insight report
```

---

## Project Structure
```
liverank-serp-tracker/
├── liverank.py              ← main pipeline
├── generate_sample_data.py  ← demo data generator
├── requirements.txt
├── .env.example
├── .gitignore
└── data/                    ← auto-created on first run
└── reports/                 ← auto-created on first run
```

---

## Skills Demonstrated
- REST API integration (SerpAPI JSON responses)
- Data cleaning & transformation with pandas
- Change detection logic across time-series snapshots
- Prompt engineering with Claude API for structured report generation
- End-to-end Python pipeline design

---

*Part of my data analytics portfolio — see also [SEO InsightBot](https://github.com/Hema-k-ds/seo-insightbot)*

