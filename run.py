import tkinter as tk
from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo
from send2trash import send2trash
import shutil
import cv2
import os

SAFE_MODE = True

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.APP_PATH = os.getcwd()
        #self.APP_PATH = ".\\tests"
        self.IMG_EXT = (".png", ".jpg", ".jpeg")
        self.VID_EXT = (".mp4", ".mov", ".gif", ".avi")

        self.media_index = 0

        self.rowconfigure((0), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        self.geometry("500x500")
        self.title("File Organizer")

    def search_folders(self):
        #self.root_folders = ["pasta1", "pasta2", "pasta3", "pasta4", "pasta5", "pasta6", "pasta 7"]
        self.root_folders = next(os.walk('.'))[1]

        if ".safe_backup" in self.root_folders:
            self.root_folders.remove(".safe_backup")

        index = 0

        for y in range(9):  # Number of rows
            for x in range(3):  # Number of columns
                if index < len(self.root_folders):
                    self.folder_btn = tk.Button(master=self, text=self.root_folders[index], 
                                                command=lambda dst=self.root_folders[index]: self.move_media(dst))
                    self.folder_btn.grid(row=y+3, column=x)
                    index+=1

    def search_media(self):
        self.root_files = os.listdir(self.APP_PATH)
        self.root_media = []
        for file in self.root_files:
            file = f"{self.APP_PATH}\\{file}"

            if file.endswith(self.IMG_EXT):
                self.root_media.append((file, "img"))
            elif file.endswith(self.VID_EXT):
                self.root_media.append((file, "vid"))

    def move_media(self, folder, delete=False):
        media_path = self.root_media[self.media_index][0]

        if delete==True:
            print(media_path)
            send2trash(media_path)
        
        else:
            if SAFE_MODE == True:
                if not os.path.exists(self.APP_PATH + "\\.safe_backup"):
                    os.mkdir(self.APP_PATH + "\\.safe_backup")

                shutil.copy(media_path, folder)
                shutil.move(media_path, self.APP_PATH + "\\.safe_backup")

            else:
                shutil.move(media_path, folder)
        
        self.root_media.remove(self.root_media[self.media_index])
        self.media_index -=1
        self.update()
        self.next_media()
    
    def resize_img(self):
        width = self.winfo_width()
        height = self.winfo_height()
        
        self.resized_img = self.org_image.resize((width, height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.resized_img)
        return self.image

    def extract_frame(self, media):
        cap = cv2.VideoCapture(media)
        ret, frame = cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

    def video_start(self):
        self.image_label.destroy()

        self.player.load(self.media_path)
        
        self.player.grid(row=0, column=0, columnspan=4, sticky="NSEW")

        self.player.play()
        self.player.bind('<<Ended>>', self.play_loop)

    def play_loop(self, e):
        self.player.play()

    def show_media(self, media):
        self.media_path = media[0]
        self.media_type = media[1]

        self.image_label.destroy()
        self.player.destroy()

        if self.media_type == "img":
            self.org_image = Image.open(self.media_path)
            span = 3

            self.play_button.grid_forget()
            self.del_btn.grid(row=1, column=1)
            self.next_btn.grid(row=1, column=2)

        elif self.media_type == "vid":
            self.vid_frame = self.extract_frame(self.media_path)
            self.org_image = Image.fromarray(self.vid_frame)

            span = 4

            self.player = TkinterVideo(master=self, scaled=True)
            self.play_button.grid(row=1, column=1)
            self.del_btn.grid(row=1, column=2)
            self.next_btn.grid(row=1, column=3)

        self.image = self.resize_img()

        self.image_label = tk.Label(master=self, image=self.image)
        self.image_label.grid(row=0, column=0, columnspan=span, sticky="NSEW")

    def next_media(self):
        self.media_index += 1
        if self.media_index > len(self.root_media)-1:
            self.media_index-=1
        self.show_media(self.root_media[self.media_index])

    def previous_media(self):
        self.media_index -= 1
        if self.media_index < 0:
            self.media_index+=1
        self.show_media(self.root_media[self.media_index])

    def buttons(self):
        self.image_label = tk.Label(master=self)
        self.player = TkinterVideo(master=self, scaled=True)

        self.previous_btn = tk.Button(master=self, text="<- previous", command=lambda: self.previous_media(), width=10)
        self.previous_btn.grid(row=1, column=0, padx=10, pady=10)

        self.play_button = tk.Button(master=self, text="play", command=lambda: self.video_start(), width=10)

        self.del_btn = tk.Button(master=self, text="delete", bg="red", fg="white", command= lambda: self.move_media("trash", delete=True),
                                 width=10)

        self.next_btn = tk.Button(text="next ->", command=lambda: self.next_media(), width=10)

main = MainWindow()
main.search_media()
main.buttons()
main.update()
main.show_media(main.root_media[0])
main.search_folders()
main.mainloop()