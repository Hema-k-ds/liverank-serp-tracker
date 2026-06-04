"""
generate_sample_data.py
-----------------------
Creates realistic sample SERP snapshots so you can demo LiveRank
without using up SerpAPI credits.
Run this first, THEN run liverank.py (it will detect "changes").
"""

import os
import pandas as pd

os.makedirs("data", exist_ok=True)

KEYWORDS = [
    "best SEO tools 2025",
    "free keyword research tool",
    "how to rank on Google",
    "SEO for beginners",
    "what is SERP",
    "on page SEO checklist",
    "keyword research tutorial",
]

SAMPLE_DAY1 = [
    # best SEO tools 2025
    ("best SEO tools 2025", 1, "10 Best SEO Tools in 2025", "https://ahrefs.com/blog/best-seo-tools/", "ahrefs.com"),
    ("best SEO tools 2025", 2, "Top SEO Tools Reviewed", "https://moz.com/blog/best-seo-tools", "moz.com"),
    ("best SEO tools 2025", 3, "SEMrush vs Ahrefs 2025", "https://semrush.com/blog/semrush-vs-ahrefs", "semrush.com"),
    # free keyword research tool
    ("free keyword research tool", 1, "Google Keyword Planner Guide", "https://ads.google.com/keyword-planner", "ads.google.com"),
    ("free keyword research tool", 2, "Ubersuggest Free Keyword Tool", "https://neilpatel.com/ubersuggest/", "neilpatel.com"),
    ("free keyword research tool", 3, "Best Free Keyword Tools 2025", "https://backlinko.com/free-keyword-tools", "backlinko.com"),
    # how to rank on Google
    ("how to rank on Google", 1, "How to Rank #1 on Google", "https://backlinko.com/how-to-rank-in-google", "backlinko.com"),
    ("how to rank on Google", 2, "Google Ranking Factors 2025", "https://moz.com/google-ranking-factors", "moz.com"),
    ("how to rank on Google", 3, "SEO Basics: Ranking on Google", "https://developers.google.com/search/docs", "developers.google.com"),
    # SEO for beginners
    ("SEO for beginners", 1, "SEO Starter Guide — Google", "https://developers.google.com/search/docs/beginner/seo-starter-guide", "developers.google.com"),
    ("SEO for beginners", 2, "The Beginner's Guide to SEO", "https://moz.com/beginners-guide-to-seo", "moz.com"),
    ("SEO for beginners", 3, "SEO Tutorial for Beginners 2025", "https://ahrefs.com/blog/seo-basics/", "ahrefs.com"),
    # what is SERP
    ("what is SERP", 1, "What is a SERP? — Moz", "https://moz.com/learn/seo/serp-features", "moz.com"),
    ("what is SERP", 2, "SERP Explained — Ahrefs", "https://ahrefs.com/blog/serp/", "ahrefs.com"),
    ("what is SERP", 3, "Understanding SERPs", "https://semrush.com/blog/serp/", "semrush.com"),
    # on page SEO checklist
    ("on page SEO checklist", 1, "On-Page SEO: The Definitive Guide", "https://backlinko.com/on-page-seo", "backlinko.com"),
    ("on page SEO checklist", 2, "On-Page SEO Checklist 2025", "https://ahrefs.com/blog/on-page-seo-checklist/", "ahrefs.com"),
    ("on page SEO checklist", 3, "Complete On-Page SEO Guide", "https://moz.com/learn/seo/on-page-factors", "moz.com"),
    # keyword research tutorial
    ("keyword research tutorial", 1, "Keyword Research: The Beginner's Guide", "https://moz.com/beginners-guide-to-seo/keyword-research", "moz.com"),
    ("keyword research tutorial", 2, "How to Do Keyword Research", "https://ahrefs.com/blog/keyword-research/", "ahrefs.com"),
    ("keyword research tutorial", 3, "Keyword Research Tutorial", "https://backlinko.com/keyword-research", "backlinko.com"),
]

