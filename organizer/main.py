"""Daily Brain: a simple CLI that sorts your tasks into categories
and saves them to a JSON file."""

import json
from categories import categorize

OUTPUT_FILE = "tasks.json"


def collect_tasks():
    """Prompt the user for tasks until they type 'done'."""
    tasks = []
    print("Enter your tasks one at a time. Type 'done' when you're finished.\n")
    while True:
        entry = input("Enter a task (or 'done' to finish): ").strip()
        if entry.lower() == "done":
            break
        if entry:
            tasks.append(entry)
    return tasks


def sort_tasks(tasks):
    """Group a list of tasks by category."""
    sorted_tasks = {}
    for task in tasks:
        category = categorize(task)
        sorted_tasks.setdefault(category, []).append(task)
    return sorted_tasks


def display_tasks(sorted_tasks):
    """Print tasks grouped by category."""
    print()
    for category, tasks in sorted_tasks.items():
        print(category)
        for task in tasks:
            print(f"  - {task}")
        print()


def save_tasks(sorted_tasks):
    """Save categorized tasks to a JSON file."""
    with open(OUTPUT_FILE, "w") as f:
        json.dump(sorted_tasks, f, indent=2)


def main():
    tasks = collect_tasks()
    if not tasks:
        print("No tasks entered. Nothing to save.")
        return

    sorted_tasks = sort_tasks(tasks)
    display_tasks(sorted_tasks)

    save_tasks(sorted_tasks)
    total = sum(len(v) for v in sorted_tasks.values())
    print(f"Saved {total} tasks to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
