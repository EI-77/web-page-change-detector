# Web Page Change Detector

指定したWebページの更新を自動で検知するPythonツールです。

本ツールは，実行時にページ内容を取得し、前回取得時の内容と比較することで、ページに変更があったかどうかを判定します。

監視結果はCSVファイルとして保存されるため、Webサイトの更新履歴を記録することができます。

以下のような用途で利用できます。

* 求人ページの更新監視
* 商品ページの更新監視
* キャンペーンページの更新監視
* お知らせページの更新監視
* 特定サイトの更新チェック

---

## 主な機能

### Webページ更新監視

指定したURLの内容を取得し、前回実行時と比較して更新の有無を判定します。

### 複数URL対応

複数のURLを登録して同時に監視できます。

```python
URLS = [
    "https://example.com",
    "https://example.org",
]
```

### 更新履歴保存

監視結果をCSVファイルとして保存します。

更新があった日時や判定結果を後から確認できます。

### エラーログ記録

通信エラーやページ取得失敗時も実行結果を記録します。

---

## 使用技術

* Python
* requests
* BeautifulSoup
* hashlib
* json
* csv

---

## 実行方法

### 1. リポジトリを取得

```bash
git clone <repository_url>
```

### 2. ディレクトリへ移動

```bash
cd web-page-change-detector
```

### 3. 必要ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 4. 監視対象URLを設定

`web_page_change_detector.py` を開き、監視したいURLを設定します。

例：

```python
URLS = [
    "https://example.com",
]
```

### 5. プログラムを実行

```bash
python web_page_change_detector.py
```

または

```bash
py web_page_change_detector.py
```

---

## 実行結果

### 初回実行

初回実行時は比較対象が存在しないため、`first_check` として記録されます。

```csv
url,status,checked_at
https://example.com,first_check,2026-05-31 20:00:00
```

### 変更なし

ページ内容に変更がない場合は `no_change` が記録されます。

```csv
url,status,checked_at
https://example.com,no_change,2026-05-31 21:00:00
```

### 変更あり

ページ内容が変更された場合は `changed` が記録されます。

```csv
url,status,checked_at
https://example.com,changed,2026-05-31 22:00:00
```

---

## 出力ファイル

### change_log.csv

監視結果を保存します。

保存場所：

```text
data/change_log.csv
```

### hashes.json

各URLの最新ハッシュ値を保存します。

保存場所：

```text
data/hashes.json
```

---

## 判定結果一覧

| Status      | 内容      |
| ----------- | ------- |
| first_check | 初回実行    |
| no_change   | 変更なし    |
| changed     | 内容変更あり  |
| error       | ページ取得失敗 |

---

## ディレクトリ構成

```text
web-page-change-detector/
├── web_page_change_detector.py
├── requirements.txt
├── README.md
└── data/
    ├── hashes.json
    └── change_log.csv
```

---

## 動作の仕組み

本ツールはページ内の表示テキストを取得し、その内容からSHA256ハッシュ値を生成します。

例えば以下のページ内容が存在するとします。

```text
Hello
World
```

取得したテキストからハッシュ値を生成し、前回保存したハッシュ値と比較します。

ハッシュ値が同じ場合は変更なし、異なる場合は変更ありと判定します。

この方法により、ページ全体のテキストを保存しなくても高速に更新検知を行うことができます。

---

## 注意事項

* scriptタグおよびstyleタグの内容は監視対象外です。
* 表示テキストのみを比較対象としています。
* ページ内容が1文字でも変化すると変更ありと判定されます。
* 本ツールは更新の有無を判定するものであり、変更箇所の詳細は出力しません。

---

# English

## Overview

Web Page Change Detector is a Python tool that automatically detects updates on web pages.

The tool retrieves page content, compares it with the content from the previous execution, and determines whether the page has changed.

Monitoring results are saved as CSV files, allowing users to track website updates over time.

Typical use cases include:

* Job posting monitoring
* Product page monitoring
* Campaign page monitoring
* Announcement page monitoring
* General website update tracking

---

## Features

* Web page change detection
* Multiple URL support
* Monitoring history export
* Error logging
* CSV output
* JSON-based hash storage

---

## Tech Stack

* Python
* requests
* BeautifulSoup
* hashlib
* json
* csv

---

## Usage

1. Clone this repository.
2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Configure target URLs.

```python
URLS = [
    "https://example.com",
]
```

4. Run the program.

```bash
python web_page_change_detector.py
```

---

## Output Files

### change_log.csv

Stores monitoring history.

### hashes.json

Stores the latest hash value for each monitored URL.

---

## Notes

* Script and style contents are excluded.
* Only visible page text is monitored.
* Any text change generates a different hash.
* The tool detects whether a page has changed, but does not identify what changed.

