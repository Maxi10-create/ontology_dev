"""Zugang zu Sprachmodellen. Echte Daten dürfen nur von lokalen Modellen verarbeitet werden."""

import json
import tomllib
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

CONFIG = Path(__file__).resolve().parent.parent / "config" / "llm.toml"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


class NotLocalError(RuntimeError):
    """Der konfigurierte Endpunkt ist kein lokales Modell."""


def load_config(path: Path = CONFIG) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def assert_local(url: str, extra_hosts: list[str] | None = None) -> None:
    host = urlparse(url).hostname
    if host not in LOCAL_HOSTS | set(extra_hosts or []):
        raise NotLocalError(f"Endpunkt {url} ist nicht lokal; Daten dürfen nur lokal verarbeitet werden.")


def complete(prompt: str, config: dict | None = None) -> str:
    """Schickt einen Prompt an das lokale Modell (Ollama-API) und gibt die Antwort zurück."""
    cfg = config or load_config()
    url = cfg["endpoint"].rstrip("/") + "/api/generate"
    assert_local(url, cfg.get("allowed_hosts"))
    body = json.dumps({"model": cfg["model"], "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=cfg.get("timeout_s", 300)) as resp:
        return json.loads(resp.read())["response"]
