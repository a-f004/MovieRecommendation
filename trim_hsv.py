# トリミングした予告映像全体における解析

import numpy as np
from matplotlib import pyplot as plt
import os
from sklearn import preprocessing
import function

movie_file='パスの指定'
image_dir='trim_image_dir/'
image_file='img_%s.jpg'
fps = 30


# フォルダの確認・作成
function.confirmation_file_figure()
function.confirmation_file_image_dir(image_dir)

# キャプチャ
function.get_capture(movie_file, image_dir, image_file, fps)

#キャプチャファイル数取得
img_cnt = sum(os.path.isfile(os.path.join(image_dir, name)) for name in os.listdir(image_dir))


#キャプチャファイル数取得
img_cnt = sum(os.path.isfile(os.path.join(image_dir, name)) for name in os.listdir(image_dir))


# HSV 合計取得
b1_sum = g1_sum = r1_sum = h1_sum = s1_sum = v1_sum = 0
for i in range(img_cnt):
    print(i)
    b1,g1,r1,h1,s1,v1 = function.get_img(image_dir + 'img_' + str(i) + '.jpg')
    b1_sum, g1_sum, r1_sum, h1_sum, s1_sum, v1_sum = function.get_img_sum(i, b1, g1, r1, h1, s1, v1, b1_sum, g1_sum, r1_sum, h1_sum, s1_sum, v1_sum)
# HSV平均取得
b1_ave, g1_ave, r1_ave, h1_ave, s1_ave, v1_ave = function.get_img_ave(b1_sum, g1_sum, r1_sum, h1_sum, s1_sum, v1_sum, img_cnt)

# 正規化
b1_ave_mm, g1_ave_mm, r1_ave_mm, h1_ave_mm, s1_ave_mm, v1_ave_mm = function.regularization(b1_ave, g1_ave, r1_ave, h1_ave, s1_ave, v1_ave)

# ヒストグラム表示
function.show_RGBimg(b1_ave_mm, g1_ave_mm, r1_ave_mm)
function.show_HSVimg(h1_ave_mm, s1_ave_mm, v1_ave_mm)


# 色割合取得
all_h, green2, yellow2, green_yellow2 = function.get_hue(h1_ave)
low_saturarion, high_saturation = function.get_saturation(s1_ave)
low_value, high_value = function.get_saturation(v1_ave)

# 割合表示
print('黄色 : ', yellow2*100/all_h, '%')
print('緑色 : ', green2*100/all_h, '%')
print('黄緑 : ', green_yellow2*100/all_h, '%')

print('low saturation : ', low_saturarion, '%')
print('high saturation : ', high_saturation, '%')

print('low value : ', low_value, '%')
print('high value : ', high_value, '%')
