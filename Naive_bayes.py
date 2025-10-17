import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np

# 1. Load and explore data
df = pd.read_csv("spam.csv", encoding="latin-1")[['v1', 'v2']]
df.columns = ['label', 'message']
print("Shape:", df.shape)
print("Columns:", df.columns)
print(df['label'].value_counts())
print("\nSpam examples:")
print(df[df['label'] == 'spam']['message'].head(3))
print("\nHam examples:")
print(df[df['label'] == 'ham']['message'].head(3))

# 2. What percentage of messages are spam?
spam_pct = (df['label'] == 'spam').mean() * 100
print(f"\nPercentage of messages that are spam: {spam_pct:.2f}%")

# 3. Calculate prior probabilities
P_spam = (df['label'] == 'spam').mean()
P_ham = (df['label'] == 'ham').mean()
print(f"P(spam): {P_spam:.2f}")
print(f"P(ham): {P_ham:.2f}")

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df['message'], df['label'], test_size=0.2, random_state=42
)

# 5. Probability that message contains "free" in spam vs ham
spam_msgs = df[df['label'] == 'spam']['message']
ham_msgs = df[df['label'] == 'ham']['message']
free_in_spam = spam_msgs.str.contains("free", case=False).sum()
free_in_ham = ham_msgs.str.contains("free", case=False).sum()
P_free_given_spam = free_in_spam / len(spam_msgs)
P_free_given_ham = free_in_ham / len(ham_msgs)
print(f"P('free'|spam): {P_free_given_spam:.2f}")
print(f"P('free'|ham): {P_free_given_ham:.2f}")

# 6. Vectorize text and build Naive Bayes model
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# 7. Evaluate the model
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("Confusion Matrix:\n", conf_matrix)

# 8. Top spam indicator words
feature_names = vectorizer.get_feature_names_out()
spam_probs = model.feature_log_prob_[1]
ham_probs = model.feature_log_prob_[0]
ratios = np.exp(spam_probs - ham_probs)
top_indices = np.argsort(ratios)[-5:]
top_words = feature_names[top_indices]
print("Top 5 spam indicator words:", top_words)

# 9. Test custom message prediction
custom_msg = ["Free call now! Win money!"]
custom_vec = vectorizer.transform(custom_msg)
custom_pred = model.predict(custom_vec)
print("Custom message prediction:", custom_pred[0])

# 10. Naive Assumption Test
msgs = ["Call me", "Free call"]
vecs = vectorizer.transform(msgs)
probs = model.predict_proba(vecs)
for msg, prob in zip(msgs, probs):
    print(f"Message: '{msg}' → Spam probability: {prob[1]:.2f}")
