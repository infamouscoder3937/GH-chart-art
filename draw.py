import os
import subprocess
import shutil
from datetime import datetime, timedelta
import argparse
import random

# ==========================
# Style and Colors
# ==========================
class style:
    RESET = '\033[0m'
    BOLD = '\033[01m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'

BANNER = style.GREEN + style.BOLD + """
  ██████╗ ██╗  ██╗  █████╗  ██████╗ ████████╗
 ██╔════╝ ██║  ██║ ██╔══██╗ ██╔══██╗╚══██╔══╝
 ██║  ███╗███████║ ███████║ ██████╔╝   ██║
 ██║   ██║██╔══██║ ██╔══██║ ██╔══██╗   ██║
 ╚██████╔╝██║  ██║ ██║  ██║ ██████╔╝   ██║
  ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝
""" + style.RESET

CREDITS = style.CYAN + "A vibe code project" + style.RESET

# ==========================
# FONT
# ==========================
FONT = {
    'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'], 'B': ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
    'C': ['01110', '10001', '10000', '10000', '10000', '10001', '01110'], 'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
    'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'], 'F': ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
    'G': ['01110', '10001', '10000', '10111', '10001', '10001', '01110'], 'H': ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
    'I': ['01110', '00100', '00100', '00100', '00100', '00100', '01110'], 'J': ['00011', '00001', '00001', '00001', '10001', '10001', '01110'],
    'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'], 'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
    'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'], 'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
    'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'], 'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
    'Q': ['01110', '10001', '10001', '10001', '10101', '10010', '01111'], 'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
    'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'], 'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
    'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'], 'V': ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
    'W': ['10001', '10001', '10001', '10101', '10101', '11011', '10001'], 'X': ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
    'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'], 'Z': ['11111', '00001', '00010', '00100', '01000', '10000', '11111'],
    '0': ['01110', '10001', '10101', '10101', '10101', '10001', '01110'], '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
    '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'], '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'], '5': ['11111', '10000', '10000', '11110', '00001', '10001', '01110'],
    '6': ['01110', '10001', '10000', '11110', '10001', '10001', '01110'], '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'], '9': ['01110', '10001', '10001', '01111', '00001', '10001', '01110'],
    ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
}

# ==========================
# Core Functions
# ==========================
def build_grid(text, total_columns=52):
    """Convert text to a pixel grid."""
    spacing = 1
    rows = 7
    grid = [[] for _ in range(rows)]
    unsupported_chars = set()

    for char in text.upper():
        if char in FONT:
            for r, row_pattern in enumerate(FONT[char]):
                grid[r].extend(list(row_pattern))
            for r in range(rows):
                grid[r].extend(["0"] * spacing)
        else:
            unsupported_chars.add(char)

    if unsupported_chars:
        print(f"{style.YELLOW}Warning: Unsupported characters found and will be skipped: {''.join(unsupported_chars)}{style.RESET}")

    if not any(grid):
        return [[0] * total_columns for _ in range(rows)]

    # Scaling logic remains the same
    factor = total_columns / len(grid[0]) if len(grid[0]) > 0 else 1
    scaled_grid = [[grid[r][int(c / factor)] for c in range(total_columns)] for r in range(rows)]
    return scaled_grid

def get_start_date(year):
    """Get the first Sunday of the year for the graph."""
    d = datetime(year, 1, 1)
    while d.weekday() != 6:  # Sunday = 6
        d -= timedelta(days=1)
    return d

