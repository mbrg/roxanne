# Roxanne


### Approach

We use an AdaBoost model to detect the ball, confine it with a rectangle. This gives us the pixel-coordinates of the ball at each frame.
Next, we estimate the distance between the camera and the ball. This is done by estimating the ball's radius in the image, and comparing it with it's known radius, and plugging these into simple optics equations.

<image with ball detections>

Projective geometry helps us to translate the ball's coordinates into the Euclidean 3D plane, where we can use well-known Physics to find the ball's expected trajectory. Using Projective geometry once more, we translate these trajectories back to the pixel-space.
At the end of this stage, we can estimate the ball's expected trajectory accross the frame. We know where the ball should go.

In sports, a lot of times the most interesting things are the ones things don't do what we expect them to. A Basketball shot gets blocked, a Soccer ball hits the goalie's hands just before eaching the goal. We use anomaly detection to find the exact points where the ball stops moving in it's expected trajencotry, and triger a slow-motion sensor to capture the event.

<gif>


### Calibration
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
