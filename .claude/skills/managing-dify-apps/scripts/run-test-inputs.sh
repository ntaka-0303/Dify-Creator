#!/bin/bash
# テスト入力でアプリを実行

# 使い方:
#   bash scripts/run-test-inputs.sh <app-id> [入力ファイル] [出力ディレクトリ]
#
# 例:
#   bash scripts/run-test-inputs.sh abc123def456
#   bash scripts/run-test-inputs.sh abc123def456 examples/inputs.json artifacts
#
# 入力ファイルまたは出力ディレクトリが指定されない場合、デフォルトが使用されます:
#   - 入力ファイル: examples/inputs.json
#   - 出力ディレクトリ: artifacts

APP_ID="${1:-}"
INPUTS_FILE="${2:-examples/inputs.json}"
OUTPUT_DIR="${3:-artifacts}"

# 入力を検証
if [ -z "$APP_ID" ]; then
    echo "❌ エラー: アプリIDが必要です"
    echo ""
    echo "使い方: bash scripts/run-test-inputs.sh <app-id> [入力ファイル] [出力ディレクトリ]"
    echo ""
    echo "例:"
    echo "  bash scripts/run-test-inputs.sh abc123def456"
    echo "  bash scripts/run-test-inputs.sh abc123def456 examples/inputs.json artifacts"
    exit 1
fi

if [ ! -f "$INPUTS_FILE" ]; then
    echo "❌ エラー: 入力ファイルが見つかりません: $INPUTS_FILE"
    exit 1
fi

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$OUTPUT_DIR"

echo "$INPUTS_FILE からのテスト入力でアプリ $APP_ID を実行中"
docker compose run --rm dify-creator sync \
  --app-id "$APP_ID" \
  --dsl app.dsl.yml \
  --inputs-json "$INPUTS_FILE" \
  --out-dir "$OUTPUT_DIR"

# 終了ステータスを確認
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ テスト実行完了"
    echo "結果の保存先: $OUTPUT_DIR/run_result.json"

    if [ -f "$OUTPUT_DIR/run_result.json" ]; then
        echo ""
        echo "結果のプレビュー:"
        head -n 20 "$OUTPUT_DIR/run_result.json"
    fi
    exit 0
else
    echo "❌ テスト実行失敗"
    exit 1
fi
