"""
Created by Myung-Joon Kwon
mjkwon2021@gmail.com
July 14, 2020
"""
import project_config
from Splicing.data.AbstractDataset import AbstractDataset

import os
import numpy as np
import random
from PIL import Image, ImageChops, ImageFilter
import torch
from pathlib import Path


class PSData(AbstractDataset):
    """
    directory structure:
    CASIA (dataset_path["CASIA"] in project_config.py)
    ├── CASIA 1.0 dataset (download: https://github.com/CauchyComplete/casia1groundtruth)
    │   ├── Au (un-zip it)
    │   └── Modified TP (un-zip it)
    ├── CASIA 1.0 groundtruth
    │   ├── CM
    │   └── Sp
    ├── CASIA 2.0 (download: https://github.com/CauchyComplete/casia2groundtruth)
    │   ├── Au
    │   └── Tp
    └── CASIA 2 Groundtruth  => Run renaming script in the excel file located in the above repo.
                            Plus, rename "Tp_D_NRD_S_N_cha10002_cha10001_20094_gt3.png" to "..._gt.png"
    """

    def __init__(self, crop_size, grid_crop, blocks: list, DCT_channels: int, tamp_list: str, read_from_jpeg=False):
        """
        :param crop_size: (H,W) or None
        :param blocks:
        :param tamp_list: EX: "Splicing/data/CASIA_list.txt"
        :param read_from_jpeg: F=from original extension, T=from jpeg compressed image
        """
        super().__init__(crop_size, grid_crop, blocks, DCT_channels)
        self._root_path = project_config.dataset_paths['PSData']
        with open(project_config.project_root / tamp_list, "r") as f:
            self.tamp_list = [t.strip().split(',') for t in f.readlines()]
        self.read_from_jpeg = read_from_jpeg

    def get_tamp(self, index):
        assert 0 <= index < len(self.tamp_list), f"Index {index} is not available!"
        tamp_path = self._root_path / (self.tamp_list[index][2] if self.read_from_jpeg else self.tamp_list[index][0])
        mask_path = self._root_path / self.tamp_list[index][1]
        if self.tamp_list[index][1] == 'None':
            mask = None
        else:
            mask = np.array(Image.open(mask_path).convert("L"))
            mask[mask > 0] = 1
        return self._create_tensor(tamp_path, mask)

    def get_qtable(self, index):
        assert 0 <= index < len(self.tamp_list), f"Index {index} is not available!"
        tamp_path = self._root_path / self.tamp_list[index][0]
        if not str(tamp_path).lower().endswith('.jpg'):
            return None
        DCT_coef, qtables = self._get_jpeg_info(tamp_path)
        Y_qtable = qtables[0]
        return Y_qtable


def tranfser_to_jpg(path_1, path_2, file_name, path_3=None):
    imlist = []
    root = project_config.dataset_paths['PSData']
    path_2.mkdir(exist_ok=True)
    for file in os.listdir(path_1):
        if not file.lower().endswith(".jpg"):
            if not file.lower().endswith(".png"):
                print(file)
                continue
            # convert to jpg
            jpg_im = Image.open(path_1 / file)
            jpg_im = jpg_im.convert('RGB')
            jpg_im.save(path_2 / (os.path.splitext(file)[0] + ".jpg"), quality=100, subsampling=0)
            p3 = str(path_2 / (os.path.splitext(file)[0] + ".jpg"))
        else:
            p3 = str(path_1 / file)
        if path_3 is None:
            p2 = 'None'
        else:
            p2 = str(path_3 / (os.path.splitext(file)[0] + ".png"))
        imlist.append(','.join([str(path_1 / file),
                                p2,
                                p3]))
    print(len(imlist))

    '''if path_3 is not None:
        new_imlist = []
        for i in range(len(imlist)):
            s = imlist[i]
            print(f'{i}/{len(imlist)}')
            im, mask, _ = s.split(',')
            im_im = np.array(Image.open(root / im))
            mask_im = np.array(Image.open(root / mask))
            if im_im.shape[0] != mask_im.shape[0] or im_im.shape[1] != mask_im.shape[1]:
                print("Skip:", im, mask)
                continue
            new_imlist.append(s)'''

    list = imlist if path_3 is None else imlist
    with open(file_name, "w") as f:
        f.write('\n'.join(list) + '\n')


if __name__ == '__main__':
    # CASIA2 has non-jpg files - we convert them here. You can choose original extension or jpeg when you test.

    root = project_config.dataset_paths['PSData']
    tamp_root = root / "ps_battles_orisize" / 'tampered'
    mask_root = root / "ps_battles_orisize" / 'mask'
    jpg_root = root / "ps_battles_orisize" / 'jpg'

    tranfser_to_jpg(tamp_root, jpg_root, "PSData_list.txt", mask_root)

    # CASIA2 authentic
    tamp_root = root / "ps_battles_orisize/original"
    jpg_root = root / "ps_battles_orisize/jpg"

    tranfser_to_jpg(tamp_root, jpg_root, 'PSData_auth_list.txt')

    with open('PSData_auth_list.txt', 'r') as file:
        lines = file.readlines()
        random.shuffle(lines)
        print(len(lines))

    train_lines = lines[:6108]
    val_lines = lines[6108:6108+764]
    test_lines = lines[6108+764:]

    with open('PSData_auth_train_list.txt', 'w') as file:
        file.write(''.join(train_lines))

    with open('PSData_auth_val_list.txt', 'w') as file:
        file.write(''.join(val_lines))

    with open('PSData_auth_test_list.txt', 'w') as file:
        file.write(''.join(test_lines))

    with open('PSData_list.txt', 'r') as file:
        lines = file.readlines()
        random.shuffle(lines)
        print(len(lines))

    train_lines = lines[:21945]
    val_lines = lines[21945:21945 + 2979]
    test_lines = lines[21945 + 2979:]

    with open('PSData_train_list.txt', 'w') as file:
        file.write(''.join(train_lines))

    with open('PSData_val_list.txt', 'w') as file:
        file.write(''.join(val_lines))

    with open('PSData_test_list.txt', 'w') as file:
        file.write(''.join(test_lines))
