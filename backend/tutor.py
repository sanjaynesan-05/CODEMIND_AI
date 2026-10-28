import ast


PREREQUISITES = {
    "Expressions and conditions": [],
    "Conditions and loops": ["Expressions and conditions"],
    "Loops and accumulation": ["Conditions and loops"],
    "Loops and list traversal": ["Conditions and loops"],
    "Strings and indexing": [],
    "Recursion and base cases": [],
    "Loops and sequences": ["Conditions and loops"],
    "Lists and membership": ["Conditions and loops"],
    "Java input and output": [],
    "C input and arithmetic": [],
    "Web structure and interaction": [],
    "Arrays & Hashing": [],
    "Two Pointers": ["Arrays & Hashing"],
    "Stack": [],
    "Binary Search": ["Arrays & Hashing"],
    "Sliding Window": ["Arrays & Hashing", "Two Pointers"],
    "Dynamic Programming": ["Arrays & Hashing"],
    "Graphs": [],
    "Loops and Accumulation": [],
    "Strings": [],
    "Math & Logic": [],
    "Recursion & DP": [],
    "Input & Arithmetic": [],
}

HINTS = {
    "Loops and accumulation": [
        "What should happen to your running total each time you visit one number?",
        "Look at the loop body: update `total` with the current number before returning it.",
    ],
    "Conditions and loops": [
        "Which characters should increase your count, and how can you check each one?",
        "Normalize the text to one case, then use a condition inside a loop to recognize vowels.",
    ],
    "Expressions and conditions": [
        "What remainder do even numbers leave when divided by 2?",
        "Use `%` to get the remainder, then compare it with zero.",
    ],
    "Loops and list traversal": [
        "How could you keep track of the best value seen so far?",
        "Start with the first item and compare each remaining item to your current largest value.",
    ],
    "Recursion and base cases": [
        "What is the simplest factorial result that should be returned without another recursive call?",
        "Add a base case for 0 or 1, then make the recursive call with a smaller number.",
    ],
    "Strings and indexing": [
        "Python strings support operations that create a reversed copy. Which operation changes the direction of a sequence?",
        "Try a slice with a step of -1.",
    ],
    "Loops and sequences": [
        "Which two values do you need to remember to build the next Fibonacci number?",
        "Keep the previous and current values, then update both on each iteration.",
    ],
    "Lists and membership": [
        "How can you tell whether you have already added an item to your result list?",
        "Check membership before appending so the first occurrence keeps its position.",
    ],
    "Java input and output": [
        "What values arrive through standard input, and which Scanner method reads each integer?",
        "Read the two integers into variables, add them, and print only the sum.",
    ],
    "C input and arithmetic": [
        "Which standard-library function reads an integer from standard input?",
        "Use `scanf` with the address of the integer variable, then print the value multiplied by itself.",
    ],
    "Web structure and interaction": [
        "Which file should define the card's appearance, and which file should respond to the button click?",
        "Select the button and message by their IDs, then update the message element's `textContent` in a click handler.",
    ],
}


def code_facts(code: str) -> dict:
    facts = {"has_return": False, "has_loop": False, "has_condition": False, "recursive_call": False}
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return facts
    functions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    facts["has_return"] = any(isinstance(node, ast.Return) for node in ast.walk(tree))
    facts["has_loop"] = any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
    facts["has_condition"] = any(isinstance(node, ast.If) for node in ast.walk(tree))
    for function in functions:
        facts["recursive_call"] |= any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function.name for node in ast.walk(function))
    return facts


