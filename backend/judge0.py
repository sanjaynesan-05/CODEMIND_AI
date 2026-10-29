"""Judge0-backed execution for deployments without a local Docker daemon."""

import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Judge0Error(Exception):
    """Raised when the configured sandbox is unavailable or misconfigured."""


LANGUAGE_IDS = {
    "c": int(os.getenv("JUDGE0_C_LANGUAGE_ID", "103")),
    "java": int(os.getenv("JUDGE0_JAVA_LANGUAGE_ID", "91")),
    "python": int(os.getenv("JUDGE0_PYTHON_LANGUAGE_ID", "100")),
}
MAX_BATCH_SIZE = 40
PENDING_STATUSES = {1, 2}
STATUS_NAMES = {
    3: "accepted",
    4: "wrong_answer",
    5: "timeout",
    6: "compile_error",
    7: "runtime_error",
    8: "runtime_error",
    9: "runtime_error",
    10: "runtime_error",
    11: "runtime_error",
    12: "runtime_error",
    13: "runner_error",
}


def _config():
    base_url = os.getenv("JUDGE0_URL", "").strip().rstrip("/")
    if not base_url.startswith("https://"):
        raise Judge0Error("Set JUDGE0_URL to the HTTPS URL of your isolated Judge0 service.")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    api_key = os.getenv("JUDGE0_API_KEY", "").strip()
    rapidapi_host = os.getenv("JUDGE0_RAPIDAPI_HOST", "").strip()
    auth_token = os.getenv("JUDGE0_AUTH_TOKEN", "").strip()
    if api_key and rapidapi_host:
        headers["X-RapidAPI-Key"] = api_key
        headers["X-RapidAPI-Host"] = rapidapi_host
    elif auth_token:
        headers["X-Auth-Token"] = auth_token
    elif api_key:
        headers["X-Auth-Token"] = api_key
    return base_url, headers


def _request(url, headers, payload=None, timeout=10):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers=headers, method="GET" if data is None else "POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
        raise Judge0Error("The isolated code execution service did not return a valid response.") from error


def _submit_many(language_id, programs, *, timeout_seconds, memory_mb):
    if not programs:
        return []
    if len(programs) > MAX_BATCH_SIZE:
        raise Judge0Error(f"This exercise exceeds the runner batch limit of {MAX_BATCH_SIZE} test cases.")
    base_url, headers = _config()
    submissions = []
    for program in programs:
        item = {
            "language_id": language_id,
            "source_code": program["source_code"],
            "stdin": program.get("stdin", ""),
            "cpu_time_limit": timeout_seconds,
            "wall_time_limit": timeout_seconds + 8,
            "memory_limit": memory_mb * 1000,
            "max_processes_and_or_threads": 32,
            "enable_network": False,
        }
        submissions.append(item)
    created = _request(
        f"{base_url}/submissions/batch?base64_encoded=false",
        headers,
        {"submissions": submissions},
        timeout=15,
    )
    if not isinstance(created, list) or len(created) != len(programs) or any(not item.get("token") for item in created):
        raise Judge0Error("The isolated runner returned an invalid batch response.")

    deadline = time.monotonic() + timeout_seconds + 30
    tokens = [item["token"] for item in created]
    results_by_token = {}
    pending = tokens
    while pending and time.monotonic() < deadline:
        time.sleep(0.5)
        pending = [token for token in tokens if token not in results_by_token]
        query = urlencode({"tokens": ",".join(pending), "base64_encoded": "false", "fields": "token,stdout,stderr,compile_output,message,status,time"})
        batch = _request(f"{base_url}/submissions/batch?{query}", headers)
        submissions = batch.get("submissions", []) if isinstance(batch, dict) else []
        for result in submissions:
            token = result.get("token")
            status_id = (result.get("status") or {}).get("id")
            if token in pending and status_id not in PENDING_STATUSES:
                results_by_token[token] = result
    if len(results_by_token) != len(tokens):
        raise Judge0Error("The isolated runner timed out while processing submissions.")
    return [results_by_token[token] for token in tokens]


