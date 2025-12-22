#!/bin/bash
# Dify接続をテスト

# 使い方:
#   bash scripts/test-connection.sh
#
# このスクリプトはDify接続が機能していること、
# および認証情報が正しく設定されていることを確認します。

echo "Dify接続をテスト中..."
docker compose run --rm dify-creator login

# 終了ステータスを確認
if [ $? -eq 0 ]; then
    echo "✅ 接続成功！"
    exit 0
else
    echo "❌ 接続失敗。.env設定を確認してください:"
    echo "   - DIFY_BASE_URL"
    echo "   - DIFY_EMAIL"
    echo "   - DIFY_PASSWORD"
    exit 1
fi
