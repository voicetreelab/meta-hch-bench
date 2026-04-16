from __future__ import annotations

import subprocess

from harness.protocol import PLAN_TURN_BUDGET_S, SUBTASK_BUDGET_S

_TIMEOUT_CAP_S = max(PLAN_TURN_BUDGET_S, SUBTASK_BUDGET_S) + 30


class LocalLLM:
    def __init__(self, model: str, system_prompt: str, *, timeout_s: int = _TIMEOUT_CAP_S):
        self.model = model
        self.system_prompt = system_prompt
        self.timeout_s = timeout_s

    def prompt(self, text: str, *, temperature: float = 0.0) -> str:
        cmd = [
            "llm",
            "-m",
            self.model,
            "-s",
            self.system_prompt,
            "--option",
            "temperature",
            format(float(temperature), "g"),
            text,
        ]
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                check=False,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("llm CLI not found in PATH") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"llm CLI timed out after {self.timeout_s}s") from exc

        if completed.returncode != 0:
            message = completed.stderr.strip() or completed.stdout.strip() or "llm CLI failed"
            raise RuntimeError(message)

        return completed.stdout.strip()
