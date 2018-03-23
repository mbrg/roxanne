import glob
import os
import shutil

DIR = 'C:\\Users\\mbargury\\Downloads\\ezra\\output1\\'
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
    if num_ints < 5:
        new_f = '%s%s%s' % (f[:-(4 + num_ints - 1)], '00000'[:5-num_ints], f[-(4 + num_ints - 1):])
        shutil.move(f, new_f)

print('DONE')