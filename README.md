# ghART

A Python CLI tool to automate Git commits and turn your GitHub contribution graph into a work of art.

<pre>
      ▄██████▄     ▄██████▄   ▄█       ▄████████    ▄████████
     ███    ███   ███    ███ ███      ███    ███   ███    ███
     ███    ███   ███    ███ ███      ███    █▀    ███    █▀
    ▄███    ███  ▄███    ███ ███     ▄███▄▄▄      ▄███▄▄▄
    ▀▀███████▀  ▀▀███████▀  ███    ▀▀███▀▀▀     ▀▀███▀▀▀
     ███    ███   ███    ███ ███      ███    █▄    ███    █▄
     ███    ███   ███    ███ ███      ███    ███   ███    ███
    ███    █▀    ███    █▀  ██████████████████   ██████████
</pre>

---

## Features

- **Menu-Driven:** An easy-to-use main menu to guide you through the options.
- **Multiple Art Modes:**
  - **Text Art:** Convert any text into a pattern on your contribution graph.
  - **Fill Graph:** Fill every day of a year with commits.
  - **Randomize Graph:** Commit on random days throughout a year.
- **Flexible Commit Density:** Specify a **minimum and maximum** number of commits per day for ultimate control over your graph's appearance.
- **Fun Animations:** Watch a fun ASCII animation while the script generates your commits.
- **Safety First:** The tool checks if Git is installed and initializes a new repository for you if needed.

## How to Use

Using ghART is simple. No command-line arguments are needed to get started.

1.  **Run the script:**
    ```bash
    python draw.py
    ```
2.  **Choose an option** from the main menu.
3.  **Follow the prompts** for the year and commit density.

## Menu Options Explained

### 1. Create Text Art
This mode lets you draw a word or phrase on your graph.
- **Commit Count:** You will be asked for a **fixed** number of commits to create for each "pixel" of the art to ensure it looks clean and uniform.

### 2. Fill The Graph
This mode will create commits for **every day** of the chosen year.
- **Commit Range:** You will be asked for a **minimum and maximum** number of commits. For each day, a random number of commits within this range will be created, producing a natural, varied look.

### 3. Randomize The Graph
This mode will create commits on **random days** of the chosen year.
- **Commit Range:** Like the Fill option, the number of commits on each random day will be a random number within your specified min/max range.

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

After updating your email, you must **delete the local repository (including the hidden `.git` folder) and start over**.

---

*A vibe code project*