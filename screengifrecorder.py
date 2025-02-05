#!/usr/bin/env python3
import tkinter as tk
from PIL import Image, ImageGrab  # pip install pillow
import time
import signal
import argparse
import sys

class ScreenGifRecorder:
    def __init__(self, quality=256, output_file="output.gif", delay=0.1):
        """
        Initialize the screen gif recorder lol
        """
        self.quality = quality          # number of colors for the GIF (2 to 256)
        self.output_file = output_file  # output GIF file name
        self.delay = delay              # delay between screenshots (in seconds)
        self.frames = []                # list to store captured frames
        self.region = None
        self.recording = False

        # variables used during area selection
        self.start_x = self.start_y = 0
        self.rect = None
        self.canvas = None

    def select_area(self):
        """
        Open a transparent fullscreen window for area selection.
        The user can drag to select a region - upon release the region is saved.
        """
        root = tk.Tk()
        root.title("Area Selection: Drag with the mouse and release")
        root.attributes("-fullscreen", True)
        root.attributes("-alpha", 0.3)

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.on_button_release(event, root))

        root.mainloop()

        if self.region is None:
            print("No area selected. Exiting.")
            sys.exit(1)
        print("Selected area:", self.region)

    def on_button_press(self, event):
        """
        Record the starting point of the selection and create a rectangle object
        """
        self.start_x = event.x
        self.start_y = event.y
        # Create a rectangle with zero size initially
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2
        )

    def on_move_press(self, event):
        """
        Update the rectangle as the mouse is dragged
        """
        curX, curY = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event, root):
        """
        When the mouse button is released, compute the selected region and close the window
        """
        end_x, end_y = event.x, event.y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        self.region = (x1, y1, x2, y2)
        root.destroy()

    def record(self):
        """
        Record screenshots of the selected area until CTRL + C is pressed
        """
        print("Recording started...")
        print("Press CTRL+C in the terminal to stop recording.")
        self.recording = True

        # register signal handler to stop recording on CTRL + C detection
        signal.signal(signal.SIGINT, lambda sig, frame: self._stop_recording())

        while self.recording:
            try:
                # capture a screenshot of the defined region (bbox expects (x1, y1, x2, y2))
                img = ImageGrab.grab(bbox=self.region)
                self.frames.append(img)
                time.sleep(self.delay)
            except Exception as e:
                print("Error during recording:", e)
                sys.exit(1)

        print("\nRecording stopped, creating GIF...")

    def _stop_recording(self):
        """
        Internal method to stop recording. Called by the signal handler
        """
        self.recording = False

    def save_gif(self):
        """
        Convert the recorded frames to palette mode and save them as an animated GIF
        """
        if self.frames:
            duration = int(self.delay * 1000)  # duration per frame in milliseconds
          
            # convert all frames to palette mode using the specified number of colors (quality)
            converted_frames = [
                frame.convert("P", palette=Image.ADAPTIVE, colors=self.quality)
                for frame in self.frames
            ]
            try:
                converted_frames[0].save(
                    self.output_file,
                    save_all=True,
                    append_images=converted_frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=True
                )
                print("GIF saved as:", self.output_file)
            except Exception as e:
                print("Error saving the GIF:", e)
        else:
            print("No frames were recorded!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ScreenGifRecorder: Record a selected area of your screen and save as an animated GIF."
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=256,
        help="Number of colors in GIF (between 2 and 256). Default is 256."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.gif",
        help="Output file name for the GIF. Default is 'output.gif'."
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=0.1,
        help="Delay between frames in seconds. Default is 0.1."
    )
    args = parser.parse_args()

    quality = args.quality
    if quality < 2 or quality > 256:
        print("Quality parameter must be between 2 and 256. Using default value 256.")
        quality = 256

    recorder = ScreenGifRecorder(quality=quality, output_file=args.output, delay=args.delay)
    recorder.select_area() # select area
    recorder.record() # record the selected area until CTRL+C is pressed
    recorder.save_gif() # save the captured frames as an animated GIF
