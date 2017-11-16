from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import os

import git_auto_pull as gtap

titleText = '자동 git 처리기'
gits = []

class GuiApp:
    def __init__(self,root,**kw):
        self.root = root
        self.env_str = gtap.getEnv()
        if self.env_str != '':
            gits = self.env_str.replace('\n','').split('_PATH=')[1].split(';')
        self.generate(kw)

    def setTxtPaths(self,txtCmd,text,ends='\n'):
        self.txtPaths.config(state=NORMAL)
        self.txtPaths.insert(txtCmd,text + ends)
        self.txtPaths.config(state=DISABLED)     

    def doReRegi(self):
        self.txtPaths.config(state=NORMAL)
        self.txtPaths.delete('1.0',END)
        self.setTxtPaths(INSERT,'컴퓨터에서 git 폴더를 검색합니다.\n(수초에서 수분정도 소요됩니다)\n')
        gits = gtap.searchGitFolder(self)
        self.setTxtPaths(INSERT,"검색이 완료되었습니다.\n경로 등록작업을 시작합니다.")
        tempArr = gits.copy()
        for path in tempArr:
            if not askokcancel('경로추가 확인',path + '\n추가하시겠습니까?'):
                gits.remove(path)
        os.popen('setx ' + gtap.env_name + ' ' + str(gits)[1:-1].replace(',',';').replace(' ','').replace('\'','').replace('\\\\','\\')).read()        

        self.txtPaths.config(state=NORMAL)
        self.txtPaths.delete('1.0',END)
        for path in gits:
            self.setTxtPaths(INSERT,path)
        self.root.title(titleText)    
        

    def preDoGitAlert(self):
        if askokcancel("확인", str(len(gits)) + "개의 경로에 대해 시작하시겠습니까?"):
            gtap.searchGitFolder(self)
        print(os.popen('set ' + gtap.env_name).read())
        
    def generate(self,kw):      
        self.root.title(titleText)        

        pathsLabel = Label(self.root,text='대상 경로')
        pathsLabel.pack()

        self.txtPaths = Text(self.root)
        self.txtPaths.config(width = 55,height=20)
        self.txtPaths.pack()
        if(os.popen('git').read() == ''):
            showerror('git 미설치','git이 설치되어있지 않습니다.\n설치페이지로 이동합니다.\n\n설치후 "~설치경로~/git/cmd" 경로가 \npath환경변수에 있는지 확인 해 주세요.')                        
            os.popen('@start http://msysgit.github.com/')
            self.root.destroy()
                    

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
        
        self.setTxtPaths(INSERT,pathsStr,'')
        self.txtPaths.config(state=DISABLED)
        
        self.root.mainloop()  
        

root = Tk()
root.geometry("400x500")
#menubar = Menu(root)
#menubar.add_command(label='test')
#root.config(menu=menubar)
guiApp = GuiApp(root)
