from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# === 日本語フォント設定（Mac専用）===
plt.rcParams["font.family"] = "Hiragino Sans"

# === 基本設定 ===
BASE_DIR = Path("/news")
OUTPUT_DIR = BASE_DIR / "output"
date_str = datetime.now().strftime("%Y%m%d")

# === キーワード読み込み ===
keywords_path = OUTPUT_DIR / "top_keywords.txt"
if not keywords_path.exists():
    sys.exit("❌ top_keywords.txt が見つかりません")

with open(keywords_path, encoding="utf-8") as f:
    KEYWORDS = [line.strip() for line in f if line.strip()]

# === pytrendsでデータ取得 ===
TIMEFRAME = "today 3-m"
pytrends = TrendReq(hl="ja-JP", tz=540)
pytrends.build_payload(KEYWORDS, timeframe=TIMEFRAME, geo="JP")
data = pytrends.interest_over_time()

if data.empty:
    sys.exit("❌ Googleトレンドデータが取得できませんでした。")

# === ピーク日抽出用リスト ===
peak_rows = []

# === グラフ描画 ===
plt.figure(figsize=(12, 6))
for keyword in KEYWORDS:
    plt.plot(data.index, data[keyword], label=keyword)
    peak_date = data[keyword].idxmax()
    peak_value = data[keyword].max()
    plt.axvline(x=peak_date, color='gray', linestyle='--', alpha=0.5)
    plt.text(peak_date, peak_value, f"{keyword}\n{peak_value}", fontsize=8, ha='right')
    peak_rows.append({
        "キーワード": keyword,
        "ピーク日": peak_date.strftime("%Y-%m-%d"),
        "関心度": int(peak_value)
    })

plt.title("Googleトレンド: 関心度の推移（ピーク日付き）")
plt.xlabel("日付")
plt.ylabel("検索関心度")
plt.legend()
plt.grid(True)
plt.tight_layout()

# === グラフ保存（表示はしない）===
img_path = OUTPUT_DIR / f"trends_{date_str}.png"
plt.savefig(img_path)
plt.close()  # ← これで表示されないようにする
print(f"✅ グラフ保存: {img_path}")

# === ピーク日CSV保存 ===
peak_df = pd.DataFrame(peak_rows)
csv_path = OUTPUT_DIR / f"trend_peaks_{date_str}.csv"
peak_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"✅ ピーク日CSV保存: {csv_path}")

# === 検索関心度データ保存 ===
trend_data_csv = OUTPUT_DIR / f"trend_data_{date_str}.csv"
data.drop(columns=["isPartial"], errors="ignore").to_csv(trend_data_csv, encoding="utf-8-sig")
print(f"✅ 関心度推移データ保存: {trend_data_csv}")