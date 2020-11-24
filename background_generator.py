# Arquivo que apaga as informações pessoais das imagens.

from colorthief import ColorThief
import numpy as np
import cv2 as cv
import os

import paths
path_base = paths.path
path_rot = path_base + r'/saida_rot'
path_back = path_base + r'/saida_back'
path_crop = path_rot + r'/crop'


# Checa se os pixels estão dentro do intervalo para pegar os 3 mais próximos.
def check_pixels(borders, pixel_correction=3):
    check = False
    if borders[0] - pixel_correction > 0:
        check = True
    return check


# Retira os pixels pretos do polylines.
def correct_polyline_spaces(area, img, dom_color, tipo_doc):
    qtd_elem = len(area)
    blue, green, red = cv.split(img)
    red_dom = dom_color[0]
    green_dom = dom_color[1]
    blue_dom = dom_color[2]

    for x in range(qtd_elem):
        if blue[area[x][0]][area[x][1]] == 0 and green[area[x][0]][area[x][1]] == 0 \
                and red[area[x][0]][area[x][1]] == 0:
            correct_color(blue, area[x], blue_dom, tipo_doc)
            correct_color(green, area[x], green_dom, tipo_doc)
            correct_color(red, area[x], red_dom, tipo_doc)

    return cv.merge((blue, green, red))


# Garante que os intervalos fiquem  do range da imagem.
def fill_black_area(min_x, min_y, max_x, max_y, pixel_correction, limit_x, limit_y):
    if max_x + pixel_correction >= limit_x:
        max_x = limit_x - 1
    else:
        max_x = max_x + pixel_correction

    if max_y + pixel_correction >= limit_y:
        max_y = limit_y - 1
    else:
        max_y = max_y + pixel_correction

    if min_x - pixel_correction < 0:
        min_x = 0
    else:
        min_x = min_x - pixel_correction

    if min_y - pixel_correction < 0:
        min_y = 0
    else:
        min_y = min_y - pixel_correction

    return [min_x, min_y, max_x, max_y]


# Cria uma área retangular na área do texto para apagá-lo.
def create_rect_area(x_inicial, y_inicial, x_final, y_final):
    area = []
    x_var = x_inicial
    y_var = y_inicial

    while y_var < y_final:
        while x_var < x_final:
            area.append([y_var, x_var])
            x_var = x_var + 1
        x_var = x_inicial
        y_var = y_var + 1

    return area


# Cobre os pixels listados dentro da área de texto.
def correct_color(img, tp, dom_color, tipo_doc):
    if check_pixels(tp):
        window = np.array([img[tp[0] - 3, tp[1]], img[tp[0] - 2, tp[1]], img[tp[0] - 1, tp[1]]])
        mean_pixel = np.mean(window)

        if tipo_doc == 'CPF':
            img[tp[0]][tp[1]] = mean_pixel

        else:
            if mean_pixel > dom_color:
                img[tp[0]][tp[1]] = mean_pixel
            else:
                img[tp[0]][tp[1]] = dom_color


# Apaga o texto.
def erase_text(img, area, dom_color, tipo_doc):
    blue, green, red = cv.split(img)
    qtd_elem = len(area)
    red_dom = dom_color[0]
    green_dom = dom_color[1]
    blue_dom = dom_color[2]

    for i in range(qtd_elem):
        correct_color(blue, area[i], blue_dom, tipo_doc)
        correct_color(green, area[i], green_dom, tipo_doc)
        correct_color(red, area[i], red_dom, tipo_doc)

    return cv.merge((blue, green, red))


# O elemento em mat[row][col] deve rodar com mat[col][10 - row - 1], mat[10 - row - 1][10 - col - 1],
# e mat[10 - col - 1][row].
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


