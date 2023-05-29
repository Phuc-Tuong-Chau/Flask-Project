from flask import Flask, render_template, jsonify, send_from_directory
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ntpath
import sched
import time

app = Flask(__name__.split('.')[0])

image_folder =  "C:\\Users\\11063\\OneDrive\\Desktop\\Flask\\pics"

# Handler for file system events
class ImageEventHandler(FileSystemEventHandler):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def on_created(self, event):
        if not event.is_directory:
            filename = ntpath.basename(event.src_path)
            image_urls.append(f"/pics/{filename}")
            if new_image_urls and new_image_urls[0] != f"/pics/{filename}":
                new_image_urls.clear()
            new_image_urls.append(f"/pics/{filename}")

    def schedule_task(self):
        self.scheduler.enter(5, 1, self.schedule_task)
        image_files = os.listdir(image_folder)
        image_urls.clear()
        image_urls.extend([f"/pics/{filename}" for filename in image_files])

# Initialize image URLs list
image_urls = []
# Initialize new image URLs list
new_image_urls = []
# Watchdog observer and event handler
event_handler = ImageEventHandler(sched.scheduler(time.time, time.sleep))
observer = Observer()
observer.schedule(event_handler, path=image_folder, recursive=False)
observer.start()

# Schedule periodic task to update image URLs every five seconds
event_handler.schedule_task()

@app.route("/")
def display_images():
    return render_template("index.html", image_urls=image_urls)

@app.route("/second")
def display_second_images():
    return render_template("secondinterface.html", image_urls=new_image_urls)

@app.route("/pics")
def get_image_urls():
    return jsonify(image_urls)

@app.route("/newpics")
def get_new_image_urls():
    return jsonify(new_image_urls)

@app.route("/pics/<path:filename>")
def serve_image(filename):
    return send_from_directory(image_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
