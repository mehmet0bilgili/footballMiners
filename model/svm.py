import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.inspection import permutation_importance

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

#SVM Pipeline
svm_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', SVC(probability=True, random_state=42))  # probability=True ile olasılık tahminlerini etkinleştirme
])

#Training
svm_model.fit(X_train, y_train)

#Prediction
svm_y_pred = svm_model.predict(X_test)

#SVM Accuracy Score
svm_accuracy = accuracy_score(y_test, svm_y_pred)
print("SVM Accuracy:", svm_accuracy)

#Feauture Importance Permutation Test
perm_importance = permutation_importance(svm_model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=4)
ohe = svm_model.named_steps['preprocessor'].named_transformers_['cat']
ohe_feature_names = ohe.get_feature_names_out(categorical_features)

#Combining all features
all_feature_names = numerical_features + list(ohe_feature_names)

perm_importance_df = pd.DataFrame({
    'feature': all_feature_names[:len(perm_importance.importances_mean)],
    'importance': perm_importance.importances_mean
}).sort_values(by='importance', ascending=False)

#Feature Importance Plot
plt.figure(figsize=(12, 8))
plt.barh(perm_importance_df['feature'], perm_importance_df['importance'], color='skyblue')
plt.xlabel('Feature Importance')
plt.title('SVM Feature Importance')
plt.gca().invert_yaxis()
plt.show()

#Creating Confusion Matrix and Plot
conf_matrix = confusion_matrix(y_test, svm_y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot()
plt.title("SVM Confusion Matrix")
plt.show()

#Creating Correlation Matrix and Plot
numerical_data = data[numerical_features]
correlation_matrix = numerical_data.corr()
plt.figure(figsize=(18, 15))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("SVM Correlation Matrix")
plt.show()

