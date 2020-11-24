# Arquivo que insere as informações falsas nas imagens.

from PIL import Image, ImageFont, ImageDraw
import cv2 as cv
import string
import random
import time
import os

import images_transformation
import background_generator
import class_pessoa
import paths

path_base = paths.path

path_input = path_base + r'/saida_back'
path_mask = path_base + r'/mask'
path_crops = path_mask + r'/crops'
path_crops_teste = path_crops + r'/teste'
path_output = path_base + r'/reboot'

# CNH
# font_color = (15, 15, 15)
# font_type = 'courier-ps-mt-std-bold.otf'

# RG
# font_color = (105, 105, 105)
# font_type = 'arial-narrow-bold.ttf'

# CPF
# font_color = (255, 255, 255)
# font_type = 'arial-narrow-bold.ttf'

# json_name = 'via_export_json.json'


# Rotaciona as imagens que tiverem na vertical de acordo com a orientação passada como o parâmetro "direction".
def rotate_crop_img(img_crop, direction):
    if direction == 1:
        rotate_crop = cv.imread(path_crops + r'/' + img_crop)
        rotate_crop = cv.rotate(rotate_crop, cv.ROTATE_90_CLOCKWISE)
        cv.imwrite(path_crops + r'/' + img_crop, rotate_crop)
    else:
        rotate_crop = cv.imread(path_crops_teste + r'/' + img_crop)
        rotate_crop = cv.rotate(rotate_crop, cv.ROTATE_90_COUNTERCLOCKWISE)
        cv.imwrite(path_crops_teste + r'/' + img_crop, rotate_crop)


# Gera o texto a ser colocado na mask.
def text_generator(tipo_texto, pessoa, tipo_doc, control_text):
    qtd_chars = control_text
    text = ''
    if tipo_texto == 'nome':
        text = pessoa.set_nome(qtd_chars)
    elif tipo_texto == 's_nome':
        text = pessoa.set_s_nome()
    elif tipo_texto == 'cpf':
        text = pessoa.set_cpf()
    elif tipo_texto == 'rg':
        text = pessoa.set_rg(tipo_doc)
    elif tipo_texto == 'org':
        text = pessoa.set_org()
    elif tipo_texto == 'est':
        text = pessoa.set_est()
    elif tipo_texto == 'cid_est':
        text = pessoa.set_cid_est(qtd_chars)
    elif tipo_texto == 'rg_org_est':
        text = pessoa.set_rg_org_est()
    elif tipo_texto == 'data':
        text = pessoa.set_data()
    elif tipo_texto == 'tipo_h':
        text = pessoa.set_tipo_h()
    elif tipo_texto == 'n_9':
        text = pessoa.set_n_9(qtd_chars)
    elif tipo_texto == 'n_reg':
        text = pessoa.set_n_reg()
    elif tipo_texto == 'n_11':
        text = pessoa.set_n_11()
    elif tipo_texto == 'cod_11':
        text = pessoa.set_cod_11()
    elif tipo_texto == 'obs':
        text = pessoa.set_obs()
    elif tipo_texto == 'cargo':
        text = pessoa.set_cargo()
    elif tipo_texto == 'd_orig':
        text = pessoa.set_d_orig()
    elif tipo_texto == 'folha':
        text = pessoa.set_folha()
    elif tipo_texto == 'aspa':
        text = pessoa.set_aspa()
    elif tipo_texto == 'via':
        text = pessoa.set_via()
    elif tipo_texto == 'pis':
        text = pessoa.set_pis(qtd_chars)
    elif tipo_texto == 'cod_4':
        text = pessoa.set_cod_4()
    elif tipo_texto == 'n_5':
        text = pessoa.set_n_5()
    elif tipo_texto == 'cod_10':
        text = pessoa.set_cod_10()
    elif tipo_texto == 'cid':
        text = pessoa.set_cid(qtd_chars)
    elif tipo_texto == 'cod_8':
        text = pessoa.set_cod_8()
    elif tipo_texto == 'n_via':
        text = pessoa.set_n_via()
    elif tipo_texto == 'n_6':
        text = pessoa.set_n_6()
    elif tipo_texto == 'per':
        text = 'PERMISSÃO'
    elif tipo_texto == 'rga':
        text = 'RG ANTERIOR'
    elif tipo_texto == 'naci':
        text = 'BRASILEIRA'
    else:
        pass
    return text


def med_text_area(text_width, text_height):
    if text_height > text_width:
        qtd_chars = text_width
    else:
        a = text_width / (text_height * 0.6)
        qtd_chars = int(a)
    return qtd_chars


