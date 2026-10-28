"""Trusted compiler/runtime harness, copied into isolated runner images."""

import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path


TIMEOUT = float(os.getenv("RUNNER_TIMEOUT_SECONDS", "4"))
OUTPUT_LIMIT = 8_000


def run_limited(command: list[str], input_text: str = "", timeout: float = TIMEOUT):
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/runner",
        start_new_session=True,
    )
    captured = {"stdout": bytearray(), "stderr": bytearray()}

    def drain(stream, target):
        while True:
            block = stream.read(2048)
            if not block:
                return
            if len(target) < OUTPUT_LIMIT:
                target.extend(block[:OUTPUT_LIMIT - len(target)])

    readers = [
        threading.Thread(target=drain, args=(process.stdout, captured["stdout"]), daemon=True),
        threading.Thread(target=drain, args=(process.stderr, captured["stderr"]), daemon=True),
    ]
    for reader in readers:
        reader.start()
    try:
        process.stdin.write(input_text.encode("utf-8"))
        process.stdin.close()
    except BrokenPipeError:
        pass
    try:
        return_code = process.wait(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        return_code = 124
        timed_out = True
    for reader in readers:
        reader.join(timeout=1)
    return {
        "returncode": return_code,
        "timeout": timed_out,
        "stdout": captured["stdout"].decode(errors="replace"),
        "stderr": captured["stderr"].decode(errors="replace"),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("runner usage error", file=sys.stderr)
        return 2
    language, entry = sys.argv[1:]
    entries = {"python": "main.py", "java": "Main.java", "c": "main.c"}
    if entries.get(language) != entry:
        print("unsupported language or entry point", file=sys.stderr)
        return 2
    source_path = Path("/input") / entry
    tests_path = Path("/input/tests.json")
    try:
        tests = json.loads(tests_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("invalid runner test data", file=sys.stderr)
        return 2

    start = time.perf_counter()
    build_dir = None
    if language == "python":
        try:
            compile(source_path.read_text(encoding="utf-8"), str(source_path), "exec")
        except SyntaxError as error:
            result = {"status": "syntax_error", "message": f"Syntax error on line {error.lineno}: {error.msg}", "tests": []}
            result["duration_ms"] = int((time.perf_counter() - start) * 1000)
            print("CODEMIND_RESULT:" + json.dumps(result, ensure_ascii=True))
            return 0
        main_command = [sys.executable, "-I", str(source_path)]
        compilation = {"returncode": 0, "timeout": False, "stdout": "", "stderr": ""}
    else:
        build_dir = tempfile.mkdtemp(prefix="codemind-build-", dir="/runner")
    if language == "java":
        compile_command = ["javac", "-J-Xmx96m", "-d", build_dir, str(source_path)]
        main_command = ["java", "-Xmx64m", "-XX:ActiveProcessorCount=1", "-cp", build_dir, "Main"]
    elif language == "c":
        binary = str(Path(build_dir) / "main")
        compile_command = ["gcc", "-std=c11", "-O1", "-pipe", "-o", binary, str(source_path)]
        main_command = [binary]

    if language in {"java", "c"}:
        compilation = run_limited(compile_command, timeout=15)
    if compilation["timeout"]:
        result = {"status": "timeout", "message": "Compilation exceeded the time limit.", "tests": []}
    elif compilation["returncode"] != 0:
        message = (compilation["stderr"] or compilation["stdout"] or "Compilation failed.")[:700]
        result = {"status": "compile_error", "message": message, "tests": []}
    else:
        results = []
        for test in tests:
            execution = run_limited(main_command, input_text=str(test.get("input", "")))
            expected = str(test.get("expected_output", "")).strip()
            actual = execution["stdout"].strip()
            if execution["timeout"]:
                results.append({"passed": False, "timeout": True, "expected": expected, "actual": ""})
            elif execution["returncode"] != 0:
                detail = execution["stderr"].strip() or f"Program exited with status {execution['returncode']}."
                results.append({"passed": False, "error": detail[:400], "expected": expected, "actual": actual})
            else:
                results.append({"passed": actual == expected, "expected": expected, "actual": actual})
        result = {"status": "completed", "message": "", "tests": results}
    result["duration_ms"] = int((time.perf_counter() - start) * 1000)
    print("CODEMIND_RESULT:" + json.dumps(result, ensure_ascii=True, default=repr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
