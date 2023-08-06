from typing import Any
from .optimizers import *

class Genome:
  '''A lightweight NeuralFit model that can only be used for predictions.'''

  inputs: Any
  '''The number of inputs of the model.'''
  outputs: Any
  '''The number of outputs of the model.'''
  recurrent: Any
  '''If the model is recurrent or not.'''

  def __init__ (self, inputs, outputs):
    '''Create a new genome.'''
    ...
  def clear (self):
     '''Clears the recurrent state of the genome, preparing it for a new sequence of inputs.'''
  ...
  def predict (self, x):
     '''Predict the the outputs for a given set of samples.'''
  ...

class Model:
  '''A NeuralFit model that can be evolved on datasets and fitness functions.'''

  inputs: Any
  '''The number of inputs of the model.'''
  outputs: Any
  '''The number of outputs of the model.'''
  size: Any
  '''Total number of nodes in the model (including inputs and outputs).'''

  def __init__ (self, inputs, outputs, size=None, recurrent=False):
    '''Create a new model.'''
    ...
  def clear (self):
     '''Clears the recurrent state of the model, preparing it for a new sequence of inputs.'''
  ...
  def compile (self, optimizer, loss, metrics, monitors):
     '''Configure the losses, metrics and monitors for evolution. For `model.evolve_func`, losses and metrics are optional.'''
  ...
  def evaluate (self, x, y):
     '''Evaluate the the network based on the compiled losses/metrics on a given dataset.'''
  ...
  def evolve (self, x_train, y_train, pop_size=100, batch_size=-1, epochs=100, validation_data=None, verbose=1):
     '''Evolves the network on a given dataset.'''
  ...
  def func_evolve (self, train_func, pop_size=100, epochs=100, verbose=1, validation_func=None):
     '''Evolves the network on a given fitness function.'''
  ...
  def get_connections (self):
     '''Returns a list of connections contained in the network.'''
  ...
  def get_nodes (self):
     '''Returns a list of nodes contained in the network.'''
  ...
  def predict (self, x):
     '''Predict the the outputs for a given set of samples.'''
  ...
  def save (self, path):
     '''Saves the model using the '.nf' format.'''
  ...
  def to_keras (self):
     '''Convert the NeuralFit model to a Keras model.'''
  ...

def from_keras (keras_model):
   '''Convert a Keras model to a NeuralFit model. This only works for Keras models that have been exported from NeuralFit using `model.to_keras()` with unmodified architecture.'''
...
def load (path):
   '''Load a model saved in the '.nf' format.'''
...
def set_license (key):
   '''Set a (non-free) license that grants you access to certain features. You can view our licenses at https://neuralfit.net/licenses/.'''
...
