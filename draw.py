import os
import subprocess
from datetime import datetime, timedelta

# ==========================
# CONFIG
# ==========================
TEXT = "FOO"
YEAR = 2012
COMMITS_PER_PIXEL = 1  # Increase this for darker pixels

# Simple block font (5x7 for each character)
FONT = {
    "M": [
        "11111","10001","10101","10101","10001","10001","10001",
    ],
    "I": [
        "11111","00100","00100","00100","00100","00100","11111",
    ],
    "D": [
        "11110","10001","10001","10001","10001","10001","11110",
    ],
    "H": [
        "10001","10001","10001","11111","10001","10001","10001",
    ],
    "U": [
        "10001","10001","10001","10001","10001","10001","11111",
    ],
    "N": [
        "10001","11001","10101","10011","10001","10001","10001",
    ],
    "7": [
        "11111","00001","00010","00100","01000","10000","10000",
    ]
}

# ==========================
# Functions
# ==========================

def build_grid(text, total_columns=52):
    """Convert text to a pixel grid scaled to fill all 52 weeks"""
    spacing = 1
    rows = 7
    # Build base pattern
    grid = [[] for _ in range(rows)]
    for char in text.upper():
        if char in FONT:
            for r, row_pattern in enumerate(FONT[char]):
                grid[r].extend(list(row_pattern))
            # Add spacing between letters
            for r in range(rows):
                grid[r].extend(["0"] * spacing)

    # Scale horizontally to fit 52 columns
    factor = total_columns / len(grid[0])
    scaled_grid = [[] for _ in range(rows)]
    for r in range(rows):
        for c in range(total_columns):
            # Map new column to old pattern index
            old_c = int(c / factor)
            scaled_grid[r].append(grid[r][old_c])
    return scaled_grid

def get_start_date(year):
    """Get the first Sunday before or on Jan 1 of the year"""
    d = datetime(year, 1, 1)
    while d.weekday() != 6:  # Sunday = 6
        d -= timedelta(days=1)
    return d

def make_commit(commit_date):
    """Make a commit for a given date"""
    with open("commit.txt", "w") as f:
        f.write(f"Commit for {commit_date}\n")
    subprocess.run(["git", "add", "commit.txt"])
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = commit_date.isoformat()
    subprocess.run(
        ["git", "commit", "--date", commit_date.isoformat(), "-m", f"Commit for {commit_date}"],
        env=env,
    )

def draw_message(text, year):
    start_date = get_start_date(year)
    grid = build_grid(text, total_columns=52)

    for col in range(len(grid[0])):  # weeks
        for row in range(len(grid)):  # days
            if grid[row][col] == "1":
                commit_date = start_date + timedelta(weeks=col, days=row)
                for _ in range(COMMITS_PER_PIXEL):
                    make_commit(commit_date)

if __name__ == "__main__":
    # Init repo if needed
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])

    draw_message(TEXT, YEAR)
    print(f"✅ Done! Now run:\n\n  git remote add origin https://github.com/xxxxxxx\n  git branch -M main\n  git push -u origin main")
