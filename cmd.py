from subprocess import Popen,PIPE,STDOUT
import sys
import pickle

rslt = Popen('temp.bat',stdout=PIPE)


print(rslt.stdout)

