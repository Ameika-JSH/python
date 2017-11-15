import os,re,time,sys

env_name = 'GIT_AUTO_PULL_PATH'
origin_path = os.getcwd()

def searchGitCmdFolder():
    mnt = re.findall(r'[a-z]:\\',os.popen('mountvol').read(),re.IGNORECASE)
    for d in mnt:
        print(d + '검색 시작...')    
        gitCmdPath = ''
        for w in os.walk(d):
            if(re.match(r'.*\\Git',w[0],re.IGNORECASE) and 'cmd' in w[1]):
                gitCmdPath = w[0] + '\\cmd'            
                break
        if len(gitCmdPath) > 0:
            print('git 폴더 발견! ( ' + gitCmdPath + ')\n해당 경로를 환경변수에 추가합니다.')            
            os.popen('setx GIT_PATH ' + gitCmdPath)        

def searchGitFolder():
    mnt = re.findall(r'[a-z]:\\',os.popen('mountvol').read(),re.IGNORECASE)
    gits = []
    for d in mnt:
        temp = []
        print(d + '검색 시작...')
        for w in os.walk(d):
            if'.git' in w[1]:
                temp.append(w[0])
                print(w[0])
        if len(temp) != 0:             
            gits += temp
        
    return gits
def getDateStr():
    rtn = str(time.localtime().tm_year) + '/'
    rtn += str(time.localtime().tm_mon) + '/'
    rtn += str(time.localtime().tm_mday)
    return rtn

def getTimeStr():
    rtn = str(time.localtime().tm_hour) + ':'
    rtn += str(time.localtime().tm_min) + ':'
    rtn += str(time.localtime().tm_sec)
    return rtn

def showHelp():
    rtnStr = ''
    rtnStr += '==git-auto-pull tool==\n\n'
    rtnStr += '/?    help\n'
    rtnStr += '/r    git path re-registration\n'
    rtnStr += 'pull, push, fetch    git default command\n'
    print(rtnStr)

def reRegi(infoStr='git auto pull 대상을 재등록 합니다.\n컴퓨터에서 git 폴더를 검색합니다.(수초에서 수분정도 소요됩니다)',gitTargets=[]):
    print(infoStr)
    gits = searchGitFolder()    
    print('git auto pull 대상을 등록합니다.')    
    for git in gits:
        if input(git + ' : 등록하시겠습니까? (Y or any other)').lower() == 'y':
            gitTargets.append(git)
    if len(gitTargets) == 0:
        print('등록 할 대상이 없습니다.\n프로그램을 종료합니다.')
        exit()
    else:
        print('총 ' + str(len(gitTargets)) + '개의 경로에 대해 git auto pull 작업을 등록합니다.')
        os.popen('setx ' + env_name + ' ' + str(gitTargets)[1:-1].replace(',',';').replace(' ','').replace('\'','').replace('\\\\','\\'))       

cmdList = {'?':showHelp,'r':reRegi}
gitCmdList = ['pull','push','fetch']
if __name__ == '__main__':
    regiMsg = 'git auto pull 대상이 등록되어 있지 않습니다.\n컴퓨터에서 git 폴더를 검색합니다.(수초에서 수분정도 소요됩니다)'
    gitCmdTest = os.popen('git').read()
    fileName = sys.argv[0].split('\\')[-1].split('.')[0]
    cmdArg = ''
    if not gitCmdTest or len(gitCmdTest) == 0:
            #print('git이 설치되어있지 않습니다.\ngit설치경로를 탐색합니다.')            
            print('git이 설치되어있지 않습니다.\n설치페이지로 이동합니다.')                        
            os.popen('@start http://msysgit.github.com/')
            input('종료하시려면 엔터키를 눌러주세요...')
    else:
        if len(sys.argv) == 1:
            print('명령어 없이 실행하셨습니다. 기본 명령어는 \'fetch\'입니다. 명령어 목록을 보시려면 \'' + fileName + ' ?\'를 입력 해 주세요.')
            cmdArg = 'fetch'
        else :
            if sys.argv[1] in list(cmdList.keys()):
                cmdList[sys.argv[1]]()
            elif sys.argv[1] in gitCmdList:
                cmdArg = sys.argv[1] 
            else:
                print('잘못된 인자값 입니다.')
                showHelp()
        if len(cmdArg) > 0 :
            env_str = os.popen('set ' + env_name).read()
            gitTargets = []
            if not env_str:
                reRegi(regiMsg,gitTargets)

            if len(gitTargets) == 0:
                gitTargets += env_str.replace('\n','').split('_PATH=')[1].split(';')
            results = []
            print('등록되어있는 ' + str(len(gitTargets)) + '개의 경로에 대해 git ' + cmdArg + '을 시작합니다.')
            for gitDir in gitTargets:
                os.chdir(gitDir)
                gitMsg = os.popen('git ' + cmdArg).read()
                rsltStr = '[' + cmdArg + '] ' + gitDir + ' - (' + getDateStr() + ' ' + getTimeStr() + ')\n' + gitMsg                
                results.append(rsltStr)
                print(results[-1],end='')
            logStr = ''
            for r in results:
                logStr += r
            logPath = origin_path + '\\gitpull.log'
            if input('로그를 남기시겠습니까? ['+logPath+'] (Y or any other)').lower() == 'y':
                if not os.path.exists(logPath):
                    open(logPath,'w',-1,'utf-8').close()
                f = open(logPath,'r',-1,'utf-8')
                dateChk = f.read().find(getDateStr())
                f.close()
                f = open(logPath,'a',-1,'utf-8')
                if dateChk == -1:
                    logStr  = '===============[' + getDateStr() + ']===============\n' + logStr
                f.write(logStr)
                f.close()      
