import os
from pathlib import Path
from time import strftime
from PIL import Image, ImageChops

dirname = os.path.dirname(__file__)
mask_filename = os.path.join(dirname, 'skintemplate_masked_alpha.png')
save_folder = os.path.join(os.getcwd(), f'/tmp/multiskin/cleaned')

def remove_second_skin_layer(skin_img: Image.Image) -> Image.Image:
    skin_converted = skin_img.convert('RGBA')
    MASK_IMG = Image.open(mask_filename)
    MASK_IMG_converted = MASK_IMG.convert('RGBA')
    masked_img = ImageChops.multiply(skin_converted, MASK_IMG_converted)
    return masked_img

def clean_skin(skin: Image.Image, save: bool = False) -> Image.Image:
    ''' Takes a 64x64 skin and cleans it (removes second layer). '''
    if skin.size == (64, 64):
        cleaned_skin = remove_second_skin_layer(skin)
        if save:
            currtime = strftime("%Y%m%d-%H%M%S")
            if not os.path.isdir(save_folder):
                os.makedirs(save_folder)
            skin_filename = os.path.basename(skin.filename)
            cleaned_skin.save(f"{save_folder}/{skin_filename}_{currtime}.png")
        return cleaned_skin
    else:
        print("Wrong size, skipping.")


if __name__ == "__main__":
    EMPTY_IMG = Image.open(mask_filename)
    clean_skin(EMPTY_IMG, True)