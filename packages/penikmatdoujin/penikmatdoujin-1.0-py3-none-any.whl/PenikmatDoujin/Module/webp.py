import os
from PIL import Image



def Convert_WEBP(file):
    out = file.replace("jpg", ".webp")
    with Image.open(file) as img:
        img.save(out, quality=75)
    size1 = os.path.getsize(file)
    size2 = os.path.getsize(out)
    if size1 > size2:
        os.remove(file)
    else:
        os.remove(out)