# Usage: python watchDownloads.py src target
# src - Absolute Path to folder to watch incoming files(Downloads folder typically)
# target - Absolute path to root directory of file extension subdirectories
import os
import subprocess
import time
import sys
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class Move_Downloads(PatternMatchingEventHandler):
    def on_modified(self, event):
        file_size = -1
        try:
            while file_size != os.path.getsize(event.src_path):
                file_size = os.path.getsize(event.src_path)
                time.sleep(1)
        except FileNotFoundError:
            return

        if not event.is_directory:
            filePath = event.src_path
            fileExtension = filePath[filePath.index('.') + 1:]
            if fileExtension != 'tmp' and fileExtension != 'crdownload':  # ignore tmp and crdownload
                print(f"File{event.src_path} Modified")
                filePath = event.src_path
                fileExtension = filePath[filePath.index('.') + 1:]
                filename = filePath[filePath.rfind('\\') + 1:]
                try:
                    os.makedirs(
                        f'{sys.argv[2]}\{fileExtension}', exist_ok=True)
                    os.rename(event.src_path,
                              f"{sys.argv[2]}\{fileExtension}\{filename}")
                    subprocess.Popen(
                        f'explorer {sys.argv[2]}\{fileExtension}')
                except FileExistsError:
                    pass
                except FileNotFoundError:
                    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        assert("MUST HAVE 3 ARGUMENTS")
    downloads_path = sys.argv[1]
    result_path = sys.argv[2]

    event_handler = Move_Downloads()

    observer = Observer()

    observer.schedule(event_handler, downloads_path, recursive=True)

    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
