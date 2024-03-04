import tkinter as tk
from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo
import os

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.APP_PATH = os.getcwd()
        self.APP_PATH = "./tests"
        self.IMG_EXT = (".png", ".jpg", ".jpeg")
        self.VID_EXT = (".mp4", ".mov", ".gif", ".avi")

        self.media_index = 0

        self.rowconfigure((0), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        self.geometry("500x500")

    def buttons(self):
        
        previous_btn = tk.Button(master=self, text="<- previous",
                                 width=10)
        previous_btn.grid(row=1, column=0, padx=10, pady=10)

        del_btn = tk.Button(master=self, text="delete", 
                            bg="red", fg="white", width=10)
        del_btn.grid(row=1, column=1)

        next_btn = tk.Button(text="next ->",
                             width=10)
        next_btn.grid(row=1, column=2)

main = MainWindow()
main.buttons()
main.mainloop()