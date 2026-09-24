import numpy as np
import matplotlib.pyplot as plt

# For Keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


# ============================================
# PART 1: CREATE XOR DATASET
# ============================================

# Input combinations
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# XOR output
y = np.array([
    0,
    1,
    1,
    0
])

print("XOR Dataset:")
print("A B | XOR")

for i in range(len(X)):
    print(X[i][0], X[i][1], "|", y[i])


# ============================================
# PART 2: STEP ACTIVATION FUNCTION
# ============================================

def step_activation(x):
    """
    Step activation function:
    Output = 1 if x >= 0
    Output = 0 otherwise
    """
    return 1 if x >= 0 else 0


# ============================================
# PART 3: MANUAL PERCEPTRON
# A AND NOT B
# ============================================

def perceptron_A_AND_NOT_B(A, B):

    # A AND NOT B
    # Output should be:
    #
    # A B | Output
    # 0 0 | 0
    # 0 1 | 0
    # 1 0 | 1
    # 1 1 | 0

    weights = np.array([1, -1])
    bias = -0.5

    weighted_sum = A * weights[0] + B * weights[1] + bias

    return step_activation(weighted_sum)


# ============================================
# PART 4: MANUAL PERCEPTRON
# NOT A AND B
# ============================================

def perceptron_NOT_A_AND_B(A, B):

    # NOT A AND B
    #
    # A B | Output
    # 0 0 | 0
    # 0 1 | 1
    # 1 0 | 0
    # 1 1 | 0

    weights = np.array([-1, 1])
    bias = -0.5

    weighted_sum = A * weights[0] + B * weights[1] + bias

    return step_activation(weighted_sum)


# ============================================
# PART 5: COMBINE THE TWO PERCEPTRONS
# TO PRODUCE XOR
# ============================================

def manual_XOR(A, B):

    output1 = perceptron_A_AND_NOT_B(A, B)

    output2 = perceptron_NOT_A_AND_B(A, B)

    # XOR = (A AND NOT B) OR (NOT A AND B)

    xor_output = output1 + output2

    # Convert to binary
    if xor_output >= 1:
        return 1
    else:
        return 0


# ============================================
# DISPLAY MANUAL PERCEPTRON RESULTS
# ============================================

print("\nManual Perceptron XOR Results:")
print("A B | A AND NOT B | NOT A AND B | XOR")

manual_predictions = []

for A, B in X:

    p1 = perceptron_A_AND_NOT_B(A, B)
    p2 = perceptron_NOT_A_AND_B(A, B)
    xor = manual_XOR(A, B)

    manual_predictions.append(xor)

    print(A, B, "|     ", p1, "      |      ", p2, "      |", xor)


# ============================================
# MANUAL PERCEPTRON ACCURACY
# ============================================

manual_predictions = np.array(manual_predictions)

manual_accuracy = np.mean(manual_predictions == y) * 100

print("\nManual Perceptron Accuracy:",
      manual_accuracy, "%")


# ============================================
# PART 6: TWO-LAYER NEURAL NETWORK USING KERAS
# ============================================

# Create the neural network
model = Sequential([

    # Hidden layer
    Dense(
        2,
        input_dim=2,
        activation='sigmoid'
    ),

    # Output layer
    Dense(
        1,
        activation='sigmoid'
    )
])


# ============================================
# COMPILE MODEL
# ============================================

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)


# ============================================
# DISPLAY MODEL STRUCTURE
# ============================================

print("\nNeural Network Architecture:")
model.summary()


# ============================================
# TRAIN THE MODEL
# ============================================

history = model.fit(
    X,
    y,
    epochs=1000,
    verbose=0
)


# ============================================
# PART 7: PREDICTIONS
# ============================================

predicted_probabilities = model.predict(X, verbose=0)

# Convert probabilities to 0 or 1
predicted_outputs = (
    predicted_probabilities >= 0.5
).astype(int).flatten()


# ============================================
# DISPLAY ACTUAL AND PREDICTED OUTPUTS
# ============================================

print("\nActual vs Predicted Outputs:")

print("A B | Actual | Predicted | Probability")

for i in range(len(X)):

    print(
        X[i][0],
        X[i][1],
        "|   ",
        y[i],
        "   |    ",
        predicted_outputs[i],
        "     |",
        round(float(predicted_probabilities[i]), 4)
    )


# ============================================
# PART 8: CLASSIFICATION ACCURACY
# ============================================

accuracy = np.mean(predicted_outputs == y) * 100

print("\nClassification Accuracy:",
      accuracy, "%")


# ============================================
# PART 9: PLOT TRAINING ACCURACY
# ============================================

plt.figure(figsize=(8, 5))

plt.plot(history.history['accuracy'])

plt.title("Training Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.grid(True)
plt.show()


# ============================================
# PART 10: PLOT TRAINING LOSS
# ============================================

plt.figure(figsize=(8, 5))

plt.plot(history.history['loss'])

plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.grid(True)
plt.show()


# ============================================
# PART 11: MANUAL XOR DECISION REGIONS
# ============================================

def manual_xor_grid(A, B):

    return manual_XOR(A, B)


# Create grid
x_min, x_max = -0.2, 1.2
y_min, y_max = -0.2, 1.2

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 300),
    np.linspace(y_min, y_max, 300)
)

grid_points = np.c_[xx.ravel(), yy.ravel()]

manual_grid_predictions = np.array([
    manual_xor_grid(A, B)
    for A, B in grid_points
])

manual_grid_predictions = manual_grid_predictions.reshape(
    xx.shape
)


# ============================================
# PLOT MANUAL PERCEPTRON DECISION REGION
# ============================================

plt.figure(figsize=(7, 6))

plt.contourf(
    xx,
    yy,
    manual_grid_predictions,
    alpha=0.4
)

plt.scatter(
    X[:, 0],
    X[:, 1],
    c=y,
    edgecolors='black',
    s=150
)

plt.xlabel("Input A")
plt.ylabel("Input B")

plt.title(
    "Decision Regions - Manual Perceptron XOR"
)

plt.grid(True)

plt.show()


# ============================================
# PART 12: TRAINED NEURAL NETWORK
# DECISION REGIONS
# ============================================

nn_probabilities = model.predict(
    grid_points,
    verbose=0
)

nn_predictions = (
    nn_probabilities >= 0.5
).astype(int).reshape(xx.shape)


# ============================================
# PLOT NEURAL NETWORK DECISION REGION
# ============================================

plt.figure(figsize=(7, 6))

plt.contourf(
    xx,
    yy,
    nn_predictions,
    alpha=0.4
)

plt.scatter(
    X[:, 0],
    X[:, 1],
    c=y,
    edgecolors='black',
    s=150
)

plt.xlabel("Input A")
plt.ylabel("Input B")

plt.title(
    "Decision Regions - Trained Multilayer Neural Network"
)

plt.grid(True)

plt.show()


# ============================================
# PART 13: COMPARISON
# ============================================

print("\n===================================")
print("FINAL COMPARISON")
print("===================================")

print("Manual Perceptron Accuracy:",
      manual_accuracy, "%")

print("Neural Network Accuracy:",
      accuracy, "%")

print("\nActual XOR:")
print(y)

print("\nManual XOR Prediction:")
print(manual_predictions)

print("\nNeural Network Prediction:")
print(predicted_outputs)
