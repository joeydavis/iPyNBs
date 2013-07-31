import os
path = str(os.system('pwd'))
dirs = [i for i in os.listdir(path) if os.path.isdir(path+i)]
for peaks in dirs:
    command1 = 'cd ' + path+peaks + ' && pwd && rm -rf *.png && rm -rf *.newcon && rm -rf *.fit'
    print command1
#os.system(command1)
