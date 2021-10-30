# epoch画像1枚を4分割し、左上のものだけを格納する
from PIL import Image
import os
import sys
import glob
from datetime import datetime
import subprocess
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
    for h1 in range(1):
        # 横の分割枚数
        for w1 in range(1):
            w2 = w1 * height
            h2 = h1 * width
            print("左上のみ取得する" )
            print(w2, h2, width + w2, height + h2)
            c = im.crop((w2, h2, width + w2, height + h2))
            buff.append(c)
    return buff


print('--------- THIS FILE IS split_image.py ---------')

# epoch_1.pngのファイル名を変更する。ファイル名の頭に「000を」つける
is_file = os.path.isfile(epoch_1_png)
if is_file:
    os.rename(epoch_1_png , os.path.join(top, output_image, '') +'000'+ datetime.now().strftime("%Y%m%d_%H%M%S") + 'epoch_001.png')
else:
    pass
# epochからはじまるファイル名を変更する
# あとでファイル名を昇順にソートするため、各ファイルの頭に日付と時刻をつける。
epoch_files = glob.glob(epoch_png + '*')
datetime_str = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
for f in epoch_files:
    os.rename(f, os.path.join(os.path.join(top, output_image, ''), datetime_str + os.path.basename(f)))

# フォルダ内のファイル名とフォルダ名をリストで出力
output_img_list = os.listdir(os.path.join(top, output_image, ''))
# 昇順にソートし、epoch_1は先頭に、最新の実行時の最後のepochのものが最後に来るようにする。
output_img_list.sort()
# ソートしたものから、最後のものつまり、最新の実行時の最後のepochのものを取得
output_img_latest = output_img_list[-1]

# 確認のため出力
print('学習結果のファイル一覧 : ' + str(output_img_list))
print('一番最後の学習結果 : ' + output_img_latest)
print('--------- EOF ---------')
if __name__ == '__main__':
    # 最新の画像の読み込み
    im = Image.open(os.path.join(top, output_image, '') + output_img_latest)
    for ig in ImgSplit(im):
        # 保存先フォルダの指定
        ig.save(os.path.join(top ,imgsplit, '') + output_img_latest + '_split' +".png", "PNG")
    
    # base64にエンコードしてpostgresqlに格納するスクリプトの呼び出し
    exec(open(os.path.join(top, postgres,"save_img_to_db.py")).read())