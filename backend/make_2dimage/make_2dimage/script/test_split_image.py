# epochの画像1枚を綺麗に4分割するスクリプト
from PIL import Image
import os
import glob
from datetime import datetime
import subprocess
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings

# PATH読み込み
top = settings.top
demo = settings.demo
output_image = settings.output_image


def ImgSplit(im):
    # 読み込んだ画像分割する
    height = 194
    width = 197

    buff = []
    # 縦の分割枚数
    for h1 in range(2):
        # 横の分割枚数
        for w1 in range(2):
            w2 = w1 * height + w1 * 67 
            h2 = h1 * width 
            print(w2, h2, width + w2, height + h2)
            c = im.crop((w2, h2, width + w2, height + h2))
            buff.append(c)
    return buff

if __name__ == '__main__':
    # 4枚全て綺麗に分割して、保存する。
    im = Image.open(os.path.join(top, output_image,'20211030_001341epoch_100.png'))
    for ig in ImgSplit(im):
        # 保存先フォルダの指定
        ig.save(os.path.join(top, output_image,'20211030_001341epoch_100.png')+ '_split' + datetime.now().strftime("%Y%m%d_%H%M%S%f_") +".png", "PNG")    