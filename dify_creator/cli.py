from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import yaml

from dify_creator.console_client import (
    DifyConsoleClient,
    DifyConsoleError,
    load_dotenv_if_present,
    read_json_file,
    read_yaml_file,
    write_json_file,
    write_text_file,
)


def _require_env(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise DifyConsoleError(f"{name} が未設定です")
    return v


def cmd_login(_: argparse.Namespace) -> int:
    client = DifyConsoleClient.from_env()
    client.login(email=_require_env("DIFY_EMAIL"), password_plain=_require_env("DIFY_PASSWORD"))
    print("ok")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    client = DifyConsoleClient.from_env()
    client.login(email=_require_env("DIFY_EMAIL"), password_plain=_require_env("DIFY_PASSWORD"))
    dsl = client.export_app(app_id=args.app_id, include_secret=args.include_secret, workflow_id=args.workflow_id)
    if args.out:
        write_text_file(args.out, dsl)
    else:
        print(dsl)
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    client = DifyConsoleClient.from_env()
    client.login(email=_require_env("DIFY_EMAIL"), password_plain=_require_env("DIFY_PASSWORD"))

    yaml_content = read_yaml_file(args.dsl) if args.dsl else None
    result = client.import_app(
        yaml_content=yaml_content,
        yaml_url=args.yaml_url,
        app_id=args.app_id,
        name=args.name,
        description=args.description,
        icon_type=args.icon_type,
        icon=args.icon,
        icon_background=args.icon_background,
    )

    # If pending, confirm
    if result.get("status") == "pending":
        confirm = client.confirm_import(result["id"])
        result = confirm

    if args.out:
        write_json_file(args.out, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    client = DifyConsoleClient.from_env()
    client.login(email=_require_env("DIFY_EMAIL"), password_plain=_require_env("DIFY_PASSWORD"))

    inputs: dict[str, Any]
    if args.inputs_json:
        inputs = read_json_file(args.inputs_json)
        if not isinstance(inputs, dict):
            raise DifyConsoleError("--inputs-json は JSON object である必要があります")
    else:
        inputs = json.loads(args.inputs_inline)
        if not isinstance(inputs, dict):
            raise DifyConsoleError("--inputs-inline は JSON object である必要があります")

    collected = client.run_draft_workflow_collect(app_id=args.app_id, inputs=inputs, max_wait_s=args.max_wait_s)
    if args.out:
        write_json_file(args.out, collected)
    print(json.dumps(collected, ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """
    Validate DSL YAML file for basic structure and required fields
    """
    yaml_text = read_yaml_file(args.dsl)
    try:
        dsl_content = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise DifyConsoleError(f"YAML パースエラー: {e}")

    if not isinstance(dsl_content, dict):
        raise DifyConsoleError("DSL は YAML object (dictionary) である必要があります")

    errors: list[str] = []
    warnings: list[str] = []

    # Check required top-level fields
    required_fields = ["version", "kind", "app"]
    for field in required_fields:
        if field not in dsl_content:
            errors.append(f"必須フィールド '{field}' が見つかりません")

    # Check version format
    version = dsl_content.get("version")
    if version and not isinstance(version, str):
        errors.append(f"'version' は文字列である必要があります（現在: {type(version).__name__}）")

    # Check kind value
    kind = dsl_content.get("kind")
    if kind and kind != "app":
        errors.append(f"'kind' は 'app' である必要があります（現在: {kind}）")

    # Check app section
    app = dsl_content.get("app")
    if app:
        if not isinstance(app, dict):
            errors.append("'app' は object（dictionary）である必要があります")
        else:
            if "name" not in app:
                errors.append("'app.name' は必須です")
            if "mode" not in app:
                errors.append("'app.mode' は必須です")
            else:
                valid_modes = {"workflow", "chat", "agent"}
                if app.get("mode") not in valid_modes:
                    errors.append(f"'app.mode' は {valid_modes} のいずれかである必要があります（現在: {app.get('mode')}）")

    # Check workflow or model_config
    mode = dsl_content.get("app", {}).get("mode")
    if mode == "workflow":
        if "workflow" not in dsl_content:
            errors.append("Workflow モードの場合、'workflow' セクションは必須です")
        else:
            workflow = dsl_content.get("workflow")
            if not isinstance(workflow, dict):
                errors.append("'workflow' は object（dictionary）である必要があります")
            elif "nodes" in workflow and isinstance(workflow["nodes"], list):
                node_ids = {node.get("id") for node in workflow["nodes"] if isinstance(node, dict)}
                # Check for required start and end nodes
                if "start" not in node_ids:
                    warnings.append("'start' ノードが見つかりません")
                if "end" not in node_ids:
                    warnings.append("'end' ノードが見つかりません")

    elif mode == "chat" or mode == "agent":
        if "model_config" not in dsl_content:
            errors.append(f"{mode.capitalize()} モードの場合、'model_config' セクションは必須です")
        else:
            model_config = dsl_content.get("model_config")
            if not isinstance(model_config, dict):
                errors.append("'model_config' は object（dictionary）である必要があります")

    # Print results
    print(f"DSL Validation: {args.dsl}")
    print("")

    if errors:
        print(f"❌ エラー ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
        print("")

    if warnings:
        print(f"⚠️  警告 ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
        print("")

    if not errors:
        print("✅ 検証成功：DSLは基本的に有効です")
        return 0
    else:
        return 1


def cmd_sync(args: argparse.Namespace) -> int:
    """
    import (create/overwrite) -> (optional confirm) -> draft run -> write artifacts
    """
    client = DifyConsoleClient.from_env()
    client.login(email=_require_env("DIFY_EMAIL"), password_plain=_require_env("DIFY_PASSWORD"))

    yaml_content = read_yaml_file(args.dsl)
    import_result = client.import_app(
        yaml_content=yaml_content,
        app_id=args.app_id,
        name=args.name,
        description=args.description,
        icon_type=args.icon_type,
        icon=args.icon,
        icon_background=args.icon_background,
    )
    if import_result.get("status") == "pending":
        import_result = client.confirm_import(import_result["id"])

    app_id = import_result.get("app_id") or args.app_id
    if not app_id:
        raise DifyConsoleError(f"import結果から app_id を取得できません: {import_result}")

    inputs: dict[str, Any] = read_json_file(args.inputs_json)
    if not isinstance(inputs, dict):
        raise DifyConsoleError("--inputs-json は JSON object である必要があります")

    run_result = client.run_draft_workflow_collect(app_id=app_id, inputs=inputs, max_wait_s=args.max_wait_s)

    out_dir = args.out_dir or "artifacts"
    os.makedirs(out_dir, exist_ok=True)
    write_json_file(os.path.join(out_dir, "import_result.json"), import_result)
    write_json_file(os.path.join(out_dir, "run_result.json"), run_result)

    print(json.dumps({"app_id": app_id, "import": import_result, "run": run_result}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dify-creator", description="Dify Console API automation (import/overwrite/test)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("login", help="Consoleへログインできるか確認")
    s.set_defaults(func=cmd_login)

    s = sub.add_parser("import", help="DSLをインポート（app_id指定で上書き）")
    s.add_argument("--dsl", help="DSL YAML file path")
    s.add_argument("--yaml-url", help="DSL YAML url (raw github etc)")
    s.add_argument("--app-id", help="Overwrite target app_id (optional)")
    s.add_argument("--name")
    s.add_argument("--description")
    s.add_argument("--icon-type")
    s.add_argument("--icon")
    s.add_argument("--icon-background")
    s.add_argument("--out", help="Write result json")
    s.set_defaults(func=cmd_import)

    s = sub.add_parser("export", help="アプリをDSLとしてエクスポート")
    s.add_argument("--app-id", required=True)
    s.add_argument("--include-secret", action="store_true")
    s.add_argument("--workflow-id")
    s.add_argument("--out", help="Write DSL to file (optional)")
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("run", help="Workflowアプリの draft workflow を実行（テスト）")
    s.add_argument("--app-id", required=True)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--inputs-json", help="Inputs JSON file (object)")
    g.add_argument("--inputs-inline", help='Inputs JSON string (e.g. \'{"foo":"bar"}\')')
    s.add_argument("--max-wait-s", type=float)
    s.add_argument("--out", help="Write result json")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("validate", help="DSL YAML を検証（Difyにアップロードせずにチェック）")
    s.add_argument("--dsl", required=True, help="DSL YAML file path")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("sync", help="import -> (confirm) -> draft run を1コマンドで")
    s.add_argument("--dsl", required=True, help="DSL YAML file path")
    s.add_argument("--app-id", help="Overwrite target app_id (optional)")
    s.add_argument("--name")
    s.add_argument("--description")
    s.add_argument("--icon-type")
    s.add_argument("--icon")
    s.add_argument("--icon-background")
    s.add_argument("--inputs-json", required=True, help="Inputs JSON file (object)")
    s.add_argument("--max-wait-s", type=float)
    s.add_argument("--out-dir", help="Artifacts dir (default: artifacts)")
    s.set_defaults(func=cmd_sync)

    return p


def main(argv: list[str] | None = None) -> int:
    load_dotenv_if_present()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except DifyConsoleError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


__all__ = ["main"]


