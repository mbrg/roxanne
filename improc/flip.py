import glob
import os
from PIL import Image

DIR = 'C:\\Users\\mbargury\\Downloads\\New\\Slowmotion_180322_160952\\FILTERED_JPG\\'
EXT = '.jpg'

# locate in files
files = glob.glob(os.path.join(DIR, '*%s' % EXT))

# flip wanted images
for f in files:
    img = Image.open(f)
    img2 = img.rotate(180)
    img2.save(f)

print('DONE')