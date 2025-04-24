from typing import Any
import httpx
import os
import base64
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("Github Mcp")

BASE_URL = "https://api.github.com/"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USER_AGENT = "FastMCP-App"


async def make_request(url: str,data: dict[str, Any]|None,used :str) -> dict[str, Any] | None:
    """Make an API request to the GitHub API."""
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": USER_AGENT 
    }
    async with httpx.AsyncClient() as client:
        try:
            if used== "delete":
                response = await client.delete(url, headers=headers)
                if response.status_code == 204:
                    return {"message": "Repository deleted successfully."}
                else:
                    return {"error": response.text}
            elif used == "create":
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()
            elif used == "put":
                response = await client.put(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()
            elif used == "delete_file":
                response = await client.request("DELETE", url, headers=headers, json=data)
                if response.status_code in (200, 204):
                    return {"message": "File deleted successfully."}
                else:
                    return {"error": response.text}
            else:
                response = await client.get(url, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Request failed: {e}")
            return None

@mcp.tool()
async def git_info(username: str) -> dict[str, Any] | None:
    """Get GitHub user info by username."""
    url = f"{BASE_URL}users/{username}"
    used_for = "info"
    return await make_request(url,None,used_for)

@mcp.tool()
async def create_repo(repo_name:str,private:bool,description :str="") -> dict[str, Any] | None:
    """
    Creates a new GitHub repository.

    Args:
        repo_name: Name of the repository to create.
        private: Whether the repo is private. Default is True.
        description: Optional description of the repo.

    Returns:
        JSON response from GitHub API or error.
    """
    payload = {
        "name": repo_name,
        "private": private,
        "description": description
    }
    url = f"{BASE_URL}user/repos"
    used_for = "create"
    return await make_request(url,payload,used_for)
@mcp.tool()
async def delete_repo(username: str, repo_name: str) -> dict[str, Any] | None:
    """
    Deletes a GitHub repository.

    Args:
        owner: The username or organization name that owns the repo.
        repo_name: The name of the repository to delete.

    Returns:
        A success message or error.
    """
    url = f"{BASE_URL}repos/{username}/{repo_name}"
    used_for = "delete"
    return await make_request(url,None,used_for)

@mcp.tool()
async def create_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    commit_message: str,
    branch: str = "main",
) -> dict[str, Any] | None:
    """
    Creates a new file in the specified GitHub repository.

    Args:
        owner: Repository owner's username.
        repo: Name of the repository.
        path: The file path (e.g. "folder/filename.txt").
        content: Content of the file (will be base64 encoded).
        commit_message: Commit message for the file creation.
        branch: Branch to commit to. Default is 'main'.
        committer_name: Name of the committer (default: GitHub Octocat).
        committer_email: Email of the committer (default: GitHub Octocat).

    Returns:
        JSON response from GitHub API or error.
    """
    url = f"{BASE_URL}repos/{owner}/{repo}/contents/{path}"
    encoded_content = base64.b64encode(content.encode()).decode()

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch,
    }
    used_for = "put" 
    return await make_request(url, payload, used_for)

@mcp.tool()
async def update_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    sha: str,
    commit_message: str,
    branch: str = "main",
) -> dict[str, Any] | None:
    """
    Updates an existing file in the specified GitHub repository.

    Args:
        owner: Repository owner's username.
        repo: Name of the repository.
        path: The file path (e.g. "folder/filename.txt").
        content: New content of the file (will be base64 encoded).
        sha: SHA of the existing file to be updated.
        commit_message: Commit message for the update.
        branch: Branch to commit to. Default is 'main'.
        
    Returns:
        JSON response from GitHub API or error.
    """
    url = f"{BASE_URL}repos/{owner}/{repo}/contents/{path}"
    encoded_content = base64.b64encode(content.encode()).decode()

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "sha": sha,
        "branch": branch,
    }
    used_for = "put"
    return await make_request(url, payload, used_for)

@mcp.tool()
async def delete_file(
    owner: str,
    repo: str,
    path: str,
    sha: str,
    commit_message: str,
    branch: str = "main",
) -> dict[str, Any] | None:
    """
    Deletes a file in the specified GitHub repository.

    Args:
        owner: Repository owner's username.
        repo: Name of the repository.
        path: The file path (e.g. "folder/filename.txt").
        commit_message: Commit message for the deletion.
        sha: SHA of the file blob to delete.
        branch: Branch to commit to. Default is 'main'.
    Returns:
        JSON response from GitHub API or error.
    """
    url = f"{BASE_URL}repos/{owner}/{repo}/contents/{path}"
    payload = {
        "message": commit_message,
        "sha": sha,
        "branch": branch,
    }

    return await make_request(url, payload, "delete_file")
