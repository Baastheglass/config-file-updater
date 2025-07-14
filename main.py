import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Created: {event.src_path}")
        folder_name = Path(event.src_path).name
        print("Using pathlib:", folder_name)
        if(".pid" not in folder_name):
            print("Created:", folder_name)
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
    path = "C:\\Users\\Well\\Desktop\\VSCODE\\config-file-updater"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
