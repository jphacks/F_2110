import base64
import os
import psycopg2
import base64
from io import BytesIO
from PIL import Image
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings

# PATH読み込み
top = settings.top
script = settings.script
image = settings.image

#DB接続用ステータス設定
path = "localhost"
port = "5432"
dbname = settings.DBNAME
user = settings.USER
password = settings.PW

def main():
    print('------------------ START OF THIS SERIES IF PROCESSING ------------------')
    print('--------- THIS FILE IS take_img_from_db.py ---------')
    #DBへの接続部分
    conText = "host={} port={} dbname={} user={} password={}"
    conText = conText.format(path,port,dbname,user,password)
    connection = psycopg2.connect(conText)
    cur = connection.cursor()

    #DBにデータを保存
    sql = "select id, image from tbl_save_image where user_id='masaru';"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        # 左側についている'data:image/png;base64,'を除去
        img_base64 = row[1].rsplit('data:image/png;base64,')[-1]
        # base64をPNGにデコードして、保存
        im = Image.open(BytesIO(base64.b64decode(img_base64)))
        im.save(os.path.join(top, image, '') + str(row[0]) +'_image.png', 'PNG')
    connection.close()


    print('--------- EOF ---------')


if __name__ == '__main__':
    main()
    # dcgan_model2.pyを走らせる。
    exec(open(os.path.join(top,script,"dcgan_model2.py")).read())