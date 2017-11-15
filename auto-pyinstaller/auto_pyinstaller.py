import os,time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def runPyInstaller(file):
    print('####' + file + ' => exe파일로 빌드중...')
    options = ' -F'
    if file.endswith('.pyw'):
        options += ' -w'
    return os.popen('pyinstaller ' + file + options)

class fileWatcher(PatternMatchingEventHandler):
    processingPath = []        
    def on_modified(self,event):         
        super()
        if not event.src_path in self.processingPath:
            self.processingPath.append(event.src_path)            
            runPyInstaller(event.src_path).close()
        else:
            self.processingPath.remove(event.src_path)
            
        

def watchPy():
    observer = Observer()
    fWatcher = fileWatcher(patterns=["*.py","*.pyw"])
    observer.schedule(fWatcher, os.getcwd(), recursive=True)
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
            lastFile = runPyInstaller(os.getcwd() + "\\" + file)
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
    
           
