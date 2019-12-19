import os
import re
from tkinter import *


class fileList:
    __root = Tk()
    __filename = StringVar()
    __thisControlFrame = Frame(__root, borderwidth=2, relief=SUNKEN, pady=5, bg="#AAA")
    __listArea = Listbox(__root)
    __thisScrollBarSide = Scrollbar(__listArea)
    __thisScrollBarBottom = Scrollbar(__listArea)

    def __init__(self):
        self.__root.title("FileList")
        self.__root.geometry("500x500")
        self.__root.minsize(500, 500)
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__listArea.grid(sticky=N + E + S + W, padx=10)
        self.__listArea.insert(0, ' please type something')
        self.__filename.trace("w", self.searchfile)
        self.__thisScrollBarSide.pack(side=RIGHT, fill=Y)
        self.__thisScrollBarSide.config(command=self.__listArea.yview)
        self.__listArea.config(yscrollcommand=self.__thisScrollBarSide.set)
        self.__thisScrollBarBottom.pack(side=BOTTOM, fill=X)
        self.__thisScrollBarBottom.config(command=self.__listArea.xview, orient=HORIZONTAL)
        self.__listArea.config(xscrollcommand=self.__thisScrollBarBottom.set)
        self.__thisControlFrame.grid(sticky=N + E + S + W, row=1, column=0, padx=10, pady=10)
        self.__listArea.config(font='monaco 11')

        self.__thisControlFrame.grid_columnconfigure(0, weight=1)
        self.__thisControlFrame.grid_rowconfigure(0, weight=1)
        Label(self.__thisControlFrame, text="Direction", bg="#AAA", font="monaco 12 bold").grid(pady=5)
        self.__fname = Entry(self.__thisControlFrame, textvariable=self.__filename, font='monaco')
        self.__fname.grid(sticky=E + W + N + S, padx=30, row=1, column=0)
        self.__fname.focus_set()
        self.__buttonFrame = Frame(self.__thisControlFrame, borderwidth=2, relief=SUNKEN)
        self.__buttonFrame.grid(row=2, column=0)
        self.__buttonSelect = Button(self.__buttonFrame, text='Select', font='monaco 11', command=self.selectPath)
        self.__buttonSelect.pack(side=LEFT)

    def selectPath(self):
        s = self.__listArea.get(ACTIVE)
        if s.endswith('(file') or s.endswith('(folder)'):
            s = re.sub('^ ', '', s)
            if s.endswith('(file)'):
                s = re.sub(' {2}\(file\)$', '', s)
            elif s.endswith('(folder)'):
                s = re.sub(' {2}\(folder\)$', '', s)
            val = ''
            for i in range(len(s) - len(self.__baseName)):
                val = val + s[i + len(self.__baseName)]
            self.__fname.insert(END, f'{val}/')
            self.__fname.focus_set()

    def run(self):
        self.__root.mainloop()

    def searchfile(self, *args):
        self.__listArea.delete(0, END)
        self.__dirName = os.path.dirname(self.__filename.get())
        self.__baseName = os.path.basename(self.__filename.get())

        if '' == self.__filename.get():
            self.__root.title("FileList")
            self.__listArea.insert(0, ' please type something')
        elif '/' == self.__filename.get()[len(self.__filename.get()) - 1]:
            if 0 == self.directionCheck(self.__filename.get()):
                self.__root.title(f'{self.__dirName} - FileList')
                self.insertFileListInTextArea(self.__filename.get())
            elif 1 == self.directionCheck(self.__filename.get()):
                self.__listArea.insert(0, ' not a directory')
            elif 2 == self.directionCheck(self.__filename.get()):
                self.__listArea.insert(0, ' file/folder not found')
        else:
            self.__root.title(f'{self.__dirName} - FileList')
            try:
                listOfElement = os.listdir(self.__dirName)
                flag = False
                for i in listOfElement:
                    if i[0:len(self.__baseName)] == self.__baseName:
                        if os.path.isfile(self.__dirName + f"/{i}"):
                            self.__listArea.insert(END, f" {i}  (file)")
                        else:
                            self.__listArea.insert(END, f" {i}  (folder)")
                        flag = True
                if not flag:
                    self.__listArea.insert(0, ' File/Folder Not Found')
            except FileNotFoundError:
                self.__listArea.insert(0, " Invalid Address")

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
                self.__listArea.insert(END, f" {i}  (file)")
            else:
                self.__listArea.insert(END, f" {i}  (folder)")


List = fileList()
List.run()
