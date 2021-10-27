# encoding: UTF-8
require 'open-uri'
# url = "https://thispersondoesnotexist.com/image"
# pre_file = "#{Rails.root}/app/assets/tmp/tmp_image"
# pre_js_file_path = "/javascript/tmp/tmp_image"

class UsersController < ApplicationController
    def show
        @user = User.find(params[:id])
    end

    def index
        # url = "https://thispersondoesnotexist.com/image"
        # pre_file = "#{Rails.root}/app/assets/images/face_image"
        pre_js_file_path = "face_image"
        randam_num = [*(0..9)]
        randam_num = randam_num.sort_by{rand}
        image_list = []
        for i in 0..4 do
            # file = "#{pre_file}_#{i.to_s}.png"
            js_file = "#{pre_js_file_path}#{randam_num[i].to_s}.png"
            image_list << js_file
            # open(file, 'w') do |pass|
            #     open(url) do |recieve|
            #         pass.write(recieve.read.force_encoding(Encoding::UTF_8))
            #         image_list << js_file
            #     end
            # end
        end
        @users = image_list
    end

end
