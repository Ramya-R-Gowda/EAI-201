import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data Load and Exploration
data_link = "http://lib.stat.cmu.edu/datasets/boston"
raw = pd.read_csv(data_link, sep="\s+", skiprows=22, header=None)
# Stack to shape data and target arrays
features = np.hstack([raw.values[::2, :], raw.values[1::2, :2]])
prices = raw.values[1::2, 2]
column_names = [
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS",
    "RAD", "TAX", "PTRATIO", "B", "LSTAT"
]
df = pd.DataFrame(features, columns=column_names)
df["PRICE"] = prices

print(df.sample(5))  # Show random sample
print("Shape:", df.shape)
print("PRICE stats: min =", df['PRICE'].min(), ", max =", df['PRICE'].max(), ", mean =", df['PRICE'].mean())

# Exploratory Data Analysis
plt.figure(figsize=(7, 5))
plt.hist(df['PRICE'], bins=18, color="lightblue", edgecolor='k')
plt.title('Boston Home Price Distribution')
plt.xlabel('PRICE')
plt.ylabel('Count')
plt.show()

cor_matrix = df.corr()
print(cor_matrix['PRICE'].sort_values(ascending=False))

# Select most positively correlated feature
best_feature = cor_matrix['PRICE'].drop('PRICE').idxmax()
print("Feature with strongest positive correlation:", best_feature)

plt.figure(figsize=(7, 5))
plt.scatter(df[best_feature], df['PRICE'], alpha=0.7, c="purple")
plt.xlabel(best_feature)
plt.ylabel('PRICE')
plt.title(f'PRICE vs {best_feature}')
plt.show()

# Model: Train/Test Split and Linear Regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X = df.drop(['PRICE'], axis=1)
y = df['PRICE']
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=1)

model = LinearRegression()
model.fit(Xtrain, ytrain)
ypred = model.predict(Xtest)

# Metrics
rmse = np.sqrt(mean_squared_error(ytest, ypred))
r2_val = r2_score(ytest, ypred)
print(f"Root Mean Square Error: {rmse:.2f}")
print(f"R^2 score: {r2_val:.2f}")

# Plot: Actual vs Predicted
plt.figure(figsize=(7, 5))
plt.scatter(ytest, ypred, color="teal", alpha=0.6, label="Predictions")
plt.plot([ytest.min(), ytest.max()], [ytest.min(), ytest.max()], 'r--', lw=2, label="Ideal")
plt.xlabel("Actual PRICE")
plt.ylabel("Predicted PRICE")
plt.legend()
plt.title("Actual vs Predicted Prices")
plt.show()
