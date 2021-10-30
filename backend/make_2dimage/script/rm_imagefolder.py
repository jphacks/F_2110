import os
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings

# PATHの読み込み
top = settings.top
train_image = settings.train_image
image = settings.image

def main():
    # imageフォルダの中身を消去する。（フォルダの消去→再作成）
    print('--------- THIS FILE IS rm_imagefolder.py ---------')
    # IMAGE_folder
    if os.path.isfile(os.path.join(top,image,'')) is False:
        print('フォルダにファイルが存在するので再作成します')
        shutil.rmtree(os.path.join(top,image))
        os.mkdir(os.path.join(top,image))
    else:
        pass    
    print("--- imageフォルダは空です ---")

    # train_imageフォルダの中身を消去する。（フォルダの消去→再作成）
    if os.path.isfile(os.path.join(top, train_image,'')) is False:
        print('フォルダにファイルが存在するので再作成します')
        shutil.rmtree(os.path.join(top,train_image))
        os.mkdir(os.path.join(top,train_image))
    else:
        pass    
    print("--- train_imageフォルダは空です ---")
    print('--------- EOF ---------')
    print('------------------ END OF THIS SERIES IF PROCESSING ------------------')

if __name__ == '__main__':
    main()
