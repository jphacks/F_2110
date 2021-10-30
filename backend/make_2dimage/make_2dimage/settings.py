import yaml
from collections import UserList
import os
from os.path import join, dirname
from dotenv import load_dotenv

# .envの読み込み
load_dotenv(verbose=True)
dotenv_path="/home/ubuntu/repos/F_2110/.env"
load_dotenv(dotenv_path)

# DB接続設定
DBNAME = os.environ.get("DB_NAME")
USER = os.environ.get('PG_USER')
PW = os.environ.get('PG_PW')


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