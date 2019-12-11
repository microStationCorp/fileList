import os
from tkinter import *


class fileList:
    __root = Tk()
    __filename = StringVar()
    __list = []
    __thisControlFrame = Frame(__root, borderwidth=2, relief=SUNKEN, pady=5, bg="#AAA")
    __textArea = Text(__root, font="monaco", padx=5, pady=5, wrap=WORD)
    __thisScrollBar = Scrollbar(__textArea)

    def __init__(self):
        self.__root.title("Files")
        self.__root.geometry("400x300")
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__textArea.grid(sticky=N + E + S + W, padx=10)
        self.__filename.trace("w", self.searchfile)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__textArea.yview)
        self.__textArea.config(yscrollcommand=self.__thisScrollBar.set)
        self.__thisControlFrame.grid(sticky=N + E + S + W, row=1, column=0, padx=10, pady=10)
        self.__textArea.config(state="disabled")

        self.__thisControlFrame.grid_columnconfigure(0, weight=1)
        self.__thisControlFrame.grid_rowconfigure(0, weight=1)
        Label(self.__thisControlFrame, text="Direction", bg="#AAA", font="monaco 12 bold").grid(pady=5)
        fname = Entry(self.__thisControlFrame, textvariable=self.__filename, font='monaco')
        fname.grid(sticky=E + W + N + S, padx=30, row=1, column=0)
        fname.focus_set()

    def run(self):
        self.__root.mainloop()

    def searchfile(self, *args):
        self.__textArea.config(state='normal')
        self.__textArea.delete(0.0, END)
        try:
            self.__list = os.listdir(self.__filename.get())
            for i in self.__list:
                if os.path.isfile(self.__filename.get() + f"/{i}"):
                    self.__textArea.insert(END, f"{i}  (file)\n")
                else:
                    self.__textArea.insert(END, f"{i}  (folder)\n")
        except NotADirectoryError:
            self.__textArea.insert(END, f"{os.path.basename(self.__filename.get())} is a file")
        except FileNotFoundError:
            dirName = os.path.dirname(self.__filename.get())
            baseName = os.path.basename(self.__filename.get())
            try:
                listOfElement = os.listdir(dirName)
                flag = False
                for i in listOfElement:
                    if baseName == i[0:len(baseName)]:
                        # self.__textArea.insert(INSERT, f"{i}\n")
                        if os.path.isfile(dirName + f"/{i}"):
                            self.__textArea.insert(END, f"{i}  (file)\n")
                        else:
                            self.__textArea.insert(END, f"{i}  (folder)\n")
                        flag = True
                if flag == False:
                    self.__textArea.insert(END, 'File/Folder Not Found')
            except FileNotFoundError:
                if self.__filename.get() == "":
                    self.__textArea.insert(INSERT, "please insert file/folder direction")
                else:
                    self.__textArea.insert(END, "Invalid Address")
        self.__textArea.config(state="disabled")


list = fileList()
list.run()
