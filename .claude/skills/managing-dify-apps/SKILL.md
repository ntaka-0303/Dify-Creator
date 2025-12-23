---
name: Difyアプリを管理・作成する
description: Difyアプリの作成・編集・検証・デプロイを自動化します。新規アプリ作成、既存アプリ修正、設定テストが必要な場合に使用してください。YAML生成・編集、検証、テスト実行をすべて自動で行います。
---

# Difyアプリを管理・作成する

ブラウザを開かずにDifyアプリを効率的に作成・管理できます。このSkillはアプリのライフサイクル全体をサポート：作成 → 修正 → 検証 → デプロイ

## このSkillでできること

- **新しいアプリを作成**: 自然言語説明からDifyアプリを自動生成
- **既存アプリを編集**: プロンプト・ワークフロー・変数・ロジックを修正
- **設定を検証**: デプロイ前にDSL構文をチェック
- **テスト・デプロイ**: テスト実行とDifyへの同期を自動実行
- **反復修正に対応**: 検証フィードバックループで効率的に改善

## クイックスタート

### 新しいアプリを作成

1. 作りたいアプリを説明：「顧客からの質問に自動で答えるチャットボット」
2. アプリの種類を指定：Q&Aチャット、ワークフロー、条件分岐、API連携
3. Claudeが自動処理：YAML生成 → 検証 → Difyへアップロード → テスト実行

### 既存のアプリを編集

1. アプリIDと修正内容を指定：「プロンプトをもっと丁寧な回答にして」
2. Claudeが自動処理：現在の設定をダウンロード → 修正 → 検証 → テスト実行
3. 結果を確認して、満足するまで繰り返す

### テストと検証

いつでも検証を実行してデプロイ前に設定エラーをキャッチできます。

## コアワークフロー

詳細は [reference/core/workflows.md](reference/core/workflows.md) を参照：
- 異なるタイプのアプリ作成
- 既存アプリの編集と反復改善
- 検証とエラーハンドリング
- よくある問題のトラブルシューティング

## 主要リソース

**テンプレートと例**：
[reference/technical/templates.md](reference/technical/templates.md) を参照：
- 利用可能なDSLテンプレート5つ
- 各テンプレートの使い分け
- テンプレート構造とカスタマイズ方法

**実際のテンプレートファイル**：
- `examples/templates/DeepResearch.yml` - 深い調査を行う高度なチャットボット
- `examples/templates/ウェブの検索と要約のワークフローパターン.yml` - Web検索と要約のワークフロー
- `examples/templates/投資分析レポート コパイロット.yml` - Yahoo Finance APIを使った投資分析エージェント
- `examples/templates/知識リトリーバル + チャットボット.yml` - 知識検索機能付きチャットボット
- `examples/templates/質問分類器 + 知識 + チャットボット.yml` - 質問分類と知識検索を組み合わせたチャットボット

**テスト用サンプル入力**：
- `examples/inputs.json` - アプリのテスト実行用サンプルデータ

**DSL設定**：
[reference/technical/dsl-guide.md](reference/technical/dsl-guide.md) を参照：
- DSL YAML構造の概要
- 必須フィールドとセクション
- よくある設定パターン

**トラブルシューティング**：
[reference/troubleshooting.md](reference/troubleshooting.md) を参照：
- よくあるエラーと解決方法
- 接続の問題
- 検証の失敗
- テスト実行の問題

## 検証とフィードバックループ

品質を確保するため、このSkillは検証フィードバックループを使用：

1. **作成または修正** - アプリ設定を作成・修正
2. **検証** - YAML構文と構造をチェック
3. **プレビュー** - 変更内容を確認してから適用
4. **テスト** - サンプル入力でアプリを実行
5. **反復改善** - 結果が期待と異なる場合は修正

エラーメッセージは具体的な問題を指摘するので、修正が簡単です。

## 自動化スクリプト

このSkillは以下のスクリプトを使って検証とテストを自動実行します：

**検証スクリプト**：
```bash
bash scripts/run-validation.sh app.dsl.yml
```
- DSL YAMLの構文と構造を検証
- エラーがあれば詳細なメッセージを返す
- 実装の詳細: [scripts/run-validation.sh](scripts/run-validation.sh)

**接続テスト**：
```bash
bash scripts/test-connection.sh
```
- Difyサーバーへの接続を確認
- 認証情報が正しいかを検証
- 実装の詳細: [scripts/test-connection.sh](scripts/test-connection.sh)

**テスト実行**：
```bash
bash scripts/run-test-inputs.sh <app-id>
```
- `examples/inputs.json`のサンプルデータでアプリをテスト
- 実際の出力を確認
- 実装の詳細: [scripts/run-test-inputs.sh](scripts/run-test-inputs.sh)

これらのスクリプトはSkillが自動的に実行するため、手動で実行する必要はありません。

## サポートするアプリタイプ

- **Q&Aチャットボット**: シンプルな質問応答
- **ワークフロー**: 複数ステップの処理
- **条件分岐ロジック**: 判定分岐とルーティング
- **API連携**: 外部サービスとの連携

詳細は [reference/technical/templates.md](reference/technical/templates.md) を参照。

## 使う前に確認すること

- Difyアカウントと認証情報（メール・パスワード）
- Difyプロジェクトが既にセットアップされていること（`Difyプロジェクトをセットアップする` Skillを参照）
- アプリの目的と入出力の基本的な理解

初期セットアップは `Difyプロジェクトをセットアップする` Skillを先に実行してください。
