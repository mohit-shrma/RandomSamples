from pylab import scatter, text, show, cm, figure
from pylab import subplot, imshow, NullLocator
from sklearn import manifold, datasets

""" reference: http://glowingpython.blogspot.it/2012/05/manifold-learning-on-handwritten-digits.html 
try to apply isomap algo to seek a lower dimensional embedding of a set of high dimensional data points estimating the intrinsic geometry of a data manifold based on a rough estimate of each data point """

#load the digits dataset, (0, 1, 2, 3, 4)
digits = datasets.load_digits(n_class=5)

#get the digit X dataVector, i.e. data set or kind of unique vector 
#obtained by spatial resampling on each image
X = digits.data

#actual digit text text corresponding to each row, ('0','1','1','0', ...) 
color = digits.target

#display some digits
figure(1)
for i in range(36):
    ax = subplot(6, 6, i)
    ax.xaxis.set_major_locator(NullLocator())
    ax.yaxis.set_major_locator(NullLocator())
    imshow(digits.images[i], cmap=cm.gray_r)

#display a sample data vector for a digit
print X[0].shape  #vector of length 64
print X[0]

#run isomap algorithm (non-linear dimensionality reduction), 
#to reduce 64 attributes to 2
#5 neighbours will be considered and reduction on a 2d space/2 components
Y = manifold.Isomap(5, 2).fit_transform(X)

#plot the result 
figure(2)

#generate the scatter plot for the result
scatter(Y[:,0], Y[:,1], c='k', alpha=0.3, s=10)

#for each reduced component, plot the label of digit
for i in range(Y.shape[0]):
    text(Y[i, 0], Y[i, 1], str(color[i]),\
             color=cm.Dark2(color[i]/5.),\
             fontdict={'weight':'bold', 'size':11})
show()

