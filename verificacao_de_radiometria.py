from PIL import Image

def is_radiometric_jpeg(img_path):
    img = Image.open(img_path)
    
    if img.mode == "L":
        depth = 8  # Imagem em tons de cinza
    elif img.mode == "RGB":
        depth = 24  # Imagem colorida
    else:
        depth = None
    
    return depth

# Caminho para a imagem
sensibilidade_termica = 0.15 #em graus ou 150mk
img_path = "1.jpeg"

# Verifica se a imagem é radiométrica
depth = is_radiometric_jpeg(img_path)

# Exibe o resultado
if depth is not None:
    print(f"A profundidade de bits da imagem é {depth}.")
    if depth > 8:
        print("A imagem provavelmente é radiométrica.")
    else:
        print("A imagem provavelmente não é radiométrica.")
else:
    print("Não foi possível determinar a prof")
