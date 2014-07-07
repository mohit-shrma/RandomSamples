import cPickle
import gzip
import os
import sys
import time
import numpy
 
import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams 

from logistic_sgd import load_data
from utils import tile_raster_images

import PIL.Image



class AutoEncoder(object):

  def __init__(self, numpy_rng, input=None, n_visible=784, n_hidden=500, W=None,
      bhid=None, bvis=None) :

    self.n_visible = n_visible
    self.n_hidden = n_hidden

    if not W:
      initial_W = numpy.asarray(numpy_rng.uniform(
        low=-4 * numpy.sqrt(6. / (n_hidden + n_visible)), 
        high=4 * numpy.sqrt(6. / (n_hidden + n_visible)), 
        size=(n_visible, n_hidden)), dtype=theano.config.floatX)
      W = theano.shared(value=initial_W, name='W')

    if not bvis:
      bvis = theano.shared(value=numpy.zeros(n_visible,
                           dtype=theano.config.floatX), name='bvis')
    
    if not bhid:
      bhid = theano.shared(value=numpy.zeros(n_hidden,
                           dtype=theano.config.floatX), name='bvis')
    
    self.W = W
    self.b = bhid
    self.b_prime = bvis
    #using tied weights hence W_prime is W transpose
    self.W_prime = self.W.T
    
    if input == None:
      self.x = T.dmatrix(name='input')
    else:
      self.x = input

    self.params = [self.W, self.b, self.b_prime]


  def get_hidden_values(self, input):
    #values of hidden layer
    return T.nnet.sigmoid(T.dot(input, self.W) + self.b)

  def get_reconstructed_input(self, hidden):
    #reconstructed input given values of hidden layer
    return T.nnet.sigmoid(T.dot(hidden, self.W_prime) + self.b_prime)

  def get_cost_updates(self, learning_rate):
    #computes the cost and updates for one training step
    y = self.get_hidden_values(self.x)
    z = self.get_reconstructed_input(y)
    
    #sum over the size of a datapoint, if we are using minibatches, L will be a
    #vector, with one entry per example in minibatch
    L = -T.sum(self.x * T.log(z) + (1 - self.x)*T.log(1-z), axis=1)
    # L is now a vector, where each element is the cross-entropy cost of the
    # reconstruction of the corresponding example of the minibatch. We need to
    # compute the average of all these to get the cost of the minibatch

    cost = T.mean(L)

    #compute gradients of cost of denoising autoenc w.r.t its parameters
    gparams = T.grad(cost, self.params)

    #generate list of updates
    updates = []
    for param, gparam in zip(self.params, gparams):
      updates.append((param, param - learning_rate*gparams))

    return (cost, updates)


class dA(object):
  """Denoising Auto-Encoder class (dA)
    A denoising autoencoders tries to reconstruct the input from a corrupted
    version of itby projecting it first in a latent space and reprojecting it
    afterwards back in the input space.
  """
  def __init__(self, numpy_rng, theano_rng=None, input=None, n_visible=784, 
      n_hidden=500, W=None, bhid=None, bvis=None) :

    self.n_visible = n_visible
    self.n_hidden = n_hidden

    if not W:
      initial_W = numpy.asarray(numpy_rng.uniform(
        low=-4 * numpy.sqrt(6. / (n_hidden + n_visible)), 
        high=4 * numpy.sqrt(6. / (n_hidden + n_visible)), 
        size=(n_visible, n_hidden)), dtype=theano.config.floatX)
      W = theano.shared(value=initial_W, name='W')

    if not bvis:
      bvis = theano.shared(value=numpy.zeros(n_visible,
                           dtype=theano.config.floatX), name='bvis')
    
    if not bhid:
      bhid = theano.shared(value=numpy.zeros(n_hidden,
                           dtype=theano.config.floatX), name='bvis')
    
    self.W = W
    self.b = bhid
    self.b_prime = bvis
    #using tied weights hence W_prime is W transpose
    self.W_prime = self.W.T
    self.theano_rng = theano_rng    
    if input == None:
      self.x = T.dmatrix(name='input')
    else:
      self.x = input

    self.params = [self.W, self.b, self.b_prime]


  def get_hidden_values(self, input):
    #values of hidden layer
    return T.nnet.sigmoid(T.dot(input, self.W) + self.b)

  def get_reconstructed_input(self, hidden):
    #reconstructed input given values of hidden layer
    return T.nnet.sigmoid(T.dot(hidden, self.W_prime) + self.b_prime)

  def get_cost_updates(self, corruption_level, learning_rate):
    #computes the cost and updates for one training step
    tilde_x = self.get_corrupted_input(self.x, corruption_level)
    y = self.get_hidden_values(tilde_x)
    z = self.get_reconstructed_input(y)
   
    #sum over the size of a datapoint, if we are using minibatches, L will be a
    #vector, with one entry per example in minibatch
    L = -T.sum(self.x * T.log(z) + (1 - self.x)*T.log(1-z), axis=1)
    # L is now a vector, where each element is the cross-entropy cost of the
    # reconstruction of the corresponding example of the minibatch. We need to
    # compute the average of all these to get the cost of the minibatch

    cost = T.mean(L)

    #compute gradients of cost of denoising autoenc w.r.t its parameters
    gparams = T.grad(cost, self.params)

    #generate list of updates
    updates = []
    for param, gparam in zip(self.params, gparams):
      updates.append((param, param - learning_rate*gparam))

    return (cost, updates)

  def get_corrupted_input(self, input, corruption_level):
    #zero out randomly selected subset of size corruption_level
    #produce an array of 0s & 1s where 1 has a probability of 
    #1 - corruption_level and 0 with corruption_level
    return self.theano_rng.binomial(size=input.shape, n=1, p=1-corruption_level) * input


