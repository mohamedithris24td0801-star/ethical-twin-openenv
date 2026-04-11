"""Small requests-based client for the Ethical Twin API."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests


class EthicalTwinClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}{path}", json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _get(self, path: str) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}{path}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def reset(self) -> Dict[str, Any]:
        return self._post("/reset")

    def step(self, action: str) -> Dict[str, Any]:
        return self._post("/step", {"action": action})

    def state(self) -> Dict[str, Any]:
        return self._get("/state")


if __name__ == "__main__":
    client = EthicalTwinClient()
    print(client.reset())
