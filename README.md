# GeradorBaseSintetica  <*README.md em construção*>
### Code used for the development of the BID Dataset: A Challenge Dataset for Document Processing Tasks. (Best Work of SIBGRAPI 2020 in Workshop of Works in Progress)

O arquivo **generic_img_generator.py** é o arquivo principal do trabalho, o qual une grande parte dos diversos processos utilizados para a geração da base que será descrito em seguida...

**O processo ocorre da seguinte forma:**
1. No VVG Image Annotator [A. Dutta and A. Zisserman, “The via annotation software for images, audio and video,” in Proceedings of the 27th ACM International Conference on Multimedia, 2019, pp. 2276–2279.], as rotulações seguiram um padrão que foi seguido no código fonte. Na ferramente citada os campos de region_attributes foram descritos da seguinte forma: O atributo "info_type" foi usado para definir que tipo de informação o campo rotulado continha, caso o valor fosse "d" o campo era **d**efault do próprio layout do documento e não precisava ser alterado, caso fosse "p", ele continha uma informação **p**essoal e precisava ser apagado e substituído por outro texto. O campo "text_type" para casos de texto do layout também possuíam o valor "d", já para os textos pessoais continha o tipo de informação que deveria ser adicionado naquele campo, como por exemplo uma "data", um "rg" e etc. O campo "transcription" continha a transcrição do texto rotulado para os casos de texto do layout e apenas um "x" para textos pessoais, visto que essa informação seria substituída futuramente. 

Segue um exemplo de um campo do layout e um de informações pessoais.

``` "region_attributes": {"info_type":"d","text_type":"d","transcription":"NOME"} ```  
``` "region_attributes":{"info_type":"p","text_type":"data","transcription":"X"} ```




### OBS.:
1. O arquivo find_face.py é um script que usa um modelo de reconhecimento de rostos pré-treinado [D. E. King, “Max-margin object detection,” arXiv preprint arXiv:1502.00046, 2015.] ,disponível no diretório "files" deste trabalho, para reconhecer os rostos nos documentos e realizar um *blur* na região. O mesmo não está diretamente interligado com o processo de geração da base, mas foi utilizado para o resultado final.
2. Já o arquivo paths.py possui apenas a assinatura de um diretório utilizado no projeto para evitar a sua repetição ao longo do desenvolvimento. 
