import os,time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def runPyInstaller(file):
    file = file.split('\\')[-1]
    print(file + ' => exe파일로 빌드중...')
    return os.popen('pyinstaller ' + file + ' -F')

class fileWatcher(PatternMatchingEventHandler):    
    def on_modified(self,event):        
        time.sleep(0.1)
        runPyInstaller(event.src_path)
        super()

def watchPy():
    observer = Observer()
    observer.schedule(fileWatcher(patterns=["*.py","*.pyw"]), os.getcwd(), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        exit()
       
def installerStarter():
    lastFile = False
    cnt = 0
    for file in os.listdir():
        if file.endswith('.py'):
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
    
           