def _status(result):
    status_id = (result.get("status") or {}).get("id")
    return STATUS_NAMES.get(status_id, "runner_error")


def _error_message(result):
    return (result.get("compile_output") or result.get("stderr") or result.get("message") or "Execution failed.")[:400]


def _function_harness(code, function_name, tests):
    payload = json.dumps(tests, ensure_ascii=True)
    return f'''import json
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
            results.append({{"passed": actual == test["expected"], "expected": test["expected"], "actual": actual}})
        except Exception as error:
            results.append({{"passed": False, "error": type(error).__name__ + ": " + str(error)}})
    print("CODEMIND_RESULT:" + json.dumps(results, default=repr))
except BaseException as error:
    print("CODEMIND_ERROR:" + type(error).__name__ + ": " + str(error))
'''


def execute_function(source, function_name, tests, *, timeout_seconds, max_source_bytes):
    if len(source.encode("utf-8")) > max_source_bytes:
        return {"status": "rejected", "message": "Your submission is too large.", "tests": [], "duration_ms": 0}
    started = time.perf_counter()
    program = _function_harness(source, function_name, tests)
    try:
        [result] = _submit_many(LANGUAGE_IDS["python"], [{"source_code": program}], timeout_seconds=timeout_seconds, memory_mb=128)
    except Judge0Error as error:
        raise error
    duration = int((time.perf_counter() - started) * 1000)
    status = _status(result)
    if status != "accepted":
        return {"status": status, "message": _error_message(result), "tests": [], "duration_ms": duration}
    output = result.get("stdout") or ""
    if "CODEMIND_RESULT:" in output:
        try:
            test_results = json.loads(output.rsplit("CODEMIND_RESULT:", 1)[1].strip().splitlines()[0])
        except (json.JSONDecodeError, IndexError):
            test_results = []
        return {"status": "completed", "tests": test_results, "duration_ms": duration, "message": ""}
    if "CODEMIND_ERROR:" in output:
        return {"status": "runtime_error", "message": output.rsplit("CODEMIND_ERROR:", 1)[1].strip()[:400], "tests": [], "duration_ms": duration}
    return {"status": "runtime_error", "message": "The isolated runner returned no test results.", "tests": [], "duration_ms": duration}


def execute_stdio(language, source, tests, *, timeout_seconds, max_source_bytes):
    if language not in LANGUAGE_IDS:
        raise ValueError("Supported judge languages are C, Python, and Java.")
    if len(source.encode("utf-8")) > max_source_bytes:
        return {"status": "rejected", "message": "Your submission is too large.", "tests": [], "duration_ms": 0}
    programs = [{"source_code": source, "stdin": str(test.get("input", ""))} for test in tests]
    started = time.perf_counter()
    results = _submit_many(LANGUAGE_IDS[language], programs, timeout_seconds=timeout_seconds, memory_mb=192)
    duration = int((time.perf_counter() - started) * 1000)
    test_results = []
    failures = []
    for test, result in zip(tests, results):
        status = _status(result)
        if status == "accepted":
            actual = result.get("stdout") or ""
            expected = str(test.get("expected_output", ""))
            test_results.append({"passed": actual.strip() == expected.strip(), "expected": expected, "actual": actual})
        else:
            error = _error_message(result)
            test_results.append({"passed": False, "error": error})
            failures.append(status)
    if "compile_error" in failures:
        return {"status": "compile_error", "message": next((item.get("error", "Compilation failed.") for item in test_results if item.get("error")), "Compilation failed."), "tests": test_results, "duration_ms": duration}
    if "timeout" in failures:
        return {"status": "timeout", "message": "Compilation or execution exceeded the time limit.", "tests": test_results, "duration_ms": duration}
    if failures:
        return {"status": "runtime_error", "message": next((item.get("error", "Execution failed.") for item in test_results if item.get("error")), "Execution failed."), "tests": test_results, "duration_ms": duration}
    return {"status": "completed", "message": "", "tests": test_results, "duration_ms": duration}
