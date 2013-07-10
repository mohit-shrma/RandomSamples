import numpy as np
import matplotlib.pyplot as plt

linearKernel = lambda x, y : np.dot(x,y)
brownianKernel = lambda x, y: min(x,y)
expKernel = lambda x, y: 1*np.exp(-1*np.square(x-y))

kernel = expKernel

#sample points
n = 200
x = np.linspace(0, 1, n)

#construct covaraince matrix
cov = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        cov[i][j] = kernel(x[i], x[j])

#sample from gaussian process at these points

#sample u ~ N(0, I)
t = np.random.randn(n)

#factor cov matrix
U, s, V = np.linalg.svd(cov, full_matrices=True)
S = np.diag(s)
#z = U S^.S t ~ N(0, cov)
z = np.dot(np.dot(U,np.sqrt(S)), t)

plt.plot(x, z, '.-')
plt.show()


