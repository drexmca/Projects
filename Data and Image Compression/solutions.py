# solutions.py
from scipy import linalg as la
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib import cm
from copy import deepcopy

# Problem 1
def truncated_svd(A,r=None,tol=10**-6):
    """Computes the truncated SVD of A. If r is None or equals the number 
        of nonzero singular values, it is the compact SVD.
    Parameters:
        A: the matrix
        r: the number of singular values to use
        tol: the tolerance for zero
    Returns:
        U - the matrix U in the SVD
        s - the diagonals of Sigma in the SVD
        Vh - the matrix V^H in the SVD
    """
    m, n = A.shape
    A_h = np.dot(A.conj().T, A)
    e_vals, e_vec = la.eig(A_h)
    e_vec = e_vec.T
    sorted_index = np.argsort(e_vals)
    sorted_index = sorted_index[::-1]
    sorted_values = np.zeros(len(e_vals))
    sorted_vectors = np.zeros((e_vec.shape))
    for i, index in enumerate(sorted_index):
        sorted_values[i] = e_vals[index]
        sorted_vectors[i] = e_vec[i]
    if r == None:
        r = 0
        for val in e_vals:
            if not np.isclose(val, 0):
                r+=1
    sorted_values = sorted_values[:r]
    sorted_vectors = sorted_vectors[:r]
    singular_values = np.sqrt(sorted_values)
    s = np.diagflat(singular_values)
    U = np.zeros((m,r))
    for i, vector in enumerate(sorted_vectors):
        U[:,i] = 1./singular_values[i] * np.dot(A, vector.T)

    V_h = sorted_vectors.conj()

    return U, s, V_h


# Problem 2
def visualize_svd():
    """Plot each transformation associated with the SVD of A."""
    A = np.array([[3,1],[1,3]])
    U, s , V_h = truncated_svd(A)
    circle_pts = np.load('circle.npz')['circle']
    V_h_circle_pts = np.dot(V_h, circle_pts)
    s_circle_pts = np.dot(s, np.dot(V_h, circle_pts))
    U_circle_pts = np.dot(U, np.dot(s, np.dot(V_h, circle_pts)))
    unit_vecs = np.load('circle.npz')['unit_vectors']
    V_h_unit_vecs = np.dot(V_h, unit_vecs)
    s_unit_vecs = np.dot(s, np.dot(V_h, unit_vecs))
    U_unit_vecs = np.dot(U, np.dot(s, np.dot(V_h, unit_vecs)))
    data = [(circle_pts, unit_vecs), (V_h_circle_pts, V_h_unit_vecs), (s_circle_pts, s_unit_vecs), (U_circle_pts, U_unit_vecs)]
    for i, combo in enumerate(data):
        x = []
        y = []
        for j, x_dat in enumerate(combo[0][0]):
            x.append(x_dat)
            y.append(combo[0][1][j])
        plt.subplot(2, 2, i+1)
        plt.plot(x, y)
        plt.plot(combo[1][0], combo[1][1])
    
    plt.show()
    pass
 
# Problem 3
def svd_approx(A, k):
    """Returns best rank k approximation to A with respect to the induced 2-norm.
    
    Inputs:
    A - np.ndarray of size mxn
    k - rank 
    
    Return:
    Ahat - the best rank k approximation
    """
    U,s,V_h = la.svd(A, full_matrices=False)
    S = np.diag(s[:k])
    A_k = U[:,:k].dot(S).dot(V_h[:k,:])
    return A_k 

# Problem 4
def lowest_rank_approx(A,error):
    """Returns the lowest rank approximation of A with error less than e 
    with respect to the induced 2-norm.
    
    Inputs:
    A - np.ndarray of size mxn
    e - error
    
    Return:
    Ahat - the lowest rank approximation of A with error less than e.
    """
    U,singular,V_h = la.svd(A, full_matrices=False)
    s=0
    while singular[s] > error:
        s+=1
    print 'rank: ', s-1
    return svd_approx(A, s-1)
        
# Problem 5
def compress_image(filename,k):
    """Plot the original image found at 'filename' and the rank k approximation
    of the image found at 'filename.'
    
    filename - jpg image file path
    k - rank
    """
    im1 = mpimg.imread(filename)
    A = svd_approx(im1[:,:,0].astype(float), k)
    B = svd_approx(im1[:,:,1].astype(float), k)
    C = svd_approx(im1[:,:,2].astype(float), k)
    A[A>255] = 255
    B[B>255] = 255
    C[C>255] = 255
    A[A<0] = 0
    B[B<0] = 0
    C[C<0] = 0
    im2 = np.dstack([A.astype(np.uint8),B.astype(np.uint8),C.astype(np.uint8)])
    plt.subplot(121)
    plt.imshow(im1)
    plt.title("Full Rank!!!!!")
    plt.subplot(122)
    plt.imshow(im2)
    plt.title("Rank {} Approx.".format(k))
    plt.show()
