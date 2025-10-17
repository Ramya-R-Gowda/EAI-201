import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. Load Iris dataset and convert target to binary: Setosa (1), Others (0)
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = (iris.target == 0).astype(int)  # 1 if Setosa, 0 if not

print(df['target'].value_counts())  # Number of samples in each class

# 2. Bar plot of class distribution
df['target'].value_counts().plot(kind='bar', color=['purple', 'lightgrey'])
plt.xlabel('Class (0=Non-Setosa, 1=Setosa)')
plt.ylabel('Count')
plt.title('Class Distribution')
plt.show()

# 3. Scatter plot petal length vs petal width, colored by class
sns.scatterplot(data=df, x='petal length (cm)', y='petal width (cm)', hue='target', palette=['grey', 'purple'])
plt.title('Petal Length vs Width by Class')
plt.show()

# 4. Summary: Feature means by class
print(df.groupby('target').mean())

# 5. Prepare data for logistic regression
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 6. Train model and predict
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# 7. Confusion matrix and heatmap
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# 8. Feature coefficients (importance)
coeff_df = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_[0]})
print(coeff_df)

# 9. Largest absolute coefficient
largest_coef = coeff_df.loc[coeff_df['Coefficient'].abs().idxmax()]
print(f"Largest absolute coefficient feature: {largest_coef['Feature']} ({largest_coef['Coefficient']:.3f})")
