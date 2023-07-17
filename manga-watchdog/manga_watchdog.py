import time
import argparse
import subprocess
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser(description='File watcher to convert and add manga to calibre database')
parser.add_argument('--data-path', default=".", help='Path to watch for manga changes (recursively)')
parser.add_argument('--calibre-library-path', default="~/Documents/calibre/library", help='Path to calibre library to '
                                                                                          'sync on each manga add')

args = parser.parse_args()


class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()

        print(f"Watcher Running in directory: {self.directory}")
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("Watcher Terminated")


class MangaHandler(FileSystemEventHandler):
    def __init__(self, calibre_library_path="."):
        self.calibre_library_path = calibre_library_path

        self.ebook_convert_options = ["--output-profile", "tablet", "--no-default-epub-cover"]
        self.calibre_add_command = ["calibredb", "add", f"--library-path={self.calibre_library_path}"]

    def convert_file_to_epub(self, src_cbz_path: Path, dst_epub_path: Path):
        print(["ebook-convert", str(src_cbz_path), str(dst_epub_path)] + self.ebook_convert_options)
        try:
            subprocess.run(["ebook-convert", str(src_cbz_path), str(dst_epub_path)] + self.ebook_convert_options,
                           check=True)
        except:
            print("Error converting ebook to epub, returned with non-zero exit code.")

    def add_manga_to_calibre(self, src_epub_path: Path):
        try:
            subprocess.run(self.calibre_add_command + [str(src_epub_path)])
        except:
            print("Error adding file to calibre db, returned with non-zero exit code.")

    def on_created(self, event):
        if event.is_directory:
            return

        cbz_path = Path(event.src_path)
        epub_path = cbz_path.parent / (cbz_path.stem + ".epub")

        if cbz_path.suffix != ".cbz":
            return

        print(f"File {event.src_path} created!")
        print("Converting file to .epub...")
        self.convert_file_to_epub(cbz_path, epub_path)
        print("Successfully converted to .epub")

        print("Adding to calibre...")
        self.add_manga_to_calibre(epub_path)
        print(f"Successfully added manga {str(epub_path)} to calibre")

        # Remove files after insert in calibre db
        cbz_path.unlink()
        epub_path.unlink()


if __name__ == "__main__":
    manga_handler = MangaHandler(args.calibre_library_path)
    w = Watcher(args.data_path, manga_handler)

    w.run()
