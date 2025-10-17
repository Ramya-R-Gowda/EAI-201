import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# 1. Load the Titanic dataset
df = pd.read_csv('titanic.csv')

# 2. Display data info and count missing values
print(df.info())
print(df.isnull().sum())

# 3. Visualize distributions for key features 
features = ['Age', 'Sex', 'Pclass', 'Fare', 'Embarked']
sns.set_style('whitegrid')
for feature in features:
    plt.figure()
    if df[feature].dtype == 'O':
        sns.countplot(x=feature, data=df, color="#FFC0CB")
    else:
        sns.histplot(df[feature].dropna(), kde=False, color="#FFC0CB")
    plt.title(f'Distribution of {feature}')
    plt.show()

# 4. Analyze relationships between features and survival rates 
for feature in ['Sex', 'Pclass', 'Embarked']:
    pd.crosstab(df[feature], df['Survived'], normalize='index').plot(kind='bar', color=["#FFC0CB","#F497B5"])
    plt.title(f'Survival Rate by {feature}')
    plt.ylabel('Proportion')
    plt.show()

# 5. Data cleaning & imputation
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df['Fare'] = df['Fare'].fillna(df['Fare'].median())
df = df.drop(['PassengerId', 'Ticket', 'Cabin'], axis=1)

# 6. Feature engineering
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['Title'] = df['Name'].str.extract(r'([A-Za-z]+)\.', expand=False)
df = df.drop(['Name'], axis=1)

# 7. Encode categorical features
le = LabelEncoder()
df['Sex'] = le.fit_transform(df['Sex'])
df = pd.get_dummies(df, columns=['Embarked', 'Title'], drop_first=True)

# 8. Prepare data for modeling
X = df.drop('Survived', axis=1)
y = df['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 9. Display train/test samples and check for missing values
print("\nTraining feature sample:\n", X_train.head())
print("\nTraining labels sample:\n", y_train.head())
print(X_train.info())
print("\nMissing values in training data:\n", X_train.isnull().sum())
print("Train shape:", X_train.shape, "Test shape:", X_test.shape)
