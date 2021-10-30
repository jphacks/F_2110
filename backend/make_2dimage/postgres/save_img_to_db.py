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
dbname = "xxxx"
user = "xxxxxxx"
password = "xxxxxxxx"


def main():
    print('--------- THIS FILE IS save_img_to_db.py ---------')
    # フォルダ内にあるデータから、一番最新のものをとってくる。
    last_img = os.listdir(os.path.join(top,imgsplit,''))
    # 昇順にソート→最新のものが一番後ろにくる。
    last_img.sort()
    # リストの最後のものを取ってくる
    last_img_name = str(last_img[-1])
    print('学習結果のファイル一覧 : ' + str(last_img))
    print('分割済みの学習結果一覧 : ' + last_img_name)

    # 画像をリサイズ
    img = Image.open(os.path.join(top, imgsplit,last_img_name))
    img_resize = img.resize((500, 492))
    img_resize.save(os.path.join(top, imgsplit,last_img_name))

    # 拡張子なしのファイル名を取得
    filename = os.path.splitext(os.path.basename(last_img_name))[0]

    # ファイルにbase64の内容を書き込む
    file_data = open(os.path.join(top,imgsplit,'') + last_img_name, "rb").read()
    b64_data = base64.b64encode(file_data).decode('utf-8')
    b64_data = 'data:image/png;base64,' + b64_data


    #接続部分
    conText = "host={} port={} dbname={} user={} password={}"
    conText = conText.format(path,port,dbname,user,password)
    connection = psycopg2.connect(conText)
    cur = connection.cursor()

    #DBにデータを保存
    sql = "insert into tbl_create_image(user_id,image) values('masaru',%s) on conflict (user_id) do update set image=%s;"
    cur.execute(sql,(b64_data,b64_data,))
    connection.commit()

    print('--------- EOF ---------')


if __name__ == '__main__':
    main()
    exec(open(os.path.join(top,script,"rm_imagefolder.py")).read())

# DBの接続時における%sの使い方
'''
sql = "INSERT INTO TEST_TABLE (filename, data1, data2) VALUES(%s, %s ,%s);"
cur.execute(sql, (filename, indata1, indata2))
'''
