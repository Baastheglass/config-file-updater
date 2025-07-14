import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
import json

def add_repository(json_file_path, repo_key, repo_data):
    """
    Add a repository entry under "repositories" section.
    
    Parameters:
    - json_file_path (str): path to the JSON file
    - repo_key (str): unique key name (e.g. "repo2")
    - repo_data (dict): repository object matching the structure in existing JSON
    """
    # 1. Load existing file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    # Ensure "repositories" exists
    repos = data.setdefault('repositories', {})
    
    # Check duplicate key
    if repo_key in repos:
        raise ValueError(f"Repository key '{repo_key}' already exists.")
    
    # Add the new repo
    repos[repo_key] = repo_data
    
    # Write back prettily
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        folder_name = Path(event.src_path).name
        if(".pid" not in folder_name and ".swp" not in folder_name and ".git" not in folder_name):
            print("Created:", folder_name)
            os.chdir('/root/CI_Server')
            print(os.getcwd())
            with open("config.json", "r") as file:
                data = file.read()
                new_repo = {
                            "name": folder_name,
                            "description": "Some description",
                            "path": "/root",
                            "branches": {
                                "1": {
                                    "name": "main",
                                    "events": ["push"],
                                    "actions": {
                                        "action1": {
                                            "name": "Deploy",
                                            "description": "Pull and deploy",
                                            "commands": ["git pull"]
                                        }
                                    }
                                }
                            }
                        }
                add_repository("config.json", folder_name, new_repo)
                print("Repository added:", folder_name)
    def on_modified(self, event):
        pass
        #print(f"Modified: {event.src_path}")
    def on_deleted(self, event):
        pass
        #print(f"Deleted: {event.src_path}")
    def on_moved(self, event):
        pass
        #print(f"Moved: {event.src_path} -> {event.dest_path}")


if __name__ == "__main__":
    server_path = "/root"
    print(os.getcwd())
    path = "C:\\Users\\Well\\Desktop\\VSCODE\\config-file-updater"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, server_path, recursive=True)
    observer.start()
    print(f"Watching: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
