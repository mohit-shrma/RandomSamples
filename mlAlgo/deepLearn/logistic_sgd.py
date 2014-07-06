import cPickle
import gzip
import os
import sys
import time
import numpy

import theano
import theano.tensor as T

class LogisticRegression(object):

  def __init__(self, input, n_in, n_out):
    #initialiae weights and b
    self.W = theano.shared(value=numpy.zeros((n_in, n_out),
      dtype=theano.config.floatX), name='W' )
    self.b = theano.shared(value=numpy.zeros((n_out,),
      dtype=theano.config.floatX), name = 'b' ) 
    
    #compute class membership prob in symbolic form
    self.p_y_given_x = T.nnet.softmax(T.dot(input, self.W) + self.b)
    
    #compute prediction in symbolic form
    self.y_pred = T.argmax(self.p_y_given_x, axis=1)
    
    #parameters of model
    self.params = [self.W, self.b]

  def negative_log_likelihood(self, y):
    return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])

  def errors(self, y):
    if y.ndim != self.y_pred.ndim:
        raise TypeError('y should have same shape as self.y_pred', ('y',
          target.type, 'y_pred', self.y_pred.type))
    if y.dtype.startswith('int'):
      return T.mean(T.neq(self.y_pred, y))
    else:
      raise NotImplementedError()

def load_data(dataset):
  #download MNIST dataset if not present
  data_dir, data_file = os.path.split(dataset)
  if data_dir == "" and not os.path.isfile(dataset):
    #check for data in current dir
    new_path = os.path.join(os.path.split(__file__)[0], "..", "data", dataset)
    if os.path.isfile(new_path) or data_file == 'mnist.pk1.gz':
      dataset = new_path

  if (not os.path.isfile(dataset)) and data_file == 'mnist.pk1.gz':
    import urllib
    origin = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
    print 'Downloading data from %s' % origin
    urllib.urlretrieve(origin, dataset)

  print '... loading data'

  #load dataset
  f = gzip.open(dataset, 'rb')
  train_set, valid_set, test_set = cPickle.load(f)
  f.close()

  #train_set, valid_set, test_set format: tuple(input, target)
  #input is an numpy.ndarray of 2 dimensions (a matrix)
  #witch row's correspond to an example. target is a
  #numpy.ndarray of 1 dimensions (vector)) that have the same length as
  #the number of rows in the input. It should give the target
  #target to the example with the same index in the input.
  
  def shared_dataset(data_xy, borrow=True):
    #storedataset in shared variable for copying in to GPU
    data_x, data_y = data_xy
    shared_x = theano.shared(numpy.asarray(data_x, dtype=theano.config.floatX),
        borrow=borrow)
    shared_y = theano.shared(numpy.asarray(data_y, dtype=theano.config.floatX),
        borrow=borrow)
    return shared_x, T.cast(shared_y, 'int32')

  test_set_x, test_set_y = shared_dataset(test_set)
  valid_set_x, valid_set_y = shared_dataset(valid_set)
  train_set_x, train_set_y = shared_dataset(train_set)

  rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y), (test_set_x,
    test_set_y)]
  return rval


def sgd_optimization_mnist(learning_rate=0.13, n_epochs=1000,
    dataset='mnist.pkl.gz', batch_size=600):
  #load datasets
  datasets = load_data(dataset)
  train_set_x, train_set_y = datasets[0]
  valid_set_x, valid_set_y = datasets[1]
  test_set_x, test_set_y = datasets[2]

  #compute number of minibatches for training, validation and testing
  n_train_batches = train_set_x.get_value(borrow=True).shape[0]/batch_size
  n_valid_batches = valid_set_x.get_value(borrow=True).shape[0]/batch_size
  n_test_batches = test_set_x.get_value(borrow=True).shape[0]/batch_size

  print 'building the model'

  #allocate symbolic variables for the data
  #index to mini batch
  index = T.lscalar()
  #images
  x = T.matrix('x')
  #labels
  y = T.ivector('y')

  #construct classifier
  classifier = LogisticRegression(input=x, n_in=28*28, n_out=10)

  #minimize -ve log likelihood cost in symbolic format
  cost = classifier.negative_log_likelihood(y)
  
  #compile theano function that computes mistakes made by model on minibatch
  test_model = theano.function(inputs=[index], outputs=classifier.errors(y),
      givens={x: test_set_x[index * batch_size: (index + 1) * batch_size], 
              y: test_set_y[index * batch_size: (index + 1) * batch_size]})

  validate_model = theano.function(inputs=[index], outputs=classifier.errors(y),
      givens={x: valid_set_x[index * batch_size: (index + 1) * batch_size], 
              y: valid_set_y[index * batch_size: (index + 1) * batch_size]})

  #compute gradient of cost w.r.t theta= (W,b)
  g_W = T.grad(cost=cost, wrt=classifier.W)
  g_b = T.grad(cost=cost, wrt=classifier.b)

  #specify how to update parameters
  updates = [(classifier.W, classifier.W - learning_rate * g_W), 
             (classifier.b, classifier.b - learning_rate * g_b)]

  #function that returns cost and at same time updates parameter of model
  train_model = theano.function(inputs=[index], outputs=cost, updates=updates,
      givens={x: train_set_x[index * batch_size: (index + 1) * batch_size], 
              y: train_set_y[index * batch_size: (index + 1) * batch_size]})

  print '... training the model'
  #early-stopping parametrs
  #look at least these many examples
  patience = 5000
  #wait this much longer when new best found
  patience_increase = 2   
  #a relative improvement of this much is significant
  improvement_threshold = 0.995
  #go through this many minibatches b4 checking on validation set
  validation_frequency = min(n_train_batches, patience/2)

  best_params = None
  best_validation_loss = numpy.inf
  test_score = 0
  start_time = time.clock()

  done_looping = False
  epoch = 0

  while (epoch < n_epochs) and (not done_looping):
    epoch += 1
    for minibatch_index in xrange(n_train_batches):
        minibatch_avg_cost= train_model(minibatch_index)
        #iteration no.
        iter = (epoch - 1) * n_train_batches + minibatch_index

        if (iter + 1) % validation_frequency == 0:
          #0-1 loss on validation set
          validation_losses = [validate_model(i) for i in xrange(n_valid_batches)]
          this_validation_loss = numpy.mean(validation_losses)
          print('epoch %i, minibatch %i/%i, validation error %f %%' % (epoch,
            minibatch_index + 1, n_train_batches, this_validation_loss*100))

          #if found best validation score
          if this_validation_loss < best_validation_loss:
            #improve patience
            if this_validation_loss < best_validation_loss * improvement_threshold:
                patience = max(patience, iter * patience_increase)

            best_validation_loss = this_validation_loss

            #test it on test set
            test_losses = [test_model(i) for i in xrange(n_test_batches)]
            test_score = numpy.mean(test_losses)

            print(('epoch %i, minibatch %i/%i, test error of best model %f %%')%
                   (epoch, minibatch_index+1, n_train_batches, test_score*100))
  
        if patience <= iter:
          done_looping = True
          break

  end_time = time.clock()
  print(('optimization completed with best validation score of %f %%'
         'with test performance %f %%') % 
         (best_validation_loss * 100.0, test_score * 100.0))
  print ('code run for %d epochs, with %f epochs/sec' % 
        (epoch, 1.*epoch/(end_time - start_time) ))
  print >> sys.stderr, ('The code for file ' + os.path.split(__file__)[1] + \
                        'ran for %.1fs' % ((end_time -start_time)))

if __name__ == '__main__':
  sgd_optimization_mnist()