def make_commit(commit_date, message, dry_run=False):
    """Make a commit for a given date."""
    if dry_run:
        # This function is not designed to print in dry run, the main loop handles it.
        return

    with open("commit.txt", "a") as f:
        f.write(f"Commit for {commit_date.isoformat()}\n")
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date.isoformat()
    env["GIT_COMMITTER_DATE"] = commit_date.isoformat()
    
    commit_message = message if message else f"ghART commit for {commit_date.strftime('%Y-%m-%d')}"
    
    subprocess.run(["git", "add", "commit.txt"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(
        ["git", "commit", "-m", commit_message, "--date", commit_date.isoformat()],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def get_commit_dates(year, mode, text=""):
    """Get a list of dates that need commits."""
    start_date = get_start_date(year)
    dates = []

    if mode == 'text':
        grid = build_grid(text)
        for col in range(len(grid[0])):
            for row in range(len(grid)):
                if grid[row][col] == "1":
                    commit_date = start_date + timedelta(weeks=col, days=row)
                    if commit_date.year == year:
                        dates.append(commit_date)
    else:
        day_iterator = timedelta(days=1)
        current_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        while current_date <= end_date:
            if mode == 'fill' or (mode == 'random' and random.random() < 0.4):
                dates.append(current_date)
            current_date += day_iterator
    return dates

# ==========================
# Safety Checks
# ==========================
def is_git_installed():
    """Check if git is installed."""
    return shutil.which("git") is not None

def check_repo_state():
    """Warn if the repository has existing commits."""
    if not os.path.exists(".git"):
        print(f"{style.GREEN}Initializing new git repository...{style.RESET}")
        subprocess.run(["git", "init"], stdout=subprocess.DEVNULL)
        return True

    try:
        # Check for existing commits
        commit_count_str = subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).strip().decode('utf-8')
        commit_count = int(commit_count_str)
        if commit_count > 0:
            print(f"{style.YELLOW}Warning: This repository already contains {commit_count} commits.{style.RESET}")
            if input("Running this script will add many new commits. Continue? (y/n): ").lower() != 'y':
                return False
    except (subprocess.CalledProcessError, ValueError):
        # No commits yet or other error, which is fine
        pass
    return True

# ==========================
# Main Execution
# ==========================
def main():
    print(BANNER)
    print(CREDITS)

    if not is_git_installed():
        print(f"{style.RED}Error: Git is not installed or not found in PATH. Please install Git to use this tool.{style.RESET}")
        return

    parser = argparse.ArgumentParser(description=f"{style.BOLD}Create GitHub contribution art with ghART.{style.RESET}", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--year", type=int, default=datetime.now().year, help="The year to create the art in.")
    parser.add_argument("--text", type=str, default=None, help="The text to display on the contribution graph.")
    parser.add_argument("--message", type=str, default="", help="The commit message to use.")
    parser.add_argument("--level", type=int, default=1, choices=range(1, 6), help="Commit density (1-5). Higher is darker.")
    parser.add_argument("--dry-run", action='store_true', help="Preview the commit dates without making any commits.")
    args = parser.parse_args()

    if not check_repo_state():
        print(f"{style.RED}Aborted by user.{style.RESET}")
        return
    
    mode = 'text' if args.text is not None else None
    
    if mode is None:
        try:
            choice = input(f"No text provided. Would you like to (F)ill the chart or (R)andomize commits? [{style.BOLD}F/R{style.RESET}]: ").upper()
            if choice == 'F':
                mode = 'fill'
            elif choice == 'R':
                mode = 'random'
            else:
                print(f"{style.RED}Invalid choice. Exiting.{style.RESET}")
                return
        except (KeyboardInterrupt, EOFError):
            print(f"\n{style.RED}Aborted by user.{style.RESET}")
            return

    commit_dates = get_commit_dates(args.year, mode, text=args.text or "")
    
    if not commit_dates:
        print(f"{style.YELLOW}No commit dates were generated for the given input. Exiting.{style.RESET}")
        return

    if args.dry_run:
        print(f"\n{style.BOLD}{style.YELLOW}--- DRY RUN MODE ---{style.RESET}")
        total_commits = len(commit_dates) * args.level
        print(f"Year: {args.year}, Mode: {mode}, Level: {args.level}")
        print(f"A total of {style.GREEN}{total_commits}{style.RESET} commits would be made on {style.GREEN}{len(commit_dates)}{style.RESET} unique days.")
        print(f"{style.BOLD}{style.YELLOW}--- END DRY RUN ---{style.RESET}")
        return

    # Create the commits
    with open("commit.txt", "w") as f: # Clear the file at the start
        f.write("ghART commit log\n")

    total_commits = len(commit_dates) * args.level
    print(f"\nGenerating {style.GREEN}{total_commits}{style.RESET} commits for the year {style.BOLD}{args.year}{style.RESET}. This may take a moment...")

    for i, date in enumerate(sorted(commit_dates)):
        for _ in range(args.level):
            make_commit(date, args.message)
        # Simple progress indicator
        progress = int((i + 1) / len(commit_dates) * 20)
        print(f"\rProgress: [{style.GREEN}{'#' * progress}{style.RESET}{'.' * (20 - progress)}]", end="")

    print(f"\n{style.BOLD}{style.GREEN}✅ Done! All commits have been created locally.{style.RESET}")
    print(f"\n{style.BOLD}Next steps:{style.RESET}")
    print(f"1. Set your remote repository: {style.CYAN}git remote add origin https://github.com/user/repo.git{style.RESET}")
    print(f"2. Push your changes: {style.CYAN}git push -u origin main --force{style.RESET}")
    print(f"{style.YELLOW}Don't forget to check your git email configuration if your contributions don't appear!{style.RESET}")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{style.RED}Aborted by user.{style.RESET}")