def rotate_poly(shape_x, shape_y, point_x, point_y, angle):
    x_inicial = point_x
    y_inicial = point_y

    if angle == 90:
        x_inicial_rot = shape_x - 1 - y_inicial
        y_inicial_rot = x_inicial

    elif angle == 180:
        x_inicial_rot = shape_x - 1 - x_inicial
        y_inicial_rot = shape_y - 1 - y_inicial

    elif angle == 270:
        x_inicial_rot = y_inicial
        y_inicial_rot = shape_y - 1 - x_inicial

    else:
        x_inicial_rot = x_inicial
        y_inicial_rot = y_inicial

    return x_inicial_rot, y_inicial_rot


# Gera as imagens do background.
def back_gen(img_name, arq, tipo_doc, angle):
    img_2_read = cv.imread(path_rot + r'/' + img_name)
    crop_name = 'crop.jpg'

    shape_y = img_2_read.shape[0]
    shape_x = img_2_read.shape[1]

    conj_img = [v for k, v in arq.items() if k.startswith(img_name)]

    if conj_img is not None:
        search = conj_img[0]
        regions = search['regions']
        qtd_regions = len(regions)
        aux = 0

        while aux < qtd_regions:
            if regions[aux]['region_attributes']['info_type'] == 'p':
                if regions[aux]['shape_attributes']['name'] == 'rect':
                    rect_x = regions[aux]['shape_attributes']['x']
                    rect_x_final = rect_x + regions[aux]['shape_attributes']['width']
                    rect_y = regions[aux]['shape_attributes']['y']
                    rect_y_final = rect_y + regions[aux]['shape_attributes']['height']

                    rect_x, rect_y, rect_x_final, rect_y_final = rotate_points(shape_x, shape_y, rect_x, rect_y,
                                                                               rect_x_final, rect_y_final, angle)

                    area_text = create_rect_area(rect_x, rect_y, rect_x_final, rect_y_final)


                    crop_img = img_2_read[rect_y:rect_y_final, rect_x:rect_x_final]
                    cv.imwrite(os.path.join(path_crop, crop_name), crop_img)

                    color_thief = ColorThief(path_crop + r'/' + crop_name)
                    palette = color_thief.get_palette(color_count=2)
                    dominant_color = palette[0]

                    os.remove(path_crop + r'/' + crop_name)

                    img_2_read = erase_text(img_2_read, area_text, dominant_color, tipo_doc)

                else:
                    all_points_x = regions[aux]['shape_attributes']['all_points_x']
                    all_points_y = regions[aux]['shape_attributes']['all_points_y']
                    qtd_points = len(all_points_x)
                    points = []

                    for i in range(qtd_points):
                        points.append(rotate_poly(shape_x, shape_y, all_points_x[i], all_points_y[i], angle))
                    pts = np.asarray(points)
                    pts = pts.reshape((-1, 1, 2))
                    cv.polylines(img_2_read, pts, isClosed=True, color=(0, 0, 0))
                    cv.fillPoly(img_2_read, [pts], (0, 0, 0))

                    pixel_correction = 3

                    min_x = min(all_points_x)
                    min_y = min(all_points_y)
                    max_y = max(all_points_y)
                    max_x = max(all_points_x)

                    min_x, min_y, max_x, max_y = rotate_points(shape_x, shape_y, min_x, min_y, max_x, max_y, angle)

                    correct_values = fill_black_area(min_x, min_y, max_x, max_y, pixel_correction, shape_x, shape_y)
                    min_x = correct_values[0]
                    min_y = correct_values[1]
                    max_x = correct_values[2]
                    max_y = correct_values[3]

                    area_poly = create_rect_area(min_x, min_y, max_x, max_y)

                    crop_img = img_2_read[min_y:max_y, min_x:max_x]
                    cv.imwrite(os.path.join(path_crop, crop_name), crop_img)

                    color_thief = ColorThief(path_crop + r'/' + crop_name)
                    palette = color_thief.get_palette(color_count=2)
                    dominant_color = palette[0]

                    os.remove(path_crop + r'/' + crop_name)

                    img_2_read = correct_polyline_spaces(area_poly, img_2_read, dominant_color, tipo_doc)

            aux = aux + 1
        os.remove(path_rot + r'/' + img_name)
        cv.imwrite(os.path.join(path_back, img_name), img_2_read)

