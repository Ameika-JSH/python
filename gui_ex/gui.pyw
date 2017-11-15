from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

import git_auto_pull as gtap
import threading


class GuiApp:
    def __init__(self,root,**kw):
        self.root = root
        self.env_str = gtap.getEnv()        
        self.generate(kw)

    def setTxtPaths(self,text):
        self.txtPaths.insert(INSERT,text + '\n')

    def doReRegi(self):
        self.txtPaths.config(state=NORMAL)
        self.txtPaths.delete('1.0',END)
        self.txtPaths.insert(INSERT,'컴퓨터에서 git 폴더를 검색합니다.(수초에서 수분정도 소요됩니다)\n')
        gits = gtap.searchGitFolder(self)        

    def preDoGitAlert(self):
        if askokcancel("확인", str(len(self.env_str)) + "개의 경로에 대해 시작하시겠습니까?"):
            print(1)
        
        
    def generate(self,kw):        
        titleLabel = Label(self.root,text='자동 git 처리기')
        titleLabel.pack()

        pathsLabel = Label(self.root,text='대상 경로')
        pathsLabel.pack()

        self.txtPaths = Text(self.root,width=30,height=40)
        self.txtPaths.pack()

        btnReRegi = Button(self.root,text='재검색',command=self.doReRegi)
        btnReRegi.pack()

        cmdCombo = Combobox(self.root,values=('fetch','pull','push'))
        cmdCombo.pack()
        cmdCombo.current(0)

        btnDoGit = Button(self.root,text='시작',command=self.preDoGitAlert)
        btnDoGit.pack()

        self.env_str = self.env_str.split(gtap.env_name+'=')[1].split(';')
        pathsStr = ''
        for p in self.env_str:
            pathsStr += p + '\n'
        
        self.setTxtPaths(pathsStr)
        self.txtPaths.config(state=DISABLED)
        
        self.root.mainloop()  
        

root = Tk()
guiApp = GuiApp(root,text="teette")