def font_selection(tipo_doc):
    font_color = (42, 42, 42)
    font_type = r'./files/arial-narrow-bold.ttf'
    color = 'red'
    if tipo_doc == 'CPF':
        font_color = (255, 255, 255)
        font_type = r'./files/arial-mt-bold.ttf'
        color = 'black'
    elif tipo_doc == 'CNH':
        font_color = (15, 15, 15)
        font_type = r'./files/courier-ps-mt-std-bold.otf'
        color = 'white'
    elif tipo_doc == 'RG':
        font_color = (105, 105, 105)
        font_type = r'./files/arial-mt-bold.ttf'
        color = 'white'
    else:
        pass

    return font_color, font_type, color


def localize_text_area():
    x, y, w, h = 0, 0, 0, 0
    temp_mask = cv.imread(path_mask + r'/' + 'temp_mask.jpg')
    gray = cv.cvtColor(temp_mask, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)

    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 2)

    thresh = cv.dilate(thresh, None, iterations=15)
    thresh = cv.erode(thresh, None, iterations=15)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)

        if w < 5 or h < 5:
            print('teve 0')
            continue
        else:
            return [x, y, w, h]

    return [x, y, w, h]


# Cria uma pequena mask para as regiões verticais.
def create_vertical_mask(img_name, tipo_texto, pessoa, tipo_doc, font_color, font_type, color, qtd_chars_name):
    image = Image.open(path_crops + r'/' + img_name)
    img_width, img_height = image.size
    image.close()

    l_mask = Image.new('RGB', (img_width, img_height), color=color)
    l_mask_name = img_name
    l_mask.save(path_crops_teste + r'/' + l_mask_name)

    l_mask_open = Image.open(path_crops_teste + r'/' + l_mask_name)

    font = ImageFont.truetype(font_type, img_height)
    text = text_generator(tipo_texto, pessoa, tipo_doc, control_text=qtd_chars_name)
    ImageDraw.Draw(l_mask_open).text((0, 0), text, font_color, font=font, align='center')

    l_mask_open.save(os.path.join(path_crops_teste, l_mask_name))
    l_mask_open.close()

    rotate_crop_img(l_mask_name, 0)

    return text


