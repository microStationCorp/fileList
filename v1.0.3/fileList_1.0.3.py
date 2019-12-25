import os
import subprocess
import sys
from tkinter import *
from tkinter.messagebox import *
import re
import shutil


def validateName(name, ftype):
    fileReg = re.compile('[~`$%^&*{}:;"\',<.>?/\[\]]')
    folderReg = re.compile('[~`$%^&*{}:;"\',<>?/\[\]]')
    if ftype == 'file' and fileReg.search(name) is None:
        return True
    elif ftype == 'folder' and folderReg.search(name) is None:
        return True
    else:
        return False


class fileList:
    __root = Tk()
    __filename = StringVar()
    __thisControlFrame = Frame(__root, borderwidth=2, relief=SUNKEN, pady=5, bg="#AAA")
    __listArea = Listbox(__root, selectmode=EXTENDED)
    __thisScrollBarSide = Scrollbar(__listArea)
    __thisScrollBarBottom = Scrollbar(__listArea)
    __dirName = ''
    __baseName = ''
    __topEntry = StringVar()

    def __init__(self):
        self.__root.title("FileList")
        x, y = self.sizeOfWindow(500, 500)
        self.__root.geometry(f"500x500+{x}+{y}")
        self.__root.minsize(500, 500)
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__root.bind('<Control-n>', self.newFile)
        self.__root.bind('<Control-Shift-N>', self.newDir)
        self.__root.bind('<Control-h>', self.shortcutDialog)
        self.__root.bind('<Control-d>', self.deleteContentSelected)
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
        Label(self.__thisControlFrame, text="Enter path Address :", bg="#AAA", font="monaco 12 bold").grid(pady=5)
        self.__fname = Entry(self.__thisControlFrame, textvariable=self.__filename, font='monaco')
        self.__fname.grid(sticky=E + W + N + S, padx=30, row=1, column=0)
        self.__fname.focus_set()

    def run(self):
        self.__root.mainloop()

    def searchFile(self, *args):
        if self.__filename.get().endswith(os.sep) and os.path.isfile(os.path.abspath(self.__filename.get())):
            showinfo('info', 'it is a file')
            self.__fname.delete(len(self.__filename.get()) - 1)
            self.printList()
        elif self.__filename.get().endswith(os.sep) and os.path.exists(self.__filename.get()):
            self.printList()
        elif not self.__filename.get().endswith(os.sep) and os.path.exists(os.path.dirname(self.__filename.get())):
            self.printList()
            if self.__listArea.size() == 0:
                showinfo('info', 'not found')
                self.__fname.delete(len(self.__filename.get()) - 1)
                self.printList()
        elif self.__filename.get().endswith(os.sep) and not os.path.exists(os.path.dirname(self.__filename.get())):
            showinfo('info', 'invalid')
            self.__fname.delete(len(self.__filename.get()) - 1)
            self.printList()
        elif self.__filename.get() == '':
            self.__listArea.delete(0, END)
            self.__root.title("FileList")

    def printList(self):
        self.__dirName, self.__baseName = os.path.split(self.__filename.get())
        try:
            __list = os.listdir(self.__dirName)
        except:
            return
        self.__listArea.delete(0, END)
        self.__root.title(f"{self.__dirName} - FileList")
        __list.sort()
        self.__listArea.insert(END, f'{os.pardir}Parent Folder')
        for i in __list:
            if i.startswith(self.__baseName) and os.path.isfile(os.path.join(self.__dirName, i)):
                self.__listArea.insert(END, f'{i}  - (file)')
            elif i.startswith(self.__baseName):
                self.__listArea.insert(END, f'{i}  - (folder)')

    def openRunFile(self, *args):
        fileName = self.__listArea.get(ACTIVE)
        if fileName.startswith(os.pardir):
            newAddress = os.path.dirname(os.path.dirname(self.__filename.get()))
            for i in range(len(self.__filename.get()) - len(newAddress)):
                self.__fname.delete(len(self.__filename.get()) - 1)
            if newAddress != os.sep:
                self.__fname.insert(END, os.sep)
        elif fileName.endswith('(file)'):
            fileName = fileName[:-10]
            if os.name == 'posix':
                subprocess.call(("xdg-open", os.path.join(os.path.dirname(self.__filename.get()), fileName)))
            elif os.name == 'nt':
                os.startfile(os.path.join(os.path.dirname(self.__filename.get()), fileName))
        elif fileName.endswith('(folder)'):
            fileName = fileName[:-12]
            _baseName = os.path.basename(self.__filename.get())
            for i in range(len(fileName) - len(_baseName)):
                self.__fname.insert(END, fileName[len(_baseName) + i])
            self.__fname.insert(END, os.sep)
        self.__fname.focus_set()

    def dialogBox(self, title, cmd):
        x, y = self.sizeOfWindow(300, 70)
        self._rootTop = Toplevel()
        self._rootTop.title(title)
        self._rootTop.geometry(f'300x70+{x}+{y}')
        self._rootTop.resizable(0, 0)
        _bFrame = Frame(self._rootTop)
        _bFrame.pack(side=BOTTOM)
        _entryTop = Entry(self._rootTop, textvariable=self.__topEntry, width=30)
        _entryTop.pack(side=TOP, pady=4)
        _entryTop.bind('<Return>', cmd)
        _entryTop.focus_set()
        _buttonTopCancel = Button(_bFrame, text="cancel", command=self._rootTop.destroy)
        _buttonTopCancel.pack(side=RIGHT, pady=4)
        _buttonTopCreate = Button(_bFrame, text="create", command=cmd)
        _buttonTopCreate.pack(side=RIGHT, pady=4)

    def newDir(self, *args):
        if self.__filename.get() != '':
            self.dialogBox('new folder dialog', self.createDir)
        else:
            showinfo('info', 'invalid Path')

    def newFile(self, *args):
        if self.__filename.get() != '':
            self.dialogBox('new file dialog', self.createFile)
        else:
            showinfo('info', 'invalid Path')

    def createFile(self, *args):
        fileName = self.__topEntry.get()
        name, extension = os.path.splitext(fileName)
        if name != '' and extension != '' and validateName(name, 'file'):
            f = open(os.path.join(os.path.dirname(self.__filename.get()), fileName), 'w+')
            f.close()
            showinfo('info', f'{fileName} has created')
            self.printList()
            self._rootTop.destroy()
        else:
            showinfo('info', 'invalid name')

    def createDir(self, *args):
        if self.__topEntry.get() != '' and validateName(self.__topEntry.get(), 'folder') == True:
            fileName = self.__topEntry.get()
            os.mkdir(os.path.join(os.path.dirname(self.__filename.get()), fileName))
            showinfo('info', f'{fileName} has created')
            self.printList()
            self._rootTop.destroy()
        else:
            showinfo('info', 'invalid name')

    def shortcutDialog(self, *args):
        text = '''1. create new file : 
    ctrl + N

2. create new Folder : 
    ctrl + shift + N

3. help : 
    ctrl + H

4. delete :
    ctrl + D'''

        x, y = self.sizeOfWindow(300, 370)
        _shortCutTop = Tk()
        _shortCutTop.title('shortcuts')
        _shortCutTop.geometry(f'300x370+{x}+{y}')
        _shortCutTop.resizable(0, 0)
        _header = Frame(_shortCutTop, bg="#CCC")
        _header.pack(side=TOP, fill=X)
        _hLabel = Label(_header, bg="#CCC", text='Shortcuts :', font='monaco 14')
        _hLabel.pack(anchor='w')
        _content = Frame(_shortCutTop)
        _content.pack(side=TOP, fill=X, padx=10, pady=5)
        _cLabel = Label(_content, text=text, font='consolas 10', justify=LEFT)
        _cLabel.pack(anchor='nw')
        _statusBar = Frame(_shortCutTop, bg="#CCC")
        _statusBar.pack(side=BOTTOM, fill=X)
        _stLabel = Label(_statusBar, bg="#CCC", text='Created by Sherlock...', font='hack 7')
        _stLabel.pack(anchor='s')

    def sizeOfWindow(self, childWindowWidth, childWindowHight):
        rootWindowWidth = self.__root.winfo_screenwidth()
        rootWindowHeight = self.__root.winfo_screenheight()

        x = (rootWindowWidth / 2) - (childWindowWidth / 2)
        y = (rootWindowHeight / 2) - (childWindowHight / 2)
        return round(x), round(y)

    def deleteContentSelected(self, *args):
        selectedIndex = self.__listArea.curselection()
        if len(selectedIndex) != 0 and self.__filename.get() != '' and os.path.exists(
                os.path.dirname(self.__filename.get())):
            condition = askyesno('info', 'do you want to delete ?')
            if condition:
                for i in selectedIndex:
                    if self.__listArea.get(i).endswith('(file)'):
                        os.remove(os.path.join(os.path.dirname(self.__filename.get()), self.__listArea.get(i)[:-10]))
                    elif self.__listArea.get(i).endswith('(folder)'):
                        shutil.rmtree(
                            os.path.join(os.path.dirname(self.__filename.get()), self.__listArea.get(i)[:-12]))
                self.printList()
        else:
            showinfo('info', 'illegal action')


if __name__ == '__main__':
    List = fileList()
    List.run()
