# Adam Optimizer Playground (adam.ipynb)

## Overview
This Jupyter notebook demonstrates training a small feed-forward neural network to fit a noisy cubic function. It compares three training approaches:
- Manual vanilla gradient descent (parameter updates performed by hand)
- Custom implementation of the Adam optimizer (from-scratch moment updates + bias correction)
- PyTorch's built-in Adam optimizer

The notebook plots training losses (log scale) and model predictions against the true data.

## Notes
- Learning rates, betas, epsilon, and number of epochs are configurable in the notebook.
- The custom Adam implementation aims to match PyTorch's algorithm but may differ slightly due to initialization or numerical detail.
