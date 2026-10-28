import ast
import json
import os
import subprocess
import tempfile
import shutil
import uuid
import time
import threading
from types import SimpleNamespace
from pathlib import Path


RUNNER_MODE = os.getenv("RUNNER_MODE", "docker")
RUNNER_IMAGE = os.getenv("RUNNER_IMAGE", "codemind-python-runner:latest")
JAVA_RUNNER_IMAGE = os.getenv("JAVA_RUNNER_IMAGE", "codemind-java-runner:latest")
C_RUNNER_IMAGE = os.getenv("C_RUNNER_IMAGE", "codemind-c-runner:latest")
TIMEOUT = float(os.getenv("RUNNER_TIMEOUT_SECONDS", "4"))
MAX_SOURCE_BYTES = int(os.getenv("MAX_SOURCE_BYTES", "20000"))
RUNNER_VOLUME = os.getenv("RUNNER_VOLUME", "").strip()


class RunnerUnavailable(Exception):
    pass


def _harness(code: str, function_name: str, tests: list[dict]) -> str:
    payload = json.dumps(tests, ensure_ascii=True)
    return f'''import json, traceback
source = {code!r}
tests = json.loads({payload!r})
try:
    namespace = {{"__name__": "__student__"}}
    exec(compile(source, "<student>", "exec"), namespace, namespace)
    function = namespace.get({function_name!r})
    if not callable(function):
        raise NameError("Define the required function {function_name}")
    results = []
    for test in tests:
        try:
            actual = function(*test["args"])
            passed = actual == test["expected"]
            results.append({{"passed": passed, "expected": test["expected"], "actual": actual}})
        except Exception as error:
            results.append({{"passed": False, "error": type(error).__name__ + ": " + str(error)}})
    print("CODEMIND_RESULT:" + json.dumps(results, default=repr))
except BaseException as error:
    print("CODEMIND_ERROR:" + type(error).__name__ + ": " + str(error))
'''


def _run_bounded(command: list[str], timeout: float, container_name: str):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    captured = {"stdout": bytearray(), "stderr": bytearray()}

    def drain(stream, key):
        while True:
            chunk = stream.read(2048)
            if not chunk:
                return
            if len(captured[key]) < 8000:
                captured[key].extend(chunk[:8000 - len(captured[key])])

    readers = [
        threading.Thread(target=drain, args=(process.stdout, "stdout"), daemon=True),
        threading.Thread(target=drain, args=(process.stderr, "stderr"), daemon=True),
    ]
    for reader in readers:
        reader.start()
    try:
        return_code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        # Killing Docker CLI doesn't reliably stop the container on every
        # platform. Explicitly stop the named container to enforce cleanup.
        try:
            subprocess.run(["docker", "stop", "--time", "1", container_name], capture_output=True, timeout=4, check=False)
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, timeout=4, check=False)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        for reader in readers:
            reader.join(timeout=1)
        result = SimpleNamespace(stdout=captured["stdout"].decode(errors="replace"), stderr=captured["stderr"].decode(errors="replace"), returncode=124)
        return result, True
    for reader in readers:
        reader.join(timeout=1)
    result = SimpleNamespace(stdout=captured["stdout"].decode(errors="replace"), stderr=captured["stderr"].decode(errors="replace"), returncode=return_code)
    return result, False


def execute(source: str, function_name: str, tests: list[dict]) -> dict:
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        return {"status": "rejected", "message": "Your submission is too large.", "tests": [], "duration_ms": 0}
    try:
        ast.parse(source)
    except SyntaxError as error:
        return {
            "status": "syntax_error",
            "message": f"Syntax error on line {error.lineno}: {error.msg}",
            "tests": [],
            "duration_ms": 0,
        }
    if RUNNER_MODE != "docker":
        raise RunnerUnavailable("RUNNER_MODE must be docker. The API never executes student code in its own process.")
    script = _harness(source, function_name, tests)
    started = time.perf_counter()
    folder = None
    cleanup_directory = None
    if RUNNER_VOLUME:
        # Compose mounts this named volume into both the API and Docker daemon
        # containers. The spawned runner mounts the same volume read-only.
        cleanup_directory = Path("/runner-input") / uuid.uuid4().hex
        cleanup_directory.mkdir(parents=True, exist_ok=False)
        script_path = cleanup_directory / "submission.py"
    else:
        folder = tempfile.TemporaryDirectory(prefix="codemind-")
        script_path = Path(folder.name) / "submission.py"
    try:
        script_path.write_text(script, encoding="utf-8")
        # A single immutable input file is mounted read-only. Student code runs
        # in a disposable container with no network, low resource limits, and
        # a read-only root filesystem.
        mounted_path = str(script_path.resolve()).replace("\\", "/")
        container_name = "codemind-run-" + uuid.uuid4().hex[:16]
        command = [
            "docker", "run", "--rm", "--name", container_name, "--network=none", "--read-only",
            "--memory=128m", "--cpus=0.5", "--pids-limit=32",
            "--cap-drop=ALL", "--security-opt=no-new-privileges",
            "--user=65534:65534", "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
            "--mount", (f"type=volume,source={RUNNER_VOLUME},target=/work/input,readonly" if RUNNER_VOLUME else f"type=bind,source={mounted_path},target=/work/submission.py,readonly"),
            "--workdir", "/work", RUNNER_IMAGE, "timeout", "--signal=KILL", f"{TIMEOUT}s", "python", "-I", "/work/submission.py",
        ]
        if RUNNER_VOLUME:
            command[-1] = f"/work/input/{cleanup_directory.name}/submission.py"
        try:
            process, host_timeout = _run_bounded(command, timeout=TIMEOUT + 8, container_name=container_name)
        except FileNotFoundError as error:
            raise RunnerUnavailable("Docker CLI is unavailable. Start Docker and build the runner image.") from error
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "message": "Execution exceeded the time limit.", "tests": [], "duration_ms": int((time.perf_counter() - started) * 1000)}
    finally:
        if cleanup_directory:
            shutil.rmtree(cleanup_directory, ignore_errors=True)
        if folder:
            folder.cleanup()
    duration = int((time.perf_counter() - started) * 1000)
    if host_timeout or process.returncode == 124:
        return {"status": "timeout", "message": "Execution exceeded the time limit.", "tests": [], "duration_ms": duration}
    stderr = process.stderr[-1000:]
    if process.returncode != 0:
        if process.returncode == 137:
            return {"status": "timeout", "message": "Execution exceeded the time limit.", "tests": [], "duration_ms": duration}
        stderr_lower = stderr.lower()
        if any(marker in stderr_lower for marker in ("failed to connect to the docker api", "cannot connect to the docker daemon", "error during connect")):
            raise RunnerUnavailable("Docker Desktop is not running. Start its Linux container engine and retry.")
        if "no such image" in stderr_lower or "pull access denied" in stderr_lower or "repository does not exist" in stderr_lower:
            raise RunnerUnavailable("The CodeMind runner image is missing. Run `docker compose --profile build-only build runner-image` and retry.")
    stdout = process.stdout[-8000:]
    if "CODEMIND_RESULT:" in stdout:
        raw = stdout.rsplit("CODEMIND_RESULT:", 1)[1].strip().splitlines()[0]
        try:
            result_tests = json.loads(raw)
        except json.JSONDecodeError:
            result_tests = []
        return {"status": "completed", "tests": result_tests, "duration_ms": duration, "message": ""}
    if "CODEMIND_ERROR:" in stdout:
        message = stdout.rsplit("CODEMIND_ERROR:", 1)[1].strip().splitlines()[0][:400]
        return {"status": "runtime_error", "message": message, "tests": [], "duration_ms": duration}
    if process.returncode != 0:
        return {"status": "runtime_error", "message": (stderr[-400:] or "Program exited before producing results.").strip(), "tests": [], "duration_ms": duration}
    return {"status": "runtime_error", "message": "The runner could not read the program result.", "tests": [], "duration_ms": duration}