def test_dA(learning_rate=0.1, training_epochs=15, dataset='mnist.pkl.gz',
    batch_size=20, output_folder='dA_plots'):

  datasets = load_data(dataset)
  train_set_x, train_set_y = datasets[0]

  #no. of minibatches for training
  n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
  
  #allocate symbolic variables for data
  #index to minibatch
  index = T.lscalar()
  #data as rasterized images
  x = T.matrix('x')

  if not os.path.isdir(output_folder):
    os.makedirs(output_folder)
  os.chdir(output_folder)


  #building the model no corruption
  rng = numpy.random.RandomState(123)
  theano_rng = RandomStreams(rng.randint(2 ** 30))

  da = dA(numpy_rng=rng, theano_rng=theano_rng, input=x, n_visible=28*28,
          n_hidden=500)

  cost, updates = da.get_cost_updates(corruption_level=0., learning_rate=learning_rate)
  train_da = theano.function([index], cost, updates=updates, 
      givens = {x: train_set_x[index * batch_size: (index + 1) * batch_size]})

  start_time = time.clock()

  #training
  #go through training epochs
  for epoch in xrange(training_epochs):
    #go through training set
    c = []
    for batch_index in xrange(n_train_batches):
      c.append(train_da(batch_index))
    
    print (('Training epoch %d, cost %f') % (epoch, numpy.mean(c))) 
  
  end_time = time.clock()
  
  training_time = (end_time - start_time)
  print (('Training took %f minutes') % (training_time/60.))

  image = PIL.Image.fromarray(tile_raster_images(X=da.W.get_value(borrow=True).T,
              img_shape=(28, 28), tile_shape=(10, 10), tile_spacing=(1,1)))
  image.save('filters_corruption_0.png')

  #building model corruption 30%
  rng = numpy.random.RandomState(123)
  theano_rng = RandomStreams(rng.randint(2 ** 30))
  da = dA(numpy_rng=rng, theano_rng=theano_rng, input=x, n_visible=28*28,
      n_hidden=500)
  cost, updates = da.get_cost_updates(corruption_level=0.3,
      learning_rate=learning_rate)
  train_da = theano.function([index], cost, updates=updates, 
      givens = {x: train_set_x[index * batch_size: (index + 1) * batch_size]})
  start_time = time.clock()

  #training
  #go through training epochs
  for epoch in xrange(training_epochs):
    #go through training set
    c = []
    for batch_index in xrange(n_train_batches):
      c.append(train_da(batch_index))
  
  end_time = time.clock()
  training_time = end_time - start_time

  image = PIL.Image.fromarray(tile_raster_images(X=da.W.get_value(borrow=True).T,
              img_shape=(28, 28), tile_shape=(10, 10), tile_spacing=(1,1)))
  image.save('filters_corruption_30.png')

  os.chdir('../')


if __name__ == '__main__':
  test_dA()








