### README.md for GitHub Repository Information Script

---

## Overview
This script fetches and formats information from a specified GitHub repository, including its directory structure and the contents of select files. The script requires a GitHub personal access token to authenticate API requests and outputs the information into a text file.

## Prerequisites
- Python 3.6 or later
- `pip` for installing Python packages
- Access to a GitHub account to generate a personal access token

## Setup

### 1. Install Required Packages
Before running the script, you need to install the required Python packages. You can install these using `pip`:

```bash
pip install requests python-dotenv
```

### 2. GitHub Personal Access Token
You will need a GitHub personal access token with the appropriate permissions to fetch repository data. Follow these steps to generate a token:

- Log in to your GitHub account.
- Navigate to **Settings** > **Developer settings** > **Personal access tokens**.
- Click on **Generate new token**.
- Select the scopes or permissions you'd like to grant this token (e.g., `repo` for full control of private repositories).
- Click **Generate token** at the bottom of the page.
- **Important:** Copy your new personal access token. You won’t be able to see it again!

### 3. Create `.env` File
Create a `.env` file in the same directory as your script with the following content:

```plaintext
GITHUB_TOKEN=your_token_here
```

Replace `your_token_here` with your GitHub personal access token.

## Running the Script

### Command Line Interface
To run the script, use the following command from the terminal:

```bash
python export.py https://github.com/your/repo
```

Replace `export.py` with the name of your Python script file, and `https://github.com/your/repo` with the GitHub repository URL you want to analyze.

### Output
The script will generate a file named `*-formatted-prompt.txt` (where `*` is the repository name) containing the repository information. It will also generate a `requirements.txt` file listing all installed Python packages.

## Note
This script is intended for educational and development purposes only. Ensure that your token is stored securely and not exposed in public or shared environments.