def execute_stdio(language: str, source: str, entry_point: str, tests: list[dict]) -> dict:
    """Run one DSA stdin/stdout solution in its language-specific container."""
    if language not in {"python", "java", "c"}:
        raise ValueError("Supported judge languages are C, Python, and Java.")
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        return {"status": "rejected", "message": "Your submission is too large.", "tests": [], "duration_ms": 0}
    expected_entry = {"python": "main.py", "java": "Main.java", "c": "main.c"}[language]
    if entry_point != expected_entry:
        raise ValueError("The exercise has an unsupported entry point.")
    runner_image = {"python": RUNNER_IMAGE, "java": JAVA_RUNNER_IMAGE, "c": C_RUNNER_IMAGE}[language]
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix=f"codemind-{language}-") as folder:
        root = Path(folder)
        (root / entry_point).write_text(source, encoding="utf-8")
        (root / "tests.json").write_text(json.dumps(tests), encoding="utf-8")
        mounted = str(root.resolve()).replace("\\", "/")
        container_name = "codemind-run-" + uuid.uuid4().hex[:16]
        command = [
            "docker", "run", "--rm", "--name", container_name,
            "--network=none", "--read-only", "--memory=192m", "--cpus=0.6", "--pids-limit=32",
            "--cap-drop=ALL", "--security-opt=no-new-privileges", "--user=65534:65534",
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
            "--tmpfs", "/runner:rw,exec,nosuid,size=64m,uid=65534,gid=65534,mode=700",
            "--mount", f"type=bind,source={mounted},target=/input,readonly",
            "--workdir", "/runner", runner_image,
            "python", "/opt/codemind/stdio_runner.py", language, entry_point,
        ]
        try:
            process, host_timeout = _run_bounded(command, timeout=TIMEOUT + 25, container_name=container_name)
        except FileNotFoundError as error:
            raise RunnerUnavailable("Docker CLI is unavailable. Start Docker Desktop and retry.") from error
    duration = int((time.perf_counter() - started) * 1000)
    if host_timeout or process.returncode in (124, 137):
        return {"status": "timeout", "message": "Compilation or execution exceeded the time limit.", "tests": [], "duration_ms": duration}
    stderr = process.stderr[-1000:]
    stderr_lower = stderr.lower()
    if process.returncode != 0 and any(marker in stderr_lower for marker in ("failed to connect to the docker api", "cannot connect to the docker daemon", "error during connect")):
        raise RunnerUnavailable("Docker Desktop is not running. Start its Linux container engine and retry.")
    if process.returncode != 0 and any(marker in stderr_lower for marker in ("no such image", "pull access denied", "repository does not exist")):
        build_target = {"python": "runner-image", "java": "java-runner", "c": "c-runner"}[language]
        build_command = f"docker compose --profile build-only build {build_target}"
        raise RunnerUnavailable(f"The {language.upper()} runner image is missing. Build it with `{build_command}` and retry.")
    stdout = process.stdout[-8000:]
    if "CODEMIND_RESULT:" in stdout:
        raw = stdout.rsplit("CODEMIND_RESULT:", 1)[1].strip().splitlines()[0]
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            result = {"status": "runtime_error", "message": "The runner returned unreadable test results.", "tests": []}
        result["duration_ms"] = duration
        return result
    return {"status": "runtime_error", "message": (stderr[-400:] or "The runner did not return test results.").strip(), "tests": [], "duration_ms": duration}
