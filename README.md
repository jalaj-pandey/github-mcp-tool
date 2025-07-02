# 🚀 MCP Tool for GitHub

## Overview

The **MCP (Model Context Protocol) Tool** helps manage and track model context in GitHub repositories. It allows you to document important details like model versions, datasets, metrics, and training configurations.

## 📦 Overview

The **MCP Tool for GitHub** is designed to help manage:
- Repositories
- Files (create/update/delete)
- User information
- GitHub API requests

## ✨ Features

### 🧑‍💻 1. User Info
- `git_info(username: str)`
  - Fetch public GitHub user profile information.

---

### 📁 2. Repository Management
- `create_repo(repo_name: str, private: bool, description: str)`
  - Create a new repository (private/public).
  
- `delete_repo(username: str, repo_name: str)`
  - Delete a repository by username and repo name.

---

### 📄 3. File Operations in Repository
- `create_file(...)`
  - Add a new file to a repository.
  - Content is automatically base64 encoded.
  
- `update_file(...)`
  - Update an existing file.
  - Requires the file's SHA from GitHub.
  
- `delete_file(...)`
  - Delete a file.
  - Requires SHA and commit message.

---

### 🔄 4. Request Utility
- `make_request(...)`
  - Handles all API interactions (`GET`, `POST`, `PUT`, `DELETE`).
  - Authenticated via GitHub Token.
  - Centralized method to perform various actions like:
    - Create repositories
    - Upload/update/delete files
    - Fetch user/repo data

---

### 🔐 5. Authentication & Setup
- Reads GitHub token securely from `.env` file.
- Sets proper headers (`User-Agent`, `Accept`, `Authorization`).
- Fully asynchronous requests using `httpx`.

---

## 🧰 Prerequisites

- ✅ Python 3.7+
- ✅ Git & uv installed
- ✅ [GitHub Personal Access Token](https://github.com/settings/tokens)

---
## 📁 .env File Format

Create a `.env` file in the root directory and add:

```env
GITHUB_TOKEN=your_personal_access_token_here
```
---

## 🛠️ Setup & Usage

```bash
# Clone the Repo
git clone https://github.com/jalaj-pandey/github-mcp-tool.git

# Change Directory
cd github-mcp-tool

# Initialize virtual environment using uv
uv init
uv venv
.venv/Scripts/activate  # Use `source ./venv/bin/activate` on Unix/Mac

# Add dependencies
uv add mcp[cli] httpx python-dotenv

# Start MCP dev server
mcp dev main.py
```

---
