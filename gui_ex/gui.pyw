from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import os


class GuiApp:    
        
       
    def __init__(self,root,**kw):
        self.root = root
        
        self.titleText = '자동 git 처리기'        
        self.env_name = 'GIT_AUTO_PULL_PATH'
        self.origin_path = os.getcwd()

        self.env_str = os.popen('set ' + self.env_name).read()
        self.gits = []
        if self.env_str != '':
            self.gits = self.env_str.replace('\n','').split('_PATH=')[1].split(';')
            
        self.mnt =  [ p + ':' for p in re.findall(r'([a-z]):\\',os.popen('mountvol').read(),re.IGNORECASE)]
        self.mnt.sort()
        self.mntAllStr = '전체'
        self.mnt.insert(0,self.mntAllStr)
        self.generate(kw)

    def arrayToString(self,arr,ends='\n'):
        tempRtn = ''
        for s in arr:
            tempRtn += str(s) + ends
        return tempRtn
        

    def setTxtPaths(self,txtCmd,text,ends='\n'):
        self.txtPaths.config(state=NORMAL)
        self.txtPaths.insert(txtCmd,text + ends)
        self.root.update()    
        self.txtPaths.config(state=DISABLED)     

    
    def searchGitFolder(self):
        self.root.title('경로 검색중...')
        mnt = []
        if self.mntCombo.get() == self.mntAllStr:
            mnt = re.findall(r'[a-z]:\\',os.popen('mountvol').read(),re.IGNORECASE)
        else:
            mnt.append(self.mntCombo.get() + '\\')
        gits = []
        indx = 0
        for d in mnt:
            temp = []
            self.setTxtPaths(INSERT,d + '검색 시작...')       
            for w in os.walk(d):   
                self.root.update()
                if'.git' in w[1]:
                    temp.append(w[0])
                    self.setTxtPaths(INSERT,w[0])
            if len(temp) != 0:             
                gits += temp
        return gits

    def pathStringToWindow(self,stringArr):
            pathsStr = self.arrayToString(stringArr)           
            self.setTxtPaths(INSERT,pathsStr,'')
        

    def doReRegi(self):
        self.txtPaths.config(state=NORMAL)
        self.txtPaths.delete('1.0',END)
        self.setTxtPaths(INSERT,str(self.mntCombo.get()) + '경로에서 git 폴더를 검색합니다.\n(수초에서 수분정도 소요됩니다)\n')
        preGits = self.gits.copy()
        self.gits = self.searchGitFolder()
        if len(self.gits) < 1:
            showwarning('결과 없음',str(self.mntCombo.get()) + '경로에 git 폴더가 없습니다.')
            self.gits = preGits.copy()
            self.txtPaths.config(state=NORMAL)
            self.txtPaths.delete('1.0',END)
            self.pathStringToWindow(self.gits)
            return
        
        self.setTxtPaths(INSERT,"검색이 완료되었습니다.\n경로 등록작업을 시작합니다.")
        tempArr = self.gits.copy()
        for path in tempArr:
            if not askokcancel('경로추가 확인',path + '\n추가하시겠습니까?'):
                self.gits.remove(path)
        os.popen('setx ' + self.env_name + ' "' + str(self.gits)[1:-1].replace(',',';').replace(' ','').replace('\'','').replace('\\\\','\\') + '"').read()

        if len(self.gits) > 0:
            showinfo('등록 완료',str(len(self.gits)) + '개의 경로가 등록되었습니다.')
            self.txtPaths.config(state=NORMAL)
            self.txtPaths.delete('1.0',END)
            self.btnDoGit.config(state=NORMAL)
            self.setTxtPaths(INSERT,self.arrayToString(self.gits))
        else:
            showwarning('등록 실패','등록 할 경로가 없습니다.\n다시 경로 등록 후 사용 해 주세요')
            self.gits = tempArr.copy()
            self.txtPaths.config(state=NORMAL)
            self.txtPaths.delete('1.0',END)
            self.pathStringToWindow(self.gits)
                
        self.root.title(self.titleText)    
        

    def preDoGitAlert(self):
        if askokcancel("확인", "등록되어있는 " + str(len(self.gits)) + "개의 경로에 대해\ngit " + self.cmdCombo.get() + '작업을 시작하시겠습니까?'):
            gitResult = ''
            for path in self.gits:
                os.chdir(path)
                cmd = os.popen('git ' + self.cmdCombo.get())
                gitResult += cmd.read()
                cmd.close()
            print(gitResult)
        
    def generate(self,kw):
        doGitState = NORMAL
        reRegiText = '경로 재검색'
                
        self.root.title(self.titleText)        

        pathsLabel = Label(self.root,text='대상 경로')
        pathsLabel.pack()

        self.txtPaths = Text(self.root)
        self.txtPaths.config(width = 55,height=20)
        self.txtPaths.pack()
        if(os.popen('git').read() == ''):
            showerror('git 미설치','git이 설치되어있지 않습니다.\n설치페이지로 이동합니다.\n\n설치후 "~설치경로~/git/cmd" 경로가 \npath환경변수에 있는지 확인 해 주세요.')                        
            os.popen('@start http://msysgit.github.com/')
            self.root.destroy()
        elif len(self.gits) < 1:
            showerror("경고",'등록된 경로가 없습니다.\n경로 등록 후 사용 해 주세요')
            doGitState = DISABLED
            reRegiText = '경로 검색'
        else:
            self.pathStringToWindow(self.gits)
            
            
        self.mntCombo = Combobox(self.root,values=self.mnt,state="readonly")
        self.mntCombo.pack()
        self.mntCombo.current(0)

        btnReRegi = Button(self.root,text=reRegiText,command=self.doReRegi)
        btnReRegi.pack()

        self.cmdCombo = Combobox(self.root,values=('fetch','pull','push'),state="readonly")
        self.cmdCombo.pack()
        self.cmdCombo.current(0)

        self.btnDoGit = Button(self.root,text='시작',command=self.preDoGitAlert, state=doGitState)
        self.btnDoGit.pack()
            
        self.txtPaths.config(state=DISABLED)        
        self.root.mainloop()          

root = Tk()
root.geometry("400x500")
guiApp = GuiApp(root)
