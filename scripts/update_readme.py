import os
import requests

# Constants
GITHUB_USERNAME = "Rizwan102003"
README_FILE = "README.md"
DEVICON_URL = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons"

# Function to fetch languages from GitHub repositories
def fetch_languages_and_tools(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repositories: {response.status_code}, {response.text}")
    
    languages = set()
    repos = response.json()
    
    for repo in repos:
        if repo.get("language"):
            languages.add(repo["language"])
    
    return languages

# Generate markdown for tools using Devicon
def generate_tools_section(languages):
    tools_md = ""
    
    # Language name to Devicon mapping (for inconsistencies)
    devicon_mapping = {
        "C++": "cplusplus",
        "C#": "csharp",
        "HTML": "html5",
        "CSS": "css3",
        "Jupyter Notebook": "jupyter",
        "Shell": "bash",
        # Add other custom mappings here if needed
    }
    
    for language in sorted(languages):
        # Normalize language names for Devicon
        devicon_name = devicon_mapping.get(language, language.lower().replace(" ", ""))
        icon_url = f"{DEVICON_URL}/{devicon_name}/{devicon_name}-original.svg"
        
        # Check if the icon exists in Devicon
        response = requests.get(icon_url)
        if response.status_code == 200:
            tools_md += (
                f'<img align="left" alt="{language}" width="30px" style="padding-right:10px;" '
                f'src="{icon_url}" />\n'
            )
        else:
            print(f"Icon not found for {language} ({devicon_name}), skipping.")
    
    return tools_md

# Update README.md with the generated tools section
def update_readme(tools_section):
    with open(README_FILE, "r") as file:
        content = file.read()

    # Replace tools section in README
    tools_marker = "### 🔧 Tools"
    tools_start = content.find(tools_marker)
    if tools_start == -1:
        raise Exception(f"'{tools_marker}' section not found in README.md")
    
    tools_end = content.find("---", tools_start)
    if tools_end == -1:
        raise Exception("End of tools section not found in README.md")

    # Insert the updated tools section
    updated_content = (
        content[:tools_start]
        + f"{tools_marker}\n{tools_section}\n<br />\n\n"
        + content[tools_end:]
    )

    with open(README_FILE, "w") as file:
        file.write(updated_content)

if __name__ == "__main__":
    try:
        # Fetch languages and tools
        print("Fetching languages from GitHub repositories...")
        languages = fetch_languages_and_tools(GITHUB_USERNAME)

        # Generate tools section
        print("Generating tools section...")
        tools_section = generate_tools_section(languages)

        # Update README.md
        print("Updating README.md...")
        update_readme(tools_section)

        print("README.md updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
