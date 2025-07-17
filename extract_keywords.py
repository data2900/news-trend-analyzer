# extract_keywords.py

import pandas as pd
from pathlib import Path
from datetime import datetime
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
import sys

# === ファイル読み込み設定（絶対パスに変更）===
BASE_DIR = Path(__file__).resolve().parent.parent / "news"
date_str = datetime.now().strftime("%Y%m%d")
INPUT_CSV = BASE_DIR / "output" / f"news_{date_str}.csv"

if not INPUT_CSV.exists():
    sys.exit(f"❌ ファイルが存在しません: {INPUT_CSV}")

print(f"📂 使用ファイル: {INPUT_CSV.name}")

# === 形態素解析器の初期化（名詞のみ）===
tokenizer = Tokenizer()

def tokenize(text):
    words = []
    for token in tokenizer.tokenize(text):
        base = token.base_form
        pos = token.part_of_speech.split(',')[0]
        if pos == '名詞' and len(base) > 1 and not re.match(r'^[\d０-９]+$', base):
            words.append(base)
    return words

# === CSV読み込み（タイトル列のみ使用）===
df = pd.read_csv(INPUT_CSV, usecols=["タイトル"])
df = df.dropna(subset=["タイトル"])
texts = df["タイトル"].tolist()

# === TF（単語の出現頻度） ===
all_words = []
for title in texts:
    all_words.extend(tokenize(title))

tf_counts = Counter(all_words)
print("\n📊 上位TF（頻出語）:")
for word, freq in tf_counts.most_common(20):
    print(f"{word}: {freq}")

# === TF-IDF（重要語） ===
def analyzer(text):
    return tokenize(text)

vectorizer = TfidfVectorizer(analyzer=analyzer, use_idf=True, smooth_idf=True)
X = vectorizer.fit_transform(texts)
scores = zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0))
sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

print("\n💡 上位TF-IDF（重要語）:")
for word, score in sorted_scores[:20]:
    print(f"{word}: {score:.4f}")

# 上位キーワードの保存
top_words = [word for word, _ in tf_counts.most_common(10)]
with open(BASE_DIR / "output" / "top_keywords.txt", "w", encoding="utf-8") as f:
    for word in top_words:
        f.write(f"{word}\n")

print("\n✅ 上位キーワードを保存しました（top_keywords.txt）")