import os,re,time

def searchGitFolder():
    mnt = re.findall(r'[a-z]:\\',os.popen('mountvol').read(),re.IGNORECASE)
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

if __name__ == '__main__':
    env_name = 'GIT_AUTO_PULL_PATH'
    gitCmdTest = os.popen('git').read()
    if not gitCmdTest or len(gitCmdTest) == 0:
        print('git이 설치되어있지 않습니다.\n설치페이지로 이동합니다.')
        time.sleep(1.5)
        os.popen('@start http://msysgit.github.com/')
    else:
        if not os.popen(env_name).read():
            print('git auto pull 대상이 등록되어 있지 않습니다.\n컴퓨터에서 git 폴더를 검색합니다.(수초에서 수분정도 소요됩니다')
            gits = searchGitFolder()
            print('git auto pull 대상을 등록합니다.')
            gitTargets = []
            for git in gits:
                if input(git + ' : 등록하시겠습니까? (Y or any other)').lower() == 'y':
                    gitTargets.append(git)
            print('총 ' + str(len(gitTargets)) + '개의 경로에 대해 git auto pull 작업을 등록합니다.\n 관리자 권한을 얻기위한 UAC가 표시되면 확인을 눌러주세요')
            batHeader = '@echo off\nsetx '
            batGits = env_name + ' ' + str(gitTargets)[1:-1].replace(',',';') + ' /m'
            batFooter = "if '%errorlevel%' NEQ '0' (\n" + 
                         'echo Set UAC = CreateObject^("Shell.Application"^) > "getadmin.vbs"\n' + 
                         'set params = %*:"=""' + 
                         'echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> getadmin.vbs"'+
                         '"getadmin.vbs"' + 
                         'rem del "getadmin.vbs"' + 
                         'exit' +
                         ')'
