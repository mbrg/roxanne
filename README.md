# roxanne


### calibration script
to run, write
`python calibrate.py --square_size 25 --threads 10  'location_of_images/*.jpg'`
it will save the data to calibration.yaml

to pull the information:
```
import yaml
with open('calibration.yaml') as f:
    loadeddict = yaml.load(f)

mtxloaded = loadeddict.get('camera_matrix')
distloaded = loadeddict.get('dist_coeff')
```
