from __future__ import annotations

import base64
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Iterable, Iterator

import requests


class DifyConsoleError(RuntimeError):
    pass


def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def _b64(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")


def _join_url(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/")


@dataclass(frozen=True)
class ConsoleConfig:
    base_url: str
    verify_ssl: bool = True
    timeout_s: float = 60.0

    @property
    def api_base(self) -> str:
        # Dify OSS は url_prefix="/console/api" を使用
        return _join_url(self.base_url, "console/api")


class DifyConsoleClient:
    """
    Dify Console API (管理エンドポイント /console/api 配下) の最小限のクライアント。

    認証モデル (OSS実装に準拠):
    - POST /console/api/login でCookieを設定:
      - access_token (httpOnly)
      - refresh_token (httpOnly)
      - csrf_token (読み取り可能)
    - 安全でないメソッドの場合、csrf_token Cookieと一致する X-CSRF-Token ヘッダーを送信。
    """

    def __init__(self, config: ConsoleConfig):
        self.config = config
        self.session = requests.Session()

    @classmethod
    def from_env(cls) -> "DifyConsoleClient":
        base_url = os.getenv("DIFY_BASE_URL", "").strip()
        if not base_url:
            raise DifyConsoleError("DIFY_BASE_URL が未設定です")
        verify_ssl = _env_bool("DIFY_VERIFY_SSL", True)
        timeout_s = float(os.getenv("DIFY_TIMEOUT_S", "60"))
        return cls(ConsoleConfig(base_url=base_url, verify_ssl=verify_ssl, timeout_s=timeout_s))

    def _csrf(self) -> str | None:
        # OSS での Cookie 名: csrf_token
        return self.session.cookies.get("csrf_token")

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        stream: bool = False,
        extra_headers: dict[str, str] | None = None,
        timeout_s: float | None = None,
    ) -> requests.Response:
        url = _join_url(self.config.api_base, path)
        headers: dict[str, str] = {}

        if extra_headers:
            headers.update(extra_headers)

        # 安全でないメソッド用の CSRF
        if method.upper() not in {"GET", "HEAD", "OPTIONS"}:
            csrf = self._csrf()
            if csrf:
                headers.setdefault("X-CSRF-Token", csrf)

        resp = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json_body,
            headers=headers,
            verify=self.config.verify_ssl,
            timeout=timeout_s or self.config.timeout_s,
            stream=stream,
        )
        return resp

    def _raise_for_status(self, resp: requests.Response) -> None:
        if 200 <= resp.status_code < 300:
            return
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise DifyConsoleError(f"HTTP {resp.status_code}: {detail}")

    def login(self, *, email: str, password_plain: str, remember_me: bool = False) -> None:
        """
        /console/api/login 経由でログイン。
        注意: 現在のDify実装ではパスワードは平文で送信されます。
        """
        resp = self._request(
            "POST",
            "/login",
            json_body={
                "email": email,
                "password": password_plain,
                "remember_me": remember_me,
            },
        )
        self._raise_for_status(resp)

        # 健全性チェック
        if not self._csrf():
            raise DifyConsoleError("ログイン後に csrf_token Cookie が見つかりません（Difyの設定/挙動を確認してください）")

    def import_app(
        self,
        *,
        yaml_content: str | None = None,
        yaml_url: str | None = None,
        app_id: str | None = None,
        name: str | None = None,
        description: str | None = None,
        icon_type: str | None = None,
        icon: str | None = None,
        icon_background: str | None = None,
    ) -> dict[str, Any]:
        # OSS は mode を {"yaml-content","yaml-url"} のいずれかで期待
        if yaml_content and yaml_url:
            raise ValueError("yaml_content と yaml_url は同時指定できません")
        if not yaml_content and not yaml_url:
            raise ValueError("yaml_content か yaml_url のどちらかが必要です")

        mode = "yaml-content" if yaml_content else "yaml-url"
        payload: dict[str, Any] = {
            "mode": mode,
            "yaml_content": yaml_content,
            "yaml_url": yaml_url,
            "name": name,
            "description": description,
            "icon_type": icon_type,
            "icon": icon,
            "icon_background": icon_background,
            "app_id": app_id,
        }
        # None のキーを削除
        payload = {k: v for k, v in payload.items() if v is not None}

        resp = self._request("POST", "/apps/imports", json_body=payload)
        # import はステータスに応じて 200/202/400 を返す
        if resp.status_code in {200, 202}:
            return resp.json()
        self._raise_for_status(resp)
        return {}  # 到達不可

    def confirm_import(self, import_id: str) -> dict[str, Any]:
        resp = self._request("POST", f"/apps/imports/{import_id}/confirm")
        self._raise_for_status(resp)
        return resp.json()

    def export_app(self, *, app_id: str, include_secret: bool = False, workflow_id: str | None = None) -> str:
        params: dict[str, Any] = {"include_secret": str(include_secret).lower()}
        if workflow_id:
            params["workflow_id"] = workflow_id
        resp = self._request("GET", f"/apps/{app_id}/export", params=params)
        self._raise_for_status(resp)
        data = resp.json()
        if "data" not in data:
            raise DifyConsoleError(f"exportレスポンスが想定外です: {data}")
        return str(data["data"])

    def run_draft_workflow_stream(
        self,
        *,
        app_id: str,
        inputs: dict[str, Any],
        files: list[dict[str, Any]] | None = None,
        external_trace_id: str | None = None,
    ) -> requests.Response:
        payload: dict[str, Any] = {"inputs": inputs}
        if files is not None:
            payload["files"] = files
        headers: dict[str, str] = {}
        if external_trace_id:
            # Dify は外部トレースID の伝播をサポート
            headers["X-External-Trace-Id"] = external_trace_id

        resp = self._request(
            "POST",
            f"/apps/{app_id}/workflows/draft/run",
            json_body=payload,
            stream=True,
            extra_headers=headers,
            timeout_s=None,  # 長時間実行を許可
        )
        self._raise_for_status(resp)
        return resp

    def iter_sse_json(self, resp: requests.Response) -> Iterator[dict[str, Any]]:
        """
        helper.compact_generate_response() から発行される SSE 風のストリーミングレスポンスを解析。
        'data: {json}' のような行のみを解析します。
        """
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line.startswith("data:"):
                continue
            data_str = line[len("data:") :].strip()
            if not data_str:
                continue
            if data_str == "[DONE]":
                return
            try:
                yield json.loads(data_str)
            except json.JSONDecodeError:
                # 一部のイベントは非JSONデータを送信する可能性があるため無視
                continue

    def run_draft_workflow_collect(
        self,
        *,
        app_id: str,
        inputs: dict[str, Any],
        files: list[dict[str, Any]] | None = None,
        external_trace_id: str | None = None,
        max_wait_s: float | None = None,
    ) -> dict[str, Any]:
        """
        ストリーミングイベントを以下に収集:
        - events: JSON イベントのリスト
        - last_event: 最後の JSON イベント (存在する場合)
        """
        resp = self.run_draft_workflow_stream(
            app_id=app_id, inputs=inputs, files=files, external_trace_id=external_trace_id
        )

        t0 = time.time()
        events: list[dict[str, Any]] = []
        last: dict[str, Any] | None = None
        for ev in self.iter_sse_json(resp):
            events.append(ev)
            last = ev
            if max_wait_s is not None and (time.time() - t0) > max_wait_s:
                break

        return {"events": events, "last_event": last}


def load_dotenv_if_present() -> None:
    # オプション; python-dotenv がインストールされていない場合は何もしない
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    load_dotenv(override=False)


def read_yaml_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_text_file(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_json_file(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


