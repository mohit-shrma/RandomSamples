import cPickle
import gzip
import os
import sys
import time
import numpy
 
import theano
import theano.tensor as T
 
from logistic_sgd import LogisticRegression, load_data

class HiddenLayer(object):
  """Typical hidden layer of a MLP: units are fully-connected and have
     sigmoidal activation function. Weight matrix W is of shape (n_in,n_out)
    and the bias vector b is of shape (n_out,)."""
  def __init__(self, rng, input, n_in, n_out, W=None, b=None, activation=T.tanh):
    self.input = input
    
    #optimal initialization of weights depend on activation function here it is
    #tanh or sigmoid
    if W is None:
      W_values = numpy.asarray(rng.uniform(low=-numpy.sqrt(6. / (n_in + n_out)),
                                         high=numpy.sqrt(6. / (n_in + n_out)), 
                                         size=(n_in, n_out)),
                               dtype=theano.config.floatX)       

      if activation == theano.tensor.nnet.sigmoid:
        W_values *= 4

      W = theano.shared(value=W_values, name='W')

  
    if  b is None:
      b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
      b = theano.shared(value=b_values, name='b')

    self.W = W
    self.b = b
    
    lin_output = T.dot(input, self.W) + self.b 
    self.output = (lin_output if activation is None 
                    else activation(lin_output))
    #model parameters
    self.params = [self.W, self.b]


class MLP(object):
  """ Multi-layer perceptron class"""

  def __init__(self, rng, input, n_in, n_hidden, n_out):
    #in this implementation there is only one hidden layer connected to logistic
    #regression layer
    self.hiddenLayer = HiddenLayer(rng=rng, input=input, n_in=n_in,
                                    n_out=n_hidden, activation=T.tanh)
    #input to logistic regression layer are hidden units of hidden layer
    self.logRegressionLayer = LogisticRegression(input=self.hiddenLayer.output,
                                                  n_in=n_hidden, n_out=n_out)
    #regularization to keep L1 and L2 norm small
    self.L1 = abs(self.hiddenLayer.W).sum() \
               + abs(self.logRegressionLayer.W.sum())
    self.L2_sqr = (self.hiddenLayer.W ** 2).sum() \
                   + (self.logRegressionLayer.W ** 2).sum()

    #negative log likelihood of multi layer perceptron equals negative log
    #likelihood of output of model in logistic regression layer
    self.negative_log_likelihood = self.logRegressionLayer.negative_log_likelihood
    #similarly the error are given by logistic regression layer
    self.errors = self.logRegressionLayer.errors
    
    #parameters of model are the parameter of all layers
    self.params = self.hiddenLayer.params + self.logRegressionLayer.params

def test_mlp(learning_rate=0.01, L1_reg=0.0, L2_reg=0.0001, n_epochs=1000,
    dataset='mnist.pkl.gz', batch_size=20, n_hidden=500):
  """SGD optimization for multilayer perceptron"""
  datasets = load_data(dataset)

  train_set_x, train_set_y = datasets[0]
  valid_set_x, valid_set_y = datasets[1]
  test_set_x, test_set_y   = datasets[2]

  #compute number of minibatches for training, validation and testing
  n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
  n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size  
  n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size

  print '... building model'

  #symbolic variables for data
  #index to mini batch
  index = T.lscalar()
  #data as images
  x = T.matrix('x')
  #labels as vector
  y = T.ivector('y')

  rng = numpy.random.RandomState(1234)

  #construct the MLP class
  classifier = MLP(rng=rng, input=x, n_in=28*28, n_hidden=n_hidden, n_out=10)

  #cost to be minimize is -ve log likelihood of model plus regularization
  #symbolically
  cost = classifier.negative_log_likelihood(y) + L1_reg * classifier.L1 \
          + L2_reg * classifier.L2_sqr

  #theano function to compute mistakes made by model
  test_model = theano.function(inputs=[index], outputs=classifier.errors(y),
      givens={x: test_set_x[index * batch_size: (index + 1) * batch_size], 
              y: test_set_y[index * batch_size: (index + 1) * batch_size]})

  validate_model = theano.function(inputs=[index], outputs=classifier.errors(y),
      givens={x: valid_set_x[index * batch_size: (index + 1) * batch_size], 
              y: valid_set_y[index * batch_size: (index + 1) * batch_size]})

  #compute gradient of cost w.r.t model parameters
  gparams = []
  for param in classifier.params:
    gparam = T.grad(cost, param)
    gparams.append(gparam)

  #specify how to update parameters of model as list of 
  #(variable, update_expression) pairs
  updates = []
  for param, gparam in zip(classifier.params, gparams):
    updates.append((param, param - learning_rate * gparam))

  #theano function to trian model that returns cost and also update the model
  train_model = theano.function(inputs=[index], outputs=cost, updates=updates,
      givens={x: train_set_x[index * batch_size: (index + 1) * batch_size], 
              y: train_set_y[index * batch_size: (index + 1) * batch_size]})

  print '... training'
  
  #early-stopping parameters
  #look at least these samples
  patience = 10000
  #wait longer when new best found
  patience_increase = 2
  #relative improvement of following is significant
  improvement_threshold = 0.995
  #atleast go through these batches b4 checking on validation set
  validation_frequency = min(n_train_batches, patience / 2)

  best_params          = None
  best_validation_loss = numpy.inf
  best_iter            = 0
  test_score           = 0.
  start_time           = time.clock()

  epoch = 0
  done_looping = False

  while (epoch < n_epochs) and (not done_looping):
    epoch = epoch + 1
    for minibatch_index in xrange(n_train_batches):
      minibatch_avg_cost = train_model(minibatch_index)
      #iteration number
      iter = (epoch - 1) * n_train_batches + minibatch_index

      if (iter + 1) % validation_frequency == 0:
        #compute 0/1 loss on validation set
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
          best_iter = iter

          #test it on test set
          test_losses = [test_model(i) for i in xrange(n_test_batches)]
          test_score  = numpy.mean(test_losses)

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
                        'ran for %.2fm' % ((end_time -start_time)/60.))

if __name__ == '__main__':
  test_mlp()    


  






  





   
  





