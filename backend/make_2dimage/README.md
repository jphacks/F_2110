# JPHACKS-devface-backendの構築に関して

## 1.環境構築
### 環境に関して
* Ubuntu 20.04
* Python3.7.12
* pip 21.3.5

### pip install するもの
* Python3.7
* tensorflow==1.14
    * [このリンクからインストール](https://github.com/lhelontra/tensorflow-on-arm/releases/tag/v1.14.0-buster)
    *  tensorflow==1.14はpython3.7じゃないと動かない。
* numpy＝1.16.4
    *  tensorflow==1.14はnumpy＝1.16じゃないと動かない。
* tqdm
* matplotlib
* pip install pyyaml
* pillow

### 参考にしたサイト
* Python3.7を入れる
    * [Python3.7 + Pipenv環境をUbuntu18.04 LTSに構築](https://qiita.com/sabaku20XX/items/67eb69f006adbbf9c525)
* styleGAN2ってなんだ？
    * [【簡単】StyleGAN2でアニメキャラの超高解像度生成を試す](https://qiita.com/ichii731/items/23a4b325d7f8c2a78e75)
    * [Ubuntu 20.04 + StyleGAN2 でアニメキャラを生成してみた](https://qiita.com/ysk0832/items/0a2ffe63bdcdcd82548f)
* Tensorflow\==1.14は、numpy\==1.16じゃないと動かない
    * [TensorFlow1.14.0でのFutureWarning （警告）対策](https://zerofromlight.com/blogs/detail/31/)

## 2.STYLEGAN？深層学習？
* **StyleGAN2**
    * [StyleGAN2で属性を指定して顔画像を生成する](https://memo.sugyan.com/entry/2021/04/02/005434) 
    * [StyleGAN2を使って顔画像の編集をやってみる](http://cedro3.com/ai/edit-new-image/)
    * [StyleGANとStyleGAN2を使って美少女キャラを無限増殖させる](https://blog.tubone-project24.xyz/2020/05/03/stylegan2-anime)
    * [今さら聞けないGAN（1）　基本構造の理解](https://qiita.com/triwave33/items/1890ccc71fab6cbca87e)
    * [GANについて概念から実装まで　～DCGANによるキルミーベイベー生成～](https://qiita.com/taku-buntu/items/0093a68bfae0b0ff879d)
* **深層学習に関して**
    * [Kerasにおけるtrain、validation、testについて](https://intellectual-curiosity.tokyo/2019/06/29/keras%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8Btrain%E3%80%81validation%E3%80%81test%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/)
    * [Epoch数とバッチサイズの解説と、変化させた時の精度の変化について確かめる](https://arakan-pgm-ai.hatenablog.com/entry/2017/09/03/080000)
    * [【学習データセット】train、validation、test datasetの違い、使い分け](https://algorithm.joho.info/programming/python/keras-train-validation-test-dataset/)
    * [はじめてのGAN](https://elix-tech.github.io/ja/2017/02/06/gan.html)
## 3.スクリプトの説明
READMEにも記載
### 1. ディレクトリの構成
* 説明
**ディレクトリ**、`ファイル`

---
* **make_2dimage**
    * `.env`
    * `settings. py`
    * `imgb64.js`
    * **config**
        * `PathList.yaml`
        * `config.yaml`
    *  **demo**
        * **demo_train_img**
        * `post_encode_img_toDB. py`
        * `save_epoch1000_toDB. py`
    *  **image**
    *  **imgsplit**
    *  **model**
        * `dcgan_generator.h5`
        * `dcgan_generatorweights.npy`
        * `dcgan_discriminator.h5`
        * `dcgan_discriminatorweights.npy`
    *  **output_image**
    *  **postgres**
        * `save_img_to_db.py`
        * `take_img_from_db.py`
    *  **script**
        * `test_split_image.py`
        * `split_image.py`
        * `rm_image_folder.py`
        * `pngtobase64.py`
        * `dcgan_model2.py`
    *  **train_image**
---

### 2. 各ディレクトリとファイルについて
* `.env`
    * DBのUserName、PW、DBNAMEが記載。
    * gitignoreに.envを記載しているので、Githubにあがることはない。

* `settings. py`
    * DBのUserName、PW、DBNAMEを`.env`ファイルから読み込み、他のPythonスクリプトで利用できるようにしている。
    * `/config/PathList.yaml`を読み込み、各ディレクトリのPATHを定義。他のPythonスクリプトで利用できるようにしている。

* `imgb64.js`
    * `/script/pngtobase64.py`の実行結果（PNGの画像ファイルがbase64にエンコードされ、その時情報(base64)）が記載されている。

* **config**：yamlファイルのディレクトリ。
    * `PathList.yaml`
        * ディレクトリが記載されている。
        * setting.pyで結合されてPATHになる。
        * 自分の環境に応じて適宜修正。ただし、同じディレクトリ構造でないと動かなくなるので、`/make_2dimage`配下は変えないことを前提とする。
    * `config.yaml`
        * `/script/dcgan_model2.py`を実行する際の**epoch**、**Batch**、**dim**を定義。

* **demo**：JPHacksでデモを行う際のスクリプト
    * **demo_train_img**：手動で`tbl_save_image`に格納したい画像置き場。
    * `post_encode_img_toDB.py`
        * **demo_train_img**に入っている全ての画像をbase64にエンコードして`tbl_save_image`に格納する。
    * `save_epoch1000_toDB.py`
        * 問答無用で一番出来がいいあの画像を`tbl_create_image`に格納するためのファイル

* **image**：`tbl_save_image`に格納されている画像を、`/postgres/save_img_to_db.py`によって取得した時の最初の画像保管場所。
  
* **imgsplit**：`/script/split_image.py`を実行し、4分割された画像のうち左上のみが格納されている。
* **model**：`/script/dcgan_model2.py`を実行した際に生成されるモデルが格納される
    * `dcgan_generator.h5`
    * `dcgan_generatorweights.npy`
    * `dcgan_discriminator.h5`
    * `dcgan_discriminatorweights.npy`

* **output_image** ：`/script/dcgan_model2.py`を実行し、出力結果4枚が1枚にまとまった画像が格納される。

* **postgres**：DBに接続する処理があるスクリプト置き場
    * `save_img_to_db.py`
        * **imgsplit**に格納されている写真のうち、最新のものが500×492にreshapeされたのちbase64にエンコードされ、`tbl_create_image`に格納される。
        * 500×492なのは、表示した時に綺麗に画面に収まるので。
        * `/script/split_image.py`が実行されたあとにそのまま実行される。
    * `take_img_from_db.py`
        * `tbl_save_image`に格納されている画像を全て取得し、PNG形式にデコード、**image**に格納される。
        * これをキックすると一連の処理が走る。（3. HOW IT WORKSに記載）

* **script**：
    * `test_split_image.py`
        * 使用していない。（勉強のため残している）
        * **output_image**に格納されている4枚が1枚に結合されている画像を、4分割し、全てに名前をつけて**imgsplit**に保存する。
    * `split_image.py`
        * **output_image**に格納されている4枚が1枚に結合されている画像を、4分割し、左上のものだけ**imgsplit**に名前をつけて保存する。
        * この時、名前に日時を入れることで、最新のものが判別できるようにしている。
        * **output_image**にepoch1が必ず格納されているが、使用しないため、ファイル名の頭に**000**をつけることで、最新のものとして引っかからないようにしている。（ファイル名に日時をつけているので、ソートしたときに、000が頭につくことで最後にならないようにする。最新のファイルはファイル名をlistで表示させ[-1]で取得）
    * `rm_image_folder.py`
        * **image**フォルダと**train_image**フォルダを消去し、新たに作り直す。
        * 毎回`tbl_save_image`にある画像を全て取得し、**image**フォルダに格納し、それらを128×128にリサイズし**train_image**に格納しているため、画像を残しておと、次に実行した際に、同じ画像が複数ある状況が生まれる可能性があるため、フォルダを毎回**image**フォルダと**train_image**フォルダを消去し、新たに作り直す。
        * `/postgres/save_img_to_db.py`が実行されたあとに自動で実行。
    * `pngtobase64.py`
        * DBがない環境で、`/script/dcgan_model2.py`を実行→`/script/split_image.py`を実行した際に、**imgsplit**にある最新の画像をbase64にエンコードし、`imgb64.js`に記載。(毎回上書き) 
    * `dcgan_model2.py`
        *　メインのコード
        *　**image**フォルダにある画像を128×128のPNGファイルにreshapeし、**train_image**フォルダに格納。
        * generator(fakeを作成)とdiscriminator(realかfakeを見分ける)を作成
        * combinedモデルを作成。
        * 学習を行う。epoch数、Batchsizeなどは`/config/config.yaml`に記載しているので、変更する際は`/config/config.yaml`を修正する。
        * 学習した結果4枚を1枚にまとめて、`output_image`に格納

*  **train_image**：`/postgres/take_img_from_db.py`の実行により**image**に保存された画像が、`/scripts/dcgan_model2.py`の実行によって、128×128のPNGにreshapeされ、保存される場所。

### 3. HOW IT WORKS

`python3.7 take_img_from_db.py`により、あとは自動でスクリプトが実行されていく。

**実行の順番**
1.　スクリプト：`/postgres/take_img_from_db.py`
DBからユーザ(user_id=masaru)がLikeした画像を全て取得し、PNGにエンコードして、**image**フォルダに格納。
2. `/script/dcgan_model2.py`
**image**フォルダに格納された画像を128×128にreshapeし、**image_train**フォルダに格納。画像をもとに学習し、epoch回数が100で割り切れる数字のものだけを**output_image**フォルダに保存。
3. `/script/split_image.py`
**output_image**にある画像が4枚で1枚になっているので、4当分し、左上の画像のみを、**img_split**フォルダに保存。
4. `/postgres/save_img_to_db.py`
**imgsplit**フォルダにある画像の中で最新のものを、500×492nいreshapeし、base64にエンコードし、DBのtbl_create_imageにuser_id=masaruで格納（UPSERT）する。
5. `/script/rm_image_folder.py`
**train_image**フォルダと、**image**フォルダを一度削除し、同じ名前で再度作る。

### 4. 改善点
* `dcgan_model2.py`を実行した際に、4枚が1枚となって出力されているので、それを1枚ずつにしたい。→`split_image.py`が不要になる
* 現状最新のものを取得する際に、epoch数3桁までのものでしか取得できないので、epoch数の桁に関わらず最新のものが取得できるようにする。(list.sort()したとき、名前順だと、[1000.png, 500.png 900.png］という順番になってしまい、最新が900と判定されてしまう)