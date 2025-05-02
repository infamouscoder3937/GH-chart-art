import os
import subprocess
from datetime import datetime, timedelta
import argparse

# ========================== 
# Banner and Credits
# ========================== 
BANNER = """
██████╗ ██╗  ██╗ █████╗ ██████╗ ████████╗     █████╗ ██████╗ ████████╗
██╔══██╗██║  ██║██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██╔══██╗╚══██╔══╝
██████╔╝███████║███████║██████╔╝   ██║       ███████║██████╔╝   ██║   
██╔═══╝ ██╔══██║██╔══██║██╔══██╗   ██║       ██╔══██║██╔══██╗   ██║   
██║     ██║  ██║██║  ██║██║  ██║   ██║       ██║  ██║██████╔╝   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═════╝    ╚═╝   
"""
CREDITS = "A vibe code project "

# ========================== 
# CONFIG
# ========================== 
COMMITS_PER_PIXEL = 1  # Increase this for darker pixels

# Simple block font (5x7 for each character)
FONT = {
    'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
    'B': ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
    'C': ['01110', '10001', '10000', '10000', '10000', '10001', '01110'],
    'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
    'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
    'F': ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
    'G': ['01110', '10001', '10000', '10111', '10001', '10001', '01110'],
    'H': ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
    'I': ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
    'J': ['00011', '00001', '00001', '00001', '10001', '10001', '01110'],
    'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'],
    'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
    'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
    'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
    'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
    'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
    'Q': ['01110', '10001', '10001', '10001', '10101', '10010', '01111'],
    'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
    'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
    'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
    'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
    'V': ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
    'W': ['10001', '10001', '10001', '10101', '10101', '11011', '10001'],
    'X': ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
    'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
    'Z': ['11111', '00001', '00010', '00100', '01000', '10000', '11111'],
    '0': ['01110', '10001', '10101', '10101', '10101', '10001', '01110'],
    '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
    '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'],
    '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
    '5': ['11111', '10000', '10000', '11110', '00001', '10001', '01110'],
    '6': ['01110', '10001', '10000', '11110', '10001', '10001', '01110'],
    '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
    '9': ['01110', '10001', '10001', '01111', '00001', '10001', '01110'],
    ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
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
    if not grid[0]:
        return [[0] * total_columns for _ in range(rows)]

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

def make_commit(commit_date, message=""):
    """Make a commit for a given date"""
    with open("commit.txt", "w") as f:
        f.write(f"Commit for {commit_date}\n")
    subprocess.run(["git", "add", "commit.txt"])
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = commit_date.isoformat()
    commit_message = message if message else f"Commit for {commit_date}"
    subprocess.run(
        ["git", "commit", "--date", commit_date.isoformat(), "-m", commit_message],
        env=env,
    )

def draw_message(text, year, message=""):
    start_date = get_start_date(year)
    grid = build_grid(text, total_columns=52)

    for col in range(len(grid[0])):  # weeks
        for row in range(len(grid)):  # days
            if grid[row][col] == "1":
                commit_date = start_date + timedelta(weeks=col, days=row)
                for _ in range(COMMITS_PER_PIXEL):
                    make_commit(commit_date, message)

def fill_chart(year, message=""):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        for _ in range(COMMITS_PER_PIXEL):
            make_commit(current_date, message)
        current_date += delta

def randomize_commits(year, message="", probability=0.3):
    import random
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        if random.random() < probability:
            for _ in range(COMMITS_PER_PIXEL):
                make_commit(current_date, message)
        current_date += delta

if __name__ == "__main__":
    print(BANNER)
    print(CREDITS)

    parser = argparse.ArgumentParser(description="Create GitHub contribution art.")
    parser.add_argument("--year", type=int, default=datetime.now().year, help="The year to create the art in.")
    parser.add_argument("--text", type=str, default="", help="The text to display on the contribution graph.")
    parser.add_argument("--message", type=str, default="", help="The commit message to use.")
    args = parser.parse_args()

    # Init repo if needed
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])

    if args.text:
        draw_message(args.text, args.year, args.message)
        print(f"✅ Done! '{args.text}' has been drawn in the year {args.year}.")
    else:
        choice = input("No text provided. Would you like to (F)ill the chart completely or (R)andomize commits? [F/R]: ").upper()
        if choice == 'F':
            fill_chart(args.year, args.message)
            print(f"✅ Done! The chart for {args.year} has been filled.")
        elif choice == 'R':
            randomize_commits(args.year, args.message)
            print(f"✅ Done! Randomized commits have been made for {args.year}.")
        else:
            print("Invalid choice. Exiting.")

    print(f"\nNow run:\n\n  git remote add origin https://github.com/xxxxxxx\n  git branch -M main\n  git push -u origin main")
