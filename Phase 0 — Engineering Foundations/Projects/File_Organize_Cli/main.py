import argparse
import hashlib
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
APP_DIR = Path(os.environ.get("FILEORG_HOME", PROJECT_DIR / ".fileorg")).expanduser()
HISTORY_FILE = APP_DIR / "history.json"
TRASH_DIR = APP_DIR / "trash"

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".pptx", ".xlsx"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi"},
    "Audio": {".mp3", ".wav", ".aac", ".flac"},
    "Archives": {".zip", ".rar", ".tar", ".gz", ".7z"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp"},
}

CLEANUP_FILE_NAMES = {".DS_Store", "Thumbs.db"}
CLEANUP_EXTENSIONS = {".pyc", ".tmp"}
CLEANUP_DIR_NAMES = {"__pycache__"}


def setup_app_dir():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    TRASH_DIR.mkdir(exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]")


def resolve_path(path):
    return Path(path).expanduser().resolve()


def get_category(file_path):
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def unique_path(destination):
    if not destination.exists():
        return destination

    counter = 1
    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_path = destination.with_name(new_name)
        if not new_path.exists():
            return new_path
        counter += 1


def safe_move(source, destination_folder):
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination = unique_path(destination_folder / source.name)
    shutil.move(str(source), str(destination))
    return destination


def load_history():
    setup_app_dir()
    try:
        return json.loads(HISTORY_FILE.read_text())
    except json.JSONDecodeError:
        return []


def save_history_entry(command, actions):
    if not actions:
        return

    history = load_history()
    history.append(
        {
            "command": command,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "actions": actions,
        }
    )
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def print_path_error(path, expected="folder"):
    print(f"Error: {path} is not a valid {expected}.")
    if not path.exists():
        print("Reason: this path does not exist.")
        print("Tip: `/fileorg-test` means a folder at the root of your system.")
        print("Try `/tmp/fileorg-test` for a temp folder or `./fileorg-test` for a folder in the current directory.")
    elif expected == "folder" and not path.is_dir():
        print("Reason: this path exists, but it is not a folder.")


def organize(path):
    folder = resolve_path(path)
    if not folder.is_dir():
        print_path_error(folder)
        return

    actions = []
    counts = {}

    for item in folder.iterdir():
        if not item.is_file() or item.name.startswith("."):
            continue

        category = get_category(item)
        destination_folder = folder / category
        destination = safe_move(item, destination_folder)

        actions.append(
            {
                "type": "move",
                "source": str(item),
                "destination": str(destination),
            }
        )
        counts[category] = counts.get(category, 0) + 1

    save_history_entry("organize", actions)

    if not actions:
        print("No files to organize.")
        return

    print(f"Organized {len(actions)} files.")
    for category, count in sorted(counts.items()):
        print(f"{category}: {count}")


def hash_file(file_path):
    sha256 = hashlib.sha256()
    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def find_duplicates(path):
    folder = resolve_path(path)
    if not folder.is_dir():
        print_path_error(folder)
        return

    hashes = {}
    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            file_hash = hash_file(file_path)
        except OSError as error:
            print(f"Skipped {file_path}: {error}")
            continue
        hashes.setdefault(file_hash, []).append(file_path)

    duplicate_groups = [paths for paths in hashes.values() if len(paths) > 1]

    if not duplicate_groups:
        print("No duplicate files found.")
        return

    print(f"Found {len(duplicate_groups)} duplicate groups.")
    for index, group in enumerate(duplicate_groups, start=1):
        print(f"\nDuplicate group {index}:")
        for file_path in group:
            print(f"- {file_path}")


