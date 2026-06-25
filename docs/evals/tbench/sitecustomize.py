"""Auto-loaded by Python (it's on PYTHONPATH) for the Terminal-Bench Claude run.

This module is pure substrate-compat plumbing for running terminus against
Claude (Opus 4.8) through a Bedrock-compatible proxy. It loads identically for
the baseline (``terminus``) and the treatment (``workflow-terminus``), touching
NEITHER arm's prompt, model, schema, nor execution path — so it cannot bias the
A/B. It does three things, all forced by the proxy/model, not by the experiment:

1. Token keep-alive. The Bedrock bearer token may be short-lived and a full
   two-arm run can outlive it. We wrap ``litellm.completion`` to refresh
   ``AWS_BEARER_TOKEN_BEDROCK`` proactively (every ~20 min) and reactively (on a
   401/expired error: force-refresh and retry). Removes auth-expiry tail-task
   failures.

2. Force terminus's schema-in-prompt fallback. LiteLLM advertises
   ``response_format`` as supported for Bedrock Claude, so terminus would pass it
   natively — but some provider proxies reject it. We drop ``response_format``
   from the model's supported-params list so terminus instead injects the JSON
   schema into the prompt (its built-in path for non-structured-output models).
   Both arms equally.

3. Strip fences + normalize the JSON to terminus's schema. With (2), Claude
   returns its JSON wrapped in ```json fences and/or behind a sentence of prose,
   and — because schema-in-prompt is advisory, not enforced like native
   structured output — it intermittently OMITS a required field (most often
   ``is_task_complete``). terminus parses with ``model_validate_json`` and does no
   cleanup, so it discards the whole command batch and burns retries. We (a)
   extract the JSON object and (b) fill any missing required field with a SAFE
   default. ``is_task_complete`` defaults to False ("not done, keep working"), so
   this can NEVER fabricate a task pass — it only prevents a valid command batch
   from being thrown away. Both arms equally; no completion is ever invented.
"""

import json
import os
import re
import subprocess
import threading
import time

_SCOPE = os.environ.get("TB_BEDROCK_TOKEN_SCOPE")
_REFRESH_EVERY_S = 20 * 60  # proactively re-fetch a token older than this
_lock = threading.Lock()
_last_refresh = [0.0]


def _fetch_token() -> str | None:
    if not _SCOPE:
        return None
    try:
        out = subprocess.run(
            [
                "az",
                "account",
                "get-access-token",
                "--scope",
                _SCOPE,
                "--query",
                "accessToken",
                "-o",
                "tsv",
            ],
            capture_output=True, text=True, timeout=60,
        )
        tok = out.stdout.strip()
        return tok or None
    except Exception:
        return None


def _ensure_token(force: bool = False) -> None:
    with _lock:
        now = time.monotonic()
        have = bool(os.environ.get("AWS_BEARER_TOKEN_BEDROCK"))
        stale = (now - _last_refresh[0]) > _REFRESH_EVERY_S
        if not (force or stale or not have):
            return
        tok = _fetch_token()
        if tok:
            os.environ["AWS_BEARER_TOKEN_BEDROCK"] = tok
            _last_refresh[0] = now


def _looks_like_auth_error(exc: Exception) -> bool:
    name = type(exc).__name__.lower()
    msg = str(exc).lower()
    return (
        "auth" in name
        or "expired" in msg
        or "jwt" in msg
        or "unauthor" in msg
        or "403" in msg
        or "401" in msg
    )


_FENCE_BLOCK_RE = re.compile(r"```(?:json)?\s*\n(.*?)\n?```", re.DOTALL)


def _strip_fence(text):
    """Extract the JSON object from Claude's response.

    terminus parses with model_validate_json and does no cleanup, but Claude
    (in schema-in-prompt mode) may wrap its JSON in a ```json fence and/or
    prepend a sentence of prose ("I'll start by..."). We recover the JSON by:
    taking the contents of a fenced block if present, else slicing from the
    first '{' to the last '}'. Applied identically to both arms.
    """
    if not isinstance(text, str):
        return text
    m = _FENCE_BLOCK_RE.search(text)
    if m:
        text = m.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    return _normalize_schema(text)


def _normalize_schema(text):
    """Fill required CommandBatchResponse fields the model omitted.

    Only safe defaults: is_task_complete=False means "not done, keep working",
    so a missing field can never be read as a fabricated success. Leaves valid
    payloads untouched; returns the original text if it isn't a JSON object.
    """
    try:
        obj = json.loads(text)
    except Exception:
        return text
    if not isinstance(obj, dict):
        return text
    changed = False
    if "commands" in obj:  # only treat objects that look like a command batch
        defaults = {
            "state_analysis": "",
            "explanation": "",
            "is_task_complete": False,
        }
        for key, val in defaults.items():
            if key not in obj:
                obj[key] = val
                changed = True
        # Per-command required fields, with conservative defaults.
        if isinstance(obj.get("commands"), list):
            for cmd in obj["commands"]:
                if isinstance(cmd, dict):
                    if "is_blocking" not in cmd:
                        cmd["is_blocking"] = True
                        changed = True
                    if "timeout_sec" not in cmd:
                        cmd["timeout_sec"] = 10
                        changed = True
    return json.dumps(obj) if changed else text


def _install():
    try:
        import litellm
    except Exception:
        return
    if getattr(litellm, "_tb_bedrock_token_wrapped", False):
        return
    _orig = litellm.completion

    def _strip_response_fences(resp):
        try:
            msg = resp["choices"][0]["message"]
            content = msg["content"]
            stripped = _strip_fence(content)
            if stripped is not content:
                msg["content"] = stripped
        except Exception:
            pass
        return resp

    def _call_once(args, kwargs):
        return _strip_response_fences(_orig(*args, **kwargs))

    def _wrapped(*args, **kwargs):
        _ensure_token()
        try:
            return _call_once(args, kwargs)
        except Exception as e:  # reactive refresh on auth failure
            if not _looks_like_auth_error(e):
                raise
            for _ in range(3):
                time.sleep(3)
                _ensure_token(force=True)
                try:
                    return _call_once(args, kwargs)
                except Exception as e2:
                    if not _looks_like_auth_error(e2):
                        raise
            raise

    litellm.completion = _wrapped
    litellm._tb_bedrock_token_wrapped = True

    # Force terminus's schema-in-prompt fallback for provider proxies that reject
    # native response_format for Bedrock Claude. Patch the symbol terminus imports.
    try:
        import terminal_bench.llms.lite_llm as ll

        _orig_params = ll.get_supported_openai_params

        def _patched_params(model_name, *a, **k):
            p = _orig_params(model_name, *a, **k)
            if p and "bedrock" in str(model_name) and "response_format" in p:
                p = [x for x in p if x != "response_format"]
            return p

        ll.get_supported_openai_params = _patched_params
    except Exception:
        pass


_install()
