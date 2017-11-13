import os,re,time,sys

env_name = 'GIT_AUTO_PULL_PATH'
batName = 'temp.bat'
origin_path = os.getcwd()

def searchGitFolder():
    mnt = re.findall(r'[d-z]:\\',os.popen('mountvol').read(),re.IGNORECASE)
    gits = []
    for d in mnt:
        temp = []
        print(d + '검색 시작...')
        for w in os.walk(d):
            if'.git' in w[1]:
                temp.append(w[0])
        if len(temp) != 0:
            print(str(temp)[1:-1])
            gits += temp
        
    print('검색 결과 : ' + str(gits)[1:-1])
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
        print('총 ' + str(len(gitTargets)) + '개의 경로에 대해 git auto pull 작업을 등록합니다.\n관리자 권한을 얻기위한 UAC가 표시되면 확인을 눌러주세요')

        vbsStr = 'Set UAC = CreateObject("Shell.Application")\n'
        vbsStr += 'UAC.ShellExecute "cmd.exe", "/c ' + origin_path + '\\' + batName + '", "", "runas", 1'

        f = open('getadmin.vbs','w',-1,'utf-8')
        f.write(vbsStr)
        f.close()
        
        batHeader = '@echo off\nsetx '
        batGits = env_name + ' ' + str(gitTargets)[1:-1].replace(',',';').replace(' ','').replace('\'','').replace('\\\\','\\') + ' /m\n'
        batFooter = 'del "getadmin.vbs"\ndel "' + batName +'"\n'
        batFooter += 'exit\n'
        batFooter += ''      
        f = open(batName,'w',-1,'utf-8')         
        f.write(batHeader + batGits + batFooter)
        f.close()

        time.sleep(1.5)
        os.popen('getadmin.vbs')

cmdList = {'/?':showHelp,'/r':reRegi}
if __name__ == '__main__':
    regiMsg = 'git auto pull 대상이 등록되어 있지 않습니다.\n컴퓨터에서 git 폴더를 검색합니다.(수초에서 수분정도 소요됩니다)'
    
    if len(sys.argv) == 1:
        gitCmdTest = os.popen('git').read()
        if not gitCmdTest or len(gitCmdTest) == 0:
            print('git이 설치되어있지 않습니다.\n설치페이지로 이동합니다.')
            time.sleep(1.5)
            os.popen('@start http://msysgit.github.com/')
        else:
            env_str = os.popen('set ' + env_name).read()
            gitTargets = []
            if not env_str:
                reRegi(regiMsg,gitTargets)

            if len(gitTargets) == 0:
                gitTargets += env_str.replace('\n','').split('_PATH=')[1].split(';')
            results = []
            print('등록되어있는 ' + str(len(gitTargets)) + '개의 경로에 대해 git pull을 시작합니다.')
            for gitDir in gitTargets:
                os.chdir(gitDir)
                results.append(gitDir + ' - ' + str(os.popen('git pull').readlines()) + '(' + getDateStr() + ' ' + getTimeStr() + ')')
                print(results[-1])
            logStr = ''
            for r in results:
                logStr += r + '\n'
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
    else:
        if sys.argv[1] in list(cmdList.keys()):
            cmdList[sys.argv[1]]()                
        else:
            print('잘못된 인자값 입니다.')
            showHelp()