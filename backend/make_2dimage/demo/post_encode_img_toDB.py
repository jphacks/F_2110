import glob
import base64
import os
import psycopg2
import base64
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
dbname = "xxxxxxxxxx"
user = "xxxxxxxxxxxxx"
password = "xxxxxxxxxxxx"

def main():
    # ソートしたファイルリストを取得
    images = sorted(glob.glob(os.path.join(top,demo,'demo_train_img/*')))

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
