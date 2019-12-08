import os
from tkinter import *


class fileList:
    __root = Tk()
    __filename = StringVar()
    __list = []
    __thisControlFrame = Frame(__root)
    __textArea = Text(__root)
    __thisScrollBar = Scrollbar(__textArea)

    def __init__(self):
        self.__root.title("Files")
        self.__root.geometry("400x300")
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__textArea.grid(sticky=N + E + S + W, )
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__textArea.yview)
        self.__textArea.config(yscrollcommand=self.__thisScrollBar.set)
        self.__thisControlFrame.grid(sticky=N + E + S + W, row=1, column=0)

        fname = Entry(self.__thisControlFrame, textvariable=self.__filename)
        fname.pack(side=LEFT)
        click = Button(self.__thisControlFrame, text="list", command=self.searchfile)
        click.pack(side=LEFT)

    def run(self):
        self.__root.mainloop()

    def searchfile(self):
        self.__textArea.delete(0.0, END)
        try:
            self.__list = os.listdir(self.__filename.get())
            for i in self.__list:
                if os.path.isfile(self.__filename.get() + f"/{i}"):
                    self.__textArea.insert(END, f"{i}  (file)\n")
                else:
                    self.__textArea.insert(END, f"{i}  (folder)\n")
        except NotADirectoryError:
            self.__textArea.insert(END, "it is a file")
        except FileNotFoundError:
            self.__textArea.insert(END, "file not found")


list = fileList()
list.run()
