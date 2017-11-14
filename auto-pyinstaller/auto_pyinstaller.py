import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def runPyInstaller(file):
    return os.popen('pyinstaller ' + file + ' -F')

class fileWatcher(PatternMatchingEventHandler):  
    def on_modified(self,event):
        print('파일내 변경  - ' + event.src_path)
        runPyInstaller(event.src_path)

def watchPy():
    observer = Observer()
    observer.schedule(fileWatcher(patterns=["*.py","*.pyw"]), os.getcwd(), recursive=True)
    observer.start()   

def installerStarter():
    lastFile = False
    cnt = 0
    for file in os.listdir():
        if file.endswith('.py'):
            print(file + ' => exe파일로 빌드중...')
            lastFile = runPyInstaller(file)
            cnt += 1
    return lastFile,cnt


if __name__ == '__main__':
    lastFile,cnt = installerStarter()
    endMsg = str(cnt) + '건 빌드 완료'
    if lastFile:
        lastFile.close()
    else:
        endMsg = '대상 파일이 없습니다.'
    print(endMsg)
    print(os.getcwd() + ' 경로의 *.py , *.pyw 파일 감시를 시작합니다.')
    watchPy() 
           
