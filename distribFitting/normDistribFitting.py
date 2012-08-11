from scipy.stats import norm
from numpy import linspace
from pylab import plot, show, hist, figure, title

""" trying to see how to fit a normal distribution on a data using scipy 
reference : glowingpython.blogspot.it """

#picking 150 samples from a normal distribution with mean 0 and standard dev 1
samp = norm.rvs(loc=0, scale = 1, size = 150)

#distribution fitting, 
#param[0] & param[1] are mean and std. dev of fitted distribution
param = norm.fit(samp)

#generate points on x-axis to plot
x = linspace(-5, 5, 100)

#find the y-axis points for fitted distribution
pdf_fitted = norm.pdf(x, loc=param[0], scale=param[1])

#get the y-axis points for original distribution with mean 0 and standard dev 1
pdf = norm.pdf(x)

title('Normal Distribution')

#plot fitted distribution and original distribution
plot(x, pdf_fitted, 'r-', x, pdf, 'b-')

#plot the histogram of picked samples from distribution. normalized
hist(samp, normed=1, alpha=0.3)

show()


