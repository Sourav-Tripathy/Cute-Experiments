# Replicating "Distilling the Knowledge in a Neural Network" on MNIST

This repository contains a PyTorch implementation that attempts to replicate the findings of the 2015 paper [***Distilling the Knowledge in a Neural Network***](https://arxiv.org/pdf/1503.02531) by Hinton, Vinyals, and Dean. The focus is on the first experiment conducted on the MNIST dataset.

## What is Knowledge Distillation?

Knowledge distillation is a model compression technique where a small, compact model (the "student") is trained to mimic the behavior of a larger, more complex model (the "teacher").

Instead of just learning from the ground-truth labels (hard targets), the student also learns from the class probabilities produced by the teacher model (soft targets). These soft targets provide more information per training sample than the hard targets, revealing how the teacher model "thinks" and generalizes. For example, the teacher might output that an image of a "2" has a 90% probability of being a "2", but also a 5% probability of being a "7" and a 3% probability of being a "1". This nuanced information helps the student learn a better decision boundary.

## Methodology

The process is broken down into two main experiments as described in the paper.

### 1. The Models

-   **Teacher Model**: A large neural network with two hidden layers of 1200 neurons each (`784 -> 1200 -> 1200 -> 10`).
-   **Student Model**: A smaller neural network with two hidden layers of 800 neurons each (`784 -> 800 -> 800 -> 10`).

### 2. Experiment 1: Standard Knowledge Distillation

1.  **Train the Teacher**: The large teacher model is trained on the standard MNIST training set (60,000 images) using cross-entropy loss.
2.  **Train a Base Student**: A student model is trained on the same dataset for comparison. This serves as a baseline.
3.  **Train a Distilled Student**: A second student model (with the same architecture as the baseline) is trained using a special loss function. This loss is a weighted average of two components:
    -   **Hard Loss**: Standard cross-entropy loss with the correct labels (hard targets).
    -   **Soft Loss**: Kullback-Leibler (KL) divergence loss between the student's softened predictions and the teacher's softened predictions. The "softening" is done using a `temperature` parameter (`T`).

    The combined loss is calculated as:
    `Loss = α * soft_loss + (1 - α) * hard_loss`

### 3. Experiment 2: Distilling "Dark Knowledge"

This experiment demonstrates that the student can learn about classes it has never seen in the training data, purely from the teacher's soft targets.

1.  **Modify Datasets**: The digit '3' is completely removed from the training datasets.
2.  **Train a Base Student**: A student model is trained on the dataset without any '3's. As expected, it cannot learn to recognize this digit.
3.  **Train a Distilled Student**: A distilled student model is trained on the dataset without '3's. However, it still uses the soft targets from the original teacher model (which *was* trained on all digits, including '3').
4.  **Evaluation**: Both models are evaluated on the full test set, which includes the digit '3'. The number of incorrect predictions for the digit '3' is compared.

## Results

The notebook `knowledge_distillation_MNIST.ipynb` contains the full implementation and output.

### Experiment 1 Results

-   The **Teacher Net** achieves high accuracy.
-   The **Base Student Net** achieves a slightly lower accuracy than the teacher.
-   The **Distilled Student Net** (trained with both hard and soft targets) outperforms the Base Student Net, demonstrating the effectiveness of knowledge distillation.
-   A student trained **only on soft targets** performs poorly, highlighting the importance of including the hard targets in the loss function.

### Experiment 2 Results

-   **Base Student (no '3's)**: When tested, this model incorrectly classifies almost all of the '3's in the test set.
-   **Distilled Student (no '3's)**: This model correctly classifies a significant portion of the '3's in the test set, despite never having been explicitly trained on them. It made only **~206** errors on the 1010 test images of '3's.

This result shows that the "dark knowledge" about the similarities between digits (e.g., a '3' looking somewhat like an '8' or a '5') was successfully transferred from the teacher to the student through the soft targets.