Rails.application.routes.draw do
  devise_for :users
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
  
  #get 'top/index'
  root 'top#index'

  resources :users, only: [:index]
  resources :result, only: [:index]
  
end
