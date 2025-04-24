# MCP Tool for GitHub

## Overview

The **MCP (Model Context Protocol) Tool** helps manage and track model context in GitHub repositories. It allows you to document important details like model versions, datasets, metrics, and training configurations.

## Features

- Track model versions
- Manage dataset information
- Record performance metrics
- Document training configurations
- Seamless GitHub integration

## Installation
    pip install -r requirements.txt
### Prerequisites

- Python 3.7+
- `git` and `pip`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/jalaj-pandey/github-mcp-tool.git
   cd github-mcp-tool
   uv init
   ./venv/Scripts/activate
   pip install "mcp[cli]"
   mcp dev main.py  
