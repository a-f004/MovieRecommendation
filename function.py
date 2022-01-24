import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import shutil
from sklearn import preprocessing

# 正規化
def regularization(b1_ave, g1_ave, r1_ave, h1_ave, s1_ave, v1_ave):
    mm = preprocessing.MinMaxScaler()
    b1_ave_mm = mm.fit_transform(b1_ave)
    g1_ave_mm = mm.fit_transform(g1_ave)
    r1_ave_mm = mm.fit_transform(r1_ave)
    h1_ave_mm = mm.fit_transform(h1_ave)
    s1_ave_mm = mm.fit_transform(s1_ave)
    v1_ave_mm = mm.fit_transform(v1_ave)
    return b1_ave_mm, g1_ave_mm, r1_ave_mm, h1_ave_mm, s1_ave_mm, v1_ave_mm

# RGB, HSV要素取得
def get_img(path):
    img = cv2.imread(path)
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
    hist_b = cv2.calcHist([b],[0],None,[256],[0,256])
    hist_g = cv2.calcHist([g],[0],None,[256],[0,256])
    hist_r = cv2.calcHist([r],[0],None,[256],[0,256])
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = img2[:,:,0], img2[:,:,1], img2[:,:,2]
    hist_h = cv2.calcHist([h],[0],None,[256],[0,256])
    hist_s = cv2.calcHist([s],[0],None,[256],[0,256])
    hist_v = cv2.calcHist([v],[0],None,[256],[0,256])
    return hist_b, hist_g, hist_r, hist_h, hist_s, hist_v

# RGBプロット
def show_RGBimg(b1_ave_mm, g1_ave_mm, r1_ave_mm):
    plt.plot(b1_ave_mm, color='r', label="b")
    plt.plot(g1_ave_mm, color='b', label="g")
    plt.plot(r1_ave_mm, color='g', label="r")
    plt.legend()
    plt.savefig('figure/RGBfigure' + str(1) + '.png')
    # plt.show() 
    plt.clf()
    print('完了1')

# HSVプロット
def show_HSVimg(h1_ave_mm, s1_ave_mm, v1_ave_mm):
    plt.plot(h1_ave_mm, color='r', label="h")
    plt.plot(s1_ave_mm, color='b', label="s")
    plt.plot(v1_ave_mm, color='g', label="v")
    plt.legend()
    plt.savefig('figure/HSVfigure' + str(1) + '.png')
    plt.show() 
    plt.clf()
    print('完了2')

# フォルダの確認・作成
def confirmation_file_figure():
    #ファイルが存在してるか確認
    if os.path.exists('figure/'):
        shutil.rmtree('figure/')

    #ファイルが存在してなかったら作る
    if not os.path.exists('figure/'):
        os.makedirs('figure/')

def confirmation_file_image_dir(image_dir):
    #ファイルが存在してるか確認
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)

    #ファイルが存在してなかったら作る
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

# キャプチャ
def get_capture(movie_file, image_dir, image_file, fps):
    i = 0
    count = 0
    cap = cv2.VideoCapture(movie_file)
    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret == False:
            break

        if count % fps == 0:
            cv2.imwrite(image_dir + image_file % str(i), frame)  # Save a frame
            print('Save', image_dir + image_file % str(i))
            i += 1
        count = count + 1
    cap.release()

# HSV 合計取得
def get_img_sum(i, b1, g1, r1, h1, s1, v1, b1_sum, g1_sum, r1_sum, h1_sum, s1_sum, v1_sum):
    b1_np = np.array(b1)
    g1_np = np.array(g1)
    r1_np = np.array(r1)
    h1_np = np.array(h1)
    s1_np = np.array(s1)
    v1_np = np.array(v1)

    if i == 0:
        b1_sum = np.zeros_like(b1_np)
        g1_sum = np.zeros_like(g1_np)
        r1_sum = np.zeros_like(r1_np)
        h1_sum = np.zeros_like(h1_np)
        s1_sum = np.zeros_like(s1_np)
        v1_sum = np.zeros_like(v1_np)
        
    b1_sum = np.add(b1_sum, b1_np)
    g1_sum = np.add(g1_sum, g1_np)
    r1_sum = np.add(r1_sum, r1_np)
    h1_sum = np.add(h1_sum, h1_np)
    s1_sum = np.add(s1_sum, s1_np)
    v1_sum = np.add(v1_sum, v1_np)
    
    return b1_sum, g1_sum, r1_sum, h1_sum, s1_sum, v1_sum

# HSV 平均取得
def get_img_ave(b1_sum, g1_sum, r1_sum, h1_sum, s1_sum, v1_sum, img_cnt):
    b1_ave = b1_sum/img_cnt
    g1_ave = g1_sum/img_cnt
    r1_ave = r1_sum/img_cnt
    h1_ave = h1_sum/img_cnt
    s1_ave = s1_sum/img_cnt
    v1_ave = v1_sum/img_cnt

    return b1_ave, g1_ave, r1_ave, h1_ave, s1_ave, v1_ave

# 色相割合取得
def get_hue(h1_ave):
    all_h = np.sum(h1_ave)

    j = 0
    green = 0
    for j in range(6):
        green += h1_ave[j + 58]
    green2 = green[0]

    j = 0
    yellow = 0
    for j in range(6):
        yellow += h1_ave[j + 28]
    yellow2 = yellow[0]

    j = 0
    green_yellow = 0
    for j in range(6):
        green_yellow += h1_ave[j + 43]
    green_yellow2 = green_yellow[0]

    return all_h, green2, yellow2, green_yellow2

# 彩度割合取得
def get_saturation(s1_ave):
    all_s = np.sum(s1_ave)
    j = 0
    saturation_l = 0
    for j in range(127):
        saturation_l += s1_ave[j + 1]
    saturation_l2 = saturation_l[0]
    # print('low saturation : ', saturation_l2*100/all_s, '%')

    j = 0
    saturation_h = 0
    for j in range(127):
        saturation_h += s1_ave[j + 128]
    saturation_h2 = saturation_h[0]
    # print('high saturation : ', saturation_h2*100/all_s, '%')

    return saturation_l2*100/all_s, saturation_h2*100/all_s

# 明度割合取得
def get_value(v1_ave):
    all_v = np.sum(v1_ave)
    j = 0
    value_l = 0
    for j in range(127):
        value_l += v1_ave[j + 1]
    value_l2 = value_l[0]
    # print('low value : ', value_l2*100/all_v, '%')

    j = 0
    value_h = 0
    for j in range(127):
        value_h += v1_ave[j + 128]
    value_h2 = value_h[0]
    # print('high value : ', value_h2*100/all_v, '%')

    return value_l2*100/all_v, value_h2*100/all_v