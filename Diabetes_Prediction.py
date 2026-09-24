# ============================================
# DIABETES PREDICTION USING ARTIFICIAL
# NEURAL NETWORK
# ============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    roc_auc_score
)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# --------------------------------------------
# 1. Load Dataset
# --------------------------------------------

# Download the CSV from Kaggle and place it
# in the same folder as this Python file.

data = pd.read_csv("diabetes.csv")

# --------------------------------------------
# 2. Display first few rows
# --------------------------------------------

print("First five rows:")
print(data.head())

# --------------------------------------------
# 3. Check missing values
# --------------------------------------------

print("\nMissing values:")
print(data.isnull().sum())

# --------------------------------------------
# 4. Separate X and y
# --------------------------------------------

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

print("\nInput features:")
print(X.head())

print("\nTarget:")
print(y.head())

# --------------------------------------------
# 5. Split into training and testing data
# --------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# --------------------------------------------
# 6. Normalize using StandardScaler
# --------------------------------------------

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# --------------------------------------------
# 7. Build ANN Model
# --------------------------------------------

model = Sequential([

    # Hidden Layer 1
    Dense(
        12,
        activation='relu',
        input_shape=(8,)
    ),

    # Hidden Layer 2
    Dense(
        8,
        activation='relu'
    ),

    # Output Layer
    Dense(
        1,
        activation='sigmoid'
    )
])

# --------------------------------------------
# 8. Display Model Summary
# --------------------------------------------

model.summary()

# --------------------------------------------
# 9. Compile Model
# --------------------------------------------

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# --------------------------------------------
# 10. Train Model
# --------------------------------------------

history = model.fit(
    X_train,
    y_train,
    epochs=40,
    batch_size=10,
    validation_split=0.20,
    verbose=1
)

# --------------------------------------------
# 11. Evaluate Model
# --------------------------------------------

test_loss, test_accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)

print("\nTest Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# --------------------------------------------
# 12. Plot Accuracy
# --------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    history.history['accuracy'],
    label='Training Accuracy'
)

plt.plot(
    history.history['val_accuracy'],
    label='Validation Accuracy'
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training Accuracy vs Validation Accuracy")

plt.legend()
plt.grid()
plt.show()

# --------------------------------------------
# 13. Plot Loss
# --------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    history.history['loss'],
    label='Training Loss'
)

plt.plot(
    history.history['val_loss'],
    label='Validation Loss'
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss vs Validation Loss")

plt.legend()
plt.grid()
plt.show()

# --------------------------------------------
# 14. Prediction
# --------------------------------------------

y_prob = model.predict(X_test).ravel()

# Convert probabilities to class labels

y_pred = (y_prob >= 0.5).astype(int)

# --------------------------------------------
# 15. Confusion Matrix
# --------------------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(6, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues'
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.show()

# --------------------------------------------
# 16. Classification Report
# --------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)

# --------------------------------------------
# 17. ROC Curve
# --------------------------------------------

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_prob
)

plt.figure(figsize=(8, 5))

plt.plot(
    fpr,
    tpr,
    label='ANN'
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle='--'
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()
plt.grid()
plt.show()

# --------------------------------------------
# 18. AUC Score
# --------------------------------------------

auc_score = roc_auc_score(
    y_test,
    y_prob
)

print("\nAUC Score:", auc_score)
