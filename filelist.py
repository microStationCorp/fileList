import os
from tkinter import *


class fileList:
    __root = Tk()
    __filename = StringVar()
    __list = []
    __textArea = Text(__root)

    def __init__(self):
        self.__root.title("Files")
        self.__root.geometry("400x300")

        fname = Entry(self.__root, textvariable=self.__filename)
        fname.pack()
        click = Button(self.__root, text="list", command=self.searchfile)
        click.pack()

        self.__textArea.pack()

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
