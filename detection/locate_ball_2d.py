import numpy as np
from scipy import signal

def find_xyr(im):
    # main function. gets an R*C or R*C*3 image and returns a triple (x,y,r) or strongest circle
    ed=edge(im)
    max_lim=min(im.shape[0],im.shape[1],20)
    L=50
    rads=np.linspace(5,max_lim,L)
    xy=np.zeros((L,2))
    maxgr=np.zeros(L)
    for i in range(L):
        filt=circle_filter(rads[i])
        grade=signal.convolve2d(im,filt)
        xy[i]=np.unravel_index(grade.argmax(), grade.shape)-(np.array(filt.shape)-3)/2
        maxgr[i]=np.max(grade)
    imax=maxgr.argmax()
    return (*xy[imax],rads[imax]+.5)

def edge(im):
    # assumes im.shape==(height,length,1/3)
    # YUV/grayscale format
    if len(im.shape)==3:
        im=im[:,:,0]
    dx = np.abs(im[1:,:]-im[:-1,:])
    dy = np.abs(im[:,1:]-im[:,:-1])
    dx2=dx[1:,:]+dx[:-1,:]
    dy2=dy[:,1:]+dy[:,:-1]
    return dx2[:,1:-1]+dy2[1:-1,:]

def sinc(mat):
    return (1-.5*np.abs(mat))*(np.abs(mat)<4)

def  circle_filter(rad):
    r=int(rad+2)
    rng=np.arange(-r,r+1)
    x=np.tile(rng,(2*r+1,1))
    y=x.transpose()
    r2=x*x+y*y
    prox=(r2/rad-rad-1)
    return sinc(prox)

def simulate(siz,x,y,r):
    im=np.zeros(siz)
    a=np.linspace(0,6.3,50)
    circ=np.array([[x],[y]])+r*np.vstack([np.cos(a),np.sin(a)])+.5
    circ=circ.astype(int)
    im[circ[0],circ[1]]=1
    return im+.2*np.random.rand(*siz)
