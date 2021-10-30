# encoding: UTF-8
require 'open-uri'

class UsersController < ApplicationController
    def show
        @user = User.find(params[:id])
    end

    def index
        pre_js_file_path = "_image.png"
        randam_num = [*(1..12)]
        randam_num = randam_num.sort_by{rand}
        image_list = []
        for i in 0..3 do
            js_file = "#{pre_js_file_path}#{randam_num[i].to_s}.png"
            image_list << js_file
        end
        @users = image_list
    end

end
