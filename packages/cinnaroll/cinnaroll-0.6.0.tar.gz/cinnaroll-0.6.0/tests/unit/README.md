# Tests

### Constructing and running simple neural networks

Module `test_simple_nn_models.py` contains basic tools for building, validating and testing simple dense neural networks. More specifically, we have functions/methods that allow us to:

1. Construct a two-layer dense neural network model in three frameworks: Keras, pure TensorFlow and PyTorch.
2. Generate suitable random data for such a model.
3. Verify that freshly initialised models can be trained and used for making predictions.
4. Verify that models with identical architecture and identical weights give the same result in all three frameworks.
5. Verify that these models can be used to instantiate subclasses of CinnarollModel (defined in `cinnaroll.model`).

While working out the details of the pure TensorFlow construction I have used the following references:
- <https://www.tensorflow.org/api_docs/python/tf/Module>
- <https://www.tensorflow.org/guide/intro_to_modules>
- <https://www.tensorflow.org/guide/basic_training_loops>
