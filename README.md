# GeradorBaseSintetica  <*README.md em construção*>
### Code used for the development of the BID Dataset: A Challenge Dataset for Document Processing Tasks. (Best Work of SIBGRAPI 2020 in Workshop of Works in Progress)

O arquivo **generic_img_generator.py** é o arquivo principal do trabalho, o qual une grande parte dos diversos processos utilizados para a geração da base que será descrito em seguida...

**O processo ocorre da seguinte forma:**
1. No VVG Image Annotator [A. Dutta and A. Zisserman, “The via annotation software for images, audio and video,” in Proceedings of the 27th ACM International Conference on Multimedia, 2019, pp. 2276–2279.], as rotulações seguiram um padrão que foi seguido no código fonte. Na ferramente citada os campos de region_attributes foram descritos da seguinte forma: O atributo "info_type" foi usado para definir que tipo de informação o campo rotulado continha, caso o valor fosse "d" o campo era **d**efault do próprio layout do documento e não precisava ser alterado, caso fosse "p", ele continha uma informação **p**essoal e precisava ser apagado e substituído por outro texto. O campo "text_type" para casos de texto do layout também possuíam o valor "d", já para os textos pessoais continha o tipo de informação que deveria ser adicionado naquele campo, como por exemplo uma "data", um "rg" e etc. O campo "transcription" continha a transcrição do texto rotulado para os casos de texto do layout e apenas um "x" para textos pessoais, visto que essa informação seria substituída futuramente. 

Segue um exemplo de um campo do layout e um de informações pessoais.

``` "region_attributes": {"info_type":"d","text_type":"d","transcription":"NOME"} ```  
``` "region_attributes":{"info_type":"p","text_type":"data","transcription":"X"} ```

2. Após as rotulações serem concluídas, as imagens passam por um pré-processamento utilizando Tesseract-OCR, o qual identifica a posição que o documento está e o rotaciona para o sentido de 0 graus (leitura da esquerda para a direita) com o objetivo de facilitar a inserção dos textos fictícios.

3. As imagens rotacionadas juntamente com os seus arquivos de .json das rotulações são processadas, de modo que ao lermos o .json verificamos o tipo de texto que está presente em determinada área, caso seja pessoal apagamos, caso não, o ignoramos, visto que faz parte do layout do documento. Para apagar as informações pessoais, utilizamos duas possíveis abordagens, na primeira utilizamos a cor de pixel dominante na região do texto (que tende a ser parte do background), na segunda utilizamos um cálculo de pixel médio da região acima da área do texto. A escolha da abordagem para cada área fica de acordo com uma verificação de valores, caso o pixel médio seja maior que a cor dominante, utilizamos o pixel médio, caso contrário, a cor dominante.

4. Com todas as informações pessoais apagadas, a imagem resultante, contendo apenas o texto de layout e o *background* do documento, passa para a etapa de inserção dos texto falsos. Esse processo ocorre da seguinte forma: Uma máscara é criada com as mesmas proporções da imagem do documento, iteramos sobre os campos rotulados fazendo a checagem de qual texto deve ser inserido naquela área. O texto é criado e inserido em uma máscara temporária, a qual possui apenas o texto inserido naquele momento. Essa máscara é binarizada, passa por alguns processos de erosão e dilatação para que o contorno do texto seja identificado e mapeado para ser futuramente adicionado em um arquivo de *Ground Truth* (GT) e por fim o texto também é inserido na máscara inicialmente criada. Com todos os textos falsos criados e inseridos na máscara o processo segue para a próxima etapa.

5. A máscara passa por um pós-processamento para que os pixels da cor de fundo da máscara sejam inseridos na região de texto, o que remove a "opacidade" do texto fictício criado e deixa o documento final mais "real". A imagem com apenas o *background* do documento e a máscara com os novos textos são multiplicadas, de modo que todos os pixels diferentes da cor de fundo da máscara são adicionados na imagem.

6. Em meio ao processo de multiplicação das iamgens, os arquivos de GT são gerados. A área do novo texto que foi mapeado anteriormente pela máscara temporária, juntamente com o arquivo de rotulação, geram uma imagem totalmente preta com a região de texto em branco, para desafios de segmentação de texto. Além dessa imagem, essas informações são usadas para a escrita do arquivo .txt que contém as informações da posição do texto e sua transcrição para desafios de OCR.

Segue um exemplo da saída do .txt:

**x, y, width, height, transcription**
123, 120, 270, 8, BACELLAR SCHALLENMUELLER MALGUEIRO

Onde x e y indicam as coordenadas X e Y, respectivamente, da ponta superior esquerda do retângulo, *width* indica a largura do retângulo, *height* indica a altura do retângulo e *transcriptio* indica a transcrição do texto presente na área.

Para os casos em que o texto não é um retângulo perfeito, a saída é dada no seguinte formato:

**x, y, width, height, transcription**
[233, 232, 513, 514, 233], [41, 55, 57, 45, 42], -1, -1, MINISTÉRIO DAS CIDADES

Onde as coordenadas X e Y são dadas por uma sequência de pontos que formam o polígono que engloba o texto. E os campos de altura e largura são dados como -1 para esses casos.

6. Após a multiplicação, a imagem final é obtida e passa por um *data augmentation*, gerando a partir dela imagens com diferentes contrastes, brilhos, ruídos e etc.

7. Finalizando o processo, a imagem é salva no diretório definido.


### OBS.:
1. O arquivo find_face.py é um script que usa um modelo de reconhecimento de rostos pré-treinado [D. E. King, “Max-margin object detection,” arXiv preprint arXiv:1502.00046, 2015.] ,disponível no diretório "files" deste trabalho, para reconhecer os rostos nos documentos e realizar um *blur* na região. O mesmo não está diretamente interligado com o processo de geração da base, mas foi utilizado para o resultado final.
2. Já o arquivo paths.py possui apenas a assinatura de um diretório utilizado no projeto para evitar a sua repetição ao longo do desenvolvimento. 