def diagnose(exercise: dict, code: str, run: dict) -> dict:
    failed = [result for result in run.get("tests", []) if not result.get("passed")]
    total = len(run.get("tests", []))
    facts = code_facts(code)
    category = exercise["concept"]
    if exercise.get("execution_mode") == "browser" and run["status"] == "completed":
        if total and not failed:
            title = "All browser checks passed"
            evidence = [f"The preview passed all {total} browser checks."]
            confidence = 0.95
        elif total:
            title = "Some browser checks need attention"
            evidence = [f"{len(failed)} of {total} browser checks failed."]
            evidence.extend(result.get("label") or result.get("message") or "Review this browser check." for result in failed[:4])
            confidence = 0.78
        else:
            title = "No browser checks were returned"
            evidence = ["Run the browser checks from the preview before submitting."]
            confidence = 0.9
    elif run["status"] == "syntax_error":
        title = "There is a syntax issue"
        evidence = [run["message"]]
        confidence = 0.99
        category = "Syntax and structure"
    elif run["status"] == "timeout":
        title = "The program did not finish in time"
        evidence = ["The isolated runner stopped the submission after its time limit."]
        confidence = 0.92
    elif run["status"] == "runtime_error":
        message = run.get("message", "Execution failed.")
        title = "A list index may be outside its bounds" if "IndexError" in message else "The program stopped with a runtime error"
        evidence = [message]
        confidence = 0.95
    elif run["status"] == "compile_error":
        title = "The program did not compile"
        evidence = [run.get("message", "Review the compiler output.")]
        confidence = 0.98
    elif exercise.get("execution_mode") in {"stdin_stdout", "multi_language_stdio"} and run["status"] == "completed":
        if total and not failed:
            title = "All checks passed"
            evidence = [f"The solution produced the expected output for all {total} test cases."]
            confidence = 1.0
        else:
            title = "Some expected output did not match"
            evidence = [f"{len(failed)} of {total} test cases failed."]
            if failed:
                evidence.append(f"Example expected {failed[0].get('expected')!r}, received {failed[0].get('actual')!r}.")
            confidence = 0.78
    elif run["status"] == "rejected":
        title = "This submission could not be checked"
        evidence = [run.get("message", "The submission did not meet the runner's limits.")]
        confidence = 1.0
    elif run["status"] == "completed" and total > 0 and not failed:
        title = "All checks passed"
        evidence = [f"The function passed all {total} supplied tests."]
        confidence = 1.0
    elif run["status"] == "completed" and total == 0:
        title = "The test results could not be read"
        evidence = ["The isolated runner returned no test results."]
        confidence = 0.9
    else:
        title = "Some expected results did not match"
        evidence = [f"{len(failed)} of {total} tests failed."]
        if all("actual" not in test for test in failed):
            evidence.extend(test.get("error", "An exception occurred") for test in failed[:2])
        else:
            evidence.extend([f"Example expected {failed[0].get('expected')!r}, received {failed[0].get('actual')!r}."])
        if exercise["concept"] == "Recursion and base cases" and facts["recursive_call"] and not facts["has_condition"]:
            title = "A stopping condition may be missing"
            evidence.append("The function calls itself, but no conditional branch appears in the parsed code.")
            confidence = 0.82
        elif not facts["has_return"]:
            title = "A return statement may be missing"
            evidence.append("The function has no parsed `return` statement, so Python would return `None` by default.")
            confidence = 0.76
        elif exercise["concept"].startswith("Loops") and not facts["has_loop"] and "loop" in exercise["description"].lower():
            title = "The list may not be fully traversed"
            evidence.append("The exercise asks for repeated processing, but no loop was found in the code structure.")
            confidence = 0.73
        elif facts["has_loop"] and any(type(test.get("expected")) is int and type(test.get("actual")) is int and abs(test["expected"] - test["actual"]) == 1 for test in failed):
            title = "A loop boundary may be off by one"
            evidence.append("At least one integer result differs from its expected value by exactly one, and the code contains a loop.")
            confidence = 0.67
        else:
            confidence = 0.68
    return {
        "title": title,
        "category": category,
        "confidence": confidence,
        "evidence": evidence,
        "facts": facts,
        "explanation": "This is a possible explanation based on the code structure and observed test results. It is not a claim about what you were thinking.",
    }


def next_hint(concept: str, current_level: int, solution: str | None = None) -> dict:
    if solution is not None:
        return {"level": 3, "label": "Worked solution", "content": solution}
    hints = HINTS.get(concept, ["Review the failing example and trace what your function returns.", "Check the relevant condition or update in the function."])
    index = min(current_level, len(hints) - 1)
    return {"level": index + 1, "label": "Conceptual hint" if index == 0 else "Structural hint", "content": hints[index]}


def update_bkt(prior: float, correct: bool) -> float:
    # Conservative BKT-style update with explicit, documented assumptions.
    learn = 0.12
    guess = 0.20
    slip = 0.10
    if correct:
        posterior = prior * (1 - slip) / (prior * (1 - slip) + (1 - prior) * guess)
    else:
        posterior = prior * slip / (prior * slip + (1 - prior) * (1 - guess))
    return min(0.99, max(0.01, posterior + (1 - posterior) * learn))
