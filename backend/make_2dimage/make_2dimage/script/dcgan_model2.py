from tensorflow.keras.layers import Input, Dense, Reshape, Flatten, Dropout
from tensorflow.keras.layers import BatchNormalization, Activation, ZeroPadding2D, LeakyReLU, UpSampling2D, Conv2D
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import yaml
from tqdm import tqdm
import numpy as np
from pathlib import Path
from PIL import Image
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings

# PATH読み込み
top = settings.top
conf_file = settings.conf_file
image = settings.image
model = settings.model
output_image = settings.output_image
script = settings.script
train_image = settings.train_image

#　画像サイズの指定
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128


class DCGANModel:
    def __init__(self):
        self.config = Config()
        if self.config.reshape:
            self.reshape()
        self.dataset = DataSet()
        self.X_train = self.dataset.X_train

        #　入力画像サイズ
        self.shape = (IMAGE_WIDTH, IMAGE_HEIGHT, 3)
        
        self.discriminator = self.build_discriminator()
        self.generator = self.build_generator()

        d_optimizer = Adam(lr=1e-5, beta_1=0.1)
        g_optimizer = Adam(lr=2e-4, beta_1=0.5)

        # DiscriminatorはRealかFakeを見分ける二値分類を行うためbinary_crossentropy
        self.discriminator.compile(loss='binary_crossentropy', optimizer=d_optimizer, metrics=['accuracy'])
        # discriminatorの重みを固定(dcganの中のみ)
        self.discriminator.trainable = False

        # G は入力としてノイズを受け取り画像を生成
        z = Input(shape=(self.config.z_dim,))
        img = self.generator(z)

        # D は入力として生成画像を受け取り、真偽を判定
        valid = self.discriminator(img)

        # combined_model(Generatorの学習用モデル）も二値分類を行うためbinary_crossentropy
        self.combined = Model(z, valid)
        self.combined.compile(loss='binary_crossentropy', optimizer=g_optimizer)
    
    def build_generator(self):
        noise_shape = (self.config.z_dim,)

        model = Sequential()

        model.add(Dense(128 * int(IMAGE_WIDTH/4) * int(IMAGE_HEIGHT/4), activation="relu", input_shape=noise_shape))
        model.add(Reshape((int(IMAGE_WIDTH/4), int(IMAGE_HEIGHT/4), 128)))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(128, kernel_size=3, padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(UpSampling2D())
        model.add(Conv2D(64, kernel_size=3, padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(3, kernel_size=3, padding="same"))
        model.add(Activation("tanh"))

        model.summary()

        noise = Input(shape=noise_shape)
        img = model(noise)

        return Model(noise, img)

    def build_discriminator(self):
        img_shape = self.shape

        model = Sequential()

        model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=img_shape, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
        model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        img = Input(shape=img_shape)
        validity = model(img)

        return Model(img, validity)

    def build_combined(self):
        self.discriminator.trainable = False
        model = Sequential([self.generator, self.discriminator])
        return model

    def train(self):
        half_batch = int(self.config.batch_size / 2)
        real_label = np.ones((half_batch, 1))
        fake_label = np.zeros((half_batch, 1))
        print('start train')
        num_batches = int(self.X_train.shape[0] / half_batch)
        for epoch in range(self.config.epochs):
            # 合計値(total)を設定
            bar = tqdm(total = num_batches)
            # 説明文を追加
            bar.set_description('Epoch [{0}/{1}]'.format(epoch, self.config.epochs))
            for idx in range(num_batches):
                # ------------------
                # Training Discriminator
                # -----------------
                # 訓練で使用する real 画像をランダムに選び出す
                imgs = self.X_train[idx*half_batch : (idx+1)*half_batch]

                # サンプルノイズを用意してから、そのノイズを元に generator で fake 画像を生成
                noise = np.random.uniform(-1, 1, (half_batch, self.config.z_dim))
                gen_imgs = self.generator.predict(noise)

                # discriminator を訓練（real 画像のラベルを 1、fake 画像のラベルは 0
                d_loss_real = self.discriminator.train_on_batch(imgs, real_label)
                d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake_label)

                d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                # -----------------
                # Training Generator
                # -----------------

                # generator を訓練（discriminator が generator の生成画像を誤って real 1 と判定するように訓練される）
                g_loss = self.combined.train_on_batch(noise, real_label)
                bar.update(1)
                #print("epoch: %d, batch: %d, g_loss: %f, d_loss: %f" % (epoch, idx, g_loss, d_loss))
            bar.close()

            # 訓練の途中経過を出力
            #print("[Discriminator loss: %f, acc.: %.2f%%] [Generator loss: %f]" % (d_loss[0], 100 * d_loss[1], g_loss))

            # 生成画像を保存
            if epoch == 0 or epoch % 100 == 99:
                noise = np.random.uniform(-1, 1, (half_batch, self.config.z_dim))
                gen_imgs = self.generator.predict(noise)
                self.combine_images(os.path.join(top, output_image,''), gen_imgs, epoch)
                # 訓練途中のモデルの重みを保存
                gen_weights = self.generator.get_weights()
                dis_weights = self.discriminator.get_weights()
                np.save(os.path.join(top, model, '', 'dcgan_generator_weights'), gen_weights)
                np.save(os.path.join(top, model, '', 'dcgan_discriminator_weights'), dis_weights)

        # モデルを保存
        self.save_model()

    def reshape(self):
        file_list = os.listdir(os.path.join(top, image, ''))
        for idx, img_file in enumerate(file_list):
            img = Image.open(os.path.join(top, image, '', img_file))
            img_resize = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            img_resize.save(os.path.join(top, train_image,'', '{}.png'.format(idx)))

    def combine_images(self, img_dir, gen_imgs, epoch):
        r, c = 2, 2
        # Rescale images 0 - 1
        gen_imgs = 0.5 * gen_imgs + 0.5

        fig, axs = plt.subplots(r, c)
        fig.subplots_adjust(wspace=0.1, hspace=0.1)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[i,j].imshow(gen_imgs[cnt, :,:,:])
                axs[i,j].axis('off')
                cnt += 1
        fig.savefig(os.path.join(img_dir, "epoch_%d"%(epoch+1)), bbox_inches='tight')
        plt.close()

    def save_model(self):
        model_dir = Path(os.path.join(top, model, ''))
        model_dir.mkdir(exist_ok=True)
        self.generator.save(os.path.join(top, model, '', 'dcgan_generator.h5'))
        self.discriminator.save(os.path.join(top, model, '', 'dcgan_discriminator.h5'))


class DataSet:
    def __init__(self):
        self._X_train = self.load_img()

    def load_img(self):
        img_list = os.listdir(os.path.join(top, train_image,''))
        X_train = []
        for img in img_list:
            img = img_to_array(load_img(os.path.join(top,train_image,'') +img, target_size=(128,128,3)))
            # -1から1の範囲に正規化
            img = (img.astype(np.float32) - 127.5)/127.5
            X_train.append(img)
        # 4Dテンソルに変換(データの個数, 128, 128, 3)
        X_train = np.array(X_train)
        return X_train

    def load_label(self):
        pass

    @property
    def X_train(self):
        return self._X_train


class Config:
    def __init__(self):
        f = open(os.path.join(top, conf_file, 'config.yaml'), 'r+')
        self._yaml_dictionary = yaml.load(f, Loader=yaml.SafeLoader)

    @property
    def input_dictionary(self):
        """input yaml dictionary
        return:
            <dictionary>
        """
        return self._yaml_dictionary

    @property
    def epochs(self):
        return self._yaml_dictionary['epochs']

    @property
    def batch_size(self):
        return self._yaml_dictionary['batch_size']

    @property
    def z_dim(self):
        return self._yaml_dictionary['z_dim']

    @property
    def reshape(self):
        return self._yaml_dictionary['reshape']


if __name__ == '__main__':
    dcgan = DCGANModel()
    dcgan.train()
    print('--------- EOF ---------')
    exec(open(os.path.join(top, script,"split_image.py")).read())



