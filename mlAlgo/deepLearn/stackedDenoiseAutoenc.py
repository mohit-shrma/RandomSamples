import cPickle
import gzip
import os
import sys
import time
import numpy
 
import theano
import theano.tensor as T


from theano.tensor.shared_randomstreams import RandomStreams

from logistic_sgd import LogisticRegression, load_data
from multiLayerPerceptron import HiddenLayer
from denoisingAutoenc import dA


class SdA(object):

  def __init__(self, numpy_rng, theano_rng=None, n_ins=784,
      hidden_layers_sizes=[500, 500], n_outs=10, corruption_levels=[0.1, 0.1]):
    self.sigmoid_layers = []
    self.dA_layers = []
    self.params = []
    self.n_layers = len(hidden_layers_sizes)

    assert self.n_layers > 0

    if not theano_rng:
      theano_rng = RandomStreams(numpy_rng.randint(2 ** 30))
    #symbolic variables for data
    self.x = T.matrix('x')
    self.y = T.ivector('y')

    for i in xrange(self.n_layers):
      if i == 0:
        input_size = n_ins
        layer_input = self.x
      else:
        input_size = hidden_layers_sizes[i-1]
        layer_input = self.sigmoid_layers[-1].output

      sigmoid_layer = HiddenLayer(rng=numpy_rng, input=layer_input, n_in=input_size,
          n_out=hidden_layers_sizes[i], activation=T.nnet.sigmoid)
      
      #add to our list of layers
      self.sigmoid_layers.append(sigmoid_layer)

      #declare thar parameters of sigmoid layers are parameters of StackedDAA
      #the visible biases in the dA are parameters of those dA but not the SdA
      self.params.extend(sigmoid_layer.params)

      #construct denoising autoencoder that shared weights with this layer
      dA_layer = dA(numpy_rng=numpy_rng, theano_rng=theano_rng, input=layer_input, 
          n_visible=input_size,
          n_hidden=hidden_layers_sizes[i],
          W=sigmoid_layer.W,
          bhid=sigmoid_layer.b)
      self.dA_layers.append(dA_layer)

    #add logistic layer on top of MLP
    self.logLayer = LogisticRegression(input=self.sigmoid_layers[-1].output,
        n_in=hidden_layers_sizes[-1], n_out=n_outs)
    self.params.extend(self.logLayer.params)

    #function that implements fine tuning

    #compute cost for second phase of training, defined as negative log likelihood
    self.finetune_cost = self.logLayer.negative_log_likelihood(self.y)
    
    #compute gradients w.r.t. model parameters
    #symbolic variable for no. of errors made on minibatch given by self.x and
    #self.y
    self.errors = self.logLayer.errors(self.y)
  
  def pretraining_functions(self, train_set_x, batch_size):
    '''generates list of function, each of them implementing one step in
      training the dA corresponding layer with same index. function will require
      as input the minibatch index, and to train a dA iterate, calling the
      corresponding function on all minibatch indexes'''
    
    #index to a [mini]batch
    index = T.lscalar('index')
    corruption_level = T.scalar('corruption')
    learning_rate = T.scalar('lr')
    #no. of batches
    n_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
    #beginnning of a batch
    batch_begin = index * batch_size
    #ending of a batch
    batch_end =  batch_begin + batch_size

    pretrain_fns = []
    for dA in self.dA_layers:
      #get cost and updates list
      cost, updates = dA.get_cost_updates(corruption_level, learning_rate)
      #compile the theano function
      fn = theano.function(inputs=[index, theano.Param(corruption_level, default=0.2), 
                                          theano.Param(learning_rate, default=0.1)], 
                                          outputs=cost, updates=updates,
                                          givens={self.x:
                                            train_set_x[batch_begin:batch_end]})
      pretrain_fns.append(fn)
    return pretrain_fns


  def build_finetune_functions(self, datasets, batch_size, learning_rate):
    '''Generate a 'train' function that implements one step of finetuning,
    'validate' that computes the error on a batch from the validation set,
    'test' that computes error on a batch from a testing set'''
    (train_set_x, train_set_y) = datasets[0]
    (valid_set_x, valid_set_y) = datasets[1]
    (test_set_x, test_set_y) = datasets[2]

    #compute no. of minibatches for validation and testing
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size
    n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size

    index = T.lscalar('index')

    #compute gradients w.r.t model params
    gparams = T.grad(self.finetune_cost, self.params)

    #list of fine tuning updates
    updates = []
    for param, gparam in zip(self.params, gparams):
      updates.append((param, param - gparam*learning_rate))

    train_fn = theano.function(inputs=[index], outputs=self.finetune_cost,
        updates=updates, givens={
          self.x: train_set_x[index * batch_size: (index + 1) * batch_size], 
          self.y: train_set_y[index * batch_size: (index + 1) * batch_size]},
        name='train')
    
    test_score_i = theano.function([index], self.errors, givens ={
      self.x: test_set_x[index * batch_size: (index + 1) * batch_size],
      self.y: test_set_y[index * batch_size: (index + 1) * batch_size]},
      name='test')

    valid_score_i = theano.function([index], self.errors, givens={
      self.x: valid_set_x[index * batch_size: (index + 1) * batch_size],
      self.y: valid_set_y[index * batch_size: (index + 1) * batch_size]},
      name='valid')

    #create func to scan entire validation set
    def valid_score():
      return [valid_score_i(i) for i in xrange(n_valid_batches)]

    #create func to scan entire test set
    def test_score():
      return [test_score_i(i) for i in xrange(n_test_batches)]

    return train_fn, valid_score, test_score


