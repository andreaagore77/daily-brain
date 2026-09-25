"""Keyword rules used to sort tasks into categories."""

CATEGORIES = {
    "School": ["exam", "homework", "study", "class", "lecture", "assignment", "quiz", "professor"],
    "Business": ["invoice", "client", "order", "product", "grant", "funding", "sponsor"],
    "Work": ["meeting", "shift", "report", "email", "deadline", "project", "call"],
}


def categorize(task):
    """Return the category a task belongs to, based on keyword matches.

    Checks the task text (case-insensitive) against each category's
    keyword list, in the order CATEGORIES is defined. The first match
    wins. If nothing matches, the task is filed under 'Personal'.
    """
    task_lower = task.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in task_lower for keyword in keywords):
            return category
    return "Personal"
