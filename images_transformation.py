# Arquivo que faz o data augmentation da imagem gerada.
from PIL import Image, ImageEnhance
import numpy as np
import cv2 as cv
import random
import paths
import os

import text_2_image

path_base = paths.path
path_entrada = path_base + r'/reboot'
path_saida = path_entrada

json_original = 'via_export_json.json'


def rotate_bound(img_name):
    img = cv.imread(path_entrada + r'/' + img_name)
    random.seed()
    angle = random.randint(0, 360)
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    rotated = cv.warpAffine(img, M, (nW, nH))
    cv.imwrite(os.path.join(path_saida, img_name), rotated)
    return rotated


def motion_blur(img):
    kernel_size = 3

    # Cria um kernel vertical.
    kernel_v = np.zeros((kernel_size, kernel_size))
    kernel_v[:, int((kernel_size - 1) / 2)] = np.ones(kernel_size)

    # Normaliza.
    kernel_v /= kernel_size

    # Aplica o kernel
    vertical_mb = cv.filter2D(img, -1, kernel_v)
    return vertical_mb


def rand_rotation(img_name, path_img):
    img = cv.imread(path_img + r'/' + img_name)
    random.seed()
    pos_angle = [0, 90, 180, 270]
    sel_num = random.randint(0, 3)
    angle = pos_angle[sel_num]

    v_blur = random.randint(0, 9)
    if v_blur >= 8:
        img = motion_blur(img)

    if angle == 90:
        rotated = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated = cv.rotate(img, cv.ROTATE_180)
    elif angle == 270:
        rotated = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated = img

    cv.imwrite(os.path.join(path_img, img_name), rotated)
    return angle


def rgb_noise(img_name, area_n_text):
    img = cv.imread(path_entrada + r'/' + img_name + '.jpg')
    random.seed()
    sel_blue = 0

    random.seed()
    sel_green = 0

    random.seed()
    sel_red = 20

    blue_img, green_img, red_img = cv.split(img)

    y = blue_img.shape[0]
    x = blue_img.shape[1]

    for j in range(y):
        for i in range(x):
            blue_img[j][i] = blue_img[j][i] + sel_blue
            green_img[j][i] = green_img[j][i] + sel_green
            red_img[j][i] = red_img[j][i] + sel_red

    img = cv.merge((blue_img, green_img, red_img))

    new_img_name = 'rgb_' + img_name
    cv.imwrite(os.path.join(path_saida, new_img_name + '.jpg'), img)

    angle = rand_rotation(new_img_name + '.jpg', path_saida)
    text_2_image.write_txt_file(new_img_name, area_n_text, angle)


def gaussian_noise(img_name, area_n_text):
    img = cv.imread(path_entrada + r'/' + img_name+'.jpg')
    gauss = np.random.normal(0, 1, img.size)
    gauss = gauss.reshape((img.shape[0], img.shape[1], img.shape[2])).astype('uint8')

    # Add the Gaussian noise to the image
    img_gauss = cv.add(img, gauss)

    new_img_name = text_2_image.create_img_name()
    cv.imwrite(os.path.join(path_saida, new_img_name + '.jpg'), img_gauss)

    angle = rand_rotation(new_img_name+'.jpg', path_saida)
    text_2_image.write_txt_file(new_img_name, area_n_text, angle)


def contrast(img_name, factor, area_n_text):
    im = Image.open(path_entrada + r'/' + img_name + '.jpg')
    enhancer_ctr = ImageEnhance.Contrast(im)

    im_output_ctr = enhancer_ctr.enhance(factor)
    new_img_name = text_2_image.create_img_name()
    im_output_ctr.save(path_saida + r'/' + new_img_name + '.jpg')
    angle = rand_rotation(new_img_name + '.jpg', path_saida)
    text_2_image.write_txt_file(new_img_name, area_n_text, angle)


def brightness(img_name, factor, area_n_text):
    im = Image.open(path_entrada + r'/' + img_name + '.jpg')
    enhancer_brig = ImageEnhance.Brightness(im)

    im_output_brig = enhancer_brig.enhance(factor)
    new_img_name = text_2_image.create_img_name()
    im_output_brig.save(path_saida + r'/' + new_img_name + '.jpg')
    angle = rand_rotation(new_img_name + '.jpg', path_saida)
    text_2_image.write_txt_file(new_img_name, area_n_text, angle)


def ctr_brg(img_name, area_n_text, tipo_doc):
    random.seed()
    factor = round(random.uniform(0.5, 0.9), 2)
    contrast(img_name, factor, area_n_text)

    random.seed()
    factor = round(random.uniform(0.5, 0.9), 2)
    brightness(img_name, factor, area_n_text)

    random.seed()
    factor = 1 + round(random.uniform(0.1, 0.3), 2)
    contrast(img_name, factor, area_n_text)

    if tipo_doc != 'RG':
        random.seed()
        factor = 1 + round(random.uniform(0.1, 0.3), 2)
        brightness(img_name, factor, area_n_text)


def augmentation(new_img_name, area_n_text, tipo_doc):
    gaussian_noise(new_img_name, area_n_text)
    ctr_brg(new_img_name, area_n_text, tipo_doc)



