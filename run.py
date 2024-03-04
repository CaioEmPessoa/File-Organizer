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

    def search_media(self):
        self.root_files = os.listdir(self.APP_PATH)
        self.root_media = []
        for file in self.root_files:
            file = f"{self.APP_PATH}/{file}"

            if file.endswith(self.IMG_EXT):
                self.root_media.append((file, "img"))
            elif file.endswith(self.VID_EXT):
                self.root_media.append((file, "vid"))
    
    def resize_img(self):
        width = self.winfo_width()
        height = self.winfo_height()
        
        resized_img = self.org_image.resize((width, height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_img)
        self.image_label.config(image=self.image)

        self.after(20, self.resize_img)


    def show_media(self, media):
        media_path = media[0]
        media_type = media[1]

        if media_type == "img":

            self.org_image = Image.open(media_path)
            self.image = ImageTk.PhotoImage(self.org_image)
            self.image_label = tk.Label(master=self, image=self.image)
            self.image_label.grid(row=0, column=0, columnspan=3, sticky="NSEW")
            
            self.after(20, self.resize_img)

        
    def next_media(self):
        self.media_index += 1
        self.show_media(self.root_media[self.media_index])

    def previous_media(self):
        self.media_index -= 1
        self.show_media(self.root_media[self.media_index])

    def buttons(self):
        self.previous_btn = tk.Button(master=self, text="<- previous", command=lambda: self.previous_media(),
                                 width=10)
        self.previous_btn.grid(row=1, column=0, padx=10, pady=10)

        self.del_btn = tk.Button(master=self, text="delete", 
                            bg="red", fg="white", width=10)
        self.del_btn.grid(row=1, column=1)

        self.next_btn = tk.Button(text="next ->", command=lambda: self.next_media(), 
                             width=10)
        self.next_btn.grid(row=1, column=2)

main = MainWindow()
main.buttons()
main.search_media()
main.show_media(main.root_media[0])
main.mainloop()