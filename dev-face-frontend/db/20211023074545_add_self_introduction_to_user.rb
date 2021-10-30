class AddSelfIntroductionToUser < ActiveRecord::Migration[6.1]
  def change
    add_column :users, :self_introduction, :text
  end
end
