#!/usr/bin/python3

import AnimatedGif
import screeninfo
from tkinter import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.frame = Frame(self.root, width=501, height=496, borderwidth=0, relief=FLAT)
        self.frame.pack_propagate(False)
        self.frame.pack()

        self.label = Label(self.frame)
        self.label.place(x=-2, y=-2)

        self.bQuit = Button(self.frame, text="X", command=self.root.quit)
        self.bQuit.place(x=470, y=0)

        # (tkinter.parent, filename, delay between frames)
        self.lbl_with_my_gif = AnimatedGif.AnimatedGif(self.label, 'installer.gif', 0.06)
        self.lbl_with_my_gif.pack()  # Packing the label with the animated gif (grid works just as well)
        self.lbl_with_my_gif.start()  # Shows gif at first frame and we are ready to go

        self.progress_label = Label(self.frame, text="0%", bg="black", fg="#fff", font=("Tiki Island", 10))
        self.show_progress()

        m = screeninfo.get_monitors()

        x = (m[0].width / 2) - (501 / 2)
        y = (m[0].height / 2) - (496 / 2)

        self.root.geometry("+%d+%d" % (x, y))

    def show_progress(self):
        self.progress_label.place(x=445, y=460)

    def hide_progress(self):
        self.progress_label.place_forget()

    def set_progress(self, percent):
        self.progress_label['text'] = "%d%%" % percent

    def hello(self):
        self.lbl_with_my_gif.stop()  # Setting stop flag, which ends the update loop (animation)


app = App()
app.root.mainloop()
