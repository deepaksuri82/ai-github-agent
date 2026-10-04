import os

from github import Github, Auth


# --------------------------------------------------
# Configuration
# --------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPOSITORY = "deepaksuri82/ai-github-agent"


# --------------------------------------------------
# Connect to GitHub
# --------------------------------------------------

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not configured.")

auth = Auth.Token(GITHUB_TOKEN)

github = Github(auth=auth)


# --------------------------------------------------
# Get repository
# --------------------------------------------------

def get_repository():
    return github.get_repo(REPOSITORY)


# --------------------------------------------------
# Get GitHub Issue
# --------------------------------------------------

def get_issue(issue_number):

    repo = get_repository()

    issue = repo.get_issue(number=issue_number)

    return {
        "number": issue.number,
        "title": issue.title,
        "description": issue.body or ""
    }


# --------------------------------------------------
# Create Pull Request
# --------------------------------------------------

def create_pull_request(
    branch_name,
    title,
    body,
    base_branch="main"
):

    repo = get_repository()

    pull_request = repo.create_pull(
        title=title,
        body=body,
        head=branch_name,
        base=base_branch
    )

    return {
        "number": pull_request.number,
        "url": pull_request.html_url,
        "title": pull_request.title
    }


# --------------------------------------------------
# Test GitHub connection
# --------------------------------------------------

if __name__ == "__main__":

    issue = get_issue(3)

    print(f"Issue number: {issue['number']}")
    print(f"Title: {issue['title']}")

    print("Description:")
    print(issue["description"])