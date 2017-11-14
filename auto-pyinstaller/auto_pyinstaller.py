import os

for file in os.listdir():
    if file.endswith('.py'):
        rslt = os.popen('pyinstaller ' + file + ' -F')
        
        
