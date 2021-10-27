#!/bin/sh
for ((i=0; i<10; i++)); do
wget -O "app/assets/images/face_image${i}.png" "https://thispersondoesnotexist.com/image"
sleep 1
done
