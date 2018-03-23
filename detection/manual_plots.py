

from detection.haar import video
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
d=2
plt.clf()
img_cache, pix_cache, euc_cache=video(100)
if d==3:

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    _ = ax.scatter3D(euc_cache[:,0], euc_cache[:,1], euc_cache[:,2])
else:
    plt.scatter(x=euc_cache[:,0], y=euc_cache[:,1])
plt.show()