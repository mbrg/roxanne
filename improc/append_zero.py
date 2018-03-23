import glob
import os
import shutil

DIR = 'C:\\Users\\mbargury\\Downloads\\ezra\\'
EXT = '.jpg'

# locate in files
files = glob.glob(os.path.join(DIR, '*%s' % EXT))

def intable(x):
    try:
        _ = int(x)
    except ValueError:
        return False
    else:
        return True

# append zeros where needed
for f in files:
    num_ints = len([c for c in f if intable(c)])
    if num_ints == 3:
        new_f = '%s0%s' % (f[:-7], f[-7:])
        shutil.move(f, new_f)

print('DONE')