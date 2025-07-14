import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        folder_name = Path(event.src_path).name
        if(".pid" not in folder_name):
            print("Created:", folder_name)
            os.chdir('/root/CI_Server')
            print(os.getcwd())
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
