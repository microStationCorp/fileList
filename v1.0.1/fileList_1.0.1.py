import os
from tkinter import *


class fileList:
    __root = Tk()
    __filename = StringVar()
    __thisControlFrame = Frame(__root, borderwidth=2, relief=SUNKEN, pady=5, bg="#AAA")
    __textArea = Text(__root, font="monaco", padx=5, pady=5, wrap=WORD)
    __thisScrollBar = Scrollbar(__textArea)

    def __init__(self):
        self.__root.title("FileList")
        self.__root.geometry("400x300")
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__textArea.grid(sticky=N + E + S + W, padx=10)
        self.__textArea.insert(INSERT, 'please type something')
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
        dirName = os.path.dirname(self.__filename.get())
        baseName = os.path.basename(self.__filename.get())

        if '' == self.__filename.get():
            self.__root.title("FileList")
            self.__textArea.insert(INSERT, 'please type something')
        elif '/' == self.__filename.get()[len(self.__filename.get()) - 1]:
            if 0 == self.directionCheck(self.__filename.get()):
                self.__root.title(f'{dirName} - FileList')
                self.insertFileListInTextArea(self.__filename.get())
            elif 1 == self.directionCheck(self.__filename.get()):
                self.__textArea.insert(INSERT, f'{dirName} :\nnot a directory')
            elif 2 == self.directionCheck(self.__filename.get()):
                self.__textArea.insert(INSERT, f'{dirName} :\nfile/folder not found')
        else:
            self.__root.title(f'{dirName} - FileList')
            try:
                listOfElement = os.listdir(dirName)
                flag = False
                for i in listOfElement:
                    if i[0:len(baseName)] == baseName:
                        if os.path.isfile(dirName + f"/{i}"):
                            self.__textArea.insert(END, f"{i}  (file)\n")
                        else:
                            self.__textArea.insert(END, f"{i}  (folder)\n")
                        flag = True
                if flag == False:
                    self.__textArea.insert(END, 'File/Folder Not Found')
            except FileNotFoundError:
                self.__textArea.insert(END, "Invalid Address")

        self.__textArea.config(state="disabled")

    @staticmethod
    def directionCheck(filename):
        try:
            os.listdir(filename)
            return 0
        except NotADirectoryError:
            return 1
        except FileNotFoundError:
            return 2

    def insertFileListInTextArea(self, filename):
        __list = os.listdir(filename)
        for i in __list:
            if os.path.isfile(filename + f"/{i}"):
                self.__textArea.insert(END, f"{i}  (file)\n")
            else:
                self.__textArea.insert(END, f"{i}  (folder)\n")


List = fileList()
List.run()
