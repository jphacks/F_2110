class ResultController < ApplicationController

    def index
        # url = "https://thispersondoesnotexist.com/image"
        # pre_file = "#{Rails.root}/app/assets/images/tmp_image"
        pre_js_file_path = "tmp_image"
        # uri = URI('https://thispersondoesnotexist.com/image')
        # res = Net::HTTP.get_response(uri)
        # puts res.body if res.is_a?(Net::HTTPSuccess)
        image_list = ["#{pre_js_file_path}_1.png"]
        # for i in 1..5 do
        #     file = "#{pre_file}_#{i.to_s}.png"
        #     js_file = "#{pre_js_file_path}_#{i.to_s}.png"
        #     open(file, 'w') do |pass|
        #         open(url) do |recieve|
        #             pass.write(recieve.read.force_encoding(Encoding::UTF_8))
        #             image_list << js_file
        #         end
        #     end
        # end
        # @users = User.where.not(id: current_user.id)
        @users = image_list
        # @user = User.find(current_user.id)
    end

end
