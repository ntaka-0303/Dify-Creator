from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

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


