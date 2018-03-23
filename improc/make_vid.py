
image_folder = 'C:\\Users\\mbargury\\Downloads\\ezra\\output1'
gif_name = 'C:\\Users\\mbargury\\Downloads\\ezra\\output1\\g.gif'

from PIL import Image
import os
import glob

import matplotlib.pyplot as plt
from matplotlib import animation, rc

file_names = sorted(glob.glob('C:\\Users\\mbargury\\Downloads\\ezra\\output1\\img*.jpg'))
images = [Image.open(fn) for fn in file_names]


def update(frame):
    return images[frame]

fig = plt.figure(figsize=(15,8))
anim = animation.FuncAnimation(fig, update,
                               interval=1, blit=True)

writer = animation.ImageMagickFileWriter(fps=120)
anim.save(gif_name, writer=writer)