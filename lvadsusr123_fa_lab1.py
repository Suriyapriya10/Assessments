# -*- coding: utf-8 -*-
"""LVADSUSR123_FA_LAB1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kPViv4EZAntEtntBcV4HPXZVTEDjPAI-
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv('/content/sample_data/loan_approval.csv')

print(data.describe())
print()

missing_values = data.isnull().sum()
print("Missing values per column:\n", missing_values)

data.fillna(data.mean(), inplace=True)

plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()
print()

plt.figure(figsize=(12, 6))
sns.boxplot(data=data)
plt.title("Boxplot of Variables")
plt.xticks(rotation=45)
plt.show()
print()

for col in data.select_dtypes(include=[np.number]).columns:
    ninety_fifth_percentile = data[col].quantile(0.95)
    data[col] = np.where(data[col] > ninety_fifth_percentile, ninety_fifth_percentile, data[col])

plt.figure(figsize=(12, 6))
sns.boxplot(data=data)
plt.title("Boxplot of Variables after Handling Outliers")
plt.xticks(rotation=45)
plt.show()

X = data.drop(' loan_status', axis=1)
y = data[' loan_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_encoded = pd.get_dummies(X_train)
X_test_encoded = pd.get_dummies(X_test)

X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='outer', axis=1, fill_value=0)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_encoded)
X_test_scaled = scaler.transform(X_test_encoded)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print()
print("Accuracy:", accuracy)
print()
print("Classification Report:\n", report)
print()