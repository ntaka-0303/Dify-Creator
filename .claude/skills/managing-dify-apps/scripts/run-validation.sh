#!/bin/bash
# DSL設定を検証

# 使い方:
#   bash scripts/run-validation.sh <DSLファイルのパス>
#
# 例:
#   bash scripts/run-validation.sh app.dsl.yml

DSL_FILE="${1:-app.dsl.yml}"

if [ ! -f "$DSL_FILE" ]; then
    echo "❌ エラー: DSLファイルが見つかりません: $DSL_FILE"
    exit 1
fi

echo "DSLを検証中: $DSL_FILE"
docker compose run --rm dify-creator validate --dsl "$DSL_FILE"
