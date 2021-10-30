# pngfileをbase64にして、img_b64.jsに書き込む
# 1枚のみ。下に複数版が記載。

import glob
import base64
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings

# PATH読み込み
top = settings.top
imgsplit = settings.imgsplit

# メイン関数
def main():
    print('--------- THIS FILE IS pngtobase64.py ---------')
    # フォルダ内にあるデータから、一番最新のものをとってくる。
    # imgsplitフォルダ配下からのファイルを全て取得してリストにする。
    last_img = os.listdir(os.path.join(top, imgsplit,''))
    # 昇順になるように並び替える
    last_img.sort()
    # 一番最新のものを持ってくる。（昇順に並べられてるので、最新のものは最後尾。）
    last_img_name = last_img[-1]

    # 'img_b64.js'ファイルに書き込む。
    f = open(os.path.join(top, 'img_b64.js'), 'w')

    # 拡張子なしのファイル名を取得
    filename = os.path.splitext(os.path.basename(last_img_name))[0]

    # ファイルにbase64にしたものを書き込む
    f.write("const " + filename + "_B64 = \"data:image/png;base64,")
    file_data = open(os.path.join(top, imgsplit,'') + last_img_name, "rb").read()
    b64_data = base64.b64encode(file_data).decode('utf-8')
    f.write(b64_data)
    f.write("\";\n")
    
    f.close()
    print('--------- EOF ---------')


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