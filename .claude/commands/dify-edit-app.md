# dify-edit-app（既存アプリを編集）

⚠️ **[重要] このコマンドは以下のSkillに統合されました：**

> **新しいSkill: [`managing-dify-apps`](./../skills/managing-dify-apps/SKILL.md)**
>
> Agent-Skillsベストプラクティスに準拠した新構造です。
> より効率的で柔軟な操作が可能になりました。
>
> **推奨**: 新しいSkillの使用をお勧めします。このコマンドは後方互換性のため保持されます。

---

**ClaudeCodeが既存のDifyアプリを修正します。ユーザーは「どう修正したいか」説明するだけです。**

---

## ユーザーに確認すること

### 1. アプリの ID を確認

Dify のウェブサイトでアプリを開いた URL から、ID を探します。

例：
```
https://cloud.dify.ai/app/abc123def456/overview
                        ^^^^^^^^^^^^^^
                         これが app_id
```

ユーザーに app_id を聞いてください。

### 2. 修正内容

何を修正したいのか、**日本語で詳しく説明**してもらってください。

例：
- 「プロンプト（指示文）を変更して、より丁寧な応答にしたい」
- 「処理の流れを追加して、複数のステップにしたい」
- 「プロンプトの言語を英語から日本語に変える」
- 「新しく条件分岐を追加したい」

---

## エージェントの実行内容

以下をすべて自動実行します：

### ステップ1：Difyからアプリをダウンロード

```bash
docker compose run --rm dify-creator export \
  --app-id <ユーザーが指定したapp_id> \
  --out app.dsl.yml
```

現在のアプリ設定を `app.dsl.yml` に保存します。

### ステップ2：修正内容を反映

ユーザーの説明に基づいて、`app.dsl.yml` を修正：
- プロンプト（指示文）を編集
- 変数を追加・変更
- ロジック・ワークフローを更新
- など

### ステップ3：修正内容を確認（ユーザーに見せる）

修正する前に、ユーザーに確認：
- 修正内容の要約を表示
- 「この修正でいいですか？」と聞く

ユーザーが OK なら次へ。修正が必要なら説明を追加してもらう。

### ステップ4：検証

```bash
docker compose run --rm dify-creator validate --dsl app.dsl.yml
```

YAMLが正しいか確認します。

### ステップ5：Difyに上書き保存

```bash
docker compose run --rm dify-creator import \
  --dsl app.dsl.yml \
  --app-id <app_id>
```

修正内容を Dify に反映させます。

### ステップ6：テスト実行

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id <app_id> \
  --inputs-json examples/inputs.json
```

修正がうまく動作しているか確認します。

### ステップ7：結果をユーザーに表示

`artifacts/run_result.json` の結果を要約して、ユーザーに見せます。

期待通りですか？

- **Yes** → 修正完了！
- **No** → 「どこが違いますか？」と聞いて、さらに修正

---

## 修正ループ

期待通りでない場合、以下を繰り返します：

```
ユーザーから追加修正の説明をもらう
        ↓
app.dsl.yml を修正
        ↓
検証 → 上書き保存 → テスト実行
        ↓
結果を確認
        ↓
OK になるまで繰り返す
```

---

## 完了後

修正が完成したら：

1. Dify のウェブサイトで「公開」ボタンを押す
2. または `/dify-edit-app` で追加修正をする
3. 複数人で開発している場合は Git にコミット

---

## 注意点

- 修正内容は詳しくしてください。詳しいほど正確な修正ができます
- テスト実行後、結果がおかしい場合は「何が違うのか」教えてください
- 複雑な修正は何回かに分けることをお勧めします

---

## トラブルシューティング

### エラー：app_id が見つからない

```bash
docker compose run --rm dify-creator login
```

で接続確認してください。

### 修正しても結果が変わらない

キャッシュの問題かもしれません。以下を試してください：

```bash
docker compose run --rm dify-creator sync \
  --dsl app.dsl.yml \
  --app-id <app_id> \
  --inputs-json examples/inputs.json
```

を再度実行
