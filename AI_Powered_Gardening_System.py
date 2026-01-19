import pandas as pd
import numpy as np  # if you use numpy
import matplotlib.pyplot as plt  # if you use plots

#Load the Dataset
import pandas as pd
# Load the dataset
df = pd.read_csv('/kaggle/input/dataset-for-predicting-watering-the-plants/TARP.csv')
# Display the first few rows
print(df.head())



#Import of libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, ConfusionMatrixDisplay
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow INFO and WARNING logs
import tensorflow as tf


#Load and Preprocess
df = pd.read_csv('/kaggle/input/dataset-for-predicting-watering-the-plants/TARP.csv')
df.columns = df.columns.str.strip()
df.dropna(inplace=True)
df['Status'] = df['Status'].map({'ON': 1, 'OFF': 0})
X = df.drop('Status', axis=1)
y = df['Status']


#Basic Balancing
count_class_0, count_class_1 = y.value_counts()
df_class_0 = df[df['Status'] == 0]
df_class_1 = df[df['Status'] == 1]
if count_class_1 > count_class_0:
    df_class_0_over = df_class_0.sample(count_class_1, replace=True, random_state=42)
    df_balanced = pd.concat([df_class_0_over, df_class_1], axis=0)
else:
    df_class_1_over = df_class_1.sample(count_class_0, replace=True, random_state=42)
    df_balanced = pd.concat([df_class_0, df_class_1_over], axis=0)
X = df_balanced.drop('Status', axis=1)
y = df_balanced['Status']

#Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42, stratify=y)


# Models
models = {
    "KNN": (KNeighborsClassifier(), 'Blues', 'blue'),
    "SVM": (SVC(probability=True, kernel='rbf', C=10, gamma=0.1), 'Greens', 'green'),
    "Decision Tree": (DecisionTreeClassifier(max_depth=10), 'Oranges', 'orange'),
    "Random Forest": (RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=2), 'Purples', 'magenta'),
    "Naive Bayes": (GaussianNB(), 'BuGn', 'cyan')
}

plt.figure(figsize=(10, 8))
for name, (model, cmap, color) in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n{name} Classification Report:")
    print(classification_report(y_test, y_pred))
 # Confusion Matrix with Custom Colors
    disp = ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap=cmap)
    disp.ax_.set_title(f"{name} Confusion Matrix")
    plt.show()

    # ROC Curve
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        try:
            y_proba = model.decision_function(X_test)
            y_proba = (y_proba - y_proba.min()) / (y_proba.max() - y_proba.min())
        except:
            print(f"{name} does not support probability outputs. Skipping ROC.")
            continue

    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, color=color, label=f'{name} (AUC={roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.title("ROC Curve Comparison")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc='lower right')
plt.grid()
plt.show()

#Hyperparameter Tuning
param_grid_rf = {'n_estimators': [100, 200], 'max_depth': [10, 20], 'min_samples_split': [2, 5]}
grid_rf = GridSearchCV(RandomForestClassifier(), param_grid_rf, cv=5, scoring='accuracy')
grid_rf.fit(X_train, y_train)
print("Best RF Parameters:", grid_rf.best_params_)
print("Best RF Accuracy:", grid_rf.best_score_)

param_grid_svm = {'C': [1, 10], 'gamma': [0.01, 0.1]}
grid_svm = GridSearchCV(SVC(probability=True), param_grid_svm, cv=5, scoring='accuracy')
grid_svm.fit(X_train, y_train)
print("Best SVM Parameters:", grid_svm.best_params_)
print("Best SVM Accuracy:", grid_svm.best_score_)


#Deep Learning Model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
import matplotlib.pyplot as plt

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y_dl = to_categorical(y)
X_train_dl, X_test_dl, y_train_dl, y_test_dl = train_test_split(X_scaled, y_dl, test_size=0.25, random_state=42)

def build_and_train_model(epochs, batch_size):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(X.shape[1],)),
        Dropout(0.4),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(2, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train_dl, y_train_dl, validation_data=(X_test_dl, y_test_dl), epochs=epochs, batch_size=batch_size, verbose=0)
    return history

def plot_history(history, title):
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(title)
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy/Loss')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting all four scenarios
history1 = build_and_train_model(epochs=8, batch_size=32)
plot_history(history1, "Training and Validation Accuracy/Loss (8 Epochs, Batch Size 32)")

history2 = build_and_train_model(epochs=11, batch_size=32)
plot_history(history2, "Training and Validation Accuracy/Loss (11 Epochs, Batch Size 32)")

history3 = build_and_train_model(epochs=2, batch_size=16)
plot_history(history3, "Training and Validation Accuracy/Loss (2 Epochs, Batch Size 16)")

history4 = build_and_train_model(epochs=5, batch_size=16)
plot_history(history4, "Training and Validation Accuracy/Loss (5 Epochs, Batch Size 16)")





#Combined ROC


from sklearn.metrics import roc_curve, auc
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt

# Train classifiers
models = {
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True, kernel='rbf', C=10, gamma=0.1),
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=2),
    "Naive Bayes": GaussianNB()
}
plt.figure(figsize=(10, 8))
for name, model in models.items():
    # Train
    model.fit(X_train, y_train)
    # Predict probabilities
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        y_proba = model.decision_function(X_test)
        y_proba = (y_proba - y_proba.min()) / (y_proba.max() - y_proba.min())  # normalize
    # Compute ROC curve and AUC
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{name} (AUC={roc_auc:.2f})')
# Plot diagonal line
plt.plot([0, 1], [0, 1], 'k--')
# Add labels and title
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.grid()
# Show plot
plt.show()
