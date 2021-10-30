# epochの画像1枚を綺麗に4分割するスクリプト
from PIL import Image
import os
import sys
import glob
from datetime import datetime
import subprocess
import shutil
import yaml

# PATHLIST
# yamlfileのパスのみ変更してください。
with open('/home/ubuntu/repos/F_2110/backend/make_2dimage/config/PathList.yaml', 'r') as yml:
    config = yaml.safe_load(yml)
top = str(config['hierarchy']['top'])
conf_file = str(config['hierarchy']['conf_file'])
demo = str(config['hierarchy']['demo'])
image = str(config['hierarchy']['image'])
imgsplit = str(config['hierarchy']['imgsplit'])
iscript = str(config['hierarchy']['iscript'])
model = str(config['hierarchy']['model'])
output_image = str(config['hierarchy']['output_image'])
script = str(config['hierarchy']['script'])
train_image = str(config['hierarchy']['train_image'])
postgres = str(config['hierarchy']['postgres'])
epoch_1_png = str(config['file']['epoch_1_png'])
epoch_png = str(config['file']['epoch_png'])

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
    # IMAGE_folder
    if os.path.isfile(os.path.join(top, demo,'')) is False:
        print('フォルダにファイルが存在するので再作成します')
        shutil.rmtree(os.path.join(top, demo))
        os.mkdir(os.path.join(top, demo))
    else:
        pass    
    print("--- imageフォルダは空です ---")

    # 4枚全て画像の読み込み
    im = Image.open(os.path.join(top, output_image,'20211028_200545epoch_1000.png'))
    for ig in ImgSplit(im):
        # 保存先フォルダの指定
        ig.save(os.path.join(top, output_image,'20211028_200545epoch_1000.png')+ '_split' + datetime.now().strftime("%Y%m%d_%H%M%S%f_") +".png", "PNG")    