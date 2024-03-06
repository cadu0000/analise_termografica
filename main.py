import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import pandas as pd
import numpy as np
from numpy import asarray

def metadata ():
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")

def redimensionar ():
    with Image.open(imagem_base) as img:
        img_redimensionada = img.resize((80, 60))
        img_redimensionada.save(f"{base}redimensionada.jpg") 
        return (f"{base}redimensionada.jpg")
    
def encontrar_ponto_medio(img):
    with Image.open(imagem_base) as img:
        largura, altura = img.size
        ponto_medio = (largura // 2, altura // 2)
        return ponto_medio

base = "" 
ext = ".jpg"
imagem_base = base + ext

image = PIL.Image.open(imagem_base)

metadata()
imagem_base = redimensionar()
ponto_medio = encontrar_ponto_medio(imagem_base)

imagem_acinzentada = cv2.imread(imagem_base, cv2.IMREAD_ANYDEPTH)

tons_cinza = asarray(imagem_acinzentada)
tons_cinza_min = tons_cinza.min() 
tons_cinza_max = tons_cinza.max() 

tons_cinza_corrigido = (tons_cinza - tons_cinza_min) * (1/(tons_cinza_max - tons_cinza_min)) 

tmin = float(input("temperatura mínima da imagem: ")) 
tmax = float(input("temperatura máxima da imagem ")) 

temperatura = tmin + (tons_cinza_corrigido) * (tmax - tmin)

dest = base + "_temp_mx.xlsx"

df = pd.DataFrame (temperatura)
df.to_excel(dest, header = False, index=False)

planilha = pd.read_excel(dest)

for coluna in planilha.columns:
    for valor in planilha[coluna]:
        if valor > tmax or valor < tmin:
            print("Error")


print(ponto_medio)
