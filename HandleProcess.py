from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image


class HP:
    def __init__(self):
        self.name=''
        self.ps='***'


    @staticmethod
    def get_img(filename, width, height):
        im = Image.open(filename).resize((width, height))
        im = ImageTk.PhotoImage(im)
        return im


class ToggledFrame(Frame):

    def __init__(self, parent, text="", *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.show = IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')
