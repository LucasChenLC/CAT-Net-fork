import os


dataset_path = '/home/ucas/Projects/CAT-Net/Splicing/CASIA2'

tp_path = os.path.join(dataset_path, 'CASIA 2.0/Tp')
files = os.listdir(tp_path)
count = 0 
'''for file in files:
    if file == 'Tp_S_CRN_S_B_arc00095_arc00095_01035.tif':
        print()
    if file.endswith('.tif'):
        if not os.path.exists(os.path.join(dataset_path, 'CASIA 2.0/jpg',f'{file[:-3]}jpg')):
            print(os.path.exists(os.path.join(dataset_path, 'CASIA 2.0/jpg',f'{file[:-3]}jpg')))
            count += 1
            
print(f'{count}/{len(files)}')'''


file_path = '/home/ucas/Projects/CAT-Net/Splicing/data/CASIA_v2_valid_list.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()
    count = 0
    valid_lines = []
    for line in lines:
        line = line[:-1]
        imgs = line.split(',')
        flags = [True, True, True]
        for i in range(len(imgs)):
            if not os.path.exists(os.path.join(dataset_path, imgs[i])):
                flags[i] = False
        if flags == [True, True, True] or flags == [True, True, False]:
            valid_lines.append(line)
        else:
            count += 1
            
data = '\n'.join(valid_lines)
with open(file_path, 'w') as file:
    file.write(data)
print(count)