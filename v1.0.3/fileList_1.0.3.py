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
    __outPutFrame = Frame(__root)
    __menuBar = Menu(__root)
    __scrollBarRight = Scrollbar(__outPutFrame)
    __scrollBarBottom = Scrollbar(__outPutFrame, orient=HORIZONTAL)
    __controlFrame = Frame(__root, bd=2, relief=SUNKEN, pady=8)
    __dirName = ''
    __baseName = ''
    __topEntry = StringVar()

    def __init__(self):
        self.__root.title("FileList")
        x, y = self.sizeOfWindow(500, 500)
        self.__root.geometry(f"500x500+{x}+{y}")
        self.__root.minsize(500, 500)

        self.__root.config(menu=self.__menuBar)
        self.__applicationMenu = Menu(self.__menuBar, tearoff=0)
        self.__applicationMenu.add_command(label="Help", command=self.shortcutDialog, accelerator='Ctrl+H')
        self.__applicationMenu.add_command(label='About App', command=self.aboutApp)
        self.__applicationMenu.add_command(label='About Dev', command=self.aboutDev)
        self.__applicationMenu.add_command(label="Exit", command=self.quit)
        self.__menuBar.add_cascade(label="FileList", menu=self.__applicationMenu, font='consolas 10 bold')

        self.__actionMenu = Menu(self.__menuBar, tearoff=0)
        self.__actionMenu.add_command(label='New file', command=self.newFile, accelerator='Ctrl+N')
        self.__actionMenu.add_command(label='New folder', command=self.newDir, accelerator='Ctrl+Shift+N')
        self.__actionMenu.add_command(label='delete', command=self.deleteContentSelected, accelerator='Ctrl+D')
        self.__menuBar.add_cascade(label="Action", menu=self.__actionMenu)

        self.__root.bind('<Control-n>', self.newFile)
        self.__root.bind('<Control-Shift-N>', self.newDir)
        self.__root.bind('<Control-h>', self.shortcutDialog)
        self.__root.bind('<Control-d>', self.deleteContentSelected)
        self.__filename.trace('w', self.searchFile)

        self.__outPutFrame.pack(fill=BOTH, expand=True, padx=10, pady=4)
        self.__scrollBarRight.pack(side=RIGHT, fill=Y)
        self.__listArea = Listbox(self.__outPutFrame)
        self.__listArea.pack(expand=True, fill=BOTH)
        self.__scrollBarBottom.pack(side=BOTTOM, fill=X)
        self.__scrollBarRight.config(command=self.__listArea.yview)
        self.__listArea.config(yscrollcommand=self.__scrollBarRight.set)
        self.__scrollBarBottom.config(command=self.__listArea.xview)
        self.__listArea.config(xscrollcommand=self.__scrollBarBottom.set)
        self.__listArea.config(font='monaco 11')
        self.__listArea.bind('<Return>', self.openRunFile)
        self.__listArea.bind('<Double-Button-1>', self.openRunFile)

        self.__controlFrame.pack(fill=BOTH, padx=10, pady=8)
        Label(self.__controlFrame, text="Enter path:", font="monaco 10 bold").pack()
        self.__fname = Entry(self.__controlFrame, textvariable=self.__filename, font='monaco', width=40)
        self.__fname.pack()
        self.__fname.focus_set()
        self.__fname.bind('<Right>', self.rightArrowKey)

    def aboutApp(self):
        __app = Toplevel()
        __app.title('About Application')
        x, y = self.sizeOfWindow(300, 200)
        __app.geometry(f'300x200+{x}+{y}')
        __app.resizable(0, 0)
        __app.grab_set()
        __head = Label(__app, text='FileList', font='Hack 14 bold', pady=20)
        __head.pack()
        text = 'version : 1.0.0\nFileList is simple file manager.\nIt is written in python.\n'
        __content = Label(__app, text=text, font='monaco 8')
        __content.pack(side=TOP)

    def aboutDev(self):
        __app = Toplevel()
        __app.title('About Developer')
        x, y = self.sizeOfWindow(300, 200)
        __app.geometry(f'300x200+{x}+{y}')
        __app.resizable(0, 0)
        __app.grab_set()
        __head = Label(__app, text='Sujan Mondal', font='Hack 14 bold', pady=20)
        __head.pack()
        text = 'diploma in Electrical Engineering\nCEO of MicroStation Corp\nProgrammer by passion'
        __content = Label(__app, text=text, font='monaco 8')
        __content.pack(side=TOP)

    def run(self):
        self.__root.mainloop()

    def quit(self):
        self.__root.destroy()

    def searchFile(self, *args):
        if self.__filename.get().endswith(f'{os.sep}{os.sep}'):
            self.__fname.delete(len(self.__filename.get()) - 1)
        elif self.__filename.get().endswith(os.sep) and os.path.isfile(os.path.abspath(self.__filename.get())):
            showinfo('info', 'it is a file')
            self.__fname.delete(len(self.__filename.get()) - 1)
            self.printList()
        elif self.__filename.get().endswith(os.sep) and os.path.exists(self.__filename.get()):
            self.printList()
        elif not self.__filename.get().endswith(os.sep) and os.path.exists(os.path.dirname(self.__filename.get())):
            self.printList()
            if self.__listArea.size() == 1:
                showinfo('info', 'not found')
                self.__fname.delete(len(self.__filename.get()) - 1)
                self.printList()
        elif self.__filename.get().endswith(os.sep) and not os.path.exists(os.path.dirname(self.__filename.get())):
            showinfo('info', 'invalid Action')
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
            if i.find(self.__baseName) != -1 and os.path.isfile(os.path.join(self.__dirName, i)):
                self.__listArea.insert(END, f'{i}  - (file)')
            elif i.find(self.__baseName) != -1:
                self.__listArea.insert(END, f'{i}  - (folder)')
        self.__listArea.activate(1)

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
            dirName = os.path.dirname(self.__filename.get())
            newAddress = os.path.join(dirName, fileName)
            self.__fname.delete(0, END)
            self.__fname.insert(END, f"{newAddress}{os.sep}")
        self.__fname.focus_set()

    def rightArrowKey(self, *args):
        if self.__listArea.get(1).endswith('(folder)'):
            fileName = self.__listArea.get(ACTIVE)
            fileName = fileName[:-12]
            dirName = os.path.dirname(self.__filename.get())
            newAddress = os.path.join(dirName, fileName)
            self.__fname.delete(0, END)
            self.__fname.insert(0, newAddress)

    def dialogBox(self, title, cmd):
        x, y = self.sizeOfWindow(300, 70)
        self._rootTop = Toplevel()
        self._rootTop.title(title)
        self._rootTop.grab_set()
        self._rootTop.geometry(f'300x70+{x}+{y}')
        self._rootTop.resizable(0, 0)
        _bFrame = Frame(self._rootTop)
        _bFrame.pack(side=BOTTOM)
        self._entryTop = Entry(self._rootTop, textvariable=self.__topEntry, width=30)
        self._entryTop.pack(side=TOP, pady=4)
        self._entryTop.bind('<Return>', cmd)
        self._entryTop.focus_set()
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
            try:
                f = open(os.path.join(os.path.dirname(self.__filename.get()), fileName), 'x')
                f.close()
            except:
                self._rootTop.grab_release()
                showinfo('info', 'file already exists')
                self._rootTop.grab_set()
                return None
            self._rootTop.grab_release()
            showinfo('info', f'{fileName} has created')
            self.printList()
            self._entryTop.delete(0, END)
            self._rootTop.destroy()
        else:
            showinfo('info', 'invalid name')

    def createDir(self, *args):
        if self.__topEntry.get() != '' and validateName(self.__topEntry.get(), 'folder') == True:
            fileName = self.__topEntry.get()
            try:
                os.mkdir(os.path.join(os.path.dirname(self.__filename.get()), fileName))
            except:
                self._rootTop.grab_release()
                showinfo('info','folder already exists')
                self._rootTop.grab_set()
                return None
            self._rootTop.grab_release()
            showinfo('info', f'{fileName} has created')
            self.printList()
            self._entryTop.delete(0, END)
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
    ctrl + D

5. Exit :
    ctrl +q'''

        x, y = self.sizeOfWindow(300, 370)
        self._shortCutTop = Toplevel()
        self._shortCutTop.title('shortcuts')
        self._shortCutTop.geometry(f'300x370+{x}+{y}')
        self._shortCutTop.resizable(0, 0)
        self._shortCutTop.grab_set()
        _header = Frame(self._shortCutTop, bg="#CCC")
        _header.pack(side=TOP, fill=X)
        _hLabel = Label(_header, bg="#CCC", text='Shortcuts :', font='monaco 14')
        _hLabel.pack(anchor='w')
        _content = Frame(self._shortCutTop)
        _content.pack(side=TOP, fill=X, padx=10, pady=5)
        _cLabel = Label(_content, text=text, font='Hack 9', justify=LEFT)
        _cLabel.pack(anchor='nw')
        _statusBar = Frame(self._shortCutTop, bg="#CCC")
        _statusBar.pack(side=BOTTOM, fill=X)
        _stLabel = Label(_statusBar, bg="#CCC", text='Created by Sujan Mondal...', font='hack 7')
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
