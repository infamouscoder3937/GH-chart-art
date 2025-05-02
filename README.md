# GitHub Chart Art

A Python CLI tool to automate Git commits to create art on your GitHub contribution graph.

```
██████╗ ██╗  ██╗ █████╗ ██████╗ ████████╗     █████╗ ██████╗ ████████╗
██╔══██╗██║  ██║██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██╔══██╗╚══██╔══╝
██████╔╝███████║███████║██████╔╝   ██║       ███████║██████╔╝   ██║   
██╔═══╝ ██╔══██║██╔══██║██╔══██╗   ██║       ██╔══██║██╔══██╗   ██║   
██║     ██║  ██║██║  ██║██║  ██║   ██║       ██║  ██║██████╔╝   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═════╝    ╚═╝   
```

---

## Features

- **Text to Art:** Convert any text into a pattern on your contribution graph.
- **Fill Chart:** Completely fill your contribution graph for a given year with commits.
- **Randomize Commits:** Make commits on random days throughout a chosen year.
- **Customizable:** Choose the year, the text, and the commit message.

## Requirements

- Python 3.x
- Git

## Setup

1.  **Clone the repository or download the files.**
2.  **Open a terminal** in the project directory.
3.  **Initialize a new Git repository** in the directory where you want to create the commits. This can be a new, empty repository that you will link to GitHub.

    ```bash
    git init
    ```

## Usage

The script `draw.py` is the main entry point for all operations.

### 1. Draw Text on the Chart

Use the `--text` argument to specify the string you want to draw. You can also specify the `--year` and a custom `--message` for the commits.

```bash
python draw.py --text "HELLO WORLD" --year 2024 --message "Custom commit message"
```

- `--text`: The text to display on the contribution graph.
- `--year`: (Optional) The year to create the art in. Defaults to the current year.
- `--message`: (Optional) The commit message to use for all commits.

### 2. Fill the Contribution Chart

To make a commit for every day of a specific year, run the script without the `--text` argument and choose the "Fill" option.

```bash
python draw.py --year 2023
```

This will prompt you:
```
No text provided. Would you like to (F)ill the chart completely or (R)andomize commits? [F/R]: F
```

### 3. Randomize Commits

To make commits on random days of a specific year, run the script without the `--text` argument and choose the "Randomize" option.

```bash
python draw.py --year 2022
```

This will prompt you:
```
No text provided. Would you like to (F)ill the chart completely or (R)andomize commits? [F/R]: R
```

## Pushing to GitHub

This script **only creates the commits locally**. It does not push them to a remote repository. You must do this manually.

```bash
# Link your local repository to a remote GitHub repository
# Replace with your GitHub repository URL
git remote add origin https://github.com/your-username/your-repo.git

# Push the commits
git push -u origin main --force
```

**Note:** You may need to use `--force` because you are rewriting the history of the repository.

## ❗ Important: Troubleshooting

### Why can't I see my contributions on the graph?

This is the most common problem. For your commits to appear on your GitHub contribution graph, the email address used for the commits **must** be associated with your GitHub account.

**1. Check your local Git email:**
```bash
git config user.email
```

**2. Check your GitHub emails:**
Go to your GitHub email settings: [https://github.com/settings/emails](https://github.com/settings/emails). The email from the command above must be in this list.

**3. If they don't match, update your local Git email:**
```bash
git config --global user.email "your-github-email@example.com"
```

After updating your email, you must **delete the local repository (including the hidden `.git` folder), re-initialize it, and re-run the script** to generate the commits with the correct email address.

### Commits with Future Dates

If you create commits for a future year (e.g., 2026), they will **not** appear on your contribution graph until that date actually arrives. This is the expected behavior of GitHub.

---

*A vibe coded project* 