# -*- coding: utf-8 -*-
"""CKD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J5jvh3_DZN1asEBTz4OzxVH00YoK7YKp
"""

# necessary imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/kidney_disease.csv')
df.head()

df.sample(10)

# Demonstrating statistics
df.info()

# dropping id column
df.drop('id', axis = 1, inplace = True)
df.head()

# rename column names to make it more user-friendly

df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
              'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
              'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
              'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
              'aanemia', 'class']
df.sample(5)

df.describe().T

df.info()

# converting necessary columns to numerical type

df['packed_cell_volume'] = pd.to_numeric(df['packed_cell_volume'], errors='coerce')
df['white_blood_cell_count'] = pd.to_numeric(df['white_blood_cell_count'], errors='coerce')
df['red_blood_cell_count'] = pd.to_numeric(df['red_blood_cell_count'], errors='coerce')

df.info()

cat_cols = [col for col in df.columns if df[col].dtype == 'object']
num_cols = [col for col in df.columns if df[col].dtype != 'object']

# looking at unique values in categorical columns

for col in cat_cols:
    print(f"{col} has {df[col].unique()} values\n")

# replace incorrect values

df['diabetes_mellitus'].replace(to_replace = {'\tno':'no','\tyes':'yes',' yes':'yes'},inplace=True)

df['coronary_artery_disease'] = df['coronary_artery_disease'].replace(to_replace = '\tno', value='no')

df['class'] = df['class'].replace(to_replace = {'ckd\t': 'ckd', 'notckd': 'not ckd'})

for col in cat_cols:
    print(f"{col} has {df[col].unique()} values\n")

df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1})
df['class'] = pd.to_numeric(df['class'], errors='coerce')

cols = ['diabetes_mellitus', 'coronary_artery_disease', 'class']

for col in cols:
    print(f"{col} has {df[col].unique()} values\n")

# looking at categorical columns

plt.figure(figsize = (20, 15))
plotnumber = 1

for column in cat_cols:
    if plotnumber <= 11:
        ax = plt.subplot(3, 4, plotnumber)
        sns.countplot(df[column], palette = 'rocket')
        plt.xlabel(column)

    plotnumber += 1

plt.tight_layout()
plt.show()

plt.figure(figsize = (15, 8))
sns.heatmap(df.corr(), annot = True, linewidths = 2, linecolor = 'lightgrey')
plt.show()

def plot_violin_kde(data, feature):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Violin plot
    sns.violinplot(data=data, y=feature, x="class", inner="box", scale="width", ax=axes[0])
    axes[0].set_title(f'Violin Plot of {feature}')

    # KDE plot
    sns.kdeplot(data=data[data['class'] == 0][feature], label='CKD', ax=axes[1])
    sns.kdeplot(data=data[data['class'] == 1][feature], label='Not CKD', ax=axes[1])
    axes[1].set_title(f'KDE Plot of {feature}')
    axes[1].legend()

    plt.tight_layout()
    plt.show()

# Plot all the violin and KDE plots
features = ['red_blood_cell_count', 'white_blood_cell_count', 'packed_cell_volume', 'haemoglobin', 'albumin',
            'blood_glucose_random', 'sodium', 'blood_urea', 'specific_gravity']

for feature in features:
    plot_violin_kde(df, feature)

sns.pairplot(data=df)
plt.title("pairplot")
plt.show()

def violin(col):
    sns.violinplot(data=df, y=col, x="class", inner="box", scale="width")
    plt.show()

def kde(col):
    grid = sns.FacetGrid(df, hue="class", height = 6, aspect=2)
    grid.map(sns.kdeplot, col)
    grid.add_legend()

def scatter(col1, col2):
    fig = sns.scatterplot(data=df, x=col1, y=col2, hue="class")
    plt.show()

def bar_plot(x_col, y_col):
    sns.barplot(data=df, x=x_col, y=y_col, hue="class")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"Bar Plot of {y_col} vs {x_col}")
    plt.show()

violin('red_blood_cell_count')

kde('red_blood_cell_count')

violin('white_blood_cell_count')

kde('white_blood_cell_count')

violin('packed_cell_volume')

kde('packed_cell_volume')

violin('haemoglobin')

kde('haemoglobin')

violin('albumin')

kde('albumin')

violin('blood_glucose_random')

kde('blood_glucose_random')

violin('sodium')

kde('sodium')

violin('blood_urea')

kde('blood_urea')

violin('specific_gravity')

kde('specific_gravity')

scatter('haemoglobin', 'packed_cell_volume')

scatter('red_blood_cell_count', 'packed_cell_volume')

scatter('red_blood_cell_count', 'albumin')

scatter('sugar', 'blood_glucose_random')

scatter('packed_cell_volume','blood_urea')

bar_plot("specific_gravity", "packed_cell_volume")

bar_plot("specific_gravity", "albumin")

bar_plot("blood_pressure", "packed_cell_volume")

bar_plot("blood_pressure", "haemoglobin")

df.hist(alpha=1, figsize=(20,15))
plt.suptitle("HIstogram")
plt.show()

sns.kdeplot(x='haemoglobin',y= 'age' , data=df , fill =True )
plt.title("haemoglobin vs age")
plt.show()

df.isna().sum().sort_values(ascending = False)

df[num_cols].isnull().sum()

df[cat_cols].isnull().sum()

def impute_mode(feature):
    mode = df[feature].mode()[0]
    df[feature] = df[feature].fillna(mode)

for col in num_cols:
    impute_mode(col)

df[num_cols].isnull().sum()

for col in cat_cols:
    impute_mode(col)

df[cat_cols].isnull().sum()

for col in cat_cols:
    print(f"{col} has {df[col].nunique()} categories\n")

df.sample(5)

le = LabelEncoder()

for col in cat_cols:
    df[col] = le.fit_transform(df[col])

df.sample(5)

ind_col = [col for col in df.columns if col != 'class']
dep_col = 'class'

X = df[ind_col]
y = df[dep_col]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

# accuracy score, confusion matrix and classification report of knn

knn_acc = accuracy_score(y_test, knn.predict(X_test))

print(f"Training Accuracy of KNN is {accuracy_score(y_train, knn.predict(X_train))}")
print(f"Test Accuracy of KNN is {knn_acc} \n")

print(f"Confusion Matrix :- \n{confusion_matrix(y_test, knn.predict(X_test))}\n")
print(f"Classification Report :- \n {classification_report(y_test, knn.predict(X_test))}")

from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)

# accuracy score, confusion matrix and classification report of decision tree

dtc_acc = accuracy_score(y_test, dtc.predict(X_test))

print(f"Training Accuracy of Decision Tree Classifier is {accuracy_score(y_train, dtc.predict(X_train))}")
print(f"Test Accuracy of Decision Tree Classifier is {dtc_acc} \n")

print(f"Confusion Matrix :- \n{confusion_matrix(y_test, dtc.predict(X_test))}\n")
print(f"Classification Report :- \n {classification_report(y_test, dtc.predict(X_test))}")