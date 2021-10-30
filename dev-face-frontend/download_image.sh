#!/bin/bash
for ((i=0; i<200; i++)); do
wget -O "app/assets/images/face_image${i}.png" "https://thispersondoesnotexist.com/image"
sleep 1
done
