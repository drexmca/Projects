import numpy as np
import scipy.misc as sp
from matplotlib import pyplot as plt

def centered_difference_quotient(f,pts,h = 1e-5):
    '''
    Compute the centered difference quotient for function (f)
    given points (pts).
    Inputs:
        f (function): the function for which the derivative will be approximated
        pts (array): array of values to calculate the derivative
    Returns:
        centered difference quotient (array): array of the centered difference
            quotient
    '''
    Df_app = lambda x: .5*(f(x+h)-f(x-h))/h
    d = np.zeros((len(pts)))
    for i, p in enumerate(pts):
        d[i] = np.abs(Df_app(p)-sp.derivative(f, p))
    return Df_app(pts)



def jacobian(f,n,m,pt,h = 1e-5):
    '''
    Compute the approximate Jacobian matrix of f at pt using the centered
    difference quotient.
    Inputs:
        f (function): the multidimensional function for which the derivative
            will be approximated
        n (int): dimension of the domain of f
        m (int): dimension of the range of f
        pt (array): an n-dimensional array representing a point in R^n
        h (float): a float to use in the centered difference approximation
    Returns:
        Jacobian matrix of f at pt using the centered difference quotient.
    '''
    identity = np.identity(n)
    jacobian = np.zeros((m, n))
    for i in range(n):
        jacobian[:][i] = centered_difference_quotient(f,pt,h)
    return jacobian.T


def findError():
    '''
    Compute the maximum error of your jacobian function for the function
    f(x,y)=[(e^x)*sin(y)+y^3,3y-cos(x)] on the square [-1,1]x[-1,1].
    Returns:
        Maximum error of your jacobian function.
    '''
    diff = 0
    A= lambda x: np.array([[np.exp(x[0])*np.sin(x[1]), np.exp(x[0])*np.cos(x[1])+3*x[1]**2],[np.sin(x[0]), 3]])
    f= lambda x: np.array([np.exp(x[0])*np.sin(x[1])+ (x[1]**3),3*x[1]-np.cos(x[0])])
    x=np.linspace(-1,1,100)
    y=np.linspace(-1,1,100)
    for i in  x:
      for j in y:
        C=A([i,j])
        D=jacobian(f,2,2,[i,j])
        errormat = np.abs(C - D)
        if la.norm(errormat)> diff:
          diff=la.norm(errormat)
    return diff
    


def Filter(image, F):
    '''
    '''
    m, n = image.shape
    h, k = F.shape
    
    image_pad = np.zeros((m + h - 1, n + k - 1))
    image_pad[h/2 : -(h/2) , (k/2) : -(k/2)] = image
    
    C = np.empty_like(image)
    for i in xrange(n):
         for j in xrange(m):
             C[i, j] = np.sum(F * image_pad[i:i+h, j:j+k])
    return C

G =  np.array([[2.,  4.,  5.,  4.,  2.],
               [4.,  9.,  12., 9.,  4.],
               [5.,  12., 15., 12., 5.],
               [4.,  9.,  12., 9.,  4.],
               [2.,  4.,  5.,  4.,  2.]])

G = (1./159) * G

S =  np.array([[-1.,0.,1.],[-2.,0.,2.],[-1.,0.,1.]])
S = (1./8) * S

def sobelFilter(image):
    '''
    '''
    image1 = Filter(image, S)
    image2 = Filter(image, S.T)
    grad = np.sqrt(image1**2 + image2**2  )
    mean = np.mean(grad) * 4
    return grad > mean

sobelFilter('cameraman.png')

