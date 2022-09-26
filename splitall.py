import os

inputpath = r'C:\Users\Pete\Documents\DOCKER\input'
outputpath = r'C:\Users\Pete\Documents\DOCKER\output'
donepath = r'C:\Users\Pete\Documents\DOCKER\done'

f = []
for (dirpath, dirnames, filenames) in walk(inputpath):
    f.extend(filenames)
    break

for i in f:
    print(i)