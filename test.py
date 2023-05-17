from PIL import Image
import time
import jpegio
import numpy as np
import os

def recover(file):
    Image.open(os.path.join(path, file)).convert('RGB').save(os.path.join(path, file))
    jpegio.read(os.path.join(path, file))

path = 'Splicing/PSData/ps_battles_orisize/mask'
txt_base = 'Splicing/data'
text_files = ['PSData_train_list.txt', 'PSData_auth_train_list.txt', 'PSData_val_list.txt', 'PSData_auth_val_list.txt']

text_file = text_files[3]
text_file = os.path.join(txt_base, text_file)

with open(text_file, 'r') as file:
    lines = file.readlines()
    lines = lines[:]
    line = lines[0][:-1]
    path1, path2, path3 = line.split(',')
    #jpegio.read(path3)
    #recover(path3)
    for i in range(len(lines)):
        print(f'{i}/{len(lines)}')
        line = lines[i][:-1]
        path1, path2, path3 = line.split(',')
        jpegio.read(path3)
        if path2 != 'None' and path2.endswith('.jpg'):
            jpegio.read(path2)

'''files = os.listdir(path)
for i in range(len(files)):
    if files[i].endswith('.jpg'):
        if i % 200 == 0:
            print(f'{i}/{len(files)}')

        #print(files[i])
        jpeg = jpegio.read(str(os.path.join(path, files[i])))'''
