# Demo用。デモ用の結果画像をとりあえずDBに格納する。
import glob
import base64
import os
import psycopg2
import base64
import yaml
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings

#DB接続用ステータス設定
path = "localhost"
port = "5432"
dbname = settings.DBNAME
user = settings.USER
password = settings.PW

# PATH読み込み
top = settings.top
imgsplit = settings.imgsplit

EPOCH_1000_IMG = '20211028_200545epoch_1000.png_split.png'


def main():
  
    # 拡張子なしのファイル名を取得
    filename = os.path.splitext(os.path.basename(EPOCH_1000_IMG))[0]
    print(filename)

    # ファイルにbase64の内容を書き込む
    file_data = open(os.path.join(top, imgsplit,'') + EPOCH_1000_IMG, "rb").read()
    b64_data = base64.b64encode(file_data).decode('utf-8')
    

    #接続部分
    conText = "host={} port={} dbname={} user={} password={}"
    conText = conText.format(path,port,dbname,user,password)
    connection = psycopg2.connect(conText)
    cur = connection.cursor()

    #DBにデータを保存
    sql = "insert into tbl_create_image(user_id,image) values('masaru',%s) on conflict (user_id) do update set image=%s;"
    cur.execute(sql,(b64_data,b64_data,))
    connection.commit()

    print("--- end ---")


if __name__ == '__main__':
    main()
