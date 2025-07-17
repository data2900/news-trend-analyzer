import feedparser
import pandas as pd
from datetime import datetime
from pathlib import Path
import re

# === 設定 ===
TOPIC_URL = "https://news.google.com/news/rss/headlines/section/topic/BUSINESS?hl=ja&gl=JP&ceid=JP:ja"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === ニュースRSSをパース ===
feed = feedparser.parse(TOPIC_URL)

# === データ抽出 ===
items = []
for entry in feed.entries:
    published = entry.get("published", "")
    try:
        published_dt = datetime(*entry.published_parsed[:6])
    except:
        published_dt = None

    # タイトル末尾の " - ○○新聞" を削除
    raw_title = entry.get("title", "")
    clean_title = re.sub(r"\s*-\s*.+$", "", raw_title)

    items.append({
        "タイトル": clean_title,
        "リンク": entry.get("link", ""),
        "公開日": published_dt,
        "概要": entry.get("summary", "")
    })

# === DataFrame化＆保存 ===
df = pd.DataFrame(items)
date_str = datetime.now().strftime("%Y%m%d")
output_path = OUTPUT_DIR / f"news_{date_str}.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ ニュースを収集し保存しました: {output_path}")