SAMPLE_DAY2 = [
    # ← rank change: semrush moved to #1 for "best SEO tools"
    ("best SEO tools 2025", 1, "SEMrush Review 2025 — #1 SEO Tool?", "https://semrush.com/blog/best-seo-tools-2025", "semrush.com"),
    ("best SEO tools 2025", 2, "10 Best SEO Tools in 2025", "https://ahrefs.com/blog/best-seo-tools/", "ahrefs.com"),
    ("best SEO tools 2025", 3, "Top SEO Tools Reviewed", "https://moz.com/blog/best-seo-tools", "moz.com"),
    # free keyword research tool — stable
    ("free keyword research tool", 1, "Google Keyword Planner Guide", "https://ads.google.com/keyword-planner", "ads.google.com"),
    ("free keyword research tool", 2, "Ubersuggest Free Keyword Tool", "https://neilpatel.com/ubersuggest/", "neilpatel.com"),
    ("free keyword research tool", 3, "Best Free Keyword Tools 2025", "https://backlinko.com/free-keyword-tools", "backlinko.com"),
    # how to rank — new entrant at #2
    ("how to rank on Google", 1, "How to Rank #1 on Google", "https://backlinko.com/how-to-rank-in-google", "backlinko.com"),
    ("how to rank on Google", 2, "Google Ranking Secrets Revealed", "https://searchengineland.com/ranking-secrets", "searchengineland.com"),
    ("how to rank on Google", 3, "Google Ranking Factors 2025", "https://moz.com/google-ranking-factors", "moz.com"),
    # SEO for beginners — stable
    ("SEO for beginners", 1, "SEO Starter Guide — Google", "https://developers.google.com/search/docs/beginner/seo-starter-guide", "developers.google.com"),
    ("SEO for beginners", 2, "The Beginner's Guide to SEO", "https://moz.com/beginners-guide-to-seo", "moz.com"),
    ("SEO for beginners", 3, "SEO Tutorial for Beginners 2025", "https://ahrefs.com/blog/seo-basics/", "ahrefs.com"),
    # what is SERP — stable
    ("what is SERP", 1, "What is a SERP? — Moz", "https://moz.com/learn/seo/serp-features", "moz.com"),
    ("what is SERP", 2, "SERP Explained — Ahrefs", "https://ahrefs.com/blog/serp/", "ahrefs.com"),
    ("what is SERP", 3, "Understanding SERPs", "https://semrush.com/blog/serp/", "semrush.com"),
    # on page SEO — ahrefs moved to #1
    ("on page SEO checklist", 1, "On-Page SEO Checklist 2025", "https://ahrefs.com/blog/on-page-seo-checklist/", "ahrefs.com"),
    ("on page SEO checklist", 2, "On-Page SEO: The Definitive Guide", "https://backlinko.com/on-page-seo", "backlinko.com"),
    ("on page SEO checklist", 3, "Complete On-Page SEO Guide", "https://moz.com/learn/seo/on-page-factors", "moz.com"),
    # keyword research — stable
    ("keyword research tutorial", 1, "Keyword Research: The Beginner's Guide", "https://moz.com/beginners-guide-to-seo/keyword-research", "moz.com"),
    ("keyword research tutorial", 2, "How to Do Keyword Research", "https://ahrefs.com/blog/keyword-research/", "ahrefs.com"),
    ("keyword research tutorial", 3, "Keyword Research Tutorial", "https://backlinko.com/keyword-research", "backlinko.com"),
]

def build_df(rows, snapshot_date):
    return pd.DataFrame([{
        "date":     snapshot_date,
        "keyword":  r[0],
        "position": r[1],
        "title":    r[2],
        "url":      r[3],
        "domain":   r[4],
        "snippet":  "",
    } for r in rows])

df1 = build_df(SAMPLE_DAY1, "2025-05-31")
df2 = build_df(SAMPLE_DAY2, "2025-06-01")
history = pd.concat([df1, df2], ignore_index=True)

history.to_csv("data/rank_history.csv", index=False)
df1.to_csv("data/serp_snapshot_2025-05-31.csv", index=False)
df2.to_csv("data/serp_snapshot_2025-06-01.csv", index=False)

print("✅ Sample data generated:")
print("   data/rank_history.csv")
print("   data/serp_snapshot_2025-05-31.csv")
print("   data/serp_snapshot_2025-06-01.csv")
print("\nNow run:  python liverank.py")
