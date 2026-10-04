import subprocess


def run_git(command):
    """Run a Git command and return its output."""

    result = subprocess.run(
        ["git"] + command,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Git command failed:\n"
            f"git {' '.join(command)}\n\n"
            f"{result.stderr}"
        )

    return result.stdout.strip()


def prepare_main():
    """Switch to main and update it from GitHub."""

    print("Switching to main...")

    run_git(["checkout", "main"])

    print("Updating main from GitHub...")

    run_git(["pull", "origin", "main"])

    print("Main is up to date.")


def create_branch(branch_name):
    """Create a new branch from the current branch."""

    print(f"Creating branch: {branch_name}")

    run_git(["checkout", "-b", branch_name])

    print(f"Branch created: {branch_name}")


def commit_changes(message):
    """Stage and commit the modified source file."""

    print("Adding changed files...")

    run_git(["add", "currency_converter.py"])

    print("Creating commit...")

    output = run_git([
        "commit",
        "-m",
        message
    ])

    print(output)


def push_branch(branch_name):
    """Push the branch to GitHub."""

    print(f"Pushing branch: {branch_name}")

    output = run_git([
        "push",
        "-u",
        "origin",
        branch_name
    ])

    print(output)