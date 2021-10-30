# PNGFileをbase64にエンコードして、DBにあっぷする。
import glob
import base64
import os
import psycopg2
import base64
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
demo = settings.demo

def main():
    # ソートしたファイルリストを取得
    images = sorted(glob.glob(os.path.join(top, demo,'demo_train_img/*')))

    for fpath in images:
        # 拡張子なしのファイル名を取得
        filename = os.path.splitext(os.path.basename(fpath))[0]
        print(filename)
        
        file_data = open(fpath, "rb").read()
        b64_data = base64.b64encode(file_data).decode('utf-8')

        #接続部分
        conText = "host={} port={} dbname={} user={} password={}"
        conText = conText.format(path,port,dbname,user,password)
        connection = psycopg2.connect(conText)
        cur = connection.cursor()

        #DBにデータを保存
        sql = "insert into tbl_save_image(user_id,image) values('masaru',%s);"
        #cur.execute(sql)
        cur.execute(sql,(forDB_b64_data,))
        connection.commit()

    print("--- end ---")


if __name__ == '__main__':
    main()
