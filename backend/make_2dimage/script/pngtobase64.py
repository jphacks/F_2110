# このファイルは使用してません
# -*- coding:utf-8 -*-
# pngfileをbase64にして、img_b64.jsに書き込む
# 1枚のみ。下に複数版が記載。

import glob
import base64
import os
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

# メイン関数
def main():
    # フォルダ内にあるデータから、一番最新のものをとってくる。
    last_img = os.listdir(os.path.join(top, imgsplit,''))
    last_img.sort()
    last_img_name = last_img[-1]

    # 画像をリサイズ
    img = Image.open(os.path.join(top, imgsplit,last_img_name))
    img_resize = img.resize((500, 492))
    img_resize.save(os.path.join(top, imgsplit,last_img_name))

    f = open(os.path.join(top, 'img_b64.js'), 'w')

    # 拡張子なしのファイル名を取得
    filename = os.path.splitext(os.path.basename(last_img_name))[0]
    print(filename)

    # ファイルにbase64の内容を書き込む
    f.write("const " + filename + "_B64 = \"data:image/png;base64,")
    file_data = open(os.path.join(top, imgsplit,'') + last_img_name, "rb").read()
    b64_data = base64.b64encode(file_data).decode('utf-8')
    f.write(b64_data)
    f.write("\";\n")
    
    f.close()
    print("--- end ---")


if __name__ == '__main__':
    main()

# フォルダの中身を全てbase64にする
'''
    # ソートしたファイルリストを取得
    images = sorted(glob.glob(IMG_FOLDER_PATH))

    f = open(SAVE_FILE_PATH, 'w')


    for fpath in images:
        # 拡張子なしのファイル名を取得
        filename = os.path.splitext(os.path.basename(fpath))[0]
        print(filename)
        
        # ファイルにbase64の内容を書き込む
        f.write("const " + filename + "_B64 = \"data:image/png;base64,")
        file_data = open(fpath, "rb").read()
        b64_data = base64.b64encode(file_data).decode('utf-8')
        f.write(b64_data)
        f.write("\";\n")

    f.close()
    print("--- end ---")
'''