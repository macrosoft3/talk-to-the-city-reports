# Talk to the City

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.txt)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)

Talk to the City（TttC）は、公開コメント、アンケート、審議会の意見をAIを使ったインタラクティブで多言語対応のレポートに変換するオープンソースプラットフォームです。[AI Objectives Institute](http://aiobjectives.org)によって構築され、最先端の自然言語処理と大規模言語モデルを使用して、大規模な洞察抽出、コンセンサス識別、視点の可視化を実現します。

## 目次

- [クイックオーバービュー](#クイックオーバービュー)
- [構築できるもの](#構築できるもの)
- [プロジェクト構成](#プロジェクト構成)
- [はじめに](#はじめに)
- [サポート・リソース](#サポートリソース)
- [貢献](#貢献)
- [ライセンス](#ライセンス)

## クイックオーバービュー

Talk to the Cityは2つの相互補完的なアプリケーションで構成されています:

### 🔄 **Scatter Reports** (Python + Next.js)

CSV形式の公開コメントからAI生成サマリー付きの静的インタラクティブな散布図レポートを生成するCLIベースのツール。

**ライブ例:**

- [Recursive Public](https://tttc.dev/recursive)
- [GenAI Taiwan](https://tttc.dev/genai)
- [Heal Michigan](https://tttc.dev/heal-michigan)

### 🎯 **Turbo** (TypeScript + Svelte)

複雑なLLM駆動レポート構築、リアルタイム協働、カスタマイズ可能なワークフローをサポートするグラフベースの計算パイプラインアプリケーション。

**ライブ例:**

- [Heal Michigan](https://tttc-turbo.web.app/report/heal-michigan-9)
- [台湾同性婚](https://tttc-turbo.web.app/report/taiwan-zh)
- [Minaプロトコル](https://tttc-turbo.web.app/report/mina-protocol)

## 構築できるもの

✨ **抽出** AIを使用して数千のコメントから主要な主張を抽出  
🗂️ **クラスタリング** セマンティック分析による類似観点のグループ化  
🏷️ **ラベリング** クラスタの自動ラベリングと要約  
📊 **可視化** インタラクティブな散布図またはカスタムダッシュボードとしてのデータ可視化  
🌍 **翻訳** レポートの多言語翻訳  
🔗 **構築** 依存グラフを使った複雑なAIパイプラインの構築

### ⚠️ AI安全性に関する免責事項

TttCは公開審議におけるジェネレーティブAIの探索的研究プロジェクトです。**大規模言語モデル（LLM）には既知のバイアスがあり、信頼できない結果を生成する可能性があります。**これらの問題を軽減するために積極的に取り組んでいますが、この段階では保証をいたしません。

**重大な決定には、このパイプラインの結果のみに依存せず、独立した検証を行ってください。**

## プロジェクト構成

```
talk-to-the-city-reports/
├── scatter/               # Scatter Reportsアプリケーション (Python + Next.js)
│   ├── pipeline/          # AI処理パイプライン
│   ├── next-app/          # レポート可視化フロントエンド
│   └── configs/           # プロジェクト設定ファイル
├── turbo/                 # Turboアプリケーション (TypeScript + Svelte)
│   ├── src/
│   │   ├── lib/           # 計算関数とユーティリティ
│   │   ├── components/    # Svelte UIコンポーネント
│   │   └── routes/        # SvelteKitルート
│   └── static/            # 静的アセット
└── LICENSE.txt            # Apache 2.0 ライセンス
```

## はじめに

ニーズに合わせてアプリケーションを選択してください:

### オプション1: Scatter Reports（シンプル、CSV入力推奨）

公開コメントを含むCSVファイルをインタラクティブレポートに変換する場合に最適です。

**前提条件:**

- Python 3.10以上
- Node.js 18以上とnpm
- [OpenAI APIキー](https://platform.openai.com/api-keys)
- [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)

**クイックスタート:**

```bash
# クローンしてナビゲート
git clone https://github.com/AIObjectives/talk-to-the-city-reports.git
cd talk-to-the-city-reports/scatter

# Python環境をセットアップ
python -m venv venv
source venv/bin/activate  # Windows の場合: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"

# Node.js依存関係をインストール
cd next-app && npm install && cd ..

# OpenAI APIを設定
cd pipeline && echo "OPENAI_API_KEY=your-api-key-here" > .env && cd ..

# サンプルデータで実行
cd pipeline && python main.py configs/example-polis.json
```

**レポートを表示:**

```bash
npm install -g http-server
http-server -p 8080
# http://localhost:8080/pipeline/outputs/example-polis/report/ を開く
```

**独自のレポートを生成:**

1. `comment-id`, `comment-body` カラムを含むCSVファイルを準備（オプション: `agree`, `disagree`, `video`, `interview`, `timestamp`）
2. `pipeline/inputs/my-project.csv` にコピー
3. `pipeline/configs/my-project.json` を作成（`example-polis.json` からコピー）
4. 実行: `python main.py configs/my-project.json`

📖 詳細なドキュメントは[scatter/README.md](scatter/README.md)を参照してください。

### オプション2: Turbo（高度なグラフベースパイプライン）

複雑でカスタマイズ可能なLLM駆動アプリケーションをリアルタイム協働で構築する場合向け。

**前提条件:**

- Node.js 18以上
- Firebaseアカウント（デプロイ向け；ローカル開発も対応）
- Google Cloudクレデンシャル（オプション、クラウド機能向け）

**クイックスタート:**

```bash
# クローンしてナビゲート
git clone https://github.com/AIObjectives/talk-to-the-city-reports.git
cd talk-to-the-city-reports/turbo

# 依存関係をインストール
npm install

# 環境をセットアップ
cp .env.example .env
# Firebaseと設定の詳細を入力

# 開発サーバーを起動
npm run dev
```

**利用可能なコマンド:**

```bash
npm run dev          # 開発サーバーを起動 (http://localhost:5173)
npm run build        # 本番用にビルド
npm run preview      # 本番ビルドをプレビュー
npm test             # テストを実行
npm run lint         # コード形式をチェック
npm run format       # コードをフォーマット
```

📖 詳細なセットアップ、Firebase設定、デプロイ手順は[turbo/README.md](turbo/README.md)を参照してください。

## サポート・リソース

### ドキュメント

- **Scatter Reports:** [scatter/README.md](scatter/README.md) - 完全なセットアップ、使用方法、パイプラインアーキテクチャ
- **Turbo:** [turbo/README.md](turbo/README.md) - 高度な設定、Firebase設定、開発ガイド
- **貢献:** [scatter/CONTRIBUTING.md](scatter/CONTRIBUTING.md) と [turbo/CONTRIBUTOR_GUIDE.md](turbo/CONTRIBUTOR_GUIDE.md)

### ヘルプの取得

- **Issues & Bugs:** [GitHub Issues](https://github.com/AIObjectives/talk-to-the-city-reports/issues)
- **Discussions:** [GitHub Discussions](https://github.com/AIObjectives/talk-to-the-city-reports/discussions)
- **お問い合わせ:** [AI Objectives Institute](http://aiobjectives.org)までご連絡ください

### 学習リソース

- **ブログ記事:** [Talk to the City: An Open-Source AI Tool to Scale Deliberation](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation)
- **AIパイプラインガイド:** [AI Pipeline Engineering Guide #1](https://tttc-turbo.web.app/docs/ai-pipe-guide)
- **ユーザードキュメント:** [tttc-turbo.web.app/docs](https://tttc-turbo.web.app/docs)

## 貢献

オープンソースコミュニティからの貢献を歓迎します！主要機能の作業を開始する前に、以下をお願いします:

1. [GitHub Issues](https://github.com/AIObjectives/talk-to-the-city-reports/issues)で既存作業を確認
2. 貢献ガイドラインを確認:
   - [Scatter CONTRIBUTING.md](scatter/CONTRIBUTING.md)
   - [Turbo CONTRIBUTOR_GUIDE.md](turbo/CONTRIBUTOR_GUIDE.md)
3. 実質的な作業を開始する前に[AI Objectives Institute](http://aiobjectives.org)にご連絡ください

**貢献方法:**

- 🐛 バグ報告と機能リクエスト
- 📝 ドキュメント改善
- ✨ 新しいパイプラインステップやコンポーネントの追加
- 🌍 言語翻訳の追加
- 🧪 テストの記述と堅牢性の向上
- 🚀 パフォーマンスの最適化

## 開発

### コード品質

両プロジェクトはコード標準を強制しています:

- **TypeScript/Svelte（Turbo）:** ESLint、Prettier、TypeScript strict mode
- **Python（Scatter）:** Blackフォーマッタ推奨

PRを提出する前にフォーマッタを実行してください:

```bash
# Turbo
npm run format
npm run lint

# Scatter
# Blackでフォーマット
black pipeline/
```

### テストの実行

```bash
# Turbo
npm test                 # すべてのテストを実行
npm run test-watch      # ウォッチモード
npm run test-ui         # カバレッジ付きUI

# Scatter
# テストはパイプラインの一部として実行
```

## テクノロジースタック

### Scatter Reports

- **バックエンド:** Python 3.10以上、LangChain、OpenAI API、UMAP、BERTopic
- **フロントエンド:** Next.js、React、Tailwind CSS
- **ML/NLP:** scikit-learn、spaCy、sentence-transformers

### Turbo

- **フロントエンド:** SvelteKit、Svelte、TypeScript、Tailwind CSS
- **状態管理:** Stores、リアクティブ変数
- **UIコンポーネント:** Svelte Material UI、SvelteFlow
- **バックエンド:** Firebase/Firestore、Google Cloud Storage
- **テスト:** Vitest、Svelte Testing Library

## ライセンス

このプロジェクトは**Apache License 2.0**の下でライセンスされています - 詳細は[LICENSE.txt](LICENSE.txt)を参照してください。

Turboアプリケーションは**GPL v3**の下でライセンスされているコンポーネントを使用しています - 詳細は[turbo/LICENSE.md](turbo/LICENSE.md)を参照してください。

## メンテナー

[AI Objectives Institute](http://aiobjectives.org)によってメンテナンスされています。これはAIアライメントと有益なAI研究に焦点を当てた非営利研究機関です。
