"""
LiveRank — SERP Keyword Tracker with AI-Powered Reporting
==========================================================
Fetches live Google SERP data via SerpAPI, tracks keyword rank
changes over time, and auto-generates insight reports using Claude AI.

Author : Hema Karoonyaa T M
GitHub : github.com/Hema-k-ds
"""

import os
import json
import requests
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
SERPAPI_KEY   = os.getenv("SERPAPI_KEY", "YOUR_SERPAPI_KEY_HERE")
CLAUDE_KEY    = os.getenv("CLAUDE_KEY",  "YOUR_CLAUDE_KEY_HERE")
HISTORY_FILE  = "data/rank_history.csv"
REPORTS_DIR   = "reports"
TODAY         = str(date.today())

KEYWORDS = [
    "best SEO tools 2025",
    "free keyword research tool",
    "how to rank on Google",
    "SEO for beginners",
    "what is SERP",
    "on page SEO checklist",
    "keyword research tutorial",
]

os.makedirs("data",    exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ── STEP 1: FETCH LIVE SERP DATA ──────────────────────────────────────────────
def fetch_rankings(keywords: list[str]) -> pd.DataFrame:
    """Call SerpAPI for each keyword and return a structured DataFrame."""
    rows = []
    for kw in keywords:
        print(f"  📡 Fetching: '{kw}'")
        params = {
            "q":       kw,
            "api_key": SERPAPI_KEY,
            "num":     10,
            "engine":  "google",
            "hl":      "en",
            "gl":      "us",
        }
        try:
            resp = requests.get("https://serpapi.com/search", params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"    ⚠️  Error fetching '{kw}': {e}")
            continue

        organic = data.get("organic_results", [])
        for i, result in enumerate(organic[:10], start=1):
            rows.append({
                "date":     TODAY,
                "keyword":  kw,
                "position": i,
                "title":    result.get("title",   ""),
                "url":      result.get("link",    ""),
                "snippet":  result.get("snippet", ""),
                "domain":   result.get("displayed_link", "").split("/")[0],
            })

    return pd.DataFrame(rows)


# ── STEP 2: DETECT RANK CHANGES ───────────────────────────────────────────────
def detect_changes(new_df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Compare today's top results against previous snapshot."""
    if not os.path.exists(HISTORY_FILE):
        return new_df, []

    old_df     = pd.read_csv(HISTORY_FILE)
    prev_dates = old_df["date"].unique()
    if len(prev_dates) == 0:
        return new_df, []

    last_date  = sorted(prev_dates)[-1]
    old_latest = old_df[old_df["date"] == last_date]
    changes    = []

    for kw in new_df["keyword"].unique():
        new_top = new_df[(new_df["keyword"] == kw) & (new_df["position"] == 1)]
        old_top = old_latest[(old_latest["keyword"] == kw) & (old_latest["position"] == 1)]

        if new_top.empty or old_top.empty:
            continue

        new_url = new_top["url"].values[0]
        old_url = old_top["url"].values[0]

        if new_url != old_url:
            changes.append(
                f"'{kw}': #1 result changed\n"
                f"  Was : {old_url}\n"
                f"  Now : {new_url}"
            )

        # Position shifts for top 5
        for pos in range(1, 6):
            new_at = new_df[(new_df["keyword"] == kw) & (new_df["position"] == pos)]
            old_at = old_latest[(old_latest["keyword"] == kw) & (old_latest["position"] == pos)]
            if not new_at.empty and not old_at.empty:
                if new_at["domain"].values[0] != old_at["domain"].values[0]:
                    changes.append(
                        f"'{kw}' position {pos}: "
                        f"'{old_at['domain'].values[0]}' → '{new_at['domain'].values[0]}'"
                    )

    return new_df, changes


# ── STEP 3: AI INSIGHT REPORT ─────────────────────────────────────────────────
def generate_ai_report(df: pd.DataFrame, changes: list[str]) -> str:
    """Send SERP snapshot to Claude and get a structured SEO insight report."""

    # Build compact summary for the prompt
    summary = {}
    for kw in df["keyword"].unique():
        top3 = df[df["keyword"] == kw].head(3)[["position", "title", "domain"]].to_dict("records")
        summary[kw] = top3

    prompt = f"""You are a senior SEO analyst reviewing today's SERP tracking data.

TODAY'S DATE: {TODAY}

TOP 3 RESULTS PER KEYWORD:
{json.dumps(summary, indent=2)}

RANK CHANGES DETECTED FROM PREVIOUS SNAPSHOT:
{chr(10).join(changes) if changes else "No changes detected — stable results."}

Write a professional SEO insight report with exactly this structure:

## Executive Summary
(2 sentences — overall health of the tracked keywords)

## Key Observations
- (3 bullet points about patterns you notice in the SERP data)

## Rank Changes & Implications
(Comment on each change detected, or note stability if none)

## Top Recommendation
(1 specific, actionable recommendation based on the data)

---
Keep total length under 250 words. Be specific — reference actual keywords and domains."""

    client  = anthropic.Anthropic(api_key=CLAUDE_KEY)
    message = client.messages.create(
        model      = "claude-opus-4-5",
        max_tokens = 600,
        messages   = [{"role": "user", "content": prompt}]
    )
    return message.content[0].text


# ── STEP 4: SAVE OUTPUTS ──────────────────────────────────────────────────────
def save_outputs(df: pd.DataFrame, report: str):
    # Append to history
    if os.path.exists(HISTORY_FILE):
        old = pd.read_csv(HISTORY_FILE)
        pd.concat([old, df], ignore_index=True).to_csv(HISTORY_FILE, index=False)
    else:
        df.to_csv(HISTORY_FILE, index=False)

    # Daily snapshot CSV
    snapshot_path = f"data/serp_snapshot_{TODAY}.csv"
    df.to_csv(snapshot_path, index=False)
    print(f"  ✅ Snapshot saved  : {snapshot_path}")

    # Markdown report
    report_path = f"{REPORTS_DIR}/seo_report_{TODAY}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# SEO Insight Report — {TODAY}\n\n")
        f.write("_Auto-generated by LiveRank using Claude AI_\n\n")
        f.write("---\n\n")
        f.write(report)
    print(f"  ✅ Report saved    : {report_path}")

    return snapshot_path, report_path


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("\n🚀 LiveRank — SERP Keyword Tracker")
    print("=" * 42)

    print("\n[1/4] Fetching live SERP data...")
    df = fetch_rankings(KEYWORDS)
    if df.empty:
        print("❌ No data fetched. Check your SERPAPI_KEY.")
        return

    print(f"\n[2/4] Detecting rank changes...")
    df, changes = detect_changes(df)
    print(f"  Found {len(changes)} change(s).")

    print("\n[3/4] Generating AI insight report...")
    report = generate_ai_report(df, changes)

    print("\n[4/4] Saving outputs...")
    snapshot_path, report_path = save_outputs(df, report)

    print("\n" + "=" * 42)
    print("📋 REPORT PREVIEW")
    print("=" * 42)
    print(report)
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