def testSdA(finetune_lr=0.1, pretraining_epochs=15, pretrain_lr=0.001,
    training_epochs=1000, dataset='mnist.pkl.gz', batch_size=1):

  datasets = load_data(dataset)
  train_set_x, train_set_y = datasets[0]
  valid_set_x, valid_set_y = datasets[1]
  test_set_x, test_set_y = datasets[2]

  #comp. no. of minibatches
  n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size

  numpy_rng = numpy.random.RandomState(89677)
  print '...building model'
  #construct stacked denoising autoencoder class
  sda = SdA(numpy_rng=numpy_rng, n_ins=28*28,
      hidden_layers_sizes=[1000,1000,1000], n_outs=10)


  #pretraining the model
  print '... getting the pretraining functions'
  pretraining_fns = sda.pretraining_functions(train_set_x=train_set_x,
      batch_size=batch_size)

  print '... pre-training the model'
  start_time = time.clock()
  #pre-train layerwise
  corruption_levels = [.1, .2, .3]
  for i in xrange(sda.n_layers):
    #go through pretraining epochs
    for epoch in xrange(pretraining_epochs):
      #go through the training set
      c = []
      for batch_index in xrange(n_train_batches):
        c.append(pretraining_fns[i](index=batch_index, corruption=corruption_levels[i], 
                                    lr=pretrain_lr))
      print 'Pre-trianing layer %i, epoch %d, cost ' % (i, epoch)
      print numpy.mean(c)

  end_time = time.clock()

  print >> sys.stderr, ('The pretraining code for file ' +
                        os.path.split(__file__)[1] + ' ran for %.2fm' %
                        ((end_time - start_time) / 60.))
  #finetuning the model
  #get training testing and validation function for the model
  print '... getting the finetuning functions'
  train_fn, validate_model, test_model = sda.build_finetune_functions(
                            datasets=datasets, batch_size=batch_size,
                            learning_rate=finetune_lr)
  
  print '... finetuning the model'
  #early-stopping parameters
  #look atleast these many examples
  patience = 10 * n_train_batches
  #wait this much longer when new best found
  patience_increase = 2.
  #following improvement is considered significant
  improvement_threshold = 0.995
  #go through these minibatches before validation checking
  validation_frequency = min(n_train_batches, patience / 2)

  best_params = None
  best_validation_loss = numpy.inf
  test_score = 0.
  start_time = time.clock()

  done_looping = False
  epoch = 0

  while (epoch < training_epochs) and (not done_looping):
    epoch = epoch + 1
    for minibatch_index in xrange(n_train_batches):
      minibatch_avg_cost = train_fn(minibatch_index)
      iter = (epoch - 1) * n_train_batches + minibatch_index

      if (iter + 1) % validation_frequency == 0:
        validation_losses = validate_model()
        this_validation_loss = numpy.mean(validation_losses)
        print('epoch %i, minibatch %i/%i, validation error %f %%' % (epoch,
          minibatch_index+1, n_train_batches, this_validation_loss*100.))

        #if we have the best validation score till now
        if this_validation_loss < best_validation_loss*improvement_threshold:
          #improve patience if loss improvement is good
          patience = max(patience, iter * patience_increase)

          #save best validation score and iteration no.
          best_validation_loss = this_validation_loss
          best_iter = iter

          #test on test set
          test_losses = test_model()
          test_score = numpy.mean(test_losses)
          print(('epoch %i, minibatch %i/%i, test error of best mdoel %f %%') %
              (epoch, minibatch_index,+1, n_train_batches, test_score * 100.))

      if patience <= iter:
        done_looping = True
        break

  end_time = time.clock()
  print(('Optimization complete with best validation score %f %% with test '
    'performance %f %%') % (best_validation_loss*100., test_score*100.))
  print >> sys.stderr, ('The training code for file ' + os.path.split(__file__)[1] +
                        ' ran for %.2fm' % ((end_time - start_time) / 60.))


if __name__ == '__main__':
  testSdA()      












  




