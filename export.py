import requests
import base64
from urllib.parse import urlparse


def parse_github_url(url):
    """
    Parses your GitHub URL and extracts the repository owner and name.
    """
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip("/").split("/")
    if len(path_segments) >= 2:
        owner, repo = path_segments[0], path_segments[1]
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL provided!")


def fetch_repo_content(owner, repo, path="", token=None):
    """
    Fetches the content of your GitHub repository.
    """
    print(f"Fetching content from {owner}/{repo}/{path}")
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_file_content(file_info):
    """
    Retrieves and decodes the content of files.
    """
    if file_info["encoding"] == "base64":
        return base64.b64decode(file_info["content"]).decode("utf-8")
    else:
        return file_info["content"]


def build_directory_tree(owner, repo, token, path="", indent=0, file_paths=[]):
    """
    Builds a string representation of the directory tree and collects file paths.
    """
    if not token:
        raise ValueError("GitHub token is required to access the repository content.")
    items = fetch_repo_content(owner, repo, path, token)
    tree_str = ""
    for item in items:
        if item["type"] == "dir":
            tree_str += "    " * indent + f"[{item['name']}/]\n"
            tree_str += build_directory_tree(
                owner, repo, token, item["path"], indent + 1, file_paths
            )[0]
        else:
            tree_str += "    " * indent + f"{item['name']}\n"
            files_supported = [
                ".py",
                ".html",
                ".css",
                ".js",
                ".jsx",
                ".rst",
                ".md",
                ".tsx",
                ".ts",
                ".swift",
            ]
            if item["name"].endswith((tuple(files_supported))):
                file_paths.append((indent, item["path"]))
    print(tree_str)
    return tree_str, file_paths


def retrieve_github_repo_info(url, token):
    """
    Retrieves and formats repository information.
    """
    owner, repo = parse_github_url(url)
    directory_tree, file_paths = build_directory_tree(owner, repo, token=token)
    formatted_string = f"Directory Structure:\n{directory_tree}\n"
    for indent, path in file_paths:
        file_info = fetch_repo_content(owner, repo, path, token)
        file_content = get_file_content(file_info)
        formatted_string += f"\n{'    ' * indent}{path}:\n{'    ' * indent}```\n{file_content}\n{'    ' * indent}```\n"
    return formatted_string
