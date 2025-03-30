# Grayfia Class
from Grayfia import Grayfia

if __name__ == "__main__":
    grayfia = Grayfia()
    # If grayfia class is initialised by credentials.json
    if grayfia.creds:
        # Fetch events and tasks
        events = grayfia.get_events()
        tasks = grayfia.get_tasks()

        # Iterate through each task in all tasks
        for task in tasks:
            print("---Tasks---")
            tasklist  =  task.get('task_list_title')
            task_name = task.get('title')
            # Print the corresponding tasklist and task
            print(f"Tasklist: {tasklist}\n Task Name: {task_name}")

    # No credentials.json file, read the error printed on terminal
    else:
        print("Authentication Failed")