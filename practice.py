
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

X = [[1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8]]
y = [0, 0, 0, 1, 1, 1]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = GaussianNB()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Predictions:", y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))
