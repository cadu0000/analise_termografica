from PIL import Image

def is_radiometric_jpeg(img_path):
    img = Image.open(img_path)
    
    if img.mode == "L":
        depth = 8  
    elif img.mode == "RGB":
        depth = 24 
    else:
        depth = None
    
    return depth


img_path = ""

depth = is_radiometric_jpeg(img_path)

if depth is not None:
    print(f"A profundidade de bits da imagem é {depth}.")
    if depth > 8:
        print("A imagem provavelmente é radiométrica.")
    else:
        print("A imagem provavelmente não é radiométrica.")
else:
    print("Não foi possível determinar a prof")
