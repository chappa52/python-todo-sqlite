import sqlite3


def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor


def show_tasks(cursor):
    cursor.execute("SELECT id, title, status FROM tasks")
    tasks = cursor.fetchall()

    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n=== TASKS ===")
    for task in tasks:
        print(f"{task[0]}. {task[1]} [{task[2]}]")


def add_task(conn, cursor):
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    cursor.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        (title, "Not Done")
    )
    conn.commit()
    print("Task added successfully.")


def mark_task_done(conn, cursor):
    show_tasks(cursor)
    task_id = input("Enter task ID to mark as done: ").strip()

    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("Task not found.")
        return

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        ("Done", task_id)
    )
    conn.commit()
    print("Task marked as done.")


def delete_task(conn, cursor):
    show_tasks(cursor)
    task_id = input("Enter task ID to delete: ").strip()

    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("Task not found.")
        return

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print("Task deleted successfully.")


def main():
    conn, cursor = connect_db()

    while True:
        print("\n=== TO-DO MANAGER WITH SQLITE ===")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            show_tasks(cursor)
        elif choice == "2":
            add_task(conn, cursor)
        elif choice == "3":
            mark_task_done(conn, cursor)
        elif choice == "4":
            delete_task(conn, cursor)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")

    conn.close()


if __name__ == "__main__":
    main()
