import glob
import os

DIR = 'C:\\Users\\mbargury\\Downloads\\ezra\\output1\\'

# locate in files
slowmo = [215, 244]
slowmo_fr = 30

for i in range(1094):
    if 180 < i < 280:
        continue

    if i > 400:
        if i % 8 != 0:
            os.remove('%simg%d.jpg' % (DIR, i))
        else:
            continue

    if i < 400:
        if i % 5 != 0:
            os.remove('%simg%d.jpg' % (DIR, i))
        else:
            continue

print('DONE')