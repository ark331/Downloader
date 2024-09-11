import customtkinter as ctk
from tkinter import StringVar, messagebox
import yt_dlp
import os
import shutil

# Initialize the app
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("360x540")
app.title("YouTube Video Downloader")

# Global variable for video path
video_path = None

# Function to handle placeholder
def add_placeholder(event):
    if entry_var.get() == "":
        entry_var.set("Search YouTube URL")
        search_entry.configure(fg_color="#E0E0E0", text_color="grey")

def remove_placeholder(event):
    if entry_var.get() == "Search YouTube URL":
        entry_var.set("")
        search_entry.configure(fg_color="white", text_color="black")

# Function to download video from YouTube
def download_video():
    global video_path
    url = entry_var.get()

    if url == "" or url == "Search YouTube URL":
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL.")
        return

    try:
        var = []
        

        ydl_opts = {
            'outtmpl': 'download.mp4',  # Set your desired filename here
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            video_path = f'download.mp4'  # Update video_path to the filename used

        # Start the download and update progress
        progress_label.configure(text="Downloading...")
        progress_bar.set(0.5)  # Indicate progress (50% here)
        progress_label.configure(text="Download Complete!")
        progress_bar.set(1)  # Set progress to 100%

        # Display the downloaded video
        open_video(video_path)

        messagebox.showinfo("Success", "Video downloaded successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video. Error: {e}")

def open_video(video_path):
    """ Opens the downloaded video using the default media player. """
    if os.name == 'nt':  # For Windows
        os.startfile(video_path)
    elif os.name == 'posix':  # For Unix-based systems (Linux, macOS)
        subprocess.call(['xdg-open', video_path])

# Create a label for instructions
description_label = ctk.CTkLabel(
    app, text="This tool accepts URLs from YouTube and downloads the video.\n"
              "Paste the URL below to get started.", 
    font=ctk.CTkFont(size=14), text_color="black", wraplength=300)
description_label.pack(pady=20)

# Input field for entering YouTube URL
entry_var = StringVar()
entry_var.set("Search YouTube URL")
search_entry = ctk.CTkEntry(app, width=280, height=40, textvariable=entry_var, corner_radius=10, font=("Arial", 14))
search_entry.configure(fg_color="#E0E0E0", text_color="grey")
search_entry.bind("<FocusIn>", remove_placeholder)
search_entry.bind("<FocusOut>", add_placeholder)
search_entry.pack(pady=15)

# Download button
download_button = ctk.CTkButton(app, text="DOWNLOAD VIDEO", width=240, height=50, corner_radius=25, 
                                font=("Arial", 16, "bold"), command=download_video)
download_button.pack(pady=30)

# Progress bar for download
progress_label = ctk.CTkLabel(app, text="Download Progress", font=ctk.CTkFont(size=12))
progress_label.pack(pady=5)

progress_bar = ctk.CTkProgressBar(app, width=280)
progress_bar.set(0)  # Initial value (0 to 1 range)
progress_bar.pack(pady=10)




# Run the app
app.mainloop()
