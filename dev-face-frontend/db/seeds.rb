# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

p "create Users"
User.create!(
  email: 'user1@gmail.com',
  password: '11111111',
  name: 'エマ',
  self_introduction: '音楽と猫と美味しいものが好き！',
  gender: 1,
  profile_image: open("/Users/h-suga/Documents/dev/jphacks/techpit-match_v3/db/dummy_images/1.jpg")
)
User.create!(
  email: 'user2@gmail.com',
  password: '11111111',
  name: 'オリビア',
  self_introduction: 'クリエイターさんと話してみたい。',
  gender: 1,
  profile_image: open("/Users/h-suga/Documents/dev/jphacks/techpit-match_v3/db/dummy_images/2.jpg")
)
User.create!(
  email: 'user3@gmail.com',
  password: '11111111',
  name: 'エヴァ',
  self_introduction: 'プロフィールをご覧いただきありがとうございます。東京でWebマーケティング関連の仕事をしています。',
  gender: 1,
  profile_image: open("/Users/h-suga/Documents/dev/jphacks/techpit-match_v3/db/dummy_images/3.jpg")
)
User.create!(
  email: 'user4@gmail.com',
  password: '11111111',
  name: 'ノア',
  self_introduction: '東京で美容師をしています。',
  gender: 0,
  profile_image: open("/Users/h-suga/Documents/dev/jphacks/techpit-match_v3/db/dummy_images/4.jpg")
)
User.create!(
  email: 'user5@gmail.com',
  password: '11111111',
  name: 'リアム',
  self_introduction: '普段は公認会計士として働いています',
  gender: 0,
  profile_image: open("/Users/h-suga/Documents/dev/jphacks/techpit-match_v3/db/dummy_images/5.jpg")
)
User.create!(
  email: 'user6@gmail.com',
  password: '11111111',
  name: 'オリバー',
  self_introduction: '週3日くらい1人ラーメンします',
  gender: 0,
  profile_image: open("/Users/h-suga/Documents/dev/jphacks/techpit-match_v3/db/dummy_images/6.jpg")
)
