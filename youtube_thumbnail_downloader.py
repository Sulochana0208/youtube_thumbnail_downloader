import tkinter as tk
from tkinter import filedialog
import pytube
import requests
from PIL import Image
from io import BytesIO


def get_thumbnail_url(video_url):
    try:
        video = pytube.YouTube(video_url)
        thumbnail_url = video.thumbnail_url
        return thumbnail_url
    except pytube.exceptions.PytubeError as e:
        raise Exception(f"Error fetching video info: {str(e)}")


def download_thumbnail():
    video_url = video_url_entry.get()
    if not video_url:
        status_label.config(text="Please enter a valid YouTube URL.", fg="red")
        return

    try:
        thumbnail_url = get_thumbnail_url(video_url)

        resolution = resolution_var.get()
        thumbnail_url = thumbnail_url.replace(
            "/hqdefault",
            f"/maxresdefault"
            if resolution == "High"
            else f"/{resolution.lower()}default",
        )

        response = requests.get(thumbnail_url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")]
        )

        if file_path:
            image.save(file_path)
            status_label.config(text="Thumbnail downloaded successfully.", fg="green")
        else:
            status_label.config(text="Download canceled.", fg="red")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")


# Create the main application window
app = tk.Tk()
app.title("YouTube Thumbnail Downloader")

# Create the Video URL entry and download button
video_url_label = tk.Label(app, text="YouTube Video URL:")
video_url_label.pack(pady=5)
video_url_entry = tk.Entry(app, width=50)
video_url_entry.pack(pady=5)

resolution_label = tk.Label(app, text="Select Resolution:")
resolution_label.pack(pady=5)

resolution_var = tk.StringVar(value="High")
resolution_high = tk.Radiobutton(
    app, text="High (maxresdefault)", variable=resolution_var, value="High"
)
resolution_high.pack(anchor="w")
resolution_medium = tk.Radiobutton(
    app, text="Medium (sddefault)", variable=resolution_var, value="Medium"
)
resolution_medium.pack(anchor="w")
resolution_low = tk.Radiobutton(
    app, text="Low (hqdefault)", variable=resolution_var, value="Low"
)
resolution_low.pack(anchor="w")

download_button = tk.Button(app, text="Download Thumbnail", command=download_thumbnail)
download_button.pack(pady=10)

# Create a label to display status messages
status_label = tk.Label(app, text="", fg="black")
status_label.pack(pady=5)

# Start the main event loop
app.mainloop()
