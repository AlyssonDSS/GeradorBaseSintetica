# Arquivo main do projeto.
import cv2 as cv
import json
import os

import background_generator
import rotate_images
import text_2_image

import paths
path_base = paths.path

# Path com a imagem.
path_entrada = path_base + r'/original/BASE_UTIL/BETA'

# Nome do json de saída do VIA ANNOTATOR com as informações de todas as imagens rotuladas.
json_name = 'via_export_json.json'


def main():
    # Escolher o tipo de imagem que será gerada CNH, RG ou CPF, isso definirá a melhor fonte para a imagem criada.
    tipo_doc = 'CNH'

    # Número de vezes que o processo irá se repetir para criar mais de uma imagem com informações diferentes a
    # partir de uma mesma imagem.
    repetir = 1

    with open(path_entrada + r'/' + json_name, 'r', encoding='utf-8') \
            as json_file:
        json_arq = json.load(json_file)

    for file_img in os.listdir(path_entrada):
        if file_img.endswith('.jpg') or file_img.endswith('.JPG') or file_img.endswith('.jpeg') \
                or file_img.endswith('.png'):
            img_name = str(file_img)
            img = cv.imread(path_entrada + r'/' + img_name)

            print('***************************')
            print('Processando: ' + img_name)

            angle_img, check_img = rotate_images.rotate_img(img, img_name)

            if check_img == 1:
                background_generator.back_gen(img_name, json_arq, tipo_doc, angle=angle_img)

                # print('Background gerado!')
                # print('-----------------------------')

                for i in range(repetir):
                    text_2_image.control_mask_gen(tipo_doc, json_arq, img_name, angle=angle_img)


if __name__ == '__main__':
    main()
