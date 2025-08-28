# news-trend-analyzer
ニュース収集、頻出キーワード抽出、Googleトレンド分析、データ整形・可視化までを行う軽量な情報分析ツールです。 プログラミング初心者でも、生成AIを活用しながら、実用的な情報処理ワークフローを構築できるよう意図して作成しています。

# ニュース＆トレンド分析パイプライン

このリポジトリは、日本のビジネスニュースを収集し、重要キーワードの抽出、Googleトレンドの解析、データ処理・集計を行う一連のPythonスクリプト群です。

---

## スクリプト一覧と概要

### 1. fetch_news.py  
GoogleニュースのRSSから最新のビジネスニュースを収集し、CSVファイルに保存します。  
- ニュースタイトルの後ろにつく新聞社名などの除去も行います。

### 2. extract_keywords.py  
収集済みニュースタイトルを形態素解析（Janome）し、名詞に絞って頻出単語（TF）と重要単語（TF-IDF）を抽出します。  
- 上位キーワードはテキストファイルに保存されます。

### 3. google_trends.py  
extract_keywords.pyで抽出したキーワードをもとに、Googleトレンドの過去3ヶ月間の関心度推移を取得します。  
- キーワードごとのピーク日を検出し、グラフとCSVファイルに保存します。

### 4. process_data.py  
ニュースデータとトレンドデータを組み合わせて解析し、  
- キーワードとニュース記事の関連づけ  
- トレンドピーク日との結合  
- ニュース件数×トレンド関心度によるバズ指数の計算  
を行い、結果をCSVファイルに出力します。

---

## 環境と依存関係

- Python 3.8以上推奨  
- 必要なPythonパッケージ:  
  ```bash
  pip install pandas feedparser janome scikit-learn matplotlib pytrends

	•	日本語形態素解析にJanomeを使用しています。
	•	Googleトレンド取得にはpytrendsを利用しています。

⸻

フォルダ構成（例）
/news
  /output
    news_YYYYMMDD.csv
    top_keywords.txt
    trend_data_YYYYMMDD.csv
    trend_peaks_YYYYMMDD.csv
    keyword_news_match_YYYYMMDD.csv
    trend_summary_YYYYMMDD.csv
    dashboard_YYYYMMDD.csv
fetch_news.py
extract_keywords.py
google_trends.py
process_data.py
README.md

注意点・補足
	•	各スクリプトは実行時に当日の日付（YYYYMMDD）でファイルを入出力します。
	•	BASE_DIR のパスは各スクリプト内で固定の絶対パスになっているため、実環境に合わせて適宜変更してください。
	•	形態素解析は名詞のみに絞っています。用途に応じて変更可能です。
	•	Googleトレンドの利用制限に注意しながらご利用ください。
	•	matplotlibの日本語表示はMacの「Hiragino Sans」を指定しています。Windows等はフォント設定を調整してください。
