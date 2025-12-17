# Talk to the City (TttC) - Scatter Reports

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](../LICENSE.txt)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)

<img width="400" alt="インタラクティブな散布図の可視化" src="https://github.com/AIObjectives/talk-to-the-city-reports/assets/3934784/57cc6367-0808-40f0-980a-540530ff0866">
<img width="400" alt="クラスター分析レポート" src="https://github.com/AIObjectives/talk-to-the-city-reports/assets/3934784/aaf45844-5a19-41c8-8943-78866db9f666">

## Talk to the City とは？

Talk to the City (TttC) は、コメントを含むCSVファイルをインタラクティブな多言語HTMLレポートに変換するAI駆動パイプラインです。最先端の自然言語処理技術を使用して以下を実現します：

✅ **抽出** - 数千のコメントから主要な論点を抽出  
✅ **クラスタリング** - 意味的類似性に基づいて類似した意見をグループ化  
✅ **ラベリング** - 各クラスターに自動的に説明的なラベルを付与  
✅ **可視化** - インタラクティブな散布図マップとしてデータを視覚化  
✅ **翻訳** - レポートを複数の言語に翻訳

**実例:**

- [Recursive Public](https://tttc.dev/recursive) - Pol.isデータと投票コンセンサスフィルター
- [GenAI Taiwan](https://tttc.dev/genai) - 台湾の公開協議からのバイリンガルレポート（英語/中国語）
- [Heal Michigan](https://tttc.dev/heal-michigan) - コミュニティ対話分析

AI アライメントに焦点を当てた非営利研究組織 [AI Objectives Institute](http://aiobjectives.org) によって開発されました。詳細は[ブログ記事](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation)をご覧ください。

## ⚠️ AI安全性に関する免責事項

TttCは、公開討議のための生成AIの可能性を探求する研究プロジェクトです。**大規模言語モデル（LLM）にはバイアスが存在し、信頼性の低い結果を生成する可能性があります。** これらの問題を軽減するために積極的に取り組んでいますが、現段階では保証を提供できません。

**独立した検証なしに、このパイプラインの結果のみに依存して重要な決定を行わないでください。**

---

## 🚀 クイックスタート

### 前提条件

開始する前に、以下が必要です：

- **Python 3.10+** がインストール済み（[ダウンロード](https://www.python.org/downloads/)）
- **Node.js & npm** レポート可視化用（[ダウンロード](https://nodejs.org/)）
- **OpenAI APIキー**（[こちらから取得](https://platform.openai.com/api-keys)）
- **Git LFS** 大きなサンプルファイル用（[インストールガイド](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)）
- 必須カラムを含む**CSV形式**のデータ（[CSV形式](#csv形式)を参照）

### インストール

1. **リポジトリをクローン：**

   ```bash
   git clone https://github.com/AIObjectives/talk-to-the-city-reports.git
   cd talk-to-the-city-reports/scatter
   ```

2. **Python環境をセットアップ：**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -c "import nltk; nltk.download('stopwords')"
   ```

3. **Node.js依存関係をインストール：**

   ```bash
   cd next-app
   npm install
   cd ..
   ```

4. **OpenAI APIキーを設定：**

   ```bash
   cd pipeline
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

   > 💡 **セキュリティ注意:** `.env` ファイルをバージョン管理にコミットしないでください。既に `.gitignore` に記載されています。

---

## 📊 使用方法

### サンプルデータで実行

付属のサンプルデータセットでパイプラインをテスト：

```bash
cd pipeline
python main.py configs/example-polis.json
```

これにより `inputs/example-polis.csv`（4件のコメント）が処理され、`outputs/example-polis/report/` にレポートが生成されます。

**その他のサンプル:**

- `example-videos.json` - ビデオタイムスタンプ機能を含む

### 独自のレポートを生成

#### ステップ1: データを準備

以下の必須カラムを含むCSVファイルを作成：

| カラム         | 型     | 説明                   |
| -------------- | ------ | ---------------------- |
| `comment-id`   | string | 各コメントの一意識別子 |
| `comment-body` | string | 実際のコメントテキスト |

**オプションカラム:** `agree`, `disagree`, `video`, `interview`, `timestamp`（[CSV形式](#csv形式)を参照）

CSVをinputsフォルダにコピー：

```bash
cp /path/to/your/data.csv pipeline/inputs/my-project.csv
```

#### ステップ2: 設定ファイルを作成

サンプル設定をコピーしてカスタマイズ：

```bash
cp pipeline/configs/example-polis.json pipeline/configs/my-project.json
```

`my-project.json` を編集：

```json
{
  "name": "プロジェクト名",
  "question": "主な議論トピックは何ですか？",
  "input": "my-project",
  "model": "gpt-3.5-turbo",
  "extraction": {
    "limit": 1000,
    "workers": 3
  },
  "clustering": {
    "clusters": 8
  },
  "translation": {
    "languages": ["Japanese", "Spanish"],
    "flags": ["JP", "ES"]
  }
}
```

#### ステップ3: パイプラインを実行

```bash
cd pipeline
python main.py configs/my-project.json
```

**パイプラインオプション:**

- `-f` - 全ステップを強制的に再実行（キャッシュを無視）
- `-o <step>` - 特定のステップのみ実行
- `-skip-interaction` - 確認プロンプトをスキップ

**例:**

```bash
python main.py configs/my-project.json -f
```

---

## 📱 レポートの表示とデプロイ

### ローカルプレビュー

生成されたレポートは `pipeline/outputs/my-project/report/` にあります。ローカルで配信：

```bash
# プロジェクトルートディレクトリから
npm install -g http-server
http-server -p 8080
open http://localhost:8080/pipeline/outputs/my-project/report/
```

### 本番環境へのデプロイ

レポートは静的ウェブサイトです—どこでもデプロイ可能：

**推奨プラットフォーム:**

- [Vercel](https://vercel.com/) - `vercel deploy pipeline/outputs/my-project/report`
- [Netlify](https://www.netlify.com/) - `report` フォルダをドラッグ＆ドロップ
- [GitHub Pages](https://pages.github.com/) - `gh-pages` ブランチにコミット＆プッシュ
- 任意の静的ホスト（AWS S3、Azure Storageなど）

> ⚠️ **重要:** HTMLは相対パスを使用します。適切なアセット読み込みのため、URLに末尾のスラッシュを含めてください（例: `https://example.com/report/`）。

---

## 🔧 パイプラインアーキテクチャ

パイプラインは9つの連続したステップで構成されています：

| ステップ             | 入力               | 出力                | 説明                                        |
| -------------------- | ------------------ | ------------------- | ------------------------------------------- |
| 1. **Extraction**    | CSVコメント        | `args.csv`          | LLMを使用して主要な論点を抽出               |
| 2. **Embedding**     | 論点               | `embeddings.pkl`    | テキストをベクトルに変換                    |
| 3. **Clustering**    | 埋め込み           | `clusters.csv`      | 類似した論点をグループ化（UMAP + BERTopic） |
| 4. **Labelling**     | クラスター         | `labels.csv`        | 説明的なラベルを生成                        |
| 5. **Takeaways**     | クラスター         | `takeaways.csv`     | 主要な洞察を抽出                            |
| 6. **Overview**      | 全データ           | `overview.txt`      | エグゼクティブサマリーを生成                |
| 7. **Translation**   | テキストコンテンツ | `translations.json` | ターゲット言語に翻訳                        |
| 8. **Aggregation**   | 全出力             | `result.json`       | 全データを結合                              |
| 9. **Visualization** | 集約データ         | `report/`           | インタラクティブなHTMLレポートを構築        |

各ステップは結果をキャッシュ—依存関係やパラメータが変更された場合のみ再実行されます。

---

## 📝 CSV形式

### 必須カラム

| カラム         | 型     | 説明             | 例                         |
| -------------- | ------ | ---------------- | -------------------------- |
| `comment-id`   | string | 一意識別子       | `"C001"`, `"12345"`        |
| `comment-body` | string | コメントテキスト | `"AIは安全性を優先すべき"` |

### オプションカラム

| カラム      | 型     | 説明                 | 例                                  |
| ----------- | ------ | -------------------- | ----------------------------------- |
| `agree`     | number | 賛成票数             | `42`                                |
| `disagree`  | number | 反対票数             | `7`                                 |
| `video`     | string | ビデオURL            | `"https://youtube.com/watch?v=..."` |
| `interview` | string | インタビュイー名     | `"田中太郎"`                        |
| `timestamp` | string | ビデオタイムスタンプ | `"00:15:30"`                        |

**CSV例:**

```csv
comment-id,comment-body,agree,disagree
C001,"AI開発には倫理的ガイドラインが必要",128,12
C002,"AI安全性への焦点は最重要",95,8
C003,"AI開発を一時停止すべき",45,67
```

---

## ⚙️ 設定リファレンス

### 必須パラメータ

```json
{
  "input": "my-data", // CSVファイル名（.csv なし）
  "question": "議論トピック？" // 参加者に尋ねられた主な質問
}
```

### オプションパラメータ

#### グローバル設定

```json
{
  "name": "プロジェクト名", // 表示名（オプション）
  "intro": "**Markdown** 序文", // プロジェクト紹介（オプション）
  "model": "gpt-3.5-turbo" // デフォルトLLMモデル
}
```

#### ステップ固有の設定

**Extraction（抽出）**

```json
"extraction": {
  "model": "gpt-4",              // グローバルモデルを上書き
  "prompt_file": "custom",       // カスタムプロンプト（prompts/extraction/ 内）
  "prompt": "Extract...",        // または完全なプロンプトテキスト
  "limit": 1000,                 // 処理する最大コメント数
  "workers": 3                   // 並列ワーカー数（1-10）
}
```

**Clustering（クラスタリング）**

```json
"clustering": {
  "clusters": 8                  // トピッククラスター数（デフォルト: 8）
}
```

**Labelling & Takeaways（ラベリングと要点抽出）**

```json
"labelling": {
  "model": "gpt-4",
  "sample_size": 30              // ラベリング用のクラスターあたりの論点数
},
"takeaways": {
  "sample_size": 30              // 洞察用のクラスターあたりの論点数
}
```

**Translation（翻訳）**

```json
"translation": {
  "model": "gpt-4",              // 翻訳用により良いモデルを使用
  "languages": ["Japanese", "Spanish", "French"],
  "flags": ["JP", "ES", "FR"]    // フラグ用のISO国コード
}
```

**Visualization（可視化）**

```json
"visualization": {
  "replacements": [              // UI内のテキスト置換
    {"replace": "AI", "by": "人工知能"}
  ]
}
```

### カスタムプロンプト

カスタムプロンプトを `pipeline/prompts/<step>/` に保存：

- `extraction/` - 論点抽出プロンプト
- `labelling/` - クラスターラベリングプロンプト
- `takeaways/` - 重要な洞察プロンプト
- `overview/` - サマリー生成プロンプト
- `translation/` - 翻訳指示

設定で `"prompt_file": "your-file-name"` で参照（`.txt` なし）。

---

## 📂 出力構造

実行成功後、`pipeline/outputs/my-project/` に出力が生成されます：

```
outputs/my-project/
├── args.csv              # コメントから抽出された論点
├── embeddings.pkl        # ベクトル埋め込み（キャッシュ用）
├── clusters.csv          # 各論点のクラスター割り当て
├── labels.csv            # 各クラスターの生成ラベル
├── takeaways.csv         # クラスターごとの重要な洞察
├── overview.txt          # エグゼクティブサマリー
├── translations.json     # すべての翻訳コンテンツ
├── result.json           # 集約データ（レポートで使用）
├── status.json           # パイプライン実行ステータス
└── report/               # 🌐 インタラクティブHTMLレポート
    ├── index.html
    ├── _next/            # Next.jsアセット
    └── [cluster-pages].html
```

**主要ファイル:**

- **`result.json`** - 可視化で使用される完全な集約データ
- **`status.json`** - 完了したステップ、パラメータ、タイミングを追跡
- **`report/`** - このフォルダをホスティングサービスにデプロイ

> 💡 中間ファイル（CSV/PKL）はキャッシュされます。異なる設定で再実行して未変更のステップをスキップ。

---

## 🐛 トラブルシューティング

### よくある問題

**「Job already running and locked」エラー**

```bash
rm pipeline/outputs/my-project/.lock
```

**依存関係更新後のインポートエラー**

```bash
pip install --upgrade -r requirements.txt
```

**LangChainインポートエラー**

- インポートを更新: `from langchain_openai import ChatOpenAI, OpenAIEmbeddings`
- LLMを直接呼び出す代わりに `.invoke()` を使用: `llm.invoke(messages)`

**大規模データセットでメモリエラー**

- 設定で `extraction.limit` を減らす
- `extraction.workers` 数を下げる
- バッチで処理

### APIレート制限

OpenAIのレート制限に達した場合：

1. `extraction.workers` を `1` に減らす
2. `gpt-4` の代わりに `gpt-3.5-turbo` を使用
3. リクエスト間に遅延を追加（`steps/extraction.py` を修正）

---

## 🤝 貢献

貢献を歓迎します！ガイドラインについては [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

**支援が必要な分野:**

- 🛡️ 改善されたエラーハンドリングとリトライロジック
- ⚡ パフォーマンス最適化
- 📝 より良いドキュメント
- 🧪 テストカバレッジ
- 🌍 追加の言語サポート

大きな作業を開始する前に、[issue を開く](https://github.com/AIObjectives/talk-to-the-city-reports/issues)か、AI Objectives Institute に直接連絡してください。

---

## 📚 リソース

- **ドキュメント:** [完全なAPIドキュメント](https://github.com/AIObjectives/talk-to-the-city-reports)
- **ブログ:** [AIによる討議のスケール化](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation)
- **サンプル:** [ライブレポート](https://tttc.dev)
- **コミュニティ:** [GitHub Discussions](https://github.com/AIObjectives/talk-to-the-city-reports/discussions)

---

## 👥 クレジットとメンテナー

**開発:** [AI Objectives Institute](http://aiobjectives.org)

**貢献者:**

- [@Klingefjord](https://github.com/Klingefjord) - 初期パイプライン開発
- [@lightningorb](https://github.com/lightningorb) - コアアーキテクチャ
- Recursive Public チーム（Chatham House、vTaiwan、OpenAI） - サンプルデータセット

---

## 📄 ライセンス

このプロジェクトは **Apache License 2.0** の下でライセンスされています - 詳細は [LICENSE.txt](../LICENSE.txt) をご覧ください。

---

## 🔗 関連プロジェクト

- **[tttc-light-js](https://github.com/AIObjectives/tttc-light-js)** - アクティブな開発（次世代バージョン）
- **[TttC Turbo](../turbo/)** - グラフベースのレポートアプリケーション（TypeScript）

> **注意:** このリポジトリ（Scatter Reports）はメンテナンスモードです。アクティブな開発は tttc-light-js で継続されています。
