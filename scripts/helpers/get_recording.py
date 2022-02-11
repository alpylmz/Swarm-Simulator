"""
import glob
from PIL import Image

# filepaths
fp_in = "figures/*.png"
fp_out = "image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=200, loop=0)
"""
""""""
import imageio
import os

path = 'figures/' # on Mac: right click on a folder, hold down option, and click "copy as pathname"

image_folder = os.fsencode(path)

filenames = []
"""
for file in os.listdir(image_folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpeg', '.png', '.gif') ):
        filenames.append(path + filename)
"""
for i in range(202):
    filenames.append("figures/{}.png".format(i))

images = list(map(lambda filename: imageio.imread(filename), filenames))

imageio.mimsave(os.path.join('movie.gif'), images, duration = 0.04) # modify duration as needed
