# ghART

A Python CLI tool to automate Git commits and turn your GitHub contribution graph into a work of art.

```
  ██████╗ ██╗  ██╗  █████╗  ██████╗ ████████╗
 ██╔════╝ ██║  ██║ ██╔══██╗ ██╔══██╗╚══██╔══╝
 ██║  ███╗███████║ ███████║ ██████╔╝   ██║
 ██║   ██║██╔══██║ ██╔══██║ ██╔══██╗   ██║
 ╚██████╔╝██║  ██║ ██║  ██║ ██████╔╝   ██║
  ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝
```

---

## Features

- **Text to Art:** Convert any text into a pattern on your contribution graph.
- **Fill Chart:** Completely fill your contribution graph for a given year.
- **Randomize Commits:** Make commits on random days throughout a chosen year.
- **Commit Density:** Control the "shade" of green on your graph with a `--level` setting (1-5).
- **Dry Run Mode:** Preview your art without making a single commit using `--dry-run`.
- **Safety First:** The tool checks if Git is installed and warns you before adding to a repository with an existing history.
- **User-Friendly:** Colorful and clear output makes the tool easy and fun to use.

## Requirements

- Python 3.x
- Git

## Setup

1.  Clone the repository or download the `draw.py` script.
2.  Open a terminal in the project directory.
3.  For best results, start in a new, empty folder and the script will initialize the repository for you.

## Usage

The script `draw.py` is the main entry point. All arguments are optional.

### Command-Line Arguments

| Argument      | Description                                                 | Default        | Example                               |
|---------------|-------------------------------------------------------------|----------------|---------------------------------------|
| `--text`      | The text to draw on the chart.                              | `None`         | `--text "ART"`                          |
| `--year`      | The target year for the commits.                            | Current Year   | `--year 2023`                         |
| `--level`     | The commit density (1-5). Higher is a darker green.         | `1`            | `--level 5`                           |
| `--message`   | A custom commit message to use for all commits.             | `ghART commit` | `--message "My project setup"`        |
| `--dry-run`   | Preview the commits without actually running them.          | `False`        | `--dry-run`                           |

### 1. Draw Text on the Chart

Create art with specific text. Use `--level` to make it stand out.

```bash
python draw.py --text "HELLO" --year 2024 --level 3
```

### 2. Fill the Contribution Chart

Run the script without `--text` and choose the "Fill" option. This will commit on every day of the year.

```bash
python draw.py --year 2023 --level 5
```

### 3. Randomize Commits

Run without `--text` and choose the "Randomize" option for a more natural, sporadic pattern.

```bash
python draw.py --year 2022 --level 2
```

### 4. Preview with Dry Run

Before you commit, see what your art will look like. The `--dry-run` flag works with all modes.

```bash
python draw.py --text "PREVIEW" --year 2025 --dry-run
```

## Pushing to GitHub

This script **only creates the commits locally**. You must push them to GitHub yourself.

```bash
# 1. Link your local repository to a remote GitHub repository
# (Replace with your GitHub repository URL)
git remote add origin https://github.com/your-username/your-repo.git

# 2. Push the commits (a force push is often required)
git push -u origin main --force
```

## ❗ Important: Troubleshooting

### "Why can't I see my contributions on the graph?"

This is the most common problem. For your commits to appear, the email in your local Git config **must** be one of the emails associated with your GitHub account.

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

After updating your email, you must **delete the local repository (including the hidden `.git` folder), re-initialize it, and re-run the script**.

---

*A vibe code project*