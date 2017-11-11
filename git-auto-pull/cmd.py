from subprocess import Popen,PIPE,STDOUT
import sys




path = Popen('temp2.bat',stdout=PIPE).stdout.readlines()[0].decode()
path = path.split('PATH=')[1].replace('\r\n','').split(';')
print(path)

    
