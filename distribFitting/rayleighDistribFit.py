from scipy.stats import norm, rayleigh
from numpy import linspace
from pylab import plot, show, hist, figure, title


""" here we try to fit rayleigh distribution to data
reference: glowingpython.blogspot.it"""

#generate 150 samples from a rayleigh distribution of mean 5 and std dev 2
samp = rayleigh.rvs(loc=5, scale=2, size=150)

#fit rayleigh distibution to generated samples
#param[0] & param[1] are mean and std. dev of fitted distribution
param = rayleigh.fit(samp)

#generate points on x-axis to plot
x = linspace(5, 13, 100)

#get the points on y-axis for fitted distribution
pdf_fitted = rayleigh.pdf(x, loc=param[0], scale=param[1])

#get the points on y-axis for original distribution
pdf = rayleigh.pdf(x, loc=5, scale=2)

title('Rayleigh distribution')
#plot the fitted distribution and original distribution
plot(x, pdf_fitted, 'r-', x, pdf, 'b-')
#histogram of normalized samples generated from rayleigh distribution
hist(samp, normed=1, alpha=0.3)

show()
