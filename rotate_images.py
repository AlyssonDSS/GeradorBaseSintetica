# Arquivo feito para realizar as rotações nas imagens.
from PIL import Image
import pytesseract
import cv2 as cv
import os
import re

import paths
path_base = paths.path

path_entrada = path_base
path_saida = path_base + r'/saida_rot'
path_dpi = path_saida + r'/dpi'

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def rotate(bin_img, orig_img):
    newdata = pytesseract.image_to_osd(image=bin_img, config='--psm 0 -l por')
    angle = int(re.search('(?<=Rotate: )\d+', newdata).group(0))
    print('-----------------------------------')
    print('Angulo: ' + str(angle))
    print('-----------------------------------')

    if angle == 90:
        rotated = cv.rotate(orig_img, cv.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated = cv.rotate(orig_img, cv.ROTATE_180)
    elif angle == 270:
        rotated = cv.rotate(orig_img, cv.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated = orig_img

    return rotated, angle


def resize_img(img, img_name):
    scale_percent = 2
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)

    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    cv.imwrite(os.path.join(path_dpi, img_name), resized)


def dpi_ajust(img_name):
    im = Image.open(path_dpi + r'/' + img_name)
    im.save(path_dpi + r'/' + img_name, dpi=(500, 500))


def rotate_img(img, img_name):
    check_img = 0  # Checa se a imagem foi realmente rotacionada pelo TESSERACT sem erros de leitura.
    angle = 0
    resize_img(img, img_name)
    dpi_ajust(img_name)

    read_img = cv.imread(path_dpi + r'/' + img_name)

    try:
        new_img, angle = rotate(read_img, img)
        cv.imwrite(os.path.join(path_saida, img_name), new_img)
        check_img = 1

    except:
        print('********************************')
        print('Erro na imagem: ' + img_name)
        print('********************************')

    os.remove(path_dpi + r'/' + img_name)

    return angle, check_img