def archive(path, older_than):
    folder = resolve_path(path)
    if not folder.is_dir():
        print_path_error(folder)
        return

    now = time.time()
    older_than_seconds = older_than * 24 * 60 * 60
    archive_root = folder / "Archive"
    actions = []

    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue
        if archive_root in file_path.parents:
            continue

        age_seconds = now - file_path.stat().st_mtime
        if age_seconds <= older_than_seconds:
            continue

        month_folder = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m")
        destination = safe_move(file_path, archive_root / month_folder)
        actions.append(
            {
                "type": "move",
                "source": str(file_path),
                "destination": str(destination),
            }
        )

    save_history_entry("archive", actions)

    if not actions:
        print(f"No files older than {older_than} days found.")
        return

    print(f"Archived {len(actions)} files.")


def format_size(size_in_bytes):
    size = float(size_in_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024


def show_large_files(path, top):
    folder = resolve_path(path)
    if not folder.is_dir():
        print_path_error(folder)
        return

    files = []
    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            files.append((file_path.stat().st_size, file_path))
        except OSError as error:
            print(f"Skipped {file_path}: {error}")

    files.sort(reverse=True, key=lambda item: item[0])

    if not files:
        print("No files found.")
        return

    for index, (size, file_path) in enumerate(files[:top], start=1):
        print(f"{index}. {format_size(size):>9}  {file_path}")


def backup(source, destination):
    source_path = resolve_path(source)
    destination_path = resolve_path(destination)

    if not source_path.is_dir():
        print_path_error(source_path)
        return

    destination_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = unique_path(destination_path / f"{source_path.name}_backup_{timestamp}")
    shutil.copytree(source_path, backup_path)

    file_count = sum(1 for item in backup_path.rglob("*") if item.is_file())
    save_history_entry(
        "backup",
        [
            {
                "type": "backup",
                "destination": str(backup_path),
            }
        ],
    )
    print(f"Backup created: {backup_path}")
    print(f"Copied {file_count} files.")


def move_to_trash(path):
    setup_app_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trash_name = f"{timestamp}_{path.name}"
    destination = unique_path(TRASH_DIR / trash_name)
    shutil.move(str(path), str(destination))
    return destination


def cleanup(path):
    folder = resolve_path(path)
    if not folder.is_dir():
        print_path_error(folder)
        return

    targets = []
    for item in folder.rglob("*"):
        if item.name in CLEANUP_DIR_NAMES and item.is_dir():
            targets.append(item)
        elif item.is_file() and (item.name in CLEANUP_FILE_NAMES or item.suffix in CLEANUP_EXTENSIONS):
            targets.append(item)

    if not targets:
        print("No cleanup files found.")
        return

    print("Cleanup will move these items to FileOrg trash:")
    for target in targets:
        print(f"- {target}")

    answer = input("Continue? [y/N]: ").strip().lower()
    if answer != "y":
        print("Cleanup cancelled.")
        return

    actions = []
    for target in targets:
        if not target.exists():
            continue
        destination = move_to_trash(target)
        actions.append(
            {
                "type": "move",
                "source": str(target),
                "destination": str(destination),
            }
        )

    save_history_entry("cleanup", actions)
    print(f"Moved {len(actions)} items to trash: {TRASH_DIR}")


def undo():
    history = load_history()
    if not history:
        print("Nothing to undo.")
        return

    last_operation = history.pop()
    actions = last_operation.get("actions", [])
    undone = 0

    for action in reversed(actions):
        action_type = action.get("type")

        if action_type == "move":
            source = Path(action["source"])
            destination = Path(action["destination"])
            if destination.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                final_path = unique_path(source)
                shutil.move(str(destination), str(final_path))
                undone += 1
            else:
                print(f"Skipped missing file: {destination}")

        elif action_type == "backup":
            destination = Path(action["destination"])
            if destination.exists() and destination.is_dir():
                answer = input(f"Remove backup folder {destination}? [y/N]: ").strip().lower()
                if answer == "y":
                    shutil.rmtree(destination)
                    undone += 1

    HISTORY_FILE.write_text(json.dumps(history, indent=2))
    print(f"Undone last operation: {last_operation.get('command')}.")
    print(f"Reversed {undone} actions.")


def watch(path, interval):
    folder = resolve_path(path)
    if not folder.is_dir():
        print_path_error(folder)
        return

    seen = {item for item in folder.iterdir()}
    print(f"Watching {folder}. Press Ctrl + C to stop.")

    try:
        while True:
            time.sleep(interval)
            current = {item for item in folder.iterdir()}
            new_items = [item for item in current - seen if item.is_file()]
            seen = current

            if not new_items:
                continue

            time.sleep(2)
            actions = []
            counts = {}
            for item in new_items:
                if not item.exists() or not item.is_file() or item.name.startswith("."):
                    continue
                category = get_category(item)
                destination = safe_move(item, folder / category)
                actions.append(
                    {
                        "type": "move",
                        "source": str(item),
                        "destination": str(destination),
                    }
                )
                counts[category] = counts.get(category, 0) + 1

            save_history_entry("watch", actions)
            if actions:
                print(f"Organized {len(actions)} new files.")
                for category, count in sorted(counts.items()):
                    print(f"{category}: {count}")

    except KeyboardInterrupt:
        print("\nWatch stopped.")


def parse_interval(interval_text):
    unit = interval_text[-1]
    value_text = interval_text[:-1]

    if not value_text.isdigit() or unit not in {"s", "m", "h"}:
        raise ValueError("Use interval format like 5s, 5m, or 2h.")

    value = int(value_text)
    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    return value * 60 * 60


def schedule_organize(path, every):
    seconds = parse_interval(every)
    print(f"Running organize every {every}. Press Ctrl + C to stop.")
    try:
        while True:
            organize(path)
            time.sleep(seconds)
    except KeyboardInterrupt:
        print("\nSchedule stopped.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="fileorg",
        description="Organize, clean, archive, inspect, and back up files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    organize_parser = subparsers.add_parser("organize", help="Organize files by type.")
    organize_parser.add_argument("path")

    watch_parser = subparsers.add_parser("watch", help="Watch a folder and organize new files.")
    watch_parser.add_argument("path")
    watch_parser.add_argument("--interval", type=int, default=5)

    duplicates_parser = subparsers.add_parser("duplicates", help="Find duplicate files.")
    duplicates_parser.add_argument("path")

    cleanup_parser = subparsers.add_parser("cleanup", help="Move junk files to FileOrg trash.")
    cleanup_parser.add_argument("path", nargs="?", default=".")

    archive_parser = subparsers.add_parser("archive", help="Archive files older than N days.")
    archive_parser.add_argument("path")
    archive_parser.add_argument("--older-than", type=int, required=True)

    large_parser = subparsers.add_parser("large", help="Show largest files.")
    large_parser.add_argument("path", nargs="?", default=".")
    large_parser.add_argument("--top", type=int, default=10)

    backup_parser = subparsers.add_parser("backup", help="Back up a folder.")
    backup_parser.add_argument("source")
    backup_parser.add_argument("destination")

    schedule_parser = subparsers.add_parser("schedule", help="Schedule a command.")
    schedule_subparsers = schedule_parser.add_subparsers(dest="schedule_command", required=True)
    schedule_organize_parser = schedule_subparsers.add_parser("organize")
    schedule_organize_parser.add_argument("path")
    schedule_organize_parser.add_argument("--every", required=True)

    subparsers.add_parser("undo", help="Undo the last file-changing command.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "organize":
        organize(args.path)
    elif args.command == "watch":
        watch(args.path, args.interval)
    elif args.command == "duplicates":
        find_duplicates(args.path)
    elif args.command == "cleanup":
        cleanup(args.path)
    elif args.command == "archive":
        archive(args.path, args.older_than)
    elif args.command == "large":
        show_large_files(args.path, args.top)
    elif args.command == "backup":
        backup(args.source, args.destination)
    elif args.command == "schedule":
        if args.schedule_command == "organize":
            schedule_organize(args.path, args.every)
    elif args.command == "undo":
        undo()


if __name__ == "__main__":
    main()
