#!/usr/bin/env python3
"""POC-B: Realtime process runner (stderr merged) with callback.

Goals
- Realtime output: process output line-by-line.
- No intentional loss: do not truncate; read until EOF.
- Avoid IDE hangs: default stdin is DEVNULL (PyCharm often keeps stdin open).

Usage
- Default: runs `opencode run hello`
- Custom command: `-- <cmd> <args...>`

Callback
- Provide `callback(line, executor)`.
- `executor` is ProcExecutor instance (command, pid, kill helpers).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import threading
from typing import Callable, List, Optional, Sequence
import sys
LineCallback = Callable[[str, "ProcExecutor"], None]

import sys

try:
    sys.setdefaultencoding('utf-8')
except Exception:
    pass
def _safe_console_write(text: str) -> None:
    """Write text to stdout without crashing on Windows GBK consoles."""
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except UnicodeEncodeError:
        # Fall back to an encoding-safe representation (e.g. turn \u2699 into \u2699).
        safe = text.encode(enc, errors="backslashreplace").decode(enc, errors="ignore")
        sys.stdout.write(safe)
        sys.stdout.flush()


def _is_windows() -> bool:
    return sys.platform.startswith("win")


class ProcExecutor:
    def __init__(self, callback: Optional[LineCallback] = None):
        self._callback: LineCallback = callback or self._default_callback
        self.cmd: List[str] = []
        self.proc: Optional[subprocess.Popen] = None

    @property
    def pid(self) -> Optional[int]:
        return self.proc.pid if self.proc is not None else None

    def _default_callback(self, line: str, _executor: "ProcExecutor") -> None:
        _safe_console_write(line)

    def emit(self, line: str) -> None:
        if not line.endswith("\n"):
            line += "\n"
        self._callback(line, self)

    def _resolve_cmd(self, cmd: List[str]) -> List[str]:
        if not cmd:
            return cmd

        resolved0 = shutil.which(cmd[0])
        if resolved0:
            cmd[0] = resolved0

        # Windows: if argv[0] is a wrapper script, run via cmd.exe.
        if _is_windows() and cmd[0].lower().endswith((".cmd", ".bat")):
            return ["cmd.exe", "/c", *cmd]

        return cmd

    def kill_tree(self) -> None:
        if self.proc is None:
            return

        if _is_windows():
            subprocess.run(
                ["taskkill", "/PID", str(self.proc.pid), "/T", "/F"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        else:
            self.proc.kill()

    def _timeout_killer(
        self, timeout_s: Optional[float], done: threading.Event
    ) -> None:
        if timeout_s is None:
            return

        if timeout_s <= 0:
            timeout_s = 0.0

        if done.wait(timeout=timeout_s):
            return

        self.emit("[SYS] [TIMEOUT] killing process")
        try:
            self.kill_tree()
        except Exception as e:
            self.emit(f"[SYS] [TIMEOUT] kill failed: {e}")

    def run(
        self,
        cmd: List[str],
        *,
        timeout_s: Optional[float] = 60,
        inherit_stdin: bool = False,
        **kwargs,
    ) -> int:
        self.cmd = self._resolve_cmd(list(cmd))
        self.emit(f"[SYS] cmd: {self.cmd}")

        # When running inside some shells, OPENCODE_* env vars may be set to force
        # opencode to use the Desktop client/session. That breaks headless CLI runs
        # (e.g. `opencode run ...`) with "Session not found". Strip these variables
        # for the child process only.
        env = kwargs.pop("env", None)
        if env is None:
            env = dict(os.environ)
        else:
            env = dict(env)
        for k in (
            "OPENCODE_CLIENT",
            "OPENCODE_PID",
            "OPENCODE_SERVER_USERNAME",
            "OPENCODE_SERVER_PASSWORD",
        ):
            env.pop(k, None)

        self.proc = subprocess.Popen(
            self.cmd,
            stdin=None if inherit_stdin else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",

            bufsize=1,
            env=env,
            **kwargs,
        )
        assert self.proc.stdout is not None

        done = threading.Event()
        killer = threading.Thread(
            target=self._timeout_killer,
            args=(timeout_s, done),
            daemon=True,
        )
        killer.start()

        try:
            # Realtime, read until EOF.
            for line in iter(self.proc.stdout.readline, ""):
                self._callback(line, self)
        finally:
            done.set()
            try:
                self.proc.stdout.close()
            except Exception:
                pass

        return self.proc.wait()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="POC-B realtime runner (stderr merged)"
    )
    parser.add_argument("--timeout-s", type=float, default=60)
    parser.add_argument(
        "--inherit-stdin",
        action="store_true",
        help="Inherit stdin from parent (default: DEVNULL to avoid IDE hangs)",
    )
    parser.add_argument(
        "--env-dump",
        action="store_true",
        help="Print cwd/PATH/opencode resolution for debugging",
    )
    parser.add_argument(
        "cmd",
        nargs=argparse.REMAINDER,
        help="Command to run, e.g. -- opencode run hello",
    )
    args = parser.parse_args(argv)

    if args.env_dump:
        sys.stderr.write(f"[SYS] python: {sys.executable}\n")
        sys.stderr.write(f"[SYS] cwd: {os.getcwd()}\n")
        sys.stderr.write(f"[SYS] PATH(head): {os.environ.get('PATH', '')[:300]}\n")
        sys.stderr.write(f"[SYS] opencode: {shutil.which('opencode')}\n")
        sys.stderr.flush()

    cmd = list(args.cmd)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        exe = shutil.which("opencode") or "opencode"
        cmd = [exe, "run", "hello"]

    ex = ProcExecutor()
    return ex.run(cmd, timeout_s=args.timeout_s, inherit_stdin=args.inherit_stdin)


if __name__ == "__main__":
    raise SystemExit(main())
