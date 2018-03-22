import glob
import os
import shutil

IN_DIR = 'C:\\Users\\mbargury\\Downloads\\New\\Slowmotion_180322_160952\\JPG\\'
OUT_DIR = 'C:\\Users\\mbargury\\Downloads\\New\\Slowmotion_180322_160952\\FILTERED_JPG\\'
EXT = '.jpg'

# locate in files
files = glob.glob(os.path.join(IN_DIR, '*%s' % EXT))

# create out dir
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# move wanted files
for f in files:
    if (('FrameID(02)' in f) or
       ('FrameID(04)' in f) or
       ('FrameID(06)' in f)):
        shutil.copyfile(f, os.path.join(OUT_DIR, os.path.basename(f)))

print('DONE')