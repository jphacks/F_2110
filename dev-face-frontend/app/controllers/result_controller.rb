class ResultController < ApplicationController

    def index
        pre_js_file_path = "face_image"
        image = "#{pre_js_file_path}#{rand(10).to_s}.png"
        @user = image
    end

end
