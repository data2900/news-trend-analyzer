import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# === 日付とパス設定 ===
date_str = datetime.now().strftime("%Y%m%d")
BASE_DIR = Path("/news")
OUTPUT_DIR = BASE_DIR / "output"

news_csv = OUTPUT_DIR / f"news_{date_str}.csv"
keywords_txt = OUTPUT_DIR / "top_keywords.txt"
trend_data_csv = OUTPUT_DIR / f"trend_data_{date_str}.csv"
trend_peaks_csv = OUTPUT_DIR / f"trend_peaks_{date_str}.csv"

# === ファイル存在チェック ===
for file in [news_csv, keywords_txt, trend_data_csv, trend_peaks_csv]:
    if not file.exists():
        sys.exit(f"❌ 必要なファイルが見つかりません: {file}")

# === ニュースとキーワードの関連づけ（目的①） ===
df_news = pd.read_csv(news_csv)
df_news["テキスト"] = df_news["タイトル"].fillna("") + " " + df_news["概要"].fillna("")

with open(keywords_txt, "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f.readlines() if line.strip()]

records = []
for kw in keywords:
    for _, row in df_news.iterrows():
        if kw in row["テキスト"]:
            records.append({
                "キーワード": kw,
                "タイトル": row["タイトル"],
                "リンク": row["リンク"],
                "公開日": row["公開日"]
            })

df_match = pd.DataFrame(records)
df_match.to_csv(OUTPUT_DIR / f"keyword_news_match_{date_str}.csv", index=False, encoding="utf-8-sig")
print("✅ keyword_news_match_*.csv を出力しました")

# === トレンドデータとピーク日を結合（目的②） ===
# 修正ポイント：date → 日付 に変換
df_trend = pd.read_csv(trend_data_csv, parse_dates=["date"])
df_trend.rename(columns={"date": "日付"}, inplace=True)

df_peaks = pd.read_csv(trend_peaks_csv)

df_summary = []
for kw in keywords:
    df_kw = df_trend[["日付", kw]].copy()
    df_kw["キーワード"] = kw
    df_kw = df_kw.rename(columns={kw: "関心度"})
    peak_row = df_peaks[df_peaks["キーワード"] == kw]
    peak_date = peak_row["ピーク日"].values[0] if not peak_row.empty else None
    peak_value = peak_row["関心度"].values[0] if not peak_row.empty else None
    df_kw["ピーク日"] = peak_date
    df_kw["最大関心度"] = peak_value
    df_summary.append(df_kw)

df_summary_all = pd.concat(df_summary)
df_summary_all.to_csv(OUTPUT_DIR / f"trend_summary_{date_str}.csv", index=False, encoding="utf-8-sig")
print("✅ trend_summary_*.csv を出力しました")

# === ニュース件数×トレンド強度（目的③） ===
match_counts = df_match["キーワード"].value_counts().rename("ニュース件数").reset_index()
match_counts = match_counts.rename(columns={"index": "キーワード"})

agg_trend = df_trend[keywords].agg(["max", "mean", "min"]).T.reset_index()
agg_trend.columns = ["キーワード", "最大関心度", "平均関心度", "最小関心度"]

df_dashboard = pd.merge(match_counts, agg_trend, on="キーワード", how="outer").fillna(0)
df_dashboard["バズ指数"] = df_dashboard["ニュース件数"] * df_dashboard["平均関心度"]
df_dashboard = df_dashboard.sort_values("バズ指数", ascending=False)

df_dashboard.to_csv(OUTPUT_DIR / f"dashboard_{date_str}.csv", index=False, encoding="utf-8-sig")
print("✅ dashboard_*.csv を出力しました")