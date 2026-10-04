from openai import OpenAI
import subprocess
import sys

from github_client import get_issue, create_pull_request
from git_client import (
    prepare_main,
    create_branch,
    commit_changes,
    push_branch
)


ISSUE_NUMBER = 3
MAX_ATTEMPTS = 3

BRANCH_NAME = "fix/issue-3-zero-exchange-rate"
COMMIT_MESSAGE = "Fix zero exchange rate validation"

client = OpenAI()


def read_code():
    with open("currency_converter.py", "r") as file:
        return file.read()


def ask_ai(prompt):
    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text


def write_code(code):

    code = code.strip()

    if code.startswith("```python"):
        code = code[len("```python"):].strip()

    if code.startswith("```"):
        code = code[3:].strip()

    if code.endswith("```"):
        code = code[:-3].strip()

    with open("currency_converter.py", "w") as file:
        file.write(code + "\n")


def run_tests():

    tests = [
        {
            "name": "Valid conversion",
            "input": "100\n83.5\n",
            "expected": "Converted amount: 8350.00"
        },
        {
            "name": "Zero exchange rate",
            "input": "100\n0\n",
            "expected": "Error: Exchange rate cannot be zero."
        },
        {
            "name": "Negative amount",
            "input": "-100\n83.5\n",
            "expected": "Error: Amount cannot be negative."
        }
    ]

    all_passed = True
    failures = []

    for test in tests:

        print(f"\nRunning test: {test['name']}")

        result = subprocess.run(
            [sys.executable, "currency_converter.py"],
            input=test["input"],
            text=True,
            capture_output=True
        )

        output = result.stdout.strip()
        error_output = result.stderr.strip()

        print(f"Output: {output}")

        if error_output:
            print(f"Error: {error_output}")

        if test["expected"] in output:
            print("PASS")
        else:
            print("FAIL")

            all_passed = False

            failures.append(
                f"""
Test: {test['name']}

Expected:
{test['expected']}

Actual:
{output}

Error:
{error_output}
"""
            )

    return all_passed, failures


print("=" * 60)
print("AI GITHUB AGENT")
print("=" * 60)

print("\nReading GitHub issue...")

issue = get_issue(ISSUE_NUMBER)

print(f"Issue #{issue['number']}")
print(f"Title: {issue['title']}")
print(f"Description: {issue['description']}")


# --------------------------------------------------
# Use the existing fix branch
# --------------------------------------------------

print("\nChecking Git branch...")

print(f"Using branch: {BRANCH_NAME}")

# We are already working on the issue branch.
# Do NOT switch to main here.


original_code = read_code()

print("\nExisting code:")
print("-" * 60)
print(original_code)
print("-" * 60)


prompt = f"""
You are modifying an existing Python project.

GitHub issue:

Issue #{issue['number']}
Title: {issue['title']}

Description:
{issue['description']}

Existing code:

{original_code}

Task:

Modify the existing code to satisfy the GitHub issue.

IMPORTANT RULES:

1. Make the smallest possible change.
2. Preserve all existing functionality.
3. Do not remove existing validation.
4. Do not rewrite the whole program unnecessarily.
5. Return the complete Python file.
6. Return ONLY Python code.
7. Do not use markdown code fences.
"""

print("\nAsking AI to implement the issue...")

generated_code = ask_ai(prompt)

write_code(generated_code)

print("\nAI changes written to currency_converter.py")


# --------------------------------------------------
# Test and retry
# --------------------------------------------------

all_tests_passed = False

for attempt in range(1, MAX_ATTEMPTS + 1):

    print("\n" + "=" * 60)
    print(f"TEST ATTEMPT {attempt}/{MAX_ATTEMPTS}")
    print("=" * 60)

    all_tests_passed, failures = run_tests()

    if all_tests_passed:

        print("\nALL TESTS PASSED!")
        break

    if attempt < MAX_ATTEMPTS:

        print("\nTests failed.")
        print("Asking AI to fix the failures...")

        failure_details = "\n".join(failures)
        current_code = read_code()

        fix_prompt = f"""
You are fixing a Python program.

GitHub issue:

Title:
{issue['title']}

Description:
{issue['description']}

Current code:

{current_code}

The automated tests failed.

Failure details:

{failure_details}

Fix the code so that the issue is correctly implemented.

IMPORTANT RULES:

1. Make the smallest possible change.
2. Preserve existing functionality.
3. Do not remove existing validation.
4. Return the complete Python file.
5. Return ONLY Python code.
6. Do not use markdown code fences.
"""

        fixed_code = ask_ai(fix_prompt)

        write_code(fixed_code)

    else:

        print("\nMaximum attempts reached.")


# --------------------------------------------------
# Commit and Push
# --------------------------------------------------

if all_tests_passed:

    print("\n" + "=" * 60)
    print("GIT OPERATIONS")
    print("=" * 60)

    print("\nCommitting changes...")

    commit_changes(COMMIT_MESSAGE)

    print("\nPushing branch to GitHub...")

    push_branch(BRANCH_NAME)
    print("\nCreating Pull Request...")

    pull_request = create_pull_request(
        branch_name=BRANCH_NAME,
        title=f"Fix: {issue['title']}",
        body=f"""## Summary

Implements GitHub Issue #{issue['number']}.

### Changes

{issue['description']}

### Automated Tests

- Valid conversion: PASS
- Zero exchange rate: PASS
- Negative amount: PASS

All automated tests passed before creating this Pull Request.
"""
    )

    print("\n" + "=" * 60)
    print("PULL REQUEST CREATED")
    print("=" * 60)

    print(f"PR #{pull_request['number']}")
    print(f"Title: {pull_request['title']}")
    print(f"URL: {pull_request['url']}")

    print("\n" + "=" * 60)
    print("SUCCESS")
    print("=" * 60)

    print(f"Branch: {BRANCH_NAME}")
    print("Changes committed and pushed to GitHub.")

else:

    print("\n" + "=" * 60)
    print("FAILED")
    print("=" * 60)

    print("Tests failed.")
    print("No Git commit or push was performed.")