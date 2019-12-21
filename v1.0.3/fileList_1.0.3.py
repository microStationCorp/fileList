import os
import subprocess
from tkinter import *
from tkinter.messagebox import *


class fileList:
    __root = Tk()
    __filename = StringVar()
    __thisControlFrame = Frame(__root, borderwidth=2, relief=SUNKEN, pady=5, bg="#AAA")
    __listArea = Listbox(__root)
    __thisScrollBarSide = Scrollbar(__listArea)
    __thisScrollBarBottom = Scrollbar(__listArea)
    __dirName = ''
    __baseName = ''

    def __init__(self):
        self.__root.title("FileList")
        self.__root.geometry("550x550")
        self.__root.minsize(500, 500)
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__filename.trace('w', self.searchFile)
        self.__listArea.grid(sticky=N + E + S + W, padx=10)
        self.__listArea.insert(0, ' please type something')
        self.__thisScrollBarSide.pack(side=RIGHT, fill=Y)
        self.__thisScrollBarSide.config(command=self.__listArea.yview)
        self.__listArea.config(yscrollcommand=self.__thisScrollBarSide.set)
        self.__thisScrollBarBottom.pack(side=BOTTOM, fill=X)
        self.__thisScrollBarBottom.config(command=self.__listArea.xview, orient=HORIZONTAL)
        self.__listArea.config(xscrollcommand=self.__thisScrollBarBottom.set)
        self.__thisControlFrame.grid(sticky=N + E + S + W, row=1, column=0, padx=10, pady=10)
        self.__listArea.config(font='monaco 11')
        self.__listArea.bind('<Return>', self.openRunFile)
        self.__listArea.bind('<Double-Button-1>', self.openRunFile)

        self.__thisControlFrame.grid_columnconfigure(0, weight=1)
        self.__thisControlFrame.grid_rowconfigure(0, weight=1)
        Label(self.__thisControlFrame, text="Direction", bg="#AAA", font="monaco 12 bold").grid(pady=5)
        self.__fname = Entry(self.__thisControlFrame, textvariable=self.__filename, font='monaco')
        self.__fname.grid(sticky=E + W + N + S, padx=30, row=1, column=0)
        self.__fname.focus_set()

    def run(self):
        self.__root.mainloop()

    def searchFile(self, *args):
        if self.__filename.get().endswith('/') and os.path.isfile(os.path.abspath(self.__filename.get())):
            showinfo('info', 'it is a file')
            self.__fname.delete(len(self.__filename.get()) - 1)
            self.printList()
        elif self.__filename.get().endswith('/') and os.path.exists(self.__filename.get()):
            self.printList()
            if self.__listArea.size() == 0:
                showinfo('info', 'empty')
                self.__fname.delete(len(self.__filename.get()) - 1)
                self.printList()
        elif not self.__filename.get().endswith('/') and os.path.exists(os.path.dirname(self.__filename.get())):
            self.printList()
            if self.__listArea.size() == 0:
                showinfo('info', 'not found')
                self.__fname.delete(len(self.__filename.get()) - 1)
                self.printList()
        elif self.__filename.get().endswith('/') and not os.path.exists(os.path.dirname(self.__filename.get())):
            showinfo('info', 'invalid')
            self.__fname.delete(len(self.__filename.get()) - 1)
            self.printList()
        elif self.__filename.get() == '':
            self.__listArea.delete(0, END)
            self.__root.title("FileList")

    def printList(self):
        self.__dirName, self.__baseName = os.path.split(self.__filename.get())
        __list = os.listdir(self.__dirName)
        self.__listArea.delete(0, END)
        self.__root.title(f"{self.__dirName} - FileList")
        for i in __list:
            if i.startswith(self.__baseName) and os.path.isfile(os.path.join(self.__dirName, i)):
                self.__listArea.insert(END, f'{i}  - (file)')
            elif i.startswith(self.__baseName):
                self.__listArea.insert(END, f'{i}  - (folder)')

    def openRunFile(self, *args):
        fileName = self.__listArea.get(ACTIVE)
        if fileName.endswith('(file)'):
            fileName = fileName[:-10]
            if os.name == 'posix':
                subprocess.call(("xdg-open", os.path.join(os.path.dirname(self.__filename.get()), fileName)))
            elif os.name == 'nt':
                os.startfile(fileName)
        elif fileName.endswith('(folder)'):
            fileName = fileName[:-12]
            _baseName = os.path.basename(self.__filename.get())
            for i in range(len(fileName) - len(_baseName)):
                self.__fname.insert(END, fileName[len(_baseName) + i])
            self.__fname.insert(END, '/')
        self.__fname.focus_set()


List = fileList()
List.run()
