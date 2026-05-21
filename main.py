import json
import os
from datetime import datetime, timedelta

HABITS_FILE = "habits.json"

def load_habits():
    """Loads habits from the JSON file."""
    if os.path.exists(HABITS_FILE):
        try:
            with open(HABITS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {HABITS_FILE} is corrupted or empty. Starting with no habits.")
            return {}
    return {}

def save_habits(habits):
    """Saves habits to the JSON file."""
    with open(HABITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(habits, f, indent=4, ensure_ascii=False)

def add_habit(habits, name):
    """Adds a new habit if it doesn't exist."""
    if name not in habits:
        habits[name] = []
        print(f"Habit '{name}' added.")
        save_habits(habits)
    else:
        print(f"Habit '{name}' already exists.")

def mark_complete(habits, name):
    """Marks a habit as complete for today."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    if name in habits:
        if today_str not in habits[name]:
            habits[name].append(today_str)
            habits[name].sort() # Keep dates sorted for easier streak calculation
            print(f"Habit '{name}' marked complete for today ({today_str}).")
            save_habits(habits)
        else:
            print(f"Habit '{name}' was already marked complete for today.")
    else:
        print(f"Habit '{name}' not found.")

def get_streak(habit_dates):
    """Calculates the current consecutive streak for a habit.
    This is the core concept of providing motivational feedback beyond a simple checklist.
    A streak is defined as consecutive days ending with the most recent completion.
    If the habit was not completed yesterday or today, the streak is 0.
    """
    if not habit_dates:
        return 0

    # Convert date strings to datetime objects and sort them
    dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in habit_dates])

    current_streak = 0
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Find the most recent completion date that is today or in the past
    last_relevant_completion = None
    for d in reversed(dates):
        if d <= today:
            last_relevant_completion = d
            break

    if last_relevant_completion is None:
        return 0 # No relevant completions found up to today

    # If the last completion was more than one day ago from today, the streak is broken.
    # E.g., today is Oct 23, last completion was Oct 21. Streak is 0.
    if last_relevant_completion < today - timedelta(days=1):
        return 0

    # If we are here, last_relevant_completion is either today or yesterday.
    # Now, count backwards from last_relevant_completion to find the consecutive sequence.
    current_streak = 0
    expected_date = last_relevant_completion

    # Iterate through the sorted dates in reverse to count consecutive days
    for d in reversed(dates):
        if d == expected_date:
            current_streak += 1
            expected_date -= timedelta(days=1)
        elif d < expected_date:
            # If the current date `d` is before the `expected_date`, it means there's a gap.
            # The streak is broken at this point.
            break
        # If d > expected_date, it means d is a future date or a duplicate already handled.
        # This shouldn't happen with sorted unique dates and `expected_date` decreasing.

    return current_streak

def display_habits(habits):
    """Displays all habits, their history, and current streak."""
    if not habits:
        print("No habits added yet.")
        return

    print("\n--- Your Habits ---")
    for name, dates in habits.items():
        streak = get_streak(dates) # Calculate streak for motivational feedback
        print(f"\nHabit: {name}")
        print(f"  Completion History: {', '.join(dates) if dates else 'None'}")
        print(f"  Current Streak: {streak} days") # Displaying the streak
    print("-------------------\n")

def main():
    habits = load_habits()

    while True:
        print("\nHabit Tracker Menu:")
        print("1. Add new habit")
        print("2. Mark habit complete for today")
        print("3. View all habits")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter habit name: ")
            add_habit(habits, name)
        elif choice == '2':
            name = input("Enter habit name to mark complete: ")
            mark_complete(habits, name)
        elif choice == '3':
            display_habits(habits)
        elif choice == '4':
            print("Exiting Habit Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
