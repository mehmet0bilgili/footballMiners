import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.inspection import permutation_importance
import seaborn as sns

data = pd.read_csv('model/dataset.csv')

#Feature Distinction According to categorical or numeric.
categorical_features = ['MatchStadium', 'Team1Formation', 'Team2Formation']
numerical_features = [col for col in data.columns if col not in categorical_features + ['Result']]

X = data.drop('Result', axis=1)
y = data['Result']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

#Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

#GaussianNB Pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', GaussianNB())
])

#Training
model.fit(X_train, y_train)

#Prediction
naive_bayes_y_pred = model.predict(X_test)

#GaussianNB Accuracy Score
naive_bayes_accuracy = accuracy_score(y_test, naive_bayes_y_pred)
print("GaussianNB Accuracy:", naive_bayes_accuracy)

#Feauture Importance Permutation Test
perm_importance = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
perm_importance_df = pd.DataFrame({
    'feature': X_test.columns,
    'importance': perm_importance.importances_mean
}).sort_values(by='importance', ascending=False)

#Feature Importance Plot
plt.figure(figsize=(12, 8))
plt.barh(perm_importance_df['feature'], perm_importance_df['importance'], color='skyblue')
plt.title('GaussionNB Feature Importance')
plt.gca().invert_yaxis()
plt.show()

#Creating Confusion Matrix and Plot
conf_matrix = confusion_matrix(y_test, naive_bayes_y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot()
plt.title("GaussianNB Confusion Matrix")
plt.show()

#Creating Correlation Matrix and Plot
correlation_matrix = data[numerical_features].corr()
plt.figure(figsize=(18, 15))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("GaussianNB Correlation Matrix")
plt.show()





