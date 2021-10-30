import glob
import base64
import os
import psycopg2
import base64
from io import BytesIO
from PIL import Image
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


#DB接続用ステータス設定
path = "localhost"
port = "5432"
dbname = "xxxxxxxx"
user = "xxxxxxxxxx"
password = "xxxxxxxxxxxxx"

def main():
    print('------------------ START OF THIS SERIES IF PROCESSING ------------------')
    print('--------- THIS FILE IS take_img_from_db.py ---------')
    #接続部分
    conText = "host={} port={} dbname={} user={} password={}"
    conText = conText.format(path,port,dbname,user,password)
    connection = psycopg2.connect(conText)
    cur = connection.cursor()

    #DBにデータを保存
    sql = "select id, image from tbl_save_image where user_id='masaru';"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        img_base64 = row[1].rsplit('data:image/png;base64,')[-1]
        
        im = Image.open(BytesIO(base64.b64decode(img_base64)))
        im.save(os.path.join(top, image, '') + str(row[0]) +'_image.png', 'PNG')
        
        print(row[0])
    connection.close()


    print('--------- EOF ---------')


if __name__ == '__main__':
    main()
    exec(open(os.path.join(top,script,"dcgan_model2.py")).read())