#!/bin/bash
# Difyプロジェクトのセットアップを検証

# 使い方:
#   bash scripts/verify-setup.sh
#
# このスクリプトは必要なセットアップ手順がすべて完了しているかを確認します

echo "Difyプロジェクトのセットアップを検証中..."
echo ""

# .envファイルを確認
echo "1. .env設定を確認中..."
if [ -f ".env" ]; then
    echo "   ✅ .envファイルが存在します"

    # 必須変数を確認
    if grep -q "DIFY_BASE_URL" .env && \
       grep -q "DIFY_EMAIL" .env && \
       grep -q "DIFY_PASSWORD" .env; then
        echo "   ✅ 必須環境変数が設定されています"
    else
        echo "   ❌ 必須環境変数が不足しています"
        exit 1
    fi
else
    echo "   ❌ .envファイルが見つかりません。最初にセットアップを実行してください。"
    exit 1
fi

echo ""
echo "2. Dockerセットアップを確認中..."
if docker --version > /dev/null 2>&1; then
    echo "   ✅ Dockerがインストールされています"
else
    echo "   ❌ Dockerがインストールされていません"
    exit 1
fi

# docker-composeを確認
if docker compose version > /dev/null 2>&1; then
    echo "   ✅ Docker Composeが利用可能です"
else
    echo "   ❌ Docker Composeが利用できません"
    exit 1
fi

echo ""
echo "3. Dify接続をテスト中..."
docker compose run --rm dify-creator login > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "   ✅ Difyへの接続に成功しました"
else
    echo "   ❌ Difyへの接続に失敗しました"
    echo "   .env設定を確認し、認証情報を確認してください"
    exit 1
fi

echo ""
echo "✅ すべてのセットアップ検証チェックに合格しました！"
echo ""
echo "Dify-Creatorを使用する準備ができました。次を試してください:"
echo "  - 新しいアプリを作成: dify-new-app"
echo "  - アプリを編集: dify-edit-app"
echo "  - アプリを管理: managing-dify-apps"
