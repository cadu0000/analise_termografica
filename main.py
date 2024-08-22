import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import pandas as pd
from numpy import asarray

## Verifica se os valores de temperatura estão presentes nos metadados da imagem
def metadata (image):
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")

def encontrar_ponto_medio(img):
    with Image.open(imagem_base) as img:
        largura, altura = img.size
        ponto_medio = (largura // 2, altura // 2)
        return ponto_medio

def redimensionar ():
    with Image.open(imagem_base) as img:
        img_redimensionada = img.resize((80, 60))
        img_redimensionada.save(f"{base}redimensionada.jpg") 
        return (f"{base}redimensionada.jpg")
  
def get_position(df, dados):
    for index, row in df.iterrows():
        for column in df.columns:
            valor = row[column]
            posicao = (index, column)

            if valor >= 40:
                classificacao = 3  
            elif valor >= 25:
                classificacao = 2 
            elif valor >= 15:
                classificacao = 1  
            else:
                classificacao = 0 
                
            dado = {
                "temperatura": valor,
                "posicao": posicao,
                "classificacao": classificacao
            }
            dados.append(dado)

base = "" 
ext = ".jpg"
imagem_base = base + ext
image = PIL.Image.open(imagem_base)

metadata(image)
imagem_base = redimensionar()
ponto_medio = encontrar_ponto_medio(imagem_base)
imagem_acinzentada = cv2.imread(imagem_base, cv2.IMREAD_ANYDEPTH)

tons_cinza = asarray(imagem_acinzentada)
tons_cinza_min = tons_cinza.min() 
tons_cinza_max = tons_cinza.max() 

tons_cinza_corrigido = (tons_cinza - tons_cinza_min) * (1/(tons_cinza_max - tons_cinza_min)) 

tmin = 15
tmax = 55
temperatura = tmin + (tons_cinza_corrigido) * (tmax - tmin)

dest = base + "_temp_mx.xlsx"
df = pd.DataFrame (temperatura)

dados = []

get_position(df, dados)

final_df = pd.DataFrame(dados)
final_df.to_excel(dest, index=False)
