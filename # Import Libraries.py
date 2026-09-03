# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve


# ==============================
# 1. Load Dataset
# ==============================


data = load_breast_cancer()


X = data.data
y = data.target
print("Total Samples:", X.shape[0])
print("Total Features:", X.shape[1])


print("\nFeature Names:")
print(data.feature_names)


print("\nTarget Classes:")
print(data.target_names)


# ==============================
# 2. Train Test Split (80:20)
# ==============================


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ==============================
# 3. Feature Scaling
# ==============================


scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==============================
# 4. Models
# ==============================


models = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Naive Bayes": GaussianNB(),
    "SVM": SVC(probability=True),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}


results = []


# ==============================
# 5. Training and Evaluation
# ==============================

for name, model in models.items():

    print("\n==============================")
    print("Model:", name)
    print("==============================")

    if name in ["KNN", "SVM"]:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:,1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:,1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    cm = confusion_matrix(y_test, y_pred)

    auc = roc_auc_score(y_test, y_prob)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    print("\nConfusion Matrix:")
    print(cm)

    print("AUC:", auc)

    results.append([name, accuracy, precision, recall, f1, auc])


    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)

    plt.plot(fpr, tpr, label=name)


# ==============================
# 6. ROC Curve Plot
# ==============================

plt.plot([0,1], [0,1], linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.show()


# ==============================
# 7. Comparison Table
# ==============================

results_df = pd.DataFrame(results, columns=[
    "Algorithm","Accuracy","Precision","Recall","F1 Score","AUC"
])

print("\n\nPerformance Comparison Table:\n")
print(results_df)
