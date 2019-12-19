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

        self.__thisControlFrame.grid_columnconfigure(0, weight=1)
        self.__thisControlFrame.grid_rowconfigure(0, weight=1)
        Label(self.__thisControlFrame, text="Direction", bg="#AAA", font="monaco 12 bold").grid(pady=5)
        self.__fname = Entry(self.__thisControlFrame, textvariable=self.__filename, font='monaco')
        self.__fname.grid(sticky=E + W + N + S, padx=30, row=1, column=0)
        self.__fname.focus_set()
        self.__buttonFrame = Frame(self.__thisControlFrame, borderwidth=2, relief=SUNKEN)
        self.__buttonFrame.grid(row=2, column=0)
        self.__buttonSelect = Button(self.__buttonFrame, text='Select', font='monaco 11')
        self.__buttonSelect.pack(side=LEFT)
        self.__buttonOpen = Button(self.__buttonFrame, text='Run', font='monaco 11', width=6)
        self.__buttonOpen.pack(side=LEFT)

    def run(self):
        self.__root.mainloop()

    # def searchFile(self, *args):


List = fileList()
List.run()
