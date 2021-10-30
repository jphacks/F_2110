import os
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


def main():
    print('--------- THIS FILE IS rm_imagefolder.py ---------')
    # IMAGE_folder
    if os.path.isfile(os.path.join(top,image,'')) is False:
        print('フォルダにファイルが存在するので再作成します')
        shutil.rmtree(os.path.join(top,image))
        os.mkdir(os.path.join(top,image))
    else:
        pass    
    print("--- imageフォルダは空です ---")

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
