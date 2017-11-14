from slimit import minify
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import os
import time
import re

def getLastChildFromArray(arr):
    if len(arr) > 0:
        return arr[len(arr)-1]
    else:
        return None

def minifyJSProc(srcText):
    return minify(srcText, mangle=True, mangle_toplevel=True)

def doMinify(filePath):    
    with open(filePath,mode='r',encoding='utf-8') as file:
        try:
            minified = minify(file.read(), mangle=True, mangle_toplevel=True)
            file.close();
            filePathSplit = filePath.split('\\')
            minPath = ''
            for str in filePathSplit:
                if str == getLastChildFromArray(filePathSplit):                    
                    minPath = minPath + str.replace('.js','.min.js')
                else:
                    minPath = minPath + str + '\\'
            print(getLastChildFromArray(filePath.split('\\')) + ' -> ' + getLastChildFromArray(minPath.split('\\')))
            file = open(minPath,'w',-1,'utf-8')
            file.write(minified)
            file.close()
        except Exception as e:
            print(filePath + ' : 변환도중 에러가 발생했습니다.')
            print(e)
       
        
        
    

class fileWatcher(PatternMatchingEventHandler):    
    def on_created(self,event):
        time.sleep(0.1)
        print('새로운 파일 생성 - ' + event.src_path)
        doMinify(event.src_path)
        
    def on_modified(self,event):
        print('파일내 변경  - ' + event.src_path)
        doMinify(event.src_path)

def main():
    default = os.getcwd() + '\\watch.txt'
    infoStr = [
        '현재 경로(' + os.getcwd() + ') 의 .js파일을 지금 수정하시겠습니까?(Y or any other) : ',
        '기본값은 \'' + default + '\' 입니다. 다른 경로를 원하시면 값을 입력 해주세요.\n']
    minifyThisDir = input(infoStr[0])        
    if minifyThisDir.lower() == 'y':
        fileArr = os.walk(os.getcwd())
        for walk in fileArr :
            for fileName in walk[2]:
                if fileName.endswith('.js') and fileName.find('.min.') == -1 :
                    print('발견 : ' + walk[0] + '\\' +  fileName)
                    doMinify(walk[0] + '\\' +  fileName)
        print('수정 완료\n')
        
    
    print('현재경로(' + os.getcwd() + ') 혹은 특정 파일을 읽어서 해당 파일내의 경로의 .js파일을 감시, 경량화 합니다.')
    watchThis = input('현재경로를 감시하시겠습니까?(Y or any other) : ')
    if watchThis.lower() == 'y':
        targetDirs = [os.getcwd()]
    else:
        print('특정 파일을 읽어서 해당 파일내의 경로들을 감시합니다.')
        path = input(infoStr[1])
        if len(path) == 0:
            path = default
        while not os.path.exists(path):
            print(path + ' : 잘못된 파일 입니다.')
            path = input(infoStr[1])
            if len(path) == 0:
                path = default

        f = open(path,'r',-1,'utf-8')
        targetDirs = f.read().split('\n')
    
    dirFine = True
    for dir in targetDirs:
        if not os.path.exists(dir):
            print(dir + ' : 존재하지 않는 경로입니다. \n' + path + ' 파일 내용을 확인 후 다시 시도 해 주세요')
            dirFine = False
            input('엔터키를 눌러 종료 해 주세요...')
        if not os.path.isdir:
            print(dir + ' : 디렉토리 경로가 아닙니다. \n' + path + ' 파일 내용을 확인 후 다시 시도 해 주세요')
            dirFine = False
            input('엔터키를 눌러 종료 해 주세요...')
    if dirFine:        
        observer = Observer()
        for dir in targetDirs:
            observer.schedule(fileWatcher(patterns=["*.js","*.css"],ignore_patterns=['*.min.*']), dir, recursive=True)
            print(dir)
        observer.start()        
        print('해당경로 감시중...')
        print('종료를 원하시면 Ctrl+C를 눌러주세요')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            
            exit()
        observer.stop()
        
if __name__ == '__main__':
    main()
