import os
import subprocess
import sys
from tkinter import *
from tkinter.messagebox import *
import re
import shutil


def validateName(name):
    Reg = re.compile('[~`$%^&*{}:;"\',<>?/\[\]]')
    if Reg.search(name) is None:
        return True
    else:
        return False


def validateExt(ext):
    try:
        with open('extension.txt', 'r') as file:
            str = file.read()
            list = str.split('\n')
            list.pop()
        if ext in list:
            return True
        else:
            return False
    except:
        return None


class fileList:
    __root = Tk()
    fileName = StringVar()
    __outPutFrame = Frame(__root)
    __menuBar = Menu(__root)
    __scrollBarRight = Scrollbar(__outPutFrame)
    __scrollBarBottom = Scrollbar(__outPutFrame, orient=HORIZONTAL)
    __controlFrame = Frame(__root, bd=2, relief=SUNKEN, pady=8)
    __dirName = ''
    __baseName = ''
    __topEntry = StringVar()
    _text = StringVar()

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
        self.__menuBar.add_cascade(label="FileList", menu=self.__applicationMenu, font='firacode 10 bold')

        self.__actionMenu = Menu(self.__menuBar, tearoff=0)
        self.__actionMenu.add_command(label='New file', command=self.newFile, accelerator='Ctrl+N')
        self.__actionMenu.add_command(label='New folder', command=self.newDir, accelerator='Ctrl+Shift+N')
        self.__actionMenu.add_command(label='Rename', command=self.renameFunc, accelerator='Ctrl+R')
        self.__actionMenu.add_command(label='delete', command=self.deleteContentSelected, accelerator='Ctrl+D')
        self.__menuBar.add_cascade(label="Action", menu=self.__actionMenu, font='hack 10')

        self.__root.bind('<Control-n>', self.newFile)
        self.__root.bind('<Control-Shift-N>', self.newDir)
        self.__root.bind('<Control-h>', self.shortcutDialog)
        self.__root.bind('<Control-d>', self.deleteContentSelected)
        self.__root.bind('<Control-r>', self.renameFunc)
        self.fileName.trace('w', self.searchFile)

        self.__outPutFrame.pack(fill=BOTH, expand=True, padx=10, pady=4)
        self.__scrollBarRight.pack(side=RIGHT, fill=Y)
        self.__listArea = Listbox(self.__outPutFrame, selectmode=EXTENDED, bd=3)
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
        self.fName = Entry(self.__controlFrame, bd=3, textvariable=self.fileName, font='monaco', width=40)
        self.fName.pack()
        self.fName.focus_set()
        self.fName.bind('<Right>', self.rightArrowKey)

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
        if self.fileName.get().endswith(f'{os.sep}{os.sep}'):
            self.fName.delete(len(self.fileName.get()) - 1)
        elif self.fileName.get().endswith(os.sep) and os.path.isfile(os.path.abspath(self.fileName.get())):
            showinfo('info', 'it is a file')
            self.fName.delete(len(self.fileName.get()) - 1)
            self.printList()
        elif self.fileName.get().endswith(os.sep) and os.path.exists(self.fileName.get()):
            self.printList()
        elif not self.fileName.get().endswith(os.sep) and os.path.exists(os.path.dirname(self.fileName.get())):
            self.printList()
            if self.__listArea.size() == 1:
                showinfo('info', 'not found')
                self.fName.delete(len(self.fileName.get()) - 1)
                self.printList()
        elif self.fileName.get().endswith(os.sep) and not os.path.exists(os.path.dirname(self.fileName.get())):
            showinfo('info', 'invalid Action')
            self.fName.delete(len(self.fileName.get()) - 1)
            self.printList()
        elif self.fileName.get() == '':
            self.__listArea.delete(0, END)
            self.__root.title("FileList")

    def printList(self):
        self.__dirName, self.__baseName = os.path.split(self.fileName.get())
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

    def renameDialog(self, w, h):
        def ren(*args):
            path = os.path.dirname(self.fileName.get())
            list = os.listdir(path)
            if __newName.get() != '' and validateName(__newName.get()):
                if self.__listArea.get(ACTIVE).endswith('(file)'):
                    srcFile = self.__listArea.get(ACTIVE)[:-10]
                    srcName, srcExt = os.path.splitext(srcFile)
                    newFile = __newName.get() + srcExt
                    if not newFile in list:
                        os.rename(os.path.join(path, srcFile), os.path.join(path, newFile))
                        self.printList()
                        showinfo('info', 'Rename done')
                        _renameTop.destroy()
                    else:
                        showinfo('info', 'file name already exist')
                else:
                    if not __newName.get() in list:
                        srcFile = self.__listArea.get(ACTIVE)[:-12]
                        os.rename(os.path.join(path, srcFile), os.path.join(path, __newName.get()))
                        self.printList()
                        showinfo('info', 'Rename done')
                        _renameTop.destroy()
                    else:
                        showinfo('info', 'folder name already exist')
            else:
                showinfo('info', 'invalid Name')

        __newName = StringVar()
        x, y = self.sizeOfWindow(w, h)
        _renameTop = Toplevel()
        _renameTop.title('Rename Dialog Box')
        _renameTop.grab_set()
        _renameTop.geometry(f'{w}x{h}+{x}+{y}')
        _renameTop.resizable(0, 0)
        Label(_renameTop, text='Enter New Name :', font='hack 10').pack()
        _entryTop = Entry(_renameTop, bd=3, textvariable=__newName, width=30)
        _entryTop.pack(side=TOP, pady=3)
        _entryTop.bind('<Return>', ren)
        _entryTop.focus_set()
        _bFrame = Frame(_renameTop)
        _bFrame.pack(side=TOP)
        _buttonTopCancel = Button(_bFrame, bd=3, text="Cancel", command=_renameTop.destroy, font='hack 10')
        _buttonTopCancel.pack(side=RIGHT, pady=4)
        _buttonTopRename = Button(_bFrame, bd=3, text="Rename", font='hack 10', command=ren)
        _buttonTopRename.pack(side=RIGHT, pady=4)
        Label(_renameTop, text=self._text, font="hack 8").pack(side=BOTTOM)

    def renameFunc(self, *args):
        if self.fileName.get() != '' and len(self.__listArea.curselection()) == 1 and self.__listArea.get(
                ACTIVE).startswith(os.pardir) == False:
            if self.__listArea.get(ACTIVE).endswith('(file)'):
                self._text = '*file extension can\'t be change'
                self.renameDialog(300, 120)
            else:
                self._text = None
                self.renameDialog(300, 100)
        else:
            showerror('error', 'invalid action')

    def openRunFile(self, *args):
        fileName = self.__listArea.get(ACTIVE)
        if fileName.startswith(os.pardir):
            newAddress = os.path.dirname(os.path.dirname(self.fileName.get()))
            for i in range(len(self.fileName.get()) - len(newAddress)):
                self.fName.delete(len(self.fileName.get()) - 1)
            if newAddress != os.sep:
                self.fName.insert(END, os.sep)
        elif fileName.endswith('(file)'):
            fileName = fileName[:-10]
            if os.name == 'posix':
                subprocess.call(("xdg-open", os.path.join(os.path.dirname(self.fileName.get()), fileName)))
            elif os.name == 'nt':
                os.startfile(os.path.join(os.path.dirname(self.fileName.get()), fileName))
        elif fileName.endswith('(folder)'):
            fileName = fileName[:-12]
            dirName = os.path.dirname(self.fileName.get())
            newAddress = os.path.join(dirName, fileName)
            self.fName.delete(0, END)
            self.fName.insert(END, f"{newAddress}{os.sep}")
        self.fName.focus_set()

    def rightArrowKey(self, *args):
        if self.__listArea.get(1).endswith('(folder)'):
            fileName = self.__listArea.get(ACTIVE)
            fileName = fileName[:-12]
            dirName = os.path.dirname(self.fileName.get())
            newAddress = os.path.join(dirName, fileName)
            self.fName.delete(0, END)
            self.fName.insert(0, newAddress)

    def dialogBox(self, title, cmd):
        x, y = self.sizeOfWindow(300, 100)
        self._rootTop = Toplevel()
        self._rootTop.title(title)
        self._rootTop.grab_set()
        self._rootTop.geometry(f'300x100+{x}+{y}')
        self._rootTop.resizable(0, 0)
        _bFrame = Frame(self._rootTop)
        _bFrame.pack(side=BOTTOM)
        Label(self._rootTop, text='Enter Name :', font='hack 10').pack()
        self._entryTop = Entry(self._rootTop, bd=3, textvariable=self.__topEntry, width=30)
        self._entryTop.pack(side=TOP, pady=4)
        self._entryTop.bind('<Return>', cmd)
        self._entryTop.focus_set()
        _buttonTopCancel = Button(_bFrame, bd=3, text="cancel", command=self._rootTop.destroy, font='hack 10')
        _buttonTopCancel.pack(side=RIGHT, pady=4)
        _buttonTopCreate = Button(_bFrame, bd=3, text="create", command=cmd, font='hack 10')
        _buttonTopCreate.pack(side=RIGHT, pady=4)

    def newDir(self, *args):
        if self.fileName.get() != '':
            self.dialogBox('new folder dialog', self.createDir)
        else:
            showinfo('info', 'invalid Path')

    def newFile(self, *args):
        if self.fileName.get() != '':
            self.dialogBox('new file dialog', self.createFile)
        else:
            showinfo('info', 'invalid Path')

    def createFile(self, *args):
        fileName = self.__topEntry.get()
        name, extension = os.path.splitext(fileName)
        if name != '' and extension != '' and validateName(name) and validateExt(extension):
            try:
                f = open(os.path.join(os.path.dirname(self.fileName.get()), fileName), 'x')
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
            showinfo('info', 'invalid filename or extension')

    def createDir(self, *args):
        if self.__topEntry.get() != '' and validateName(self.__topEntry.get()) == True:
            fileName = self.__topEntry.get()
            try:
                os.mkdir(os.path.join(os.path.dirname(self.fileName.get()), fileName))
            except:
                self._rootTop.grab_release()
                showinfo('info', 'folder already exists')
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

5. Rename :
    ctrl + R'''

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
        if len(selectedIndex) != 0 and self.fileName.get() != '' and os.path.exists(
                os.path.dirname(self.fileName.get())):
            condition = askyesno('info', 'do you want to delete ?')
            if condition:
                for i in selectedIndex:
                    if self.__listArea.get(i).endswith('(file)'):
                        os.remove(os.path.join(os.path.dirname(self.fileName.get()), self.__listArea.get(i)[:-10]))
                    elif self.__listArea.get(i).endswith('(folder)'):
                        shutil.rmtree(
                            os.path.join(os.path.dirname(self.fileName.get()), self.__listArea.get(i)[:-12]))
                self.printList()
        else:
            showinfo('info', 'illegal action')


if __name__ == '__main__':
    try:
        List = fileList()
        try:
            past = open('history.txt', 'r')
            List.fName.insert(0,past.read())
            past.close()
            List.printList()
        except:
            past = open('history.txt', 'x')
        f = open('extension.txt', 'r')
        f.close()
        List.run()
        past = open('history.txt', 'w')
        past.write(List.fileName.get())
        past.close()
    except:
        showinfo('info', 'Please download \'extension.txt\' from fileList repository '
                         'link = \'https://github.com/microStationCorp/fileList\'')