def crop_n_bin_seg(img_name, min_x, min_y, max_x, max_y):
    temp_crop = 'temp_crop.jpg'

    img = Image.open(path_input + r'/' + img_name)
    crop = img.crop((min_x, min_y, max_x, max_y))
    crop.save(os.path.join(path_crops, temp_crop))
    crop.close()

    img_crop = cv.imread(path_crops + r'/' + temp_crop, 0)
    bin_img = cv.adaptiveThreshold(img_crop, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    cv.imwrite(os.path.join(path_crops, 'bin_img.jpg'), bin_img)

    mini = Image.open(path_crops + r'/' + 'bin_img.jpg')
    full_mask = Image.open(path_crops + r'/' + 'teste_crop.jpg')
    full_mask.paste(mini, (min_x, min_y))
    full_mask.save(os.path.join(path_crops, 'teste_crop.jpg'))


# Gera as demais masks.
def mask_generator(tipo_doc, json_arq, img_name, angle):
    area_n_text = []
    font_color, font_type, color = font_selection(tipo_doc)
    p1 = class_pessoa.Person()

    img = Image.open(path_input + r'/' + img_name)
    img_width, img_height = img.size

    mask = Image.new('RGB', (img_width, img_height), color=color)
    mask_name = 'mask_' + img_name
    mask.save(os.path.join(path_mask, mask_name))
    mask.close()

    conj_img = [v for k, v in json_arq.items() if k.startswith(img_name)]

    # Checa se a imagem está no path
    if conj_img is not None:
        search = conj_img[0]
        regions = search['regions']
        qtd_regions = len(regions)
        aux = 0

        while aux < qtd_regions:
            mask_open = Image.open(path_mask + r'/' + mask_name)

            if regions[aux]['region_attributes']['info_type'] == 'p' and \
                    len(regions[aux]['region_attributes']) > 1:

                tipo_texto = regions[aux]['region_attributes']['text_type']

                # Região é um retângulo.
                if regions[aux]['shape_attributes']['name'] == 'rect':
                    x_inicial = regions[aux]['shape_attributes']['x']
                    width = regions[aux]['shape_attributes']['width']
                    y_inicial = regions[aux]['shape_attributes']['y']
                    height = regions[aux]['shape_attributes']['height']

                    x_final = x_inicial + width
                    y_final = y_inicial + height

                    x_inicial, y_inicial, x_final, y_final = background_generator.rotate_points(img_width,
                                                                                                img_height,
                                                                                                x_inicial, y_inicial,
                                                                                                x_final, y_final,
                                                                                                angle=angle)

                    width = x_final - x_inicial
                    height = y_final - y_inicial

                    min_x, max_x, min_y, max_y = x_inicial, x_final, y_inicial, y_final

                else:  # Não é um retângulo.
                    all_points_x = regions[aux]['shape_attributes']['all_points_x']
                    all_points_y = regions[aux]['shape_attributes']['all_points_y']
                    qtd_points = len(all_points_x)

                    points_x = []
                    points_y = []

                    for i in range(qtd_points):
                        pts_x, pts_y = background_generator.rotate_poly(img_width, img_height,
                                                                        all_points_x[i], all_points_y[i], angle=angle)

                        points_x.append(pts_x)
                        points_y.append(pts_y)

                    min_x, min_y, max_x, max_y,  = min(points_x), min(points_y), max(points_x), max(points_y)

                    #  Dimininui a fonte dos polígonos para 80%
                    width = max_x - min_x
                    height = max_y - min_y

                    height = int(height*0.8)

                if width > height:  # Horizontal
                    qtd_chars = med_text_area(width, height)
                    font = ImageFont.truetype(font_type, height)
                    text = text_generator(tipo_texto, p1, tipo_doc, control_text=qtd_chars)
                    ImageDraw.Draw(mask_open).text((min_x, min_y), text, font_color,
                                                   font=font, align='center')

                    if tipo_texto != 'x':
                        temp_mask = Image.new('RGB', (img_width, img_height), color=color)
                        temp_mask.save(os.path.join(path_mask, 'temp_mask.jpg'))
                        temp_mask = Image.open(path_mask + r'/' + 'temp_mask.jpg')
                        ImageDraw.Draw(temp_mask).text((min_x, min_y), text, font_color,
                                                       font=font, align='center')
                        temp_mask.save(os.path.join(path_mask, 'temp_mask.jpg'))
                        temp_mask.close()

                        area = localize_text_area()
                        area.append(text)
                        area_n_text.append(area)
                        os.remove(path_mask + r'/temp_mask.jpg')

                    mask_open.save(os.path.join(path_mask, mask_name))
                    mask_open.close()

                else:  # Vertical
                    qtd_chars = med_text_area(height, width)
                    crop = img.crop((min_x, min_y, max_x, max_y))
                    img_crop = img_name
                    crop.save(os.path.join(path_crops, img_crop))
                    crop.close()

                    rotate_crop_img(img_crop, 1)
                    text = create_vertical_mask(img_crop, tipo_texto, p1, tipo_doc, font_color, font_type,
                                                color, qtd_chars_name=qtd_chars)

                    # Cola os crops verticais com a mask original.
                    mini = Image.open(path_crops_teste + r'/' + img_name)
                    full_mask = Image.open(path_mask + r'/' + mask_name)
                    full_mask.paste(mini, (min_x, min_y))
                    full_mask.save(os.path.join(path_mask, mask_name))

                    if tipo_texto != 'x':
                        temp_mask = Image.new('RGB', (img_width, img_height), color=color)
                        temp_mask.save(os.path.join(path_mask, 'temp_mask.jpg'))
                        temp_mask = Image.open(path_mask + r'/' + 'temp_mask.jpg')

                        temp_mask.paste(mini, (min_x, min_y))
                        temp_mask.save(os.path.join(path_mask, 'temp_mask.jpg'))
                        temp_mask.close()

                        area = localize_text_area()
                        area.append(text)
                        area_n_text.append(area)
                        os.remove(path_mask + r'/temp_mask.jpg')

                    mini.close()
                    full_mask.close()

                    os.remove(path_crops_teste + r'/' + img_crop)
                    os.remove(path_crops + r'/' + img_crop)

            else:  # Texto default do documento
                transcription = regions[aux]['region_attributes']['transcription']

                # Região é um retângulo
                if regions[aux]['shape_attributes']['name'] == 'rect':
                    x_inicial = regions[aux]['shape_attributes']['x']
                    width = regions[aux]['shape_attributes']['width']
                    y_inicial = regions[aux]['shape_attributes']['y']
                    height = regions[aux]['shape_attributes']['height']

                    x_final = x_inicial + width
                    y_final = y_inicial + height

                    x_inicial, y_inicial, x_final, y_final = background_generator.rotate_points(img_width,
                                                                                                img_height,
                                                                                                x_inicial, y_inicial,
                                                                                                x_final, y_final,
                                                                                                angle=angle)

                    min_x, max_x, min_y, max_y = x_inicial, x_final, y_inicial, y_final

                    width = max_x - min_x
                    height = max_y - min_y

                    if transcription != 'X':
                        area = [min_x, min_y, width, height, transcription]
                        area_n_text.append(area)

                else:
                    all_points_x = regions[aux]['shape_attributes']['all_points_x']
                    all_points_y = regions[aux]['shape_attributes']['all_points_y']
                    qtd_points = len(all_points_x)

                    points_x = []
                    points_y = []
                    width = -1
                    height = -1

                    for i in range(qtd_points):
                        pts_x, pts_y = background_generator.rotate_poly(img_width, img_height,
                                                                        all_points_x[i], all_points_y[i], angle=angle)
                        points_x.append(pts_x)
                        points_y.append(pts_y)

                    if transcription != 'X':
                        area = [points_x, points_y, width, height, transcription]
                        area_n_text.append(area)

            aux = aux + 1
    else:
        pass

    return area_n_text


# Retira as informações da pessoa para inserir no txt.
def get_pessoa_text(pessoa, tipo_texto):
    text = ''
    if tipo_texto == 'nome':
        text = pessoa.get_nome()
    elif tipo_texto == 's_nome':
        text = pessoa.get_s_nome()
    elif tipo_texto == 'cpf':
        text = pessoa.get_cpf()
    elif tipo_texto == 'rg':
        text = pessoa.get_rg()
    elif tipo_texto == 'org':
        text = pessoa.get_org()
    elif tipo_texto == 'est':
        text = pessoa.get_est()
    elif tipo_texto == 'cid_est':
        text = pessoa.get_local()
    elif tipo_texto == 'rg_org_est':
        text = pessoa.get_rg_org_est()
    elif tipo_texto == 'data':
        text = pessoa.get_data()
    elif tipo_texto == 'tipo_h':
        text = pessoa.get_tipo_h()
    elif tipo_texto == 'n_9':
        text = pessoa.get_n_9()
    elif tipo_texto == 'n_reg':
        text = pessoa.get_n_reg()
    elif tipo_texto == 'n_11':
        text = pessoa.get_n_11()
    elif tipo_texto == 'cod_11':
        text = pessoa.get_cod_11()
    elif tipo_texto == 'obs':
        text = pessoa.get_obs()
    elif tipo_texto == 'cargo':
        text = pessoa.get_cargo()
    elif tipo_texto == 'd_orig':
        text = pessoa.get_d_orig()
    elif tipo_texto == 'folha':
        text = pessoa.get_folha()
    elif tipo_texto == 'aspa':
        text = pessoa.get_aspa()
    elif tipo_texto == 'via':
        text = pessoa.get_via()
    elif tipo_texto == 'pis':
        text = pessoa.get_pis()
    elif tipo_texto == 'cod_4':
        text = pessoa.get_cod_4()
    elif tipo_texto == 'n_5':
        text = pessoa.get_n_5()
    elif tipo_texto == 'cod_10':
        text = pessoa.get_cod_10()
    elif tipo_texto == 'cid':
        text = pessoa.get_cid()
    elif tipo_texto == 'cod_8':
        text = pessoa.get_cod_8()
    elif tipo_texto == 'n_via':
        text = pessoa.get_n_via()
    elif tipo_texto == 'n_6':
        text = pessoa.get_n_6()
    elif tipo_texto == 'per':
        text = 'PERMISSÃO'
    elif tipo_texto == 'rga':
        text = 'RG ANTERIOR'
    elif tipo_texto == 'naci':
        text = 'BRASILEIRA'
    else:
        pass
    return text


# Cria o txt baseado nas possíveis rotações que ocorreram com a imagem
def write_txt_file(txt_name, area_n_text, angle):
    txt_text = ''
    img = Image.open(path_output + r'/' + txt_name + '.jpg')
    img_width, img_height = img.size

    im = Image.new('RGB', (img_width, img_height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for element in area_n_text:
        width = element[2]
        height = element[3]
        transcription = element[4]

        # A informação é um polígono
        if width == -1 and height == -1:
            final_points_x = []
            final_points_y = []

            x_points = element[0]
            y_points = element[1]
            qtd_points = len(x_points)

            for i in range(qtd_points):
                pts_x, pts_y = background_generator.rotate_poly(img_width, img_height,
                                                                x_points[i], y_points[i], angle=angle)
                final_points_x.append(pts_x)
                final_points_y.append(pts_y)

            xy = []
            for a in range(len(final_points_x)):
                xy.append((final_points_x[a], final_points_y[a]))

            txt_text = txt_text + '{}, {}, {}, {}, {}\n' \
                .format(final_points_x, final_points_y, width, height, transcription)

            draw.polygon(xy, fill=(255, 255, 255))

        else:
            x_inicial = element[0]
            y_inicial = element[1]
            x_final = x_inicial + width
            y_final = y_inicial + height

            x_inicial, y_inicial, x_final, y_final = background_generator.rotate_points(img_width,
                                                                                        img_height,
                                                                                        x_inicial, y_inicial,
                                                                                        x_final, y_final,
                                                                                        angle=angle)
            width = x_final - x_inicial
            height = y_final - y_inicial

            txt_text = txt_text + '{}, {}, {}, {}, {}\n' \
                .format(x_inicial, y_inicial, width, height, transcription)

            draw.rectangle((x_inicial, y_inicial, x_final, y_final), fill=(255, 255, 255))

    im.save(path_output + r'/' + txt_name + '_mask_GT' + '.jpg')
    with open(path_output + r'/' + txt_name + '_GT.txt', 'w') as file:
        file.write('x, y, width, height, transcription\n')
        file.write(txt_text)


# Joga pixels brancos na imagem para que pareça mais real.
def blur_mask(img_name, path_img, tipo_doc):
    mask_img = cv.imread(os.path.join(path_img, img_name))
    blue_mask, green_mask, red_mask = cv.split(mask_img)

    for j in range(mask_img.shape[0]):
        for i in range(mask_img.shape[1]):
            random.seed()
            ruido = random.randint(0, 100)

            if tipo_doc == 'CPF':
                if ruido > 95:
                    blue_mask[j][i] = 0
                    green_mask[j][i] = 0
                    red_mask[j][i] = 0
                else:
                    pass
            else:
                if ruido > 95:
                    blue_mask[j][i] = 255
                    green_mask[j][i] = 255
                    red_mask[j][i] = 255
                else:
                    pass

    dst = cv.merge((blue_mask, green_mask, red_mask))

    # Antes era path_blur
    cv.imwrite(os.path.join(path_mask, img_name), dst)


# Cria um nome aleatório para as imagens geradas.
def create_img_name():
    num = ''
    random.seed()
    let = ''.join(random.choice(string.ascii_letters) for x in range(7))
    random.seed()
    for i in range(7):
        num = num + str(random.randrange(10))

    return num + let


# Faz a multiplicação da mask com a imagem original.
def mult_img(mask_name, img_name, tipo_doc, area_n_text, param):
    new_img_name = create_img_name()
    back = cv.imread(os.path.join(path_input, img_name))
    blue_back, green_back, red_back = cv.split(back)

    y = back.shape[0]
    x = back.shape[1]

    mask = cv.imread(os.path.join(path_mask, mask_name))
    blue_mask, green_mask, red_mask = cv.split(mask)

    for j in range(y):
        for i in range(x):
            if tipo_doc == 'CPF':
                if blue_mask[j][i] > param and green_mask[j][i] > param \
                        and red_mask[j][i] > param:
                    blue_back[j][i] = blue_mask[j][i]
                    green_back[j][i] = green_mask[j][i]
                    red_back[j][i] = red_mask[j][i]
                else:
                    pass

            else:
                if blue_mask[j][i] < param and green_mask[j][i] < param \
                        and red_mask[j][i] < param:
                    blue_back[j][i] = blue_mask[j][i]
                    green_back[j][i] = green_mask[j][i]
                    red_back[j][i] = red_mask[j][i]
                else:
                    pass

    final_img = cv.merge((blue_back, green_back, red_back))
    cv.imwrite(os.path.join(path_output, new_img_name + '.jpg'), final_img)
    write_txt_file(new_img_name, area_n_text, angle=0)  # angle = 0 pq a mask final foi gerada na posição de 0 graus.

    return new_img_name


# Chama as funções de ruído e de multiplicação para cada imagem.
def noise_mask(tipo_doc, img_name, area_n_text):
    mask_name = 'mask_' + img_name
    blur_mask(mask_name, path_mask, tipo_doc)
    img_base_name = mult_img(mask_name, img_name, tipo_doc, area_n_text, param=150)
    images_transformation.augmentation(img_base_name, area_n_text, tipo_doc)


# Faz a função de main() desse arquivo.
def control_mask_gen(tipo_doc, json_arq, img_name, angle):
    print('GERANDO a mask...')
    inicio = time.time()
    area_n_text = mask_generator(tipo_doc, json_arq, img_name, angle)
    noise_mask(tipo_doc, img_name, area_n_text)
    fim = time.time()
    tempo = fim - inicio
    print('Tempo de execução:' + str(tempo))






