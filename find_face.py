# Detecção e blur do rosto presente nos documentos solicitados.
from PIL import Image, ImageFilter
import image_slicer
import cv2 as cv
import dlib
import os

dnn = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")  # Detector pré-treinado.

path_input = r'./input'
path_rot = r'./rot'
path_tiles = r'./tiles'
path_output = r'./output'
path_result = r'./results'


def detect_face_cnn(orig_img, file_name, angle, pos_x, pos_y):
    shape_x, shape_y = orig_img.size

    tile_name = str(file_name)
    img = cv.imread(os.path.join(path_tiles, tile_name))

    gray = cv.imread(os.path.join(path_tiles, tile_name), 0)
    rects = dnn(gray, 1)

    for (i, rect) in enumerate(rects):
        x1 = rect.rect.left()
        y1 = rect.rect.top()
        x2 = rect.rect.right()
        y2 = rect.rect.bottom()
        x_ini, y_ini, x_fin, y_fin = rotate_points(shape_x, shape_y, x1 + pos_x, y1 + pos_y, x2 + pos_x, y2 + pos_y,
                                                    360 - angle)
        # Rectangle around the face
        x_ini = x_ini - 20
        y_ini = y_ini - 25
        x_fin = x_fin + 20
        y_fin = y_fin + 25

        crop = orig_img.crop((x_ini, y_ini, x_fin, y_fin))
        blur_crop = crop.filter(ImageFilter.GaussianBlur(radius=40))
        orig_img.paste(blur_crop, (x_ini, y_ini, x_fin, y_fin))

        cv.rectangle(img, (x1, y2), (x2, y2), (255, 0, 0), 3)

    cv.imwrite(os.path.join(path_tiles, tile_name), img)

    return orig_img


def rotate_points(shape_x, shape_y, x_ini, y_ini, x_fin, y_fin, angle):
    if angle == 90:
        x_inicial = x_ini
        y_inicial = y_fin

        x_final = x_fin
        y_final = y_ini

        x_inicial_rot = shape_x - 1 - y_inicial
        y_inicial_rot = x_inicial

        x_final_rot = shape_x - 1 - y_final
        y_final_rot = x_final

    elif angle == 180:
        x_inicial = x_fin
        y_inicial = y_fin

        x_final = x_ini
        y_final = y_ini

        x_inicial_rot = shape_x - 1 - x_inicial
        y_inicial_rot = shape_y - 1 - y_inicial

        x_final_rot = shape_x - 1 - x_final
        y_final_rot = shape_y - 1 - y_final

    elif angle == 270:
        x_inicial = x_fin
        y_inicial = y_ini

        x_final = x_ini
        y_final = y_fin

        x_inicial_rot = y_inicial
        y_inicial_rot = shape_y - 1 - x_inicial

        x_final_rot = y_final
        y_final_rot = shape_y - 1 - x_final

    else:
        x_inicial_rot = x_ini
        y_inicial_rot = y_ini
        x_final_rot = x_fin
        y_final_rot = y_fin

    return x_inicial_rot, y_inicial_rot, x_final_rot, y_final_rot


def slice_img(orig_img, img_name, path_img_rot, angle, control):
    if control == 0:
        pos_x = 0
        pos_y = 0

        img_rot = cv.imread(os.path.join(path_img_rot + r'/' + img_name))
        cv.imwrite(os.path.join(path_tiles, img_name), img_rot)

        orig_img = detect_face_cnn(orig_img, img_name, angle, pos_x, pos_y)
        orig_img.save(path_output+r'/'+img_name)
        # cv.imwrite(os.path.join(path_output, img_name), orig_img)

    else:
        tiles = image_slicer.slice(path_img_rot + r'/' + img_name, 2, save=False)
        image_slicer.save_tiles(tiles, directory=path_tiles, prefix='slice')

        slice_name = 'slice_01_01.png'
        pos_x = tiles[0].coords[0]
        pos_y = tiles[0].coords[1]
        orig_img = detect_face_cnn(orig_img, slice_name, angle, pos_x, pos_y)

        slice_name = 'slice_01_02.png'
        pos_x = tiles[1].coords[0]
        pos_y = tiles[1].coords[1]
        orig_img = detect_face_cnn(orig_img, slice_name, angle, pos_x, pos_y)

        orig_img.save(path_output + r'/' + img_name)

        tiles[0].image = Image.open(path_tiles + r'/' + 'slice_01_01.png')
        tiles[1].image = Image.open(path_tiles + r'/' + 'slice_01_02.png')

        image = image_slicer.join(tiles)
        image.save(path_result + r'/' + str(angle) + '_' + img_name)


def rotate_img_360dg(orig_img, angle):
    if angle == 90:
        rotated = cv.rotate(orig_img, cv.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated = cv.rotate(orig_img, cv.ROTATE_180)
    elif angle == 270:
        rotated = cv.rotate(orig_img, cv.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated = orig_img

    return rotated


def face_detect(orig_img, img_rotated, img_name, path_img_rot, angle):
    altura = img_rotated.shape[0]
    largura = img_rotated.shape[1]

    if largura > altura:
        slice_img(orig_img, img_name, path_img_rot, angle, control=1)
    else:
        slice_img(orig_img, img_name, path_img_rot, angle, control=0)


def replicate_img(img_name):
    img_read = cv.imread(path_input + r'/' + img_name)
    img_read_pil = Image.open(path_input+ r'/' +img_name)

    rotated_0 = rotate_img_360dg(img_read, 0)
    rotated_90 = rotate_img_360dg(img_read, 90)
    rotated_180 = rotate_img_360dg(img_read, 180)
    rotated_270 = rotate_img_360dg(img_read, 270)

    cv.imwrite(os.path.join(path_rot, img_name), rotated_0)
    face_detect(img_read_pil, rotated_0, img_name, path_rot, angle=0)

    cv.imwrite(os.path.join(path_rot, img_name), rotated_90)
    face_detect(img_read_pil, rotated_90, img_name, path_rot, angle=90)

    cv.imwrite(os.path.join(path_rot, img_name), rotated_180)
    face_detect(img_read_pil, rotated_180, img_name, path_rot, angle=180)

    cv.imwrite(os.path.join(path_rot, img_name), rotated_270)
    face_detect(img_read_pil, rotated_270, img_name, path_rot, angle=270)


def main():
    for file_img in os.listdir(path_input):
        if file_img.endswith('.jpg') or file_img.endswith('.JPG') or file_img.endswith('.jpeg') \
                or file_img.endswith('.png'):
            img_name = str(file_img)
            print('******************IMAGEM:****************')
            print('NOME: ' + img_name)
            replicate_img(img_name)

            print('Processada: ' + img_name)


if __name__ == '__main__':
    main()
